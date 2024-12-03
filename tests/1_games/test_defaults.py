import pytest
import numpy as np
import os
import pickle as pkl
from ocatari.core import OCAtari, AVAILABLE_GAMES

# Get GAMES from the environment variable or use default if not set

if os.getenv("GAMES") != None:
    GAMES = [f"ALE/{g}-v5" for g in os.getenv("GAMES").split()]
else:
    GAMES = [f"ALE/{g}-v5" for g in AVAILABLE_GAMES]
    GAMES = ["ALE/Freeway-v5"]

PICKLE_PATH = f"pickle_files"

MODES = ["ram", "vision"]
OBS_MODES = ["ori", "dqn"]
FRAMESKIPS = [1, 4]

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
    pickle_file_path = os.path.join(PICKLE_PATH, game_name, state_nr)
    if os.path.exists(pickle_file_path):
        with open(pickle_file_path, "rb") as f:
            state, objects = pkl.load(f)
            env._ale.restoreState(state)
            env._objects = objects
            print(f"State loaded from {pickle_file_path}")
    else:
        return
        raise FileNotFoundError(f"Pickle file {pickle_file_path} not found.")


@pytest.mark.parametrize("env_name, mode, obs_mode", [(game, mode, obs_mode) for game in GAMES for mode in MODES for obs_mode in OBS_MODES])
def test_environment_initialization(env_name, mode, obs_mode):
    """
    Test the OCAtari environment initialization with different modes.
    """

    env = OCAtari(env_name=env_name, mode=mode, obs_mode=obs_mode)
    assert env is not None, f"Failed to initialize OCAtari environment: {env_name}"
    assert env.env_name == env_name or env.env_name == f"ALE/{env_name}-v5" or env.env_name == f"ALE/{env_name}", "Environment name does not match."
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
    env = OCAtari(env_name=env_name, mode=mode, obs_mode=obs_mode, frameskip=frameskip)
    load_pickle_state(env, env.game_name, state_nr)
    env.reset()
    obs, reward, truncated, terminated, info = env.step(0)  # Execute a random action (e.g., action 0)
    assert obs is not None, "Observation should not be None after taking a step."
    assert isinstance(reward, (int, float)), "Reward should be a number."
    assert isinstance(truncated, bool), "Truncated should be a boolean value."
    assert isinstance(terminated, bool), "Terminated should be a boolean value."
    assert isinstance(info, dict), "Info should be a dictionary."
    env.close()


@pytest.mark.parametrize("env_name, mode, obs_mode, frameskip, state_nr", [(game, mode, obs_mode, frameskip, state_nr) for game in GAMES for mode in MODES for obs_mode in OBS_MODES for frameskip in FRAMESKIPS for state_nr in get_states(game.split("/")[1].split("-")[0])])
def test_seeding(env_name, mode, obs_mode, frameskip, state_nr):
    env = OCAtari(env_name, hud=False, mode=mode, render_mode="rgb_array", render_oc_overlay=False, obs_mode=obs_mode, frameskip=frameskip)
    load_pickle_state(env, env.game_name, state_nr)

    env.action_space.seed(42)

    observation, info = env.reset(seed=42)
    observation, reward, terminated, truncated, info = env.step(0)

    for _ in range(100):
        action = env.action_space.sample()  # pick random action
        obs, reward, truncated, terminated, info = env.step(action)

    obs1 = obs
    env.close()
    env = OCAtari(env_name, hud=False, mode=mode, render_mode="rgb_array", render_oc_overlay=False, obs_mode=obs_mode, frameskip=frameskip)
    load_pickle_state(env, env.game_name, state_nr)

    env.action_space.seed(42)

    observation, info = env.reset(seed=42)
    observation, reward, terminated, truncated, info = env.step(0)

    for _ in range(100):
        action = env.action_space.sample()  # pick random action
        obs, reward, truncated, terminated, info = env.step(action)

    obs2 = obs

    if obs_mode == "dqn":
        obs2 = obs2[0]
        obs1 = obs1[0]

    # Compute the difference
    assert np.array_equal(obs1, obs2)
    env.close()


@pytest.mark.parametrize("env_name, obs_mode, frameskip, state_nr", [(game, obs_mode, frameskip, state_nr) for game in GAMES for obs_mode in OBS_MODES for frameskip in FRAMESKIPS for state_nr in get_states(game.split("/")[1].split("-")[0])])
def test_outputsimilarity_between_modes(env_name, obs_mode, frameskip, state_nr):
    env = OCAtari(env_name, hud=False, mode="ram", render_mode="rgb_array", render_oc_overlay=False, obs_mode=obs_mode, frameskip=frameskip)
    load_pickle_state(env, env.game_name, state_nr)

    env.action_space.seed(42)

    observation, info = env.reset(seed=42)
    observation, reward, terminated, truncated, info = env.step(0)

    for _ in range(100):
        action = env.action_space.sample()  # pick random action
        obs, reward, truncated, terminated, info = env.step(action)

    obs1 = obs
    env.close()
    env = OCAtari(env_name, hud=False, mode="vision", render_mode="rgb_array", render_oc_overlay=False, obs_mode=obs_mode, frameskip=frameskip)
    load_pickle_state(env, env.game_name, state_nr)

    env.action_space.seed(42)

    observation, info = env.reset(seed=42)
    observation, reward, terminated, truncated, info = env.step(0)

    for _ in range(100):
        action = env.action_space.sample()  # pick random action
        obs, reward, truncated, terminated, info = env.step(action)

    obs2 = obs

    if obs_mode == "dqn":
        obs2 = obs2[0]
        obs1 = obs1[0]

    # Compute the difference
    assert np.allclose(obs1, obs2, rtol=2)
    env.close()
