# appends parent path to syspath to make ocatari importable
# like it would have been installed as a package
import sys
import random
import matplotlib.pyplot as plt
sys.path.insert(0, '../../') # noqa

from ocatari.core import OCAtari
from ocatari.vision.utils import mark_bb, make_darker
from ocatari.utils import load_agent, parser

game_name = "MsPacman"
MODE = "revised"
HUD = True
env = OCAtari(game_name, mode=MODE, hud=HUD, render_mode='rgb_array')
observation, info = env.reset()

opts = parser.parse_args()

if opts.path:
    agent = load_agent(opts, env.action_space.n)

for i in range(10000000):
    env._env.unwrapped.ale.setRAM(63, 0)
    if opts.path is not None:
        action = agent.draw_action(env.dqn_obs)
    else:
        action = random.randint(0, 4)
    obs, reward, terminated, truncated, info = env.step(action)

    
    if i % 1 == 0 and i > 50:
        # obse2 = deepcopy(obse)
        print(env.objects)
        ram = env._env.unwrapped.ale.getRAM()
        print(format(int(ram[63]), 'b').zfill(8))
        for obj in env.objects:
            x, y = obj.xy
            if x < 160 and y < 210:
                opos = obj.xywh
                ocol = obj.rgb
                sur_col = make_darker(ocol)
                mark_bb(obs, opos, color=sur_col)
            # mark_point(obs, *opos[:2], color=(255, 255, 0))

        plt.imshow(obs)
        plt.show()

    if terminated or truncated:
        observation, info = env.reset()
    # modify and display render
env.close()
