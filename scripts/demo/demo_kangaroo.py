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
MODE = "revised"
HUD = True
env = OCAtari(game_name, mode=MODE, hud=HUD, render_mode='rgb_array')
observation, info = env.reset()

opts = parser.parse_args()

if opts.path:
    agent = load_agent(opts, env.action_space.n)

# env._env.unwrapped.ale.setRAM(36, 1)
# snapshot = pickle.load(open("lvl3.pkl", "rb"))
# env._env.env.env.ale.restoreState(snapshot)

for i in range(1000):
    if opts.path is not None:
        action = agent.draw_action(env.dqn_obs)
    else:
        action = 6
    obs, reward, terminated, truncated, info = env.step(action)  # env.step(6) for easy movement

    if i%10 == 0 and i > 60:
        # obse2 = deepcopy(obse)
        print(env.objects)
        for obj in env.objects:
            x, y = obj.xy
            if x < 160 and y < 210:
                opos = obj.xywh
                ocol = obj.rgb
                sur_col = make_darker(ocol)
                mark_bb(obs, opos, color=sur_col)
        _, ax = plt.subplots(1, 1, figsize=(13, 20))
        ax.imshow(obs)
        plt.show()
    if terminated or truncated:
        observation, info = env.reset()
env.close()
