from .game_objects import GameObject, NoObject
from ._helper_methods import _convert_number
import sys
import numpy as np

"""
RAM extraction for the game GALAXIAN. Supported modes: ram.
"""

# TODO: Diving Enemies, Enemy Missiles, Enemy x pos, width of Score and Round

MAX_NB_OBJECTS = {'Player': 1, 'PlayerMissile': 1,
                  'EnemyMissile': 2, 'EnemyShip': 42}
MAX_NB_OBJECTS_HUD = {'Player': 1, 'PlayerMissile': 1,
                      'EnemyMissile': 2, 'EnemyShip': 42, 'Score': 1, 'Round': 1, 'Lives': 1}


class Player(GameObject):
    """
    The player figure i.e, the gun.
    """

    def __init__(self):
        super().__init__()
        self._xy = 66, 186
        self.wh = 8, 13
        self.rgb = 236, 236, 236
        self.hud = False


class PlayerMissile(GameObject):
    """
    The projectiles fired by the player.
    """

    def __init__(self):
        super().__init__()
        self._xy = 66, 186
        self.wh = 1, 3
        self.rgb = 210, 164, 74
        self.hud = False


class EnemyMissile(GameObject):
    """
    The projectiles fired by the Enemy.
    """

    def __init__(self):
        super().__init__()
        self._xy = 66, 186
        self.wh = 1, 4
        self.rgb = 228, 111, 111
        self.hud = False


class EnemyShip(GameObject):
    """
    The Enemy Ships.
    """

    def __init__(self):
        super().__init__()
        self._xy = 66, 186
        self.wh = 6, 9
        self.rgb = 232, 204, 99
        self.hud = False


class DivingEnemy(GameObject):
    """
    The Diving Enemies.
    """

    def __init__(self):
        super().__init__()
        self._xy = 0, 0
        self.wh = 6, 9
        self.rgb = 255, 0, 0  # Example RGB for diving enemy
        self.hud = False


class Score(GameObject):
    """
    The player's remaining lives (HUD).
    """

    def __init__(self):
        super().__init__()
        self.rgb = 232, 204, 99
        self._xy = 63, 4
        self.wh = 39, 7
        self.hud = True


class Round(GameObject):
    """
    The round counter display (HUD).
    """

    def __init__(self):
        super().__init__()
        self.rgb = 214, 214, 214
        self._xy = 137, 188
        self.wh = 7, 7
        self.hud = True


class Lives(GameObject):
    """
    The remaining lives of the player (HUD).
    """

    def __init__(self):
        super().__init__()
        self.rgb = 214, 214, 214
        self._xy = 19, 188
        self.wh = 13, 7
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
    objects = [Player()]
    objects.extend([NoObject()]*45)

    if hud:
        objects.extend([Lives(), Score(), Round()])

    return objects


def _detect_objects_ram(objects, ram_state, hud=False):
    """
       For all objects:
       (x, y, w, h, r, g, b)
    """

    player = objects[0]
    if ram_state[11] != 255:  # else player not on screen
        if isinstance(player, NoObject):
            player = Player()
        player.xy = ram_state[100]+8, 170
        objects[0] = player
    else:
        objects[0] = NoObject()

    player_missile = objects[1]
    if ram_state[11] != 255 and ram_state[11] != 151:  # else there is no missile
        if isinstance(player_missile, NoObject):
            player_missile = PlayerMissile()
            objects[1] = player_missile
        player_missile.x, player_missile.y = ram_state[60] + \
            2, ram_state[11] + 16
    elif not isinstance(player_missile, NoObject):
        objects[1] = NoObject()

    # The 7 rightmost bits of the ram positions 38 to 44 represent a bitmap of the enemies.
    # Each bit is 1 if there is an enemy in its position and 0 if there is not.
    # the y-coordinates of the rows of enemies
    row_y = {0: 19, 1: 32, 2: 43, 3: 56, 4: 67, 5: 79}
    k = 0

    for i in range(6):
        # gets a string of the 7 relevant bits
        row = format(ram_state[38 + i] & 0x7F, '07b')
        row = [int(x) for x in row]
        for j in range(7):
            if row[j] == 1:
                enemy_ship = EnemyShip()
                enemy_ship.y = row_y[i]
                enemy_ship.x = 72 + 2 * ram_state[36] + j * 17
                if i == 1 or i == 3:
                    enemy_ship.h = 8
                objects[4+k] = enemy_ship
                k += 1
            else:
                objects[4+k] = NoObject()
                k += 1

    if hud:
        lives = objects[2]
        if ram_state[57] != 0:
            lives.w = ram_state[57] * 3 + (ram_state[57] - 1) * 2
            objects[2] = lives
        elif not isinstance(lives, NoObject):
            objects[2] = NoObject()


def _detect_objects_galaxian_raw(info, ram_state):

    info["score"] = _convert_number(ram_state[45]) * 10000 + _convert_number(
        ram_state[45]) * 100 + _convert_number(ram_state[46])
    info["lives"] = ram_state[57]
    info["round"] = ram_state[47]
