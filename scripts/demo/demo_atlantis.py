# appends parent path to syspath to make ocatari importable
# like it would have been installed as a package
import sys
import random
import matplotlib.pyplot as plt
sys.path.insert(0, '../../') # noqa

from ocatari.core import OCAtari
from ocatari.vision.utils import mark_bb, make_darker
from ocatari.utils import load_agent, parser
from copy import deepcopy

game_name = "Atlantis"
MODE = "vision"
MODE = "revised"
HUD = True
env = OCAtari(game_name, mode=MODE, hud=HUD, render_mode='rgb_array')
observation, info = env.reset()
prev_ram = None


def tamper_state(env, ram_poses=[50, 51, 54], lambda_func=lambda x: x+20, to_exclude=[]):
    # import ipdb;ipdb.set_trace()
    fig, axes = plt.subplots(1, 3, sharey=True)
    current_obs = deepcopy(env._get_obs())
    cram = deepcopy(env.get_ram())
    for ram_pos in ram_poses:
        cram_at_pos = cram[ram_pos]
        print(cram, " -> ", end="")
        nram_at_pos = max(0, min(lambda_func(cram_at_pos), 255))
        env.set_ram(ram_pos, nram_at_pos)
    nram = env.get_ram()
    import ipdb;ipdb.set_trace()
    # new_state, _, _, _, _ = env.step(0)
    new_obs = env.render()
    diff_obs = current_obs - new_obs
    for ax, obs, val in zip(axes, [current_obs, new_obs, diff_obs], [cram_at_pos, nram_at_pos, ""]):
        ax.imshow(obs)
        ax.set_title(f"RAM[{ram_pos}] -> {val}")
    plt.tight_layout()
    plt.show()


opts = parser.parse_args()

if opts.path:
    agent = load_agent(opts, env.action_space.n)

for i in range(10000):
    if opts.path is not None:
        action = agent.draw_action(env.dqn_obs)
    else:
        # action = random.randint(0, 3)
        action = random.randint(0, 1)
        action = 0
    if i % 5:
        action = 1
    print(action)
    obs, reward, terminated, truncated, info = env.step(action)
    ram = env._env.unwrapped.ale.getRAM()
    tamper_state(env)
    # import ipdb; ipdb.set_trace()
    # if i % 1 == 0:
    #     print(env.objects)
    #     print(ram)
    #     for obj in env.objects:
    #         x, y = obj.xy
    #         if x < 160 and y < 210 and obj.visible:
    #             opos = obj.xywh
    #             ocol = obj.rgb
    #             sur_col = make_darker(ocol)
    #             mark_bb(obs, opos, color=sur_col)
    #     plt.imshow(obs)
    #     plt.show()
    #     # import ipdb;ipdb.set_trace()
    #     # env.detect_objects(env.objects, obs, "Atlantis")
    #     prev_ram = ram
    if terminated or truncated:
        observation, info = env.reset()
env.close()
