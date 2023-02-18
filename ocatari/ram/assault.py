from ._helper_methods import _convert_number
from .game_objects import GameObject
import numpy as np
import math

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
        self.wh = 32, 16
        self.rgb = 72, 160, 72
        self.hud = False


class Enemy(GameObject):
    def __init__(self):
        self.visible = True
        self._xy = 0, 0
        self.wh = 16, 8
        self.rgb = 167, 26, 26
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
        self.rgb = 170, 170, 170
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
    objects = [Player(), PlayerMissile(), Enemy(), EnemyMissile(), MotherShip()]
    if hud:
        objects.extend([PlayerScore(), Health(), Lives()])
    return objects


player_x_pos = [3, 3, 15, 30, 45, 60, 75, 90, 105, 120, 135, 150, 3, 3, 3, 3]
player_x_pos_128 = [11, 11, 23, 38, 53, 68, 83, 98, 113, 128, 143, 158, 11, 11, 11, 11]


def _detect_objects_assault_revised(objects, ram_state, hud=False):
    """
    For all objects:
    (x, y, w, h, r, g, b)
    """
    del objects[0:]

    # player
    player = Player()
    x_mod = ram_state[16]
    x_diff = (x_mod // 16) % 8
    if ram_state[16] < 128:
        x = player_x_pos[ram_state[16] % 16] - x_diff
        if x < 0:
            x = 160 + x
        player.xy = x, 178
    else:
        player.xy = player_x_pos_128[ram_state[16] % 16] - x_diff, 178
    objects.append(player)

    # mother ship
    mother_ship = MotherShip()
    x_mother = ram_state[69]
    x_mother_diff = (x_mother // 16) % 8
    if ram_state[69] < 128:
        x_val = player_x_pos[(ram_state[69] - 1) % 16] - x_mother_diff
        if x_val < 0:
            x_val = 160 + x_val
        mother_ship.xy = x_val, 18
    else:
        mother_ship.xy = player_x_pos_128[(ram_state[69] - 1) % 16] - x_mother_diff, 18

    if ram_state[11] == 112:    # mother ship changes color
        mother_ship.rgb = 184, 70, 162
    objects.append(mother_ship)

    # enemy
    for en in range(3):
        enemy = Enemy()
        x_enemy = ram_state[33 + en]
        x_enemy_diff = (x_enemy // 16) % 8
        if ram_state[33 + en] < 128:
            x_val = player_x_pos[(ram_state[33 + en]) % 16] - x_enemy_diff
            if x_val < 0:
                x_val = 160 + x_val
            enemy.xy = x_val, 103 - 25 * en

        else:
            x_val = player_x_pos_128[(ram_state[33 + en]) % 16] - x_enemy_diff
            if x_val < 0:
                x_val = 160 + x_val
            enemy.xy = x_val, 103 - 25 * en

        if ram_state[54 + en] != 0: # else enemy not visible
            objects.append(enemy)


    if hud:
        # score
        for i in range(6):
            sc = PlayerScore()
            sc.xy = 96 - 8 * i, 2
            objects.append(sc)

        # lives
        for i in range(ram_state[101] - 1):
            l = Lives()
            l.xy = 15 + 16 * i, 192
            objects.append(l)

        # health
        health = Health()
        if ram_state[28] == 192 and ram_state[29] == 0:
            health.wh = 8, 8
        elif ram_state[28] == 224 and ram_state[29] == 0:
            health.wh = 12, 8
        elif ram_state[28] == 240 and ram_state[29] == 0:
            health.wh = 16, 8
        elif ram_state[28] == 248 and ram_state[29] == 0:
            health.wh = 20, 8
        elif ram_state[28] == 252 and ram_state[29] == 0:
            health.wh = 24, 8
        elif ram_state[28] == 254 and ram_state[29] == 0:
            health.wh = 28, 8
        elif ram_state[28] == 255 and ram_state[29] == 0:
            health.wh = 32, 8
        elif ram_state[28] == 255 and ram_state[29] == 1:
            health.wh = 36, 8
        elif ram_state[28] == 255 and ram_state[29] == 3:
            health.wh = 40, 8
        elif ram_state[28] == 255 and ram_state[29] == 7:
            health.wh = 44, 8
        elif ram_state[28] == 255 and ram_state[29] == 15:
            health.wh = 48, 8
        elif ram_state[28] == 255 and ram_state[29] == 31:
            health.wh = 52, 8
        elif ram_state[28] == 255 and ram_state[29] == 63:
            health.wh = 56, 8
        elif ram_state[28] == 255 and ram_state[29] == 127:
            health.wh = 60, 8
        elif ram_state[28] == 255 and ram_state[29] == 255:
            health.wh = 64, 8

        if ram_state[21] == 70:
            health.rgb = 200, 72, 72
        objects.append(health)


def _detect_objects_assault_raw(info, ram_state):
    """
    O: NOP
    1:
    2: shoot
    3: move right
    4: move left
    5: shoot to the right
    6: shoot to the left
    """

    info["score"] = _convert_number(ram_state[0]) * 10000 + _convert_number(ram_state[1]) * 100 + \
                    _convert_number(ram_state[2])
    info["player_x"] = ram_state[16]    # start at x = 134
    info["player_missile_x"] = ram_state[39]    # start at x = 182
    info["player_missile_y"] = ram_state[67]
    info["enemy_x"] = ram_state[33:36]  # 33 most down enemy
    info["enemy_app"] = ram_state[54:57]
    info["enemy_color"] = ram_state[40:42]
    info["mother_ship_color"] = ram_state[12]   # oder 11
    info["mother_ship_x"] = ram_state[69]
    info["healt_color"] = ram_state[21]     # 198 = green, 70 = red
    info["health"] = ram_state[28:30]
    info["player_sprite"] = ram_state[30]
    info["lives"] = ram_state[101]
