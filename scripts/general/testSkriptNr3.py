import time
import random
import ipdb
from matplotlib import pyplot as plt
import sys
# import pathlib
sys.path.insert(0, '../../ocatari') # noqa
from ocatari.core import OCAtari

"""
Test vision mode with rgb_array as render_mode.
"""

env = OCAtari("Atlantis", mode="raw", render_mode='human')
observation, info = env.reset()
prevRam = None
already_figured_out = []


for _ in range(1000):
    if info.get('frame_number') > 400:
        ipdb.set_trace()

    obs, reward, terminated, truncated, info = env.step(random.randint(0, 0))

    ram = env._env.unwrapped.ale.getRAM()
    if prevRam is not None:
        for i in range(len(ram)):
            if ram[i] != prevRam[i] and i not in already_figured_out:
                pad = "           "
                for u in range(4 - len(str(i))):
                    pad += " "
                print(str(i) + pad + "value:" + str(ram[i]) + pad + " was previously " + str(prevRam[i]))
    print("------------------------------------------")
    prevRam = ram
    if terminated or truncated:
        observation, info = env.reset()
    print(info)
    if info.get("frame_number") % 20 == 0:
        rgb_array = env.render()
        plt.imshow(rgb_array)
        plt.show()
        print(rgb_array)
    time.sleep(0)
env.close()
