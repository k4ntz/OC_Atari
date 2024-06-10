from .utils import find_objects, find_mc_objects, find_rope_segments
from .game_objects import GameObject
import numpy as np
import matplotlib as plt


objects_colors = {
        "logs":[105,105,15], "smallpit": [0,0,0], "scorpion":[236,236,236], "rope":[72,72,0], "waterhole": [45,109,152],
        "crocodile":[20,60,0], "hud_objs":[214,214,214]
    }

playercolors = [[105,105,15],[228,111,111],[92,186,92],[53,95,24]]
wallcolors = [[167,26,26],[142,142,142]]
snakecolors=[[167,26,26],[0,0,0],[111,111,111]]
goldenbarcolors=[[252,252,84],[236,236,236]]
firecolors=[[236,200,96],[252,188,116],[72,72,0]]
moneybagcolors=[[111,111,111],[105,105,15]]
silverbarcolors=[[142,142,142],[236,236,236]]
diamondringcolors=[[236,236,236],[252,252,84]]


class Player(GameObject):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.rgb = 53,95,24
        self.hud = False

class Wall(GameObject):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.rgb = 167,26,26
        self.hud = False

class Logs(GameObject):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.rgb = 105,105,15
        self.hud = False

class StairPit(GameObject):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.rgb = 0,0,0
        self.hud = False

class Pit(GameObject):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.rgb = 252,188,116
        self.hud = False

class Scorpion(GameObject):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.rgb = 236,236,236
        self.hud = False

class Rope(GameObject):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.rgb = 72,72,0
        self.hud = False

class Snake(GameObject):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.rgb = 167,26,26
        self.hud = False

class Tarpit(GameObject):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.rgb = 0,0,0
        self.hud = False

class Waterhole(GameObject):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.rgb = 45,109,152
        self.hud = False

class Crocodile(GameObject):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.rgb = 20,60,0
        self.hud = False

class GoldenBar(GameObject):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.rgb = 252,252,84
        self.hud = False
        
class SilverBar(GameObject):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.rgb = 142,142,142
        self.hud = False

class Fire(GameObject):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.rgb = 236,200,96
        self.hud = False

class MoneyBag(GameObject):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.rgb = 111,111,111
        self.hud = False

class DiamondRing(GameObject):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.rgb = 236,236,236
        self.hud = False

class LifeCount(GameObject):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.rgb =214,214,214
        self.hud = True

class PlayerScore(GameObject):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.rgb =214,214,214
        self.hud = True

class Timer(GameObject):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.rgb =214,214,214
        self.hud = True

def _detect_objects(objects, obs, hud=False):
    # detection and filtering
    objects.clear()
    # Rope and wall is not working 

    player = find_mc_objects(obs, playercolors, size=(7, 20), tol_s=4)
    if player:
        objects.append(Player(*player[0]))

    wall = find_mc_objects(obs, wallcolors, size=(7, 35), tol_s=5,closing_dist=5) #,miny=140,maxy=190,
    for w in wall:
        objects.append(Wall(*w))
    logs=find_objects(obs,objects_colors["logs"],size=(6,14),tol_s=2,maxy=132,miny=114)
    for l in logs:
        objects.append(Logs(*l))
    sp=find_objects(obs,objects_colors["smallpit"],size=(8,6),tol_s=2,maxy=130,miny=114)
    for s in sp:
        objects.append(StairPit(*s))

    sc=find_objects(obs,objects_colors["scorpion"],size=(7,10),tol_s=3,maxy=178,miny=160)
    for s in sc:
        objects.append(Scorpion(*s))

    rope_slices=find_rope_segments(obs, objects_colors["rope"],seg_height=(1,45), maxy=120, miny=70, minx=40, maxx=112)
    if rope_slices:
        lowest = max(rope_slices, key=lambda x:x[1])
        if lowest[3]>1:
            lowest[1]=lowest[1]+lowest[3]-1
            lowest[3]=1
        objects.append(Rope(*lowest))

    snake=find_mc_objects(obs,snakecolors,size=(8,14),tol_s=2,maxy=132,miny=114)
    for s in snake:
        objects.append(Snake(*s))
        
    tp=find_objects(obs,objects_colors["smallpit"],size=(64,10),tol_s=10,maxy=130,miny=114)#same color as small pit
    for s in tp:
        objects.append(Tarpit(*s))
    
    pp=find_objects(obs,objects_colors["smallpit"],size=(12,6),tol_s=1,maxy=130,miny=114)#same color as small pit
    for p in pp:
        objects.append(Pit(*p))
    
    wh=find_objects(obs,objects_colors["waterhole"],size=(64,10),tol_s=10,maxy=130,miny=114)
    for w in wh:
        objects.append(Waterhole(*w))
    
    gold=find_mc_objects(obs,goldenbarcolors,size=(7,13),tol_s=3,maxy=132,miny=114,closing_dist=4)
    for g in gold:
        objects.append(GoldenBar(*g))

    sc=find_objects(obs,objects_colors["crocodile"],size=(8,8),tol_s=2,maxy=132,miny=114)
    for c in sc:
        objects.append(Crocodile(*c))
    
    fire=find_mc_objects(obs,firecolors,size=(8,14),tol_s=3,maxy=132,miny=114,closing_dist=4)
    for f in fire:
        objects.append(Fire(*f))
    
    mb=find_mc_objects(obs,moneybagcolors,size=(7,14),tol_s=3,maxy=132,miny=114,closing_dist=4)
    for b in mb:
        objects.append(MoneyBag(*b))
    
    gold=find_mc_objects(obs,silverbarcolors,size=(7,13),tol_s=3,maxy=132,miny=114,closing_dist=4)
    for g in gold:
        objects.append(SilverBar(*g))
    
    gold=find_mc_objects(obs,diamondringcolors,size=(7,13),tol_s=3,maxy=132,miny=114,closing_dist=4)
    for g in gold:
        objects.append(DiamondRing(*g))
    

    if hud:
        lc = find_objects(obs, objects_colors["hud_objs"], size=(1, 8), tol_s=1, maxy=30, miny=20, minx=15, maxx=26,
                          closing_active=False)
        for l in lc:
            objects.append(LifeCount(*l))
        ps=find_objects(obs,objects_colors["hud_objs"],maxy=18,miny=7,minx=16,maxx=70,closing_dist= 8)
        for p in ps:
            objects.append(PlayerScore(*p))
        ts=find_objects(obs,objects_colors["hud_objs"],maxy=30,miny=20,minx=28,maxx=69,closing_dist= 8)
        for t in ts:
            objects.append(Timer(*t))
