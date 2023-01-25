from .utils import find_objects
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


def _detect_objects_freeway(objects, obs, hud=False):
    objects.clear()

    chickens = find_objects(obs, objects_colors["chicken"], min_distance=1)
    for chicken in chickens:
        objects.append(Chicken(*chicken))

    for carcolor in car_colors.values():
        car = find_objects(obs, carcolor, min_distance=1)
        if len(car) >= 1:
            car_inst = Car(*car[0])
            car_inst.rgb = carcolor
            objects.append(car_inst)

    if hud:
        scores = find_objects(obs, objects_colors["score"], min_distance=1)
        for score in scores:
            objects.append(Score(*score))
