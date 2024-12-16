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


env = OCAtari(opts.game+"Deterministic", mode="both",
              render_mode='rgb_array', hud=opts.hud)

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


class IndexTracker:
    def __init__(self, axes):

        self.frame_idx = 0
        self.images = dict.fromkeys(['ram', 'vision'], None)
        self.fast_forward(opts.start)

        if opts.dqn:
            self.action = dqn_agent.draw_action(env.dqn_obs)
        else:
            self.action = random.randint(0, env.nb_actions-1)

        # self.action_func, self.gen_opts = action_generator
        # action = self.action_func(*(self.gen_opts))
        self.axes = axes
        obs, reward, terminated, truncated, info = env.step(self.action)
        obs2 = deepcopy(obs)
        # for robj in env.objects:
        #     print(robj, robj.closest_object(env.objects_v))
        for obs, objects_list, title, ax in zip([obs, obs2], [env.objects, env.objects_v], ["ram", "vision"], self.axes):
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
            self.images[title] = ax.imshow(obs)
            self.images[title].set_data(obs)
            ax.set_title(title)
            self.im = Image.fromarray(obs)
            # cv2.imwrite(f"frames/{title}_frame_{self.frame_idx}.png", obs, [cv2.IMWRITE_PNG_COMPRESSION, 0])
            # im.save()
            self.images[title].axes.figure.canvas.draw()

        if terminated or truncated:
            observation, info = env.reset()

        self.images['ram'].axes.figure.suptitle(
            f"frame {self.frame_idx}", fontsize=20)

    def fast_forward(self, target_idx):
        while self.frame_idx < target_idx:
            if opts.dqn:
                action = dqn_agent.draw_action(env.dqn_obs)
            else:
                action = random.randint(0, env.nb_actions-1)

            obs, reward, terminated, truncated, info = env.step(action)
            self.frame_idx += 1

    def skip_frames(self):
        self.fast_forward(self.frame_idx + opts.interval - 1)

    def on_press(self, event):
        if event.key == 'up':
            self.skip_frames()
            self.update()

    def update(self):
        if opts.dqn:
            action = dqn_agent.draw_action(env.dqn_obs)
        else:
            action = random.randint(0, env.nb_actions-1)
        # action = self.action_func(*self.gen_opts)
        obs, reward, terminated, truncated, info = env.step(action)
        obs2 = deepcopy(obs)

        # for robj in env.objects:
        #     print(robj, robj.closest_object(env.objects_v))
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
            self.images[title].set_data(obs)
            im = Image.fromarray(obs)
            # cv2.imwrite(f"frames/{title}_frame_{self.frame_idx}.png", obs, [cv2.IMWRITE_PNG_COMPRESSION, 0])
            # im.save()
            self.images[title].axes.figure.canvas.draw()
        self.images['ram'].axes.figure.suptitle(
            f"frame {self.frame_idx}", fontsize=20)

# if opts.dqn:
#     action_generator = (dqn_agent.draw_action, tuple(env.dqn_obs))
# else:
#     action_generator = (random.randint, (0, env.nb_actions-1))


fig, axes = plt.subplots(1, 2)
tracker = IndexTracker(axes)
fig.canvas.mpl_connect('key_press_event', tracker.on_press)
plt.show()

env.close()
