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



game_name = "Gopher-v4"
MODE = "vision"
RENDER_MODE = "human"
RENDER_MODE = "rgb_array"
env = OCAtari(game_name, mode=MODE, render_mode=RENDER_MODE)
random.seed(0)



ONE_CHANGE = True
initial_ram_n = 30


make_deterministic(0, env)

get_bin = lambda x: format(int(x), 'b').zfill(8)


observation, info = env.reset()
# object_list = ["Projectile"]
object_list = ["AcmeMine"]
# create dict of list
objects_infos = {}
subset = []
# for obj in object_list:
#     objects_infos[f"{obj}_x"] = []
#     objects_infos[f"{obj}_y"] = []
#     subset.append(f"{obj}_x")
#     subset.append(f"{obj}_y")
for i in range(1):
    objects_infos[f"AcmeMine_x"] = []
    subset.append(f"AcmeMine_x")
    objects_infos[f"AcmeMine_y"] = []
    subset.append(f"AcmeMine_y")
ram_saves = []
actions = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
class Options(object):
    pass
opts = Options()
opts.path = "models/Gopher/dqn.gz"
dqn_agent = load_agent(opts, env.action_space.n)

# snapshot = pickle.load(open("/home/anurag/Desktop/HiWi_OC/OC_Atari/player.pkl", "rb"))
# env._env.env.env.ale.restoreState(snapshot)

base_next_obs, _, _, _, _ = env.step(0)
base_objects = deepcopy(env.objects)
binary_mode = False

# MAX_DIFF = 200
original_ram, ram_n = 0, 0
def show_ims(obs_list, new_ram):
    _, axes = plt.subplots(1, len(obs_list))
    for ax, im in zip(axes, obs_list):
        ax.imshow(im)
    if binary_mode:
        plt.suptitle(f"{ram_n} set to {get_bin(new_ram)} (instead of {get_bin(original_ram)}, (={original_ram}))", fontsize=20)
    else:
        plt.suptitle(f"{ram_n} set to {new_ram} (instead of {original_ram})", fontsize=20)
    plt.show()

ram_n = initial_ram_n-1
while ram_n < 128:
    ram_n += 1
    askinput = True
    for i in range(255):
        # env._env.env.env.ale.restoreState(snapshot)
        original_ram = env.get_ram()[ram_n]
        env.set_ram(ram_n, i)
        resulting_obs, _, _, _, _ = env.step(0)
        im_diff = resulting_obs - base_next_obs
        nb_diff = np.sum(resulting_obs != base_next_obs) // 3
        if 0 < nb_diff < 200:
            print(nb_diff)
            if ONE_CHANGE:
                print(f"{ram_n} set to {i} (instead of {original_ram})")
                show_ims([base_next_obs, resulting_obs, im_diff], i)
                break
            else:
                if binary_mode:
                    print(f"{ram_n} set to {get_bin(i)} (instead of {get_bin(original_ram)})")
                else:
                    print(f"{ram_n} set to {i} (instead of {original_ram})")
                for oobj, nobj in zip(base_objects, env.objects):
                    if str(oobj) != str(nobj):
                        print(f"{oobj} -> {nobj}")
                show_ims([base_next_obs, resulting_obs, im_diff], i)
                prev_obs = deepcopy(resulting_obs)
                prev_objects = deepcopy(env.objects)
                original_ram = i
                while askinput:
                    el = input("What to do next ? (number/a/j/c/b)")
                    if el.isnumeric():
                        env._env.env.env.ale.restoreState(snapshot)
                        env.set_ram(ram_n, int(el))
                        new_obs, _, _, _, _ = env.step(0)
                        im_diff = new_obs - prev_obs
                        print(int(el)//16)
                        if binary_mode:
                            print(f"{get_bin(original_ram)} -> {get_bin(el)}")
                        else:
                            print(f"{int(original_ram)} -> {el}")
                        for oobj, nobj in zip(prev_objects, env.objects):
                            if str(oobj) != str(nobj):
                                print(f"{oobj} -> {nobj}")
                        show_ims([prev_obs, new_obs, im_diff], el)
                        prev_obs = deepcopy(new_obs)
                        prev_objects = deepcopy(env.objects)
                        original_ram = el
                    elif el == "b":
                        binary_mode = not(binary_mode)
                        print(f"{binary_mode=}")
                    elif el == "a":
                        askinput = False
                    elif el == "j":
                        ram_n = int(input("which ram pos to jump to ?")) - 1
                        askinput = False
                        break
                    else:
                        askinput = False
                        break
                if not askinput:
                    break

