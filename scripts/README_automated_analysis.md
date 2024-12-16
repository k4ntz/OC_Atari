`automated_analysis` is a test that requires minimal human interaction
to create a pretty good understanding of which ram value is responsible for
which game object.

the only requirement is an already working vision mode.

Unfortunately the change of oc_atari to an object-oriented data representation
made this skript work significantly less effective (needs fixing)

all relevant variables can be set in line 300 following:
```python
    GAME_NAME = "Asterix-v4
    MAXIMUM_X = 160  # right side of screen in rgb_array
    MAXIMUM_Y = 210  # bottom of screen in rgb_array
    DUMP_PATH = None  # path to dump otherwise takes standard
    NEW_DUMP = False  # if True creates new datasets and dumps it overwriting the previous ones
    MIN_CORRELATION = 0.8  # the minimal correlation required for a ram value to be relevant for an object
    DROP_CONSTANTS = True  # if True does not consider not changing variables for objects
    START_FRAME = 100  # selects the frame at which each simulation starts
```
however the skript should work when only setting the GAME_NAME
