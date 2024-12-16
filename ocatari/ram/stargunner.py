import sys
from .game_objects import GameObject, NoObject
import numpy as np

"""
RAM extraction for the game StarGunner.

"""

MAX_NB_OBJECTS = {'Player': 1, 'PlayerMissile': 1, 'BombThrower': 1, 'Bomb': 1,
                  'FlyingEnemy': 3}
MAX_NB_OBJECTS_HUD = {'Player': 1, 'PlayerMissile': 1, 'BombThrower': 1, 'Bomb': 1,
                      'FlyingEnemy': 3, 'PlayerScore': 1, 'Lives': 1}


class Player(GameObject):
    """
    The player spaceship.
    """

    def __init__(self):
        super().__init__()
        self.xy = 0, 157
        self.wh = 14, 12
        self.rgb = 214, 92, 92
        self.hud = False


class PlayerMissile(GameObject):
    """
    The missiles launched be the player.
    """

    def __init__(self):
        super().__init__()
        self.xy = 0, 157
        self.wh = 8, 1
        self.rgb = 214, 92, 92
        self.hud = False


class BombThrower(GameObject):
    """
    The enemy spaceship which throws bombs.
    """

    def __init__(self):
        super().__init__()
        self.xy = 0, 157
        self.wh = 14, 12
        self.rgb = 169, 169, 169
        self.hud = False


class Bomb(GameObject):
    """
    The bombs thrown by enemy spaceship.
    """

    def __init__(self):
        super().__init__()
        self.xy = 0, 157
        self.wh = 14, 12
        self.rgb = 169, 169, 169
        self.hud = False


class FlyingEnemy(GameObject):
    """
    The flying enemy spaceships.
    """

    def __init__(self):
        super().__init__()
        self.xy = 0, 157
        self.wh = 14, 12
        self.rgb = 169, 169, 169
        self.num_frames_invisible = 0
        self.hud = False


class PlayerScore(GameObject):
    """
    The player's score display (HUD).
    """

    def __init__(self):
        super().__init__()
        self.xy = 56, 3
        self.wh = 6, 9
        self.rgb = 101, 160, 225
        self.score = 0
        self.hud = True

    def __eq__(self, o):
        return isinstance(o, PlayerScore) and self.xy == o.xy


class Lives(GameObject):
    """
    The indicator for the remaining lives of the player (HUD).
    """

    def __init__(self):
        super().__init__()
        self.visible = True
        self.xy = 55, 219
        self.rgb = 214, 92, 92
        self.wh = 5, 5
        self.lives = 2
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

    objects = [Player()] + [PlayerMissile()] + [BombThrower()] + \
        [Bomb()] + [FlyingEnemy()] * 3
    if hud:
        objects += [PlayerScore()] + [Lives()]
    return objects


def _detect_objects_ram(objects, ram_state, hud=False):
    """
    For all objects:
    (x, y, w, h, r, g, b)
    """
    pass
