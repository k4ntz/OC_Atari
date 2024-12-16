import pytest
import numpy as np
import os
import pickle as pkl
from ocatari.core import OCAtari
import warnings

# Get GAMES from the environment variable or use default if not set
if os.getenv("GAMES") != None:
    GAMES = [f"ALE/{g}-v5" for g in os.getenv("GAMES").split()]
else:
    GAMES = ["ALE/Amidar-v5", "ALE/Asterix-v5", "ALE/Asteroids-v5", "ALE/BankHeist-v5", "ALE/Berzerk-v5", "ALE/Bowling-v5", "ALE/Breakout-v5", "ALE/DonkeyKong-v5", "ALE/FishingDerby-v5", "ALE/Freeway-v5", "ALE/Frogger-v5",
             "ALE/Frostbite-v5", "ALE/Gopher-v5", "ALE/IceHockey-v5", "ALE/Kangaroo-v5", "ALE/MontezumaRevenge-v5", "ALE/MsPacman-v5", "ALE/Pong-v5", "ALE/Seaquest-v5", "ALE/Skiing-v5", "ALE/SpaceInvaders-v5", "ALE/Tennis-v5"]

MODES = ["ram", "vision"]
OBS_MODES = ["obj"]
FRAMESKIPS = [1, 4]

PICKLE_PATH = "pickle_files"


def get_states(game_name):
    path = f"{PICKLE_PATH}/{game_name}"
    if os.path.exists(path):
        return [f for f in os.listdir(path) if f.startswith("state_") and f.endswith(".pkl")]
    else:
        return [""]


def load_pickle_state(env, game_name, state_nr):
    """
    Load the state from the pickle file for the given game.
    """
    pickle_file_path = os.path.join(PICKLE_PATH, game_name, f"{state_nr}.pkl")
    if os.path.exists(pickle_file_path):
        with open(pickle_file_path, "rb") as f:
            state, objects = pkl.load(f)
            env._ale.restoreState(state)
            env._objects = objects
            print(f"State loaded from {pickle_file_path}")
    else:
        return
        raise FileNotFoundError(f"Pickle file {pickle_file_path} not found.")


@pytest.mark.parametrize("env_name, mode, obs_mode, state_nr", [(game, mode, obs_mode, state_nr) for game in GAMES for mode in MODES for obs_mode in OBS_MODES for state_nr in get_states(game.split("/")[1].split("-")[0])])
def test_environment_initialization(env_name, mode, obs_mode, state_nr):
    """
    Test the OCAtari environment initialization with different modes.
    """
    env = OCAtari(env_name=env_name, mode=mode, obs_mode=obs_mode)
    load_pickle_state(env, env.game_name, state_nr)
    assert env is not None, f"Failed to initialize OCAtari environment: {env_name}"
    assert env.env_name == env_name, "Environment name does not match."
    assert env.mode == mode, "Mode does not match expected."
    env.close()


@pytest.mark.parametrize("env_name, mode, obs_mode, state_nr", [(game, mode, obs_mode, state_nr) for game in GAMES for mode in MODES for obs_mode in OBS_MODES for state_nr in get_states(game.split("/")[1].split("-")[0])])
def test_environment_reset(env_name, mode, obs_mode, state_nr):
    """
    Test resetting the OCAtari environment.
    """
    env = OCAtari(env_name=env_name, mode=mode, obs_mode=obs_mode)
    load_pickle_state(env, env.game_name, state_nr)
    obs, info = env.reset()
    assert obs is not None, "Observation should not be None after reset."
    assert isinstance(info, dict), "Info should be a dictionary."
    env.close()


@pytest.mark.parametrize("env_name, mode, obs_mode, frameskip, state_nr", [(game, mode, obs_mode, frameskip, state_nr) for game in GAMES for mode in MODES for obs_mode in OBS_MODES for frameskip in FRAMESKIPS for state_nr in get_states(game.split("/")[1].split("-")[0])])
def test_environment_step(env_name, mode, obs_mode, frameskip, state_nr):
    """
    Test stepping through the environment.
    """
    env = OCAtari(env_name=env_name, mode=mode,
                  obs_mode=obs_mode, frameskip=frameskip)
    load_pickle_state(env, env.game_name, state_nr)
    env.reset()
    obs, reward, truncated, terminated, info = env.step(
        0)  # Execute a random action (e.g., action 0)
    assert obs is not None, "Observation should not be None after taking a step."
    assert isinstance(reward, (int, float)), "Reward should be a number."
    assert isinstance(truncated, bool), "Truncated should be a boolean value."
    assert isinstance(
        terminated, bool), "Terminated should be a boolean value."
    assert isinstance(info, dict), "Info should be a dictionary."
    env.close()
