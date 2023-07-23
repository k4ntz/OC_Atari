"""
Demo script that allows me to find the game mode (the orientation of the
field) in Tennis
"""
import random
import matplotlib.pyplot as plt
# from copy import deepcopy
# from tqdm import tqdm
import numpy as np
import pandas as pd
import seaborn as sns
import pickle
import sys
# import pathlib
sys.path.insert(0, '../../ocatari') # noqa
from core import OCAtari

DROP_LOW = True
MIN_CORRELATION = 0.8

game_name = "TennisDeterministic-v0"
MODE = "vision"
RENDER_MODE = "human"
# RENDER_MODE = "rgb_array"
env = OCAtari(game_name, mode=MODE, render_mode=RENDER_MODE)
random.seed(0)

observation, info = env.reset()
# object_list = ["ball", "enemy", "player"]
# create dict of list
objects_infos = {}

# UNCOMMENT BELLOW TO CREATE THE DATA
# ram_saves = []
# mode = 0
# modes = []
# MODE_CHANGED = False
# for i in tqdm(range(800)):
#     obs, reward, terminated, truncated, info = env.step(random.randint(0, 5))
#     if info.get('frame_number') > 300 * 4 and i % 3 == 0 and not MODE_CHANGED:
#         mode = int(input("Enter actual field orientation (0 default)"))
#         if mode == 1:
#             MODE_CHANGED = True
#     ram = env._env.unwrapped.ale.getRAM()
#     ram_saves.append(deepcopy(ram))
#     modes.append(mode)
#         # env.render()
#
#     # modify and display render
# env.close()
# pickle.dump(np.array(ram_saves), open('dumps/ram_saves.pkl', 'wb'))
# pickle.dump(modes, open('dumps/modes.pkl', 'wb'))

ram_saves = pickle.load(open('../../dumps/ram_saves.pkl', 'rb'))
modes = pickle.load(open('../../dumps/modes.pkl', 'rb'))

objects_infos["mode"] = modes

ram_saves = np.array(ram_saves).T
from_rams = {str(i): ram_saves[i] for i in range(128) if not np.all(ram_saves[i] == ram_saves[i][0])}
objects_infos.update(from_rams)
df = pd.DataFrame(objects_infos)

# find correlation
METHOD = "spearman"
METHOD = "pearson"
corr = df.corr(method=METHOD)
# Reduce the correlation matrix
subset = ["mode"]

# Use submatrice
corr = corr[subset].T
corr.drop(subset, axis=1, inplace=True)

if DROP_LOW:
    corr = corr[corr.columns[[corr.abs().max() > MIN_CORRELATION]]]

ax = sns.heatmap(corr, vmin=-1, vmax=1, annot=True, cmap=sns.diverging_palette(20, 220, n=200))


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
        plt.scatter(x, y, marker="x")
        plt.xlabel(idx)
        plt.ylabel(el)
        plt.show()
