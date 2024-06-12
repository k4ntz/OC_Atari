from .game_objects import GameObject
from .utils import find_objects, find_rope_segments

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


def _detect_objects(objects, obs, hud=True):
    objects.clear()
    modified_obs = obs.copy()

    for shark in find_objects(obs, objects_colors["shark"], closing_dist=1, minx=28, maxx=131, miny=80, maxy=93):
        shark_instance = Shark(*shark)
        if shark_instance.w > 20:
            objects.append(shark_instance)
            modified_obs[shark_instance.y: shark_instance.y - 1+ shark_instance.h + 2, shark_instance.x - 1: shark_instance.x + shark_instance.w + 2] = (24, 26, 167)


    p1_fishing_hook = find_rope_segments(obs, objects_colors["player 1 fishing string"], seg_height=(7, 150),
                                         minx=30, maxx=79, maxy=188, miny=90)
    if p1_fishing_hook:
        for pixels in p1_fishing_hook:
            modified_obs[pixels[1] - 1:pixels[1] + pixels[3] + 1, pixels[0] - 1:pixels[0] + 1] = (24, 26, 167)
        lowest = max(p1_fishing_hook, key=lambda x: x[1])
        if lowest[3] > 1:
            lowest[1] = lowest[1] + lowest[3] - 1
            lowest[3] = 1
        objects.append(PlayerOneHook(*lowest))

    else:
        p1_fishing_hook = find_rope_segments(obs, objects_colors["player 1 fishing string"], seg_height=(1, 150),
                                             minx=30, maxx=79, maxy=95)
        if p1_fishing_hook:
            for pixels in p1_fishing_hook:
                modified_obs[pixels[1] - 1:pixels[1] + pixels[3] + 1, pixels[0] - 1:pixels[0] + 1] = (24, 26, 167)
            lowest = max(p1_fishing_hook, key=lambda x: x[1])
            if lowest[3] > 1:
                lowest[1] = lowest[1] + lowest[3] - 1
                lowest[3] = 1
            objects.append(PlayerOneHook(*lowest))

    p1_fishing_hook = find_rope_segments(obs, objects_colors["player 1 fishing string"], seg_height=(1, 150),
                                         minx=30, maxx=79, maxy=94)
    for pixels in p1_fishing_hook:
        obs[pixels[1] - 1:pixels[1] + pixels[3] + 1, pixels[0] - 1:pixels[0] + 1] = (24, 26, 167)

    p2_fishing_hook = find_rope_segments(modified_obs, objects_colors["player 2 fishing string"], seg_height=(1, 150),
                                         minx=79, maxx=130, maxy=188, miny=43)
    if p2_fishing_hook:
        lowest = max(p2_fishing_hook, key=lambda x: x[1])
        if lowest[3] > 1:
            lowest[1] = lowest[1] + lowest[3] - 1
            lowest[3] = 1
        objects.append(PlayerTwoHook(*lowest))

    for fish in find_objects(modified_obs, objects_colors["fish"], closing_dist=7, maxy=190):
        fish_instance = Fish(*fish)
        if 5 < fish_instance.h and fish_instance.w > 5:
            objects.append(fish_instance)

            # if np.shape(find_objects(obs, objects_colors["player 1 fishing string"], minx=x + w - 3, maxx=x + w,
            #                          miny=y + h - 3, maxy=y + h))[0] != 0:
            #     p1_hook = PlayerOneHook(x=x + w - 2, y=y + h - 2, w=4, h=4)
            #     p1_hook.hook_position = x + w, y + h
            #     objects.append(p1_hook)
            # else:
            #     p1_hook = PlayerOneHook(x=x - 2, y=y + h - 2, w=4, h=4)
            #     p1_hook.hook_position = x, y + h
            #     objects.append(p1_hook)

    # for p2_fish_hook in find_objects(obs, objects_colors["player 2 fishing string"], miny=75, minx=30, maxx=130,
    #                                  maxy=188, closing_dist=1):
    #     x, y, w, h = p2_fish_hook
    #     if 80 > y:
    #         if len(find_objects(obs, objects_colors["player 2 fishing string"], minx=x + w - 3, maxx=min(x + w, 131),
    #                             miny=y + h - 3, maxy=y + h)) != 0:
    #             objects.append(PlayerTwoHook(x=x + w - 2, y=y + h - 2, w=4, h=4))
    #         else:
    #             objects.append(PlayerTwoHook(x=x - 2, y=y + h - 2, w=4, h=4))

    if hud:
        for score in find_objects(obs, objects_colors["score"], closing_dist=1):
            if score[1] < 20:
                if score[0] < 80:
                    objects.append(ScorePlayerOne(*score))
                else:
                    objects.append(ScorePlayerTwo(*score))
    print(objects)
