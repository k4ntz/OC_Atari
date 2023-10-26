# alter_ram_while_playing

`alter_ram_while_playing.py` is a script that allows you to play the game. 
It takes as argument (``-g``) the game that you want to play (e.g. `Pong`), as well as a potential list of RAM values (``-t``) that you want to be printed at each step.

## Altering the RAM
You can pause the Game using `tab`. Once in pause mode, you can alter a RAM value using `enter`.
You will be asked with the position of the RAM that you want to modify, as well as the new value that you want to input. (You have to presse `enter` again to see if your alteration has modified e.g. an object color or position.)

## Saving a snapshot
In Pause mode, you can also press `s` to save a snapshot of the game of the emulator state (using pickle, c.f. [clone_state](https://github.com/mgbellemare/Arcade-Learning-Environment/blob/259f24951d27bdfcb5d7b3f54f1f420ca44b71ef/src/python/env/gym.py#L380)). This allows you to save a state of parts of the games that agents usually don't access.

Check the `snapshots` folder for some snapshots that we already used.
