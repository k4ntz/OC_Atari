from .game_objects import GameObject
from .utils import find_objects

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
    objects.clear()
    ball_h = 6
    ball_w = 4
    x_special_target = 0
    for flipper in find_objects(obs, objects_colors["flipper"], miny=165, maxy=193, minx=X_MIN_GAMEZONE,
                                maxx=145):
        objects.append(Flipper(*flipper))
    for ball in find_objects(obs, objects_colors["ball"], minx=X_MIN_GAMEZONE,
                             maxx=X_MAX_GAMEZONE-1, closing_active=False):
        if ball[3] < ball_h and ball[2] < ball_w:
            objects.append(Ball(*ball))
    for drop_target in find_objects(obs, objects_colors["target"], minx=X_MIN_GAMEZONE,
                                    maxx=X_MAX_GAMEZONE, miny=24, maxy=170):
        objects.append(DropTarget(*drop_target))
    for spinner in find_objects(obs, objects_colors["spinner"], minx=X_MIN_GAMEZONE,
                                maxx=X_MAX_GAMEZONE, miny=88, maxy=102, closing_dist=12):
        objects.append(Spinner(*spinner))
    for plunger in find_objects(obs, objects_colors["plunger"], minx=147,
                                maxx=152, miny=88, maxy=102):
        objects.append(Plunger(*plunger))
    for bumper in find_objects(obs, objects_colors["bumper"], minx=26,
                               maxx=131, miny=42, maxy=147):
        if bumper[3] > ball_h and bumper[2] >= ball_w:
            objects.append(Bumper(*bumper))
    for special_target in find_objects(obs, objects_colors["target"], minx=69,
                                       maxx=140, miny=117, maxy=137):
        x_special_target = special_target[0]
        objects.append(DropTarget(*special_target))
    if hud:
        for score in find_objects(obs, objects_colors["hud"], minx=63, miny=0, maxy=16, closing_dist=6):
            objects.append(Score(*score))
        for life_used in find_objects(obs, objects_colors["hud"], minx=36,
                                      maxx=60, miny=0, maxy=16):
            objects.append(LifeUsed(*life_used))
        for difficulty_level in find_objects(obs, objects_colors["hud"], minx=0,
                                             maxx=35, miny=0, maxy=16):
            objects.append(DifficultyLevel(*difficulty_level))
    return
