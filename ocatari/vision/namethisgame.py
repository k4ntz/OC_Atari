from .game_objects import GameObject
from .utils import find_objects, find_mc_objects, most_common_color
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
    objects.clear()

    player = find_objects(obs, objects_colors["Player"])
    for bb in player:
        if bb[2] > 1:
            objects.append(Player(*bb))

    boat = find_mc_objects(
        obs, [objects_colors["Boat1"], objects_colors["Boat2"], objects_colors["Boat3"]])
    for bb in boat:
        objects.append(Oxygen_Boat(*bb))

    shark = find_objects(obs, objects_colors["Shark"])
    for bb in shark:
        if bb[3] <= 2:
            objects.append(Shot(*bb))
        elif bb[2] > 1:
            objects.append(Shark(*bb))
        elif bb[1] < 30:
            objects.append(Oxygen_Pipe(bb[0], bb[1]-5, bb[2], 123))

    oct = find_objects(obs, objects_colors["Octopus"], closing_dist=1)
    for bb in oct:
        if bb[2] > 10:
            objects.append(Octopus(*bb))
        elif bb[3] > 3:
            objects.append(Tentacle(*bb))

    treasue = find_objects(obs, objects_colors["Treasure"])
    for bb in treasue:
        objects.append(Treasure(*bb))

    if hud:

        score = find_objects(obs, objects_colors["Score"], closing_dist=10)
        for bb in score:
            objects.append(Score(*bb))

        timer = find_objects(obs, objects_colors["Boat3"], miny=75)
        for bb in timer:
            objects.append(Timer(*bb))

        oxy = find_objects(obs, objects_colors["Oxygen_Meter"])
        for bb in oxy:
            objects.append(Oxygen_Meter(*bb))
