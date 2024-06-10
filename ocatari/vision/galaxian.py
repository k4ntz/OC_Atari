from .utils import find_objects, find_mc_objects
from .game_objects import GameObject

objects_colors = {
    "player": [236, 236, 236], 
    "sentry": [135, 183, 84],
                  "deathray": [[101, 209, 174], [72, 160, 72]], "score": [252, 188, 116],
                  "projectile": [[45, 109, 152], [84, 138, 210], [125, 48, 173], [127, 92, 213],
                                 [158, 208, 101], [164, 89, 208], [184, 70, 162], [187, 187, 53],
                                 [227, 151, 89], [228, 11, 111], [252, 188, 116]]
                  }


class Player(GameObject):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.rgb = 236, 236, 236


class Sentry(GameObject):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.rgb = 135, 183, 84

def _detect_objects(objects, obs, hud=True):
    objects.clear()
    player = find_objects(obs, objects_colors["player"], miny=166)
    for play in player:
        objects.append(Player(*play))
    sentries = find_objects(obs, objects_colors["sentry"])
    for sent in sentries:
        objects.append(Sentry(*sent))
