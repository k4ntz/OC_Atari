from .utils import find_objects, find_mc_objects
from .game_objects import GameObject
import numpy as np
import matplotlib as plt


objects_colors = {
        "logs":[105,105,15], "smallpit": [0,0,0], "scorpion":[236,236,236], "rope":[72,72,0]
    }

playercolors = [[105,105,15],[228,111,111],[92,186,92],[53,95,24]]
wallcolors = [[167,26,26],[0,0,0],[142,142,142]]
c_house_colors=[[142,142,142],[0,0,0]]
frostbite=[[84,138,210],[66,114,194],[45,87,176],[24,59,157]]


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

def _detect_objects_pitfall(objects, obs, hud=False):
    # detection and filtering
    objects.clear()

    player = find_mc_objects(obs, playercolors, size=(7, 20), tol_s=4)
    if player:
        objects.append(Player(*player[0]))

    wall = find_mc_objects(obs, wallcolors, size=(7, 35), tol_s=2, closing_active=False)
    for w in wall:
        objects.append(Wall(*w))
    logs=find_objects(obs,objects_colors["logs"],size=(6,14),tol_s=2,maxy=130,miny=114)
    for l in logs:
        objects.append(Logs(*l))
    sp=find_objects(obs,objects_colors["smallpit"],size=(8,6),tol_s=4,maxy=130,miny=114)
    for s in sp:
        objects.append(StairPit(*s))

    sc=find_objects(obs,objects_colors["scorpion"],size=(7,10),tol_s=3,maxy=178,miny=160)
    for s in sc:
        objects.append(Scorpion(*s))

    rope=find_objects(obs,objects_colors["rope"],size=(10,10),tol_s=10,maxy=114,miny=64,minx=52,maxx=107)
    for r in rope:
        objects.append(Rope(*s))
    

    if hud:
        pass