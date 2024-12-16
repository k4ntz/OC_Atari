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
obs, info = env.reset()
prevRam = None


# env._env.unwrapped.ale.setRAM(3, 0)
# env._env.unwrapped.ale.setRAM(42, 150)
# env._env.unwrapped.ale.setRAM(43, 160)

# env._env.unwrapped.ale.setRAM(65, 2)

# env._env.unwrapped.ale.setRAM(61, 1)

for _ in range(10000):
    # action = policy(observation)  # User-defined policy function
    target_ram_position = 72
    new_ram_value = 100
    # env._env.unwrapped.ale.setRAM(42, 14)
    # env._env.unwrapped.ale.setRAM(43, 200)
    # env._env.unwrapped.ale.setRAM(target_ram_position, new_ram_value)

    # -------------------manipulate ram----------------------------------
    ram = env._env.unwrapped.ale.getRAM()
    previous_ram_at_position = ram[target_ram_position]
    # print(new_ram_value)
    # print(ram)
    print(ram[target_ram_position])
    # print(ram[26:30])
    if new_ram_value > 255 or new_ram_value < 0:
        print("ram out of bounds")
        new_ram_value = 0
    # -------------------------------------------------------------------
    terminated, truncated = False, False
    # if _ < 25:
    obs, reward, terminated, truncated, info = env.step(3)
    # else:
    #     obs, reward, terminated, truncated, info = env.step(0)
    # obs, reward, terminated, truncated, info = env.step(1)
    if terminated or truncated:
        obs, info = env.reset()
    # if _ % 5 == 0 and _ > 150:
    #     plt.imshow(obs)
    #     plt.show()

    rgb_array = env.render()
    time.sleep(0.01)
env.close()
