from ._helper_methods import _convert_number
from .game_objects import GameObject
import numpy as np
import sys

"""
RAM extraction for the game BERZERK. Supported modes: ram.
Attention: EvilOtto enemy not implemented due to not getting it spawned during development.
"""

MAX_NB_OBJECTS =  {'Player': 1, 'Enemy': 8, 'PlayerMissile': 1, 'EnemyMissile': 1}
MAX_NB_OBJECTS_HUD = {'Player': 1, 'Enemy': 8, 'PlayerMissile': 1, 'EnemyMissile': 1, 'PlayerScore': 1, 'Logo': 2, 'RoomCleared': 1}

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
    
    def __init__(self):
        super().__init__()
        self._xy = 0, 0
        self.wh = 8, 16
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


class PlayerScore(GameObject):
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


class Logo(GameObject):
    """
    The Atari logo, which is displayed in place of the score if the score is zero (HUD).
    """
    
    def __init__(self):
        super().__init__()
        self._xy = 63, 183
        self.rgb = 232, 232, 74
        self.wh = 20, 7
        self.hud = True


class RoomCleared(GameObject):
    """
    The display for bonus points scored, if and when all robots in a maze have been cleared (HUD).
    """
    
    def __init__(self):
        super().__init__()
        self._xy = 56, 183
        self.rgb = 232, 232, 74
        self.wh = 14, 7
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
    objects = [Player(), PlayerMissile(), Enemy(), EnemyMissile()]
    if hud:
        objects.extend([PlayerScore(), RoomCleared(), Logo()])
    return objects


# enemy color based on current game level
enemy_colors = {0: [210, 210, 64], 1: [210, 210, 64], 2: [198, 108, 58], 3: [198, 108, 58], 4: [214, 214, 214],
                5: [214, 214, 214], 6: [111, 210, 111], 7: [111, 210, 111], 8: [240, 128, 128], 9: [240, 128, 128],
                10: [84, 160, 197], 11: [84, 160, 197], 12: [232, 204, 99], 13: [232, 204, 99], 14: [198, 89, 179],
                15: [198, 89, 179]}
prev_missile = [0, 0]
two_prev_missile = [0, 0]
prev_enemy_missile = [0, 0]
two_prev_enemy_missiles = [0, 0]


def _detect_objects_ram(objects, ram_state, hud=False):
    """
    For all objects:
    (x, y, w, h, r, g, b)
    """
    del objects[0:]

    # player
    if ram_state[19] != 0:
        player = Player()
        player.xy = ram_state[19] + 4, ram_state[11] + 5
        objects.append(player)

    # player missile
    if ram_state[22] != 0 and ram_state[23] != 0:
        missile = PlayerMissile()
        y = 0
        x = 0
        add_missile = True
        # based on the missile direction another offset is needed
        if ram_state[21] == 1:  # shooting up
            x = ram_state[22] + 2
            y = ram_state[23] * 2 + 3
            if two_prev_missile[1] == y and prev_missile[1] == y:
                add_missile = False
        elif ram_state[21] == 2:
            x = ram_state[22] + 2
            y = ram_state[23] * 2 - 1
            if two_prev_missile[1] == y and prev_missile[1] == y:
                add_missile = False
        elif ram_state[21] == 4 or ram_state[21] == 5:
            x = ram_state[22] + 4
            y = ram_state[23] * 2 + 2
            if two_prev_missile[0] == x and prev_missile[0] == x:
                add_missile = False
        elif ram_state[21] == 6:
            x = ram_state[22] + 4
            y = ram_state[23] * 2
            if two_prev_missile[0] == x and prev_missile[0] == x:
                add_missile = False
        elif ram_state[21] == 9:
            x = ram_state[22]
            y = ram_state[23] * 2 + 4
            if two_prev_missile[0] == x and prev_missile[0] == x:
                add_missile = False
        else:
            x = ram_state[22]
            y = ram_state[23] * 2
            if two_prev_missile[0] == x and prev_missile[0] == x:
                add_missile = False
        missile.xy = x, y
        two_prev_missile[0] = prev_missile[0]
        two_prev_missile[1] = prev_missile[1]
        prev_missile[0] = x
        prev_missile[1] = y
        if ram_state[21] <= 2:
            missile.wh = 1, 6
        else:
            missile.wh = 4, 2

        if add_missile:
            objects.append(missile)

    # enemies
    if ram_state[56] != 127 and ram_state[1] != 255:
        for i in range(8):
            if ram_state[65 + i] != 0 and ram_state[56 + i] != 127:
                enemy = Enemy()
                enemy.xy = ram_state[65 + i] + 6, (ram_state[56 + i] * 2) + 4
                enemy.rgb = enemy_colors.get(ram_state[92] % 16)
                objects.append(enemy)

    # enemy missile
    if ram_state[29] != 0 and ram_state[30] != 0:
        missile = EnemyMissile()
        x = ram_state[29] + 2
        y = ram_state[30] * 2
        add_en_missile = True
        if ram_state[26] == 4 or ram_state[26] == 12 or ram_state[26] == 8:  # shooting up or down
            missile.wh = 1, 6
            if two_prev_enemy_missiles[1] == y:
                add_en_missile = False
        else:
            missile.wh = 4, 3
            if two_prev_enemy_missiles[0] == x:
                add_en_missile = False
        # initial values for the enemy missile when screen is loading
        if x == 2 and y == 0:
            add_en_missile = False
        missile.xy = x, y
        two_prev_enemy_missiles[0] = prev_enemy_missile[0]
        two_prev_enemy_missiles[1] = prev_enemy_missile[1]
        prev_enemy_missile[0] = x
        prev_enemy_missile[1] = y
        missile.rgb = enemy_colors.get(ram_state[92] % 16)
        if add_en_missile:
            objects.append(missile)

    if hud:
        score_value = _convert_number(ram_state[93]) * 10000 + _convert_number(ram_state[94]) * 100 + \
                      _convert_number(ram_state[95])
        # if score is 0 the logo is shown
        if score_value == 0:
            logo = Logo()
            logo.xy = 86, 183
            logo.wh = 17, 7
            logo2 = Logo()
            objects.append(logo)
            objects.append(logo2)
        # or if the room is cleared another value than the score is shown
        elif np.count_nonzero(ram_state[65:74]) == 0:
            room_cleared = RoomCleared()
            objects.append(room_cleared)
        elif score_value < 100:
            score = PlayerScore()
            objects.append(score)
        elif 1000 > score_value >= 100:
            score = PlayerScore()
            score.xy = 80, 183
            score.wh = 22, 7
            objects.append(score)
        elif 10000 > score_value >= 1000:
            score = PlayerScore()
            score.xy = 72, 183
            score.wh = 30, 7
            objects.append(score)
        elif 100000 > score_value >= 10000:
            score = PlayerScore()
            score.xy = 64, 183
            score.wh = 38, 7
            objects.append(score)
        else:
            score = PlayerScore()
            score.xy = 56, 183
            score.wh = 46, 7
            objects.append(score)


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
    info["player_direction"] = ram_state[14]  # 1 = up, 2 = down, 4 = left, 5 = up left, 6 = down left
    # 8 = right, 9 = up right, 10 = down right
    info["player_missile_direction"] = ram_state[21]  # 1 = up, 2 = down, 8 = right
    info["robot_missile_direction"] = ram_state[26]  # 1 = right, 2 = left, 3 = left, 4,12 = down,
    # 5,7,13 = down and right, 6 = down and left, 8 = up, 9,11 = up and right, 10 = up and left
