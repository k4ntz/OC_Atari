from ._helper_methods import _convert_number
from .game_objects import GameObject
import sys

MAX_NB_OBJECTS =  {'Chicken': 2, 'Car': 10}
MAX_NB_OBJECTS_HUD =  {'Chicken': 2, 'Car': 10, 'Score' : 2}

class Chicken(GameObject):
    def __init__(self):
        super(Chicken, self).__init__()
        self._xy = 0, 0
        self.wh = 6, 8
        self.rgb = 252, 252, 84
        self.hud = False


class Car(GameObject):
    def __init__(self):
        super(Car, self).__init__()
        self._xy = 0, 0
        self.wh = 7, 10
        self.rgb = 167, 26, 26
        self.hud = False


class Score(GameObject):
    def __init__(self):
        super(Score, self).__init__()
        self._xy = 49, 5
        self.wh = 6, 8
        self.rgb = 228, 111, 111
        self.hud = True


car_colors = {"car1": [167, 26, 26], "car2": [180, 231, 117], "car3": [105, 105, 15],
              "car4": [228, 111, 111], "car5": [24, 26, 167], "car6": [162, 98, 33],
              "car7": [84, 92, 214], "car8": [184, 50, 50], "car9": [135, 183, 84],
              "car10": [210, 210, 64]
              }


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


def _init_objects_freeway_ram(hud=False):
    """
    (Re)Initialize the objects
    """
    objects = [Chicken(), Chicken()]
    y = 27
    for color in car_colors.values():
        car = Car()
        car.rgb = (*color, )
        car.xy = 0, y
        objects.append(car)
        y += 16

    if hud:
        objects.append(Score())
        s = Score()
        s.xy = 113, 5
        objects.append(s)

    return objects


def _detect_objects_freeway_revised(objects, ram_state, hud=False):
    """
    For all objects:
    (x, y, w, h, r, g, b)
    """
    c1, c2 = objects[:2]
    cars = objects[2:12]
    scores = objects[12:]

    c1.xy = 44, 193 - ram_state[14]
    c2.xy = 108, 193 - ram_state[15]

    for i in range(10):
        car = cars[i]
        x = ram_state[117 - i] - 2
        if x < 2:   # Edges
            x = 160 + x - 1
            car.wh = 160 - x, car.h
        elif x <= 7:
            w = x - 1
            x = 8
            car.wh = w, car.h
        else:
            car.wh = 7, car.h
        car.xy = x, car.y

    if hud:
        if len(scores) < 3 and _convert_number(ram_state[103]) > 10:
            s = Score()
            s.xy = 41, 5
            objects.append(s)


def _detect_objects_freeway_raw(info, ram_state):
    info["chicken1_y"] = ram_state[14]
    info["chicken2_y"] = ram_state[15]
    info["score1"] = _convert_number(ram_state[103])
    info["score2"] = _convert_number(ram_state[104])
    info["car_x"] = ram_state[108:117]
