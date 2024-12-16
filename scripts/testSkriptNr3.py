import time
import random
import ipdb
from matplotlib import pyplot as plt
import sys
# import pathlib
sys.path.insert(0, '../../')  # noqa
from ocatari.core import OCAtari

"""
Test vision mode with rgb_array as render_mode.
"""

env = OCAtari("Qbert", mode="vision", render_mode='rgb_array')
observation, info = env.reset()
prevRam = None
already_figured_out = []


# env._env.unwrapped.ale.setRAM(42, 14)
env._env.unwrapped.ale.setRAM(43, 160)

for _ in range(1000):
    # if info.get('frame_number') > 400:
    #     ipdb.set_trace()

    obs, reward, terminated, truncated, info = env.step(0)
    # obs, reward, terminated, truncated, info = env.step(1)

    ram = env._env.unwrapped.ale.getRAM()
    if _ % 10 == 0 and _ > 100:
        if prevRam is not None:
            for i in range(len(ram)):
                if ram[i] != prevRam[i] and i not in already_figured_out:
                    pad = "           "
                    for u in range(4 - len(str(i))):
                        pad += " "
                    print(str(i) + pad + "value:" +
                          str(ram[i]) + pad + " was previously " + str(prevRam[i]))
        print("------------------------------------------")
        prevRam = ram
        rgb_array = env.render()
        plt.imshow(obs)
        plt.show()
    if terminated or truncated:
        obs, info = env.reset()
    # print(info)
    # if info.get("frame_number") % 10 == 0:
    #     rgb_array = env.render()
    #     plt.imshow(obs)
    #     plt.show()
    #     # print(obs)
    # time.sleep(0)
env.close()
