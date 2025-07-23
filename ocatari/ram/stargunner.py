import sys
from .game_objects import GameObject, ValueObject, NoObject, Orientation, OrientedObject, OrientedNoObject
import numpy as np

"""
RAM extraction for the game StarGunner.

"""

MAX_NB_OBJECTS = {'Player': 1, 'PlayerMissile': 1, 'BombThrower': 1, 'Bomb': 1,
                  'FlyingEnemy': 3}
MAX_NB_OBJECTS_HUD = {'Player': 1, 'PlayerMissile': 1, 'BombThrower': 1, 'Bomb': 1,
                      'FlyingEnemy': 3, 'PlayerScore': 1, 'Lives': 1}


class Player(OrientedObject):
    """
    The player spaceship.
    """

    def __init__(self):
        super().__init__()
        self.xy = 0, 157
        self.wh = 8, 4
        self.rgb = 214, 92, 92
        self.hud = False
        self.orientation = Orientation.E


class PlayerMissile(GameObject):
    """
    The missiles launched be the player.
    """

    def __init__(self):
        super().__init__()
        self.xy = 0, 157
        self.wh = 8, 1
        self.rgb = 72, 160, 72
        self.hud = False


class BombThrower(GameObject):
    """
    The enemy spaceship which throws bombs.
    """

    def __init__(self):
        super().__init__()
        self.xy = 0, 157
        self.wh = 7, 10
        self.rgb = 169, 169, 169
        self.hud = False


class Bomb(GameObject):
    """
    The bombs thrown by enemy spaceship.
    """

    def __init__(self):
        super().__init__()
        self.xy = 0, 157
        self.wh = 4, 1
        self.rgb = 252, 188, 116
        self.hud = False


class FlyingEnemy(GameObject):
    """
    The flying enemy spaceships.
    """

    def __init__(self):
        super().__init__()
        self.xy = 0, 157
        self.wh = 8, 10
        self.rgb = 164, 89, 208
        self.num_frames_invisible = 0
        self.hud = False


class PlayerScore(ValueObject):
    """
    The player's score display (HUD).
    """

    def __init__(self):
        super().__init__()
        self.xy = 82, 14
        self.wh = 12, 7
        self.rgb = 101, 160, 225
        self.value = 0
        self.hud = True

    def __eq__(self, o):
        return isinstance(o, PlayerScore) and self.xy == o.xy


class Lives(ValueObject):
    """
    The indicator for the remaining lives of the player (HUD).
    """

    def __init__(self):
        super().__init__()
        self.visible = True
        self.xy = 56, 23
        self.rgb = 214, 92, 92
        self.wh = 40, 4
        self.value = 5
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

    objects = [OrientedNoObject()] + [NoObject()] * 6
    if hud:
        objects.extend([PlayerScore(), Lives()])
    return objects


def _detect_objects_ram(objects, ram_state, hud=False):
    """
    For all objects:
    (x, y, w, h, r, g, b)
    """
    # player xy = 21, 14
    if ram_state[12] == 2:
        if type(objects[0]) is NoObject:
            objects[0] = Player()
        objects[0].xy = ram_state[21] - 10, ram_state[14] + 33
        objects[0].orientation = Orientation.W if ram_state[19] == 246 else Orientation.E
        
        if ram_state[31]:
            if type(objects[2]) is NoObject:
                objects[2] = BombThrower()
            objects[2].xy = ram_state[31] - 9, 37
        else:
            objects[2] = NoObject()
        
        for i in range(3):
            if not ram_state[15] < i and ram_state[74+i]:
                if type(objects[4+i]) is NoObject:
                    objects[4+i] = FlyingEnemy()
                x, y = ram_state[74+i] - 10, ram_state[71+i] + 33
                w, h = 8, 10
                if not ((ram_state[113] + 1) % 4):
                    w, h = 7, 8
                    x+=1
                objects[4+i].xywh = x, y, w, h
            else:
                objects[4+i] = NoObject()
    else:
        objects[0] = OrientedNoObject()
        objects[2] = NoObject()
        objects[4] = NoObject()
        objects[5] = NoObject()
        objects[6] = NoObject()

    
    if ram_state[40]:
        if type(objects[1]) is NoObject:
            objects[1] = PlayerMissile()
        objects[1].xy = ram_state[40] - 11, ram_state[41] + 32
    else:
        objects[1] = NoObject()
    
    if ram_state[108]:
        if type(objects[3]) is NoObject:
            objects[3] = Bomb()
        objects[3].xy = ram_state[33] - 11, ram_state[34] + 32
    else:
        objects[3] = NoObject()


    if hud:
        #score
        x, w = 82, 12
        for i in range(4):
            if ram_state[3+i] < 10:
                x-=8
                w+=8
        objects[7].xywh = x, 14, w, 7

        # lives
        w = 40
        if ram_state[7] == 2:
            w = 24
        elif ram_state[7] == 1:
            w = 8
        objects[8].wh = w, 4
        objects[8].value = ram_state[7]
    return objects
