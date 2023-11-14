from .game_objects import GameObject
from .utils import find_objects, find_mc_objects, most_common_color
import numpy as np

objects_colors = {"green": [111, 210, 111], "red": [240, 128, 128], "blue": [0, 0, 148], "dark_blue": [0, 48, 100],
                  "life_green": [72, 160, 72]}


class Player(GameObject):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.rgb = [111, 210, 111]


#  ---- HUD -----
class Score(GameObject):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.rgb = [111, 210, 111]


class Life(GameObject):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.rgb = [72, 160, 72]


def _detect_objects_amidar(objects, obs, hud=False):
    objects.clear()

    player = find_mc_objects(obs, [objects_colors["green"], objects_colors["red"]], miny=40)
    for bb in player:
            objects.append(Player(*bb))
    
            

    if hud:
        score = find_objects(obs, objects_colors["green"], maxy=40, closing_dist=4, min_distance=1)
        for bb in score:
                objects.append(Score(*bb))
        
        lives = find_mc_objects(obs, [objects_colors["life_green"], objects_colors["red"]], maxy=40)
        for bb in lives:
                objects.append(Life(*bb))
