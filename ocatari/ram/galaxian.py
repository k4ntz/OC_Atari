from .game_objects import GameObject
from ._helper_methods import _convert_number
import sys


"""
RAM extraction for the game GALAXIAN. Supported modes: ram.
"""

MAX_NB_OBJECTS =  {'Player': 1}
MAX_NB_OBJECTS_HUD =  {'Player': 1}


class Player(GameObject):
    """
    The player figure i.e, the gun.
    """
    
    def __init__(self):
        super().__init__()
        self._xy = 66, 186
        self.wh = 6, 13
        self.rgb = 236, 236, 236
        self.hud = False

# parses MAX_NB* dicts, returns default init list of objects
def _get_max_objects(hud=False):

    def fromdict(max_obj_dict):
        objects = []
        mod = sys.modules[__name__]
        for k, v in max_obj_dict.items():
            for _ in range(0, v):
                objects.append(getattr(mod, k)())    
        return objects

    if hud:
        return fromdict(MAX_NB_OBJECTS_HUD)
    return fromdict(MAX_NB_OBJECTS)


def _init_objects_ram(hud=False):
    """
    (Re)Initialize the objects
    """
    objects = [Player()]

    # if hud:
    #     objects.extend([PlayerScore()])

    return objects


def _detect_objects_ram(objects, ram_state, hud=False):
    """
       For all objects:
       (x, y, w, h, r, g, b)
    """
    player = objects[0]
    player.x, player.y = ram_state[60]+7, 170 
