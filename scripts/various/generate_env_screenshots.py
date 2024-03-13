# appends parent path to syspath to make ocatari importable
# like it would have been installed as a package
import sys
import random
import matplotlib.pyplot as plt
import numpy as np
from pathlib import Path
sys.path.append(str(Path(__file__).parent.parent.parent))
from ocatari.core import OCAtari
from ocatari.vision.utils import mark_bb, make_darker
from ocatari.vision.spaceinvaders import objects_colors
from ocatari.vision.pong import objects_colors
from ocatari.utils import load_agent, parser, make_deterministic



envs = ["Assault", "Asterix", "Atlantis", "Berzerk", "Bowling",
        "Boxing", "Breakout", "Carnival", "Centipede", "FishingDerby", 
        "Freeway", "Frostbite", "Kangaroo", "MontezumaRevenge", "MsPacman", 
        "Pong", "Qbert", "Riverraid", "Seaquest", "Skiing", "SpaceInvaders", "Tennis"]

opt_mode = "ram"
agent_dir = None
save_steps = [1000, 2000, 3000, 5000, 10_000]
shots_dir = Path("env_screenshots")
shots_dir.mkdir(exist_ok=True)

for env_str in envs:
    env = OCAtari(env_str + "-v4", "ram", render_mode='rgb_array', hud=True)
    observation, info = env.reset()

    if agent_dir:
        agent = load_agent(str(Path(agent_dir) / Path(env_str + ".ckpt")), env.action_space.n)
        print(f"Loaded agents from {agent_dir}")


    env.step(2)
    make_deterministic(0, env)
    ax = plt.gca()
    for i in range(100000):
        if i > save_steps[-1]:
            break
        if agent_dir is not None:
            action = agent.draw_action(env.dqn_obs)
        else:
            action = random.randint(0, env.nb_actions-1)
        obs, reward, terminated, truncated, info = env.step(action)
        if i in save_steps:
            for obs, objects_list, title in zip([obs],
                                                    [env.objects],
                                                    ["ram"] if opt_mode == "ram" else ["vision"]):
                for obj in objects_list:
                    opos = obj.xywh
                    ocol = obj.rgb
                    sur_col = make_darker(ocol)
                    mark_bb(obs, opos, color=sur_col)
            ax.set_xticks([])
            ax.set_yticks([])
            #plt.title(f"{opts.mode}: {opts.mode} mode (frame {i})", fontsize=20)
            #plt.imshow(obs)
            fname = Path(f"{env_str}_{i}.png")
            fstr = str(shots_dir / fname)

            out_data = np.repeat(np.repeat(obs, 4, axis=0), 4, axis=1)

            plt.imsave(fstr, out_data)
            print(f"{fname} saved!")

        if terminated or truncated:
            observation, info = env.reset()

    env.close()
