from .utils import find_objects
from .game_objects import GameObject

objects_colors = {"shark": [0, 0, 0], "fish": [232, 232, 74],
                  "player 1 fishing hook": [232, 232, 74],
                  "score": [167, 26, 26], "player 2 fishing hook": [0, 0, 0],
                  }


class Shark(GameObject):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.rgb = 0, 0, 0


class Fish(GameObject):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.rgb = 232, 232, 74


class PlayerOneFishingHook(GameObject):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.rgb = 232, 232, 74


class ScorePlayerTwo(GameObject):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.rgb = 167, 26, 26


class PlayerTwoFishingHook(GameObject):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.rgb = 0, 0, 0


class ScorePlayerOne(GameObject):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.rgb = 167, 26, 26


def _detect_objects_fishingDerby(objects, obs, hud=True):
    objects.clear()

    for shark in find_objects(obs, objects_colors["shark"], closing_dist=1, minx=28):
        shark_instance = Shark(*shark)
        if shark_instance.wh[1] < 20 and shark_instance.wh[1] > 5 and shark_instance.y > 50:
            objects.append(Shark(*shark))

    for fish in find_objects(obs, objects_colors["fish"], closing_dist=8):
        fish_instance = Fish(*fish)
        if fish_instance.y > 90 and fish_instance.y < 190:
            objects.append(fish_instance)

    for p1_fish_hook in find_objects(obs, objects_colors["player 1 fishing hook"], closing_dist=1):
        p1_fish_hook_instance = PlayerOneFishingHook(*p1_fish_hook)
        if p1_fish_hook_instance.y < 80 and p1_fish_hook_instance.x > 25:
            objects.append(p1_fish_hook_instance)

    notp2FishingPole = [[90, 80], [70, 130], [90, 77], [80, 77]]
    for p2_fishing_pole in find_objects(obs, objects_colors["player 2 fishing hook"]):
        player_two_fishing_pole = PlayerTwoFishingHook(*p2_fishing_pole)
        if player_two_fishing_pole.y > 75 and player_two_fishing_pole.x > 80:
            fishing_pole = True
            for coordinates in notp2FishingPole:
                if player_two_fishing_pole.x == coordinates[0] and player_two_fishing_pole.y == coordinates[1]:
                    fishing_pole = False
                    break

            if fishing_pole:
                objects.append(player_two_fishing_pole)

    if hud:
        for score in find_objects(obs, objects_colors["score"], closing_dist=1):
            if score[1] < 20:
                if score[0] < 80:
                    objects.append(ScorePlayerOne(*score))
                else:
                    objects.append(ScorePlayerTwo(*score))
