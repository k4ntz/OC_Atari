"""
Demo script that allows me to find the correlation between ram states and
detected objects through vision in Tennis
"""

# appends parent path to syspath to make ocatari importable
# like it would have been installed as a package
import sys
import random
import matplotlib.pyplot as plt
from copy import deepcopy
from tqdm import tqdm
import numpy as np
import pandas as pd
import seaborn as sns
from sklearn.linear_model import RANSACRegressor, LinearRegression
sys.path.insert(0, '../ocatari')  # noqa
from ocatari.core import OCAtari
from alive_progress import alive_bar
from ocatari.utils import load_agent, make_deterministic, RandomAgent
from time import sleep
from argparse import ArgumentParser

parser = ArgumentParser()
parser.add_argument("-g", "--game", type=str, required=True,
                    help="game to evaluate (e.g. 'Pong')")
parser.add_argument("-s", "--seed", type=int, default=0,
                    help="If provided, set the seed")
parser.add_argument("-tt", "--to_track", type=int, required=True, nargs='+',
                    help="A list of the ram position to track")
opts = parser.parse_args()


NB_SAMPLES = 1000
game_name = f"{opts.game}-v4"
MODE = "vision"
RENDER_MODE = "rgb_array"
env = OCAtari(game_name, mode=MODE, render_mode=RENDER_MODE, obs_mode="dqn")

make_deterministic(opts.seed, env)

observation, info = env.reset()

opts.path = f"models/{opts.game}/dqn.gz"
dqn_agent = load_agent(opts, env.action_space.n)
rand_agent = RandomAgent(env.nb_actions)

ram_saves = {}
for tt in opts.to_track:
    ram_saves[tt] = []

for agent in [dqn_agent, rand_agent]:
    env.reset()
    for i in tqdm(range(NB_SAMPLES)):
        action = agent.draw_action(env.dqn_obs)
        obs, reward, terminated, truncated, info = env.step(action)
        ram = env.get_ram()
        for tt in opts.to_track:
            ram_saves[tt].append(ram[tt])
        if terminated:
            env.reset()
env.close()


fig, axes = plt.subplots(1, len(opts.to_track))
for tt, ax in zip(opts.to_track, axes):
    labels, counts = np.unique(ram_saves[tt], return_counts=True)
    ax.bar(labels, counts, align='center')
    ax.set_xticks(labels)
    ax.set_title(f"Distribution on RAM[{tt}]")

plt.show()
