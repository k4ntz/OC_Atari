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
game_name = "RiverraidNoFrameskip-v4"
MODE = "vision"
RENDER_MODE = "human"
RENDER_MODE = "rgb_array"
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

snapshot = pickle.load(open("riverplane.pkl", "rb"))
env._env.env.env.ale.restoreState(snapshot)

base_next_obs, _, _, _, _ = env.step(0)

# MAX_DIFF = 200

for ram_n in range(128):
    for i in range(255):
        env._env.env.env.ale.restoreState(snapshot)
        original_ram = env.get_ram()[ram_n]
        env.set_ram(ram_n, i)
        resulting_obs, _, _, _, _ = env.step(0)
        im_diff = resulting_obs - base_next_obs
        nb_diff = np.sum(resulting_obs != base_next_obs) // 3
        if 0 < nb_diff:
            fig, axes = plt.subplots(1, 3)
            for ax, im in zip(axes, [base_next_obs, resulting_obs, im_diff]):
                ax.imshow(im)
            plt.suptitle(f"{ram_n} set to {i} (instead of {original_ram})", fontsize=20)
            plt.show()
            break