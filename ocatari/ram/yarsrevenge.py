from .game_objects import GameObject, ValueObject, NoObject, Orientation, OrientedObject, OrientedNoObject
from ._helper_methods import _convert_number
import numpy as np
import sys

"""
RAM extraction for the game Yars' Revenge.
"""

MAX_NB_OBJECTS = {"Player": 1, "Enemy": 1, "Swirl": 1, "Enemy_Missile": 1, "Player_Bullet": 1, "Barrier": 1, "Shield_Block": 128}
MAX_NB_OBJECTS_HUD = {"Player": 1, "Enemy": 1, "Swirl": 1, "Enemy_Missile": 1, "Player_Bullet": 1, "Barrier": 1, "Shield_Block": 128, "Score": 1, "Life": 1}


class Player(OrientedObject):
    """
    The player figure i.e., the Yar.
    """

    def __init__(self):
        super().__init__()
        self._xy = 0, 0
        self.wh = (8, 16)
        self.rgb = 169, 128, 240
        self.hud = False
        self.orientation = Orientation.S


class Enemy(GameObject):
    """
    The enemy Qotile.
    """

    def __init__(self):
        super().__init__()
        self._xy = 0, 0
        self.wh = (8, 18)
        self.rgb = 163, 57, 21
        self.hud = False


class Swirl(GameObject):
    """
    The Qotile when transformed into a Swirl, charging at the player.
    """

    def __init__(self):
        super().__init__()
        self._xy = 0, 0
        self.wh = (8, 18)
        self.rgb = 163, 57, 21
        self.hud = False


class Enemy_Missile(GameObject):
    """
    The Destroyer Missles fired by the Qotile.
    """

    def __init__(self):
        super().__init__()
        self._xy = 0, 0
        self.wh = (4, 2)
        self.rgb = 169, 128, 240
        self.hud = False


class Barrier(GameObject):
    """
    The colorful and glittering neutral zone.
    """

    def __init__(self):
        super().__init__()
        self._xy = 0, 0
        self.wh = (28, 190)
        self.rgb = 250, 250, 250
        self.hud = False


class Player_Bullet(GameObject):
    """
    The Energy Missles fired by the player.
    """

    def __init__(self):
        super().__init__()
        self._xy = 0, 0
        self.wh = (1, 2)
        self.rgb = 169, 128, 240
        self.hud = False


class Shield_Block(GameObject):
    """
    The cells of the energy shield protecting the Qotile.
    """

    def __init__(self):
        super().__init__()
        self._xy = 0, 0
        self.wh = 4, 8
        self.rgb = 163, 57, 21
        self.hud = False


class Score(ValueObject):
    def __init__(self):
        super(Score, self).__init__()
        self._xy = 0, 0
        self.wh = (7, 7)
        self.rgb = 78, 50, 181
        self.hud = False
        self.value = 0


class Life(ValueObject):
    def __init__(self):
        super(Life, self).__init__()
        self._xy = 95, 74
        self.wh = (7, 7)
        self.rgb = 78, 50, 181
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
    objects = [OrientedNoObject()]

    objects.extend([NoObject()] * 133)
    if hud:
        objects.extend([NoObject()] * 2)
    return objects


def _detect_objects_ram(objects, ram_state, hud=False):
    """
    For all 3 objects:
    (x, y, w, h, r, g, b)
    """
    if ram_state[53] > 159:
        if type(objects[0]) is OrientedNoObject:
            objects[0] = Player()
        objects[0].xy = ram_state[32], ram_state[31]+3
        objects[0].orientation = [Orientation.S, Orientation.E, Orientation.N, Orientation.W][(ram_state[30]&15)>>2]

        if ram_state[43] >= 145:
            if type(objects[1]) is NoObject:
                objects[1] = Enemy()
            objects[1].xy = ram_state[43], ram_state[42]+3
            objects[2] = NoObject()
        else:
            if type(objects[2]) is NoObject:
                objects[2] = Swirl()
            objects[2].xy = ram_state[43]+4, ram_state[42]+3
            objects[1] = NoObject()

        # Enemy Missile
        if type(objects[3]) is NoObject:
            objects[3] = Enemy_Missile()
        objects[3].xy = ram_state[47], ram_state[46]+2

        # Player Missile
        if abs(ram_state[38]-3-ram_state[32]) > 5 and abs(ram_state[37]-ram_state[31]) > 5:
            if type(objects[4]) is NoObject:
                objects[4] = Player_Bullet()
            objects[4].xy = ram_state[38]-1, ram_state[37]+4
        else:
            objects[4] = NoObject()

        # Adding Barrier
        if ram_state[53] > 159:
            if type(objects[5]) is NoObject:
                objects[5] = Barrier()
            objects[5].xy = 52, 4
        else:
            objects[5] = NoObject()

        # blocks ram 0 to 16 binary coding lsb left to msb right

        for j in range(16):
            for i in range(8):
                if ram_state[j+1] & 2**i:
                    if type(objects[6]) is NoObject:
                        objects[6+(i+(j*8))] = Shield_Block()
                    if j == 15:
                        objects[6+(i+(j*8))].xy = 128 + (i*4), ram_state[26] + 122 - (j*8)
                        objects[6+(i+(j*8))].wh = 4, 7
                    else:
                        objects[6+(i+(j*8))].xy = 128 + (i*4), ram_state[26] + 121 - (j*8)
                else:
                    objects[6+(i+(j*8))] = NoObject()
    else:
        objects[0] = OrientedNoObject()
        objects[1:134] = [NoObject()]*133

    if hud:
        if ram_state[53] < 159:
            x, y, w, h = 95, 48, 7, 7
            # scores ram: 96-98 lives 99
            if ram_state[96] > 15:
                x = 55
                w = 47
            elif ram_state[96]:
                x = 63
                w = 39
            elif ram_state[97] > 15:
                x = 71
                w = 31
            elif ram_state[97]:
                x = 79
                w = 23
            elif ram_state[98] > 15:
                x = 87
                w = 15
            elif ram_state[98]:
                x = 95
                w = 7
            
            
            if type(objects[-2]) is NoObject:
                objects[-2] = Score()
            objects[-2].xywh = x, y, w, h
            objects[-2].value = _convert_number(ram_state[96])*10000 + _convert_number(ram_state[97])*100 + _convert_number(ram_state[98])

            if type(objects[-1]) is NoObject:
                objects[-1] = Life()
            objects[-1].value = ram_state[99]>>4
        else:
            objects[-2], objects[-1] = NoObject(), NoObject()
