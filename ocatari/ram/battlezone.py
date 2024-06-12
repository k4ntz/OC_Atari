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
        self.rgb = 66, 136, 176
        self.hud = False


class Yellow_Blue_Tank(GameObject):
    def __init__(self):
        super(Yellow_Blue_Tank, self).__init__()
        self._xy = 74, 3
        self.wh = (16, 10)
        self.rgb = 223, 183, 85
        self.hud = False


class Red_Thing(GameObject):
    def __init__(self):
        super(Red_Thing, self).__init__()
        self._xy = 74, 3
        self.wh = (16, 10)
        self.rgb = 200, 72, 72
        self.hud = False


class Boss(GameObject):
    def __init__(self):
        super(Boss, self).__init__()
        self._xy = 74, 3
        self.wh = (20, 7)
        self.rgb = 223, 183, 85
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


def _init_objects_ram(hud=False):
    """
    (Re)Initialize the objects
    """
    objects = [Player(), Crosshair(), Radar()]

    objects.extend([None] * 150)
    if hud:
        objects.extend([None] * 7)
    return objects


def _detect_objects_ram(objects, ram_state, hud=False):
    """
    For all 3 objects:
    (x, y, w, h, r, g, b)
    """

    # 48, 47; 54, 53 == x, y
    # 46
    # 73, 81 == type; 1 == blue tank; 2 == other tank; 3 == destroyed; 4 == red thing; 5 == yellow boss

    if ram_state[73] and ram_state[48] and ram_state[46]:
        enemy = None
        x, y = ram_state[48]+1, 97-ram_state[47]
        w, h = 16, 10
        if ram_state[46]:
            if ram_state[73] == 1:
                enemy = Blue_Tank()
                if ram_state[46] == 6:
                    x+=3
                    y-=1
                    w-=12
                    h-=6
                if ram_state[46] == 7:
                    x+=2
                    y-=1
                    w-=11
                    h-=6
                elif ram_state[46] == 11:
                    x+=1
                    y-=1
                    w-=10
                    h-=6
                elif ram_state[46] == 12:
                    x-=1
                    y-=1
                    w-=8
                    h-=5
                elif ram_state[46] == 13:
                    x-=1
                    y-=1
                    w-=8
                    h-=5
                elif ram_state[46] == 18:
                    x+=4
                    w-=4
                    h-=3
                elif ram_state[46] == 21:
                    w-=5
                    h-=1
                elif ram_state[46] == 26:
                    w-=4
                elif ram_state[46] == 27:
                    x+=4
                    w-=4
                elif ram_state[46] == 28:
                    x+=2
                    w-=2
                elif ram_state[46] == 30:
                    x+=12
                    w+=4
                elif ram_state[46] == 32:
                    x+=2
                    w-=2
                elif ram_state[46] == 33:
                    h+=5
                elif ram_state[46] == 34:
                    h+=4
                elif ram_state[46] == 35:
                    x+=7
                    w+=4
                    h+=4
                elif ram_state[46] == 36:
                    x+=9
                    w+=8
                    h+=4
                elif ram_state[46] == 39:
                    h+=6
                elif ram_state[46] == 40:
                    h+=6
                elif ram_state[46] == 41:
                    x+=12
                    w+=4
                    h+=7
                elif ram_state[46] == 46:
                    x+=12
                    w+=4
                    h+=7
            elif ram_state[73] == 2:
                enemy = Yellow_Blue_Tank()
                if ram_state[46] == 26:
                    x+=4
                    w-=4
                elif ram_state[46] == 27:
                    x+=4
                    w-=4
                elif ram_state[46] == 28:
                    x+=2
                    w-=2
                elif ram_state[46] == 30:
                    x+=12
                    w+=4
                elif ram_state[46] == 32:
                    x+=2
                    w-=2
                elif ram_state[46] == 33:
                    h+=5
                elif ram_state[46] == 34:
                    h+=4
                elif ram_state[46] == 35:
                    x+=7
                    w+=4
                    h+=4
                elif ram_state[46] == 36:
                    w+=8
                    h+=4
                elif ram_state[46] == 39:
                    h+=6
                elif ram_state[46] == 40:
                    h+=6
                elif ram_state[46] == 41:
                    x+=12
                    w+=4
                    h+=7
                elif ram_state[46] == 46:
                    w+=4
                    h+=7
                elif ram_state[46] == 48:
                    w+=8
                    h+=6
                elif ram_state[46] == 49:
                    w+=12
                    h+=6
            elif ram_state[73] == 3:
                enemy = None
            elif ram_state[81] == 1 and ram_state[73] == 4:
                enemy = Red_Thing()
                if ram_state[47] == 0:
                    x+=2
                    y-=2
                    w=2
                    h=1
                elif ram_state[47] == 1:
                    y-=1
                    w = 5
                    h = 2
                elif ram_state[47] == 2:
                    y-=1
                    w = 6
                    h = 3
                elif ram_state[47] == 3:
                    x-=1
                    y-=1
                    w = 8
                    h = 3
                elif ram_state[47] == 4:
                    x+=2
                    w = 12
                    h = 5
                elif ram_state[47] == 5:
                    h = 5
                elif ram_state[47] == 6:
                    x+=4
                    w = 24
                    h = 6
                elif ram_state[47] == 7:
                    x+=4
                    y+=1
                    w = 24
                    h = 8
                elif ram_state[47] == 8:
                    y+=1
                    w = 32
                    h-=1
                elif ram_state[47] == 9:
                    w = 32
                    h+=1
            elif ram_state[73] == 4:
                enemy = Red_Thing()
                if ram_state[47] == 0:
                    x+=2
                    y-=2
                    w=2
                    h=1
                elif ram_state[47] == 1:
                    y-=1
                    w = 5
                    h = 2
                elif ram_state[47] == 2:
                    y-=1
                    w = 6
                    h = 3
                elif ram_state[47] == 3:
                    x-=1
                    y-=1
                    w = 8
                    h = 3
                elif ram_state[47] == 4:
                    x+=2
                    w = 12
                    h = 5
                elif ram_state[47] == 5:
                    h = 5
                elif ram_state[47] == 6:
                    x+=4
                    w = 24
                    h = 6
                elif ram_state[47] == 7:
                    x+=4
                    y+=1
                    w = 24
                    h = 8
                elif ram_state[47] == 8:
                    y+=1
                    w = 32
                    h-=1
                elif ram_state[47] == 9:
                    w = 32
                    h+=1
            elif ram_state[73] == 5:
                enemy = Boss()
                if ram_state[47] == 7:
                    x+=4
                    y+=1
                    w+=8
                    h-=1
                elif ram_state[47] == 8:
                    x+=4
                    y+=1
                    w+=12
                    h+=1
                elif ram_state[47] == 9:
                    w+=16
                    h+=3
        objects[3] = enemy
        if enemy is not None:
            enemy.xy = x, y
            enemy.wh = w, h
    else:
        objects[3] = None

    if ram_state[81] and ram_state[54]:
        enemy = None
        x, y = ram_state[54]+1, 97-ram_state[53]
        w, h= 16, 10
        if ram_state [52]:
            if ram_state[81] == 1 and ram_state[73] == 1:
                enemy = Blue_Tank()
                if ram_state[46] == 6:
                    x+=3
                    y-=1
                    w-=12
                    h-=6
                elif ram_state[46] == 7:
                    x+=2
                    y-=1
                    w-=11
                    h-=6
                elif ram_state[46] == 11:
                    x+=1
                    y-=1
                    w-=10
                    h-=6
                elif ram_state[46] == 12:
                    x-=1
                    y-=1
                    w-=8
                    h-=5
                elif ram_state[52] == 13:
                    x-=1
                    y-=1
                    w-=8
                    h-=5
                elif ram_state[52] == 18:
                    x+=4
                    w-=4
                    h-=3
                elif ram_state[52] == 21:
                    # w-=5
                    # h-=1
                    pass
                elif ram_state[52] == 26:
                    w-=4
                elif ram_state[52] == 27:
                    x+=4
                    w-=4
                elif ram_state[52] == 28:
                    x+=2
                    w-=2
                elif ram_state[52] == 30:
                    x+=12
                    w+=4
                elif ram_state[52] == 32:
                    x+=2
                    w-=2
                elif ram_state[52] == 33:
                    h+=5
                elif ram_state[52] == 34:
                    h+=4
                elif ram_state[52] == 35:
                    x+=7
                    w+=4
                    h+=4
                elif ram_state[52] == 36:
                    x+=9
                    w+=8
                    h+=4
                elif ram_state[52] == 39:
                    h+=6
                elif ram_state[52] == 40:
                    h+=6
                elif ram_state[52] == 41:
                    x+=12
                    w+=4
                    h+=7
                elif ram_state[52] == 46:
                    x+=12
                    w+=4
                    h+=7
            elif ram_state[81] == 1 and ram_state[73] != 1:
                enemy = Blue_Tank()
                if ram_state[52] == 21:
                    # w-=5
                    # h-=1
                    pass
                elif ram_state[52] == 26:
                    w-=4
                elif ram_state[52] == 27:
                    x+=4
                    w-=4
                elif ram_state[52] == 28:
                    x+=2
                    w-=2
                elif ram_state[52] == 30:
                    x+=12
                    w+=4
                elif ram_state[52] == 32:
                    x+=2
                    w-=2
                elif ram_state[52] == 33:
                    h+=5
                elif ram_state[52] == 34:
                    h+=4
                elif ram_state[52] == 35:
                    x+=7
                    w+=4
                    h+=4
                elif ram_state[52] == 36:
                    x+=9
                    w+=8
                    h+=4
                elif ram_state[52] == 39:
                    h+=6
                elif ram_state[52] == 40:
                    h+=6
                elif ram_state[52] == 41:
                    x+=12
                    w+=4
                    h+=7
                elif ram_state[52] == 46:
                    x+=12
                    w+=4
                    h+=7
            elif ram_state[81] == 2 and ram_state[73] == 1:
                enemy = Yellow_Blue_Tank()
                if ram_state[52] == 21:
                    w-=5
                    h-=1
                elif ram_state[52] == 26:
                    w-=4
                elif ram_state[52] == 27:
                    x+=4
                    w-=4
                elif ram_state[52] == 28:
                    x+=2
                    w-=2
                elif ram_state[52] == 30:
                    x+=12
                    w+=4
                elif ram_state[52] == 32:
                    x+=2
                    w-=2
                elif ram_state[52] == 33:
                    h+=5
                elif ram_state[52] == 34:
                    h+=4
                elif ram_state[52] == 35:
                    x+=7
                    w+=4
                    h+=4
                elif ram_state[52] == 36:
                    x+=9
                    w+=8
                    h+=4
                elif ram_state[52] == 39:
                    h+=6
                elif ram_state[52] == 40:
                    h+=6
                elif ram_state[52] == 41:
                    x+=12
                    w+=4
                    h+=7
                elif ram_state[52] == 46:
                    x+=12
                    w+=4
                    h+=7
            elif ram_state[81] == 2 and ram_state[73] != 1:
                enemy = Yellow_Blue_Tank()
                if ram_state[52] == 21:
                    w-=5
                    h-=1
                elif ram_state[52] == 26:
                    w-=4
                elif ram_state[52] == 27:
                    x+=4
                    w-=4
                elif ram_state[52] == 28:
                    x+=2
                    w-=2
                elif ram_state[52] == 30:
                    x+=12
                    w+=4
                elif ram_state[52] == 32:
                    x+=2
                    w-=2
                elif ram_state[52] == 33:
                    h+=5
                elif ram_state[52] == 34:
                    h+=4
                elif ram_state[52] == 35:
                    x+=7
                    w+=4
                    h+=4
                elif ram_state[52] == 36:
                    x+=9
                    w+=8
                    h+=4
                elif ram_state[52] == 39:
                    h+=6
                elif ram_state[52] == 40:
                    h+=6
                elif ram_state[52] == 41:
                    x+=12
                    w+=4
                    h+=7
                elif ram_state[52] == 46:
                    x+=12
                    w+=4
                    h+=7
            elif ram_state[81] == 3:
                enemy = None
            elif ram_state[81] == 4:
                enemy = Red_Thing()
                if ram_state[53] == 0:
                    x+=2
                    y-=2
                    w=2
                    h=1
                elif ram_state[53] == 1:
                    y-=1
                    w = 5
                    h = 2
                elif ram_state[53] == 2:
                    y-=1
                    w = 6
                    h = 3
                elif ram_state[53] == 3:
                    x-=1
                    y-=1
                    w = 8
                    h = 3
                elif ram_state[53] == 4:
                    x+=2
                    w = 12
                    h = 5
                elif ram_state[53] == 5:
                    h = 5
                elif ram_state[53] == 6:
                    x+=4
                    w = 24
                    h = 6
                elif ram_state[53] == 7:
                    x+=4
                    y+=1
                    w = 24
                    h = 8
                elif ram_state[53] == 8:
                    y+=1
                    w = 32
                    h-=1
                elif ram_state[53] == 9:
                    w = 32
                    h+=1
            elif ram_state[81] == 5:
                enemy = Boss()
                if ram_state[52] == 7:
                    x+=4
                    y+=1
                    w+=8
                    h-=1
                elif ram_state[52] == 8:
                    x+=4
                    y+=1
                    w+=12
                    h+=1
                elif ram_state[52] == 9:
                    w+=16
                    h+=3
        objects[4] = enemy
        if enemy is not None:
            enemy.xy = x, y
            enemy.wh = w, h
    else:
        objects[4] = None

    # r82, r83 = y coordinates
    # no clue about x
    if ram_state[82] != 255:
        con1 = Radar_Content()
        objects[5] = con1
        con1.xy = 94 - int(ram_state[74]/9), 34 - ram_state[82]

    if hud:
        pass
