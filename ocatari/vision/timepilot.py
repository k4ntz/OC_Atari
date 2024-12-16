from .game_objects import GameObject
from .utils import find_objects, find_mc_objects, most_common_color
import numpy as np

objects_colors = {"player_blue": [84, 92, 214], "player_green": [50, 132, 50], "player_red": [167, 26, 26], "player_black": [0, 0, 0],
                  "enemy_green": [135, 183, 84], "enemy_black": [0, 0, 0], "enemy_yellow": [187, 187, 53], "enemy_blue": [84, 138, 210], "enemy_orange": [180, 122, 48],
                  "score_yellow": [210, 164, 74], "life_blue": [101, 111, 228]}


class Player(GameObject):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.rgb = [84, 92, 214]


class Player_Shot(GameObject):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.rgb = [84, 92, 214]


class Enemy_Green(GameObject):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.rgb = [135, 183, 84]


class Enemy_Green_Shot(GameObject):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.rgb = [135, 183, 84]


class Enemy_Black(GameObject):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.rgb = [0, 0, 0]


class Enemy_Black_Shot(GameObject):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.rgb = [0, 0, 0]


class Enemy_Yellow(GameObject):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.rgb = [187, 187, 53]


class Enemy_Yellow_Shot(GameObject):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.rgb = [187, 187, 53]


class Enemy_Blue(GameObject):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.rgb = [187, 187, 53]


class Enemy_Blue_Shot(GameObject):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.rgb = [187, 187, 53]


class Enemy_Orange(GameObject):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.rgb = [187, 187, 53]


class Enemy_Orange_Shot(GameObject):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.rgb = [187, 187, 53]


#  ---- HUD -----
class Score(GameObject):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.rgb = [210, 164, 74]


class Life(GameObject):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.rgb = [101, 111, 228]


def _detect_objects(objects, obs, hud=False):
    objects.clear()

    mcc = most_common_color(obs, exclude_black=False)
    # (51, 26, 163)
    # (84, 160, 197)
    # (142, 142, 142)
    # (168, 48, 143)
    # (0, 0, 0)

    if mcc == (51, 26, 163):
        player = find_objects(
            obs, objects_colors["player_blue"], miny=32, maxy=177)
        for bb in player:
            if bb[2] > 2:
                p = Player(*bb)
                p.rgb = objects_colors["player_blue"]
                objects.append(p)
            else:
                s = Player_Shot(*bb)
                s.rgb = objects_colors["player_blue"]
                objects.append(s)
        enemy = find_objects(
            obs, objects_colors["enemy_green"], miny=32, maxy=177)
        for bb in enemy:
            if bb[2] > 2:
                objects.append(Enemy_Green(*bb))
            else:
                objects.append(Enemy_Green_Shot(*bb))

    elif mcc == (84, 160, 197):
        player = find_objects(
            obs, objects_colors["player_green"], miny=32, maxy=177)
        for bb in player:
            if bb[2] > 2:
                p = Player(*bb)
                p.rgb = objects_colors["player_green"]
                objects.append(p)
            else:
                s = Player_Shot(*bb)
                s.rgb = objects_colors["player_green"]
                objects.append(s)
        enemy = find_objects(
            obs, objects_colors["enemy_black"], miny=32, maxy=177)
        for bb in enemy:
            if bb[3] > 2:
                objects.append(Enemy_Black(*bb))
            elif bb[3] > 1:
                objects.append(Enemy_Black_Shot(*bb))

    elif mcc == (142, 142, 142):
        player = find_objects(
            obs, objects_colors["player_red"], miny=32, maxy=177)
        for bb in player:
            if bb[2] > 2:
                p = Player(*bb)
                p.rgb = objects_colors["player_red"]
                objects.append(p)
            else:
                s = Player_Shot(*bb)
                s.rgb = objects_colors["player_red"]
                objects.append(s)
        enemy = find_objects(
            obs, objects_colors["enemy_yellow"], miny=32, maxy=177)
        for bb in enemy:
            if bb[2] > 2:
                objects.append(Enemy_Yellow(*bb))
            else:
                objects.append(Enemy_Yellow_Shot(*bb))

    elif mcc == (168, 48, 143):
        player = find_objects(
            obs, objects_colors["player_black"], miny=32, maxy=177)
        for bb in player:
            if bb[3] > 2:
                p = Player(*bb)
                p.rgb = objects_colors["player_black"]
                objects.append(p)
            elif bb[3] > 1:
                s = Player_Shot(*bb)
                s.rgb = objects_colors["player_black"]
                objects.append(s)
        enemy = find_objects(
            obs, objects_colors["enemy_blue"], miny=32, maxy=177)
        for bb in enemy:
            if bb[2] > 2:
                objects.append(Enemy_Blue(*bb))
            else:
                objects.append(Enemy_Blue_Shot(*bb))

    elif mcc == (0, 0, 0):
        player = find_objects(
            obs, objects_colors["player_blue"], miny=32, maxy=177)
        for bb in player:
            if bb[2] > 2:
                p = Player(*bb)
                p.rgb = objects_colors["player_blue"]
                objects.append(p)
            else:
                s = Player_Shot(*bb)
                s.rgb = objects_colors["player_blue"]
                objects.append(s)
        enemy = find_objects(
            obs, objects_colors["enemy_orange"], miny=32, maxy=177)
        for bb in enemy:
            if bb[2] > 2:
                objects.append(Enemy_Orange(*bb))
            else:
                objects.append(Enemy_Orange_Shot(*bb))

    if hud:
        score = find_objects(obs, objects_colors["score_yellow"], maxy=33)
        for bb in score:
            objects.append(Score(*bb))

        life = find_objects(
            obs, objects_colors["life_blue"], maxy=33, closing_active=False)
        for bb in life:
            w = bb[2]
            for i in range(4):
                if w >= 8:
                    objects.append(Life(bb[0]+i*8, bb[1], 8, bb[3]))
                    w -= 8
