# appends parent path to syspath to make ocatari importable
# like it would have been installed as a package
import sys
import matplotlib.pyplot as plt
sys.path.insert(0, '../../') # noqa

from ocatari.core import OCAtari
from ocatari.vision.utils import mark_bb, make_darker
from ocatari.utils import load_agent, parser


game_name = "MontezumaRevenge"
MODE = "revised"
# MODE = "vision"
HUD = True
env = OCAtari(game_name, mode=MODE, hud=HUD, render_mode='rgb_array')
obs, info = env.reset()

opts = parser.parse_args()

if opts.path:
    agent = load_agent(opts, env.action_space.n)

# level
# env._env.unwrapped.ale.setRAM(57, 9)

# room
# env._env.unwrapped.ale.setRAM(3, 10)

# player
# env._env.unwrapped.ale.setRAM(42, 150)
env._env.unwrapped.ale.setRAM(43, 160)

# env._env.unwrapped.ale.setRAM(44, 100)
# env._env.unwrapped.ale.setRAM(45, 240)

# items
env._env.unwrapped.ale.setRAM(65, 128)

for i in range(1000):
    # if opts.path is not None:
    #     action = agent.draw_action(env.dqn_obs)
    # else:
    #     action = 0
    # obs, reward, terminated, truncated, info = env.step(action)
    # if i > 30:
    #     env._env.unwrapped.ale.setRAM(42, 80)
    #     env._env.unwrapped.ale.setRAM(43, 200)
    #     obs, reward, terminated, truncated, info = env.step(0)  # env.step(env.action_space.sample())
    # else:
    #     obs, reward, terminated, truncated, info = env.step(0)
    # obs, reward, terminated, truncated, info = env.step(0)
    # obs, reward, terminated, truncated, info = env.step(3)
    if i < 4:
        obs, reward, terminated, truncated, info = env.step(3)
    # elif i == 4:
    #     env._env.unwrapped.ale.setRAM(42, 25)
    else:
        obs, reward, terminated, truncated, info = env.step(0)
        # obs, reward, terminated, truncated, info = env.step(1)
    
    # if i < 25:
    #     obs, reward, terminated, truncated, info = env.step(0)
    #     obs, reward, terminated, truncated, info = env.step(1)
    # elif i == 25:
    #     env._env.unwrapped.ale.setRAM(42, 25)
    #     env._env.unwrapped.ale.setRAM(43, 240)
    #     obs, reward, terminated, truncated, info = env.step(0)
    # else:
    #     obs, reward, terminated, truncated, info = env.step(4)

    if i % 5 == 0:
        # obse2 = deepcopy(obse)
        print(env.objects)
        ram = env._env.unwrapped.ale.getRAM()
        # print(ram)
        print(ram[34])
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
