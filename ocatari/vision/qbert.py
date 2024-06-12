from .utils import find_objects, color_analysis
from .game_objects import GameObject


objects_colors = {"player": [181, 83, 40], "red_ball": [], "purple_ball": [146, 70, 192],
                  "coily": [146, 70, 192], "flying_discs": [], "sam": [50, 132, 50],
                  "green_ball": [50, 132, 50], "score": [210, 210, 64], "lives": [210, 210, 64]
                  }


cubes_colors = [[45, 87, 176], [210, 210, 64], [192, 192, 192], [111, 111, 111]]



class Player(GameObject):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.rgb = 181, 83, 40


class Cube(GameObject):
    def __init__(self, color, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.rgb = color


class Disk(GameObject):
    def __init__(self, color, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.rgb = color


class PurpleBall(GameObject):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.rgb = 146, 70, 192


class RedBall(GameObject):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.rgb = 223, 183, 85


class GreenBall(GameObject):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.rgb = 50, 132, 50


class Coily(GameObject):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.rgb = 146, 70, 192


class Sam(GameObject):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.rgb = 50, 132, 50


class FlyingDiscs(GameObject):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.rgb = 223, 183, 85


class Score(GameObject):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.rgb = 210, 210, 64


class Lives(GameObject):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.rgb = 210, 210, 64


def _detect_objects(objects, obs, hud=True):
    objects.clear()

    player = find_objects(obs, objects_colors["player"], closing_dist=5, min_distance=1, size=(8,20), tol_s=5)
    # player = find_objects(obs, objects_colors["player"], min_distance=1, size=(8, 20), tol_s=5)
    for bb in player:
        objects.append(Player(*bb))
    
    for ccolor in cubes_colors:
        cubes = find_objects(obs, ccolor, min_distance=1, miny=30)
        for bb in cubes:
            objects.append(Cube(ccolor, *bb))

    disk_poses = [(12, 138, 8, 2), (140, 138, 8, 2)] # x,y,w,h
    for disk_pos in disk_poses:
        cntr = color_analysis(obs, disk_pos)
        dcolor = cntr.most_common()[0][0]
        if tuple(dcolor) != (0, 0, 0):
            objects.append(Disk(dcolor, *disk_pos))

    purple_ball = find_objects(obs, objects_colors["purple_ball"], min_distance=18, size=(7, 7), tol_s=3)
    for bb in purple_ball:
        objects.append(PurpleBall(*bb))

    green_ball = find_objects(obs, objects_colors["green_ball"], min_distance=1, size=(7, 7), tol_s=3)
    for bb in green_ball:
        objects.append(GreenBall(*bb))

    # red_ball = find_objects(obs, objects_colors["red_ball"], min_distance=1, size=(7, 7), tol_s=3)
    # for bb in red_ball:
    #     objects.append(RedBall(*bb))

    coily = find_objects(obs, objects_colors["coily"], min_distance=1, size=(8, 18), tol_s=5)
    for bb in coily:
        objects.append(Coily(*bb))

    sam = find_objects(obs, objects_colors["sam"], min_distance=1, size=(8, 18), tol_s=2)
    for bb in sam:
        objects.append(Sam(*bb))

    if hud:
        score = find_objects(obs, objects_colors["score"], min_distance=1, maxy=13, closing_dist=7)
        for bb in score:
            objects.append(Score(*bb))

        lives = find_objects(obs, objects_colors["lives"], min_distance=1, miny=14, maxy=30)
        for bb in lives:
            objects.append(Lives(*bb))
