from .game_objects import GameObject, ValueObject, NoObject
from .utils import match_objects
from ._helper_methods import _convert_number
import sys
import numpy as np

"""
RAM extraction for the game Road Runner.
"""

MAX_NB_OBJECTS = {"Player_Crosshair": 1, "PlayerShot": 1, "EnemyTank": 1, "EnemyShot": 1}
MAX_NB_OBJECTS_HUD = {"Player_Crosshair": 1, "PlayerShot": 1, "EnemyTank": 1, "EnemyShot": 1, "Score": 1, "Lives": 1, "Clock": 1}


class Player_Crosshair(GameObject):
    """
    The player crosshair, shows where the player is aiming at.
    """

    def __init__(self):
        super().__init__()
        self._xy = 72, 82
        self.wh = (16, 23)
        self.rgb = 236, 236, 236
        self.hud = False


class PlayerShot(GameObject):
    """
    Player shot.
    """

    def __init__(self):
        super().__init__()
        self._xy = 0, 0
        self.wh = (8, 8)
        self.rgb = 1, 1, 1
        self.hud = False


class EnemyTank(GameObject):
    """
    Opposing tanks.
    """

    def __init__(self):
        super().__init__()
        self._xy = 0, 0
        self.wh = (16, 11)
        self.rgb = 1, 1, 1
        self.hud = False


class EnemyShot(GameObject):
    """
    Opposing tanks shot.
    """

    def __init__(self):
        super().__init__()
        self._xy = 0, 0
        self.wh = (16, 11)
        self.rgb = 1, 1, 1
        self.hud = False


class Score(ValueObject):
    """
    The number of enemy tanks defeated (HUD).
    """

    def __init__(self):
        super().__init__()
        self.rgb = 1, 1, 1
        self._xy = 32, 22
        self.wh = (6, 8)
        self.hud = True
        self.value = 0


class Lives(ValueObject):
    """
    The player's lives (HUD).
    """

    def __init__(self):
        super().__init__()
        self.rgb = 184, 50, 50
        self._xy = 32, 175
        self.wh = (6, 8)
        self.hud = True
        self.value = 0


class Clock(ValueObject):
    """
    Clock displaying time of day (HUD).
    """

    def __init__(self):
        super().__init__()
        self.rgb = 236, 236, 236
        self._xy = 83, 10
        self.wh = (14, 8)
        self.hud = True
        self.value = 0

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
    objects = [Player_Crosshair()]
    objects.extend([NoObject()] * 3)
    if hud:
        objects.extend([NoObject(), Lives(), Clock()])
    return objects

offsets = [0, 1, 2, 2, 1, 0, -1, -2, -3, -4, -4, -3, -2, -1]

def _detect_objects_ram(objects, ram_state, hud=False):
    """
    For all 3 objects:
    (x, y, w, h, r, g, b)
    """
    # ram 60 == up and down movement
    # 6 -> every thing moved down by 3 pixels
    # 12 -> neutral
    # 18 -> every thing moved up by 3 pixels

    offset = offsets[(ram_state[60]%28)>>1]

    objects[0].xy = 72, 82 + offset

    # base y == 125
    if ram_state[64] > 4:
        if type(objects[1]) is NoObject:
            objects[1] = PlayerShot()
        size = ram_state[64] - 6
        objects[1].xy = 77 - (size>>1), 101 + size*5 + ram_state[65] + offset
        objects[1].wh = size+4, size+3
    else:
        objects[1] = NoObject()


    # ram 37 == wh
    if 63 < ram_state[37] and ram_state[35] and not ram_state[77]:
        if type(objects[2]) is NoObject:
            objects[2] = EnemyTank()
        size = (ram_state[37]>>4) - 3
        x, y = ram_state[32] - 4 - size, 87 + offset
        w, h = 4 + size, size
        if size < 3:
            y +=2
        elif size == 3:
            y +=1

        if 0 < ram_state[69] < 15:
            w = w>>1
            x+=w
        elif ram_state[69]==15:
            x+= 4 + (size>>2)

        objects[2].xy = x, y
        objects[2].wh = w, h
    else:
        objects[2] = NoObject()

    if ram_state[67]:
        if type(objects[3]) is NoObject:
            objects[3] = EnemyShot()
        size = 32 - ram_state[67]
        y = 89 + offset

        objects[3].xy = ram_state[62] - 1, y
        objects[3].wh = (size>>1)+1, size - 1
    else:
        objects[3] = NoObject()

    if hud:
        if ram_state[53]:
            if type(objects[4]) is NoObject:
                objects[4] = Score()
            objects[4].wh = 6 + (8 * (ram_state[53] - 1)), 8
            objects[4].value = ram_state[53]
        else:
            objects[4] = NoObject()

        if ram_state[40]:
            if type(objects[5]) is NoObject:
                objects[5] = Lives()
            objects[5].wh = 6 + (8 * (ram_state[40] - 1)), 8
            objects[5].value = ram_state[40]
        else:
            objects[5] = NoObject()
        
        objects[6].value = _convert_number(ram_state[49])
        
