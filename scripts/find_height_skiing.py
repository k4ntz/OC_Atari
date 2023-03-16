# appends parent path to syspath to make ocatari importable
# like it would have been installed as a package
import sys
from os import path
sys.path.append(path.dirname(path.dirname(path.abspath(__file__))))

import random
import matplotlib.pyplot as plt
from ocatari.core import OCAtari
from ocatari.vision.utils import mark_bb, make_darker
from ocatari.vision.skiing import objects_colors
from ocatari.utils import load_agent, parser
from copy import deepcopy
import numpy as np
import pickle
import pandas as pd
import seaborn as sns
from sklearn.linear_model import RANSACRegressor, LinearRegression


def ransac_regression(x, y):
    ransac = RANSACRegressor(estimator=LinearRegression(),
                             min_samples=10, max_trials=100,
                             loss='absolute_error', random_state=42,
                             residual_threshold=10)
    ransac.fit(np.array(x).reshape(-1, 1), y)
    return ransac.estimator_.coef_.item(), ransac.estimator_.intercept_.item()

game_name = "Skiing"
MODE = "vision"
MODE = "revised"
env = OCAtari(game_name, mode=MODE, render_mode='rgb_array')
# env = OCAtari(game_name, mode=MODE, render_mode='human')
observation, info = env.reset()
prevRam = None
already_figured_out = []

opts = parser.parse_args()

if opts.path:
    agent = load_agent(opts, env.action_space.n)

opts = parser.parse_args()

if opts.path:
    agent = load_agent(opts, env.action_space.n)


def show_detected_objects(obs, info):
    if "objects" in info:
        print("True")
        for obj_name, oinfo in info["objects"].items():
            opos = oinfo[:4]
            ocol = oinfo[4:]
            print(obj_name, ":", oinfo)
            if MODE == "vision":
                ocol = objects_colors[obj_name]
            sur_col = make_darker(ocol)
            mark_bb(obs, opos, color=sur_col)
            # mark_point(obs, *opos[:2], color=(255, 255, 0))
    print("-"*30, end="")
    plt.imshow(obs)
    plt.tight_layout()
    plt.show()

sizes = []
ram_states = []
for i in range(100):
    if opts.path is not None:
        action = agent.draw_action(env.dqn_obs)
    else:
        action = random.randint(0, 2)
        action = 0
    obs, reward, terminated, truncated, info = env.step(action)
    # if i > 60 and i % 1 == 0:
    if "size" in info:
        show_detected_objects(obs, info)
        print(i)
        ymax = input("Please ymax:")
        if ymax:
            sizes.append(int(ymax))
            ram = env._env.unwrapped.ale.getRAM()
            ram_states.append(deepcopy(ram))
    if terminated or truncated:
        observation, info = env.reset()
    # modify and display render
env.close()
pickle.dump(ram_states, open('dumps/ram_saves_sc.pkl', 'wb'))
pickle.dump(sizes, open('dumps/sizes.pkl', 'wb'))



ram_states = pickle.load(open('dumps/ram_saves_sc.pkl', 'rb'))
sizes = pickle.load(open('dumps/sizes.pkl', 'rb'))

objects_infos = {}
ram_saves = np.array(ram_states).T
from_rams = {str(i): ram_saves[i] for i in range(128) if not np.all(ram_saves[i] == ram_saves[i][0])}
objects_infos["ymax"] = sizes
objects_infos.update(from_rams)
df = pd.DataFrame(objects_infos)

# find correlation
METHOD = "spearman"
# METHOD = "kendall"
METHOD = "pearson"
corr = df.corr(method=METHOD)
# Reduce the correlation matrix
subset = ["ymax"]

# Use submatrice
corr = corr[subset].T
corr.drop(subset, axis=1, inplace=True)
DROP_LOW = False
MIN_CORRELATION = 0.6
# import ipdb; ipdb.set_trace()
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
import ipdb; ipdb.set_trace()
for el in ["32", "90"]:
    # maxval = corrT[el].abs().max()
    idx = corr[el].abs().idxmax()
    if True:
        x, y = df[idx], df[el]
        a, b = ransac_regression(x, y)
        plt.plot(x, a * x + b, color="k", lw=2.5)
        plt.scatter(x, y, marker="x")
        plt.xlabel(idx)
        plt.ylabel(el)
        plt.show()

# for el in corrT:
#     maxval = corrT[el].abs().max()
#     idx = corrT[el].abs().idxmax()
#     if maxval > 0.9:
#         x, y = df[idx], df[el]
#         # a, b = np.polyfit(x, y, deg=1)
#         plt.scatter(x, y, marker="x")
#         plt.plot(x, a * x + b, color="k", lw=2.5)
#         print(f"{el} = {a:.2f} x ram[{idx}] + {b:.2f} ")
#         plt.xlabel(idx)
#         plt.ylabel(el)
#         plt.show()
