# appends parent path to syspath to make ocatari importable
# like it would have been installed as a package
import sys
import random
import matplotlib.pyplot as plt
sys.path.insert(0, '../../') # noqa

from ocatari.core import OCAtari
from ocatari.vision.utils import mark_bb, make_darker

game_name = "AsteroidsNoFrameskip-v4"
MODE = "vision"
MODE = "revised"
HUD = True
env = OCAtari(game_name, mode=MODE, hud=HUD, render_mode='rgb_array')
observation, info = env.reset()

for i in range(1000000):
    obs, reward, terminated, truncated, info = env.step(0)   #random.randint(0, 4))
    obs, reward, terminated, truncated, info = env.step(1)
    
    ram = env._env.unwrapped.ale.getRAM()
   # env.set_ram(3, 30)
    if i % 1 == 0:
        env.set_ram(62, 32)
        # obse2 = deepcopy(obse)
        print(env.objects)
        # print(ram[21])
        # print(ram[39])
        for obj in env.objects:
            x, y = obj.xy
            if x < 160 and y < 210:
                opos = obj.xywh
                ocol = obj.rgb
                sur_col = make_darker(ocol)
                mark_bb(obs, opos, color=sur_col)
            # mark_point(obs, *opos[:2], color=(255, 255, 0))
        plt.imshow(obs)
        plt.show()
    if terminated or truncated:
        observation, info = env.reset()
    # modify and display render
env.close()
