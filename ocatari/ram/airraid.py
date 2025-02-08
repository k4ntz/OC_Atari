import sys
from .game_objects import GameObject, NoObject
import numpy as np

"""
RAM extraction for the game AirRaid.

"""

MAX_NB_OBJECTS = {'Player': 1, 'Building': 3, 'Enemy25': 3, 'Enemy50': 3,
                  'Enemy75': 3, 'Enemy100': 3, 'Missile': 2}
MAX_NB_OBJECTS_HUD = {'Player': 1, 'Building': 3, 'Enemy25': 3, 'Enemy50': 3,
                      'Enemy75': 3, 'Enemy100': 3, 'Missile': 2, 'PlayerScore': 1, 'Lives': 1}


class Player(GameObject):
    """
    The player spaceship.
    """

    def __init__(self):
        super().__init__()
        self.xy = 0, 157
        self.wh = 14, 12
        self.rgb = 169, 169, 169
        self.hud = False


class Building(GameObject):
    """
    The buildings
    """

    def __init__(self):
        super().__init__()
        self.xy = 0, 178
        self.wh = 32, 32
        self.rgb = 114, 114, 114
        self.hud = False
        self.damage = 0


class Enemy25(GameObject):
    """
    The enemy spaceship with 25 scores.
    """

    def __init__(self):
        super().__init__()
        self.xy = 44, 69
        self.wh = 16, 18
        self.rgb = 135, 135, 135
        self.hud = False


class Enemy50(GameObject):
    """
    The enemy spaceship with 50 scores.
    """

    def __init__(self):
        super().__init__()
        self.xy = 44, 69
        self.wh = 14, 16
        self.rgb = 129, 129, 129
        self.hud = False


class Enemy75(GameObject):
    """
    The enemy spaceship with 75 scores.
    """

    def __init__(self):
        super().__init__()
        self.xy = 44, 69
        self.wh = 14, 16
        self.rgb = 86, 86, 186
        self.hud = False


class Enemy100(GameObject):
    """
    The enemy spaceship with 100 scores.
    """

    def __init__(self):
        super().__init__()
        self.xy = 44, 69
        self.wh = 14, 14
        self.rgb = 137, 137, 137
        self.hud = False

# It would be better to separate player missiles and enemy missiles.


class Missile(GameObject):
    """
    Missiles lunched by both enemies and the player.
    """

    def __init__(self):
        super().__init__()
        self.xy = 0, 157
        self.wh = 2, 2
        self.rgb = 236, 236, 236
        self.hud = False

# class PlayerMissile(GameObject):
#     """
#     Missiles lunched by the player.
#     """

#     def __init__(self):
#         super().__init__()
#         self.xy = 96, 3
#         self.wh = 2, 2
#         self.rgb = 236, 236, 236
#         self.hud = False

# class EnemyMissile(GameObject):
#     """
#     Missiles lunched by enemies.
#     """

#     def __init__(self):
#         super().__init__()
#         self.xy = 96, 3
#         self.wh = 2, 2
#         self.rgb = 236, 236, 236
#         self.hud = False


class PlayerScore(GameObject):
    """
    The player's score display (HUD).
    """

    def __init__(self):
        super().__init__()
        self.xy = 56, 3
        self.wh = 6, 9
        self.rgb = 131, 131, 131
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
        self.rgb = 151, 151, 151
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

    objects = [Player()] + [Building()] * 3 + [Enemy25()] * 3 + [Enemy50()] * 3 + \
        [Enemy75()] * 3 + [Enemy100()] * 3 + [Missile()] * 2
    if hud:
        objects += [PlayerScore()] + [Lives()]
    return objects


