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
from ocatari.utils import parser, load_agent, make_deterministic
import pickle
from time import sleep


def ransac_regression(x, y):
    ransac = RANSACRegressor(estimator=LinearRegression(),
                             min_samples=15, max_trials=100,
                             loss='absolute_error', random_state=42,
                             residual_threshold=10)
    ransac.fit(np.array(x).reshape(-1, 1), y)
    return ransac.estimator_.coef_.item(), ransac.estimator_.intercept_.item()



parser.add_argument("-dqn", "--dqn", action="store_true", help="Use DQN agent")


opts = parser.parse_args()


DROP_LOW = True
MIN_CORRELATION = 0.6

NB_SAMPLES = 1000
game_name = "Centipede"
MODE = "vision"
RENDER_MODE = "human"
# RENDER_MODE = "rgb_array"
env = OCAtari(game_name, mode=MODE, render_mode=RENDER_MODE)
random.seed(0)

make_deterministic(0, env)

observation, info = env.reset()
object_list = ["Player"]
# object_list = ["ball", "enemy", "player"]
# create dict of list
objects_infos = {
    "player": []
                 }
subset = list(objects_infos.keys())

if opts.dqn:
    opts.game = game_name
    opts.path = f"models/{opts.game}/dqn.gz"
    dqn_agent = load_agent(opts, env.action_space.n)



ram_saves = []
for i in tqdm(range(NB_SAMPLES)):
    # obs, reward, terminated, truncated, info = env.step(random.randint(0, env.action_space.n-1))
    action = dqn_agent.draw_action(env.dqn_obs)
    # action = random.randint(0, env.nb_actions-1)
    obs, reward, terminated, truncated, info = env.step(action)
    ram = env._env.unwrapped.ale.getRAM()
    if ram[35] != 22:
        sleep(0.5)
    if i % 5 == 0:
        if str(env.objects).count("Player at") == 1:
            objects_infos["player"].append(1)
        elif str(env.objects).count("Player at") == 0:
            objects_infos["player"].append(0)
        else:
            continue
        ram_saves.append(deepcopy(ram))        

    # modify and display render
env.close()


ram_saves = np.array(ram_saves).T
from_rams = {str(i): ram_saves[i] for i in range(128) if not np.all(ram_saves[i] == ram_saves[i][0])}

objects_infos.update(from_rams)
df = pd.DataFrame(objects_infos)




pickle.dump(df, open("centipede2.pkl", "wb"))
# df = pickle.load(open("centipede2.pkl", "rb"))


# find correlation
METHOD = "spearman"
# METHOD = "kendall"
# METHOD = "pearson"
corr = df.corr(method=METHOD)
# Reduce the correlation matrix
# subset = objects_infos
# [f"{obj}_x" for obj in object_list] + [f"{obj}_y" for obj in object_list]

# Use submatrice
corr = corr[subset].T
import ipdb;ipdb.set_trace()
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
    keys = corrT[el].keys()
    for idx in range(len(keys)):
        maxval = corrT[el].abs()[keys[idx]]
        #idx = corrT[el].abs()
        if maxval >= 0.6:
            x, y = df[keys[idx]], df[el]
            # a, b = np.polyfit(x, y, deg=1)
            a, b = ransac_regression(x, y)
            plt.scatter(x, y, marker="x", alpha=10/len(x))
            plt.plot(x, a * x + b, color="k", lw=2.5)
            print(f"{el} = ({a:.2f} * ram_state[{keys[idx]}] + {b:.2f}) ")
            plt.xlabel(keys[idx])
            plt.ylabel(el)
            plt.show()
