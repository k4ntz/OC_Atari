import time
import random
import ipdb
from matplotlib import pyplot as plt
import sys
# import pathlib
sys.path.insert(0, '../../')  # noqa

from ocatari.core import OCAtari

"""
set the ram and see whats changed
"""


env = OCAtari("ChopperCommand", mode="vision", render_mode='human')
prevRam = None
observation, info = env.reset(seed=42)
observation, reward, terminated, truncated, info = env.step(0)
target_ram_position = -1

print("Round: ", target_ram_position)

for _ in range(100000):

    if _ % 100 == 0:
        target_ram_position += 1
        print("Round: ", target_ram_position)
        env.close()
        env = OCAtari("ChopperCommand", mode="vision", render_mode='human')
        observation, info = env.reset(seed=42)
        observation, reward, terminated, truncated, info = env.step(1)
    new_ram_value = 255
    env._env.unwrapped.ale.setRAM(target_ram_position, new_ram_value)

    terminated, truncated = False, False
    observation, reward, terminated, truncated, info = env.step(2)
    if terminated or truncated:
        observation, info = env.reset()

    rgb_array = env.render()
    time.sleep(0.01)
env.close()
