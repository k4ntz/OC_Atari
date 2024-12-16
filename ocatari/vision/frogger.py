
from .utils import find_objects, match_objects, match_blinking_objects
from .game_objects import GameObject


objects_colors = {"frog": [[110, 156, 66], [162, 162, 42]], "log": [105, 105, 15], "turtle": [[144, 72, 17], [66, 114, 194]],
                  "lady frog": [236, 236, 236], "alligator": [105, 105, 15], "snake": [82, 126, 45], "happy frog": [82, 126, 45],
                  "alligator's head": [110, 156, 66], "fly": [110, 156, 66],
                  "score": [195, 144, 61], "lives": [236, 236, 236], "time": [[0, 0, 0], [144, 72, 17]]}

car_colors = [[195, 144, 61], [164, 89, 208], [
    82, 126, 45], [198, 89, 179], [236, 236, 236]]
lane_limits = [[158, 170], [147, 159], [134, 146], [121, 133], [104, 120]]
max_cars_per_line = [6, 6, 6, 6, 2]


logs_per_line = [3, 2, 3]
logs_lane_limits = [[66, 78], [53, 65], [27, 39]]

turtles_per_line = [6, 4]
turtles_lane_limits = [[79, 91], [40, 52]]

frog_limit_x = [[12, 20], [44, 52], [76, 82], [108, 116], [140, 148]]
max_frog_per_col = [1, 1, 1, 1, 1]

snakes_limit_y = [[55, 65], [85, 100]]
max_snake_per_line = [1, 1]


class Frog(GameObject):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.rgb = 110, 156, 66


class Log(GameObject):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.rgb = 105, 105, 15
        self.num_frames_invisible = -1
        self.max_frames_invisible = 4


class Alligator(GameObject):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.rgb = 105, 105, 15
        self.num_frames_invisible = -1
        self.max_frames_invisible = 4


class Turtle(GameObject):
    def __init__(self, x, y, w, h, rgb=[144, 72, 17]):
        super().__init__(x, y, w, h)
        self.rgb = rgb
        self.num_frames_invisible = -1
        self.max_frames_invisible = 4

    @property
    def diving(self):
        return self.rgb == [66, 114, 194]


class LadyFrog(GameObject):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.rgb = 236, 236, 236
        self.num_frames_invisible = -1
        self.max_frames_invisible = 6


class Snake(GameObject):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.rgb = 82, 126, 45
        self.num_frames_invisible = -1
        self.max_frames_invisible = 4


class HappyFrog(GameObject):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.rgb = 82, 126, 45
        self.num_frames_invisible = -1
        self.max_frames_invisible = 4


class AlligatorHead(GameObject):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.rgb = 110, 156, 66
        self.num_frames_invisible = -1
        self.max_frames_invisible = 4


class Fly(GameObject):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.rgb = 110, 156, 66
        self.num_frames_invisible = -1
        self.max_frames_invisible = 4


class Car(GameObject):
    def __init__(self, x, y, w, h, rgb=[144, 72, 17]):
        super().__init__(x, y, w, h)
        self.rgb = rgb
        self.num_frames_invisible = -1
        self.max_frames_invisible = 4


class Score(GameObject):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.rgb = 195, 144, 61
        self.hud = True


class Lives(GameObject):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.rgb = 236, 236, 236
        self.hud = True


class Time(GameObject):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.rgb = 0, 0, 0
        self.hud = True


