from .utils import find_objects
from .game_objects import GameObject

objects_colors = {'player': [187, 187, 53],
                  'Cauldron': [184, 50, 50],
                  'enemy': [227, 110, 110],
                  'score': [187, 187, 53],
                  'lives_1': [187, 187, 53],
                  'lives_2': [187, 187, 53],

                  }  # they still not all objects covered


class Player(GameObject):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.rgb = 187, 187, 53


class Cauldron(GameObject):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.rgb = 184, 50, 50


class Enemy(GameObject):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.rgb = 227, 110, 110


class Score(GameObject):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.rgb = 187, 187, 53  # same color as player


class Lives(GameObject):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.rgb = 187, 187, 53  # same color as player


# initialize new classes for new covered objects


# TODO
def _detect_objects_asterix(objects, obs, hud=False):
    objects.clear()
