from .game_objects import GameObject
from .utils import find_objects, find_mc_objects, most_common_color
import numpy as np

objects_colors = {"green": [111, 210, 111], "red": [240, 128, 128], "blue": [0, 0, 148], "dark_blue": [0, 48, 100],
                  "life_green": [72, 160, 72], "enemy_red": [200, 72, 72], "bird": [214, 214, 214], "yellow": [210, 210, 64],
                  "purple": [181, 108, 224], "blue_proj": [101, 160, 225], "heli": [66, 72, 200]}


class Player(GameObject):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.rgb = [111, 210, 111]


class Window(GameObject):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.rgb = [255, 255, 255]


class Enemy_Red(GameObject):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.rgb = [200, 72, 72]


class Enemy_Bird(GameObject):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.rgb = [214, 214, 214]


class Yellow_Projectile(GameObject):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.rgb = [210, 210, 64]


class Purple_Projectile(GameObject):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.rgb = [181, 108, 224]


class Blue_Projectile(GameObject):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.rgb = [101, 160, 225]


class Yellow_Ball(GameObject):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.rgb = [210, 210, 64]


class Helicopter(GameObject):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.rgb = [66, 72, 200]


#  ---- HUD -----
class Score(GameObject):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.rgb = [111, 210, 111]


class Life(GameObject):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.rgb = [72, 160, 72]


def _detect_objects(objects, obs, hud=False):
    objects.clear()

    player = find_mc_objects(
        obs, [objects_colors["green"], objects_colors["red"]], miny=40)
    for bb in player:
        objects.append(Player(*bb))

    # minx=40, miny=
    window = find_objects(obs, [0, 0, 0], minx=40,
                          miny=42, maxx=119, maxy=198, closing_dist=1)
    for bb in window:
        if bb[2] <= 8 and bb[3] <= 8:
            objects.append(Window(*bb))

    red = find_objects(obs, objects_colors["enemy_red"])
    for bb in red:
        objects.append(Enemy_Red(*bb))

    bird = find_objects(obs, objects_colors["bird"])
    for bb in bird:
        objects.append(Enemy_Bird(*bb))

    yellow = find_objects(obs, objects_colors["yellow"])
    for bb in yellow:
        if bb[2] < 8 and bb[3] > 8:
            objects.append(Yellow_Projectile(*bb))
        else:
            objects.append(Yellow_Ball(*bb))

    purple = find_objects(obs, objects_colors["purple"])
    for bb in purple:
        objects.append(Purple_Projectile(*bb))

    blue = find_objects(obs, objects_colors["blue_proj"])
    for bb in blue:
        objects.append(Blue_Projectile(*bb))

    heli = find_objects(obs, objects_colors["heli"])
    for bb in heli:
        objects.append(Helicopter(*bb))

    if hud:
        score = find_objects(
            obs, objects_colors["green"], maxy=40, closing_dist=4, min_distance=1)
        for bb in score:
            objects.append(Score(*bb))

        lives = find_mc_objects(
            obs, [objects_colors["life_green"], objects_colors["red"]], maxy=40)
        for bb in lives:
            objects.append(Life(*bb))
