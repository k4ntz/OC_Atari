# appends parent path to syspath to make ocatari importable
# like it would have been installed as a package
import sys
import random
import matplotlib.pyplot as plt
from os import path
sys.path.append(path.dirname(path.dirname(path.abspath(__file__)))) # noqa
from ocatari.core import OCAtari
from ocatari.vision.utils import mark_bb, make_darker
from ocatari.vision.spaceinvaders import objects_colors
from ocatari.vision.pong import objects_colors
from ocatari.utils import load_agent, parser, make_deterministic

parser.add_argument("-g", "--game", type=str, required=True,
                    help="game to evaluate (e.g. 'Pong')")
parser.add_argument("-i", "--interval", type=str, default=10,
                    help="The frame interval (default 10)")
parser.add_argument("-m", "--mode", choices=["vision", "ram"],
                    default="ram", help="The frame interval")
parser.add_argument("-hud", "--hud", action="store_true", help="Detect HUD")
parser.add_argument("-om", "--observation_mode", default="ori", help="Observation mode")

opts = parser.parse_args()

# import ipdb; ipdb.set_trace()
env = OCAtari(opts.game, mode=opts.mode, render_mode='rgb_array', hud=opts.hud, 
              obs_mode=opts.observation_mode)
observation, info = env.reset()


if opts.path:
    agent = load_agent(opts, env.action_space.n)
    print(f"Loaded agents from {opts.path}")

env.step(2)
make_deterministic(0, env)
# ax = plt.gca()
for i in range(10000):
    if opts.path is not None:
        action = agent.draw_action(env.dqn_obs)
    else:
        action = random.randint(0, env.nb_actions-1)
    obs, reward, terminated, truncated, info = env.step(action)
    if i > i % opts.interval == 0:
        env.render_explanations()

    if terminated or truncated:
        observation, info = env.reset()
    # modify and display render
env.close()
