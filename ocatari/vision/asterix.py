from .utils import find_objects
from .game_objects import GameObject

objects_colors = {"score": [187, 187, 53],
                  "Cauldron": [184, 50, 50],
                  "player": [187, 187, 53],
                  "background": [0, 0, 0],
                  "enemy": [227, 110, 110],
                  "lives_1": [187, 187, 53],
                  "lives_2": [187, 187, 53],
                  }


class Player(GameObject):
    pass


def _detect_objects_asterix(objects, obs, hud=False):
    pass
