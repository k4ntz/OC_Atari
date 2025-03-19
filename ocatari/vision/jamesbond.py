from .game_objects import GameObject, NoObject
from .utils import find_objects, find_mc_objects, most_common_color
import numpy as np

objects_colors = {"orange": [227, 151, 89], "red": [167, 26, 26], "white": [236, 236, 236], "yellow_heli": [134, 134, 29],
                  "grey": [170, 170, 170], "blue": [45, 87, 176], "orange_horn": [181, 83, 40], "yellow_shot": [252, 224, 112],
                  "light_blue": [84, 138, 210], "brown": [72, 44, 0], "green": [26, 102, 26], "yellow_score": [187, 187, 53],
                  "orange_life": [180, 122, 48], "grey_life": [192, 192, 192]}


class Player(GameObject):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.rgb = [227, 151, 89]


class Player_Shot(GameObject):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.rgb = [227, 151, 89]


class Helicopter(GameObject):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.rgb = [167, 26, 26]


class Hornet(GameObject):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.rgb = [170, 170, 170]


class Enemy_Shot(GameObject):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.rgb = [252, 224, 112]


class Ice(GameObject):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.rgb = [84, 138, 210]


class Fire_Hole(GameObject):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.rgb = [72, 44, 0]


class Eruption(GameObject):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.rgb = [26, 102, 26]


class Diver(GameObject):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.rgb = [26, 102, 26]


#  ---- HUD -----
class Score(GameObject):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.rgb = [252, 252, 84]


class Life(GameObject):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.rgb = [180, 122, 48]


def _detect_objects(objects, obs, hud=False):

    player = find_objects(obs, objects_colors["orange"])
    shot = False
    for bb in player:
        if bb[2] == 1 and bb[3] == 4:
            if type(objects[1]) is NoObject:
                objects[1] = Player_Shot(*bb)
            objects[1].xywh = bb
            shot = True
        else:
            objects[0].xywh = bb

    if not shot:
        objects[1] = NoObject()

    heli = find_mc_objects(obs, [objects_colors["red"], objects_colors["white"],
                           objects_colors["yellow_heli"]], miny=50, maxy=125)
    if heli:
        if type(objects[2]) is NoObject:
            objects[2] = Helicopter(*heli[0])
        objects[2].xywh = heli[0]
    else:
        objects[2] = NoObject()

    horn = find_mc_objects(obs, [objects_colors["grey"], objects_colors["blue"],
                           objects_colors["orange_horn"]], miny=50, maxy=125, size=(8, 14), tol_s=1)
    if horn:
        if type(objects[4]) is NoObject:
            objects[4] = Hornet(*horn[0])
        objects[4].xywh = horn[0]
    else:
        objects[4] = NoObject()

    shot = find_objects(
        obs, objects_colors["yellow_shot"], miny=50, maxy=125, closing_dist=8)
    for bb in shot:
        if bb[2] == 1 and 1 < bb[3] < 5:
            if type(objects[5]) is NoObject:
                objects[5] = Enemy_Shot(*bb)
            objects[5].xywh = bb
    else:
        objects[5] = NoObject()


    ice = find_mc_objects(obs, [objects_colors["grey"], objects_colors["light_blue"],
                          objects_colors["blue"]], miny=50, maxy=125, size=(7, 12), tol_s=2)
    if ice:
        if type(objects[3]) is NoObject:
            objects[3] = Ice(*ice[0])
        objects[3].xywh = ice[0]
    else:
        objects[3] = NoObject()

    hole = find_objects(obs, objects_colors["brown"])
    if hole:
        if type(objects[8]) is NoObject:
            objects[8] = Fire_Hole(*hole[0])
        objects[8].xywh = hole[0]
    else:
        objects[8] = NoObject()

    erup = find_mc_objects(obs, [objects_colors["green"], objects_colors["yellow_score"]],
                           miny=100, maxy=157, closing_dist=10, all_colors=False)
    for bb in erup:
        if bb[2] > 10:
            if type(objects[6]) is NoObject:
                objects[6] = Eruption(*bb)
            objects[6].xywh = bb
            objects[7] = NoObject()
            break
        elif bb[3] > 16:
            objects[6] = NoObject()
            if type(objects[7]) is NoObject:
                objects[7] = Diver(*bb)
            objects[7].xywh = bb
            break
    else:
        objects[6] = NoObject()
        objects[7] = NoObject()

    if hud:
        score = find_objects(
            obs, objects_colors["yellow_score"], maxy=30, closing_dist=5)
        if score:
            objects[9].xywh = score[0]

        lives = find_mc_objects(
            obs, [objects_colors["grey_life"], objects_colors["orange_life"], objects_colors["yellow_heli"]], miny=180, closing_dist=16)
        
        if lives:
            objects[10].xywh = lives[0]
