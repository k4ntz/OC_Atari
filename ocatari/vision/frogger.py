from .utils import find_objects, match_objects
from .game_objects import GameObject

objects_colors = {"frog": [110, 156, 66]}

car_colors = {"car1": [195, 144, 61], "car2": [164, 89, 208], "car3": [82, 126, 45],
              "car4": [198, 89, 179], "car5": [236, 236, 236]}

class Frog(GameObject):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.rgb = 110, 156, 66

class Car(GameObject):
    def __init__(self, x, y, w, h, rgb):
        super().__init__(x, y, w, h)
        self.rgb = rgb

def _detect_objects(objects, obs, hud=False):
    # objects.clear()

    frog = objects[0]
    frog_bb = find_objects(obs, objects_colors["frog"], size=(7, 7), tol_s=2)[0]
    frog.xywh = frog_bb

    cars_bb, max_cars = [], 0
    for color in car_colors.values():
        cars_bb.extend([list(bb) + [color] for bb in find_objects(obs, color, minx=8, maxx=152, miny=104, maxy=170)])
    match_objects(objects, cars_bb, 1, 12, Car)