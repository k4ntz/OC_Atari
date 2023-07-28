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
import pickle
from ocatari.utils import load_agent, parser, make_deterministic


parser.add_argument("-dqn", "--dqn", action="store_true", help="Use DQN agent")
opts = parser.parse_args()

def ransac_regression(x, y):
    ransac = RANSACRegressor(estimator=LinearRegression(),
                             min_samples=50, max_trials=100,
                             loss='absolute_error', random_state=42,
                             residual_threshold=10) 
    ransac.fit(np.array(x).reshape(-1, 1), y)
    return ransac.estimator_.coef_.item(), ransac.estimator_.intercept_.item()


DROP_LOW = True
MIN_CORRELATION = 0.8 #0.8

NB_SAMPLES = 600# 600 before
game_name = "YarsRevenge" #RoadRunner-v4
MODE = "vision"
RENDER_MODE = "human"
# RENDER_MODE = "rgb_array"
env = OCAtari(game_name, mode=MODE, render_mode=RENDER_MODE,hud=True)
random.seed(0)
observation, info = env.reset()
# snapshot = pickle.load(open("/home/anurag/Desktop/HiWi_OC/OC_Atari/roadrunner_level5.pkl", "rb"))
# env._env.env.env.ale.restoreState(snapshot)
if opts.dqn:
    opts.path = f"models/RoadRunner/dqn.gz"
    dqn_agent = load_agent(opts, env.action_space.n)
# object_list = ["Projectile"]
object_list = ["Shield_Block"]
# create dict of list
objects_infos = {}
subset = []
for obj in object_list:
    objects_infos[f"{obj}_x"] = []
    objects_infos[f"{obj}_y"] = []
    subset.append(f"{obj}_x")
    subset.append(f"{obj}_y")
ram_saves = []
actions = [0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]

for i in tqdm(range(NB_SAMPLES)):
    # obs, reward, terminated, truncated, info = env.step(random.randint(0, env.action_space.n-1))
    action = actions[i%len(actions)]
    prob = random.random()
    if prob > 0.8:
        action = 1 #fire
    elif prob > 0.7:
        action = 2 
    else:
        action = 4 # 4-RIGHT 3- Left, Truck at (56, 129), (16, 18), Cactus at (125, 55), (8, 8), Cactus at (129, 46), (8, 8)]
    # if i % 5: # reset for pressing
    #     action = 0
    # action = dqn_agent.draw_action(env.dqn_obs)
    obs, reward, terminated, truncated, info = env.step(action)
    if info.get('frame_number') > 10 and i % 1 == 0:
        SKIP = False
        # print(env.objects)
        print(env.objects)
        for obj_name in object_list:  # avoid state without the tracked objects
            if str(env.objects).count(obj_name) != 1:
                SKIP = True
                break
        # if str(env.objects).count("Projectile at (75,") == 0:
        #     print(env._env.unwrapped.ale.getRAM()[106])
        if SKIP:# or env.objects[-2].y < env.objects[-1].y:
            continue
        for obj in env.objects:
            objname = obj.category
            if objname in object_list:
                objects_infos[f"{objname}_x"].append(obj.xy[0])
                objects_infos[f"{objname}_y"].append(obj.xy[1])
            # n += 1
        ram = env._env.unwrapped.ale.getRAM()
        ram_saves.append(deepcopy(ram))
        # env.render()

    # modify and display render
env.close()


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
    maxval = corrT[el].abs().max()
    idx = corrT[el].abs().idxmax()
    if maxval > 0.9:
        x, y = df[idx], df[el]
        # a, b = np.polyfit(x, y, deg=1)
        a, b = ransac_regression(x, y)
        plt.scatter(x, y, marker="x")
        plt.plot(x, a * x + b, color="k", lw=2.5)
        print(f"{el} = {a:.2f} x ram[{idx}] + {b:.2f} ")
        plt.xlabel(idx)
        plt.ylabel(el)
        plt.show()