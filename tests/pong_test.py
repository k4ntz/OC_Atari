# appends parent path to syspath to make ocatari importable
# like it would have been installed as a package
import sys
import random
import matplotlib.pyplot as plt
from os import path
sys.path.append(path.dirname(path.dirname(path.abspath(__file__)))) # noqa
from ocatari.core import OCAtari, HideEnemyPong
from ocatari.vision.utils import mark_bb, make_darker
from ocatari.vision.spaceinvaders import objects_colors
from ocatari.vision.pong import objects_colors
from ocatari.utils import AtariNet, make_deterministic, _load_checkpoint
import numpy as np


if "hide" in sys.argv:
    env = HideEnemyPong("PongDeterministic-v0", mode="revised", render_mode='human', hud=False, obs_mode='dqn')
else:
    env = OCAtari("PongDeterministic-v0", mode="revised", render_mode='human', hud=False, obs_mode='dqn')
observation, info = env.reset()
AGENT_TYPE = "dqn"
dist = "c51" in AGENT_TYPE
agent = AtariNet(env.nb_actions, distributional=dist)
ckpt = _load_checkpoint(f"models/Pong/{AGENT_TYPE}.gz")
agent.load_state_dict(ckpt["estimator_state"])

print(f"Loaded {AGENT_TYPE} agents")

env.step(2)
make_deterministic(0, env)
ax = plt.gca()
ret = 0
all_returns = []
for i in range(100000):
    action = agent.draw_action(env.dqn_obs)
    obs, reward, terminated, truncated, info = env.step(action)
    ret += reward

    if terminated or truncated:
        print(ret)
        all_returns.append(ret)
        ret = 0
        observation, info = env.reset()
    if len(all_returns) == 10:
        break
    # modify and display render
env.close()
print(np.mean(all_returns), "+-", np.std(all_returns))
