from .utils import find_objects, find_mc_objects
from .game_objects import GameObject, NoObject


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


class Enemy_Final_Fighter(GameObject):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.rgb = 74, 74, 74


class Knifes(GameObject):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.rgb = 74, 74, 74


class Score(GameObject):
    """
    Score of the game
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.rgb = 128, 232, 128


class Time(GameObject):
    """
    Time left to beat the level
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.rgb = 214, 214, 214


class Lives(GameObject):
    """
    Life value. Counts how many restarts are left before the game resets
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.rgb = 214, 214, 214


class Player_Health_Bar(GameObject):
    """
    Indicates how many hits the player can still take.
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.rgb = 232, 232, 74


class Enemy_Health_Bar(GameObject):
    """
    Indicates how many hits the enemy can still take.
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.rgb = 184, 50, 50


def _detect_objects(objects, obs, hud=False):
    # detection and filtering

    player = find_mc_objects(obs, [objects_colors["player"], objects_colors["skin1"],
                             objects_colors["black"]], minx=8, miny=95, maxy=160, size=(8, 34), tol_s=8)
    if player:
        objects[0].xywh = player[0]

    thrower = find_mc_objects(obs, [objects_colors["thrower"], objects_colors["player"],
                              objects_colors["skin1"], objects_colors["black"]], minx=8, miny=95, maxy=160, size=(8, 34), tol_s=8)
    if thrower:
        if type(objects[1]) is NoObject:
            objects[1] = Enemy_Thrower(*thrower[0])
        objects[1].xywh = thrower[0]
    else:
        objects[1] = NoObject()

    fighter = find_mc_objects(obs, [objects_colors["fighter_purple1"], objects_colors["fighter_purple2"], objects_colors["fighter_blue"],
                              objects_colors["skin2"], objects_colors["black"]], minx=8, miny=95, maxy=160, size=(8, 34), tol_s=8)
    
    if fighter:
        for i in range(3):
            try:
                if type(objects[2+i]) is NoObject:
                    objects[2+i] = Enemy_Thrower(*thrower[i])
                objects[2+i].xywh = thrower[i]
            except:
                objects[2+i] = NoObject()

    final = find_mc_objects(obs, [objects_colors["projectile"], objects_colors["skin2"], objects_colors["black"], [
                            236, 236, 236]], minx=8, miny=95, maxy=160, size=(8, 34), tol_s=8)
    if final:
        if type(objects[13]) is NoObject:
            objects[13] = Enemy_Final_Fighter(*final[0])
        objects[13].xywh = final[0]
    else:
        objects[13] = NoObject()

    proj = find_objects(obs, objects_colors["projectile"], miny=100)

    for bb in proj:
        if bb[3] < 4:
            if type(objects[14]) is NoObject:
                objects[14] = Knifes(*bb)
            objects[14].xywh = bb
            break
    else:
        objects[14] = NoObject()
