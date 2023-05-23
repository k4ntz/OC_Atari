# appends parent path to syspath to make ocatari importable
# like it would have been installed as a package
import sys
import random

import cv2
import ipdb
import matplotlib.pyplot as plt
import numpy as np

from ocatari.vision import utils
from os import path
sys.path.append(path.dirname(path.dirname(path.abspath(__file__)))) # noqa
from ocatari.core import OCAtari
from ocatari.vision.utils import mark_bb, make_darker
from ocatari.vision.spaceinvaders import objects_colors
from ocatari.vision.pong import objects_colors
from ocatari.utils import load_agent, parser

game_name = "Asterix-v4"  # Pong
# game_name = "SpaceInvaders"
# game_name = "Tennis"
MODE = "vision"
# MODE = "revised"
env = OCAtari(game_name, mode=MODE, render_mode='human')
observation, info = env.reset()

# notice: agent runs away from meat and mug
opts = parser.parse_args()
if opts.path:
    agent = load_agent(opts, env.action_space.n)

fig, axes = plt.subplots(1, 2)
for i in range(10000000):
    if opts.path is not None:
        action = agent.draw_action(env.dqn_obs)
    else:
        action = random.randint(0, 5)
    obs, reward, terminated, truncated, info = env.step(action)
    env._env.unwrapped.ale.setRAM(83, 2)

    # if i % 3000 == 0 or i % 3000 < 15:
    #     # obse2 = deepcopy(obse)
    #     for ax, obs, objects_list, title in zip(axes, [obs],
    #                                             [env.objects],
    #                                             ["ram"] if MODE == "revised" else ["vision"]):
    #         for obj in objects_list:
    #             opos = obj.xywh
    #             ocol = obj.rgb
    #             sur_col = make_darker(ocol)
    #             mark_bb(obs, opos, color=sur_col)
    #             # mark_point(obs, *opos[:2], color=(255, 255, 0))
    #         plt.imshow(obs)
    #         plt.show()
    ########
    # ipdb.set_trace()
    #
    # masks = [cv2.inRange(obs[0:200, 0:159, :],
    #                      np.array(color), np.array(color)) for color in ocol]
    #
    # mask = sum(masks)
    #
    # ipdb.set_trace()
    ########

    ################
    # print ram when changing score to detect bits responsible for kind of objects
    ram = env._env.unwrapped.ale.getRAM()
    if i>1 and prevRam[95] != ram[95]:
        for k in range(len(ram)):
            if ram[k] != prevRam[k]:
                if ram[k] > prevRam[k]:
                    integ = ram[k] - prevRam[k]
                else:
                    integ = prevRam[k] - ram[k]

                if integ > 127:
                    print(str(k), '\t', -integ, '\t',
                          format(-integ, '08b'), '\t',
                          str(ram[k]), '\t',
                          format(ram[k], '08b'),
                          "negativ")
                else:
                    print(str(k), '\t', integ, '\t',
                          format(integ, '08b'), '\t',
                          str(ram[k]), '\t',
                          format(ram[k], '08b')
                          )
        print(ram)
        # env.render()
        # rgb_array = env.render()
        # plt.imshow(rgb_array)  # rgb_array stuff for fun
        # plt.show()

        # plt.imshow(obs)
        # plt.show()
        print("------------------------------------------")

    if i > 0:
        prevRam = ram
    ################
        for ax in axes.flatten():
            ax.set_xticks([])
            ax.set_yticks([])

    if terminated or truncated:
        observation, info = env.reset()
    # modify and display render
env.close()
