import pytest
import numpy as np
from ocatari.core import OCAtari

@pytest.mark.parametrize(
    "env_name, mode, obs_mode",
    [
        ("ALE/Pong-v5", "ram", "ori"),
        ("ALE/Freeway-v5", "ram", "ori"),
        ("ALE/Skiing-v5", "ram", "ori"),
        ("ALE/Kangaroo-v5", "ram", "ori"),
        ("ALE/Pong-v5", "ram", "dqn"),
        ("ALE/Freeway-v5", "ram", "dqn"),
        ("ALE/Skiing-v5", "ram", "dqn"),
        ("ALE/Kangaroo-v5", "ram", "dqn"),
        ("ALE/Pong-v5", "ram", "obj"),
        ("ALE/Freeway-v5", "ram", "obj"),
        ("ALE/Skiing-v5", "ram", "obj"),
        ("ALE/Kangaroo-v5", "ram", "obj"),
        ("ALE/Pong-v5", "vision", "ori"),
        ("ALE/Freeway-v5", "vision", "ori"),
        ("ALE/Skiing-v5", "vision", "ori"),
        ("ALE/Kangaroo-v5", "vision", "ori"),
        ("ALE/Pong-v5", "vision", "dqn"),
        ("ALE/Freeway-v5", "vision", "dqn"),
        ("ALE/Skiing-v5", "vision", "dqn"),
        ("ALE/Kangaroo-v5", "vision", "dqn"),
        ("ALE/Pong-v5", "vision", "obj"),
        ("ALE/Freeway-v5", "vision", "obj"),
        ("ALE/Skiing-v5", "vision", "obj"),
        ("ALE/Kangaroo-v5", "vision", "obj"),
    ]
)
def test_environment_initialization(env_name, mode, obs_mode):
    """
    Test the OCAtari environment initialization with different modes.
    """
    env = OCAtari(env_name=env_name, mode=mode, obs_mode=obs_mode)
    assert env is not None, f"Failed to initialize OCAtari environment: {env_name}"
    assert env.env_name == env_name, "Environment name does not match."
    assert env.mode == mode, "Mode does not match expected."  
    env.close()

@pytest.mark.parametrize(
    "env_name, mode, obs_mode",
    [
        ("ALE/Pong-v5", "ram", "ori"),
        ("ALE/Freeway-v5", "ram", "ori"),
        ("ALE/Pong-v5", "ram", "dqn"),
        ("ALE/Freeway-v5", "ram", "dqn"),
        ("ALE/Pong-v5", "ram", "obj"),
        ("ALE/Freeway-v5", "ram", "obj"),
        ("ALE/Pong-v5", "vision", "ori"),
        ("ALE/Freeway-v5", "vision", "ori"),
        ("ALE/Pong-v5", "vision", "dqn"),
        ("ALE/Freeway-v5", "vision", "dqn"),
        ("ALE/Pong-v5", "vision", "obj"),
        ("ALE/Freeway-v5", "vision", "obj"),
    ]
)
def test_environment_reset(env_name, mode, obs_mode):
    """
    Test resetting the OCAtari environment.
    """
    env = OCAtari(env_name=env_name, mode=mode, obs_mode=obs_mode)
    obs, info = env.reset()
    assert obs is not None, "Observation should not be None after reset."
    assert isinstance(info, dict), "Info should be a dictionary."
    env.close()

