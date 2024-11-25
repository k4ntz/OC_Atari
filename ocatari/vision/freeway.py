from .utils import find_objects, match_objects
from .game_objects import GameObject

objects_colors = {"score": [228, 111, 111], "logo": [228, 111, 111], "chicken": [252, 252, 84]}

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
    chickens = find_objects(obs, objects_colors["chicken"], size=(7, 8), tol_s=3)
    i = 0
    for chicken in chickens:
        objects[i] = (Chicken(*chicken))
        i+=1


    cars_bb = []
    for carcolor in car_colors.values():
        cars_bb.extend([list(bb) + [carcolor] for bb in find_objects(obs, carcolor, min_distance=1, miny=20, maxy=184)])
    match_objects(objects, cars_bb, 2, 10, Car)
    
    if hud:
        scores = find_objects(obs, objects_colors["score"], min_distance=1, maxy=14)
        for score in scores:
            objects.append(Score(*score))
