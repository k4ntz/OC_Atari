# appends parent path to syspath to make ocatari importable
# like it would have been installed as a package
import sys
import random
import matplotlib.pyplot as plt
sys.path.insert(0, '../../') # noqa

from ocatari.core import OCAtari
from ocatari.vision.utils import mark_bb, make_darker
from ocatari.utils import load_agent, parser

game_name = "NameThisGame"
# MODE = "vision"
MODE = "ram"
HUD = True
env = OCAtari(game_name, mode=MODE, hud=HUD, render_mode='rgb_array')
observation, info = env.reset()

# opts = parser.parse_args()

# if opts.path:
#     agent = load_agent(opts, env.action_space.n)

for i in range(10000):
    # if opts.path is not None:
    #     action = agent.draw_action(env.dqn_obs)
    # else:
    action = random.randint(0, 5)
    obs, reward, terminated, truncated, info = env.step(action)
    # ram = env._env.unwrapped.ale.getRAM()
    for i in range(5):
        env.set_ram(10*i, 255)
    # env.set_ram(0, 128)
    # env.set_ram(40, 1)
    print(env.get_ram())
    # print(env.objects)
    for obj in env.objects:
        x, y = obj.xy
        if x < 160 and y < 210:
            opos = obj.xywh
            ocol = obj.rgb
            sur_col = make_darker(ocol)
            mark_bb(obs, opos, color=sur_col)
    _, ax = plt.subplots(1, 1, figsize=(6, 8))
    ax.imshow(obs)
    plt.show()
    if terminated or truncated:
        observation, info = env.reset()
env.close()
