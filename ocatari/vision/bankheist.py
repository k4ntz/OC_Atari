from .game_objects import GameObject, NoObject
from .utils import find_objects, find_mc_objects, most_common_color, match_objects, \
    match_blinking_objects, find_exact_bounding_boxes
import numpy as np

objects_colors = {"player": [162, 98, 33], "police": [24, 26, 167], "bank": [142, 142, 142],
                  "gaz": [[167, 26, 26], [142, 142, 142]], "black": [0, 0, 0],
                  "explosion": [(74, 74, 74), (111, 111, 111), (142, 142, 142)]}


class Player(GameObject):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.rgb = [162, 98, 33]


class Police(GameObject):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.rgb = [24, 26, 167]
        self.num_frames_invisible = -1
        self.max_frames_invisible = 4


class Bank(GameObject):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.rgb = [142, 142, 142]
        self.num_frames_invisible = -1
        self.max_frames_invisible = 4


class Dynamite(GameObject):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.num_frames_invisible = -1
        self.max_frames_invisible = 4

#  ---- HUD -----


class Score(GameObject):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.rgb = [0, 0, 0]


class Life(GameObject):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.rgb = [162, 98, 33]


class Gas_Tank(GameObject):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.rgb = [167, 26, 26]


def _detect_objects(objects, obs, hud=False):
    player = objects[0]
    wall_color = most_common_color(obs[37:187, 12:148, :])
    if wall_color in objects_colors["explosion"]:
        walls = []
    else:
        # extremely slow
        walls = find_exact_bounding_boxes(
            obs, wall_color, minx=10, maxx=150, miny=37, maxy=187)
    player_bb = find_objects(obs, objects_colors["player"], miny=40, maxy=175)
    for bb in player_bb:
        player.xywh = bb

    bank_bb = find_objects(obs, objects_colors["bank"], miny=40, maxy=175,
                           size=(8, 8), tol_s=(3, 3))
    match_blinking_objects(objects, bank_bb, 1, 3, Bank)

    police = find_objects(obs, objects_colors["police"], miny=40, maxy=175)
    match_blinking_objects(objects, police, 4, 3, Police)

    dynamites_bb = []
    for wall in walls:
        if wall[-1] < 3:
            dynamites_bb.append(wall)
    match_blinking_objects(objects, dynamites_bb, 7, 2, Dynamite, obs)

    if hud:
        score = find_objects(
            obs, objects_colors["black"], minx=13, maxx=146, miny=175, maxy=186, closing_dist=6, min_distance=1)
        match_objects(objects, score, 7, 1, Score)

        lives_bb = find_objects(obs, objects_colors["player"], maxy=40)
        match_objects(objects, lives_bb, 8, 6, Life)

        gas = find_mc_objects(
            obs, objects_colors["gaz"], maxy=40, closing_dist=2, all_colors=False)
        match_objects(objects, gas, 14, 1, Gas_Tank)
