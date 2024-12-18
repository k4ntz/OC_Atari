from ocatari.utils import load_agent
from ocatari import OCAtari
import sys
import torch
sys.path.insert(0, '../')  # noqa
import gymnasium as gym
import pygame
import argparse

parser = argparse.ArgumentParser(
    description="OCAtari run.py Argument Setter")

parser.add_argument(
    "-g", "--game", type=str, default="Seaquest", help="Game to be run"
)

parser.add_argument(
    "-a",
    "--agent",
    type=str,
    default="",
    help="Path to the cleanrl trained agent to be loaded.",
)

parser.add_argument(
    "-o",
    "--obs_mode",
    type=str,
    default="obj",
    help="The observation mode (ori, dqn, obj)",
)

parser.add_argument(
    "-w",
    "--window",
    type=int,
    default=4,
    help="The buffer window size (default = 4)",
)

parser.add_argument(
    "-f",
    "--frameskip",
    type=int,
    default=4,
    help="The frames skipped after each action + 1 (default = 4)",
)

parser.add_argument(
    "-m",
    "--movie",
    type=bool,
    default=False,
    help="Movie or Render",
)

args = parser.parse_args()

env = OCAtari(
    args.game,
    render_mode="rgb_array" if args.movie else "human",
    obs_mode=args.obs_mode,
    mode="ram",
    hud=False,
    render_oc_overlay=True,
    buffer_window_size=args.window,
    frameskip=args.frameskip,
)

if args.movie:
    env = gym.wrappers.RecordVideo(env, f"media/videos")

pygame.init()
if args.agent:
    # agent = load_agent("../OC_Atari/models/Skiing/obj_based_ppo.cleanrl_model", env.action_space.n, env)
    agent, policy = load_agent(args.agent, env, "cpu")
    print(f"Loaded agents from {args.agent}")

obs, _ = env.reset()
obs, _, _, _, _ = env.step(0)
done = False

while not done:
    # Human intervention to end the run
    events = pygame.event.get()
    for event in events:
        if (
            event.type == pygame.KEYDOWN and event.key == pygame.K_q
        ):  # 'Q': Quit
            done = True
    if args.agent:
        dqn_obs = torch.Tensor(obs).unsqueeze(0)
        action = policy(dqn_obs)[0]
    else:
        action = env.action_space.sample()
    # import ipdb; ipdb.set_trace()
    obs, reward, terminated, truncated, _ = env.step(action)
    # print(reward) if reward != 0 else None
    # if reward and args.reward_function:
    #     print(reward)
    if terminated or truncated:
        env.reset()
    # if nstep % 100 == 0:
    #     print(".", end="", flush=True)
    env.render()

if args.movie:
    env.close_video_recorder()
env.close()
