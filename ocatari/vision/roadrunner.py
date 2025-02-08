from .utils import find_objects, find_mc_objects,find_objects_in_color_range, match_objects
from .game_objects import GameObject, NoObject
import numpy as np

objects_colors = { 
    "blue" : [[101, 111, 228], [84, 92, 214], [66, 72, 200]],
    "red" : [[198, 108, 58], [181, 83, 40], [213, 130, 74]],         
    "truck": [[252, 224, 112], [198, 108, 58], [213, 130, 74], [181, 83, 40]],
    "sign": [[0, 0, 0], [214, 92, 92], [84, 92, 214]],
    "score": [252,252,84], 
    "bonus":[0, 0, 0],
    "bird" : [[132, 144, 252], [252, 188, 116]]

}

# lanes = [[120,125],[136,140],[150,155],[164,178]]
# seed_per_lane = [1,1,1,1]

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


class Seed(GameObject):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.rgb = 84, 92, 214
        self.hud = False


class Truck(GameObject):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.rgb = 198, 108, 58
        self.hud = False

#LEVEL 2
class RoadCrack(GameObject):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.rgb = 181, 83, 40
        self.hud = False


class AcmeMine(GameObject):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.rgb = 84, 92, 214
        self.hud = False


# class Turret(GameObject):
#     def __init__(self, *args, **kwargs):
#         super().__init__(*args, **kwargs)
#         self.rgb = 66, 72, 200
#         self.hud = False


# class TurretBall(GameObject):
#     def __init__(self, *args, **kwargs):
#         super().__init__(*args, **kwargs)
#         self.rgb = 198, 108, 58
#         self.hud = False


class Stone(GameObject):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.rgb = 181, 83, 40
        self.hud = False




class Sign(GameObject):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.rgb = 0, 0, 0
        self.hud = True


class Bird(GameObject): #Lives
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.rgb = 252, 188, 116
        self.hud = True


class Score(GameObject):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.rgb = 0, 0, 0
        self.hud = True

class Bonus(GameObject):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.rgb = 0, 0, 0
        self.hud = True


