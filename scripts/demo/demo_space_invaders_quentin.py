# appends parent path to syspath to make ocatari importable
# like it would have been installed as a package
import sys
sys.path.insert(0, '../../ocatari') # noqa
from ocatari.core import OCAtari
import random
import matplotlib.pyplot as plt
from ocatari.vision.utils import mark_bb, make_darker
from ocatari.vision.spaceinvaders import objects_colors
from ocatari.utils import load_agent, parser

game_name = "SpaceInvaders-v4"
MODE = "vision"
# MODE = "raw"
# MODE = "revised"
env = OCAtari(game_name, mode=MODE, render_mode='rgb_array')
observation, info = env.reset()
prevRam = None
already_figured_out = []

opts = parser.parse_args()

if opts.path:
    agent = load_agent(opts, env.action_space.n)

for i in range(1000):
    if opts.path is not None:
        action = agent.draw_action(env.dqn_obs)
    else:
        action = random.randint(0, 2)
    obs, reward, terminated, truncated, info = env.step(action)
    if info.get('frame_number') > 0 and i % 100 == 0:
        for obj_name, o_list in info["objects"].items():
            print(obj_name)
            for oinfo in o_list:
                opos = oinfo[:4]
                ocol = oinfo[4:]
                if MODE == "vision":
                    ocol = objects_colors[obj_name]
                sur_col = make_darker(ocol)
                mark_bb(obs, opos, color=sur_col)
                # mark_point(obs, *opos[:2], color=(255, 255, 0))
        plt.imshow(obs)
        plt.show()

    if terminated or truncated:
        observation, info = env.reset()
    # modify and display render
env.close()