@pytest.mark.parametrize(
    "env_name, mode, obs_mode",
    [
        ("ALE/Pong-v5", "ram", "ori"),
        ("ALE/Freeway-v5", "ram", "ori"),
        ("ALE/Pong-v5", "ram", "dqn"),
        ("ALE/Freeway-v5", "ram", "dqn"),
        ("ALE/Pong-v5", "ram", "obj"),
        ("ALE/Freeway-v5", "ram", "obj"),
        ("ALE/Pong-v5", "vision", "ori"),
        ("ALE/Freeway-v5", "vision", "ori"),
        ("ALE/Pong-v5", "vision", "dqn"),
        ("ALE/Freeway-v5", "vision", "dqn"),
        ("ALE/Pong-v5", "vision", "obj"),
        ("ALE/Freeway-v5", "vision", "obj"),
    ]
)
def test_environment_step(env_name, mode, obs_mode):
    """
    Test stepping through the environment.
    """
    env = OCAtari(env_name=env_name, mode=mode, obs_mode=obs_mode)
    env.reset()
    obs, reward, truncated, terminated, info = env.step(0)  # Execute a random action (e.g., action 0)
    assert obs is not None, "Observation should not be None after taking a step."
    assert isinstance(reward, (int, float)), "Reward should be a number."
    assert isinstance(truncated, bool), "Truncated should be a boolean value."
    assert isinstance(terminated, bool), "Terminated should be a boolean value."
    assert isinstance(info, dict), "Info should be a dictionary."
    env.close()

@pytest.mark.parametrize(
    "env_name, mode, obs_mode, seed, frameskip",
    [
        ("ALE/Pong-v5", "ram", "ori", 42, 1),
        ("ALE/Freeway-v5", "ram", "ori", 42, 1),
        ("ALE/Pong-v5", "ram", "dqn", 42, 1),
        ("ALE/Freeway-v5", "ram", "dqn", 42, 1),
        ("ALE/Pong-v5", "ram", "obj", 42, 1),
        ("ALE/Freeway-v5", "ram", "obj", 42, 1),
        #
        ("ALE/Pong-v5", "ram", "ori", 24, 1),
        ("ALE/Freeway-v5", "ram", "ori", 24, 1),
        ("ALE/Pong-v5", "ram", "dqn", 24, 1),
        ("ALE/Freeway-v5", "ram", "dqn", 24, 1),
        ("ALE/Pong-v5", "ram", "obj", 24, 1),
        ("ALE/Freeway-v5", "ram", "obj", 24, 1),
        #
        ("ALE/Pong-v5", "ram", "ori", 42, 4),
        ("ALE/Freeway-v5", "ram", "ori", 42, 4),
        ("ALE/Pong-v5", "ram", "dqn", 42, 4),
        ("ALE/Freeway-v5", "ram", "dqn", 42, 4),
        ("ALE/Pong-v5", "ram", "obj", 42, 4),
        ("ALE/Freeway-v5", "ram", "obj", 42, 4),
        #
        ("ALE/Pong-v5", "vision", "ori", 42, 1),
        ("ALE/Freeway-v5", "vision", "ori", 42, 1),
        ("ALE/Pong-v5", "vision", "dqn", 42, 1),
        ("ALE/Freeway-v5", "vision", "dqn", 42, 1),
        ("ALE/Pong-v5", "vision", "obj", 42, 1),
        ("ALE/Freeway-v5", "vision", "obj", 42, 1),
    ]
)
def test_seeding(env_name, mode, obs_mode, frameskip, seed):
    env = OCAtari(env_name, hud=False, mode=mode, render_mode="rgb_array", render_oc_overlay=False, obs_mode=obs_mode, frameskip=frameskip)


    env.action_space.seed(seed)

    observation, info = env.reset(seed=seed)
    observation, reward, terminated, truncated, info = env.step(0)


    for _ in range(100):
        action = env.action_space.sample()  # pick random action
        obs, reward, truncated, terminated, info = env.step(action)

    obs1 = obs
    env.close()
    env = OCAtari(env_name, hud=False, mode=mode, render_mode="rgb_array", render_oc_overlay=False, obs_mode=obs_mode, frameskip=frameskip)

    env.action_space.seed(seed)

    observation, info = env.reset(seed=seed)
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

