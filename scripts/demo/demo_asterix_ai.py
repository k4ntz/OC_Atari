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
from ocatari.utils import load_agent, parser

game_name = "Asterix-v4"  # Pong
# game_name = "SpaceInvaders"
# game_name = "Tennis"
MODE = "vision"
MODE = "revised"
env = OCAtari(game_name, mode=MODE, render_mode='rgb_array')
observation, info = env.reset()

opts = parser.parse_args()

if opts.path:
    agent = load_agent(opts, env.action_space.n)

fig, axes = plt.subplots(1, 2)
for i in range(1000):
    if opts.path is not None:
        action = agent.draw_action(env.dqn_obs)
    else:
        action = random.randint(0, 5)
    obs, reward, terminated, truncated, info = env.step(action)
    if i % 25 == 0:
        # obse2 = deepcopy(obse)
        for ax, obs, objects_list, title in zip(axes, [obs],
                                                [env.objects],
                                                ["ram"] if MODE == "revised" else ["vision"]):
            for obj in objects_list:
                opos = obj.xywh
                ocol = obj.rgb
                sur_col = make_darker(ocol)
                mark_bb(obs, opos, color=sur_col)
                # mark_point(obs, *opos[:2], color=(255, 255, 0))
            plt.imshow(obs)
            plt.show()
        for ax in axes.flatten():
            ax.set_xticks([])
            ax.set_yticks([])

    if terminated or truncated:
        observation, info = env.reset()
    # modify and display render
env.close()
