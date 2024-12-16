from .utils import find_objects
from .game_objects import GameObject
import numpy as np
import matplotlib as plt

objects_colors = {
    "Player": [192, 192, 192], "hud_objs": [0, 0, 0]
}

carcolors = [[136, 146, 62], [72, 160, 72], [104, 72, 198], [66, 136, 176], [66, 114, 194], [198, 108, 58], [
    162, 162, 42], [66, 158, 130], [162, 134, 56], [110, 156, 66], [184, 70, 162], [66, 72, 200], [200, 72, 72]]
nightcar_colors = [[200, 72, 72]]


class Player(GameObject):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.rgb = 192, 192, 192
        self.hud = False


class Car(GameObject):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.rgb = 192, 192, 192
        self.hud = False


class PlayerScore(GameObject):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.rgb = 132, 144, 252
        self.hud = True


class NumberOfCars(GameObject):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.rgb = 0, 0, 0
        self.hud = True


class Level(GameObject):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.rgb = 0, 0, 0
        self.hud = True


def _detect_objects(objects, obs, hud=False):
    # detection and filtering
    objects.clear()
    player = find_objects(obs, objects_colors["Player"], size=(
        16, 11), tol_s=3, closing_dist=2)
    if player:
        objects.append(Player(*player[0]))

    for color in carcolors:
        cars = find_objects(obs, color, size=(10, 10),
                            tol_s=8, maxy=156, closing_dist=5)
        for c in cars:
            c_obj = Car(*c)
            c_obj.rgb = color
            objects.append(c_obj)

    if hud:
        # score=find_objects(obs,objects_colors["hud_objs"],size=(40,8),tol_s=5,maxy=175,miny=163,maxx=105, minx=55,closing_dist=3)
        # for s in score:
        #     objects.append(PlayerScore(*s))

        # Hardcoding this step due to segmentation issues
        score = (65, 164, 38, 9)
        objects.append(PlayerScore(*score))

        level = (56, 180, 8, 8)
        objects.append(Level(*level))

        num_cars = (79, 180, 24, 7)
        objects.append(NumberOfCars(*num_cars))
        # num_cars=find_objects(obs,objects_colors["hud_objs"],size=(22,10),tol_s=5,maxy=190,miny=177,maxx=105, minx=79,closing_dist=5)
        # for n in num_cars:
        #     objects.append(NumberOfCars(*n))
