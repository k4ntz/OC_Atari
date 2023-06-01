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
import pickle


def ransac_regression(x, y):
    ransac = RANSACRegressor(estimator=LinearRegression(),
                             min_samples=6, max_trials=100,
                             loss='absolute_error', random_state=42,
                             residual_threshold=10)
    ransac.fit(np.array(x).reshape(-1, 1), y)
    return ransac.estimator_.coef_.item(), ransac.estimator_.intercept_.item()


DROP_LOW = True
MIN_CORRELATION = 0.4

NB_SAMPLES = 420
game_name = "Riverraid-v4"
MODE = "vision"
RENDER_MODE = "human"
# RENDER_MODE = "rgb_array"
env = OCAtari(game_name, mode=MODE, render_mode=RENDER_MODE)
random.seed(0)

make_deterministic(0, env)

observation, info = env.reset()
# object_list = ["Projectile"]
object_list = ["Fuel"]
# create dict of list
objects_infos = {}
subset = []
# for obj in object_list:
#     objects_infos[f"{obj}_x"] = []
#     objects_infos[f"{obj}_y"] = []
#     subset.append(f"{obj}_x")
#     subset.append(f"{obj}_y")
for i in range(1):
    objects_infos[f"fuel_x"] = []
    subset.append(f"fuel_x")
    objects_infos[f"fuel_y"] = []
    subset.append(f"fuel_y")
ram_saves = []
actions = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
class Options(object):
    pass
opts = Options()
opts.path = "models/Riverraid/dqn.gz"
dqn_agent = load_agent(opts, env.action_space.n)

snapshot = pickle.load(open("riverraid.pkl", "rb"))
env._env.env.env.ale.restoreState(snapshot)

for i in tqdm(range(NB_SAMPLES)):
    # obs, reward, terminated, truncated, info = env.step(random.randint(0, env.action_space.n-1))
    action = dqn_agent.draw_action(env.dqn_obs)
    # action = 0
    # if i % 120 == 0:
    #     action = 1
    # for i, val in enumerate([0, 0, 0, 0, 0, 7]):
    #     env.set_ram(32+i, val)
    obs, reward, terminated, truncated, info = env.step(action)
    # print(env.get_ram()[21], info.get('frame_number'))
    SKIP = True
    if i > 200 and i % 1 == 0:
        
        if str(env.objects).count("Jet") == 1:
            for obj in env.objects:
                if obj.category == "Jet":
                    objects_infos[f"fuel_x"].append(obj.xy[0])
                    objects_infos[f"fuel_y"].append(obj.xy[1])
                    ram = env._env.unwrapped.ale.getRAM()
                    ram_saves.append(deepcopy(ram))
                    break
        # if str(env.objects).count("Fuel") < 3:
        #     SKIP = False
        # if SKIP:
        #     prevy = None
        #     continue
        # sortedy = sorted(env.objects, key=lambda o:o.xy[1])
        # print(sortedy)
        # for i, obj in enumerate(sortedy):
        #     if "Fuel" in obj.category and (env.get_ram()[37] == 10):
        #         print(True)
        #         objects_infos[f"fuel_x"].append(obj.xy[0])
        #         objects_infos[f"fuel_y"].append(obj.xy[1])
        #         ram = env._env.unwrapped.ale.getRAM()
        #         ram_saves.append(deepcopy(ram))
        #         break
            # n += 1
        env.render()

    # modify and display render
env.close()

# import ipdb; ipdb.set_trace()

print(len(ram_saves))

ram_saves = np.array(ram_saves).T
from_rams = {str(i): ram_saves[i] for i in range(128) if not np.all(ram_saves[i] == ram_saves[i][0])}
objects_infos.update(from_rams)
df = pd.DataFrame(objects_infos)

# df["sum"] = df["Projectile_1_y"] + df["Projectile_2_y"]
# df["diff"] = df["Projectile_1_y"] - df["Projectile_2_y"]
# subset.append("sum")
# subset.append("diff")
# print(np.array(objects_infos['Projectile_1_y']) > np.array(objects_infos['Projectile_2_y']))


# find correlation
METHOD = "spearman"
# METHOD = "kendall"
METHOD = "pearson"
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
    for idx, val in corrT[el].items():
        # maxval = corrT[el].abs().max()
        # idx = corrT[el].abs().idxmax()
        if abs(val) > 0.4:
            x, y = df[idx], df[el]
            # a, b = np.polyfit(x, y, deg=1)
            a, b = ransac_regression(x, y)
            plt.scatter(x, y, marker="x")
            plt.plot(x, a * x + b, color="k", lw=2.5)
            print(f"{el} = {a:.2f} x ram[{idx}] + {b:.2f} ")
            plt.xlabel(idx)
            plt.ylabel(el)
            plt.show()