def _detect_objects(objects, obs, hud=False):
    frog = objects[0]
    # Detect Frog
    for color in objects_colors["frog"]:
        frog_bb = find_objects(obs, color)
        if frog_bb:
            frog.xywh = frog_bb[0]
            frog.rgb = color

    # Detect Cars
    start_idx = 1
    for nbcars, color, (miny, maxy) in zip(max_cars_per_line, car_colors, lane_limits):
        cars_bb = [list(bb) + [color] for bb in find_objects(obs, color,
                                                             closing_active=True, minx=8, maxx=152, miny=miny, maxy=maxy)]
        match_blinking_objects(objects, cars_bb, start_idx, nbcars, Car)
        start_idx += nbcars

    aligators_bb = []
    # Detect Log and Alligator
    for nblogs, (miny, maxy) in zip(logs_per_line, logs_lane_limits):
        logs_bb = find_objects(
            obs, objects_colors["log"], closing_active=True, minx=8, maxx=152, miny=miny, maxy=maxy)
        for bb in logs_bb:
            if not (obs[bb[1]][bb[0]] == [105, 105, 15]).all():  # check if it is an alligator
                aligators_bb.append(bb)
                logs_bb.remove(bb)
        match_blinking_objects(objects, logs_bb, start_idx, nblogs, Log)
        start_idx += nblogs
    # Detect Alligator
    if aligators_bb:
        match_objects(objects, aligators_bb, start_idx, 2, Alligator)
    start_idx += 2
    # Detect Turtle
    for nbturtles, (miny, maxy) in zip(turtles_per_line, turtles_lane_limits):
        turtles_bb = []
        for color in objects_colors["turtle"]:
            turtles_bb += [list(bb) + [color]
                           for bb in find_objects(obs, color, miny=miny, maxy=maxy)]
        match_blinking_objects(objects, turtles_bb,
                               start_idx, nbturtles, Turtle)
        start_idx += nbturtles

    # Detect lady frog
    lady_bb = find_objects(
        obs, objects_colors["lady frog"], maxy=100, size=(8, 11))
    match_blinking_objects(objects, lady_bb, start_idx, 1, LadyFrog)
    start_idx += 1

    flys_bb = []
    heads_bb = []
    # Detect Alligator's Head and flys
    heads_bb = find_objects(
        obs, objects_colors["alligator's head"], miny=15, maxy=30, minx=11, maxx=149, size=(8, 10), tol_s=2)
    for bb in heads_bb:
        if not (obs[bb[1]+8][bb[0]] == [110, 156, 66]).all():  # check if it is a fly
            flys_bb.append(bb)
            heads_bb.remove(bb)
    match_blinking_objects(objects, heads_bb, start_idx, 1, AlligatorHead)
    start_idx += 1

    # Detect fly
    match_blinking_objects(objects, flys_bb, start_idx, 1, Fly)
    start_idx += 1

    # Detect Happy Frogs
    for i, (minx, maxx) in zip(max_frog_per_col, frog_limit_x):
        frog_bb = [bb for bb in find_objects(
            obs, objects_colors["happy frog"], maxy=26, miny=14, minx=minx, maxx=maxx, size=(8, 10), tol_s=2)]
        match_blinking_objects(objects, frog_bb, start_idx, i, HappyFrog)
        start_idx += i

    # frogs_bb = []
    # for (minx,maxx) in frog_limit_x :
    #     frogs_bb += find_objects(obs, objects_colors["happy frog"], maxy= 26, miny =14, minx=minx, maxx= maxx, size=(8,10), tol_s = 2)
    # match_objects(objects, frogs_bb, start_idx, 5, HappyFrog)
    # start_idx+=5

    # Detect Snakes
    for i, (miny, maxy) in zip(max_snake_per_line, snakes_limit_y):
        snake_bb = [bb for bb in find_objects(
            obs, objects_colors["snake"], minx=8, maxx=152, miny=miny, maxy=maxy, size=(16, 5), tol_s=2)]
        match_blinking_objects(objects, snake_bb, start_idx, i, Snake)
        start_idx += i

    # HUD elements: Score, Lives and Time
    if hud:
        score = find_objects(
            obs, objects_colors["score"], miny=0, maxy=20, closing_dist=10)
        match_objects(objects, score, start_idx, 1, Score)
        start_idx += 1

        lives = find_objects(obs, objects_colors["lives"], miny=180, maxy=200)
        match_objects(objects, lives, start_idx, 1, Lives)
        start_idx += 1

        time = []
        for color in objects_colors["time"]:
            time += find_objects(obs, color, miny=180,
                                 maxy=200, minx=120, maxx=190)
        match_objects(objects, time, start_idx, 1, Time)
        start_idx += 1
