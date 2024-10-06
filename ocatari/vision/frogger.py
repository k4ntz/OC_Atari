from .utils import find_objects, match_objects
from .game_objects import GameObject

objects_colors = {"frog": [110, 156, 66]}

car_colors = [[195, 144, 61], [164, 89, 208], [82, 126, 45], [198, 89, 179], [236, 236, 236]]
cars_per_line = [2, 2, 4, 2, 2]

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
    frog_bb = find_objects(obs, objects_colors["frog"], size=(7, 7), tol_s=2)
    if frog_bb:
        frog.xywh = frog_bb[0]

    start_idx = 1
    for nbcars, color in zip(cars_per_line, car_colors):
        cars_bb = [list(bb) + [color] for bb in find_objects(obs, color, minx=8, maxx=152, miny=104, maxy=170)]
        match_objects(objects, cars_bb, start_idx, nbcars, Car)
        start_idx += nbcars