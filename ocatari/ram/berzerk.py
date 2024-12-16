from ._helper_methods import _convert_number
from .game_objects import GameObject, NoObject, ValueObject
import numpy as np
from .utils import match_objects
import sys

"""
RAM extraction for the game BERZERK. Supported modes: ram.
Attention: EvilOtto enemy not implemented due to not getting it spawned during development.
"""

MAX_NB_OBJECTS = {'Player': 1, 'Enemy': 8,
                  'PlayerMissile': 1, 'EnemyMissile': 1}
MAX_NB_OBJECTS_HUD = {'Player': 1, 'Enemy': 8, 'PlayerMissile': 1, 'EnemyMissile': 1,
                      'PlayerScore': 1, 'BonusPoints': 1, 'Lives': 1}


class Player(GameObject):
    """
    The player figure i.e., the earth man stuck on planet Mazeon.
    """

    def __init__(self):
        super().__init__()
        self._xy = 8, 79
        self.wh = 8, 20
        self.rgb = 240, 170, 103
        self.hud = False


class PlayerMissile(GameObject):
    """
    The projectiles shot from the player's laser gun.
    """

    def __init__(self):
        super().__init__()
        self._xy = 0, 0
        self.wh = 1, 6
        self.rgb = 240, 170, 103
        self.hud = False


class Enemy(GameObject):
    """
    The enemy Automazeons stalking the player.
    """

    def __init__(self, x=0, y=0, w=8, h=16):
        super(Enemy, self).__init__()
        self._xy = x, y
        self.wh = w, h
        self.rgb = 210, 210, 64
        self.hud = False


class EnemyMissile(GameObject):
    """
    The projectiles fired at the player by the enemy Automazeons.
    """

    def __init__(self):
        super().__init__()
        self._xy = 0, 0
        self.wh = 1, 6
        self.rgb = 255, 255, 255
        self.hud = False


class PlayerScore(ValueObject):
    """
    The player's score display (HUD).
    """

    def __init__(self):
        super().__init__()
        self._xy = 88, 183
        self.rgb = 232, 232, 74
        self.wh = 14, 7
        self.hud = True

    def __eq__(self, o):
        return isinstance(o, PlayerScore) and self.xy == o.xy


class BonusPoints(ValueObject):
    """
    The player's score display (HUD).
    """

    def __init__(self):
        super().__init__()
        self._xy = 56, 183
        self.rgb = 232, 232, 74
        self.wh = 14, 7
        self.hud = True


class Lives(ValueObject):
    """
    The Atari logo, which is displayed in place of the score if the score is zero (HUD).
    """

    def __init__(self):
        super().__init__()
        self._xy = 63, 183
        self.rgb = 232, 232, 74
        self.wh = 20, 7
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
    objects.extend([NoObject()]*10)
    if hud:
        objects.extend([NoObject()]*3)
    return objects


# enemy color based on current game level
enemy_colors = {0: [210, 210, 64], 1: [210, 210, 64], 2: [198, 108, 58], 3: [198, 108, 58], 4: [214, 214, 214],
                5: [214, 214, 214], 6: [111, 210, 111], 7: [111, 210, 111], 8: [240, 128, 128], 9: [240, 128, 128],
                10: [84, 160, 197], 11: [84, 160, 197], 12: [232, 204, 99], 13: [232, 204, 99], 14: [198, 89, 179],
                15: [198, 89, 179]}


