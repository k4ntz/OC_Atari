import time
import random
import ipdb
import sys
sys.path.insert(0, '../..') # noqa
from ocatari.core import OCAtari

"""
Test raw/revised mode with a human render_mode and ipdb debugger
"""

env = OCAtari("Tennis", mode="raw", render_mode="human")
observation, info = env.reset()
prevRam = None
already_figured_out = []
for _ in range(10000000):
    # n: next line, c: resume execution
    # if info.get('frame_number') > 400:
    # for b in range(126):
    #   obs, reward, terminated, truncated, info = env.step(random.randint(0, 0))
    #   print(b)
    #    env.set_ram(b, 2)
    #   env.render()
    #    ipdb.set_trace()
    # action = self._action_set[1]

    # done split into 2 parts:
    # terminated = True if env terminates (completion or failure),
    # truncated = True if episodes truncates due to a time limit or a reason that is not defined of the task
    obs, reward, terminated, truncated, info = env.step(random.randint(-2, 2))
    # env.set_ram(57, 1)

    ram = env._env.unwrapped.ale.getRAM()
    env.set_ram(2, i)
    if prevRam is not None:
        for i in range(len(ram)):
            if ram[i] != prevRam[i] and i not in already_figured_out:
                pad = "           "
                for u in range(4 - len(str(i))):
                    pad += " "
                print(str(i) + pad + "value:" + str(ram[i]) + pad + " was previously " + str(prevRam[i]))
    print("------------------------------------------")
    prevRam = ram

    ipdb.set_trace()

    if terminated or truncated:
        observation, info = env.reset()
    print(info)
    env.render()
    if info.get('episode_frame_number') > 50:
        ipdb.set_trace()
    time.sleep(0.01)
    ipdb.set_trace()
env.close()
