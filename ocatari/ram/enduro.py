from .game_objects import GameObject, NoObject
from .utils import match_objects
import sys
import math


"""
RAM extraction for the game Enduro.
"""

MAX_NB_OBJECTS = {"Player": 1, "Car": 27}
MAX_NB_OBJECTS_HUD = {"Player": 1, "Car": 27,
                      "NumberOfCars": 4, "PlayerScore": 6, "Level": 1}


class Player(GameObject):

    def __init__(self):
        super().__init__()
        self._xy = 0, 0
        self.wh = (16, 11)
        self.rgb = 192, 192, 192
        self.hud = False


class Car(GameObject):
    def __init__(self, x=0, y=0, w=16, h=10):
        super().__init__()
        self._xy = x, y
        self.wh = w, h
        self.rgb = 192, 192, 192
        self.hud = False


class PlayerScore(GameObject):
    def __init__(self):
        super().__init__()
        self._xy = 0, 0
        self.wh = (16, 10)
        self.rgb = 132, 144, 252
        self.hud = True


class NumberOfCars(GameObject):
    def __init__(self):
        super().__init__()
        self._xy = 0, 0
        self.wh = (16, 10)
        self.rgb = 0, 0, 0
        self.hud = True


class Level(GameObject):
    def __init__(self):
        super().__init__()
        self._xy = 0, 0
        self.wh = (16, 10)
        self.rgb = 0, 0, 0
        self.hud = True


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
    objects = [Player()] + [NoObject()]*7
    if hud:
        objects.extend([NoObject]*12)
    return objects


def _detect_objects_ram(objects, ram_state, hud=False):
    """
    For all 3 objects:
    (x, y, w, h, r, g, b)
    """
    # 106 ram_state is somewhat controlling the y of the player when it's dying by sinking
    # ram 54 was the previous x position migh be important for turns
    x = 77
    if ram_state[46] & 128:
        x += ((~ram_state[46]) >> 1)+2
    else:
        x -= (ram_state[46] >> 1)
    objects[0].xy = x, 89 + ram_state[52]

    # ram 34 changes depending on turn, I guess it is a singed byte value
    car_bb = []
    for i in range(7):
        if ram_state[27+i]:
            car = Car()
            # x = 0

            # # x: 103, 103, 104, 104, 104, 105, 105, 106, 107, 107, 108, 108, 108, 108

            # if ram_state[46]&128:
            #     x = x - (~ram_state[46])
            # else:
            #     x = x + ram_state[46]

            y = 150 - int(1.2*((18-i)*i) + ((ram_state[59] >> 3)*(0.9**i)))
            x = 0

            x_drift = ram_state[46]
            if x_drift & 128:
                x_drift = (-(ram_state[46]))*(-1)

            if not ram_state[27+i] & 16:
                x = 87
            elif ram_state[27+i] & 1:
                x = int((2192 + (7*y))/30) + x_drift
            else:
                # 50  + int(((5*(0.95**i))*i) + ((ram_state[59]>>4)&7)*(0.9**i))
                x = int(((6498 - (23*y))/60) + x_drift)

            car.xy = x, y
            car_bb.append(car.xywh)

    match_objects(objects, car_bb, 1, 7, Car)

    if hud:
        # ram_state[45] indicates the level
        pass