def _detect_objects_ram(objects, ram_state, hud=False):
    """
    For all objects:
    (x, y, w, h, r, g, b)
    """
    if ram_state[80] >= 44:
        objects[0:10] = [NoObject() for _ in range(10)]
    elif not objects[0]:
        objects[0] = Player()
    player = objects[0]

    # player
    if ram_state[19] != 0:
        player.xy = ram_state[19] + 4, ram_state[11] + 5

    # player missile
    if ram_state[15] == 0:
        if objects[9]:
            objects[9] = NoObject()
    else:
        if objects[9]:
            missile = objects[9]
        else:
            missile = PlayerMissile()
            objects[9] = missile
        # based on the missile direction another offset is needed
        if ram_state[21] == 1:  # shooting up
            x = ram_state[22] + 2
            y = ram_state[23] * 2 + 3
        elif ram_state[21] == 2:
            x = ram_state[22] + 2
            y = ram_state[23] * 2 - 1
        elif ram_state[21] == 4 or ram_state[21] == 5:
            x = ram_state[22] + 4
            y = ram_state[23] * 2 + 2
        elif ram_state[21] == 6:
            x = ram_state[22] + 4
            y = ram_state[23] * 2
        elif ram_state[21] == 9:
            x = ram_state[22]
            y = ram_state[23] * 2 + 4
        else:
            x = ram_state[22]
            y = ram_state[23] * 2
        missile.xy = x, y
        if ram_state[21] <= 2:
            missile.wh = 1, 6
        else:
            missile.wh = 4, 2

    # enemies
    enemy_bbs = []
    if np.count_nonzero(ram_state[65:74]) != 0:
        for i in range(8):
            if ram_state[65 + i] != 0 and ram_state[56 + i] != 127:
                enemy = Enemy()
                enemy.xy = ram_state[65 + i] + 6, (ram_state[56 + i] * 2) + 4
                enemy.rgb = enemy_colors.get(ram_state[92] % 16)
                enemy_bbs.append(enemy.xywh)

    match_objects(objects, enemy_bbs, 1, 8, Enemy)

    # enemy missile
    if ram_state[24] == 0:
        if objects[10]:
            objects[10] = NoObject()
    else:
        if objects[10]:
            missile = objects[10]
        else:
            missile = EnemyMissile()
            objects[10] = missile
        x = ram_state[29] + 2
        y = ram_state[30] * 2
        if ram_state[26] == 4 or ram_state[26] == 12 or ram_state[26] == 8:  # shooting up or down
            missile.wh = 1, 6
        else:
            missile.wh = 4, 3
        # initial values for the enemy missile when screen is loading
        missile.xy = x, y
        missile.rgb = enemy_colors.get(ram_state[92] % 16)

    if hud:
        if ram_state[80] >= 44:  # no score, nor bonus but lives
            if objects[11]:
                objects[11] = NoObject()
            if objects[12]:
                objects[12] = NoObject()
            nb_lives = ram_state[90]
            if not objects[13] and nb_lives > 0:
                lives = Lives()
                objects[13] = lives
            else:
                lives = objects[13]
            lives.value = nb_lives
            lives.xy = 104 - 8*nb_lives, 183
            lives.wh = 8*nb_lives-2, 7
        elif np.count_nonzero(ram_state[65:74]) == 0:  # no score, but bonus
            if objects[11]:
                objects[11] = NoObject()
            if objects[13]:
                objects[13] = NoObject()
            if not objects[12]:
                bonus = BonusPoints()
                objects[12] = bonus
                bonus.value = ram_state[91] * 10
        else:
            if objects[13]:
                objects[13] = NoObject()
            score_value = _convert_number(ram_state[93]) * 10000 + _convert_number(ram_state[94]) * 100 + \
                _convert_number(ram_state[95])
            if score_value > 0:
                if not objects[11]:
                    score = PlayerScore()
                    objects[11] = score
                else:
                    score = objects[11]
                if score_value < 100:
                    score.xy = 88, 183
                    score.wh = 14, 7
                elif 1000 > score_value >= 100:
                    score.xy = 80, 183
                    score.wh = 22, 7
                elif 10000 > score_value >= 1000:
                    score.xy = 72, 183
                    score.wh = 30, 7
                elif 100000 > score_value >= 10000:
                    score.xy = 64, 183
                    score.wh = 38, 7
                else:
                    score.xy = 56, 183
                    score.wh = 46, 7


def _detect_objects_berzerk_raw(info, ram_state):
    """
    0: NOP
    1: Shoot
    2: move up
    3: move right
    4: move left
    5: move down
    6: move up, right
    7: move up, left
    8: move down, right
    9: move down, left
    ...
    """
    player = [ram_state[19], ram_state[11]]     # player_x, player_y
    player_missile = [ram_state[22], ram_state[23]]     # missile_x, missile_y
    robot_misile = [ram_state[29],  ram_state[30]]   # missile_x, missile_y
    robot = ram_state[56:74]    # x [65:74] and y [56:65]
    evil_otto = [ram_state[46], ram_state[89]]
    objects = player + player_missile + robot.tolist() + robot_misile + evil_otto
    info["objects"] = objects

    # additional info
    info["number_lives"] = ram_state[90]
    info["robots_killed_count"] = ram_state[91]
    info["game_level"] = ram_state[92]  # starts at 1
    info["player_score"] = _convert_number(ram_state[93]) * 10000 + _convert_number(ram_state[94]) * 100 \
                                                                  + _convert_number(ram_state[95])
    # 1 = up, 2 = down, 4 = left, 5 = up left, 6 = down left
    info["player_direction"] = ram_state[14]
    # 8 = right, 9 = up right, 10 = down right
    # 1 = up, 2 = down, 8 = right
    info["player_missile_direction"] = ram_state[21]
    # 1 = right, 2 = left, 3 = left, 4,12 = down,
    info["robot_missile_direction"] = ram_state[26]
    # 5,7,13 = down and right, 6 = down and left, 8 = up, 9,11 = up and right, 10 = up and left
