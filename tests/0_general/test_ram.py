import pytest
import numpy as np
from ocatari.core import OCAtari


def test_set_get_ram():
    """
    Test setting and getting RAM state in the environment.
    """
    env = OCAtari(env_name="ALE/Pong-v5", mode="ram")
    env.reset()
    initial_ram = env.get_ram()
    assert initial_ram is not None, "Initial RAM state should not be None."
    env.set_ram(5, 10)  # Set a value in RAM for testing
    modified_ram = env.get_ram()
    assert modified_ram[5] == 10, "RAM state at position 5 should be updated to 10."
    env.close()


def test_ram_extraction_values():
    """
    Test the values extracted from RAM to ensure they are within the expected range.
    """
    env = OCAtari(env_name="ALE/Pong-v5", mode="ram")
    env.reset()
    ram = env.get_ram()
    assert ram is not None, "RAM state should not be None."
    assert len(ram) > 0, "RAM state should contain elements."
    assert all(
        0 <= value <= 255 for value in ram), "All RAM values should be in the range 0-255."
    env.close()


def test_ram_extraction_specific_addresses():
    """
    Test specific RAM addresses to verify correct extraction.
    """
    env = OCAtari(env_name="ALE/Pong-v5", mode="ram")
    env.reset()
    ram = env.get_ram()
    assert ram is not None, "RAM state should not be None."
    assert len(ram) > 10, "RAM state should contain enough elements."
    specific_value = ram[10]
    assert isinstance(
        specific_value, np.uint8), "RAM value at specific address should be an integer."
    assert 0 <= specific_value <= 255, "RAM value at specific address should be in the range 0-255."
    env.close()


def test_ram_state_changes():
    """
    Test if the RAM state changes after taking a step.
    """
    env = OCAtari(env_name="ALE/Pong-v5", mode="ram")
    env.reset()
    initial_ram = env.get_ram()
    env.step(0)  # Take a step in the environment
    new_ram = env.get_ram()
    assert not np.array_equal(
        initial_ram, new_ram), "RAM state should change after taking a step."
    env.close()


def test_ram_state_reset():
    """
    Test if the RAM state is reset properly when the environment is reset.
    """
    env = OCAtari(env_name="ALE/Pong-v5", mode="ram")
    env.reset()
    initial_ram = env.get_ram()
    env.step(0)  # Take a step to change the state
    env.reset()  # Reset the environment
    reset_ram = env.get_ram()
    assert np.array_equal(
        initial_ram, reset_ram), "RAM state should be reset to initial values."
    env.close()
