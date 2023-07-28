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


game_name = "PrivateEyeNoFrameskip"
MODE = "vision"
# MODE = "revised"
HUD = True
env = OCAtari(game_name, mode=MODE, hud=HUD, render_mode='rgb_array')
observation, info = env.reset()

opts = parser.parse_args()

if opts.path:
    agent = load_agent(opts, env.action_space.n)

# env._env.unwrapped.ale.setRAM(36, 1)
# snapshot = pickle.load(open("save_pe.pickle", "rb"))
# env._env.env.env.ale.restoreState(snapshot)
# env._env.unwrapped.ale.setRAM(41, 7)
# env._env.unwrapped.ale.setRAM(47, 50)
# env._env.unwrapped.ale.setRAM(67, 15)

action2 = 3

for i in range(1000000):
    if opts.path is not None:
        action = agent.draw_action(env.dqn_obs)
    else:
        action = 3
    obs, reward, terminated, truncated, info = env.step(action)

    if i%5 == 0 and i > -1:
        # action2 = 0
        # with open('save_pe.pickle', 'wb') as handle:
        #     pickle.dump(env._env.env.env.ale.cloneState(), handle, protocol=pickle.HIGHEST_PROTOCOL)
        print(env.objects)
        ram = env._env.unwrapped.ale.getRAM()
        # print(format(int(ram[84]), 'b').zfill(8))
        print(ram[41:44])

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
