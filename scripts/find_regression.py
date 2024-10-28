"""
Script to automatically perform a symbolic regression of object's positions from the ram state.
Uses the vision detection of objects for the regression, performed with PySR.
"""

import math
import numpy as np
import pandas as pd
from os import makedirs
from copy import deepcopy
from pysr import PySRRegressor
from ocatari.core import OCAtari
from ocatari.utils import parser, make_deterministic, load_agent
from ocatari.vision.utils import find_objects

game = "PongDeterministic-v4"
slots = {'enemy': [213, 130, 74], 'player': [92, 186, 92], 'ball': [236, 236, 236]} # objects to track and their color
properties = []
for object in slots.keys():
    properties.extend([object + '_x', object + '_y', object + '_w', object + '_h'])

def generate_dataset():
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

    N_FRAMES = 200
    columns = properties + ['ram_states']
    data = pd.DataFrame(columns=columns)
                                    
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
        row.append(deepcopy(env.get_ram()))
        data.loc[i] = row

        if terminated or truncated:
            break

    makedirs("data/datasets/", exist_ok=True)
    filename = f"data/datasets/{game}_{agent}_ram_and_objects_{N_FRAMES}_frames.csv"
    data.to_csv(filename)

# generate_dataset()
dataset = pd.read_csv('data/datasets/PongDeterministic-v4_c51_ram_and_objects_3000_frames.csv')

def get_ram_states(dataset):
    ram_states_raw = dataset['ram_states']
    ram_states = np.empty((len(ram_states_raw), 128), dtype=int)

    for i, row in enumerate(ram_states_raw):
        d = row.replace('[', '').replace(']', '').replace('\n', ' ') # clean brackets and \n
        d = list(map(int, d.split())) # split on spaces to list
        ram_states[i, :] = np.array(d) # to np array
    
    return ram_states

def clean_data(ram_states, data):
    clean_ram, clean_data = [], []
    for ram, val in zip(ram_states, data):
        if not math.isnan(val):
            clean_ram.append(ram)
            clean_data.append(val)
    return clean_ram, clean_data

model = PySRRegressor(
    niterations = 100,  # < Increase me for better results
    binary_operators = ["+", "-", "max", "min", "mod", "cond", "greater"],
    elementwise_loss = "loss(prediction, target) = (prediction - target)^2",
    # ^ Custom loss function (julia syntax)
    # constraints={
    #     "*": {"constants": 1},  # Ensure one constant in multiplication, i.e., only integer factors
    #     "+": {"constants": 1},  # Ensure one constant in addition, only integers
    # }, # ^ Constraints to limit the constants to integers
    # extra_sympy_mappings={
    #     "IntConstant": lambda: np.random.randint(-50, 50),  # Random integers between -50 and 50
    # }, # ^ Function to generate integer constants only
)

ram_states = get_ram_states(dataset)
for prop in properties:
    print("Property  :", prop)
    prop_data = dataset[prop].to_numpy()
    cl_ram, cl_data = clean_data(ram_states, prop_data)
    model.fit(cl_ram, cl_data)
    equations = model.get_hof()
    print(equations)
    print()
    # print("Sympy equation:", model.sympy())