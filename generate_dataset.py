#!/usr/bin/env python
# coding: utf-8
# %%

# %%


# appends parent path to syspath to make ocatari importable
# like it would have been installed as a package
import sys
import random
import matplotlib.pyplot as plt
from os import path
#sys.path.append(path.dirname(path.dirname(path.abspath(__file__)))) # noqa
from ocatari.core import OCAtari
from ocatari.vision.utils import mark_bb, make_darker
from ocatari.vision.space_invaders import objects_colors
from ocatari.vision.pong import objects_colors
from ocatari.utils import load_agent, parser, make_deterministic
from copy import deepcopy
import pandas as pd


# %%


parser.add_argument("-g", "--game", type=str, 
                    help="game to evaluate (e.g. 'Pong')")
parser.add_argument("-i", "--interval", type=int, default=1,
                    help="The frame interval (default 10)")
# parser.add_argument("-m", "--mode", choices=["vision", "revised"],
#                     default="revised", help="The frame interval")
parser.add_argument("-hud", "--hud", action="store_true", default=True, help="Detect HUD")


# %%


opts = parser.parse_args()


# %%


env = OCAtari(opts.game, mode="test", render_mode='rgb_array', hud=opts.hud)
observation, info = env.reset()


# %%


if opts.path:
    agent = load_agent(opts, env.action_space.n)
    print(f"Loaded agents from {opts.path}")


# %%


"""
env.step(2)
make_deterministic(0, env)
#fig, axes = plt.subplots(1, 2)
for i in range(10000):
    if opts.path is not None:
        action = agent.draw_action(env.dqn_obs)
    else:
        action = random.randint(0, env.nb_actions-1)
    obs, reward, terminated, truncated, info = env.step(action)
    obs2 = deepcopy(obs)
    if i % opts.interval == 0:
        print("-"*50)
        print(f"Frame {i}")
        print("-"*50)
        fig, axes = plt.subplots(1, 2)
        for obs, objects_list, title, ax in zip([obs,obs2], [env.objects, env.objects_v], ["ram", "vis"], axes):
            print(f"{title}: ", sorted(objects_list, key=lambda o: str(o)))
            for obj in objects_list:
                opos = obj.xywh
                ocol = obj.rgb
                sur_col = make_darker(ocol)
                mark_bb(obs, opos, color=sur_col)
                # mark_point(obs, *opos[:2], color=(255, 255, 0))
            ax.set_xticks([])
            ax.set_yticks([])
            ax.imshow(obs)
            ax.set_title(title)
        plt.suptitle(f"frame {i}", fontsize=20)
        plt.show()

    if terminated or truncated:
        observation, info = env.reset()
    # modify and display render
env.close()
"""


# %%


dataset = {"INDEX": [], "OBS": [], "RAM": [], "VIS": []}
env.step(2)
make_deterministic(0, env)
game_nr = 0
turn_nr = 0
for i in range(100000):
    if opts.path is not None:
        action = agent.draw_action(env.dqn_obs)
    else:
        action = random.randint(0, env.nb_actions-1)
    obs, reward, terminated, truncated, info = env.step(action)
    #for obs, objects_list, title, ax in zip([obs,obs2], [env.objects, env.objects_v], ["ram", "vis"], axes):
    #print(f"RAM : ", sorted(env.objects, key=lambda o: str(o)))
    #print(f"VIS : ", sorted(env.objects_v, key=lambda o: str(o)))
    if i % 1000 == 0:
        print(f"{i} done")
    dataset["INDEX"].append(f"{'%0.5d' %(game_nr)}_{'%0.5d' %(turn_nr)}")
    dataset["OBS"].append(obs)
    dataset["RAM"].append(sorted(env.objects, key=lambda o: str(o)))
    dataset["VIS"].append(sorted(env.objects_v, key=lambda o: str(o)))
    turn_nr = turn_nr+1
    if terminated or truncated:
        observation, info = env.reset()
        turn_nr = 0
        game_nr = game_nr + 1
env.close()

        


# %%


df = pd.DataFrame(dataset, columns = ['INDEX', 'OBS', 'RAM', 'VIS'])
#display(df)


# %%


df.to_csv(f"/data/datasets/{opts.game}.csv", index=False)


# %%





