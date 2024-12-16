import time
import random
import ipdb
import sys
from os import path
sys.path.append(path.dirname(path.dirname(path.abspath(__file__))))  # noqa
from ocatari.core import OCAtari

"""
Use this test to set each RAM state to a chosen ram_value. This may lead to the game crashing and destroying it but
it can also give you the meaning for the RAM states, due to the changes you can see in the human representation of the
game after the value is set.
"""

env = OCAtari("Assault", mode="ram", render_mode="human")  # set game
observation, info = env.reset()
prevRam = None
already_figured_out = []
for i in range(1000):

    ram_value = 9   # set here the RAM value

    for b in range(0, 126):     # loop through the RAM
        obs, reward, terminated, truncated, info = env.step(
            random.randint(0, 0))
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
                print(str(i) + pad + "value:" +
                      str(ram[i]) + pad + " was previously " + str(prevRam[i]))
    print("------------------------------------------")
    prevRam = ram

    if terminated or truncated:
        observation, info = env.reset()
    print(info)
    env.render()
    time.sleep(0.01)
env.close()
