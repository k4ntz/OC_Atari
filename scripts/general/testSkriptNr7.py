import time
import random
import ipdb
import sys
sys.path.insert(0, '../..') # noqa
from ocatari.core import OCAtari

"""
Set each RAM position to a specific value.
"""

env = OCAtari("Assault", mode="raw", render_mode="human")
observation, info = env.reset()
prevRam = None
already_figured_out = []
for i in range(1000):
    ram_value = 20
    for b in range(3, 126):
        obs, reward, terminated, truncated, info = env.step(random.randint(0, 3))
        print(b - 1)
        env.set_ram(b, ram_value)
        env.render()
        ipdb.set_trace()

    obs, reward, terminated, truncated, info = env.step(random.randint(0, 1))
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
    env.render()
    time.sleep(0.01)
env.close()

