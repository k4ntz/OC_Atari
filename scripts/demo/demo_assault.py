# appends parent path to syspath to make ocatari importable
# like it would have been installed as a package
import sys
import pickle
import random
import matplotlib.pyplot as plt
import os.path as op
sys.path.insert(0, '../../') # noqa

from ocatari.core import OCAtari
from ocatari.vision.utils import mark_bb, make_darker
from ocatari.utils import load_agent, parser

game_name = "Assault-v4"
MODE = "vision"
MODE = "revised"
HUD = True
env = OCAtari(game_name, mode=MODE, hud=HUD, render_mode='rgb_array')
observation, info = env.reset()

opts = parser.parse_args()

if opts.path:
    agent = load_agent(opts, env.action_space.n)


# snapshot = pickle.load(open("C:\\Users\\simon\\OC_Atari\\snapshots\\Assault_Level4.pkl", "rb") )
# env._env.env.env.ale.restoreState(snapshot)

# env._env.unwrapped.ale.setRAM(40, 188)

for i in range(10000):
    if opts.path is not None:
        action = agent.draw_action(env.dqn_obs)
    else:
        action = random.randint(6, 6)
    obs, reward, terminated, truncated, info = env.step(action)
    ram = env._env.unwrapped.ale.getRAM()
    if i % 5 == 0:
        # print(env.objects)
        # print("Enemy_app: " + str(ram[54:57]))
        # print("enemy_type " + str(ram[40:42]))
        # print("enemy_x " + str(ram[33:36]))
        # print("enemy_x_2 " + str(ram[36:39]))
        print(ram[40])
        for obj in env.objects:
            x, y = obj.xy
            if x < 160 and y < 210: # and obj.visible
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
