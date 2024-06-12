from .game_objects import GameObject
from .utils import find_objects, find_mc_objects, most_common_color
import numpy as np

objects_colors = {"orange": [162, 98, 33], "blue": [24, 26, 167], "grey": [142, 142, 142], "red": [167, 26, 26],
                  "black": [0, 0, 0]}


class Player(GameObject):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.rgb = [162, 98, 33]


class Police(GameObject):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.rgb = [24, 26, 167]


class Bank(GameObject):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.rgb = [142, 142, 142]

#  ---- HUD -----
class Score(GameObject):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.rgb = [0, 0, 0]


class Life(GameObject):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.rgb = [162, 98, 33]


class Gas_Tank(GameObject):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.rgb = [167, 26, 26]


def _detect_objects(objects, obs, hud=False):
    objects.clear()

    orange = find_objects(obs, objects_colors["orange"])
    for bb in orange:
        if 40 < bb[1] < 175:
            objects.append(Player(*bb))

    police = find_objects(obs, objects_colors["blue"], miny=40, maxy=175)
    for bb in police:
        objects.append(Police(*bb))

    bank = find_objects(obs, objects_colors["grey"], miny=40, maxy=175)
    for bb in bank:
        objects.append(Bank(*bb))
        

    if hud:
        
        for bb in orange:
            if bb[1] < 40:
                objects.append(Life(*bb))

        score = find_objects(obs, objects_colors["black"], minx=13, maxx=146, miny=175, maxy=186, closing_dist=6, min_distance=1)
        for bb in score:
            objects.append(Score(*bb))

        gas = find_objects(obs, objects_colors["red"], maxy=40, closing_dist=2)
        for bb in gas:
            objects.append(Gas_Tank(*bb))
