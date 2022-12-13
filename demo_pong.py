from ocatari import OCAtari
import random
import matplotlib.pyplot as plt
from vision.utils import mark_bb, make_darker
from vision.tennis import objects_colors


game_name = "Boxing"
game_name = "Pong"
game_name = "Tennis"
MODE = "vision"
MODE = "revised"
env = OCAtari(game_name, mode=MODE, render_mode='rgb_array')
observation, info = env.reset()
prevRam = None
already_figured_out = []
for i in range(1000):
    obs, reward, terminated, truncated, info = env.step(random.randint(0, 5))
    if info.get('frame_number') > 100 and i % 100 == 0:
        for obj_name, oinfo in info["objects"].items():
            opos = oinfo[:4]
            ocol = oinfo[4:]
            if MODE == "vision":
                ocol = objects_colors[obj_name]
            sur_col = make_darker(ocol)
            mark_bb(obs, opos, color=sur_col)
            # mark_point(obs, *opos[:2], color=(255, 255, 0))
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
