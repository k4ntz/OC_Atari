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
    "bird" : [[132, 144, 252], [252, 188, 116]],
    #"gray" :[[111,111,111],[142,142,142],[93,93,93]]

}
player_colors = [objects_colors['blue']]# +[objects_colors['gray']]


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

class AcmeMine(GameObject):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.rgb = 181, 83, 40
        self.hud = False
        
class RoadCrack(GameObject):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.rgb = 181, 83, 40
        self.hud = False


#Level 4
class Turret(GameObject):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.rgb = 66, 72, 200 #BLUE
        self.hud = False


class TurretBall(GameObject):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.rgb = 198, 108, 58 #ORANGE
        self.hud = False

class Rock(GameObject):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.rgb = 181, 83, 40
        self.hud = False


class SteelShot(GameObject):
        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)
            self.rgb = 66, 72, 200
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

    #Player
    player = objects[0]
    for color in player_colors:
        player_bb = find_mc_objects(obs, color, size=(8, 32),
                                    tol_s=(0,8), miny=70, closing_dist = 1, all_colors=False) #ALL COLOR FALSE ADDED ON LEVEL 4 AND SHOULD BE CHECKED!!!
        if player_bb:
            player.xywh = player_bb[0]
        start_idx = 1
        
    #Enemy    
    enemy_bb = find_mc_objects(obs, objects_colors["red"],
        size=(8, 29), tol_s = (2,2), miny=30, min_distance=0, closing_active=1)
    if not enemy_bb:
        enemy_bb = find_mc_objects(obs, objects_colors["red"],
        size=(8, 29), tol_s = (2,2), miny=100, maxy =157, min_distance=0, closing_active=1) #Level 2
    if not enemy_bb:
        enemy_bb = find_mc_objects(obs, objects_colors["red"],
        size=(7, 31), tol_s = (2,2), miny=100, maxy =157, min_distance=0, closing_active=1) #Level 4
    if not enemy_bb:
        enemy_bb = find_mc_objects(obs, objects_colors["red"],
        size=(12, 22) ,tol_s = (4,4), miny=80, maxy =157, min_distance=0, closing_active=1) #Level 4 enemy on the rocket  
    match_objects(objects, enemy_bb, start_idx, 1, Enemy)
    start_idx +=1
    
    #Seed
    seed_bb = find_mc_objects(
        obs, objects_colors["blue"], closing_dist = 3, size=(5, 3), tol_s=(1,1), all_colors=False)
    acmeMine_bb = []
    for s in seed_bb[:]:
        if s[2:4] == (4, 3) or s[2:4] == (4, 4) :
            acmeMine_bb.append(s)
            seed_bb.remove(s)
    match_objects(objects, seed_bb, start_idx, 4, Seed)
    start_idx+=4
    
    #Truck
    trucks_bb = find_mc_objects(obs, objects_colors["truck"], size=(16, 18), tol_s=2, all_colors = False, miny =110)
    for t in trucks_bb:
        if (obs[t[1]][t[0]]!=[252, 224, 112]).all():
            trucks_bb.remove(t)
    match_objects(objects, trucks_bb, start_idx, 2, Truck)
    start_idx+=2
    
    #Roadcrack
    roadcracks_bb = find_mc_objects(obs, objects_colors['red'], size=(
                    13, 32), tol_s=1, miny=122, maxy=157, closing_active= False, min_distance=0)
    match_objects(objects, roadcracks_bb, start_idx, 2, RoadCrack)
    start_idx+=2

    #AcmeMine
    match_objects(objects, acmeMine_bb, start_idx, 4, AcmeMine)
    start_idx+=4
    
    #SteelShot
    shot_bb = find_mc_objects(
        obs, objects_colors["blue"], closing_dist = 3, size=(10, 3), tol_s=0, all_colors=False)
    match_objects(objects, shot_bb, start_idx, 3, SteelShot)
    start_idx+=3
    
    #Turret
    turret_bb = find_mc_objects(obs, objects_colors["blue"],
        size=(12, 8), tol_s =0, miny=30, min_distance=0, closing_active=1, all_colors= False)
    match_objects(objects, turret_bb, start_idx, 1, Turret)
    start_idx+=1
    
    #TurretBall
    ball_bb = find_mc_objects(obs, objects_colors["red"],
        size=(4, 4), tol_s =0, miny=30, min_distance=0, closing_active=1, all_colors= False)
    match_objects(objects, ball_bb, start_idx, 2, TurretBall)
    start_idx+=2
    
    #Rock
    rock_bb = find_mc_objects(obs, objects_colors["red"],
        size=(8, 11), tol_s =3, miny=30, min_distance=0, closing_active=1, all_colors= False)
    match_objects(objects, rock_bb, start_idx, 2, Rock)
    start_idx+=2
    
                
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
        
       
    #print(objects)
