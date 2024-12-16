
import sys
from .game_objects import GameObject, NoObject

"""
RAM extraction for the game TENNIS. Supported modes: ram.
"""


MAX_NB_OBJECTS = {'Player': 1, 'Enemy': 1, 'Ball': 1, 'BallShadow': 1}
MAX_NB_OBJECTS_HUD = {'Player': 1, 'Enemy': 1, 'Ball': 1,
                      'BallShadow': 1, 'PlayerScore': 1, 'EnemyScore': 1}


class Player(GameObject):
    """
    The player figure i.e., the tennis player.
    """

    def __init__(self):
        super().__init__()
        self._xy = 0, 0
        self.wh = 13, 23
        self.rgb = 240, 128, 128
        self.hud = False
        self.visible = True


class Enemy(GameObject):
    """
    The enemy tennis player.
    """

    def __init__(self):
        super().__init__()
        self._xy = 0, 0
        self.wh = 13, 23
        self.rgb = 117, 128, 240
        self.hud = False
        self.visible = True


class Ball(GameObject):
    """
    The tennis ball.
    """

    def __init__(self):
        super().__init__()
        self._xy = 0, 0
        self.wh = 2, 2
        self.rgb = 236, 236, 236
        self.hud = False
        self.visible = True


class BallShadow(GameObject):
    """
    The shadow cast by the ball onto the ground.
    """

    def __init__(self):
        super().__init__()
        self._xy = 0, 0
        self.wh = 2, 2
        self.rgb = 74, 74, 74
        self.hud = False
        self.visible = True


class PlayerScore(GameObject):
    """
    The player's score display (HUD).
    """

    def __init__(self):
        super().__init__()
        self._xy = 49, 5
        self.rgb = 240, 128, 128
        self.wh = 6, 7
        self.hud = True
        self.visible = True

    def __eq__(self, o):
        return isinstance(o, PlayerScore) and self.xy == o.xy


class EnemyScore(GameObject):
    """
    The enemy's score display (HUD).
    """

    def __init__(self):
        super().__init__()
        self._xy = 113, 5
        self.rgb = 117, 128, 240
        self.wh = 6, 7
        self.hud = True
        self.visible = True

    def __eq__(self, o):
        return isinstance(o, PlayerScore) and self.xy == o.xy


def _init_objects_ram(hud=False):
    """
    (Re)Initialize the objects
    """

    objects = [Player(), Enemy(), Ball(), BallShadow()]

    if hud:
        objects.extend([PlayerScore(), EnemyScore()])

    return objects


def _detect_objects_ram(objects, ram_state, hud=False):
    player, enemy, ball, shadow = objects[0:4]

    # player and enemy based off on field orientation
    field_orientation = ram_state[80]
    if field_orientation == 0:  # player up
        player.xy = ram_state[26] - 1, 166 - ram_state[24]
        enemy.xy = ram_state[27] - 1, 166 - ram_state[25]
    elif field_orientation == 1:  # player down
        player.xy = ram_state[27] - 1, 166 - ram_state[25]
        enemy.xy = ram_state[26] - 1, 166 - ram_state[24]

    if ram_state[16] > 2:   # else ball and shadow are out
        ballx, ball_y = ram_state[16] - 2, 189 - ram_state[54]
        shadowx, shadowy = ram_state[16] - 2, 189 - ram_state[55]
        if 98 < ball_y < 113:   # behind the net
            objects[2] = NoObject()
        else:
            if not ball:
                ball = Ball()
                objects[2] = ball
            ball.xy = ballx, ball_y
        if 100 < shadowy < 113 or shadowy == ball_y or shadowy == 0:
            objects[3] = NoObject()
        else:
            if not shadow:
                shadow = BallShadow()
                objects[3] = shadow
            shadow.xy = shadowx, shadowy
    else:
        objects[2] = NoObject()
        objects[3] = NoObject()

    if hud:
        player_score,  enemy_score = objects[4:6]
        enemy_score_val = min(15 * ram_state[70], 40)
        player_score_val = min(15 * ram_state[69], 40)
        add_plr = True
        add_emy = True

        if player_score_val == 0:
            player_score.xy = 49, 5
            player_score.wh = 6, 7
        elif player_score_val == 15:
            player_score.xy = 42, 5
            player_score.wh = 13, 7
        else:  # 30 or 40
            player_score.xy = 41, 5
            player_score.wh = 14, 7

        if enemy_score_val == 0:
            enemy_score.xy = 113, 5
            enemy_score.wh = 6, 7
        elif enemy_score_val == 15:
            enemy_score.xy = 106, 5
            enemy_score.wh = 13, 7
        else:  # 30 or 40
            enemy_score.xy = 105, 5
            enemy_score.wh = 14, 7

        # deuce for player
        if ram_state[7] == 8:
            player_score.xy = 41, 5
            player_score.wh = 22, 7
            add_emy = False

        # deuce for enemy
        if ram_state[6] == 8:
            enemy_score.xy = 105, 5
            enemy_score.wh = 22, 7
            add_plr = False

        # AD out for player
        if ram_state[7] == 10 and ram_state[6] == 12:
            player_score.xy = 41, 5
            player_score.wh = 30, 7
            add_emy = False

        # AD in for player
        if ram_state[7] == 10 and ram_state[6] == 11:
            player_score.xy = 41, 5
            player_score.wh = 22, 7
            add_emy = False

        # AD out for enemy
        if ram_state[6] == 10 and ram_state[7] == 12:
            enemy_score.xy = 105, 5
            enemy_score.wh = 30, 7
            add_plr = False

        # AD in for enemy
        if ram_state[6] == 10 and ram_state[7] == 11:
            enemy_score.xy = 105, 5
            enemy_score.wh = 22, 7
            add_plr = False


