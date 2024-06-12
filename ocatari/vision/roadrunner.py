from .utils import find_objects, find_mc_objects
from .game_objects import GameObject
import numpy as np

objects_colors = {
    "birdseeds": [84, 92, 214], "cactus": [187, 187, 53],
    "PlayerScore": [0,0,0], "sign": [0, 0, 0],
    "hud_objs": [20, 60, 0], "SteelShotSign": [214,92,92], "AcmeMineSign": [84,92,214], "AcmeMine": [84,92,214], "AcmeMine2": [66,72,200], "AcmeMine3": [101,111,228],
    "turret":[66,72,200], "turretball1":[198,108,58], "turretball2":[181,83,40]
    }

playercolors = [[101, 111, 228], [84, 92, 214], [66, 72, 200]]
enemycolors = [[198, 108, 58], [181, 83, 40], [213, 130, 74]]
truckcolors = [[252, 224, 112], [198, 108, 58], [213, 130, 74], [181, 83, 40]]
birdcolors=[[132,144,252],[252,188,116]]
roadcrackcolors=[[181,83,40],[198,108,58],[213,130,74]]
turretcolors=[[84,92,214],[101,111,228]]
stonecolors=[[181,83,40],[198,108,58],[198,108,58]]


class Player(GameObject):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.rgb = 101, 111, 228
        self.hud = False


class Enemy(GameObject):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.rgb = 198, 108, 58
        self.hud = False


class BirdSeeds(GameObject):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.rgb = 84, 92, 214
        self.hud = False


class Truck(GameObject):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.rgb = 198, 108, 58
        self.hud = False

class RoadCrack(GameObject):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.rgb =181, 83,40
        self.hud = False

class AcmeMine(GameObject):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.rgb = 84,92,214
        self.hud = False

class Turret(GameObject):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.rgb = 66,72,200
        self.hud = False

class TurretBall(GameObject):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.rgb = 198,108,58
        self.hud = False

class Stone(GameObject):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.rgb = 181,83,40
        self.hud = False

class Cactus(GameObject):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.rgb =187, 187, 53
        self.hud = True


class Sign(GameObject):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.rgb = 0, 0, 0
        self.hud = True

class SteelShotSign(GameObject):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.rgb = 214,92,92
        self.hud = True

class AcmeMineSign(GameObject):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.rgb = 84,92,214
        self.hud = True


class Bird(GameObject):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.rgb = 252,188,116
        self.hud = True


class PlayerScore(GameObject):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.rgb = 0,0,0
        self.hud = True


def _detect_objects(objects, obs, hud=False):
    # detection and filtering
    objects.clear()
    player = find_mc_objects(obs, playercolors, size=(8, 28), tol_s=8, miny=37, min_distance=1)
    if player:
        objects.append(Player(*player[0]))
    enemy = find_mc_objects(obs, enemycolors, size=(8, 28), tol_s=8, miny=37, min_distance=1)
    if enemy:
        objects.append(Enemy(*enemy[0]))
    birdseeds = find_objects(obs, objects_colors["birdseeds"], closing_dist=4,size=(5,3), tol_s=1)
    for seed in birdseeds:
        objects.append(BirdSeeds(*seed))
    trucks = find_mc_objects(obs, truckcolors, size=(16, 18), tol_s=2, min_distance=1)
    for truck in trucks:
        objects.append(Truck(*truck))
    am= find_objects(obs, objects_colors["AcmeMine"], closing_active=False, size=(4,3), tol_s=1)
    for s in am:
            if player:
                if abs(s[0]-player[0][0])<10:
                    pass
                elif abs(s[1]-player[0][1])<28:
                    pass
                else:
                    objects.append(AcmeMine(*s))
            else:
                objects.append(AcmeMine(*s))
    am= find_objects(obs, objects_colors["AcmeMine2"], closing_active=False, size=(4,3), tol_s=1)
    for s in am:
            if player:
                if abs(s[0]-player[0][0])<10:
                    pass
                elif abs(s[1]-player[0][1])<28:
                    pass
                else:
                    objects.append(AcmeMine(*s))
            else:
                objects.append(AcmeMine(*s))
    roadcracks = find_mc_objects(obs, roadcrackcolors, size=(14,32), tol_s=5, miny=122, maxy=157)
    for r in roadcracks:
            objects.append(RoadCrack(*r))
    if len(roadcracks)==0:
        turrets = find_mc_objects(obs, turretcolors, size=(12,8), tol_s=3, miny=110, maxy=157)
        for t in turrets:
            objects.append(Turret(*t))
        turrets= find_objects(obs, objects_colors["turret"], closing_active=False, size=(12,8), tol_s=2)
        for t in turrets:
                objects.append(Turret(*t))
        turretballs= find_objects(obs, objects_colors["turretball1"], closing_active=False, size=(4,4), tol_s=2, miny=110, maxy=140)
        for t in turretballs:
                if enemy :
                    if abs(t[0]-enemy[0][0])<10:
                        pass
                    elif abs(t[1]-enemy[0][1])<28:
                        pass
                    else:
                        objects.append(TurretBall(*t))
                else:
                    objects.append(TurretBall(*t))
        turretballs= find_objects(obs, objects_colors["turretball2"], closing_active=False, size=(4,4), tol_s=2, miny=110, maxy=140)
        for t in turretballs:
                if enemy:
                    if abs(t[0]-enemy[0][0])<10:
                        pass
                    elif abs(t[1]-enemy[0][1])<28:
                        pass
                    else:
                        objects.append(TurretBall(*t))
                else:
                    objects.append(TurretBall(*t))
        stones = find_mc_objects(obs, stonecolors, size=(8, 11), tol_s=2, closing_active=False, miny=137, maxy=180)
        for s in stones:
                if enemy:
                    if abs(s[0]-enemy[0][0])<10:
                        pass
                    elif abs(s[1]-enemy[0][1])<28:
                        pass
                    else:
                        objects.append(Stone(*s))
                else:
                    objects.append(Stone(*s))
    if hud:
        cactus = find_objects(obs, objects_colors["cactus"], closing_active=False, size=(8, 8),tol_s=4)
        for cac in cactus:
            objects.append(Cactus(*cac))
        twss= find_objects(obs, objects_colors["sign"], closing_active=False, size=(18, 15), tol_s=3, miny=25, maxy=107)
        for tws in twss:
            objects.append(Sign(*tws))
        sss= find_objects(obs, objects_colors["SteelShotSign"], closing_active=False, size=(16, 13), tol_s=3, miny=25, maxy=107)
        for s in sss:
            objects.append(SteelShotSign(*s))
        ams= find_objects(obs, objects_colors["AcmeMineSign"], closing_active=False, size=(16, 13), tol_s=3, miny=25, maxy=107)
        for s in ams:
            objects.append(AcmeMineSign(*s))
        birds = find_mc_objects(obs, birdcolors, size=(6, 8), tol_s=2)
        for b in birds:
            objects.append(Bird(*b))
        # Removing player score since they are ot really needed and they create problems in some levels
        # pss= find_objects(obs, objects_colors["PlayerScore"],closing_active= False, size=(3, 5), tol_s=2, minx=8, maxx=150,miny=178, maxy=190)
        # for p in pss:
        #     objects.append(PlayerScore(*p))
