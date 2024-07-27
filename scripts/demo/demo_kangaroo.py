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


game_name = "Kangaroo"
MODE = "vision"
MODE = "ram"
HUD = True
env = OCAtari(game_name, mode=MODE, hud=HUD, render_mode='rgb_array')
observation, info = env.reset()

opts = parser.parse_args()

# if opts.path:
#     agent = load_agent(opts, env.action_space.n)

env._env.unwrapped.ale.setRAM(36, 1)
snapshot = pickle.load(open("../Kangaroo_save_state2.pickle", "rb"))
env._env.env.env.ale.restoreState(snapshot)

prev_ram = None

for i in range(1000):
    # if opts.path is not None:
    #     action = agent.draw_action(env.dqn_obs)
    # else:
    #     action = 6
    action = 0
    obs, reward, terminated, truncated, info = env.step(action)  # env.step(6) for easy movement

    if i == 0:
        env._env.unwrapped.ale.setRAM(36, 1)
        snapshot = pickle.load(open("../Kangaroo_save_state2.pickle", "rb"))
        env._env.env.env.ale.restoreState(snapshot)
    if i%1 == 0 and i > 10:
        # obse2 = deepcopy(obse)
        # print(env.objects)
        ram = env._env.unwrapped.ale.getRAM()
        # if prev_ram is not None:
        #     for i in range(128):
        #         if ram[i] != prev_ram[i]:
        #             print(i, ram[i], prev_ram[i])
        # print(ram)
        print(ram[68])
        print(ram[17], ram[83])
        print("----------------------------------------------")
        for obj in env.objects:
            x, y = obj.xy
            if x < 160 and y < 210:
                opos = obj.xywh
                ocol = obj.rgb
                sur_col = make_darker(ocol)
                mark_bb(obs, opos, color=sur_col)
        _, ax = plt.subplots(1, 1, figsize=(8, 15))
        ax.imshow(obs)
        # plt.imshow(obs)
        plt.show()
        prev_ram = ram
    if terminated or truncated:
        observation, info = env.reset()
env.close()
