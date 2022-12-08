from ocatari import OCAtari
import time
import random
import ipdb
import matplotlib.pyplot as plt
from vision.utils import mark_point, mark_bb, make_darker
from vision.pong import objects_colors


env = OCAtari("Pong", mode="vision", render_mode='rgb_array')
# env = OCAtari("Pong", mode="revised", render_mode='rgb_array')
observation, info = env.reset()
prevRam = None
already_figured_out = []
for i in range(1000):
    # done split into 2 parts:
    # terminated = True if env terminates (completion or failure),
    # truncated = True if episodes truncates due to a time limit or a reason that is not defined of the task

    obs, reward, terminated, truncated, info = env.step(random.randint(0, 0))
    if info.get('frame_number') > 100 and i % 10 == 0:
        for obj_name, pos in info["objects"].items():
            sur_col = make_darker(objects_colors[obj_name])
            mark_bb(obs, pos, color=sur_col)
            mark_point(obs, *pos[:2], color=(255, 255, 0))
        plt.imshow(obs)
        plt.show()

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
    # modify and display render
env.close()
