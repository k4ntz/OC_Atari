from .game_objects import GameObject, NoObject
from .utils import find_objects, find_mc_objects, most_common_color, match_objects
import numpy as np

objects_colors = {"Player": [92, 186, 92], "Boat1": [184, 70, 162], "Boat2": [181, 108, 224],
                  "Boat3": [50, 132, 50], "Shark": [170, 170, 170], "Octopus": [0, 0, 0],
                  "Treasure": [195, 144, 61], "Score": [236, 236, 236], "Oxygen_Meter": [198, 108, 58]}


class Player(GameObject):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.rgb = [92, 186, 92]


class Shot(GameObject):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.rgb = [170, 170, 170]


class Oxygen_Boat(GameObject):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.rgb = [184, 70, 162]


class Oxygen_Pipe(GameObject):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.rgb = [170, 170, 170]


class Shark(GameObject):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.rgb = [170, 170, 170]


class Treasure(GameObject):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.rgb = [195, 144, 61]


class Octopus(GameObject):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.rgb = [0, 0, 0]


class Tentacle(GameObject):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.rgb = [0, 0, 0]


#  ---- HUD -----
class Score(GameObject):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.rgb = [236, 236, 236]


class Timer(GameObject):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.rgb = [50, 132, 50]


class Oxygen_Meter(GameObject):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.rgb = [198, 108, 58]


def _detect_objects(objects, obs, hud=False):

    player = find_objects(obs, objects_colors["Player"])
    for bb in player:
        if bb[2] > 1:
            objects[0].xywh = bb
            break

    boat = find_mc_objects(
        obs, [objects_colors["Boat1"], objects_colors["Boat2"], objects_colors["Boat3"]])
    if boat:
        objects[1].xywh = boat[0]

    shark = find_objects(obs, objects_colors["Shark"])
    for bb in shark:
        if bb[3] <= 2:
            if type(objects[6]) is NoObject:
                objects[6] = Shot(*bb)
            objects[6].xywh = bb
        elif bb[2] > 1:
            if type(objects[3]) is NoObject:
                objects[3] = Shark(*bb)
            objects[3].xywh = bb
        elif bb[1] < 30:
            if type(objects[2]) is NoObject:
                objects[2] = Oxygen_Pipe(bb[0], bb[1]-5, bb[2], 123)
            objects[2].xywh = bb[0], bb[1]-5, bb[2], 123

    oct = find_objects(obs, objects_colors["Octopus"], closing_dist=1)
    for bb in oct:
        if bb[2] > 10:
            if type(objects[4]) is NoObject:
                objects[4] = Octopus(*bb)
            objects[4].xywh = bb
            oct.remove(bb)
        elif bb[3] < 3:
            oct.remove(bb)
    
    match_objects(objects, oct, 7, 360, Tentacle)

    treasue = find_objects(obs, objects_colors["Treasure"])

    if treasue:
        if type(objects[5]) is NoObject:
            objects[5] = Treasure(*treasue[0])
        objects[5].xywh = treasue[0]

    if hud:

        score = find_objects(obs, objects_colors["Score"], closing_dist=10)
        if score:
            objects[-3].xywh = score[0]
        timer = find_objects(obs, objects_colors["Boat3"], miny=75)
        if timer:
            objects[-2].xywh = timer[0]

        oxy = find_objects(obs, objects_colors["Oxygen_Meter"])
        if oxy:
            objects[-1].xywh = oxy[0]
