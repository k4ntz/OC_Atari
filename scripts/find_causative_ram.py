import gymnasium as gym
# import time
# import random
import numpy as np
from matplotlib import pyplot as plt
from tqdm import tqdm

"""
This script can be used to find score like objects in RAM
given bb should contain the score like object.
"""


def crop_rgb_array(rgb_array, x, y, width, height):
    """
    Crops the given rgb_array to the given bb.
    """
    ret = np.ndarray(shape=(height, width, 3), dtype=int)

    for i in range(height):
        index = i + y
        ret[i] = rgb_array[index][x:x + width]

    return ret


def find_causative_ram(game, x, y, width, height, show_plot=False):
    """
    Goes over the entire ram. Manipulating it to observe possible changes in the given bb

    if something in the given bb changes, the causative ram_position will be included in the return.
    """
    env = gym.make(game, render_mode="rgb_array")
    env.metadata['render_fps'] = 60
    env.reset(seed=42)
    observation, reward, terminated, truncated, info = env.step(0)
    obs0 = crop_rgb_array(observation, x, y, width, height)
    env.reset(seed=42)
    ram = env.unwrapped.ale.getRAM()

    candidates = []
    for i in tqdm(range(len(ram))):
        env.reset(seed=42)
        # observation, reward, terminated, truncated, info = env.step(0)
        env.unwrapped.ale.setRAM(i, 0)

        observation, reward, terminated, truncated, info = env.step(0)
        obs = crop_rgb_array(observation, x, y, width, height)
        if not np.all(obs0 == obs):
            if show_plot:
                plt.imshow(obs)  # rgb_array stuff for fun
                plt.show()
            candidates.append(i)

    env.close()
    return candidates


if __name__ == "__main__":

    X = 20
    Y = 173
    WIDTH = 110
    HEIGHT = 13

    candidates = find_causative_ram(
        "Assault", X, Y, WIDTH, HEIGHT, show_plot=False)
    print(candidates)
