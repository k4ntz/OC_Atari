from .game_objects import GameObject
from .utils import find_objects, find_mc_objects, most_common_color
import numpy as np

objects_colors = {"yellow": [252, 252, 84], "green": [135, 183, 84], "red": [214, 92, 92]}


class Player(GameObject):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.rgb = [252, 252, 84]


class Monster_green(GameObject):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.rgb = [135, 183, 84]


class Monster_yellow(GameObject):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.rgb = [252, 252, 84]


class Monster_red(GameObject):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.rgb = [214, 92, 92]


#  ---- HUD -----
class Score(GameObject):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.rgb = [252, 252, 84]


class Life(GameObject):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.rgb = [252, 252, 84]


def _detect_objects(objects, obs, hud=False):
    objects.clear()

    yellow = find_objects(obs, objects_colors["yellow"], maxy=170)
    for bb in yellow:
            # print(np.shape(obs))
            if obs[bb[1]][bb[0]][0] == 252:
                objects.append(Monster_yellow(*bb))
            else:
                objects.append(Player(*bb))

    green = find_objects(obs, objects_colors["green"])
    for bb in green:
            objects.append(Monster_green(*bb))

    red = find_objects(obs, objects_colors["red"])
    for bb in red:
            objects.append(Monster_red(*bb))

    if hud:
        score = find_objects(obs, objects_colors["yellow"], miny=175, closing_dist=4, min_distance=1)
        for bb in score:
                if bb[2] > 4:
                    objects.append(Score(*bb))
                else:
                    objects.append(Life(*bb))
