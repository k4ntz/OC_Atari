# appends parent path to syspath to make ocatari importable
# like it would have been installed as a package
import sys
import random
import matplotlib.pyplot as plt
from os import path
sys.path.append(path.dirname(path.dirname(path.abspath(__file__)))) # noqa
from ocatari.core import OCAtari
from ocatari.vision.utils import mark_bb, make_darker
from ocatari.utils import load_agent, parser, make_deterministic
from tqdm import tqdm


game_name = "Asterix"
MODE = "vision"
MODE = "revised"
import ipdb;ipdb.set_trace()
env = OCAtari(game_name, mode=MODE, render_mode='rgb_array')
observation, info = env.reset()

opts = parser.parse_args()

if opts.path:
    agent = load_agent(opts, env.action_space.n)
    print(f"Loaded agents from {opts.path}")
env.step(2)
make_deterministic(0, env)
fig, axes = plt.subplots(1, 2)
for i in tqdm(range(10000)):
    if opts.path is not None:
        action = agent.draw_action(env.dqn_obs)
    else:
        action = random.randint(0, env.action_space.n-1)
    obs, reward, terminated, truncated, info = env.step(action)
    if i > 60 and i % 10 == 0:
    # if show:
        for ax, obs, objects_list, title in zip(axes, [obs],
                                                [env.objects],
                                                ["ram"] if MODE == "revised" else ["vision"]):
            for obj in objects_list:
                opos = obj.xywh
                ocol = obj.rgb
                sur_col = make_darker(ocol)
                mark_bb(obs, opos, color=sur_col)
                # mark_point(obs, *opos[:2], color=(255, 255, 0))
        for ax in axes.flatten():
            ax.set_xticks([])
            ax.set_yticks([])
        plt.imshow(obs)
        plt.show()

    if terminated or truncated:
        observation, info = env.reset()
    # modify and display render
env.close()
