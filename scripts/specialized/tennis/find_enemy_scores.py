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
import ipdb
import sys
# import pathlib
sys.path.insert(0, '../../ocatari') # noqa
from core import OCAtari

DROP_LOW = True
MIN_CORRELATION = 0.5

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

#  ### UNCOMMENT BELLOW TO CREATE THE DATA
ram_saves = []
mode = 0
modes = []
MODE_CHANGED = False
# for i in tqdm(range(600)):
#     obs, reward, terminated, truncated, info = env.step(random.randint(0, 5))
#     if i > 0 and i % 40 == 0:
#         mode = int(input("Enter actual enemy score"))
#         ram = env._env.unwrapped.ale.getRAM()
#         ram_saves.append(deepcopy(ram))
#         modes.append(mode)
#
#     # modify and display render
# env.close()
# pickle.dump(np.array(ram_saves), open('dumps/ram_saves_sc.pkl', 'wb'))
# pickle.dump(modes, open('dumps/scores.pkl', 'wb'))


ram_saves = pickle.load(open('../../dumps/ram_saves_sc.pkl', 'rb'))
modes = pickle.load(open('../../dumps/scores.pkl', 'rb'))

objects_infos["scores"] = modes

ram_saves = np.array(ram_saves).T
from_rams = {str(i): ram_saves[i] for i in range(128) if not np.all(ram_saves[i] == ram_saves[i][0])}
objects_infos.update(from_rams)
df = pd.DataFrame(objects_infos)

# find correlation
METHOD = "spearman"
# METHOD = "pearson"
corr = df.corr(method=METHOD)
# Reduce the correlation matrix
subset = ["scores"]

# Use submatrice
corr = corr[subset].T
corr.drop(subset, axis=1, inplace=True)

# if DROP_LOW:
#     corr = corr[corr.columns[[corr.abs().max() > MIN_CORRELATION]]]

ax = sns.heatmap(corr, vmin=-1, vmax=1, annot=True, cmap=sns.diverging_palette(20, 220, n=200))

ipdb.set_trace()

for tick in ax.get_yticklabels():
    tick.set_rotation(0)

xlabs = corr.columns.to_list()
plt.xticks(list(np.arange(0.5, len(xlabs) + .5, 1)), xlabs)
plt.title(game_name)
plt.show()

corrT = corr
for el in ["6", "72", "70"]:
    maxval = corrT[el].abs().max()
    idx = corrT[el].abs().idxmax()
    if True:
        x, y = df[idx], df[el]
        plt.scatter(x, y, marker="x")
        plt.xlabel(idx)
        plt.ylabel(el)
        plt.show()
