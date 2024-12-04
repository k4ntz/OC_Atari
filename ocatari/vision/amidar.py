from .game_objects import GameObject
from .utils import find_objects, find_mc_objects, most_common_color, NoObject, match_objects
import numpy as np

objects_colors = {"yellow": [252, 252, 84], "green": [135, 183, 84], "red": [214, 92, 92]}


class Player(GameObject):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.rgb = [252, 252, 84]

class Enemy(GameObject):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.rgb = [135, 183, 84]

class Warrior(Enemy):
    def __init__(self, x=0, y=160, w=7, h=7):
        super().__init__(self, x, y, w, h)
        self.rgb = [135, 183, 84]


class Pig(Enemy):
    def __init__(self, x=0, y=160, w=7, h=7):
        super().__init__(self, x, y, w, h)
        self.rgb = [214, 92, 92]


class Chicken(GameObject):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.rgb = [252, 252, 84]


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
    enemy_bb = []
    chicken_bb = []
    enemy_type = Warrior

    yellow = find_objects(obs, objects_colors["yellow"], maxy=170)
    for bb in yellow:
            # print(np.shape(obs))
            if obs[bb[1]][bb[0]][0] == 252:
                chicken_bb.append(Chicken(*bb))
            else:
                objects[0] = Player(*bb)

    green = find_objects(obs, objects_colors["green"])
    for bb in green:
            enemy_bb.append(bb) # or *bb?
            enemy_type = Warrior

    red = find_objects(obs, objects_colors["red"])
    for bb in red:
            enemy_bb.append(bb) # or *bb?
            enemy_type = Pig

    if enemy_type != type(objects[1]): #Deletes the previous enemys if the type of enemies has changed
        objects[1:7] = [NoObject()] * 6

    match_objects(objects, enemy_bb, 1, 6, enemy_type)

    match_objects(objects, chicken_bb, 7, 6, Chicken)

    if hud:
        score = find_objects(obs, objects_colors["yellow"], miny=175, closing_dist=4, min_distance=1)
        for bb in score:
                if bb[2] > 4:
                    objects.append(Score(*bb))
                else:
                    objects.append(Life(*bb))
