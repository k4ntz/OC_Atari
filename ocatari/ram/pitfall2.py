import math
import sys

import numpy as np

from ._helper_methods import _convert_number
from .utils import match_objects
from .game_objects import GameObject, ValueObject, NoObject

RAM_21 = 0

"""
RAM extraction for the game Pitfall.

"""

MAX_NB_OBJECTS = {"Player": 1, "Frog": 4, "Bat": 4, "Scorpion": 4, "Bird": 4, "ElectricSerpent": 4, "Balloon": 1, "GoldBar": 4,
                  "RedCross": 1, "Rat": 1, "DiamondRing": 1, "Rhonda": 1, "Quickclaw": 1, "Wall": 8, "Ladder": 4, "Platform": 16, "Water": 1}
MAX_NB_OBJECTS_HUD = {"Player": 1, "Frog": 4, "Bat": 4, "Scorpion": 4, "Bird": 4, "ElectricSerpent": 4, "Balloon": 1, "GoldBar": 4,
                      "RedCross": 1, "Rat": 1, "DiamondRing": 1, "Rhonda": 1, "Quickclaw": 1, "Wall": 8, "Ladder": 4, "Platform": 16, "Water": 1,
                      "PlayerScore": 1}


class Player(GameObject):
    """
    The player figure: Pitfall Harry.
    """

    def __init__(self):
        super().__init__()
        self._xy = 0, 0
        self.wh = (4, 21)
        self.rgb = 53, 95, 24
        self.hud = False


class Frog(GameObject):
    """
    The Frog.
    """

    def __init__(self, x=0, y=0, w=7, h=6):
        super().__init__()
        self.xy = x, y
        self.wh = (w, h)
        self.rgb = 53, 95, 24
        self.hud = False


class Bat(GameObject):
    """
    The Bat.
    """

    def __init__(self, x=0, y=0, w=7, h=10):
        super().__init__()
        self.xy = x, y
        self.wh = (w, h)
        self.rgb = 111, 111, 111
        self.hud = False


class Bird(GameObject):
    """
    The Bird.
    """

    def __init__(self, x=0, y=0, w=9, h=8):
        super().__init__()
        self.xy = x, y
        self.wh = (w, h)
        self.rgb = 180, 122, 48
        self.hud = False


class Scorpion(GameObject):
    """
    The scorpions.
    """

    def __init__(self, x=0, y=0, w=0, h=0):
        super().__init__()
        self.xy = x, y
        self.wh = (w, h)
        self.rgb = 236, 236, 236
        self.hud = False


class ElectricSerpent(GameObject):
    """
    The electric serpent.
    """

    def __init__(self, x=0, y=0, w=0, h=0):
        super().__init__()
        self.xy = x, y
        self.wh = (w, h)
        self.rgb = 236, 236, 236
        self.hud = False


class Balloon(GameObject):
    """
    A ballon that transports the player to a higher level.
    """

    def __init__(self):
        super().__init__()
        self.xy = 0, 0
        self.wh = (7, 27)
        self.rgb = 167, 26, 26
        self.hud = False


class RedCross(GameObject):
    """
    The red cross. Is a checkpoint.
    """

    def __init__(self):
        super().__init__()
        self.xy = 0, 0
        self.wh = (7, 7)
        self.rgb = 163, 57, 21
        self.hud = False


class GoldBar(GameObject):
    """
    The collectable gold bars.
    """

    def __init__(self, x=0, y=0, w=7, h=14):
        super().__init__()
        self.xy = x, y
        self.wh = (w, h)
        self.rgb = 252, 252, 84
        self.hud = False


class DiamondRing(GameObject):
    """
    The collectable diamond rings.
    """

    def __init__(self):
        super().__init__()
        self.xy = 0, 0
        self.wh = (5, 11)
        self.rgb = 252, 252, 84
        self.hud = False


class Rhonda(GameObject):
    """
    The friend to be rescued.
    """

    def __init__(self):
        super().__init__()
        self.xy = 0, 0
        self.wh = (5, 19)
        self.rgb = 110, 156, 66
        self.hud = False


