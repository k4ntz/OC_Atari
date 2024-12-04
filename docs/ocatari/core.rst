The OCAtari Environments
==============================

The OCAtari class provides an extended interface to interact with Atari 2600 games through Gymnasium, enabling enhanced object tracking and analysis. Below, we provide the documentation for the available methods and attributes.

.. module:: ocatari.core
.. autoclass:: OCAtari

Example
~~~~~~~~~~

    .. code-block:: python
        :caption: Create an OCAtari env and play random moves
        :linenos:

        # Create an OCAtari environment with ram-based object detection and DQN-like observation
        env = OCAtari(env_name="ALE/Pong-v5", mode="ram", obs_mode="dqn")

        # Interact with the environment
        obs = env.reset()
        done = False
        while not done:
            action = env.action_space.sample()  # Sample a random action
            obs, reward, terminated, truncated, info = env.step(action)
            done = terminated or truncated

            # Render the environment with object overlays
            env.render()

Methods
~~~~~~~~~~

.. automethod:: ocatari.core.OCAtari.reset
.. automethod:: ocatari.core.OCAtari.step
.. automethod:: ocatari.core.OCAtari.render
.. automethod:: ocatari.core.OCAtari.getScreenRGB