def _detect_objects(objects, obs, hud=False):
    # detection and filtering
    #objects.clear()
    
    #Player
    player = objects[0]
    player_bb = find_mc_objects(obs, objects_colors["blue"], size=(8, 32),
                                tol_s=(0,8), miny=70, closing_dist = 1)
    if player_bb:
        player.xywh = player_bb[0]
    start_idx = 1
    
    #Enemy    
    
    enemy_bb = find_mc_objects(obs, objects_colors["red"],
        size=(8, 29), tol_s = (2,2), miny=100, min_distance=0, closing_active=1) #Level 1
    if not enemy_bb:
        enemy_bb = find_mc_objects(obs, objects_colors["red"],
        size=(8, 29), tol_s = (2,2), miny=100, maxy=157, min_distance=0, closing_active=1) #Level 2
        
    match_objects(objects, enemy_bb, start_idx, 1, Enemy)
    start_idx +=1
    
    #Seed
    seed_bb = find_mc_objects(
        obs, objects_colors["blue"], closing_dist = 3, size=(5, 3), tol_s=(0,1), all_colors=False)
    match_objects(objects, seed_bb, start_idx, 4, Seed)
    start_idx+=4

    #TODO
    # for nbseed, (miny, maxy) in zip(seed_per_lane, lanes):
    #     seed_bb = [list(bb) for bb in find_objects(
    #     obs, objects_colors["seed"], closing_dist = 1, size=(5, 3), tol_s=0, miny=miny,maxy=maxy, min_distance=5)]
    #     match_objects(objects, seed_bb, start_idx, 2, Seed)
    #     start_idx += 2
    
    #Truck
    trucks_bb = find_mc_objects(obs, objects_colors["truck"], size=(16, 18), tol_s=2, all_colors = False, miny =110)
    match_objects(objects, trucks_bb, start_idx, 2, Truck)
    start_idx+=2
    
    #Roadcrack
    roadcracks_bb = find_mc_objects(obs, objects_colors['red'], size=(
                    13, 32), tol_s=1, miny=122, maxy=157, closing_active= False, min_distance=0)
    match_objects(objects, roadcracks_bb, start_idx, 2, RoadCrack)
    start_idx+=2

    #Stone
    stone_bb = find_mc_objects(obs, objects_colors['blue'], size=(4,4), tol_s=0, closing_active= False, min_distance=1)
    match_objects(objects, stone_bb, start_idx, 1, Stone)
    start_idx+=2
    
    '''for color in objects_colors["AcmeMine"]:
        am = find_objects(
            obs, color, closing_active=False, size=(4, 3), tol_s=1)
        if am:
            for s in am:
                if player:
                    if abs(s[0]-player[0][0]) < 10 or abs(s[1]-player[0][1]) < 28:
                        pass
                    else:
                        match_objects(objects, am, start_idx, 4, Seed)
                        objects.append(AcmeMine(*s))
                else:
                    objects.append(AcmeMine(*s))
    '''
    
    '''  
    if len(roadcracks) == 0:
        turrets = find_mc_objects(obs, turretcolors, size=(
            12, 8), tol_s=3, miny=110, maxy=157)
        for t in turrets:
            objects.append(Turret(*t))
        turrets = find_objects(
            obs, objects_colors["turret"], closing_active=False, size=(12, 8), tol_s=2)
        for t in turrets:
            objects.append(Turret(*t))
        turretballs = find_objects(obs, objects_colors["turretball1"], closing_active=False, size=(
            4, 4), tol_s=2, miny=110, maxy=140)
        for t in turretballs:
            if enemy:
                if abs(t[0]-enemy[0][0]) < 10:
                    pass
                elif abs(t[1]-enemy[0][1]) < 28:
                    pass
                else:
                    objects.append(TurretBall(*t))
            else:
                objects.append(TurretBall(*t))
        turretballs = find_objects(obs, objects_colors["turretball2"], closing_active=False, size=(
            4, 4), tol_s=2, miny=110, maxy=140)
        for t in turretballs:
            if enemy:
                if abs(t[0]-enemy[0][0]) < 10:
                    pass
                elif abs(t[1]-enemy[0][1]) < 28:
                    pass
                else:
                    objects.append(TurretBall(*t))
            else:
                objects.append(TurretBall(*t))
        stones = find_mc_objects(obs, stonecolors, size=(
            8, 11), tol_s=2, closing_active=False, miny=137, maxy=180)
        for s in stones:
            if enemy:
                if abs(s[0]-enemy[0][0]) < 10:
                    pass
                elif abs(s[1]-enemy[0][1]) < 28:
                    pass
                else:
                    objects.append(Stone(*s))
            else:
                objects.append(Stone(*s))'''
                
    if hud:
        sign_bb = []
        for color in objects_colors['sign']:
            sign_bb += find_objects(obs, color, closing_active=False, size=(
                18, 15), tol_s=3, miny=25, maxy=107, minx= 9)
        match_objects(objects, sign_bb, start_idx, 1, Sign)
        start_idx+=1
        
        birds_bb = find_mc_objects(obs, objects_colors['bird'], size=(6, 8), tol_s=0, min_distance=0, closing_active= False, minx=40, maxx= 80)
        match_objects(objects, birds_bb, start_idx, 2, Bird)
        start_idx+=2
        
        score_bb = find_objects(obs, objects_colors['score'], maxy=16,closing_dist=10)
        match_objects(objects, score_bb, start_idx, 1, Score)
        start_idx+=1
        
        bonus_bb = find_objects(obs, objects_colors['bonus'], minx=20, miny= 182, maxy=188, maxx = 100, closing_dist=5)
        match_objects(objects, bonus_bb, start_idx, 1, Bonus)
        start_idx+=1
        
        # ams_bb = find_objects(obs, objects_colors["AcmeMineSign"], closing_active=False, size=(
        #     16, 13), tol_s=3, miny=25, maxy=107)
        # match_objects(objects, ams_bb, 1, start_idx, AcmeMineSign)
        # start_idx+=1
    #print(objects)
