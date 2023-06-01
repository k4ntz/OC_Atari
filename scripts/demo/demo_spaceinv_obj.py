# appends parent path to syspath to make ocatari importable
# like it would have been installed as a package
import sys
import random
import matplotlib.pyplot as plt
sys.path.insert(0, '../../ocatari') # noqa
from core import OCAtari
from vision.utils import mark_bb, make_darker
from vision.spaceinvaders import objects_colors
# from ocatari.vision.pong import objects_colors
from utils import load_agent, parser
from tqdm import tqdm


game_name = "Pong"
game_name = "SpaceInvaders"
# game_name = "Tennis"
MODE = "vision"
# MODE = "revised"
env = OCAtari(game_name, mode=MODE, render_mode='rgb_array')
observation, info = env.reset()
prevRam = None
already_figured_out = []

opts = parser.parse_args()

if opts.path:
    agent = load_agent(opts, env.action_space.n)

for i in tqdm(range(10000)):
    if opts.path is not None:
        action = agent.draw_action(env.dqn_obs)
    else:
        action = random.randint(0, 5)
    obs, reward, terminated, truncated, info = env.step(action)
    if info.get('frame_number') > 0 and i % 100 == 0:
        for obj in env.objects:
            opos = obj.xywh
            ocol = obj.rgb
            sur_col = make_darker(ocol)
            mark_bb(obs, opos, color=sur_col)
            # mark_point(obs, *opos[:2], color=(255, 255, 0))
        print(env.objects)
        plt.imshow(obs)
        plt.show()

    if terminated or truncated:
        observation, info = env.reset()
    # modify and display render
env.close()