class Quickclaw(GameObject):
    """
    The dancing cat to be rescued.
    """

    def __init__(self):
        super().__init__()
        self.xy = 0, 0
        self.wh = (7, 21)
        self.rgb = 162, 162, 42
        self.hud = False


class Rat(GameObject):
    """
    The rat. Can be collected.
    """

    def __init__(self):
        super().__init__()
        self.xy = 0, 0
        self.wh = (8, 8)
        self.rgb = 192, 192, 192
        self.hud = False


class Platform(GameObject):
    """
    Permanent platforms.
    """

    def __init__(self, x=0, y=0, w=8, h=4, *args, **kwargs):
        super().__init__()
        self._xy = x, y
        self.wh = w, h
        self.rgb = 187, 187, 53
        self.hud = False


class Wall(GameObject):
    """
    The underground brick walls.
    """

    def __init__(self, x=0, y=0, w=4, h=26):
        super().__init__()
        self.xy = 0, 0
        self.wh = (7, 32)
        self.rgb = 105, 105, 15
        self.hud = False


class Ladder(GameObject):
    """
    The escape shafts from the underground.
    """

    def __init__(self, x=0, y=0, w=4, h=16):
        super().__init__()
        self.xy = x, y
        self.wh = w, h
        self.rgb = 105, 105, 15
        self.hud = False


class Water(GameObject):
    """
    The escape shafts from the underground.
    """

    def __init__(self):
        super().__init__()
        self.xy = 8, 150
        self.wh = 152, 33
        self.rgb = 45, 50, 184
        self.hud = False


class PlayerScore(ValueObject):
    """
    The player's score display (HUD).
    """

    def __init__(self):
        super().__init__()
        self.xy = 63, 10
        self.wh = (6, 8)
        self.rgb = 214, 214, 214
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
    objects = [Player()] + [NoObject()]*59
    if hud:
        objects.append(PlayerScore())
    return objects


