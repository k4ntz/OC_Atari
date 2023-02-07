# appends parent path to syspath to make ocatari importable
# like it would have been installed as a package
import sys
import random
import matplotlib.pyplot as plt
sys.path.insert(0, '../..') # noqa
from ocatari.core import OCAtari
from ocatari.vision.utils import mark_bb, make_darker
from ocatari.vision.space_invaders import objects_colors
from ocatari.vision.pong import objects_colors
from ocatari.utils import load_agent, parser, make_deterministic

parser.add_argument("-g", "--game", type=str, required=True,
                    help="game to evaluate (e.g. 'Pong')")
parser.add_argument("-i", "--interval", type=str, default=10,
                    help="The frame interval (default 10)")
parser.add_argument("-m", "--mode", choices=["vision", "revised"],
                    default="revised", help="The frame interval")
parser.add_argument("-hud", "--hud", action="store_true", help="Detect HUD")

opts = parser.parse_args()

game_name = opts.game
MODE = opts.mode
env = OCAtari(game_name, mode=MODE, render_mode='rgb_array', hud=opts.hud)
observation, info = env.reset()


if opts.path:
    agent = load_agent(opts, env.action_space.n)
    print(f"Loaded agents from {opts.path}")

env.step(2)
make_deterministic(0, env)
ax = plt.gca()
for i in range(10000):
    if opts.path is not None:
        action = agent.draw_action(env.dqn_obs)
    else:
        action = random.randint(0, env.nb_actions-1)
    obs, reward, terminated, truncated, info = env.step(action)
    if i % opts.interval == 0:
        for obs, objects_list, title in zip([obs],
                                                [env.objects],
                                                ["ram"] if MODE == "revised" else ["vision"]):
            for obj in objects_list:
                opos = obj.xywh
                ocol = obj.rgb
                sur_col = make_darker(ocol)
                mark_bb(obs, opos, color=sur_col)
                # mark_point(obs, *opos[:2], color=(255, 255, 0))
        ax.set_xticks([])
        ax.set_yticks([])
        plt.title(f"{game_name}: {MODE} mode (frame {i})", fontsize=20)
        plt.imshow(obs)
        plt.show()

    if terminated or truncated:
        observation, info = env.reset()
    # modify and display render
env.close()
