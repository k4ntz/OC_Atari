import numpy as np
from .game_objects import GameObject
from .utils import find_objects

objects_colors = {}
def _detect_objects_fishingDerby(objects, obs, hud=True):
    objects.clear()
    return objects