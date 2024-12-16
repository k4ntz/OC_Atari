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


@pytest.mark.parametrize("env_name, mode, obs_mode, frameskip, state_nr", [(game, mode, obs_mode, frameskip, state_nr) for game in GAMES for mode in MODES for obs_mode in OBS_MODES for frameskip in FRAMESKIPS for state_nr in get_states(game.split("/")[1].split("-")[0])])
def test_seeding(env_name, mode, obs_mode, frameskip, state_nr):
    env = OCAtari(env_name, hud=False, mode=mode, render_mode="rgb_array",
                  render_oc_overlay=False, obs_mode=obs_mode, frameskip=frameskip)
    load_pickle_state(env, env.game_name, state_nr)

    env.action_space.seed(42)

    observation, info = env.reset(seed=42)
    observation, reward, terminated, truncated, info = env.step(0)

    for _ in range(100):
        action = env.action_space.sample()  # pick random action
        obs, reward, truncated, terminated, info = env.step(action)

    obs1 = obs
    env.close()

    # Reinitialize the environment and load the same pickle state
    env = OCAtari(env_name, hud=False, mode=mode, render_mode="rgb_array",
                  render_oc_overlay=False, obs_mode=obs_mode, frameskip=frameskip)
    load_pickle_state(env, env.game_name, state_nr)

    env.action_space.seed(42)

    observation, info = env.reset(seed=42)
    observation, reward, terminated, truncated, info = env.step(0)

    for _ in range(100):
        action = env.action_space.sample()  # pick random action
        obs, reward, truncated, terminated, info = env.step(action)

    obs2 = obs

    # Compute the difference
    assert np.array_equal(obs1, obs2)
    env.close()


@pytest.mark.parametrize("env_name, obs_mode, frameskip, state_nr", [(game, obs_mode, frameskip, state_nr) for game in GAMES for obs_mode in OBS_MODES for frameskip in FRAMESKIPS for state_nr in get_states(game.split("/")[1].split("-")[0])])
def test_outputsimilarity_between_modes(env_name, obs_mode, frameskip, state_nr):
    env = OCAtari(env_name, hud=False, mode="ram", render_mode="rgb_array",
                  render_oc_overlay=False, obs_mode=obs_mode, frameskip=frameskip)
    load_pickle_state(env, env.game_name, state_nr)

    env.action_space.seed(42)

    observation, info = env.reset(seed=42)
    observation, reward, terminated, truncated, info = env.step(0)

    for _ in range(100):
        action = env.action_space.sample()  # pick random action
        obs, reward, truncated, terminated, info = env.step(action)

    obs1 = obs
    env.close()

    # Reinitialize the environment in a different mode and load the same pickle state
    env = OCAtari(env_name, hud=False, mode="vision", render_mode="rgb_array",
                  render_oc_overlay=False, obs_mode=obs_mode, frameskip=frameskip)
    load_pickle_state(env, env.game_name, state_nr)

    env.action_space.seed(42)

    observation, info = env.reset(seed=42)
    observation, reward, terminated, truncated, info = env.step(0)

    for _ in range(100):
        action = env.action_space.sample()  # pick random action
        obs, reward, truncated, terminated, info = env.step(action)

    obs2 = obs

    # Compute the difference
    assert np.allclose(obs1, obs2, rtol=2)
    env.close()


@pytest.mark.parametrize("env_name, obs_mode, frameskip, state_nr", [(game, obs_mode, frameskip, state_nr) for game in GAMES for obs_mode in OBS_MODES for frameskip in FRAMESKIPS for state_nr in get_states(game.split("/")[1].split("-")[0])])
def test_objects_slots(env_name, obs_mode, frameskip, state_nr):
    env = OCAtari(env_name, hud=False, mode="ram", render_mode="rgb_array",
                  render_oc_overlay=False, obs_mode=obs_mode, frameskip=frameskip)
    load_pickle_state(env, env.game_name, state_nr)
    env.reset()
    object_dict = env.max_objects_per_cat
    object_list = [key for key, count in object_dict.items()
                   for _ in range(count)]

    for _ in range(100):
        action = env.action_space.sample()  # pick random action
        obs, reward, truncated, terminated, info = env.step(action)
        current_objects = env.objects

        print(object_list)
        print(current_objects)
        for type, object in zip(object_list, current_objects):
            assert not object or object.category == type

    env.close()
