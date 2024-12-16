import os.path

import gymnasium as gym
# import time
# import random
import numpy as np
import pathlib as pathlib
from matplotlib import pyplot as plt
from tqdm import tqdm
import pathlib
import shutil

"""
This script can be used to get a rough idea of which ram_positions are relevant for objects.
"""


def _count_inequalities(obs0, obs):
    counter = 0
    for i in range(len(obs0)):
        for u in range(len(obs0[i])):
            if np.all(obs0[i][u] != obs[i][u]):
                counter += 1
    return counter


def find_causative_ram(game, repetitions=3):
    """
    goes over the entire ram. manipulating it to observe possible changes in the given bb

    if something in the given bb changes, the causative ram_position will be included in the return
    """
    env = gym.make(game, render_mode="rgb_array")
    env.metadata['render_fps'] = 60
    env.reset(seed=42)
    observation, reward, terminated, truncated, info = env.step(0)
    obs0 = observation
    env.reset(seed=42)
    ram = env.unwrapped.ale.getRAM()
    fig = plt.figure()
    fig_list = []
    fig_list.append(fig)
    candidates = []
    current_plots = 1
    for i in tqdm(range(len(ram))):
        for u in range(repetitions):
            env.reset(seed=42)
            env.unwrapped.ale.setRAM(123, 60)
            env.unwrapped.ale.setRAM(i, u * 20 + 40)
            obs, reward, terminated, truncated, info = env.step(0)

            count = _count_inequalities(obs0, obs)
            if count >= 60:
                # I assume its too large to be an object
                # probably
                pass
            elif count <= 1:
                # no noticable difference
                pass
            else:
                # this might be correllated to an object
                candidates.append(i)
                if current_plots > 4:
                    fig = plt.figure()
                    fig_list.append(fig)
                    current_plots = 1

                ax = fig.add_subplot(2, 2, current_plots)
                ax.set_yticklabels([])
                ax.set_xticklabels([])
                ax.set_title(i)
                ax.add_artist(plt.imshow(obs))
                current_plots += 1
                break

    env.close()
    return candidates, fig_list


def _check_path(game_name):
    path = str(pathlib.Path().resolve()) + "/../../dumps/"
    if not os.path.exists(path):
        os.mkdir(path)
    path = path + "find_causative_ram_full/"
    if not os.path.exists(path):
        os.mkdir(path)
    path = path + game_name + "/"
    if not os.path.exists(path):
        os.mkdir(path)
    return path


if __name__ == "__main__":
    game = "Gopher"
    dump_path = _check_path(game)
    candidates, fig_list1 = find_causative_ram(game)

    for i in range(len(fig_list1)):
        dump_path_new = dump_path + "possible_objects" + str(i) + ".png"
        fig_list1[i].savefig(dump_path_new)

    print(candidates)
