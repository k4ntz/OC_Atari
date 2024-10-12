"""
Script to automatically perform a symbolic regression of object's positions from the ram state.
Uses the vision detection of objects for the regression, performed with PySR.
"""

import random
import numpy as np
from copy import deepcopy
from pysr import PySRRegressor
from ocatari.core import OCAtari
from ocatari.utils import parser, make_deterministic, load_agent
from ocatari.vision.utils import find_objects

game = "PongDeterministic-v4"

MODE = "both"
# RENDER_MODE = "rgb_array"
RENDER_MODE = "human"
env = OCAtari(game, mode=MODE, render_mode=RENDER_MODE, frameskip=1)
observation, info = env.reset()

path = f"models/{game}/dqn.gz" # game will be cleaned by load_agent
dqn_agent = load_agent(path, env.action_space.n)

env.step(2)
make_deterministic(42, env)

# skip first frames
for _ in range(60):
    # _, _, _, _, _ = env.step(random.randint(0, env.nb_actions-1))
    action = dqn_agent.draw_action(env.dqn_obs)
    _, _, _, _, _ = env.step(action)

N_FRAMES = 500
ram_states = np.empty((N_FRAMES, 128))
colors = [[213, 130, 74], [92, 186, 92], [236, 236, 236]] # enemy, player, ball
objects = np.empty((N_FRAMES, 4 * len(colors))) # record x and y positions + width and height

for i in range(N_FRAMES):
    # action = random.randint(0, env.nb_actions-1)
    # obs, _, _, _, _ = env.step(action) # random action
    action = dqn_agent.draw_action(env.dqn_obs)
    obs, _, _, _, _ = env.step(action)

    for c, color in enumerate(colors):
        obj = find_objects(obs, color, miny=34, maxy=194)
        # import ipdb; ipdb.set_trace()
        if obj:
            objects[i, 4*c] = obj[0][0] # x position
            objects[i, 4*c + 1] = obj[0][1] # y position
            objects[i, 4*c + 2] = obj[0][2] # width
            objects[i, 4*c + 3] = obj[0][3] # height
    test = env.get_ram()
    ram_states[i,:] = deepcopy(test)

# enemy_y = objects[:,1]
# enemy_h = objects[:,3]
# print(enemy_y, enemy_h)

# player_y = objects[:,5]
# player_h = objects[:,7]

# ball_x = objects[:,8]
# ball_y = objects[:,9]
# print(ball_x, ball_y)

model = PySRRegressor(
    niterations = 50,  # < Increase me for better results
    binary_operators = ["+", "-", "max", "min", "mod", "cond", "greater"],
    elementwise_loss = "loss(prediction, target) = (prediction - target)^2",
    # ^ Custom loss function (julia syntax)
)

# model.fit(ram_states, enemy_y)

# model.fit(ram_states, player_y)
# model.fit(ram_states, player_h)

# model.fit(ram_states, ball_x)
# model.fit(ram_states, ball_y)

# print(model)
