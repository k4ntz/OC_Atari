from typing import Tuple
from ._helper_methods import _convert_number
from .game_objects import GameObject, NoObject
from .utils import match_objects
import sys
"""
RAM extraction for the game ASTEROIDS. Supported modes: raw

Revised is missing the x-Position for Asteroids and Player. The RAM states for these values are found (look at raw) but
they were not interpretable. One x Value corresponds to multiple positions on the rendered image. So either there is
another RAM state which separates them into quadrants or the x-Axis is moving.
"""

# Asteroid count can get really high
MAX_NB_OBJECTS = {'Player': 1, 'Asteroid': 30, 'PlayerMissile': 2}
MAX_NB_OBJECTS_HUD = {'Player': 1, 'Asteroid': 30,
                      'PlayerMissile': 2, 'Lives': 1, 'PlayerScore': 1}


class Player(GameObject):
    """
    The player figure i.e., the space ship on patrol.
    """

    def __init__(self):
        super().__init__()
        self._xy = 84, 99
        self.wh = 5, 10
        self.rgb = 240, 128, 128
        self.hud = False
        self.orientation = 0

    @property
    def xy(self):
        return self._xy

    @xy.setter
    def xy(self, value):
        self._xy = value

    @property
    def _nsrepr(self):
        return [self.x, self.y, self.orientation]

    @property
    def _ns_meaning(self):
        return ["POSITION", "ORIENTATION"]

    @property
    def _ns_types(self):
        return [Tuple[int, int], Tuple[int]]


class Asteroid(GameObject):
    """
    The asteroid boulders.
    """

    def __init__(self, x=8, y=87, w=16, h=28):
        super().__init__()
        self._xy = x, y
        self.wh = w, h
        self.rgb = 180, 122, 48
        self.hud = False

    @property
    def xy(self):
        return self._xy

    @xy.setter
    def xy(self, value):
        self._xy = value


class PlayerMissile(GameObject):
    """
    The photon torpedoes that can be fired from the space ship.
    """

    def __init__(self):
        super().__init__()
        self._xy = 0, 0
        self.wh = 1, 2
        self.rgb = 117, 181, 239
        self.hud = False

    @property
    def xy(self):
        return self._xy

    @xy.setter
    def xy(self, value):
        self._xy = value


class PlayerScore(GameObject):
    """
    The player's score display (HUD).
    """

    def __init__(self):
        super().__init__()
        self._xy = 68, 5
        self.rgb = 184, 50, 50
        self.wh = 12, 10
        self.hud = True

    @property
    def xy(self):
        return self._xy

    @xy.setter
    def xy(self, value):
        self._xy = value

    def __eq__(self, o):
        return isinstance(o, PlayerScore) and self.xy == o.xy


class Lives(GameObject):
    """
    The indicator for remaining lives of the player (HUD).
    """

    def __init__(self):
        super().__init__()
        self._xy = 132, 5
        self.rgb = 184, 50, 50
        self.wh = 12, 10
        self.hud = True

    @property
    def xy(self):
        return self._xy

    @xy.setter
    def xy(self, value):
        self._xy = value


class NoObjectPlayer(NoObject):
    """
    A placeholder class for empty slots where no game object is present.
    """

    def __init__(self):
        super().__init__()
        self.orientation = 0

    @property
    def xy(self):
        return self._xy

    @xy.setter
    def xy(self, value):
        self._xy = value

    @property
    def _nsrepr(self):
        return [self.x, self.y, self.orientation]

    @property
    def _ns_meaning(self):
        return ["POSITION", "ORIENTATION"]

    @property
    def _ns_types(self):
        return [Tuple[int, int], Tuple[int]]


asteroids_colors = {"brown": [180, 122, 48], "purple": [104, 72, 198], "yellow": [136, 146, 62],
                    "lightyellow": [187, 187, 53], "grey": [214, 214, 214], "lightblue": [117, 181, 239],
                    "pink": [184, 70, 162], "red": [184, 50, 50]}

player_missile_colors = {"blue": [117, 181, 239], "red": [240, 128, 128]}


def _init_objects_ram(hud=False):
    """
    (Re)Initialize the objects
    """
    objects = [Player()]
    objects.extend([NoObject()] * 33)
    if hud:
        objects.extend([Lives(), PlayerScore()])
    return objects


