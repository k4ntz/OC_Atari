"""
Demo script that allows to find the correlation between ram states and
detected objects through vision in a specified game.
"""

# appends parent path to syspath to make ocatari importable
# like it would have been installed as a package
import ipdb
import sys
import random
import matplotlib.pyplot as plt
from copy import deepcopy
from tqdm import tqdm
import numpy as np
import pandas as pd
import seaborn as sns
from sklearn.linear_model import RANSACRegressor, LinearRegression
from os import path
import pathlib
sys.path.append(path.dirname(path.dirname(path.abspath(__file__))))  # noqa
from ocatari.core import OCAtari
from ocatari.utils import parser, load_agent, make_deterministic
import pickle
from time import sleep


def binarize(ram):
    return np.unpackbits(ram).astype(int)


def ransac_regression(x, y):
    ransac = RANSACRegressor(estimator=LinearRegression(),
                             min_samples=15, max_trials=100,
                             loss='absolute_error', random_state=42,
                             residual_threshold=10)
    ransac.fit(np.array(x).reshape(-1, 1), y)
    return ransac.estimator_.coef_.item(), ransac.estimator_.intercept_.item()


parser.add_argument("-g", "--game", type=str, required=True,
                    help="game to evaluate (e.g. 'Pong')")
parser.add_argument("-to", "--tracked_objects", type=str, default=["Player"], nargs='+',
                    help="A list of objects to track")
parser.add_argument("-tp", "--tracked_properties", type=str, default=['x', 'y'], nargs='+',
                    help="A list of properties to track for each object")
parser.add_argument("-tn", "--top_n", type=int, default=3,
                    help="The top n value to be kept in the correlation matrix")
parser.add_argument("-ns", "--nb_samples", type=int, default=1000,
                    help="The number of samples to use.")
parser.add_argument("-dqn", "--dqn", action="store_true", help="Use DQN agent")
parser.add_argument("-s", "--seed", default=0,
                    help="Seed to make everything deterministic")
parser.add_argument("-r", "--render", action="store_true",
                    help="If provided, renders")
parser.add_argument("-m", "--method", type=str, default="pearson", choices={"pearson", "spearman", "kendall"},
                    help="The method to use for computing the correlation")
parser.add_argument("-snap", "--snapshot", type=str, default=None,
                    help="Path to an emulator state snapshot to start from.")
parser.add_argument("-hud", "--hud", action="store_true",
                    help="Track HUD objects")
parser.add_argument("-b", "--binary", action="store_true",
                    help="Convert RAMs to binary")
parser.add_argument("-pr", "--presence", action="store_true",
                    help="Track presence/absence of objects")
opts = parser.parse_args()

if opts.binary:
    _convert = binarize
else:
    def _convert(x): return x

MODE = "vision"
if opts.render:
    RENDER_MODE = "human"
else:
    RENDER_MODE = "rgb_array"
env = OCAtari(opts.game, mode=MODE, render_mode=RENDER_MODE, hud=opts.hud)

make_deterministic(opts.seed, env)

observation, info = env.reset()
if opts.snapshot:
    snapshot = pickle.load(open(opts.snapshot, "rb"))
    env._env.env.env.ale.restoreState(snapshot)

tracked_objects_infos = {}
if opts.presence:
    for objname in opts.tracked_objects:
        tracked_objects_infos[f"{objname}.is_present"] = []
else:
    for objname in opts.tracked_objects:
        for prop in opts.tracked_properties:
            tracked_objects_infos[f"{objname}.{prop}"] = []

subset = list(tracked_objects_infos.keys())

if opts.dqn:
    opts.game = opts.game
    opts.path = f"models/{opts.game}/dqn.gz"
    try:
        dqn_agent = load_agent(opts, env.action_space.n)
    except FileNotFoundError:
        oc_atari_dir = pathlib.Path(__file__).parents[1].resolve()
        opts.path = str(oc_atari_dir / 'models' / f"{opts.game}" / 'dqn.gz')
        dqn_agent = load_agent(opts, env.action_space.n)


