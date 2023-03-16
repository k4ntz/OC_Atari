# appends parent path to syspath to make ocatari importable
# like it would have been installed as a package
import sys
import random
import matplotlib.pyplot as plt
sys.path.insert(0, '../../') # noqa

from ocatari.core import OCAtari
from ocatari.vision.utils import mark_bb, make_darker
from ocatari.utils import load_agent, parser

game_name = "BeamRider"
MODE = "vision"
# MODE = "revised"
HUD = False
env = OCAtari(game_name, mode=MODE, hud=HUD, render_mode='rgb_array')
observation, info = env.reset()

opts = parser.parse_args()
# env._env.unwrapped.ale.setRAM(36, 1)

if opts.path:
    agent = load_agent(opts, env.action_space.n)

for i in range(10000):
    # env._env.unwrapped.ale.setRAM(41, 94)
    env._env.unwrapped.ale.setRAM(33, 36)
    env._env.unwrapped.ale.setRAM(25, 38)
    if opts.path is not None:
        action = agent.draw_action(env.dqn_obs)
    else:
        action = 0 # random.randint(0, 8)
    obs, reward, terminated, truncated, info = env.step(action)
    ram = env._env.unwrapped.ale.getRAM()
    # print(ram[41])
    if i % 10 == 0 and i > 80:
        print(env.objects)
        # print(ram)
        for obj in env.objects:
            x, y = obj.xy
            if x < 160 and y < 210 and obj.visible:
                opos = obj.xywh
                ocol = obj.rgb
                sur_col = make_darker(ocol)
                mark_bb(obs, opos, color=sur_col)
        plt.imshow(obs)
        plt.show()
    if terminated or truncated:
        observation, info = env.reset()
env.close()