def _detect_objects_ram(objects, ram_state, hud=False):
    """
       For all objects:
       (x, y, w, h, r, g, b)
    """

    def update_player():
        player = Player()
        if ram_state[74] != 224:
            x = _x_position(ram_state[73])
            y = 100 + (2 * (ram_state[74] - 41))
            player.xy = (x - 1, y) if ram_state[60] % 16 == 4 else (
                x + 1, y) if ram_state[60] % 16 == 12 else (x, y)
            player.wh = (6, 10) if ram_state[60] % 16 in [4, 12] else (
                5, 10) if 2 > ram_state[60] & 8 > 6 else (6, 10)
            player.orientation = ram_state[60] % 16
            objects[0] = player
            return
        else:
            objects[0] = NoObjectPlayer()

    def update_asteroids():
        ast_list = [3, 4, 5, 6, 7, 8, 9, 12, 13, 14, 15, 16, 17, 18, 19]
        ast_bb = []
        for i, idx in enumerate(ast_list):
            if ram_state[idx + 18] and not ram_state[idx] & 128:
                x = int(_x_position(ram_state[idx + 18]))
                y = 184 - 2 * (80 - ram_state[idx])
                ast = Asteroid()
                ast.xy = (x, y)
                w, h = calculate_dimensions(x, y, ram_state, idx)
                ast.wh = (w, h)
                ast_bb.append(ast.xywh)

        match_objects(objects, ast_bb, 1, 30, Asteroid)

    def calculate_dimensions(x, y, ram_state, idx):
        split = False
        if ram_state[idx + 36] & 127 < 32:
            w, h = 16, 28
        elif ram_state[idx + 36] & 127 < 48:
            w, h = 8, 15
        else:
            w, h = 4, 8

        if x >= 160 - w:
            w -= (x + w) - 160
            split = True
        if y >= 194 - h:
            h -= (y + h) - 194
            split = True
        return w, h

    def update_missiles():
        for i, offset in enumerate([83, 84]):
            if ram_state[offset] and not ram_state[offset + 3] & 128:
                miss = PlayerMissile()
                miss.xy = (_x_position(
                    ram_state[offset]) + 1, 175 - 2 * (80 - ram_state[offset + 3]) + 2)
                objects[31 + i] = miss
            else:
                objects[31 + i] = NoObject()

    def update_hud():
        if hud:
            score = PlayerScore()
            if ram_state[61] >= 16:
                score.xy, score.wh = (4, 5), (76, 10)
            elif ram_state[61]:
                score.xy, score.wh = (20, 5), (60, 10)
            elif ram_state[62] >= 16:
                score.xy, score.wh = (36, 5), (44, 10)
            elif ram_state[62]:
                score.xy, score.wh = (52, 5), (28, 10)
            else:
                score.xy, score.wh = (68, 5), (12, 10)
            objects[-1] = score

    update_player()
    update_asteroids()
    update_missiles()
    update_hud()


def _x_position(value):
    ls = value & 15
    add = 8*((value >> 7) & 1)
    sub = (value >> 4) & 7
    if value == 0:
        return 64
    elif value == 1:
        return 4
    elif ls % 2 == 0:
        mult = (ls/2)-1
        return 97 + 15 * mult + add - sub
    elif ls % 2 == 1:
        mult = ((ls-1)/2)-1
        return 10 + 15 * mult + add - sub


def _augment_info_asteroids_ram(info, ram_state):
    """
    For all objects:
    (x, y, w, h, r, g, b)
    """
    objects = {}
    if ram_state[74] <= 80:
        objects["player"] = 81 - (2 * (ram_state[77])), 100 + \
            (2 * (ram_state[74] - 41)), 10, 10, 240, 128, 128

    for i in range(16):
        if ram_state[3 + i] != 0 and ram_state[21 + 1] != 0:
            if ram_state[21 + i] <= 160:
                prev_y = ram_state[3 + i] % 80
                x, y = ram_state[21 + i], 210 - round(prev_y * 2.5)
                objects[f"asteroi_{i}"] = x, y, 16, 28, 255
    # objects["asteroid"] = 0, round(ram_state[3] * 2.625), 16, 28, 0, 0, 0
    info["score"] = _convert_number(
        ram_state[61]) * 1000 + _convert_number(ram_state[62]) * 10
    info["objects"] = objects


def _detect_objects_asteroids_raw(info, ram_state):
    """
    Actions:
    0: NOP
    1: shoot
    2: move  forward
    3: rotate right
    4: rotate left
    5: random teleport
    y = 0 top
    y = 85 bottom
    """
    info["player_x"] = ram_state[73]    # starts at x = 29
    info["player_y"] = ram_state[74]    # starts at y = 41
    # starts at 255, goes down if go to right and up to the left
    info["diff_to_start_x"] = ram_state[77]
    # 64: looking up, 78: up and right, 76: to the right, 74: down and right
    info["player_direction"] = ram_state[60]
    # 72: down, 70: down and left, 68: left, 66: up and left
    info["score_high"] = _convert_number(ram_state[61])
    info["score_low"] = _convert_number(
        ram_state[62])  # 153 = 990 at 160 again 0
    info["score"] = _convert_number(
        ram_state[61]) * 1000 + _convert_number(ram_state[62]) * 10
    info["player_missile_1_x"] = ram_state[83]  # beginning x = 253, y = 224
    info["player_missile_2_x"] = ram_state[84]  # blue one
    info["player_missile_1_y"] = ram_state[86]
    info["player_missile_2_y"] = ram_state[87]
    info["player_missile_1_dir"] = ram_state[89]    # 0 if not flying
    info["player_missile_2_dir"] = ram_state[90]
    info["asteroid_1"] = {ram_state[21]: ram_state[3]}
    info["asteroid_2"] = {ram_state[22]: ram_state[4]}
    info["asteroid_3"] = {ram_state[23]: ram_state[5]}
    info["asteroid_4"] = {ram_state[24]: ram_state[6]}
    info["asteroid_5"] = {ram_state[25]: ram_state[7]}
    info["asteroid_6"] = {ram_state[26]: ram_state[8]}
    info["asteroid_7"] = {ram_state[27]: ram_state[9]}
    info["asteroid_8"] = {ram_state[28]: ram_state[10]}
    info["asteroid_9"] = {ram_state[29]: ram_state[11]}
    info["asteroid_10"] = {ram_state[30]: ram_state[12]}
    info["asteroid_11"] = {ram_state[31]: ram_state[13]}
    info["asteroid_12"] = {ram_state[32]: ram_state[14]}
    info["asteroid_13"] = {ram_state[33]: ram_state[15]}
    info["asteroid_14"] = {ram_state[34]: ram_state[16]}
    info["asteroid_15"] = {ram_state[35]: ram_state[17]}
    info["asteroid_16"] = {ram_state[36]: ram_state[18]}
    info["asteroid_17"] = {ram_state[37]: ram_state[19]}
    info["asteroid_variation"] = ram_state[39:57]
