import numpy as np

from .game_objects import GameObject
from .utils import find_objects

objects_colors = {"shark": [0, 0, 0], "fish": [232, 232, 74],
                  "player 1 fishing string": [232, 232, 74],
                  "score": [167, 26, 26], "player 2 fishing string": [0, 0, 0]
                  }


class Shark(GameObject):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.rgb = 0, 0, 0
        self.direction = True  # is the shark going from right to left


class Fish(GameObject):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.rgb = 232, 232, 74
        self.hooked = False


class PlayerOneHook(GameObject):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.rgb = 232, 232, 74
        self.hook_position = 0, 0


class ScorePlayerTwo(GameObject):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.rgb = 167, 26, 26


class PlayerTwoHook(GameObject):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.rgb = 0, 0, 0
        self.hook_position = 0, 0


class ScorePlayerOne(GameObject):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.rgb = 167, 26, 26


def _detect_objects_fishingderby(objects, obs, hud=True):
    objects.clear()

    count_shark = 0
    for shark in find_objects(obs, objects_colors["shark"], closing_dist=1, minx=28, maxx=131, miny=80, maxy=93):
        shark_instance = Shark(*shark)
        if shark_instance.w > 20:
            objects.append(shark_instance)
            count_shark += 1

    for fish in find_objects(obs, objects_colors["fish"], closing_dist=8, miny=85):
        fish_instance = Fish(*fish)
        if 90 < fish_instance.y < 190:
            objects.append(fish_instance)

    for p1_fish_hook in find_objects(obs, objects_colors["player 1 fishing string"], closing_dist=1):
        x, y, w, h = p1_fish_hook
        if y < 80 and x > 25:
            if np.shape(find_objects(obs, objects_colors["player 1 fishing string"], minx=x + w - 3, maxx=x + w,
                                     miny=y + h - 3, maxy=y + h))[0] != 0:
                p1_hook = PlayerOneHook(x=x + w - 2, y=y + h - 2, w=4, h=4)
                p1_hook.hook_position = x + w, y + h
                objects.append(p1_hook)
            else:
                p1_hook = PlayerOneHook(x=x - 2, y=y + h - 2, w=4, h=4)
                p1_hook.hook_position = x, y + h
                objects.append(p1_hook)

    for p2_fish_hook in find_objects(obs, objects_colors["player 2 fishing string"], miny=75, minx=30, maxx=130,
                                     maxy=188, closing_dist=1):
        x, y, w, h = p2_fish_hook
        if 80 > y:
            if len(find_objects(obs, objects_colors["player 2 fishing string"], minx=x + w - 3, maxx=min(x + w, 131),
                                miny=y + h - 3, maxy=y + h)) != 0:
                objects.append(PlayerTwoHook(x=x + w - 2, y=y + h - 2, w=4, h=4))
            else:
                objects.append(PlayerTwoHook(x=x - 2, y=y + h - 2, w=4, h=4))

    if hud:
        for score in find_objects(obs, objects_colors["score"], closing_dist=1):
            if score[1] < 20:
                if score[0] < 80:
                    objects.append(ScorePlayerOne(*score))
                else:
                    objects.append(ScorePlayerTwo(*score))
