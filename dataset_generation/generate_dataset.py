#!/usr/bin/env python
# coding: utf-8

import random
# appends parent path to syspath to make ocatari importable
# like it would have been installed as a package
import sys
from copy import deepcopy
from os import path, makedirs

import matplotlib.pyplot as plt
import pandas as pd
from numpy import random
# sys.path.append(path.dirname(path.dirname(path.abspath(__file__)))) # noqa
from ocatari.core import OCAtari
from ocatari.utils import load_agent, parser, make_deterministic
# from ocatari.vision.space_invaders import objects_colors
from ocatari.vision.pong import objects_colors
from ocatari.vision.utils import mark_bb, make_darker
import pickle
from tqdm import tqdm


parser.add_argument("-g", "--game", type=str, default="Pong",
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

# Init the environment
env = OCAtari(opts.game, mode="both", render_mode='human', hud=True)
observation, info = env.reset()

# Set up an agent
if opts.dqn:
    opts.path = f"models/{opts.game}/dqn.gz"
    dqn_agent = load_agent(opts, env.action_space.n)

# make environment deterministic
env.step(2)
make_deterministic(42, env)

# Init an empty dataset
game_nr = 0
turn_nr = 0
dataset = {"INDEX": [],  # "OBS": [],
           "RAM": [], "VIS": [], "HUD": []}
frames = []
r_objs = []
v_objs = []

# Generate 10,000 samples
for i in tqdm(range(10000)):
    action = dqn_agent.draw_action(env.dqn_obs)
    obs, reward, terminated, truncated, info = env.step(action)

    # make a short print every 1000 steps
    # if i % 1000 == 0:
    #    print(f"{i} done")

    step = f"{'%0.5d' % (game_nr)}_{'%0.5d' % (turn_nr)}"
    dataset["INDEX"].append(step)
    frames.append(deepcopy(obs))
    r_objs.append(deepcopy(env.objects))
    v_objs.append(deepcopy(env.objects_v))
    # dataset["OBS"].append(obs.flatten().tolist())
    dataset["VIS"].append(
        [x for x in sorted(env.objects_v, key=lambda o: str(o))])
    dataset["RAM"].append(
        [x for x in sorted(env.objects, key=lambda o: str(o)) if x.hud == False])
    dataset["HUD"].append(
        [x for x in sorted(env.objects, key=lambda o: str(o)) if x.hud == True])
    turn_nr = turn_nr + 1

    # if a game is terminated, restart with a new game and update turn and game counter
    if terminated or truncated:
        observation, info = env.reset()
        turn_nr = 0
        game_nr = game_nr + 1

    # The interval defines how often images are saved as png files in addition to the dataset
    if i % opts.interval == 0:
        """
        print("-"*50)
        print(f"Frame {i}")
        print("-"*50)
        fig, axes = plt.subplots(1, 2)
        for obs, objects_list, title, ax in zip([obs,obs2], [env.objects, env.objects_v], ["ram", "vis"], axes):
            print(f"{title}: ", sorted(objects_list, key=lambda o: str(o)))
            for obj in objects_list:
                opos = obj.xywh
                ocol = obj.rgb
                sur_col = make_darker(ocol, 0.2)
                mark_bb(obs, opos, color=sur_col)
                # mark_point(obs, *opos[:2], color=(255, 255, 0))
            ax.set_xticks([])
            ax.set_yticks([])
            ax.imshow(obs)
            ax.set_title(title)
        plt.suptitle(f"frame {i}", fontsize=20)
        plt.show()
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
        for obj in env.objects_v:
            opos = obj.xywh
            ocol = obj.rgb
            sur_col = make_darker(ocol, 0.8)
            mark_bb(obs4, opos, color=sur_col)
        ax3.imshow(obs4)
        ax3.set_xticks([])
        ax3.set_yticks([])
        plt.show()
        """
env.close()

df = pd.DataFrame(dataset, columns=['INDEX', 'RAM', 'HUD', 'VIS'])
makedirs("data/datasets/", exist_ok=True)
prefix = f"{opts.game}_dqn" if opts.dqn else f"{opts.game}_random"
df.to_csv(f"data/datasets/{prefix}.csv", index=False)
pickle.dump(v_objs, open(f"data/datasets/{prefix}_objects_v.pkl", "wb"))
pickle.dump(r_objs, open(f"data/datasets/{prefix}_objects_r.pkl", "wb"))
pickle.dump(frames, open(f"data/datasets/{prefix}_frames.pkl", "wb"))
print(f"Finished {opts.game}")
