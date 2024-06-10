from .utils import find_objects, find_mc_objects
from .game_objects import GameObject
import numpy as np
import matplotlib as plt


objects_colors = {
    "WhitePlate": [214,214,214], "BluePlate": [84,138,210],
    "Bird": [132,144,252],
    "hud_objs": [132,144,252], "house":[142,142,142], "greenfish":[111,210,111],
    "crab": [213,130,74], "clam":[210,210,64], "bear":[111,111,111]
    }

playercolors = [[162, 98,33], [198,108,58], [142,142,142],[162,162,42]]
logocolors = [[214,214,214], [184, 50, 50], [180,122,48],[210,210,64],[110,156,66],[45,50,184]]
c_house_colors=[[142,142,142],[0,0,0]]
frostbite=[[84,138,210],[66,114,194],[45,87,176],[24,59,157]]


class Player(GameObject):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.rgb = 198,108,58
        self.hud = False


class GreenFish(GameObject):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.rgb = 111,210,111
        self.hud = False


class FrostBite(GameObject):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.rgb = 84,38,210
        self.hud = False


class WhitePlate(GameObject):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.rgb = 214,214,214
        self.hud = False


class BluePlate(GameObject):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.rgb = 84,138,210
        self.hud = False


class Bird(GameObject):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.rgb = 132,144,252
        self.hud = False


class Bear(GameObject):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.rgb = 0,0,0
        self.hud = False


class Crab(GameObject):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.rgb = 213,130,74
        self.hud = False


class Clam(GameObject):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.rgb = 210,210,64
        self.hud = False

class House(GameObject):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.rgb = 142,142,142
        self.hud = False


class CompletedHouse(GameObject):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.rgb = 0,0,0
        self.hud = False


class LifeCount(GameObject):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.rgb =132,144,252
        self.hud = True


class PlayerScore(GameObject):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.rgb =132,144,252
        self.hud = True


class Degree(GameObject):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.rgb =132,144,252
        self.hud = True


# class PlayerScore(GameObject):
#     def __init__(self, *args, **kwargs):
#         super().__init__(*args, **kwargs)
#         self.rgb = 0,0,0
#         self.hud = True

def _detect_objects(objects, obs, hud=False):
    # detection and filtering
    objects.clear()

    player = find_mc_objects(obs, playercolors, size=(8, 17), tol_s=3)
    if player:
        objects.append(Player(*player[0]))
    blueplate = find_objects(obs, objects_colors["BluePlate"], closing_active=False, size=(20,7), tol_s=6)
    for b in blueplate:
        objects.append(BluePlate(*b))
    whiteplate = find_objects(obs, objects_colors["WhitePlate"], closing_active=False, size=(20,7), maxy=185,tol_s=6)
    for w in whiteplate:
        objects.append(WhitePlate(*w))
    bird = find_objects(obs, objects_colors["Bird"], closing_dist=5, size=(8,7), tol_s=2)
    for b in bird:
        objects.append(Bird(*b))
    flag=find_objects(obs,[0,0,0],miny=43,maxy=56,minx=120,maxx=133)
    house = find_objects(obs, objects_colors["house"], minx=84, miny=42,maxx=155,maxy=64)
    if len(flag)==0:
        for h in house:
            objects.append(House(*h))
    if len(flag)!=0:
        c_house = find_mc_objects(obs, c_house_colors, size=(34, 20), tol_s=5)
        if c_house:
            objects.append(CompletedHouse(*c_house[0]))
    # f_bite = find_mc_objects(obs, frostbite, size=(8, 17), tol_s=3)
    # if f_bite:
    #     objects.append(FrostBite(*f_bite[0]))
    g_fish = find_objects(obs, objects_colors["greenfish"], size=(8,6),tol_s=2)
    for g in g_fish:
        objects.append(GreenFish(*g))
    crab = find_objects(obs, objects_colors["crab"], miny=75,maxy=180)
    for c in crab:
        objects.append(Crab(*c))
    clam = find_objects(obs, objects_colors["clam"], miny=75,maxy=180)
    for c in clam:
        objects.append(Clam(*c))
    bear = find_objects(obs, objects_colors["bear"], miny=13,maxy=75,size=(14,15),tol_s=5)
    for b in bear:
        objects.append(Bear(*b))
    

    if hud:
        lifecount = find_objects(obs, objects_colors["hud_objs"], closing_dist=5, minx=50, miny=19, maxx=75,maxy=32,size=(6,8), tol_s=2)
        for l in lifecount:
            objects.append(LifeCount(*l))
        score = find_objects(obs, objects_colors["hud_objs"], closing_active=False, minx=45, miny=8, maxx=75,maxy=18,size=(6,8), tol_s=2)
        for s in score:
            objects.append(PlayerScore(*s))
        degrees = find_objects(obs, objects_colors["hud_objs"], closing_dist=2, minx=19, miny=19, maxx=37,maxy=30,size=(6,8), tol_s=2)
        for d in degrees:
            objects.append(Degree(*d))
