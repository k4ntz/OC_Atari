import pytest
import numpy as np
from ocatari.core import OCAtari


@pytest.mark.parametrize(
    "env_name, mode",
    [
        ("ALE/Pong-v5", "ram"),
        ("ALE/Freeway-v5", "ram"),
        ("ALE/Pong-v5", "vision"),
        ("ALE/Freeway-v5", "vision"),
    ]
)
def test_object_state_size(env_name, mode):
    """
    Test object detection with the RAM mode.
    """
    env = OCAtari(env_name=env_name, mode=mode, obs_mode="obj")
    env.reset()

    action = env.action_space.sample()  # pick random action
    obs, reward, truncated, terminated, info = env.step(action)

    assert obs.shape == env._env.observation_space.shape
    env.close()


def test_object_extraction_properties():
    """
    Test properties of objects extracted from RAM and Vision modes.
    """
    env = OCAtari(env_name="ALE/Pong-v5", mode="both", obs_mode="obj")
    env.reset()
    env.detect_objects()  # Use both RAM and vision-based detection
    for obj in env.objects:
        assert hasattr(
            obj, 'category'), "Extracted object should have a category attribute."
        assert hasattr(
            obj, 'xy'), "Extracted object should have an xy attribute (position)."
        assert hasattr(
            obj, 'wh'), "Extracted object should have a wh attribute (width and height)."
    env.close()


def test_object_extraction_count():
    """
    Test the count of objects extracted in RAM and Vision modes.
    """
    env = OCAtari(env_name="ALE/Pong-v5", mode="both", obs_mode="obj")
    env.reset()
    env.detect_objects()  # Use both RAM and vision-based detection
    num_objects = len(env.objects)
    assert num_objects == 3, "There should be 3 objects detected."
    env.close()


def test_object_extraction_consistency():
    """
    Test consistency of object extraction between steps.
    """
    env = OCAtari(env_name="ALE/Pong-v5", mode="ram", obs_mode="obj")
    env.reset()
    env.detect_objects()
    initial_objects = env.objects.copy()
    env.step(0)
    env.detect_objects()
    new_objects = env.objects.copy()
    assert len(initial_objects) == len(
        new_objects), "The number of detected objects should remain consistent between steps."
    env.close()


def test_object_extraction_category_types():
    """
    Test that object categories are extracted correctly and are non-empty strings.
    """
    env = OCAtari(env_name="ALE/Pong-v5", mode="ram", obs_mode="obj")
    env.reset()
    env.detect_objects()
    for obj in env.objects:
        assert isinstance(
            obj.category, str), "Object category should be a string."
        assert len(
            obj.category) > 0, "Object category should not be an empty string."
    env.close()
