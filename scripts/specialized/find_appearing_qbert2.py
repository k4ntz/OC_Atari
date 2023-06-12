"""
Demo script that allows me to find the correlation between ram states and
detected objects through vision in Tennis
"""

# appends parent path to syspath to make ocatari importable
# like it would have been installed as a package
import sys
import random
import matplotlib.pyplot as plt
from copy import deepcopy
from tqdm import tqdm
import numpy as np
import pandas as pd
import seaborn as sns
from sklearn.linear_model import RANSACRegressor, LinearRegression
sys.path.insert(0, '../ocatari') # noqa
from ocatari.core import OCAtari
from alive_progress import alive_bar
from ocatari.utils import load_agent, make_deterministic
from time import sleep


def ransac_regression(x, y):
    ransac = RANSACRegressor(estimator=LinearRegression(),
                             min_samples=10, max_trials=100,
                             loss='absolute_error', random_state=42,
                             residual_threshold=10)
    ransac.fit(np.array(x).reshape(-1, 1), y)
    return ransac.estimator_.coef_.item(), ransac.estimator_.intercept_.item()


DROP_LOW = True
MIN_CORRELATION = 0.5

NB_SAMPLES = 1200
game_name = "Qbert-v4"
MODE = "vision"
RENDER_MODE = "human"
# RENDER_MODE = "rgb_array"
env = OCAtari(game_name, mode=MODE, render_mode=RENDER_MODE)
random.seed(0)

make_deterministic(0, env)

observation, info = env.reset()
# object_list = ["Projectile"]
# object_list = ["GreenBall", "PurpleBall"]
object_list = ["PurpleBall"]
# create dict of list
objects_infos = {}
subset = []
for obj in object_list:
    objects_infos[f"{obj}_x"] = []
    subset.append(f"{obj}_x")
    # objects_infos[f"{obj}_y"] = []
    # subset.append(f"{obj}_y")
ram_saves = []
actions = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
actions = ([5] * 18 + [4] * 5) * 4 + 50 * [3]
class Options(object):
    pass
opts = Options()
opts.path = "models/QBert/dqn.gz"
dqn_agent = load_agent(opts, env.action_space.n)

_cubes_cinfo=[        21,               # row of 1
                    52,  54,            # row of 2
                 83, 85,  87,           # row of 3
               98, 100, 102, 104,       # row of 4
              1,  3,   5,   7,  9,      # row of 5
            32, 34, 36,  38,  40, 42]   # row of 6

to_exclude = _cubes_cinfo + [112, 122]  # disks


was_here = False
ram_saves.append(env._env.unwrapped.ale.getRAM())
potentials = set(np.arange(128))
previous = None
for i in tqdm(range(NB_SAMPLES)):
# for i in range(NB_SAMPLES):
    # obs, reward, terminated, truncated, info = env.step(random.randint(0, env.action_space.n-1))
    action = dqn_agent.draw_action(env.dqn_obs)
    # action = random.randint(1, 5)
    # action = actions[i%len(actions)]
    # env.set_ram(112, 93)
    # env.set_ram(122, 93)
    obs, reward, terminated, truncated, info = env.step(action)
    ram = env._env.unwrapped.ale.getRAM()
    # print(ram[75:80])
    env.set_ram(119, 5) # no purple
    if i % 300 == 0:
        env.set_ram(103, 17)
    if i % 40:
        env.set_ram(105, 5) # no peer
    # print(ram[103])
    # if i > 100:
    #     sleep(0.1)
    if i > 0 and i % 1 == 0:
        SKIP = False
        if terminated:
            env.reset()
        for obj_name in object_list:  # avoid state without the tracked objects
            if str(env.objects).count("GreenBall") == 0 and str(env.objects).count("PurpleBall") == 1:
                print(ram[75:80])
                sleep(0.5)
                pass
                # import ipdb; ipdb.set_trace()
                # if previous is not None:
                # previous = deepcopy(ram)
                # import ipdb; ipdb.set_trace()
            #     objects_infos[f"{obj_name}"].append(1) # appeared
            #     ram_saves.append(deepcopy(ram))
            #     was_here = True
            # elif str(env.objects).count(obj_name) == 1 and was_here:
            #     objects_infos[f"{obj_name}"].append(0)
            #     ram_saves.append(deepcopy(ram))
            else:
                # was_here = False
                SKIP = True
                prev_x = None
        if SKIP:
            continue
        for obj in env.objects:
            obj_name = obj.category
            if obj_name in object_list:
                if prev_x is not None and abs(obj.xy[0] - prev_x):
                    objects_infos[f"{obj_name}_x"].append(obj.xy[0] - prev_x)
                    ram_saves.append(deepcopy(ram))
                    # objects_infos[f"{obj_name}_y"].append(obj.xy[1])
                # objects_infos[f"{obj_name}_y"].append(obj.xy[1])
                prev_x = obj.xy[0]
        
        # ram_saves.append(deepcopy(ram))
env.close()

ram_saves.pop(-1)

import ipdb; ipdb.set_trace()

ram_saves = np.array(ram_saves).T
from_rams = {str(i): ram_saves[i] for i in range(128) if not np.all(ram_saves[i] == ram_saves[i][0]) and i not in to_exclude}
objects_infos.update(from_rams)
df = pd.DataFrame(objects_infos)

# df["sum"] = df["Projectile_1_y"] + df["Projectile_2_y"]
# df["diff"] = df["Projectile_1_y"] - df["Projectile_2_y"]
# subset.append("sum")
# subset.append("diff")
# print(np.array(objects_infos['Projectile_1_y']) > np.array(objects_infos['Projectile_2_y']))


# find correlation
# METHOD = "kendall"
# METHOD = "pearson"
METHOD = "spearman"
corr = df.corr(method=METHOD)
# Reduce the correlation matrix
# subset = objects_infos
# [f"{obj}_x" for obj in object_list] + [f"{obj}_y" for obj in object_list]

# Use submatrice
corr = corr[subset].T
corr.drop(subset, axis=1, inplace=True)

if DROP_LOW:
    # corr = corr[corr.columns[[corr.abs().max() > MIN_CORRELATION]]]
    corr = corr.loc[:, (corr.abs() > MIN_CORRELATION).any()]

# if METHOD == "pearson":
ax = sns.heatmap(corr, vmin=-1, vmax=1, annot=True, cmap=sns.diverging_palette(20, 220, n=200))
# else:
#     ax = sns.heatmap(corr, vmin=0, vmax=1, annot=True, cmap=sns.diverging_palette(20, 220, n=200))
# ax.set_yticklabels(ax.get_yticklabels(), rotation=90, horizontalalignment='right')


for tick in ax.get_yticklabels():
    tick.set_rotation(0)

xlabs = corr.columns.to_list()
plt.xticks(list(np.arange(0.5, len(xlabs) + .5, 1)), xlabs)
plt.title(game_name)
plt.show()

# import ipdb;ipdb.set_trace()


corrT = corr.T
for el in corrT:
    maxval = corrT[el].abs().max()
    idx = corrT[el].abs().idxmax()
    x, y = df[idx], df[el]
    # a, b = np.polyfit(x, y, deg=1)
    a, b = ransac_regression(x, y)
    plt.scatter(x, y, alpha=0.2)
    plt.plot(x, a * x + b, color="k", lw=2.5)
    print(f"{el} = {a:.2f} x ram[{idx}] + {b:.2f} ")
    plt.xlabel(idx)
    plt.ylabel(el)
    plt.show()

