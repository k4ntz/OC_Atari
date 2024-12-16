from .utils import find_objects, match_objects
from .game_objects import GameObject

objects_colors = {"score": [228, 111, 111], "logo": [
    228, 111, 111], "chicken": [252, 252, 84]}

car_colors = {"car1": [167, 26, 26], "car2": [180, 231, 117], "car3": [105, 105, 15],
              "car4": [228, 111, 111], "car5": [24, 26, 167], "car6": [162, 98, 33],
              "car7": [84, 92, 214], "car8": [184, 50, 50], "car9": [135, 183, 84],
              "car10": [210, 210, 64]}


class Chicken(GameObject):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.rgb = 252, 252, 84


class Car(GameObject):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.rgb = 167, 26, 26


class Score(GameObject):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.rgb = 228, 111, 111
        super().hud = True


def _detect_objects(objects, obs, hud=False):
    chicken1, chicken2 = objects[:2]
    chicken1_bb = find_objects(
        obs, objects_colors["chicken"], size=(7, 8), tol_s=3, maxx=80)
    chicken2_bb = find_objects(
        obs, objects_colors["chicken"], size=(7, 8), tol_s=3, minx=80)
    if chicken1_bb:
        chicken1.xywh = chicken1_bb[0]
    if chicken2_bb:
        chicken2.xywh = chicken2_bb[0]

    cars = objects[2:]
    for i in range(10):
        car_bb = find_objects(
            obs, car_colors[f"car{i+1}"], min_distance=1, miny=22 + 16 * i, maxy=22 + 16 * (i + 1))
        if car_bb:
            cars[i].xywh = car_bb[0]
            cars[i].rgb = car_colors[f"car{i+1}"]

    if hud:
        pscore, escore = objects[-2:]
        pscore_bb = find_objects(
            obs, objects_colors["score"], min_distance=1, maxy=14, maxx=80)
        if pscore_bb:
            pscore.xywh = pscore_bb[0]
        escore_bb = find_objects(
            obs, objects_colors["score"], min_distance=1, maxy=14, minx=80)
        if escore_bb:
            escore.xywh = escore_bb[0]
