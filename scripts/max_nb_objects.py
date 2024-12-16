# appends parent path to syspath to make ocatari importable
# like it would have been installed as a package
import sys
import random
import matplotlib.pyplot as plt
from os import path
sys.path.append(path.dirname(path.dirname(path.abspath(__file__))))  # noqa
from ocatari.core import OCAtari
from ocatari.vision.spaceinvaders import objects_colors
from ocatari.vision.pong import objects_colors
from ocatari.utils import load_agent, parser
from tqdm import tqdm


parser.add_argument("-g", "--game", type=str, required=True,
                    help="game to evaluate (e.g. 'Pong')")
parser.add_argument("-i", "--interval", type=str, default=10,
                    help="The frame interval (default 10)")
parser.add_argument("-m", "--mode", choices=["vision", "ram"],
                    default="ram", help="The frame interval")
parser.add_argument("-hud", "--hud", action="store_true", help="Detect HUD")

opts = parser.parse_args()

env = OCAtari(opts.game, mode=opts.mode, render_mode='rgb_array',
              hud=opts.hud)
observation, info = env.reset()


if opts.path:
    agent = load_agent(opts, env.action_space.n)

max_number_objs = {}
pbar = tqdm(range(30000))
for i in pbar:
    if opts.path is not None:
        action = agent.draw_action(env.dqn_obs)
    else:
        number_available_actions = env.action_space.n
        action = random.randint(0, number_available_actions-1)
    obs, reward, terminated, truncated, info = env.step(action)

    for obj in env.objects:
        classname = obj.__class__.__name__
        if classname not in max_number_objs:
            max_number_objs[classname] = 0
        nb_obj = sum([o.__class__.__name__ == classname for o in env.objects])
        if nb_obj > max_number_objs[classname]:
            max_number_objs[classname] = nb_obj
            pbar.set_description(f"Found {nb_obj} for class {classname}")

    if terminated or truncated:
        observation, info = env.reset()
        # print("Reset")
    # modify and display render

env.close()
print(f"{opts.game} in {opts.mode} mode")
print("Please add:")
if opts.hud:
    print("MAX_NB_OBJECTS_HUD = ", max_number_objs)
else:
    print("MAX_NB_OBJECTS = ", max_number_objs)
folder = "ram" if opts.mode == "ram" else "vision"
print(f"to ocatari/{folder}/{opts.game.lower()}.py")
