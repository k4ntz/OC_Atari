import pytest
import numpy as np
import os
from ocatari.core import OCAtari, OBJv2_SUPPORTED
import warnings

# Get GAMES from the environment variable or use default if not set

if os.getenv("GAMES") != None:
    GAMES = [f"ALE/{g}-v5" for g in os.getenv("GAMES").split() if g in OBJv2_SUPPORTED]
else:
    GAMES = [f"ALE/{g}-v5" for g in OBJv2_SUPPORTED]

MODES = ["ram", "vision"]
OBS_MODES = ["obj"]
FRAMESKIPS = [1,4]


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

@pytest.mark.parametrize("env_name, mode, obs_mode", [(game, mode, obs_mode) for game in GAMES for mode in MODES for obs_mode in OBS_MODES])
def test_environment_reset(env_name, mode, obs_mode):
    """
    Test resetting the OCAtari environment.
    """
    env = OCAtari(env_name=env_name, mode=mode, obs_mode=obs_mode)
    obs, info = env.reset()
    assert obs is not None, "Observation should not be None after reset."
    assert isinstance(info, dict), "Info should be a dictionary."
    env.close()

@pytest.mark.parametrize("env_name, mode, obs_mode, frameskip", [(game, mode, obs_mode, frameskip) for game in GAMES for mode in MODES for obs_mode in OBS_MODES for frameskip in FRAMESKIPS])
def test_environment_step(env_name, mode, obs_mode, frameskip):
    """
    Test stepping through the environment.
    """
    env = OCAtari(env_name=env_name, mode=mode, obs_mode=obs_mode, frameskip=frameskip)
    env.reset()
    obs, reward, truncated, terminated, info = env.step(0)  # Execute a random action (e.g., action 0)
    assert obs is not None, "Observation should not be None after taking a step."
    assert isinstance(reward, (int, float)), "Reward should be a number."
    assert isinstance(truncated, bool), "Truncated should be a boolean value."
    assert isinstance(terminated, bool), "Terminated should be a boolean value."
    assert isinstance(info, dict), "Info should be a dictionary."
    env.close()


@pytest.mark.parametrize("env_name, mode, obs_mode, frameskip", [(game, mode, obs_mode, frameskip) for game in GAMES for mode in MODES for obs_mode in OBS_MODES for frameskip in FRAMESKIPS])
def test_seeding(env_name, mode, obs_mode, frameskip):
    env = OCAtari(env_name, hud=False, mode=mode, render_mode="rgb_array", render_oc_overlay=False, obs_mode=obs_mode, frameskip=frameskip)


    env.action_space.seed(42)

    observation, info = env.reset(seed=42)
    observation, reward, terminated, truncated, info = env.step(0)


    for _ in range(100):
        action = env.action_space.sample()  # pick random action
        obs, reward, truncated, terminated, info = env.step(action)

    obs1 = obs
    env.close()
    env = OCAtari(env_name, hud=False, mode=mode, render_mode="rgb_array", render_oc_overlay=False, obs_mode=obs_mode, frameskip=frameskip)

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
    assert np.array_equal(obs1,obs2)
    env.close()

@pytest.mark.parametrize("env_name, obs_mode, frameskip", [(game, obs_mode, frameskip) for game in GAMES for obs_mode in OBS_MODES for frameskip in FRAMESKIPS])
def test_outputsimilarity_between_modes(env_name, obs_mode, frameskip):
    env = OCAtari(env_name, hud=False, mode="ram", render_mode="rgb_array", render_oc_overlay=False, obs_mode=obs_mode, frameskip=frameskip)


    env.action_space.seed(42)

    observation, info = env.reset(seed=42)
    observation, reward, terminated, truncated, info = env.step(0)


    for _ in range(100):
        action = env.action_space.sample()  # pick random action
        obs, reward, truncated, terminated, info = env.step(action)

    obs1 = obs
    env.close()
    env = OCAtari(env_name, hud=False, mode="vision", render_mode="rgb_array", render_oc_overlay=False, obs_mode=obs_mode, frameskip=frameskip)

    env.action_space.seed(42)

    observation, info = env.reset(seed=42)
    observation, reward, terminated, truncated, info = env.step(0)


    for _ in range(100):
        action = env.action_space.sample()  # pick random action
        obs, reward, truncated, terminated, info = env.step(action)
    
    obs2 = obs
    
    # Compute the difference
    assert np.allclose(obs1,obs2, rtol=10)
    env.close()

@pytest.mark.parametrize("env_name, obs_mode, frameskip", [(game, obs_mode, frameskip) for game in GAMES for obs_mode in OBS_MODES for frameskip in FRAMESKIPS])
def test_identified_objects_after_100_steps(env_name, obs_mode, frameskip):
    env = OCAtari(env_name, hud=False, mode="ram", render_mode="rgb_array", render_oc_overlay=False, obs_mode=obs_mode, frameskip=frameskip)


    env.action_space.seed(42)

    observation, info = env.reset(seed=42)
    observation, reward, terminated, truncated, info = env.step(0)


    for _ in range(100):
        action = env.action_space.sample()  # pick random action
        obs, reward, truncated, terminated, info = env.step(action)

    objects1 = [o.category for o in env.objects]
    env.close()
    env = OCAtari(env_name, hud=False, mode="vision", render_mode="rgb_array", render_oc_overlay=False, obs_mode=obs_mode, frameskip=frameskip)

    env.action_space.seed(42)

    observation, info = env.reset(seed=42)
    observation, reward, terminated, truncated, info = env.step(0)


    for _ in range(100):
        action = env.action_space.sample()  # pick random action
        obs, reward, truncated, terminated, info = env.step(action)
    
    objects2 = [o.category for o in env.objects]

    print(objects1)
    print(objects2)
    assert set(objects1) == set(objects2)
    assert (objects1) == (objects2)

    # Compute the difference
    
    env.close()
