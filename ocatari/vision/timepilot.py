from .game_objects import GameObject, NoObject
from .utils import find_objects, find_mc_objects, most_common_color, match_objects
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

    mcc = most_common_color(obs, exclude_black=False)
    # (51, 26, 163)
    # (84, 160, 197)
    # (142, 142, 142)
    # (168, 48, 143)
    # (0, 0, 0)

    if mcc == (51, 26, 163):
        player = find_objects(
            obs, objects_colors["player_blue"], miny=32, maxy=177)
        
        p = False
        ps = False

        for bb in player:
            if bb[2] > 2:
                if type(objects[0]) is NoObject:
                    objects[0] = Player(*bb)
                else:
                    objects[0].xywh = bb
                objects[0].rgb = objects_colors["player_blue"]
                p = True
            else:
                if type(objects[1]) is NoObject:
                    objects[1] = Player_Shot(*bb)
                else:
                    objects[1].xywh = bb
                objects[1].rgb = objects_colors["player_blue"]
                ps = True
        
        if not p:
            objects[0] = NoObject()
        
        if not ps:
            objects[1] = NoObject()

        enemy = find_objects(
            obs, objects_colors["enemy_green"], miny=32, maxy=177)
        e = []
        s = []
        for bb in enemy:
            if bb[2] > 2:
                e.append(bb)
            else:
                s.append(bb)

        match_objects(objects, e, 2, 8, Enemy_Green)
        match_objects(objects, s, 10, 2, Enemy_Green_Shot)

    elif mcc == (84, 160, 197):
        player = find_objects(
            obs, objects_colors["player_green"], miny=32, maxy=177)
        
        p = False
        ps = False

        
        for bb in player:
            if bb[2] > 2:
                if type(objects[0]) is NoObject:
                    objects[0] = Player(*bb)
                else:
                    objects[0].xywh = bb
                objects[0].rgb = objects_colors["player_green"]
                p = True
            else:
                if type(objects[1]) is NoObject:
                    objects[1] = Player_Shot(*bb)
                else:
                    objects[1].xywh = bb
                objects[1].rgb = objects_colors["player_green"]
                ps = True
        
        if not p:
            objects[0] = NoObject()
        
        if not ps:
            objects[1] = NoObject()
                
        enemy = find_objects(
            obs, objects_colors["enemy_black"], miny=32, maxy=177)
        e = []
        s = []
        for bb in enemy:
            if bb[3] > 2:
                e.append(bb)
            elif bb[3] > 1:
                s.append(bb)

        match_objects(objects, e, 12, 8, Enemy_Black)
        match_objects(objects, s, 20, 2, Enemy_Black_Shot)

    elif mcc == (142, 142, 142):
        player = find_objects(
            obs, objects_colors["player_red"], miny=32, maxy=177)
        
        p = False
        ps = False

        
        for bb in player:
            if bb[2] > 2:
                if type(objects[0]) is NoObject:
                    objects[0] = Player(*bb)
                else:
                    objects[0].xywh = bb
                objects[0].rgb = objects_colors["player_red"]
                p = True
            else:
                if type(objects[1]) is NoObject:
                    objects[1] = Player_Shot(*bb)
                else:
                    objects[1].xywh = bb
                objects[1].rgb = objects_colors["player_red"]
                ps = True
        
        if not p:
            objects[0] = NoObject()
        
        if not ps:
            objects[1] = NoObject()
                
        enemy = find_objects(
            obs, objects_colors["enemy_yellow"], miny=32, maxy=177)
        e = []
        s = []
        for bb in enemy:
            if bb[2] > 2:
                e.append(bb)
            else:
                s.append(bb)

        match_objects(objects, e, 22, 8, Enemy_Yellow)
        match_objects(objects, s, 30, 2, Enemy_Yellow_Shot)

    elif mcc == (168, 48, 143):
        player = find_objects(
            obs, objects_colors["player_black"], miny=32, maxy=177)
        
        p = False
        ps = False

        
        for bb in player:
            if bb[3] > 2:
                if type(objects[0]) is NoObject:
                    objects[0] = Player(*bb)
                else:
                    objects[0].xywh = bb
                objects[0].rgb = objects_colors["player_black"]
                p = True
            elif bb[3] > 1:
                if type(objects[1]) is NoObject:
                    objects[1] = Player_Shot(*bb)
                else:
                    objects[1].xywh = bb
                objects[1].rgb = objects_colors["player_black"]
                ps = True
        
        if not p:
            objects[0] = NoObject()
        
        if not ps:
            objects[1] = NoObject()

        enemy = find_objects(
            obs, objects_colors["enemy_blue"], miny=32, maxy=177)
        e = []
        s = []
        for bb in enemy:
            if bb[2] > 2:
                e.append(bb)
            else:
                s.append(bb)

        match_objects(objects, e, 32, 8, Enemy_Blue)
        match_objects(objects, s, 40, 2, Enemy_Blue_Shot)

    elif mcc == (0, 0, 0):
        player = find_objects(
            obs, objects_colors["player_blue"], miny=32, maxy=177)
        
        p = False
        ps = False

        
        for bb in player:
            if bb[2] > 2:
                if type(objects[0]) is NoObject:
                    objects[0] = Player(*bb)
                else:
                    objects[0].xywh = bb
                objects[0].rgb = objects_colors["player_blue"]
                p = True
            else:
                if type(objects[1]) is NoObject:
                    objects[1] = Player_Shot(*bb)
                else:
                    objects[1].xywh = bb
                objects[1].rgb = objects_colors["player_blue"]
                ps = True
        
        if not p:
            objects[0] = NoObject()
        
        if not ps:
            objects[1] = NoObject()
                
        enemy = find_objects(
            obs, objects_colors["enemy_orange"], miny=32, maxy=177)
        e = []
        s = []
        for bb in enemy:
            if bb[2] > 2:
                e.append(bb)
            else:
                s.append(bb)

        match_objects(objects, e, 32, 8, Enemy_Orange)
        match_objects(objects, s, 40, 2, Enemy_Orange_Shot)

    if hud:
        score = find_objects(obs, objects_colors["score_yellow"], maxy=33)
        if score:
            if type(objects[-2]) is NoObject:
                objects[-2] = Score(*score[0])
            else:
                objects[-2].xywh = score[0]
        else:
            objects[-2] = NoObject()

        life = find_objects(
            obs, objects_colors["life_blue"], maxy=33)
        if life:
            if type(objects[-1]) is NoObject:
                objects[-1] = Life(*life[0])
            else:
                objects[-1].xywh = life[0]
        else:
            objects[-1] = NoObject()
