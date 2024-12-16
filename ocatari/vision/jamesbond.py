from .game_objects import GameObject
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
    objects.clear()

    player = find_objects(obs, objects_colors["orange"])
    for bb in player:
        if bb[2] == 1 and bb[3] == 4:
            objects.append(Player_Shot(*bb))
        else:
            objects.append(Player(*bb))

    heli = find_mc_objects(obs, [objects_colors["red"], objects_colors["white"],
                           objects_colors["yellow_heli"]], miny=50, maxy=125)
    for bb in heli:
        objects.append(Helicopter(*bb))

    horn = find_mc_objects(obs, [objects_colors["grey"], objects_colors["blue"],
                           objects_colors["orange_horn"]], miny=50, maxy=125, size=(8, 14), tol_s=1)
    for bb in horn:
        objects.append(Hornet(*bb))

    shot = find_objects(
        obs, objects_colors["yellow_shot"], miny=50, maxy=125, closing_dist=8)
    for bb in shot:
        if bb[2] == 1 and 1 < bb[3] < 5:
            objects.append(Enemy_Shot(*bb))

    ice = find_mc_objects(obs, [objects_colors["grey"], objects_colors["light_blue"],
                          objects_colors["blue"]], miny=50, maxy=125, size=(7, 12), tol_s=2)
    for bb in ice:
        objects.append(Ice(*bb))

    hole = find_objects(obs, objects_colors["brown"])
    for bb in hole:
        objects.append(Fire_Hole(*bb))

    erup = find_mc_objects(obs, [objects_colors["green"], objects_colors["yellow_score"]],
                           miny=100, maxy=157, closing_dist=10, all_colors=False)
    for bb in erup:
        if bb[2] > 10:
            objects.append(Eruption(*bb))
        elif bb[3] > 16:
            objects.append(Diver(*bb))

    if hud:
        score = find_objects(
            obs, objects_colors["yellow_score"], maxy=30, closing_dist=5)
        for bb in score:
            objects.append(Score(*bb))

        lives = find_mc_objects(
            obs, [objects_colors["grey_life"], objects_colors["orange_life"], objects_colors["yellow_heli"]], miny=180)
        for bb in lives:
            objects.append(Life(*bb))
