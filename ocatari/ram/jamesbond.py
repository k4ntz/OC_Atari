from .game_objects import GameObject, ValueObject, NoObject
from ._helper_methods import _convert_number
import sys

MAX_NB_OBJECTS = {"Player": 1, "Player_Shot": 1, "Helicopter": 1, "Ice": 1, "Hornet": 1,
                  "Enemy_Shot": 1, "Eruption": 1, "Diver": 1, "Fire_Hole": 1}
MAX_NB_OBJECTS_HUD = {"Player": 1, "Player_Shot": 1, "Helicopter": 1, "Ice": 1, "Hornet": 1,
                      "Enemy_Shot": 1, "Eruption": 1, "Diver": 1, "Fire_Hole": 1, "Score": 1, "Life": 1} 


class Player(GameObject):
    def __init__(self):
        super(Player, self).__init__()
        self._xy = 0, 160
        self.wh = (8, 4)
        self.rgb = 227, 151, 89
        self.hud = False


class Player_Shot(GameObject):
    def __init__(self):
        super(Player_Shot, self).__init__()
        self._xy = 0, 160
        self.wh = (1, 4)
        self.rgb = 227, 151, 89
        self.hud = False


class Helicopter(GameObject):
    def __init__(self):
        super(Helicopter, self).__init__()
        self._xy = 0, 160
        self.wh = (8, 6)
        self.rgb = 167, 26, 26
        self.hud = False


class Hornet(GameObject):
    def __init__(self):
        super(Hornet, self).__init__()
        self._xy = 0, 160
        self.wh = (8, 14)
        self.rgb = 170, 170, 170
        self.hud = False


class Enemy_Shot(GameObject):
    def __init__(self):
        super(Enemy_Shot, self).__init__()
        self._xy = 0, 160
        self.wh = (1, 4)
        self.rgb = 252, 224, 112
        self.hud = False


class Ice(GameObject):
    def __init__(self):
        super(Ice, self).__init__()
        self._xy = 0, 160
        self.wh = (8, 12)
        self.rgb = 45, 87, 176
        self.hud = False


class Fire_Hole(GameObject):
    def __init__(self):
        super(Fire_Hole, self).__init__()
        self._xy = 0, 160
        self.wh = (16, 48)
        self.rgb = 72, 44, 0
        self.hud = False


class Eruption(GameObject):
    def __init__(self):
        super(Eruption, self).__init__()
        self._xy = 0, 125
        self.wh = (32, 15)
        self.rgb = 26, 102, 26
        self.hud = False


class Diver(GameObject):
    def __init__(self):
        super(Diver, self).__init__()
        self._xy = 0, 125
        self.wh = (7, 20)
        self.rgb = 26, 102, 26
        self.hud = False


class Score(ValueObject):
    def __init__(self):
        super(Score, self).__init__()
        self._xy = 95, 15
        self.wh = (6, 7)
        self.rgb = 252, 252, 84
        self.hud = False
        self.value = 0


class Life(GameObject):
    def __init__(self):
        super(Life, self).__init__()
        self._xy = 9, 184
        self.wh = (8, 4)
        self.rgb = 252, 252, 84
        self.hud = False
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
    objects = [Player()]

    objects.extend([NoObject()] * 8)
    if hud:
        objects.extend([Score(), Life()])
    return objects


def _detect_objects_ram(objects, ram_state, hud=False):
    """
    For all 3 objects:
    (x, y, w, h, r, g, b)
    """

    # player x,y == r27 - 1, 50 + r25
    objects[0].xy = ram_state[27] - 1, 50 + ram_state[25]

    # pshot xy = r38, r31
    if ram_state[31] != 128:
        p_shot = Player_Shot()
        objects[1] = p_shot
        p_shot.xy = ram_state[38] - 11, 55 + ram_state[31]
    else:
        objects[1] = NoObject()

    # row1 x,y == r61, 57
    if ram_state[49] != 255:
        if ram_state[49] == 6:
            if type(objects[2]) is NoObject:
                objects[2] = Helicopter()
            objects[2].xy = ram_state[61] - 1, 57
        else:
            if type(objects[3]) is NoObject:
                objects[3] = Ice()
            objects[3].xy = ram_state[61] - 1, 57
    else:
        objects[2] = NoObject()
        objects[3] = NoObject()

    # row2 x,y == r59, 57
    if ram_state[50] != 255:
        if type(objects[4]) is NoObject:
            objects[4] = Hornet()
        objects[4].xy = ram_state[59] - 2, 75
    else:
        objects[4] = NoObject()

    # eshot xy = r39, r30
    if ram_state[30] != 128:
        if type(objects[5]) is NoObject:
            objects[5] = Enemy_Shot()
        objects[5].xy = ram_state[39] - 11, 55 + ram_state[30]
    else:
        objects[5] = NoObject()

    # fire hole x == 43
    # erupt == r51; x == r60; size == r109, 86 == small, 102 == big
    if ram_state[51] == 54 and ram_state[108] == 251:
        if type(objects[6]) is NoObject:
            objects[6] = Eruption()
        if ram_state[109] == 86:
            objects[6].xy = ram_state[60] + 4, 125
            objects[6].wh = 20, 7
        else:
            objects[6].xy = ram_state[60], 125
            objects[6].wh = 32, 15
    elif ram_state[51] == 48:
        if type(objects[7]) is NoObject:
            objects[7] = Diver()
        objects[7].xy = ram_state[60] - 1, 131
    elif ram_state[108] == 250:
        if type(objects[8]) is NoObject:
            objects[8] = Fire_Hole()
        objects[8].xy = ram_state[43], 122
    else:
        objects[8] = NoObject()

    if hud:
        # Score
        x, w = 95, 6
        if ram_state[94] > 15:
            x, w = 55, 46
        elif ram_state[94]:
            x, w = 63, 38
        elif ram_state[93] > 15:
            x, w = 71, 30
        elif ram_state[93]:
            x, w = 79, 22
        elif ram_state[92] > 15:
            x, w = 87, 14
        
        objects[9].xywh = x, 15, w, 7
        objects[9].value = _convert_number(ram_state[28])*10000 + _convert_number(ram_state[29])*100 + _convert_number(ram_state[30])


        # Lives 86
        if ram_state[111]:
            if type(objects[10]) is NoObject:
                objects[10] = Life()
            if ram_state[111] < 3:
                objects[10].wh = 8 + (16*(ram_state[111]-1)), 4
            else:
                objects[10].wh = 40, 4
            objects[10].value = ram_state[111]
        else:
            objects[10] = NoObject()
