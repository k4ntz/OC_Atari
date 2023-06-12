# appends parent path to syspath to make ocatari importable
# like it would have been installed as a package
import sys
import random
import matplotlib.pyplot as plt
from os import path
sys.path.append(path.dirname(path.dirname(path.dirname(path.abspath(__file__))))) # noqa
from ocatari.core import OCAtari
from ocatari.vision.utils import mark_bb, make_darker
from ocatari.vision.spaceinvaders import objects_colors
from ocatari.vision.pong import objects_colors
from ocatari.utils import load_agent, parser, make_deterministic
from pathlib import Path

envs = ["Assault", "Asterix", "Atlantis", "Berzerk", "Bowling", 
        "Boxing", "Breakout", "Carnival", "Centipede", "FishingDerby", 
        "Freeway", "Frostbite", "Kangaroo", "MontezumaRevenge", "MsPacman", 
        "Pong", "Qbert", "Riverraid", "Seaquest", "Skiing", "SpaceInvaders", "Tennis"]

opt_mode = "revised"
agent_dir = None
save_after_steps = 1000
shots_dir = Path("screenshots")
shots_dir.mkdir(exist_ok=True)

for env_str in envs:
    env = OCAtari(env_str, "revised", render_mode='rgb_array', hud=True)
    observation, info = env.reset()


    if agent_dir:
        agent = load_agent(str(Path(agent_dir) / Path(env_str + ".ckpt")), env.action_space.n)
        print(f"Loaded agents from {agent_dir}")


    env.step(2)
    make_deterministic(0, env)
    ax = plt.gca()
    for i in range(100000):
        if agent_dir is not None:
            action = agent.draw_action(env.dqn_obs)
        else:
            action = random.randint(0, env.nb_actions-1)
        obs, reward, terminated, truncated, info = env.step(action)
        if i == save_after_steps:
            for obs, objects_list, title in zip([obs],
                                                    [env.objects],
                                                    ["ram"] if opt_mode == "revised" else ["vision"]):
                for obj in objects_list:
                    opos = obj.xywh
                    ocol = obj.rgb
                    sur_col = make_darker(ocol)
                    mark_bb(obs, opos, color=sur_col)
                    # mark_point(obs, *opos[:2], color=(255, 255, 0))
            ax.set_xticks([])
            ax.set_yticks([])
            #plt.title(f"{opts.mode}: {opts.mode} mode (frame {i})", fontsize=20)
            #plt.imshow(obs)
            fstr = str(shots_dir / Path(env_str+ ".png"))
            plt.imsave(fstr, obs)
            print(f"{env_str} screenshot saved!")
            break
            #plt.show()


        if terminated or truncated:
            observation, info = env.reset()
        # modify and display render
    env.close()
