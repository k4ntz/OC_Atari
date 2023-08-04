from .utils import find_objects, find_mc_objects
from .game_objects import GameObject
import numpy as np
import matplotlib as plt


class Player(GameObject):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.rgb = 192,192,192
        self.hud = False

class Car(GameObject):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.rgb = 192,192,192
        self.hud = False

class PlayerScore(GameObject):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.rgb =132,144,252
        self.hud = True


def _detect_objects_enduro(objects, obs, hud=False):
    # detection and filtering
    objects.clear()


    
    

    if hud:
        pass