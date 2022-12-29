# appends parent path to syspath to make ocatari importable
# like it would have been installed as a package
import sys
from os import path
sys.path.append(path.dirname(path.dirname(path.abspath(__file__))))

import random
import matplotlib.pyplot as plt
from ocatari.core import OCAtari
from ocatari.vision.utils import mark_bb, make_darker
from ocatari.vision.skiing import objects_colors
from ocatari.utils import load_agent, parser


game_name = "Skiing"
MODE = "vision"
MODE = "revised"
env = OCAtari(game_name, mode=MODE, render_mode='rgb_array')
# env = OCAtari(game_name, mode=MODE, render_mode='human')
observation, info = env.reset()
prevRam = None
already_figured_out = []

opts = parser.parse_args()

if opts.path:
    agent = load_agent(opts, env.action_space.n)

opts = parser.parse_args()

if opts.path:
    agent = load_agent(opts, env.action_space.n)


def show_detected_objects(obs, info):
    for obj_name, oinfo in info["objects"].items():
        opos = oinfo[:4]
        ocol = oinfo[4:]
        print(obj_name, ":", oinfo)
        if MODE == "vision":
            ocol = objects_colors[obj_name]
        sur_col = make_darker(ocol)
        mark_bb(obs, opos, color=sur_col)
        # mark_point(obs, *opos[:2], color=(255, 255, 0))
    print("-"*30, end="")
    plt.imshow(obs)
    plt.show()


for i in range(40000):
    if opts.path is not None:
        action = agent.draw_action(env.dqn_obs)
    else:
        action = random.randint(0, 2)
        action = 0
    obs, reward, terminated, truncated, info = env.step(action)
    if i > 55 and i % 1 == 0:
        # import ipdb; ipdb.set_trace()
        # if info["score"] < 10:
        show_detected_objects(obs, info)
        print(i)
    if terminated or truncated:
        observation, info = env.reset()
    # modify and display render
env.close()
