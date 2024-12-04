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
import time

parser.add_argument("-g", "--game", type=str, required=True,
                    help="game to evaluate (e.g. 'Pong')")
parser.add_argument("-i", "--interval", type=int, default=10,
                    help="The frame interval (default 10)")
parser.add_argument("-m", "--mode", choices=["vision", "ram"],
                    default="ram", help="The extraction mode")
parser.add_argument("-hud", "--hud", action="store_true", help="If provided, detect objects from HUD")

opts = parser.parse_args()


env = OCAtari(opts.game+"Deterministic", mode=opts.mode, render_mode='rgb_array', hud=opts.hud, obs_mode='dqn')
observation, info = env.reset()


if opts.path:
    agent = load_agent(opts, env.action_space.n)
    print(f"Loaded agents from {opts.path}")

make_deterministic(0, env)

ax = plt.gca()
plt.ion()  # activate interactive modus
plt.show(block=False)
for i in range(100000):
    if opts.path is not None:
        action = agent.draw_action(env.dqn_obs)
    else:
        action = random.randint(0, env.nb_actions-1)
    obs, reward, terminated, truncated, info = env.step(action)
    if i % opts.interval == 0:
        print(env.objects)
        for obs, objects_list, title in zip([obs],
                                                [env.objects],
                                                ["ram"] if opts.mode == "ram" else ["vision"]):
            for obj in objects_list:
                opos = obj.xywh
                ocol = obj.rgb
                sur_col = make_darker(ocol)
                mark_bb(obs, opos, color=sur_col)
                # mark_point(obs, *opos[:2], color=(255, 255, 0))
        ax.set_xticks([])
        ax.set_yticks([])
        ax.set_title(f"{opts.mode}: {opts.mode} mode (frame {i})", fontsize=20)
        ax.imshow(obs)
        plt.pause(0.00001)  # pause the interaction for a bit, so that the plot is drawn


    if terminated or truncated:
        observation, info = env.reset()
    # modify and display render
env.close()
