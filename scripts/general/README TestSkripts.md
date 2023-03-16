`TestSkriptNr1`:
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

`TestSkriptNr2`:
    Uses Gymnasium to creat a game-enviroment.
    This Script lets you set values to a RAM state.
    'target_ram_position' determins which RAM-position will be changed
    'new_ram_value' determins what value the RAM-position will  be set to.

`TestSkriptNr3`:
    Does the same as TestSkriptNr1, but instead of using gymnasium it will call the OCAtari-wrapper.
    Use:
    ```python
    env = OCAtari("insert game name here", mode="raw/revised/vision", render_mode="human/rgb_array")
    ```
    to setup the enviroment.

`testSkriptNr7` can be used to identify for which attribute each RAM state stands
by setting the RAM values for each RAM position or an user-defined slice of the
RAM positions. After each position ipdb stops the game and the rendered image, so
that you can see which object position exactly changed.

Caution this can crash the game!

```python
env = OCAtari("Assault", mode="raw", render_mode="human")  # set game
observation, info = env.reset()
prevRam = None
already_figured_out = []
for i in range(1000):

    ram_value = 9   # set here the RAM value

    for b in range(0, 126):     # loop through the RAM
        obs, reward, terminated, truncated, info = env.step(random.randint(0, 0))
        print(b - 1)
        env.set_ram(b, ram_value)
        env.render()
        ipdb.set_trace()
```
