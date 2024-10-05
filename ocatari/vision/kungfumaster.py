from .utils import find_objects, find_mc_objects
from .game_objects import GameObject


objects_colors = {"player": [214, 214, 214], "thrower": [192, 192, 192], "fighter_purple1": [104, 25, 154],
                  "fighter_purple2": [125, 48, 173], "fighter_blue": [101, 183, 217], "skin1": [210, 164, 74], "skin2": [213, 130, 74],
                  "projectile": [74, 74, 74], "black": [0, 0, 0]}


class Player(GameObject):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.rgb = 214, 214, 214

class Enemy_Thrower(GameObject):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.rgb = 192, 192, 192

class Enemy_Fighter(GameObject):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.rgb = 104, 25, 154

class Projectile(GameObject):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.rgb = 74, 74, 74


def _detect_objects(objects, obs, hud=False):
    # detection and filtering
    objects.clear()

    player = find_mc_objects(obs, [objects_colors["player"], objects_colors["skin1"], objects_colors["black"]], minx=8, miny=95, maxy=160, size=(8, 34), tol_s=8)
    for el in player:
        objects.append(Player(*el))
    
    thrower = find_mc_objects(obs, [objects_colors["thrower"], objects_colors["player"], objects_colors["skin1"], objects_colors["black"]], minx=8, miny=95, maxy=160, size=(8, 34), tol_s=8)
    for el in thrower:
        objects.append(Enemy_Thrower(*el))
    
    fighter = find_mc_objects(obs, [objects_colors["fighter_purple1"], objects_colors["fighter_purple2"], objects_colors["fighter_blue"], objects_colors["skin2"], objects_colors["black"]], minx=8, miny=95, maxy=160, size=(8, 34), tol_s=8)
    for el in fighter:
        objects.append(Enemy_Fighter(*el))
    
    final = find_mc_objects(obs, [objects_colors["projectile"], objects_colors["skin2"], objects_colors["black"], [236, 236, 236]], minx=8, miny=95, maxy=160, size=(8, 34), tol_s=8)
    for el in final:
        objects.append(Enemy_Fighter(*el))
    
    proj = find_objects(obs, objects_colors["projectile"], miny=100)
    for el in proj:
        if el[3] < 4:
            objects.append(Projectile(*el))