ram_saves = []
for i in tqdm(range(opts.nb_samples*5)):
    # obs, reward, terminated, truncated, info = env.step(random.randint(0, env.action_space.n-1))
    if opts.dqn:
        action = dqn_agent.draw_action(env.dqn_obs)
    else:
        action = random.randint(0, env.nb_actions-1)
    obs, reward, terminated, truncated, info = env.step(action)
    ram = env.get_ram()
    if random.random() < 1/5:  # every 5 frames
        save = True
        if opts.presence:
            for objstr in opts.tracked_objects:
                tracked_objects_infos[f"{objstr}.is_present"].append(
                    str(env.objects).count(f"{objstr} at"))
            ram_saves.append(deepcopy(_convert(ram)))
            continue
        for objstr in opts.tracked_objects:
            if str(env.objects).count(f"{objstr} at") != 1:
                save = False  # don't save anything
        if not save:
            continue
        for obj in env.objects:
            objname = obj.category
            if objname in opts.tracked_objects:
                for prop in opts.tracked_properties:
                    tracked_objects_infos[f"{objname}.{prop}"].append(
                        obj.__getattribute__(prop))
        ram_saves.append(deepcopy(_convert(ram)))
    if terminated or truncated:
        observation, info = env.reset()
        if opts.snapshot:
            env._env.env.env.ale.restoreState(snapshot)

    # modify and display render
env.close()


ipdb.set_trace()

ram_saves = np.array(ram_saves).T
from_rams = {str(i): ram_saves[i] for i in range(
    128) if not np.all(ram_saves[i] == ram_saves[i][0])}

tracked_objects_infos.update(from_rams)
df = pd.DataFrame(tracked_objects_infos)


# find correlation
corr = df.corr(method=opts.method)
# Reduce the correlation matrix
# subset = tracked_objects_infos
# [f"{obj}_x" for obj in opts.tracked_objects] + [f"{obj}_y" for obj in opts.tracked_objects]
print("-"*20)
for el, onlynans in corr.isna().all(axis=1).items():
    if onlynans:
        print(
            f"Only NaNs found for {el} in the correlation matrix, most probably fix attribute.")
print("-"*20)
# Use submatrice
corr = corr[subset].T
corr.drop(subset, axis=1, inplace=True)

if opts.top_n:
    print(f"Filtering, keeping only top {opts.top_n} correlated elements")
    # corr = corr[corr.columns[[corr.abs().max() > MIN_CORRELATION]]]
    to_keep = []
    for index, row in corr.iterrows():
        au_corr = row.to_frame().abs().unstack().sort_values(ascending=False)
        au_corr = au_corr[0:opts.top_n].dropna()
        to_keep.extend([key[1]
                       for key in au_corr.keys() if key[1] not in to_keep])
    corr = corr[to_keep]


# if opts.method == "pearson":
ax = sns.heatmap(corr, vmin=-1, vmax=1, annot=True,
                 cmap=sns.diverging_palette(20, 220, n=200))
# else:
#     ax = sns.heatmap(corr, vmin=0, vmax=1, annot=True, cmap=sns.diverging_palette(20, 220, n=200))
# ax.set_yticklabels(ax.get_yticklabels(), rotation=90, horizontalalignment='right')


for tick in ax.get_yticklabels():
    tick.set_rotation(0)

xlabs = corr.columns.to_list()
plt.xticks(list(np.arange(0.5, len(xlabs) + .5, 1)), xlabs)
plt.title(opts.game)
plt.show()


print("-"*20)
print("Finding relashionshinps using RANSAC regression")
corrT = corr.T
for el in corrT:
    keys = corrT[el].keys()
    for idx in range(len(keys)):
        maxval = corrT[el].abs()[keys[idx]]
        # idx = corrT[el].abs()
        if maxval >= 0.6:
            x, y = df[keys[idx]], df[el]
            xys = pd.DataFrame({'x': x, 'y': y})
            # a, b = np.polyfit(x, y, deg=1)
            a, b = ransac_regression(x, y)
            for (xp, yp), sp in xys.value_counts(normalize=True).items():
                plt.scatter(xp, yp, marker="x", color="b", s=500*sp)
            if b >= 0:
                formulae = f"{el} = {a:.2f} * ram_state[{keys[idx]}] + {b:.2f} "
            else:
                formulae = f"{el} = {a:.2f} * ram_state[{keys[idx]}] - {-b:.2f} "
            print(formulae)
            plt.plot(x, a * x + b, color="k", lw=2.5, alpha=0.3)
            plt.title(formulae)
            plt.xlabel(keys[idx])
            plt.ylabel(el)
            plt.show()