def _old_detect_objects_ram(info, ram_state):
    """
    For all 3 objects:
    (x, y, w, h, r, g, b)
    """
    objects = {}
    objects["logo"] = 39, 193, 33, 7, 240, 128, 128
    field_orientation = ram_state[80]  # stores the orientation of the field
    if field_orientation == 0:  # player up
        objects["enemy"] = ram_state[27]-1, 166 - \
            ram_state[25], 16, 22, 117, 128, 240  # DOWN player
        objects["player"] = ram_state[26]-1, 166 - \
            ram_state[24], 16, 22, 240, 128, 128  # UP player
    elif field_orientation == 1:  # player down
        objects["player"] = ram_state[27]-1, 166 - \
            ram_state[25], 16, 22, 240, 128, 128  # UP player
        objects["enemy"] = ram_state[26]-1, 166 - \
            ram_state[24], 16, 22, 117, 128, 240  # DOWN player
    else:
        raise TypeError("Couldn't find the game field_orientation")
    enemy_score = min(15 * ram_state[70], 40)
    player_score = min(15 * ram_state[69], 40)
    # enemy_sets = ram_state[72]
    if enemy_score == 0:
        objects["enemy_scores"] = 113, 5, 6, 7, 117, 128, 240
    elif enemy_score == 15:
        objects["enemy_scores"] = 106, 5, 13, 7, 117, 128, 240
    else:  # 30 or 40
        objects["enemy_scores"] = 105, 5, 14, 7, 117, 128, 240
    if player_score == 0:
        objects["player_score"] = 49, 5, 6, 7, 240, 128, 128
    elif player_score == 15:
        objects["player_score"] = 42, 5, 13, 7, 240, 128, 128
    else:  # 30 or 40
        objects["player_score"] = 41, 5, 14, 7, 240, 128, 128
    bx, by = ram_state[16]-2, 190-ram_state[54]
    if by < 99:
        by -= 1
    if bx < 32 or bx > 127 or by < 99 or by > 112:  # not behind the net
        objects["ball"] = bx, by, 2, 2, 236, 236, 236
    b_shadowx = ram_state[16]-2
    b_shadowy = 190-ram_state[55]
    if b_shadowy < 99:
        b_shadowy -= 1
    if b_shadowx < 32 or b_shadowx > 127 or b_shadowy < 99 or \
            b_shadowy > 112 or (b_shadowx == bx and b_shadowy == by):  # not behind the net
        objects["ball_shadow"] = b_shadowx, b_shadowy, 2, 2, 74, 74, 74
    info["objects"] = objects


def _detect_objects_tennis_raw(info, ram_state):
    """
    returns unprocessed list with
    Upper and lower field person x, y and ball x, y and ball shadow y
    """

    # info["objects_list"] = ram_state[32:36]
    upper_person = [ram_state[26], ram_state[24]]
    lower_person = [ram_state[27], ram_state[25]]
    ball = [ram_state[16], ram_state[54]]
    ball_shadowy = [ram_state[55]]
    relevant_objects = upper_person + lower_person + ball + ball_shadowy
    info["relevant_objects"] = relevant_objects

    # additional info
    # 0: player upper field, 1: player lower field
    info["field_orientation"] = ram_state[80]
    # points: 13 = 0; 14 = 15; 15 = 30; 16 = 40 but also shows won sets
    info["player_score"] = ram_state[7]
    info["enemy_score"] = ram_state[6]
    info["player_points"] = ram_state[69]   # 0 = 0; 1 = 15; 2 = 30; 3 = 40
    info["enemy_points"] = ram_state[70]
    info["player_score_sprite"] = ram_state[45:49]
    info["enemy_score_sprite"] = ram_state[49:53]
