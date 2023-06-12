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
from utils import load_agent, parser


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

opts = parser.parse_args()

agent = load_agent(opts, env.action_space.n)


#  ### UNCOMMENT BELLOW TO CREATE THE DATA
# ram_saves = []
# mode = 0
# modes = []
# last_sc = 0
# for i in tqdm(range(600)):
#     if opts.path is not None:
#         action = agent.draw_action(env.dqn_obs)
#     else:
#         action = random.randint(0, 5)
#     obs, reward, terminated, truncated, info = env.step(action)
#     if i > 0 and i % 20 == 0:
#         inp = input("Please provide current player score: ")
#         if len(inp) == 0:
#             sc = last_sc
#             print(f"Using last score {last_sc} as current score")
#         else:
#             sc = int(inp)
#             last_sc = sc
#         ram = env._env.unwrapped.ale.getRAM()
#         ram_saves.append(deepcopy(ram))
#         modes.append(sc)
# #   #### modify and display render
# env.close()
# pickle.dump(np.array(ram_saves), open('dumps/ram_saves_psc.pkl', 'wb'))
# pickle.dump(modes, open('dumps/scoresp.pkl', 'wb'))


ram_saves = pickle.load(open('dumps/ram_saves_psc.pkl', 'rb'))
modes = pickle.load(open('dumps/scoresp.pkl', 'rb'))

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

if DROP_LOW:
    corr = corr[corr.columns[[corr.abs().max() > MIN_CORRELATION]]]

ax = sns.heatmap(corr, vmin=-1, vmax=1, annot=True, cmap=sns.diverging_palette(20, 220, n=200))


for tick in ax.get_yticklabels():
    tick.set_rotation(0)

xlabs = corr.columns.to_list()
plt.xticks(list(np.arange(0.5, len(xlabs) + .5, 1)), xlabs)
plt.title(game_name)
plt.show()


corrT = corr
for el in ["69"]:
    maxval = corrT[el].abs().max()
    idx = corrT[el].abs().idxmax()
    if True:
        x, y = df[idx], df[el]
        plt.scatter(x, y, marker="x")
        plt.xlabel(idx)
        plt.ylabel(el)
        plt.show()
