# appends parent path to syspath to make ocatari importable
# like it would have been installed as a package
import sys
import random
import matplotlib.pyplot as plt
sys.path.insert(0, '../../') # noqa

from ocatari.core import OCAtari
from ocatari.vision.utils import mark_bb, make_darker
from ocatari.utils import load_agent, parser

game_name = "Atlantis"
MODE = "vision"
MODE = "revised"
HUD = True
env = OCAtari(game_name, mode=MODE, hud=HUD, render_mode='rgb_array')
observation, info = env.reset()
prev_ram = None

opts = parser.parse_args()

if opts.path:
    agent = load_agent(opts, env.action_space.n)

for i in range(10000):
    if opts.path is not None:
        action = agent.draw_action(env.dqn_obs)
    else:
        action = 1
    obs, reward, terminated, truncated, info = env.step(action)
    ram = env._env.unwrapped.ale.getRAM()
    if i % 20 == 0:
        print(env.objects)
        print(ram)
        if prev_ram is not None:
            for i in range(len(ram)):
                if ram[i] != prev_ram[i]:
                    pad = "           "
                    for u in range(4 - len(str(i))):
                        pad += " "
                    print(str(i) + pad + "value:" + str(ram[i]) + pad + " was previously " + str(prev_ram[i]))
            print("------------------------------------------")
        for obj in env.objects:
            x, y = obj.xy
            if x < 160 and y < 210 and obj.visible:
                opos = obj.xywh
                ocol = obj.rgb
                sur_col = make_darker(ocol)
                mark_bb(obs, opos, color=sur_col)
        plt.imshow(obs)
        plt.show()
        prev_ram = ram
    if terminated or truncated:
        observation, info = env.reset()
env.close()
