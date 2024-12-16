"""
Demo script that allows me to compare the effects of change on ram_state where ram_state can take only fixed values.
The fixed values ="ram_dict" are obtained in a form of dictionary through categorical snippet in TestPitfall script
"""

# appends parent path to syspath to make ocatari importable
# like it would have been installed as a package
import sys
import random
import matplotlib.pyplot as plt
from copy import deepcopy
import numpy as np

from sklearn.linear_model import RANSACRegressor, LinearRegression
sys.path.insert(0, '../ocatari')  # noqa
from ocatari.core import OCAtari
from ocatari.utils import parser, load_agent, make_deterministic
import pickle

#  a dictionary containing the possible values that the particular ram_state can take
# Find this dictionary from the categorical snippet in TestPitfall
# This ram dict is for gopher
ram_dict = {19: [i for i in range(0, 256)]}
# {0: [128, 0], 1: [128, 152, 153, 0], 2: [1, 0], 3: [], 4: [24, 25, 0], 5: [24, 25, 0], 6: [128, 0], 7: [128, 152, 153, 0], 8: [1, 0], 9: [], 10: [24, 25, 0], 11: [1, 25, 0], 12: [128, 0], 13: [128, 152, 153, 0], 14: [1, 0], 15: [], 16: [1, 25, 0], 17: [24, 25, 0], 18: [], 19: [128, 192, 224, 240, 252, 255, 0], 20: [3, 15, 63, 255, 0], 21: [48, 112, 240, 0], 22: [1, 3, 131, 227, 243, 251, 255, 0], 23: [248, 252, 254, 255, 240], 24: [], 25: [], 26: [], 27: [], 28: [], 29: [], 30: [], 31: [], 32: [], 33: [], 34: [], 35: []}


parser.add_argument("-g", "--game", type=str, required=True,
                    help="game to evaluate (e.g. 'Pong')")
parser.add_argument("-s", "--snapshot", type=str, default=None,
                    help="Path to snapshot to start from.")
parser.add_argument("-dqn", "--dqn", action="store_true", help="Use DQN agent")

opts = parser.parse_args()

MODE = "vision"
RENDER_MODE = "human"
RENDER_MODE = "rgb_array"
env = OCAtari(opts.game+"NoFrameskip", mode=MODE, render_mode=RENDER_MODE)
random.seed(0)


INTERACTIVE = False
ONE_CHANGE = False
initial_ram_n = 19  # always starts from 1 due to corresponding indexing
stop_ram_n = 35

make_deterministic(0, env)


def get_bin(x): return format(int(x), 'b').zfill(8)


observation, info = env.reset()


class Options(object):
    pass


snapshot = None

if opts.snapshot:
    snapshot = pickle.load(open(opts.snapshot, "rb"))
    env._ale.restoreState(snapshot)

if snapshot is None:
    for _ in range(20):
        resulting_obs, _, _, _, _ = env.step(
            random.randint(0, env.nb_actions-1))
        snapshot = env._ale.cloneState()

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
        plt.suptitle(
            f"{ram_n} set to {get_bin(new_ram)} (instead of {get_bin(original_ram)}, (={original_ram}))", fontsize=20)
    else:
        plt.suptitle(
            f"{ram_n} set to {new_ram} (instead of {original_ram})", fontsize=20)
    plt.show()


ram_n = initial_ram_n-1
while ram_n < stop_ram_n:
    ram_n += 1
    askinput = True
    already_seen_frames = []
    shown = 0
    for i in ram_dict[ram_n]:
        already_seen = False
        env._ale.restoreState(snapshot)
        original_ram = env.get_ram()[ram_n]
        env.set_ram(ram_n, i)
        resulting_obs, _, _, _, _ = env.step(0)
        im_diff = resulting_obs - base_next_obs
        nb_diff = np.sum(resulting_obs != base_next_obs) // 3
        if 0 < nb_diff < 200:
            if not INTERACTIVE:
                if ONE_CHANGE:
                    print(f"{ram_n} set to {i} (instead of {original_ram})")
                    show_ims([base_next_obs, resulting_obs, im_diff], i)
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
                    else:
                        askinput = False
                        break
                if not askinput:
                    break
