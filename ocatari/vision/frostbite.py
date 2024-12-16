from .utils import find_objects, find_mc_objects, find_objects_in_color_range, match_objects
from .game_objects import GameObject, NoObject
import numpy as np
import matplotlib as plt


objects_colors = {
    "WhitePlate": [214, 214, 214], "BluePlate": [84, 138, 210],
    "Bird": [132, 144, 252],
    "hud_objs": [132, 144, 252], "house": [142, 142, 142], "greenfish": [111, 210, 111],
    "crab": [213, 130, 74], "clam": [210, 210, 64], "bear": [111, 111, 111]
}

playercolors = [[162, 98, 33], [198, 108, 58], [142, 142, 142], [162, 162, 42]]
logocolors = [[214, 214, 214], [184, 50, 50], [180, 122, 48],
              [210, 210, 64], [110, 156, 66], [45, 50, 184]]
c_house_colors = [[142, 142, 142], [0, 0, 0]]
frostbite = [[84, 138, 210], [66, 114, 194], [45, 87, 176], [24, 59, 157]]

plate_per_col = [6, 6, 6, 6]
floors = [[95, 105], [120, 130], [145, 155], [170, 180]]


class Player(GameObject):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.rgb = 198, 108, 58
        self.hud = False


class GreenFish(GameObject):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.rgb = 111, 210, 111
        self.hud = False


class FrostBite(GameObject):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.rgb = 84, 38, 210
        self.hud = False


class WhitePlate(GameObject):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.rgb = 214, 214, 214
        self.hud = False


class BluePlate(GameObject):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.rgb = 84, 138, 210
        self.hud = False


class Bird(GameObject):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.rgb = 132, 144, 252
        self.hud = False


class Bear(GameObject):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.rgb = 0, 0, 0
        self.hud = False


class Crab(GameObject):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.rgb = 213, 130, 74
        self.hud = False


class Clam(GameObject):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.rgb = 210, 210, 64
        self.hud = False


class House(GameObject):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.rgb = 142, 142, 142
        self.hud = False


class CompletedHouse(GameObject):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.rgb = 0, 0, 0
        self.hud = False


class LifeCount(GameObject):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.rgb = 132, 144, 252
        self.hud = True


class PlayerScore(GameObject):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.rgb = 132, 144, 252
        self.hud = True


class Degree(GameObject):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.rgb = 132, 144, 252
        self.hud = True


def _detect_objects(objects, obs, hud=False):
    # detection and filtering

    player = objects[0]
    player_bb = find_mc_objects(obs, playercolors, size=(
        8, 17), tol_s=2, closing_active=False)
    if player_bb:
        player.xywh = player_bb[0]
    start_idx = 1

    bird_bb = find_objects(
        obs, objects_colors["Bird"], closing_dist=5, size=(8, 7), tol_s=2, miny=30)
    match_objects(objects, bird_bb, start_idx, 8, Bird)
    start_idx += 8

    bear_bb = find_objects(
        obs, objects_colors["bear"], miny=13, maxy=75, size=(14, 15), tol_s=5)
    if bear_bb:
        objects[start_idx] = Bear(*bear_bb[0])
    else:
        objects[start_idx] = NoObject()
    start_idx += 1

    for i, (miny, maxy) in zip(plate_per_col, floors):
        whiteplates_bb = [list(bb) + [objects_colors["WhitePlate"]] for bb in find_objects(
            obs, objects_colors["WhitePlate"], closing_active=False, size=(20, 7), tol_s=6, miny=miny, maxy=maxy)]
        blueplates_bb = [list(bb) + [objects_colors["BluePlate"]] for bb in find_objects(
            obs, objects_colors["BluePlate"], closing_active=False, size=(20, 7), tol_s=6, miny=miny, maxy=maxy)]
        plate_bb = whiteplates_bb+blueplates_bb
        plate_bb += [None]*(i-len(plate_bb))
        for bb in plate_bb:
            if not bb:
                objects[start_idx] = NoObject()
            elif bb[-1] == objects_colors["WhitePlate"]:
                objects[start_idx] = WhitePlate(*bb)
            elif bb[-1] == objects_colors["BluePlate"]:
                objects[start_idx] = BluePlate(*bb)
            start_idx += 1

    crabs_bb = find_objects(obs, objects_colors["crab"], miny=75, maxy=180)
    match_objects(objects, crabs_bb, start_idx, 8, Crab)
    start_idx += 8

    clams_bb = find_objects(obs, objects_colors["clam"], miny=75, maxy=180)
    match_objects(objects, clams_bb, start_idx, 8, Clam)
    start_idx += 8

    g_fish_bb = find_objects(
        obs, objects_colors["greenfish"], size=(8, 6), tol_s=2)
    match_objects(objects, g_fish_bb, start_idx, 8, GreenFish)
    start_idx += 8

    flag = find_objects(obs, [0, 0, 0], miny=43, maxy=56, minx=120, maxx=133)
    house = find_objects(
        obs, objects_colors["house"], minx=84, miny=42, maxx=155, maxy=62, closing_active=False)
    if len(flag) == 0:
        for h in house:
            objects[start_idx] = House(*house[0])
    if len(flag) != 0:
        objects[start_idx] = CompletedHouse(*house[0])

    start_idx += 1

    # # f_bite = find_mc_objects(obs, frostbite, size=(8, 17), tol_s=3)
    # # if f_bite:
    # #     objects.append(FrostBite(*f_bite[0]))
    start_idx += 1

    if hud:

        lifecount_bb = find_objects(
            obs, objects_colors["hud_objs"], closing_dist=10, minx=50, miny=19, maxx=75, maxy=32)
        if lifecount_bb:
            objects[start_idx] = LifeCount(*lifecount_bb[0])
        else:
            objects[start_idx] = NoObject()
        start_idx += 1

        degrees_bb = find_objects(
            obs, objects_colors["hud_objs"], closing_dist=10, minx=19, miny=19, maxx=37, maxy=30)
        match_objects(objects, degrees_bb, start_idx, 1, Degree)
        start_idx += 1

        score_bb = find_objects(
            obs, objects_colors["hud_objs"], closing_dist=10, minx=40, miny=8, maxx=75, maxy=18)
        match_objects(objects, score_bb, start_idx, 1, PlayerScore)
