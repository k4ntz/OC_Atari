# appends parent path to syspath to make ocatari importable
# like it would have been installed as a package
import sys
import matplotlib.pyplot as plt
from ocatari.ram._helper_methods import bitfield_to_number
sys.path.insert(0, '../../') # noqa

from ocatari.core import OCAtari
from ocatari.vision.utils import mark_bb, make_darker


game_name = "Centipede"
MODE = "revised"
HUD = True
env = OCAtari(game_name, mode=MODE, hud=HUD, render_mode='rgb_array')
observation, info = env.reset()


for i in range(1000):
    obs, reward, terminated, truncated, info = env.step(env.action_space.sample())
    if i % 20 == 0:
        # print(env.objects)
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