def _detect_objects_ram(objects, ram_state, hud=False):
    """
    For all objects:
    (x, y, w, h, r, g, b)
    """

    grayscaled = ram_state[84] != 248

    # player
    player = Player()
    player.xy = ram_state[19] - 3, 157 - grayscaled * 1
    player.wh = 14, 12
    if not grayscaled:
        player.rgb = [121, 181, 236]
    else:
        player.rgb = [169, 169, 169]
    objects[0] = player

    # buildings
    h_by_damage = [32, 29, 29, 29, 27, 23, 21, 19, 15, 19, 23, 25, 25, 8, 32]
    y_by_damage = [178, 181, 181, 181, 183, 187,
                   189, 191, 195, 191, 187, 185, 185, 202, 178]
    building_color_by_mode = [[150, 113, 26], [114, 114, 114]]

    b1 = Building()
    b1.damage = ram_state[27]
    b1.xy = ram_state[20] - 3 if ram_state[20] > 3 else ram_state[20] + \
        156, y_by_damage[b1.damage]
    b1.wh = min(32, 160 - b1.xy[0]), h_by_damage[b1.damage]
    b1.rgb = building_color_by_mode[grayscaled]
    b2 = Building()
    b2.damage = ram_state[28]
    b2.xy = ram_state[21] - 3 if ram_state[21] > 3 else ram_state[21] + \
        156, y_by_damage[b2.damage]
    b2.wh = min(32, 160 - b2.xy[0]), h_by_damage[b2.damage]
    b2.rgb = building_color_by_mode[grayscaled]

    hb = NoObject()
    if b1.xy[0] > 128:
        hb = Building()
        hb.xy = 0, b1.xy[1]
        hb.wh = 32 - b1.wh[0], b1.wh[1]
        hb.rgb = b1.rgb
        hb.damage = b1.damage
    elif b2.xy[0] > 128:
        hb = Building()
        hb.xy = 0, b2.xy[1]
        hb.wh = 32 - b2.wh[0], b2.wh[1]
        hb.rgb = b2.rgb
        hb.damage = b2.damage

    objects[1] = b1
    objects[2] = b2
    objects[3] = hb

    # Enemy
    enemy_offsets = {25: [2, 0, 0],
                     50: [0, -1, 0],
                     75: [2, 1, 2],
                     100: [0, 1, 0]}
    for i in range(4, 16):
        objects[i] = NoObject()
    for i in range(3):
        enemy = NoObject()
        if ram_state[29 + i] != 44 and ram_state[78 + i] != 236:
            if ram_state[63 + i] in [0, 1]:
                enemy = Enemy25()
                enemy.xy = enemy_offsets[25][i] + \
                    ram_state[66 + i] - 3, 195 - ram_state[29 + i]
                enemy.wh = 16, min(18, 151 - enemy.xy[1])  # 18
                enemy.rgb = 147, 111, 223
                objects[4 + i] = enemy
            elif ram_state[63 + i] in [2, 3]:
                enemy = Enemy50()
                enemy.xy = enemy_offsets[50][i] + ram_state[66 +
                                                            i] - 3 + int(i == 1), 195 - ram_state[29 + i]
                enemy.wh = 14, min(16, 151 - enemy.xy[1])  # 16
                enemy.rgb = 183, 92, 176
                objects[7 + i] = enemy
            elif ram_state[63 + i] in [4, 5]:
                enemy = Enemy75()
                enemy.xy = enemy_offsets[75][i] + ram_state[66 +
                                                            i] - 3 + int(i == 1), 195 - ram_state[29 + i]
                enemy.wh = 14, min(16, 151 - enemy.xy[1])  # 16
                enemy.rgb = 72, 72, 194
                objects[10 + i] = enemy
            elif ram_state[63 + i] in [6, 7]:
                enemy = Enemy100()
                enemy.xy = enemy_offsets[100][i] + ram_state[66 +
                                                             i] - 3 + int(i == 1), 195 - ram_state[29 + i]
                enemy.wh = 14, min(14, 151 - enemy.xy[1])  # 14
                enemy.rgb = 72, 176, 110
                objects[13 + i] = enemy

    # player missile:
    player_missile = NoObject()
    if ram_state[85] != 35 and ram_state[85] != 34:
        player_missile = Missile()
        player_missile.xy = ram_state[86] - 5, 194 - ram_state[85]
    objects[16] = player_missile

    # enemy missile
    enemy_missile = NoObject()
    if ram_state[83] != 0 and ram_state[83] != 248:
        enemy_missile = Missile()
        enemy_missile.xy = ram_state[84] - 5, 193 - ram_state[83]
    objects[17] = enemy_missile

    # player score
    ps_color_by_mode = [[87, 139, 201], [131, 131, 131]]
    # player_score = NoObject()
    if hud:
        player_score = PlayerScore()
        a = ram_state[40] % 16 + 10 * (ram_state[40] // 16)
        b = ram_state[41] % 16 + 10 * (ram_state[41] // 16)
        c = ram_state[42] % 16 + 10 * (ram_state[42] // 16)
        player_score.score = a * 10000 + b * 100 + c

        if player_score.score < 10:
            player_score.xy = 96, 11
            player_score.wh = 6, 9
        elif player_score.score < 100:
            player_score.xy = 88, 11
            player_score.wh = 14, 9
        elif player_score.score < 1000:
            if player_score.score < 200:
                player_score.xy = 81, 11
                player_score.wh = 21, 9
            else:
                player_score.xy = 80, 11
                player_score.wh = 22, 9
        elif player_score.score < 10000:
            if player_score.score < 2000:
                player_score.xy = 73, 11
                player_score.wh = 29, 9
            else:
                player_score.xy = 72, 11
                player_score.wh = 30, 9
        elif player_score.score < 100000:
            if player_score.score < 20000:
                player_score.xy = 65, 11
                player_score.wh = 37, 9
            else:
                player_score.xy = 64, 11
                player_score.wh = 38, 9
        else:
            if player_score.score < 200000:
                player_score.xy = 57, 11
                player_score.wh = 45, 9
            else:
                player_score.xy = 56, 11
                player_score.wh = 46, 9
        player_score.rgb = ps_color_by_mode[grayscaled]
        objects[18] = player_score

    # lives
    # lives = NoObject()
    if hud and ram_state[39] in [1, 2]:
        lives = Lives()
        lives.lives = ram_state[39]
        lives.xy = 55, 220 - int(grayscaled)
        w = 0
        if lives.lives == 1:
            lives.wh = 7, 5 + int(grayscaled)
        elif lives.lives == 2:
            lives.wh = 15, 5 + int(grayscaled)
        objects[19] = lives
