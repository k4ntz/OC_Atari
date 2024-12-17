import pytest
import numpy as np
import os
import pickle as pkl
from ocatari.core import OCAtari, AVAILABLE_GAMES
from ocatari.utils import load_agent
import torch

# Get GAMES from the environment variable or use default if not set

GAMES = ["ALE/Skiing"]

MODLE_PATH = f"models/Skiing/obj_based_ppo.cleanrl_model"

MODES = ["ram", ]
OBS_MODES = ["obj"]
FRAMESKIPS = [1, 4]


def load_model(env, game_name, model_path):
    """
    Load the model from the path.
    """
    return load_agent(model_path, env, "cpu")


@pytest.mark.parametrize("env_name, mode, obs_mode", [(game, mode, obs_mode) for game in GAMES for mode in MODES for obs_mode in OBS_MODES])
def test_environment_initialization(env_name, mode, obs_mode):
    """
    Test the OCAtari environment initialization with different modes.
    """

    env = OCAtari(env_name=env_name, mode=mode, obs_mode=obs_mode,
                  frameskip=4, buffer_window_size=2)
    assert env is not None, f"Failed to initialize OCAtari environment: {env_name}"
    assert env.env_name == env_name or env.env_name == f"ALE/{env_name}-v5" or env.env_name == f"ALE/{env_name}", "Environment name does not match."
    assert env.mode == mode, "Mode does not match expected."
    agent, policy = load_model(env, env.game_name, MODLE_PATH)
    assert agent is not None
    assert policy is not None
    env.close()


@pytest.mark.parametrize("env_name, mode, obs_mode, frameskip", [(game, mode, obs_mode, frameskip) for game in GAMES for mode in MODES for obs_mode in OBS_MODES for frameskip in FRAMESKIPS])
def test_environment_step(env_name, mode, obs_mode, frameskip):
    """
    Test stepping through the environment.
    """
    env = OCAtari(env_name=env_name, mode=mode,
                  obs_mode=obs_mode, frameskip=frameskip, buffer_window_size=2)
    agent, policy = load_model(env, env.game_name, MODLE_PATH)
    env.reset()
    obs, reward, truncated, terminated, info = env.step(0)
    # Execute a random action (e.g., action 0)
    assert obs is not None, "Observation should not be None after taking a step."
    assert isinstance(reward, (int, float)), "Reward should be a number."
    assert isinstance(truncated, bool), "Truncated should be a boolean value."
    assert isinstance(
        terminated, bool), "Terminated should be a boolean value."
    assert isinstance(info, dict), "Info should be a dictionary."

    dqn_obs = torch.Tensor(obs).unsqueeze(0)
    action = policy(dqn_obs)[0]
    assert action is (int, float)
    obs, reward, truncated, terminated, info = env.step(action)
    env.close()
