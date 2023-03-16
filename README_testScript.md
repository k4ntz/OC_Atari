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
