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
from os import path
from sklearn.linear_model import RANSACRegressor, LinearRegression
sys.path.append(path.dirname(path.dirname(path.abspath(__file__))))  # noqa
from ocatari.core import OCAtari
from ocatari.utils import parser, load_agent, make_deterministic
import pickle
import gymnasium as gym

import os
# os.environ['QT_QPA_PLATFORM_PLUGIN_PATH'] = r'/home/quentin/bin/sysenv/lib/python3.11/site-packages/PyQt5/Qt5/plugins/platforms'


def ransac_regression(x, y):
    ransac = RANSACRegressor(estimator=LinearRegression(),
                             min_samples=6, max_trials=100,
                             loss='absolute_error', random_state=42,
                             residual_threshold=10)
    ransac.fit(np.array(x).reshape(-1, 1), y)
    return ransac.estimator_.coef_.item(), ransac.estimator_.intercept_.item()


parser.add_argument("-g", "--game", type=str, required=True,
                    help="game to evaluate (e.g. 'Pong')")
parser.add_argument("-s", "--snapshot", type=str, default=None,
                    help="Path to snapshot to start from.")
parser.add_argument("-dqn", "--dqn", action="store_true", help="Use DQN agent")
parser.add_argument("-po", "--print-options",
                    action="store_true", help="Use DQN agent")

opts = parser.parse_args()

if opts.print_options:
    print("MODE: ram or vision for the object detection")
    print()
    print("INTERACTIVE: if False, loop from 0 to 255 for each ram_n")
    print("\t else, ask for input after each ram_n change")
    print()
    print("ONE_CHANGE: if True, shows the image after each iteration (even if no difference)")
    print("\t else, shows the image only if there is a difference with *ALL* the previous images")
    print()
    print("COMPARE_WITH_PREVIOUS: if True, updates the base image and ram_n after each display")
    print("\telse: keeps the base image and ram_n values")
    print()
    print("initial_ram_n: the initial ram_n to start from")
    print()
    print("binary_mode: if True, shows the ram_n in binary format in the plots")
    print("\t else, shows the ram_n in decimal format in the plots")

    exit()

# RENDER_MODE = "human"
MODE = "vision"
RENDER_MODE = "rgb_array"
env = OCAtari(opts.game, mode=MODE, render_mode=RENDER_MODE, frameskip=1)
# env = gym.make(opts.game, render_mode=RENDER_MODE, frameskip=1)
random.seed(0)


INTERACTIVE = False
ONE_CHANGE = False
COMPARE_WITH_PREVIOUS = False
initial_ram_n = 22
binary_mode = True


make_deterministic(0, env)


def get_bin(x): return format(int(x), 'b').zfill(8)


observation, info = env.reset()


class Options(object):
    pass

# opts = Options()
# opts.path = "models/Kangaroo/dqn.gz"
# dqn_agent = load_agent(opts, env.action_space.n)


snapshot = None

if opts.snapshot:
    snapshot = pickle.load(open(opts.snapshot, "rb"))
    env._ale.restoreState(snapshot)

if snapshot is None:
    print("No snapshot provided, running for 20 frames")
    for _ in range(5):
        resulting_obs, _, _, _, _ = env.step(
            random.randint(0, env.nb_actions-1))
        snapshot = env._ale.cloneState()

base_next_obs, _, _, _, _ = env.step(0)
base_next_obs = deepcopy(base_next_obs)
base_objects = deepcopy(env.objects)


# MAX_DIFF = 200
ram_n = initial_ram_n
original_ram = env.get_ram()[ram_n]


def show_ims(obs_list, new_ram):
    _, axes = plt.subplots(1, len(obs_list))
    for ax, im in zip(axes, obs_list):
        ax.imshow(im)
    if binary_mode:
        plt.suptitle(
            f"{ram_n} set to {get_bin(new_ram)} (instead of {get_bin(original_ram)}, (={original_ram}))", fontsize=20)
    else:
        plt.suptitle(
            f"{ram_n} set to {new_ram} (instead of {original_ram})", fontsize=20)
    plt.show()


while ram_n < 127:
    print('Testing ram_n:', ram_n)
    askinput = True
    already_seen_frames = []
    shown = 0
    for i in range(0, 255, 16):
        already_seen = False
        env._ale.restoreState(snapshot)
        env.set_ram(ram_n, i)
        resulting_obs, _, _, _, _ = env.step(0)
        im_diff = resulting_obs - base_next_obs
        nb_diff = np.sum(resulting_obs != base_next_obs) // 3
        if 0 < nb_diff < 200:
            if not INTERACTIVE:
                if ONE_CHANGE:
                    print(f"{ram_n} set to {i} (instead of {original_ram})")
                    show_ims([base_next_obs, resulting_obs, im_diff], i)
                    if COMPARE_WITH_PREVIOUS:
                        base_next_obs = deepcopy(resulting_obs)
                        base_objects = deepcopy(env.objects)
                        original_ram = i
                        print("updated ram")
                    break
                else:
                    for frame in already_seen_frames:
                        nb_diff = np.sum(resulting_obs != frame)
                        if nb_diff == 0:
                            already_seen = True
                    if not already_seen:
                        already_seen_frames.append(deepcopy(resulting_obs))
                        print(f"{ram_n} set to {i} (instead of {original_ram})")
                        show_ims([base_next_obs, resulting_obs, im_diff], i)
                        if COMPARE_WITH_PREVIOUS:
                            base_next_obs = deepcopy(resulting_obs)
                            base_objects = deepcopy(env.objects)
                            original_ram = i
                            print("updated ram")
                        shown += 1
                    if shown and shown % 5 == 0:
                        ans = input("Loop on the same ram_state ? (y/n)")
                        if ans == "n":
                            break

            else:
                if binary_mode:
                    print(
                        f"{ram_n} set to {get_bin(i)} (instead of {get_bin(original_ram)})")
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
                        env._ale.restoreState(snapshot)
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
                        binary_mode = not (binary_mode)
                        print(f"{binary_mode=}")
                    elif el == "a":
                        askinput = False
                    elif el == "j":
                        ram_n = int(input("which ram pos to jump to ?")) - 1
                        askinput = False
                        break
                    elif el == "s":
                        env.step(0)
                        snapshot = env._ale.cloneState()
                    else:
                        askinput = False
                        break
                if not askinput:
                    break
    ram_n += 1
