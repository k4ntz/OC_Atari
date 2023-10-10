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
sys.path.insert(0, '../ocatari') # noqa
from ocatari.core import OCAtari
import pickle

DROP_LOW = True
MIN_CORRELATION = 0.8

NB_SAMPLES = 600
game_name = "Seaquest" + "NoFrameskip"
MODE = "vision"
RENDER_MODE = "human"
RENDER_MODE = "rgb_array"
env = OCAtari(game_name, mode=MODE, render_mode=RENDER_MODE)
random.seed(0)

snapshot = pickle.load(open("snapshots/seaquest.pkl", "rb"))

env.reset()
# env.step(0)
dico = {}
for i in range(128):
    env._ale.restoreState(snapshot)
    env.set_ram(44, 2*i)
    obs, reward, terminated, truncated, info = env.step(0)
    color = obs[147, 89]
    dico[i] = tuple(color)
    # print(f"{i}: {color}")
    # plt.imshow(obs)
    # plt.show()
print(dico)