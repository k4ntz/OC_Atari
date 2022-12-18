import time
import random
import ipdb
from matplotlib import pyplot as plt
import sys
import pathlib

try:
    from ocatari import OCAtari
except:
    # sys.path.append(pathlib.Path().resolve() / "../..")
    sys.path.append("../..")
    from ocatari import OCAtari

# test with the ipdb debugger

env = OCAtari("Tennis", mode="vision", render_mode='rgb_array_with_bbs')
observation, info = env.reset()
prevRam = None
already_figured_out = []
for i in range(1000):
    # n: next line, c: resume execution
    if info.get('frame_number') > 400:
        ipdb.set_trace()
    # action = self._action_set[1]

    # done split into 2 parts:
    # terminated = True if env terminates (completion or failure),
    # truncated = True if episodes truncates due to a time limit or a reason that is not defined of the task
    obs, reward, terminated, truncated, info = env.step(random.randint(4, 5))

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
    rgb_array = env.render()
    plt.imshow(rgb_array)  # rgb_array stuff for fun
    plt.show()
    print(rgb_array)
    time.sleep(0.01)
env.close()
