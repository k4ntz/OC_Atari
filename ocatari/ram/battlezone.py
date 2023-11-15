from .game_objects import GameObject, ValueObject
from ._helper_methods import number_to_bitfield
import sys 

MAX_NB_OBJECTS = {"Player": 1, "Blue_Tank": 1, "Crosshair": 1, "Radar": 1, "Radar_Content": 10}
MAX_NB_OBJECTS_HUD = {"Player": 1, "Blue_Tank": 1, "Crosshair": 1, "Radar": 1, "Radar_Content": 10, "Score": 1, "Life": 5}# 'Score': 1}

class Player(GameObject):
    def __init__(self):
        super(Player, self).__init__()
        self._xy = 19, 140
        self.wh = (122, 38)
        self.rgb = 26, 102, 26
        self.hud = False

class Crosshair(GameObject):
    def __init__(self):
        super(Crosshair, self).__init__()
        self._xy = 78, 79
        self.wh = (1, 6)
        self.rgb = 0, 0, 0
        self.hud = False

class Shot(GameObject):
    def __init__(self):
        super(Shot, self).__init__()
        self._xy = 78, 79
        self.wh = (1, 3)
        self.rgb = 236, 236, 236
        self.hud = False


class Radar(GameObject):
    def __init__(self):
        super(Radar, self).__init__()
        self._xy = 74, 3
        self.wh = (22, 33)
        self.rgb = 111, 210, 111
        self.hud = False


class Radar_Content(GameObject):
    def __init__(self):
        super(Radar_Content, self).__init__()
        self._xy = 74, 3
        self.wh = (7, 7)
        self.rgb = 236, 236, 236
        self.hud = False


class Blue_Tank(GameObject):
    def __init__(self):
        super(Blue_Tank, self).__init__()
        self._xy = 74, 3
        self.wh = (16, 10)
        self.rgb = 24, 80, 128
        self.hud = False


class Red_Thing(GameObject):
    def __init__(self):
        super(Red_Thing, self).__init__()
        self._xy = 74, 3
        self.wh = (16, 10)
        self.rgb = 200, 72, 72
        self.hud = False


class Score(ValueObject):
    def __init__(self):
        super(Score, self).__init__()
        self._xy = 0, 0
        self.wh = (7, 7)
        self.rgb = 252, 252, 84
        self.hud = False


class Life(GameObject):
    def __init__(self):
        super(Life, self).__init__()
        self._xy = 0, 0
        self.wh = (1, 8)
        self.rgb = 252, 252, 84
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


def _init_objects_battlezone_ram(hud=False):
    """
    (Re)Initialize the objects
    """
    objects = [Player(), Crosshair(), Radar()]

    objects.extend([None] * 150)
    if hud:
        objects.extend([None] * 7)
    return objects


def _detect_objects_battlezone_revised(objects, ram_state, hud=False):
    """
    For all 3 objects:
    (x, y, w, h, r, g, b)
    """

    # 48, 47; 54, 53 == x, y
    # 46
    # 73, 81 == type; 1 == blue tank; 2 == other tank; 3 == destroyed; 4 == red thing; 5 == yellow boss

    if ram_state[73]:
        enemy = None
        if ram_state[73] == 1:
            enemy = Blue_Tank()
        elif ram_state[73] == 2:
            enemy = Blue_Tank()
        elif ram_state[73] == 3:
            enemy = Blue_Tank()
        elif ram_state[73] == 4:
            enemy = Red_Thing()
        elif ram_state[73] == 5:
            enemy = Blue_Tank()
        objects[3] = enemy
        if enemy is not None:
            enemy.xy = ram_state[48]+1, 97-ram_state[47]

    if hud:
        pass
