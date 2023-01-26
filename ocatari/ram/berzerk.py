from ._helper_methods import _convert_number
from .game_objects import GameObject

"""
RAM extraction for the game BERZERK. Supported modes: raw, revised.
"""


class Player(GameObject):
    def __init__(self):
        self.visible = True
        self._xy = 8, 79
        self.wh = 8, 20
        self.rgb = 240, 170, 103
        self.hud = False


class PlayerMissile(GameObject):
    def __init__(self):
        self.visible = True
        self._xy = 0, 0
        self.wh = 1, 6
        self.rgb = 240, 170, 103
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
        self._xy = 88, 183
        self.rgb = 232, 232, 74
        self.wh = 14, 7
        self.hud = True

    def __eq__(self, o):
        return isinstance(o, PlayerScore) and self.xy == o.xy


class Logo(GameObject):
    def __init__(self):
        self.visible = True
        self._xy = 63, 183
        self.rgb = 232, 232, 74
        self.wh = 20, 7
        self.hud = True


def _init_objects_berzerk_ram(hud=False):
    """
    (Re)Initialize the objects
    """
    objects = []
    if hud:
        pass
    return objects


enemy_colors = {1: [210, 210, 64], 2: [198, 108, 58], 3: [198, 108, 58], 4: [214, 214, 214], "green": [111, 210, 111],
                "rose": [240, 128, 128], "blue": [84, 160, 197], "lightyellow": [232, 204, 99], "pink": [198, 89, 179]}


def _detect_objects_berzerk_revised(objects, ram_state, hud=False):
    """
    For all 3 objects:
    (x, y, w, h, r, g, b)
    """
    del objects[0:]

    # player
    if ram_state[19] != 0:
        player = Player()
        player.xy = ram_state[19] + 4, ram_state[11] + 5
        objects.append(player)

    # player missile
    if ram_state[22] != 0 and ram_state[23] != 0 and ram_state[23] != 3:
        missile = PlayerMissile()
        missile.xy = ram_state[22] + 2, (ram_state[23] * 2) + 3
        y = 0
        if ram_state[21] == 1:  # shooting up
            y = ram_state[23] * 2 + 3
        elif ram_state[21] == 2:
            y = ram_state[23] * 2 - 1
        missile.xy = ram_state[22] + 2, y
        if ram_state[21] <= 2:
            missile.wh = 1, 6
        else:
            missile.wh = 4, 4
        objects.append(missile)

    # enemies
    for i in range(8):
        if ram_state[65 + i] != 0 and ram_state[56 + i] != 127:
            enemy = Enemy()
            enemy.xy = ram_state[65 + i] + 5, (ram_state[56 + i] * 2) + 4
            enemy.rgb = enemy_colors.get(ram_state[92])
            objects.append(enemy)

    # enemy missile
    if ram_state[29] != 0 and ram_state[30] != 0:
        missile = EnemyMissile()
        missile.xy = ram_state[29] + 2, (ram_state[30] * 2) + 3
        y = 0
        if ram_state[26] == 1:  # shooting up
            y = ram_state[30] * 2 + 3
        elif ram_state[26] == 2:
            y = ram_state[30] * 2
        missile.xy = ram_state[29] + 2, y
        if ram_state[26] == 2:
            missile.wh = 4, 3
        else:
            missile.wh = 1, 6
        missile.rgb = enemy_colors.get(ram_state[92])
        objects.append(missile)

    if hud:
        score_value = _convert_number(ram_state[93]) * 10000 + _convert_number(ram_state[94]) * 100 + \
                      _convert_number(ram_state[95])
        print(score_value)
        if score_value == 0:
            logo = Logo()
            logo.xy = 86, 183
            logo.wh = 17, 7
            logo2 = Logo()
            objects.append(logo)
            objects.append(logo2)
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
    print(objects)


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
    """
    info["player_x"] = ram_state[19]  # starts at x = 6
    info["player_y"] = ram_state[11]  # starts at y = 74
    info["player_direction"] = ram_state[14]  # 1 = up, 2 = down, 4 = left, 5 = up left, 6 = down left
    # 8 = right, 9 = up right, 10 = down right
    info["player_missile_x"] = ram_state[22]
    info["player_missile_y"] = ram_state[23]
    info["player_missile_direction"] = ram_state[21]  # 1 = up, 2 = down, 8 = right
    info["robot_missile_direction"] = ram_state[26]  # 2 = left
    info["robot_missile_x"] = ram_state[29]
    info["robot_missile_y"] = ram_state[30]
    info["num_lives"] = ram_state[90]
    info["robots_killed_count"] = ram_state[91]
    info["game_level"] = ram_state[92]  # starts at 1
    # info["enemies_count"] # 124
    info["enemy_evilOtto_x"] = ram_state[46]
    info["enemy_evilOtto_y"] = ram_state[89]
    info["robot"] = ram_state[74:78]
    info["enemy_robots_x"] = ram_state[65:74]
    info["enemy_robots_y"] = ram_state[56:65]
    info["player_score"] = _convert_number(ram_state[93]) * 10000 + _convert_number(ram_state[94]) * 100 \
                           + _convert_number(ram_state[95])
