# appends parent path to syspath to make ocatari importable
# like it would have been installed as a package
import sys
import random
import matplotlib.pyplot as plt
sys.path.insert(0, '../../') # noqa

from ocatari.core import OCAtari
from ocatari.vision.utils import mark_bb, make_darker
from ocatari.utils import load_agent, parser
import pickle
import numpy as np


game_name = "VentureNoFrameskip"
MODE = "vision"
MODE = "revised"
HUD = True
env = OCAtari(game_name, mode=MODE, hud=HUD, render_mode='rgb_array')
observation, info = env.reset()

opts = parser.parse_args()

if opts.path:
    agent = load_agent(opts, env.action_space.n)

snapshot = pickle.load(open("save_ve.pickle", "rb"))
env._env.env.env.ale.restoreState(snapshot)

action2 = 2

for i in range(1000000):
    if opts.path is not None:
        action = agent.draw_action(env.dqn_obs)
    else:
        action = 0
    
    if i < 57:
        obs, reward, terminated, truncated, info = env.step(1)
    obs, reward, terminated, truncated, info = env.step(action2)

    if i > 57 and i < 100:
        action2 = 4
    elif i >= 100 and i < 150:
        action2 = 5
    elif i >= 150 and i < 160:
        action2 = 4
    elif i >= 160:
        action2 = 1

    # if i > 1901 and i < 1910:
    #     print("hi")
    #     env._env.unwrapped.ale.setRAM(79, 79)
    #     env._env.unwrapped.ale.setRAM(20, 73)
    #     action2 = 5

    # elif i > 2901 and i < 2910:
    #     print("hi")
    #     env._env.unwrapped.ale.setRAM(79, 79)
    #     env._env.unwrapped.ale.setRAM(20, 73)
    #     action2 = 5

    # if i%100 == 0:
    #     print("\n\nahhh")
    #     if i < 100:
    #     # room 0
    #         env._env.unwrapped.ale.setRAM(85, 111)
    #         env._env.unwrapped.ale.setRAM(26, 51)
    #         action2 = 2
    #     elif i < 200:
    #         env._env.unwrapped.ale.setRAM(79, 25)
    #         env._env.unwrapped.ale.setRAM(20, 69)
    #         # action2 = 0
    #     elif i < 300:
    #         env._env.unwrapped.ale.setRAM(79, 60)
    #         env._env.unwrapped.ale.setRAM(20, 1)
    #         # action2 = 5
    #     elif i < 400:
    #     # room 1
    #         action2 = 5
    #         env._env.unwrapped.ale.setRAM(85, 34)
    #         env._env.unwrapped.ale.setRAM(26, 32)
    #     elif i < 500:
    #         env._env.unwrapped.ale.setRAM(79, 25)
    #         env._env.unwrapped.ale.setRAM(20, 69)
    #         action2 = 0
    #     elif i < 600:
    #         env._env.unwrapped.ale.setRAM(79, 56)
    #         env._env.unwrapped.ale.setRAM(20, 5)
    #         action2 = 2
    #     elif i < 700:
    #     # room 2
    #         action2 = 3
    #         env._env.unwrapped.ale.setRAM(85, 85)
    #         env._env.unwrapped.ale.setRAM(26, 10)
    #     elif i < 800:
    #         env._env.unwrapped.ale.setRAM(79, 119)
    #         env._env.unwrapped.ale.setRAM(20, 69)
    #     elif i < 900:
    #         env._env.unwrapped.ale.setRAM(79, 25)
    #         env._env.unwrapped.ale.setRAM(20, 14)
    #     elif i < 1000:
    #     # room 3
    #         env._env.unwrapped.ale.setRAM(85, 15)
    #         env._env.unwrapped.ale.setRAM(26, 18)
    #     elif i < 1100:
    #         env._env.unwrapped.ale.setRAM(79, 80)
    #         env._env.unwrapped.ale.setRAM(20, 37)
    #         action2 = 0
    #     elif i < 1200:
    #         env._env.unwrapped.ale.setRAM(79, 30)
    #         env._env.unwrapped.ale.setRAM(20, 37)
    #     # elif i < 1300:
    #     # # room 0
    #     #     env._env.unwrapped.ale.setRAM(85, 111)
    #     #     env._env.unwrapped.ale.setRAM(26, 51)
    #     #     action2 = 2
    #     elif i < 1500:
    #         pass
    #     elif i < 1600:
    #     # room 7
    #         action2 = 3
    #         env._env.unwrapped.ale.setRAM(85, 10)
    #         env._env.unwrapped.ale.setRAM(26, 60)
    #     elif i < 1700:
    #         action2 = 4
    #         env._env.unwrapped.ale.setRAM(79, 85)
    #         env._env.unwrapped.ale.setRAM(20, 22)
    #     elif i < 1800:
    #         env._env.unwrapped.ale.setRAM(79, 136)
    #         env._env.unwrapped.ale.setRAM(20, 37)
    #     elif i < 1900:
    #         action2 = 2
    #         env._env.unwrapped.ale.setRAM(85, 83)
    #         env._env.unwrapped.ale.setRAM(26, 46)
    #     elif i < 2000:
    #         env._env.unwrapped.ale.setRAM(79, 75)
    #         env._env.unwrapped.ale.setRAM(20, 5)
    #     elif i < 2100:
    #         env._env.unwrapped.ale.setRAM(85, 12)
    #         env._env.unwrapped.ale.setRAM(26, 8)
    #         action2 = 3
    #     elif i < 2200:
    #         env._env.unwrapped.ale.setRAM(79, 85)
    #         env._env.unwrapped.ale.setRAM(20, 71)
    #     elif i < 2300:
    #         env._env.unwrapped.ale.setRAM(79, 22)
    #         env._env.unwrapped.ale.setRAM(20, 9)
    #     elif i < 2400:
    #         env._env.unwrapped.ale.setRAM(85, 114)
    #         env._env.unwrapped.ale.setRAM(26, 26)
    #         action2 = 2
    #     elif i < 2900:
    #         action2 = 4
    #     elif i < 3000:
    #         env._env.unwrapped.ale.setRAM(79, 120)
    #         env._env.unwrapped.ale.setRAM(20, 6)
    #         action2 = 5
    #     elif i < 3400:
    #         pass
    #     elif i < 3500:
    #     # room 0
    #         env._env.unwrapped.ale.setRAM(85, 111)
    #         env._env.unwrapped.ale.setRAM(26, 51)
    #         action2 = 2

    if i%1 == 0 and i > 57:
        # action2 = 4
        # with open('save_ve.pickle', 'wb') as handle:
        #     pickle.dump(env._env.env.env.ale.cloneState(), handle, protocol=pickle.HIGHEST_PROTOCOL)
        # if i <= 2100:
        #     env._env.unwrapped.ale.setRAM(85, 83)
        #     env._env.unwrapped.ale.setRAM(26, 46)
        print(env.objects)
        ram = env._env.unwrapped.ale.getRAM()
        print(ram[90])
        # print(ram[79], ram[26])
        # print(ram[64])
        # print(ram[0])
        # print(ram[39], ram[40], ram[41], ram[42], ram[43], ram[44])
        # print(ram[79:85], ram[20:26])
        # print(format(int(ram[84]), 'b').zfill(8))

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
