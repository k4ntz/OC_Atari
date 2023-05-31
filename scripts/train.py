import sys
from os import path
sys.path.append(path.dirname(path.dirname(path.abspath(__file__)))) # noqa
from ocatari.core import OCAtari #replace with gym env wrapper
#from scobi import Environment
import gymnasium as gym
from stable_baselines3.common.env_checker import check_env
from stable_baselines3.common.vec_env import SubprocVecEnv
from stable_baselines3 import PPO, DQN, A2C
from stable_baselines3.common.evaluation import evaluate_policy
from stable_baselines3.common.logger import configure
from stable_baselines3.common.utils import set_random_seed
from stable_baselines3.common.monitor import Monitor

from typing import Callable
#def make_env(seed):
#    env = Environment(env_name='PongDeterministic-v4', interactive=True, focus_dir="experiments/my_focusfiles", focus_file="properties_pong.yaml", seed=seed)
#    env.reset(seed=seed)
#    return env


env = OCAtari("Pong")
check_env(env)


# TODO: proper seeding
def make_env(rank: int, seed: int = 0) -> Callable:
    def _init() -> gym.Env:
        env = Environment(env_name='PongDeterministic-v4', interactive=True, focus_dir="experiments/my_focusfiles", focus_file="properties_pong.yaml", seed=seed)
        env = Monitor(env)
        env.reset(seed=seed + rank)
        return env

    set_random_seed(seed)
    return _init

def main():
    #env = make_env()
    #check_env(env)
    env = SubprocVecEnv([make_env(i) for i in range(8)], start_method="fork")

    policy_kwargs = dict(normalize_images=False)
    log_path = "baseline_logs/ppo_multiproc"
    new_logger = configure(log_path, ["stdout", "tensorboard"])
    #model = DQN("MlpPolicy", env, buffer_size=10_000, target_update_interval=1_000, exploration_final_eps=0.01, verbose=1, policy_kwargs=policy_kwargs)
    #model = A2C("MlpPolicy", env=env, verbose=1, policy_kwargs=policy_kwargs)
    model = PPO("MlpPolicy", env=env, verbose=1, policy_kwargs=policy_kwargs)
    #model = DQN.load("pong_baseline")
    #model.set_env(env)
    #model.load_replay_buffer("pong_baseline_rb")
    #print(model.policy)
    model.set_logger(new_logger)
    #model.learn(total_timesteps=8_000_000, reset_num_timesteps=False)
    model.learn(total_timesteps=8_000_000)
    model.save("pong_baseline2")
    model.save_replay_buffer("pong_baseline_rb2")


if __name__ == '__main__':
    main()