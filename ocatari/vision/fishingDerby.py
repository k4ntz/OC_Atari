from .utils import find_objects
from .game_objects import GameObject

objects_colors = {"shark": [0, 0, 0], "fish": [232, 232, 74],
                  "player 1 fishing string": [232, 232, 74],
                  "score": [167, 26, 26], "player 2 fishing string": [0, 0, 0],
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


class PlayerOneFishingString(GameObject):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.rgb = 232, 232, 74
        self.hook_position = 0, 0


class ScorePlayerTwo(GameObject):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.rgb = 167, 26, 26


class PlayerTwoFishingString(GameObject):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.rgb = 0, 0, 0
        self.hook_position = 0, 0


class ScorePlayerOne(GameObject):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.rgb = 167, 26, 26


def _detect_objects_fishingDerby(objects, obs, hud=True):
    objects.clear()

    count_shark = 0
    for shark in find_objects(obs, objects_colors["shark"], closing_dist=1, minx=30, maxx=126, miny=75, maxy=96):
        shark_instance = Shark(*shark)
        if 82 > shark_instance.y > 78 and 11 < shark_instance.h < 14:
            objects.append(shark_instance)
            count_shark += 1
    if count_shark == 0:
        for shark in find_objects(obs, objects_colors["shark"], closing_dist=1, minx=30, maxx=126, miny=75, maxy=96):
            shark_instance = Shark(*shark)
            objects.append(shark_instance)

    for fish in find_objects(obs, objects_colors["fish"], closing_dist=8):
        fish_instance = Fish(*fish)
        if 90 < fish_instance.y < 190:
            objects.append(fish_instance)

    for p1_fish_hook in find_objects(obs, objects_colors["player 1 fishing string"], closing_dist=1):
        p1_fish_hook = PlayerOneFishingString(*p1_fish_hook)
        if p1_fish_hook.y < 80 and p1_fish_hook.x > 25:
            p1_fish_hook.hook_position = p1_fish_hook.x + p1_fish_hook.w, \
                                         p1_fish_hook.y + p1_fish_hook.wh[1]
            objects.append(p1_fish_hook)

    for p2_fishing_pole in find_objects(obs, objects_colors["player 2 fishing string"], miny=75, minx=30, maxx=130,
                                        maxy=188, closing_dist=1):
        p2_fish_hook = PlayerTwoFishingString(*p2_fishing_pole)
        if 80 > p2_fish_hook.y > 75:
            p2_fish_hook.hook_position = p2_fish_hook.x + p2_fish_hook.w, \
                                                    p2_fish_hook.y + p2_fish_hook.wh[1]
            objects.append(p2_fish_hook)

    if hud:
        for score in find_objects(obs, objects_colors["score"], closing_dist=1):
            if score[1] < 20:
                if score[0] < 80:
                    objects.append(ScorePlayerOne(*score))
                else:
                    objects.append(ScorePlayerTwo(*score))
