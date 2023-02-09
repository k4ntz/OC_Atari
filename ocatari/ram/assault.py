from ._helper_methods import _convert_number
from .game_objects import GameObject
import numpy as np

"""
RAM extraction for the game ASSAULT. Supported modes: raw, revised.
"""


class Player(GameObject):
    def __init__(self):
        self.visible = True
        self._xy = 0, 0
        self.wh = 8, 8
        self.rgb = 214, 214, 214
        self.hud = False


class PlayerMissile(GameObject):
    def __init__(self):
        self.visible = True
        self._xy = 0, 0
        self.wh = 1, 8
        self.rgb = 236, 236, 236
        self.hud = False


class MotherShip(GameObject):
    def __init__(self):
        self.visible = True
        self._xy = 0, 0
        self.wh = 28, 18
        self.rgb = 72, 160, 72
        self.hud = False


class Enemy(GameObject):
    def __init__(self):
        self.visible = True
        self._xy = 0, 0
        self.wh = 8, 16
        self.rgb = 210, 210, 64
        self.hud = False


class EnemyMissile(GameObject):
    def __init__(self):
        self.visible = True
        self._xy = 0, 0
        self.wh = 1, 6
        self.rgb = 255, 255, 255
        self.hud = False


class PlayerScore(GameObject):
    def __init__(self):
        self.visible = True
        self._xy = 0, 0
        self.rgb = 195, 144, 61
        self.wh = 6, 8
        self.hud = True

    def __eq__(self, o):
        return isinstance(o, PlayerScore) and self.xy == o.xy


class Lives(GameObject):
    def __init__(self):
        self.visible = True
        self._xy = 0, 0
        self.rgb = 195, 144, 61
        self.wh = 8, 8
        self.hud = True


class Health(GameObject):
    def __init__(self):
        self.visible = True
        self._xy = 96, 192
        self.rgb = 72, 160, 72
        self.wh = 8, 8
        self.hud = True


def _init_objects_assault_ram(hud=False):
    """
    (Re)Initialize the objects
    """
    objects = []
    return objects


def _detect_objects_assault_revised(objects, ram_state, hud=False):
    """
    For all objects:
    (x, y, w, h, r, g, b)
    """
    pass


def _detect_objects_assault_raw(info, ram_state):
    """
    O: NOP
    1:
    2: shoot
    3: move right
    """

    info["score"] = _convert_number(ram_state[0]) * 10000 + _convert_number(ram_state[1]) * 100 + \
                    _convert_number(ram_state[2])
    info["player_x"] = ram_state[16]    # start at x = 134
    info["player_missile_x"] = ram_state[39]    # start at x = 182
    info["enemy_x"] = ram_state[33:36]
    info["mother_ship_color"] = ram_state[12]
    info["mother_ship_x"] = ram_state[69]
    info["healt_color"] = ram_state[21]