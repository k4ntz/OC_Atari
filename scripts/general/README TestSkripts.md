'TestSkriptNr1':
    Uses Gymnasium to creat a game-enviroment.
    It will print the current RAM state as an array aswell as any values that changed since the last iteration.
    Use:
    ```python
    gym.make("insert game name here", render_mode="human/rgb_array")
    ```
    this will set up the enviroment for the game.
    Use:
    ```python
    observation, reward, terminated, truncated, info = env.step(any number  between 0-8)
    ```
    this will let you choose the input given to the enviroment.

'TestSkriptNr2':
    Uses Gymnasium to creat a game-enviroment.
    This Script lets you set values to a RAM state.
    'target_ram_position' determins which RAM-position will be changed
    'new_ram_value' determins what value the RAM-position will  be set to.

'TestSkriptNr3':
    Does the same as TestSkriptNr1, but instead of using gymnasium it will call the OCAtari-wrapper.
    Use:
    ```python
    env = OCAtari("insert game name here", mode="raw/revised/vision", render_mode="human/rgb_array")
    ```
    to setup the enviroment.
