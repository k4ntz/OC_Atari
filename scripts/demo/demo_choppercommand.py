# appends parent path to syspath to make ocatari importable
# like it would have been installed as a package
import random
import sys
import matplotlib.pyplot as plt
import ipdb
sys.path.insert(0, '../../')  # noqa
import pickle

from ocatari.core import OCAtari
from ocatari.vision.utils import mark_bb, make_darker
from ocatari.utils import load_agent, parser
from ocatari.ram.demonattack import ProjectileHostile

game_name = "ChopperCommandNoFrameskip-v4"
MODE = "vision"
MODE = "revised"
HUD = True
env = OCAtari(game_name, mode=MODE, hud=HUD, render_mode='rgb_array')
observation, info = env.reset()

opts = parser.parse_args()

if opts.path:
    agent = load_agent(opts, env.action_space.n)

# snapshot = pickle.load(open("save.pickle", "rb"))
# env._env.env.env.ale.restoreState(snapshot)

for i in range(100000):
    # if opts.path is not None:
    #     action = agent.draw_action(env.dqn_obs)
    # else:
    #     action = 3
    # if i < 50:
    #     obs, reward, terminated, truncated, info = env.step(4)
    # else:
    #     obs, reward, terminated, truncated, info = env.step(3)
    obs, reward, terminated, truncated, info = env.step(3)
    obs, reward, terminated, truncated, info = env.step(1)  # env.step(6) for easy movement
    # env._env.unwrapped.ale.setRAM(8, 91)
    # env._env.unwrapped.ale.setRAM(68, 0)
    # obs, reward, terminated, truncated, info = env.step(random.randint(-2, 2))
    # env.step(env.action_space.sample())
    if i % 20 == 0:
        # print(env.objects)
        ram = env._env.unwrapped.ale.getRAM()
        # with open('save.pickle', 'wb') as handle:
        #     pickle.dump(env._env.env.env.ale.cloneState(), handle, protocol=pickle.HIGHEST_PROTOCOL)
        # print(ram[97])
        # print(ram[74])
        print(ram[70], ram[94], ram[95])
        
        for obj in env.objects:
            x, y = obj.xy
            if x < 160 and y < 210:
                opos = obj.xywh
                ocol = obj.rgb
                sur_col = make_darker(ocol)
                if isinstance(obj, ProjectileHostile):
                    sur_col = 255, 255, 255
                mark_bb(obs, opos, color=sur_col)
            # mark_point(obs, *opos[:2], color=(255, 255, 0))

        plt.imshow(obs)
        plt.show()

        # ipdb.set_trace()

    if terminated or truncated:
        observation, info = env.reset()
    # modify and display render
env.close()
