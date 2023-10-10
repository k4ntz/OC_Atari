"""
Demo script that allows me to find the linear relation between selected ram states and
detected objects through vision in game
"""

import random
# appends parent path to syspath to make ocatari importable
# like it would have been installed as a package
import sys
from copy import deepcopy

import numpy as np
from sklearn.linear_model import RANSACRegressor, LinearRegression
from tqdm import tqdm

sys.path.insert(0, '../ocatari')  # noqa
from ocatari.core import OCAtari
from ocatari.utils import load_agent


def ransac_regression(x, y):
    ransac = RANSACRegressor(estimator=LinearRegression(),
                             min_samples=50, max_trials=100,
                             loss='absolute_error', random_state=42,
                             residual_threshold=10)
    ransac.fit(np.array(x).reshape(-1, 1), y)
    return ransac.estimator_.coef_.item(), ransac.estimator_.intercept_.item()


DROP_LOW = True
MIN_CORRELATION = 0.7  # 0.8

NB_SAMPLES = 50  # 600 before
game_name = "FishingDerby-v4"  # RoadRunner-v4
MODE = "vision"
RENDER_MODE = "human"
# RENDER_MODE = "rgb_array"
env = OCAtari(game_name, mode=MODE, render_mode=RENDER_MODE, hud=True)
random.seed(0)

observation, info = env.reset()
# object_list = ["Projectile"]
object_list = ["FishingPolePlayerTwo"]
# create dict of list
objects_infos = {}
subset = []
for obj in object_list:
    objects_infos[f"{obj}_w"] = []
    objects_infos[f"{obj}_y"] = []
    subset.append(f"{obj}_w")
    subset.append(f"{obj}_y")
ram_saves = []
actions = [3] * 5 + [0] * 20 + [4] * 2 + [0] * 40 + [3] * 10 + [0] * 20 + [4] * 2 + [0] * 20 + [3] * 4 + [0] * 15 + [
    4] * 2 + [0] * 40


class Dummy():
    def __init__(self) -> None:
        pass


opts = Dummy()

opts.path = "models/FishingDerby/dqn.gz"

if opts.path:
    agent = load_agent(opts, env.action_space.n)
    print(f"Loaded agents from {opts.path}")
last_size = 0

for i in tqdm(range(NB_SAMPLES)):
    # obs, reward, terminated, truncated, info = env.step(random.randint(0, env.action_space.n-1))
    # action = agent.draw_action(env.dqn_obs)
    action = actions[i%len(actions)]
    # prob = random.random()
    # if prob > 0.9:
    #     action = 2 # UP
    # elif prob > 0.8:
    #     action = 5 # DOWN
    # else:
    #     action = 4 # 4-RIGHT 3- Left, Truck at (56, 129), (16, 18), Cactus at (125, 55), (8, 8), Cactus at (129, 46), (8, 8)]
    # if i % 5: # reset for pressing
    #     action = 0

    obs, reward, terminated, truncated, info = env.step(action)
    if info.get('frame_number') > 10 and i % 1 == 0:
        SKIP = False
        # print(env.objects)
        print(env.objects)
        for obj_name in object_list:  # avoid state without the tracked objects
             if str(env.objects).count(f"{obj_name} at") != 1:
                SKIP = True
                break
        # if str(env.objects).count("Projectile at (75,") == 0:
        #     print(env._env.unwrapped.ale.getRAM()[106])
        if SKIP:# or env.objects[-2].y < env.objects[-1].y:
            continue
        for obj in env.objects:
            objname = obj.category
            if objname in object_list:
                objects_infos[f"{objname}_w"].append(obj.wh[0])
                objects_infos[f"{objname}_y"].append(obj.wh[1])
            # n += 1
        ram = env._env.unwrapped.ale.getRAM()
        ram_saves.append(deepcopy(ram))
        # env.render()

    # modify and display render
env.close()

if len(ram_saves) == 0:
    print("No data point was taken")

# import ipdb; ipdb.set_trace()

ram_saves = np.array(ram_saves).T
list_important_ram = [21, ]
from_rams = {str(i): ram_saves[i] for i in list_important_ram if not np.all(ram_saves[i] == ram_saves[i][0])}
objects_infos.update(from_rams)
X = []
y = []
for i in range(len(from_rams)):
    l = []
    for key in list_important_ram:
        l.append(from_rams[str(key)][i])
    X.append(l)
    y.append(objects_infos["FishingPolePlayerTwo_w"][i])
reg = LinearRegression().fit(np.array(X), np.array(y))
print("score = " + str(reg.score(X, y)))
coeffs = reg.coef_

final_expression = f"{reg.intercept_} + "

for i in range(len(list_important_ram)):
    final_expression += f"{coeffs[i]} * ram_state[{list_important_ram[i]}] + "

print(final_expression)
