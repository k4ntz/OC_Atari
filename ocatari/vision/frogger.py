from .utils import find_objects
from .game_objects import GameObject

objects_colors = {"frog": [110, 156, 66]}

class Frog(GameObject):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.rgb = 110, 156, 66

def _detect_objects(objects, obs, hud=False):
    objects.clear()

    frog = find_objects(obs, objects_colors["frog"], size=(6, 6), tol_s=2)
    for el in frog:
        objects.append(Frog(*el))