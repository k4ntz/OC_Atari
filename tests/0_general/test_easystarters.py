import pytest
import numpy as np
from ocatari.core import OCAtari


def test_invalid_game_name():
    """
    Test if the game environments are playable by running a few steps.
    """
    with pytest.raises(Exception):
        env = OCAtari(env_name="AEL/Pong", mode="ram", obs_mode="obj")


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
    env = OCAtari(env_name="ALE/Pong-v5", mode="ram",
                  create_buffer_stacks=cbs, obs_mode=obs_mode)
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
    assert np.array_equal(
        initial_state, restored_state), "Restored state should match the initial state."
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
