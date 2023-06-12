import sys
import random
import matplotlib.pyplot as plt
from os import path
sys.path.append(path.dirname(path.dirname(path.abspath(__file__)))) # noqa
from ocatari.core import OCAtari
from ocatari.vision.spaceinvaders import objects_colors
from ocatari.vision.pong import objects_colors
from ocatari.utils import load_agent, parser


game_name = "Skiing"

MODE = "revised"
env = OCAtari(game_name, mode=MODE, render_mode='rgb_array')
observation, info = env.reset()

opts = parser.parse_args()

if opts.path:
    agent = load_agent(opts, env.action_space.n)

max_number_objs = {}
for i in range(10000):
    if opts.path is not None:
        action = agent.draw_action(env.dqn_obs)
    else:
        action = random.randint(0, 2)
    obs, reward, terminated, truncated, info = env.step(action)

    for obj in env.objects:
        classname = obj.__class__.__name__
        if classname not in max_number_objs:
            max_number_objs[classname] = 0
        nb_obj = sum([o.__class__.__name__ == classname for o in env.objects])
        if nb_obj > max_number_objs[classname]:
            max_number_objs[classname] = nb_obj
            print(f"Found {nb_obj} for class {classname}")

    if terminated or truncated:
        observation, info = env.reset()
        print("Reset")
    # modify and display render

env.close()
import ipdb; ipdb.set_trace()
