import gymnasium as gym
import pytest
from ocatari.core import OCAtari


def _episode_end(env, seed=0):
    """
    Play random actions until the episode ends and return (terminated, truncated).
    """
    env.reset(seed=seed)
    env.action_space.seed(seed)
    while True:
        _, _, terminated, truncated, _ = env.step(env.action_space.sample())
        if terminated or truncated:
            return terminated, truncated


@pytest.mark.parametrize(
    "kwargs, expected",
    [
        ({}, (True, False)),  # game over
        ({"max_episode_steps": 50}, (False, True)),  # time limit
    ]
)
def test_step_flags_match_ale(kwargs, expected):
    """
    Test that step returns terminated and truncated in Gymnasium order, as the wrapped ALE env does.
    """
    ocatari_env = OCAtari(env_name="ALE/Breakout-v5", mode="ram", obs_mode="obj", **kwargs)
    ale_env = gym.make("ALE/Breakout-v5", **kwargs)

    assert _episode_end(ale_env) == expected
    assert _episode_end(ocatari_env) == expected
