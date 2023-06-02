#!/usr/bin/env python
# coding: utf-8
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
#from ocatari.vision.space_invaders import objects_colors
from ocatari.vision.pong import objects_colors
from ocatari.utils import load_agent, parser, make_deterministic
from copy import deepcopy
import pandas as pd
from numpy import random


# %%


parser.add_argument("-g", "--game", type=str,
                    help="game to evaluate (e.g. 'Pong')")
parser.add_argument("-i", "--interval", type=int, default=1000,
                    help="The frame interval (default 10)")
# parser.add_argument("-m", "--mode", choices=["vision", "revised"],
#                     default="revised", help="The frame interval")
parser.add_argument("-hud", "--hud", action="store_true", default=True, help="Detect HUD")
parser.add_argument("-dqn", "--dqn", action="store_true", default=True, help="Use DQN agent")


# %%
opts = parser.parse_args()


# %%
env = OCAtari(opts.game, mode="vision", render_mode='rgb_array', hud=True)
observation, info = env.reset()



# %%
if opts.dqn:
    opts.path = f"../models/{opts.game}/dqn.gz"
    dqn_agent = load_agent(opts, env.action_space.n)



# %%
dataset = {"INDEX": [], "OBS": [], "RAM": [], "VIS": [], "HUD": []}
env.step(2)
make_deterministic(42, env)
game_nr = 0
turn_nr = 0
for i in range(10000):
    r = random.random(1)[0]
    if r>0.7:
        action = dqn_agent.draw_action(env.dqn_obs)
    else:
        action = random.randint(0, env.nb_actions-1)
        
    obs, reward, terminated, truncated, info = env.step(action)
    obs2 = deepcopy(obs)
    obs3 = deepcopy(obs)
    obs4 = deepcopy(obs)
    #for obs, objects_list, title, ax in zip([obs,obs2], [env.objects, env.objects_v], ["ram", "vis"], axes):
    #print(f"RAM : ", sorted(env.objects, key=lambda o: str(o)))
    #print(f"VIS : ", sorted(env.objects_v, key=lambda o: str(o)))
    if i % opts.interval == 0:
        print(f"{i} done")
    dataset["INDEX"].append(f"{'%0.5d' %(game_nr)}_{'%0.5d' %(turn_nr)}")
    #dataset["OBS(Readable)"].append(obs)
    dataset["OBS"].append(obs.flatten().tolist())
    #dataset["RAM"].append([x for x in sorted(env.objects, key=lambda o: str(o)) if x.hud==False])
    dataset["RAM"].append([])
    dataset["VIS"].append([x for x in sorted(env.objects, key=lambda o: str(o))])
    #dataset["HUD"].append([x for x in sorted(env.objects, key=lambda o: str(o)) if x.hud==True])
    dataset["HUD"].append([])
    turn_nr = turn_nr+1
    if terminated or truncated:
        observation, info = env.reset()
        turn_nr = 0
        game_nr = game_nr + 1
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

        


# %%
df = []

df = pd.DataFrame(dataset, columns = ['INDEX', 'OBS', 'RAM', 'HUD', 'VIS'])
#display(df)


# %%
#display(df)

# %%
#df.iloc[0]["OBS"]

# %%
#df.iloc[0]["VIS"]

# %%
#df.iloc[40]["RAM"]

# %%
df.to_csv(f"/data/datasets_v/{opts.game}.csv", index=False)


# %%
print(f"Finished {opts.game}")





# %% [markdown]
# Seed = 42, commit 1906
#
# Finished Games:
# * Assault, 10k, 23.5
# * Asterix, 10k, 23.5
# * Atlantis, 10k, 23.5, took long, some print command is active, no HUD yet
# * Berzerk, 10k, 23.5
# * Bowling, 10k, 23.5
# * Boxing, 10k, 23.5
# * Breakout, 10k, 23.5
# * Carnival, 10k, 23.5, took long
# * ChopperCommand, 10k, 23.5, bad score, redo later, no HUD support
# * Kangaroo, 10k, 23.5
# * Pong, 10k, 24.5
# * Riverraid makes problems
# * Seaquest, 10k, 24.5
# * Skiing, 10k, 24.5
# * Space Invaders, 10k, 24.5
# * Tennis, 10k, 24.5
# * Centipede, 10k, 24.5
# * MsPacman, 10k, 26.5
# * BeamRider, 10k, 26.5, vision only
# * RoadRunner, 10k, 26.5, wrong HUD elements
# * Qbert, 10k, 26.5
# * DemonAttack, 10k, 26.5, vision only
# * FishingDerby, 10k, 26.5, no HUD support, vision only
# * RiverRaid, 10k, 26.5, vision only
# * Frostbite, 10k, 28.5, vision only
# * Alien, 10k, 29.5, vision only, Score is divided into numbers 
# * Freeway, 10k, 30.5
# * Asteroids, 10k, 30.5, vision only
#
#
# Errors Redo:
# * DemonAttack, 26.5
# * FishingDerby, 26.5, no visual output
#
#
# Not working:
# * FishingDerby, 26.5
# * Frostbite, 26.5
# * 
