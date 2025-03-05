from .game_objects import GameObject
from .utils import find_objects, find_mc_objects, most_common_color, match_objects
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
    # objects.clear()

    player = find_mc_objects(
        obs, [objects_colors["green"], objects_colors["red"]], miny=40)
    match_objects(objects, player, 0, 1, Player)

    # minx=40, miny=
    window = find_objects(obs, [0, 0, 0], minx=40,
                          miny=42, maxx=119, maxy=198, closing_dist=1)
    window_bbs = []
    # match_objects(objects, window, 1, 72, Window)
    for bb in window:
        if bb[2] <= 8 and bb[3] <= 8:
            window_bbs.append(bb)
    
    match_objects(objects,window_bbs, 1, 72, Window)

    red_enemy = find_objects(obs, objects_colors["enemy_red"])
    if red_enemy:
        match_objects(objects, red_enemy, 73, 1, Enemy_Red)

    bird = find_objects(obs, objects_colors["bird"])
    if bird:
        match_objects(objects, bird, 73, 1, Enemy_Bird)

    yellow = find_objects(obs, objects_colors["yellow"])
    yellow_ball_bb = []
    yellow_projectile_bb = []
    for bb in yellow:
        if bb[2] < 8 and bb[3] > 8:
            yellow_projectile_bb.append(bb)
        else:
            yellow_ball_bb.append(bb)

    if yellow_projectile_bb:
        match_objects(objects, yellow_projectile_bb, 75, 1, Yellow_Projectile)
    else:
        match_objects(objects, yellow_projectile_bb, 78, 1, Yellow_Ball)

    purple = find_objects(obs, objects_colors["purple"])
    match_objects(objects, purple, 77, 1, Purple_Projectile)

    blue = find_objects(obs, objects_colors["blue_proj"])
    match_objects(objects, blue, 76, 1, Blue_Projectile)

    heli = find_objects(obs, objects_colors["heli"])
    match_objects(objects, heli, 79, 1, Helicopter)

    if hud:
        score = find_objects(
            obs, objects_colors["green"], maxy=40, closing_dist=4, min_distance=1)
        match_objects(objects, score, 80, 1, Score)
        # for bb in score:
        #     objects.append(Score(*bb))

        lives = find_mc_objects(
            obs, [objects_colors["life_green"], objects_colors["red"]], maxy=40)
        match_objects(objects, lives, 81, 3, Life)
        # for bb in lives:
        #     objects.append(Life(*bb))
