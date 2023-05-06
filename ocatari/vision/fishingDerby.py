from .utils import find_objects
from .game_objects import GameObject

objects_colors = {"shark": [0, 0, 0], "fish": [232, 232, 74],
                  "player 1 fish hook": [232, 232, 74],
                  "score": [167, 26, 26], "player 2 fishing pole": [0, 0, 0],
                  }


class Shark(GameObject):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.rgb = 0, 0, 0


class Fish(GameObject):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.rgb = 232, 232, 74


class PlayerOneFishHook(GameObject):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.rgb = 232, 232, 74


class ScorePlayerTwo(GameObject):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.rgb = 167, 26, 26


class PlayerTwoFishingPole(GameObject):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.rgb = 0, 0, 0


class ScorePlayerOne:
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.rgb = 167, 26, 26


def isInThePlayingZone(object: GameObject):
    if object.y < 50 or object.x < 5 or object.x > 152:
        return False
    return True


def _detect_objects_fishingDerby(objects, obs, hud=True):
    objects.clear()

    for shark in find_objects(obs, objects_colors["shark"], closing_dist=1):
        shark_instance = Shark(*shark)
        if isInThePlayingZone(shark_instance) and shark_instance.wh[1] < 20 and shark_instance.wh[1] > 5 and shark_instance.y > 50:
            objects.append(Shark(*shark))

    for fish in find_objects(obs, objects_colors["fish"], closing_dist=6):
        fish_instance = Fish(*fish)
        if isInThePlayingZone(fish_instance) and fish_instance.y > 90 and fish_instance.y < 190:
            objects.append(fish_instance)

    for p1_fish_hook in find_objects(obs, objects_colors["player 1 fish hook"], closing_dist=1):
        p1_fish_hook_instance = PlayerOneFishHook(*p1_fish_hook)
        if isInThePlayingZone(p1_fish_hook_instance) and p1_fish_hook_instance.y < 80 and p1_fish_hook_instance.x > 25:
            objects.append(p1_fish_hook_instance)

    notp2FishingPole = [[90, 80], [70, 130], [90, 77], [80, 77]]
    for p2_fishing_pole in find_objects(obs, objects_colors["player 2 fishing pole"]):
        player_two_fishing_pole = PlayerTwoFishingPole(*p2_fishing_pole)
        if isInThePlayingZone(player_two_fishing_pole) and player_two_fishing_pole.y > 75 and player_two_fishing_pole.x > 80:
            fishing_pole = True
            for coordinates in notp2FishingPole:
                if player_two_fishing_pole.x == coordinates[0] and player_two_fishing_pole.y == coordinates[1]:
                    fishing_pole = False
                    break

            if fishing_pole:
                objects.append(player_two_fishing_pole)

    if hud:
        for score in find_objects(obs, objects_colors["player 2 fishing pole"]):
            if score[0] < 80:
                objects.append(ScorePlayerOne(*score))
            else:
                objects.append(ScorePlayerTwo(*score))