@pytest.mark.parametrize(
    "env_name, obs_mode, seed, frameskip",
    [
        ("ALE/Pong-v5", "ori", 42, 1),
        ("ALE/Freeway-v5", "ori", 42, 1),
        ("ALE/Pong-v5", "dqn", 42, 1),
        ("ALE/Freeway-v5",  "dqn", 42, 1),
        ("ALE/Pong-v5", "obj", 42, 1),
        ("ALE/Freeway-v5", "obj", 42, 1),
    ]
)
def test_outputsimilarity_between_modes(env_name, obs_mode, frameskip, seed):
    env = OCAtari(env_name, hud=False, mode="ram", render_mode="rgb_array", render_oc_overlay=False, obs_mode=obs_mode, frameskip=frameskip)


    env.action_space.seed(seed)

    observation, info = env.reset(seed=seed)
    observation, reward, terminated, truncated, info = env.step(0)


    for _ in range(100):
        action = env.action_space.sample()  # pick random action
        obs, reward, truncated, terminated, info = env.step(action)

    obs1 = obs
    env.close()
    env = OCAtari(env_name, hud=False, mode="vision", render_mode="rgb_array", render_oc_overlay=False, obs_mode=obs_mode, frameskip=frameskip)

    env.action_space.seed(seed)

    observation, info = env.reset(seed=seed)
    observation, reward, terminated, truncated, info = env.step(0)


    for _ in range(100):
        action = env.action_space.sample()  # pick random action
        obs, reward, truncated, terminated, info = env.step(action)
    
    obs2 = obs

    if obs_mode == "dqn":
        obs2 = obs2[0]
        obs1 = obs1[0]

    # Compute the difference
    assert np.allclose(obs1,obs2, rtol=2)
    env.close()

@pytest.mark.parametrize(
    "cbs, obs_mode",
    [
        (["ori", "dqn", "obs"], "dqn"),
        (["ori", "dqn"], "dqn"),
        (["ori", "dqn", "obs"], "ori"),
        (["ori", "dqn"], "ori"),
        (["ori", "dqn", "obs"], "obj"),
        (["ori", "dqn"], "obj"),
        (["ori"], "ori"),
    ]
)
def test_multiple_stacks(cbs, obs_mode):
    """
    Test cloning and restoring the state of the environment.
    """
    env = OCAtari(env_name="ALE/Pong-v5", mode="ram", create_buffer_stacks=cbs, obs_mode=obs_mode)
    env.reset()
    
    if "dqn" in cbs or obs_mode == "dqn":
        assert env.create_dqn_stack
    else:
        assert env.create_dqn_stack == False 
    if "obj" in cbs or obs_mode == "obj":
        assert env.create_ns_stack
    else:
        assert env.create_ns_stack == False
    if "ori" in cbs or obs_mode == "ori":
        assert env.create_rgb_stack 
    else:
        assert env.create_rgb_stack == False
    

    action = env.action_space.sample()  # pick random action
    obs, reward, truncated, terminated, info = env.step(action)

    if env.create_dqn_stack:
        assert env._state_buffer_dqn is not None
    else:
        assert env._state_buffer_dqn is None
    if env.create_ns_stack:
        assert env._state_buffer_ns is not None
    else:
        assert env._state_buffer_ns is None
    if env.create_rgb_stack:
        assert env._state_buffer_rgb is not None
    else:
        assert env._state_buffer_rgb is None

def test_clone_restore_state():
    """
    Test cloning and restoring the state of the environment.
    """
    env = OCAtari(env_name="ALE/Pong-v5", mode="ram")
    env.reset()
    initial_state = env._clone_state()
    assert initial_state is not None, "Initial state should not be None."
    env.step(0)  # Take a step to change the state
    env._restore_state(initial_state)  # Restore the previous state
    restored_state = env._clone_state()
    assert np.array_equal(initial_state, restored_state), "Restored state should match the initial state."
    env.close()

def test_step_with_invalid_action():
    """
    Test stepping through the environment with an invalid action.
    """
    env = OCAtari(env_name="ALE/Pong-v5")
    env.reset()
    with pytest.raises(Exception):
        env.step(999)  # Invalid action should raise an exception
    env.close()