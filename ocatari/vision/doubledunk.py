from .game_objects import GameObject
from .utils import find_objects, find_mc_objects, most_common_color
import numpy as np

objects_colors = {"Player": [45, 129, 105], "Opponent": [236, 236, 236], "Ball": [144, 72, 17],
                  "Skin_color1": [160, 171, 79], "Skin_color1": [80, 89, 22],
                  "Basket": [162, 162, 42], "Backboard": [214, 214, 214]}


class Player_Small(GameObject):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.rgb = [45, 129, 105]

class Player_Big(GameObject):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.rgb = [45, 129, 105]

class Opponent_Small(GameObject):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.rgb = [236, 236, 236]

class Opponent_Big(GameObject):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.rgb = [236, 236, 236]

class Ball(GameObject):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.rgb = [144, 72, 17]

class Basket(GameObject):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.rgb = [162, 162, 42]

class Backboard(GameObject):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.rgb = [214, 214, 214]



#  ---- HUD -----
class Player_Score(GameObject):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.rgb = [45, 129, 105]

class Opponent_Score(GameObject):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.rgb = [236, 236, 236]


def _detect_objects(objects, obs, hud=False):
    objects.clear()

    player = find_mc_objects(obs, [objects_colors["Player"], ["Skin_color1"]])
    for bb in player:
        objects.append(Player_Small(*bb))

    if hud:
        pass
