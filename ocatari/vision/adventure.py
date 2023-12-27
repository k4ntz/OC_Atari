from .game_objects import GameObject
from .utils import find_objects, find_mc_objects, most_common_color
import numpy as np

def _detect_objects_adventure(objects, obs, hud=False):
    objects.clear()

