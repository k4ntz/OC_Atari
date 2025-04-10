from .game_objects import GameObject, NoObject
from .utils import find_objects, match_objects

objects_colors = {"ball": [104, 72, 198], "spinner": [236, 236, 236], "flipper": [236, 236, 236],
                  "target": [210, 164, 74], "plunger": [187, 159, 71], "bumper": [104, 72, 198], "hud": [187, 159, 71]}

X_MIN_GAMEZONE = 6
X_MAX_GAMEZONE = 153


class Flipper(GameObject):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.rgb = 236, 236, 236
        self.hud = False


class Ball(GameObject):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.rgb = 104, 72, 198
        self.hud = False


class Spinner(GameObject):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.rgb = 236, 236, 236
        self.hud = False


class DropTarget(GameObject):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.rgb = 210, 164, 74
        self.hud = False


class Plunger(GameObject):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.rgb = 187, 159, 71
        self.hud = False


class Bumper(GameObject):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.rgb = 104, 72, 198
        self.hud = False


class Score(GameObject):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        value = 0
        self.rgb = 187, 159, 71
        self.hud = True


class LifeUsed(GameObject):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        value = 0
        self.rgb = 187, 159, 71
        self.hud = True


class DifficultyLevel(GameObject):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        value = 1
        self.rgb = 187, 159, 71
        self.hud = True


def _detect_objects(objects, obs, hud=True):
    ball_h = 6
    ball_w = 4
    x_special_target = 0

    for flipper in find_objects(obs, objects_colors["flipper"], miny=165, maxy=193, minx=X_MIN_GAMEZONE, maxx=145):
        if flipper[0] < 80:
            objects[0].xywh = flipper
        else:
            objects[1].xywh = flipper

    for ball in find_objects(obs, objects_colors["ball"], minx=X_MIN_GAMEZONE,
                             maxx=X_MAX_GAMEZONE-1, closing_active=False):
        if ball[3] < ball_h and ball[2] < ball_w:
            objects[2].xywh = ball

    for spinner in find_objects(obs, objects_colors["spinner"], minx=X_MIN_GAMEZONE,
                                maxx=X_MAX_GAMEZONE, miny=88, maxy=102, closing_dist=12):
        if spinner[0] < 80:
            objects[3].xywh = spinner
        else:
            objects[4].xywh = spinner

    drop_target = find_objects(obs, objects_colors["target"], minx=X_MIN_GAMEZONE,
                                    maxx=X_MAX_GAMEZONE, miny=24, maxy=170)
    match_objects(objects, drop_target, 5, 11, DropTarget)

    for special_target in find_objects(obs, objects_colors["target"], minx=69,
                                       maxx=140, miny=117, maxy=137):
        if type(objects[16]) is NoObject:
            objects[16] = DropTarget(*special_target)
        else:
            objects[16].xywh = special_target

    plunger = find_objects(obs, objects_colors["plunger"], minx=145,
                                maxx=152, miny=88, maxy=180)
    if plunger:
        objects[25].xywh = plunger[0]
    # objects.append(Plunger(*plunger))
