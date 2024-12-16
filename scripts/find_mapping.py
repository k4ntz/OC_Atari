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

DROP_LOW = True
MIN_CORRELATION = 0.8

NB_SAMPLES = 600
game_name = "VideoPinballNoFrameskip"
MODE = "vision"
RENDER_MODE = "rgb_array"
env = OCAtari(game_name, mode=MODE, render_mode=RENDER_MODE)
random.seed(0)


def extract_prop(objs):
    for obj in objs:
        if "Flipper" in str(obj):
            if obj.x > 80:
                return obj.xywh


env.reset()
env.step(0)
dico = {}
for i in tqdm(range(3000)):
    rmst = env.get_ram()[102]
    if i % 3 == 0:
        action = random.randint(0, env.nb_actions - 1)
    obs, reward, terminated, truncated, info = env.step(action)
    # ram = env.get_ram()
    # color = obs[151, 30]
    props = extract_prop(env.objects)
    dico[rmst] = props
    # print(f"{rmst}: {props}")
    # plt.imshow(obs)
    # plt.show()
print(dico)
