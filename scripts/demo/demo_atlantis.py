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
# MODE = "revised"
HUD = True
env = OCAtari(game_name, mode=MODE, hud=HUD, render_mode='human')
observation, info = env.reset()
prev_ram = None

# ram_code_review = [0,31,0,31,30,31,40,31,10,31,100,31,255,0,1,0,255,255
# ,29,126,29,128,112,152,152,152,24,152,152,0,152,29,162,0,67,1
# ,0,78,40,0,0,255,0,96,4,192,2,96,0,96,0,96,5,48
# ,2,224,0,96,91,160,75,52,0,67,64,0,253,96,2,91,17,7
# ,7,130,201,254,2,2,2,208,48,48,176,1,0,0,5,5,5,0
# ,5,0,2,0,3,0,0,0,0,7,186,198,192,48,224,42,29,0
# ,0,8,3,0,13,2,0,0,16,3,3,2,0,1,24,20,255,77
# ,115,21]

# for i in range(128):
#     env._env.unwrapped.ale.setRAM(i, ram_code_review[i])

opts = parser.parse_args()

if opts.path:
    agent = load_agent(opts, env.action_space.n)

for i in range(10000):
    if opts.path is not None:
        action = agent.draw_action(env.dqn_obs)
    else:
        action = random.randint(-2, 2)
    obs, reward, terminated, truncated, info = env.step(action)
    ram = env._env.unwrapped.ale.getRAM()
    # import ipdb; ipdb.set_trace()
    if i % 20 == 0:
        print(env.objects)
        print(ram)
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
