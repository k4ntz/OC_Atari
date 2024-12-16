#!/usr/bin/env python
# coding: utf-8
import sys
import random
import matplotlib.pyplot as plt
from os import path
# sys.path.append(path.dirname(path.dirname(path.abspath(__file__)))) # noqa
from ocatari.core import OCAtari
from ocatari.vision.utils import mark_bb, make_darker
# from ocatari.vision.space_invaders import objects_colors
from ocatari.vision.pong import objects_colors
from ocatari.utils import load_agent, parser, make_deterministic
from copy import deepcopy
import pandas as pd
from numpy import random


parser.add_argument("-g", "--game", type=str,
                    help="game to evaluate (e.g. 'Pong')")
parser.add_argument("-i", "--interval", type=int, default=1000,
                    help="The frame interval (default 10)")
# parser.add_argument("-m", "--mode", choices=["vision", "ram"],
#                     default="ram", help="The frame interval")
parser.add_argument("-hud", "--hud", action="store_true",
                    default=True, help="Detect HUD")
parser.add_argument("-dqn", "--dqn", action="store_true",
                    default=True, help="Use DQN agent")

opts = parser.parse_args()

env = OCAtari(opts.game, mode="vision", render_mode='rgb_array', hud=True)
observation, info = env.reset()

if opts.dqn:
    opts.path = f"../models/{opts.game}/dqn.gz"
    dqn_agent = load_agent(opts, env.action_space.n)

env.step(2)
make_deterministic(42, env)

game_nr = 0
turn_nr = 0
dataset = {"INDEX": [], "OBS": [], "RAM": [], "VIS": [], "HUD": []}

for i in range(10000):
    action = dqn_agent.draw_action(env.dqn_obs)

    obs, reward, terminated, truncated, info = env.step(action)

    # if i % 1000 == 0:
    #    print(f"{i} done")

    dataset["INDEX"].append(f"{'%0.5d' %(game_nr)}_{'%0.5d' %(turn_nr)}")
    dataset["OBS"].append(obs.flatten().tolist())
    dataset["RAM"].append([])
    dataset["VIS"].append(
        [x for x in sorted(env.objects, key=lambda o: str(o))])
    dataset["HUD"].append([])
    turn_nr = turn_nr+1

    # if a game is terminated, restart with a new game and update turn and game counter
    if terminated or truncated:
        observation, info = env.reset()
        turn_nr = 0
        game_nr = game_nr + 1

    # The interval defines how often images are saved as png files in addition to the dataset
    if i % opts.interval == 0:
        """
        fig2 = plt.figure()
        ax2 = fig2.add_subplot(1, 1, 1)
        for obj in env.objects:
            opos = obj.xywh
            ocol = obj.rgb
            sur_col = make_darker(ocol, 0.8)
            mark_bb(obs3, opos, color=sur_col)
        ax2.imshow(obs3)
        ax2.set_xticks([])
        ax2.set_yticks([])
        plt.show()
        fig3 = plt.figure()
        ax3 = fig3.add_subplot(1, 1, 1)
        #for obj in env.objects_v:
        #    opos = obj.xywh
        #   ocol = obj.rgb
        #    sur_col = make_darker(ocol, 0.8)
        #    mark_bb(obs4, opos, color=sur_col)
        ax3.imshow(obs4)
        ax3.set_xticks([])
        ax3.set_yticks([])
        plt.show()
        """
env.close()

df = pd.DataFrame(dataset, columns=['INDEX', 'OBS', 'RAM', 'HUD', 'VIS'])
df.to_csv(f"/data/datasets_v/{opts.game}.csv", index=False)
print(f"Finished {opts.game}")