def _detect_objects_ram(objects, ram_state, hud=False):
    """
    For all 3 objects:
    (x, y, w, h, r, g, b)
    """

    # ram 108 == 4,1 -> x-=3, w+=4; == 3,2 -> x-=1, w+=1;

    x, y = ram_state[103], ram_state[105]+11
    w, h = 4, 21
    if 0 < ram_state[94] < 32:
        w+=4
        h-=5
    elif ram_state[110]&8 or 8 < ram_state[108] < 13:
        x+=1
    else:
        x+=3
    
    if ram_state[108] in (0, 1):
        x-=3
        w+=4
    elif ram_state[108] in (2, 3):
        x-=1
        w+=2
    elif ram_state[108] == 4:
        x-=2
        w+=3
    elif ram_state[108] in (9, 12):
        x-=1
        w+=4
        h-=6
    elif ram_state[108] in (10, 11):
        x-=1
        w+=4
        y+=1
        h-=8
    
    objects[0].xywh = x, y, w, h

    # 33-36 types
    # 38-41 x positions
    # 33/38 are type and position on the top level 36/41 for the bottom
    # 115 y offset on drop-down/ladder movement
    # floor 0 == 172, floor 1 == 127

    # 158, 113, 68

    # types:
    # 32/88 == NoObject
    # 46/64 == Frog
    # 22/42 == Bat
    # 186/208 == Scorpion
    # 230/252 == Bird
    # 4/12/20/28 = Electric serpent
    # 114/142 == Goldbar
    # 56 == red cross
    # 80 == Rat
    # 122/166 == Quickclaw

    y = (ram_state[105] - np.int8(ram_state[115])) - 24 - (ram_state[116]-1)*45
    # if ram_state[102]:
    #     y-=45

    frogs = []
    for i in range(4):
        if ram_state[33+i] == 46:
            x = ram_state[38+i]
            if not (ram_state[23+i])&8:
                x+=1
            if 21 < y+(i*45) - 5 < 183:
                frogs.append((x, y+(i*45)-5, 7, 6))
        elif ram_state[33+i] == 64:
            offset = (118 - ram_state[18+i])>>1
            if 21 < y+(i*45) - 5 - offset < 183:
                frogs.append((ram_state[38+i], y+(i*45)-5-offset, 8, 9))

    match_objects(objects, frogs, 1, 4, Frog)

    bat = []
    for i in range(4):
        if ram_state[33+i] in (22, 42):
            bat_y = y - (25 + (8 - ((ram_state[18+i]%20)>>1))) 
            if 30 < bat_y+(i*45) < 183:
                bat.append((ram_state[38+i]-1, bat_y+(i*45), 7, 10))
    match_objects(objects, bat, 5, 4, Bat)

    scorpion = []
    for i in range(4):
        if 18 < y+(i*45) - 10 < 183 and ram_state[33+i] in (186, 208):
            scorpion.append((ram_state[38+i], y+(i*45) - 10, 8, 12))
    match_objects(objects, scorpion, 9, 4, Scorpion)

    bird = []
    for i in range(4):
        if ram_state[33+i] == 252:
            bird_y = y - 27 + (np.int8(ram_state[18+i])>>1)
            if 22 < bird_y+(i*45) < 183:
                bird.append((ram_state[38+i]-1, bird_y+(i*45), 9, 8))
        elif ram_state[33+i] == 230:
            bird_y = y - 19 + (np.int8(ram_state[18+i])>>1)
            if 19 < bird_y+(i*45) < 183:
                bird.append((ram_state[38+i]-1, bird_y+(i*45), 9, 11))
    match_objects(objects, bird, 13, 4, Bird)

    es = []
    for i in range(4):
        if ram_state[33+i] == 4:
            es_y = y - 33 + (np.int8(ram_state[18+i])>>1)
            if 27 < es_y+(i*45) < 183:
                es.append((ram_state[38+i], es_y+(i*45), 8, 3))

        elif ram_state[33+i] == 12:
            es_y = y - 36 + (np.int8(ram_state[18+i])>>1)
            if 28 < es_y+(i*45) < 183:
                es.append((ram_state[38+i], es_y+(i*45), 8, 2))

        elif ram_state[33+i] == 20:
            es_y = y - 41 + (np.int8(ram_state[18+i])>>1)
            if 27 < es_y+(i*45) < 183:
                es.append((ram_state[38+i], es_y+(i*45), 8, 3))

        elif ram_state[33+i] == 28:
            es_y = y - 44 + (np.int8(ram_state[18+i])>>1)
            if 28 < es_y+(i*45) < 183:
                es.append((ram_state[38+i], es_y+(i*45), 8, 2))

    match_objects(objects, es, 17, 4, ElectricSerpent)

    for i in range(4):
        if ram_state[33+i] == 2:
            ballon_y = y - 33 + (ram_state[18+i]>>1)
            if 3 < ballon_y+(i*45) < 183:
                if type(objects[21]) is NoObject:
                    objects[21] = Balloon()
                objects[21].xy = ram_state[38+i], ballon_y+(i*45)
            else:
                objects[21] = NoObject()
            break
        elif ram_state[108] == 13:
            if 3 < y+(i*45) < 183:
                if type(objects[21]) is NoObject:
                    objects[21] = Balloon()
                objects[21].xy = ram_state[103], ram_state[105] - 16
            else:
                objects[21] = NoObject()
            break
    else:
        objects[21] = NoObject()

    gold = []
    for i in range(4):
        if 16 < y+(i*45) - 17 < 183 and ram_state[33+i] in (114, 142):
            gold.append((ram_state[38+i], y+(i*45)-17, 7, 14))
    match_objects(objects, gold, 22, 4, GoldBar)

    for i in range(4):
        if 24 < y+(i*45) - 5 < 183 and ram_state[33+i] == 56:
            if type(objects[26]) is NoObject:
                objects[26] = RedCross()
            objects[26].xy = ram_state[38+i], y+(i*45)-5
            break
    else:
        objects[26] = NoObject()

    for i in range(4):
        if 22 < y+(i*45) - 13 < 183 and ram_state[33+i] in (80, 96):
            if type(objects[27]) is NoObject:
                objects[27] = Rat()
            objects[27].xy = ram_state[38+i], y+(i*45) - 13
            break
    else:
        objects[27] = NoObject()

    for i in range(4):
        if 22 < y+(i*45) < 183 and ram_state[33+i] == 164:
            if type(objects[28]) is NoObject:
                objects[28] = DiamondRing()
            objects[28].xy = ram_state[38+i] + 1, y+(i*45) - 15
            break
    else:
        objects[28] = NoObject()

    for i in range(4):
        if 9 < y+(i*45) - 18 < 183 and ram_state[33+i] == 204:
            if type(objects[29]) is NoObject:
                objects[29] = Rhonda()
            objects[29].xy = ram_state[38+i] + 1, y+(i*45) - 18
            break
    else:
        objects[29] = NoObject()

    for i in range(4):
        if 9 < y+(i*45) - 20 < 183 and ram_state[33+i] in (122, 166):
            if type(objects[30]) is NoObject:
                objects[30] = Quickclaw()
            objects[30].xy = ram_state[38+i], y+(i*45) - 20
            break
    else:
        objects[30] = NoObject()
    
    walls = []
    for i in range(4):
        if ram_state[53+i]&240 and 10 < y + (45*i) - 29 < 183:
            walls.append((8, y + (45*i) - 29, 8, 20))

        if ram_state[53+i]&15 and 6 < y + (45*i) - 29 < 183:
            walls.append((144, y + (45*i) - 31, 16, 24))
    match_objects(objects, walls, 31, 8, Wall)
    
    ladders = []
    for i in range(4):
        if ram_state[43+i] == 250 and 4 < y + (45*i) - 33 < 183:
            ladders.append((78, y + (45*i) - 33, 4, 26))
    match_objects(objects, ladders, 39, 4, Ladder)

    # ram 9+i == Platforms and holes
    # ram 13+i == no clue some bg shit
    
    platforms = []
    for i in range(4):
        if 30 < y + (45*i) + 1 < 183:
            if ram_state[9+i] == 249:
                platforms.append((8, y + (45*i) + 1, 151, 1))
            elif ram_state[9+i] == 204:
                platforms.append((8, y + (45*i) + 1, 68, 1))
                platforms.append((84, y + (45*i) + 1, 76, 1))
            elif ram_state[18+i] == 140:
                if ram_state[38+i]+1 < 8:
                    x, w = 8, 25
                else:
                    x, w = ram_state[38+i]+1, 32
                platforms.append((x, y + (45*i) + 1, w, 1))
            elif ram_state[9+i] == 218:
                platforms.append((8, y + (45*i) + 1, 44, 1))
                platforms.append((64, y + (45*i) + 1, 12, 1))
                platforms.append((84, y + (45*i) + 1, 12, 1))
                platforms.append((108, y + (45*i) + 1, 52, 1))

    match_objects(objects, platforms, 43, 16, Platform)

    for i in range(4):
        if 9 < y+(i*45) - 20 < 183 and ram_state[9+i] in (142, 187, 232):
            if type(objects[59]) is NoObject:
                objects[59] = Water()
            objects[59].xy = 8, y+(i*45)+3
            if ram_state[9+i+1] == 52:
                objects[59].wh = 152, 82
            break
    else:
        objects[59] = NoObject()

    if hud:

        scr = 0
        for i in range(3):
            if ram_state[71+i] > 15:
                scr = 5-2*i
                break
            elif ram_state[71+i] > 0:
                scr = 4-2*i
                break

        objects[60].xywh = 63 - (scr * 8), 10, 6 + (scr * 8), 8
        objects[60].value = _convert_number(ram_state[71]) * 10000 + _convert_number(ram_state[72]) * 100 +\
            _convert_number(ram_state[73])


def _detect_objects_pitfall_raw(info, ram_state):
    """
    returns unprocessed list with
    ball_x, ball_y, enemy_y, player_y
    """
    info["objects_list"] = ram_state[32:36]
