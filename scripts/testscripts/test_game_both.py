# appends parent path to syspath to make ocatari importable
# like it would have been installed as a package
import sys
import random
import matplotlib.pyplot as plt
from os import path
import pathlib
sys.path.append(path.dirname(path.dirname(path.abspath(__file__))))  # noqa
from ocatari.core import OCAtari
from ocatari.vision.utils import mark_bb, make_darker
from ocatari.vision.spaceinvaders import objects_colors
from ocatari.vision.pong import objects_colors
from ocatari.utils import load_agent, parser, make_deterministic
from copy import deepcopy
from PIL import Image
import cv2
import pickle


parser.add_argument("-g", "--game", type=str, required=True,
                    help="game to evaluate (e.g. 'Pong')")
parser.add_argument("-i", "--interval", type=int, default=10,
                    help="The frame interval (default 10)")
parser.add_argument("-s", "--start", type=int, default=0,
                    help="The frame to start from")
parser.add_argument("-hud", "--hud", action="store_true", help="Detect HUD")
parser.add_argument("-dqn", "--dqn", action="store_true", help="Use DQN agent")
parser.add_argument("-snap", "--snapshot", type=str, default="",
                    help="A path to a state snapshot")


opts = parser.parse_args()


# env = OCAtari(opts.game+"NoFrameskip", mode="both", render_mode='rgb_array', hud=opts.hud)
env = OCAtari(opts.game, mode="both", render_mode='rgb_array', hud=opts.hud)

observation, info = env.reset()
if opts.snapshot:
    snapshot = pickle.load(open(opts.snapshot, "rb"))
    env._env.env.env.ale.restoreState(snapshot)

if opts.dqn:
    opts.game = opts.game
    opts.path = f"models/{opts.game}/dqn.gz"
    try:
        dqn_agent = load_agent(opts, env.action_space.n)
    except FileNotFoundError:
        oc_atari_dir = pathlib.Path(__file__).parents[1].resolve()
        opts.path = str(oc_atari_dir / 'models' / f"{opts.game}" / 'dqn.gz')
        dqn_agent = load_agent(opts, env.action_space.n)

make_deterministic(0, env)

for i in range(100000):
    # try:
    if True:
        if opts.dqn:
            action = dqn_agent.draw_action(env.dqn_obs)
        else:
            action = random.randint(0, env.nb_actions-1)

        obs1, reward, terminated, truncated, info = env.step(action)
        obs2 = deepcopy(obs1)
        if i >= opts.start and i % opts.interval == 0:
            fig, axes = plt.subplots(1, 2)
            print(env.objects)
            print(env.objects_v)
            for obs, objects_list, title, ax in zip([obs1, obs2], [env.objects, env.objects_v], ["ram", "vision"], axes):
                toprint = sorted(objects_list, key=lambda o: str(o))
                # print([o for o in toprint if "Fuel" in str(o)])
                # print(title, end=": ")
                # print(toprint)
                for obj in objects_list:
                    opos = obj.xywh
                    ocol = obj.rgb
                    sur_col = make_darker(ocol)
                    mark_bb(obs, opos, color=sur_col)
                    # mark_point(obs, *opos[:2], color=(255, 255, 0))
                ax.set_xticks([])
                ax.set_yticks([])
                ax.imshow(obs)
                ax.set_title(title)
                # im = Image.fromarray(obs)
                # cv2.imwrite(f"frames/{title}_frame_{i}.png", obs, [cv2.IMWRITE_PNG_COMPRESSION, 0])
                # im.save()
            fig.suptitle(f"frame {i}", fontsize=20)
            plt.show()
            # import ipdb; ipdb.set_trace()

        if terminated or truncated:
            observation, info = env.reset()
            if opts.snapshot:
                env._env.env.env.ale.restoreState(snapshot)
        # modify and display render
    # except ValueError as e:
    #     print(e)
    else:
        import ipdb
        ipdb.set_trace()
        fig, axes = plt.subplots(1, 2)
        for obs, objects_list, title, ax in zip([obs, obs2], [env.objects, env.objects_v], ["ram", "vision"], axes):
            toprint = sorted(objects_list, key=lambda o: str(o))
            # print([o for o in toprint if "Fuel" in str(o)])
            print(toprint)
            for obj in objects_list:
                opos = obj.xywh
                ocol = obj.rgb
                sur_col = make_darker(ocol)
                mark_bb(obs, opos, color=sur_col)
                # mark_point(obs, *opos[:2], color=(255, 255, 0))
            ax.set_xticks([])
            ax.set_yticks([])
            ax.imshow(obs)
            ax.set_title(title)
        fig.suptitle(f"frame {i}", fontsize=20)
        plt.show()
env.close()
