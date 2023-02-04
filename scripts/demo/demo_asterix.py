# appends parent path to syspath to make ocatari importable
# like it would have been installed as a package
import random
import sys
import matplotlib.pyplot as plt
import ipdb
sys.path.insert(0, '../../')  # noqa

from ocatari.core import OCAtari
from ocatari.vision.utils import mark_bb, make_darker
from ocatari.ram.demonAttack import ProjectileHostile

game_name = "Asterix-v4"
MODE = "vision"
HUD = True
env = OCAtari(game_name, mode=MODE, hud=HUD, render_mode='rgb_array')
observation, info = env.reset()

for i in range(10000000):
    # obs, reward, terminated, truncated, info = env.step(-2)
    obs, reward, terminated, truncated, info = env.step(random.randint(-2, 2))
    # env.step(env.action_space.sample())
    env._env.unwrapped.ale.setRAM(83, 2)

    if i % 1000 == 0:
        print(i)
    if i % 1 == 0:  # i > 3000 and and i % 3000 < 300
        print(env.objects)
        for obj in env.objects:
            x, y = obj.xy
            if x < 160 and y < 210 and obj.visible:
                opos = obj.xywh
                ocol = obj.rgb
                sur_col = make_darker(ocol)
                if isinstance(obj, ProjectileHostile):
                    sur_col = 255, 255, 255
                mark_bb(obs, opos, color=sur_col)
            # mark_point(obs, *opos[:2], color=(255, 255, 0))

        plt.imshow(obs)
        plt.show()

        # ipdb.set_trace()

    if terminated or truncated:
        observation, info = env.reset()
    # modify and display render
env.close()
