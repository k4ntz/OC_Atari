"""
Script to automatically perform a symbolic regression of object's positions from the ram state.
Uses the vision detection of objects for the regression, performed with PySR.
"""

import numpy as np
import pandas as pd
from os import makedirs
from copy import deepcopy
from pysr import PySRRegressor
from ocatari.core import OCAtari
from ocatari.utils import parser, make_deterministic, load_agent
from ocatari.vision.utils import find_objects

game = "PongDeterministic-v4"

MODE = "both"
# RENDER_MODE = "rgb_array"
RENDER_MODE = "human"
env = OCAtari(game, mode=MODE, render_mode=RENDER_MODE)
# env = OCAtari(game, mode=MODE, render_mode=RENDER_MODE, frameskip=1)
observation, info = env.reset()

agent = 'c51'
path = f"models/{game}/{agent}.gz" # game will be cleaned by load_agent
dqn_agent = load_agent(path, env.action_space.n)

make_deterministic(0, env)

# skip first frames
for _ in range(50):
    action = dqn_agent.draw_action(env.dqn_obs)
    _, _, _, _, _ = env.step(action)

N_FRAMES = 3000
ram_states = []
slots = {'enemy': [213, 130, 74], 'player': [92, 186, 92], 'ball': [236, 236, 236]} # objects to track and their color
properties = []
for object in slots.keys():
    properties.extend([object + '_x', object + '_y', object + '_w', object + '_h'])
data = pd.DataFrame(columns=properties)
                                
for i in range(N_FRAMES):
    action = dqn_agent.draw_action(env.dqn_obs)
    obs, _, terminated, truncated, _ = env.step(action)

    row = []
    for color in slots.values():
        obj = find_objects(obs, color, size=15, tol_s=15) # TODO: add a maxsize
        if obj == []:
            row.extend([None] * 4)
        else:
            row.extend(list(obj[0]))
    data.loc[i] = row
    ram_states.append(deepcopy(env.get_ram()))
    if terminated or truncated:
        break

data.insert(0, 'ram_states', ram_states)

makedirs("data/datasets/", exist_ok=True)
filename = f"data/datasets/{game}_{agent}_ram_and_objects_{N_FRAMES}_frames.csv"
data.to_csv(filename)

# enemy_y = objects[:,1]
# enemy_h = objects[:,3]
# print(enemy_y, enemy_h)

# player_y = objects[:,5]
# player_h = objects[:,7]

# ball_x = objects[:,8]
# ball_y = objects[:,9]
# print(ball_x, ball_y)

# model = PySRRegressor(
#     niterations = 50,  # < Increase me for better results
#     binary_operators = ["+", "-", "max", "min", "mod", "cond", "greater"],
#     elementwise_loss = "loss(prediction, target) = (prediction - target)^2",
#     # ^ Custom loss function (julia syntax)
# )

# model.fit(ram_states, enemy_y)

# model.fit(ram_states, player_y)
# model.fit(ram_states, player_h)

# model.fit(ram_states, ball_x)
# model.fit(ram_states, ball_y)

# print(model)
