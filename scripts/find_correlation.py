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
from core import OCAtari


def ransac_regression(x, y):
    ransac = RANSACRegressor(estimator=LinearRegression(),
                             min_samples=50, max_trials=100,
                             loss='absolute_error', random_state=42,
                             residual_threshold=10)
    ransac.fit(np.array(x).reshape(-1, 1), y)
    return ransac.estimator_.coef_.item(), ransac.estimator_.intercept_.item()


DROP_LOW = True
MIN_CORRELATION = 0.8

game_name = "TennisDeterministic-v0"
# game_name = "PongDeterministic-v0"
MODE = "vision"
RENDER_MODE = "human"
RENDER_MODE = "rgb_array"
env = OCAtari(game_name, mode=MODE, render_mode=RENDER_MODE)
random.seed(0)

observation, info = env.reset()
object_list = ["ball", "enemy", "player", "ball_shadow"]
# object_list = ["ball", "enemy", "player"]
# create dict of list
objects_infos = {}
for obj in object_list:
    objects_infos[f"{obj}_x"] = []
    objects_infos[f"{obj}_y"] = []
ram_saves = []
for i in tqdm(range(600)):
    obs, reward, terminated, truncated, info = env.step(random.randint(0, 5))
    if info.get('frame_number') > 10 and i % 3 == 0:
        SKIP = False
        for obj_name in object_list:  # avoid state without the tracked objects
            if obj_name not in info["objects"]:
                SKIP = True
                break
        if SKIP:
            continue
        for obj_name in object_list:
            oinfo = info["objects"][obj_name]
            objects_infos[f"{obj_name}_x"].append(oinfo[0])
            objects_infos[f"{obj_name}_y"].append(oinfo[1])
        ram = env._env.unwrapped.ale.getRAM()
        ram_saves.append(deepcopy(ram))
        # env.render()

    # modify and display render
env.close()

import ipdb # noqa

ipdb.set_trace()

ram_saves = np.array(ram_saves).T
from_rams = {str(i): ram_saves[i] for i in range(128) if not np.all(ram_saves[i] == ram_saves[i][0])}
objects_infos.update(from_rams)
df = pd.DataFrame(objects_infos)

# find correlation
METHOD = "spearman"
# METHOD = "kendall"
METHOD = "pearson"
corr = df.corr(method=METHOD)
# Reduce the correlation matrix
subset = [f"{obj}_x" for obj in object_list] + [f"{obj}_y" for obj in object_list]

# Use submatrice
corr = corr[subset].T
corr.drop(subset, axis=1, inplace=True)

if DROP_LOW:
    corr = corr[corr.columns[[corr.abs().max() > MIN_CORRELATION]]]

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
