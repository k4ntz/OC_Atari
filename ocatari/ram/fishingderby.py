from .game_objects import GameObject
import sys

MAX_NB_OBJECTS = {"Player1FishingHook":1 , "Player2FishingHook":1, "Fish": 50, "Shark":1}
MAX_NB_OBJECTS_HUD = {"Player1FishingHook":1 , "Player2FishingHook":1, "Fish": 50, "Shark":1, "ScoreP1":1, "ScoreP2":1}


class Fish(GameObject):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.rgb = 232, 232, 74


class PlayerOneFishHook(GameObject):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.rgb = 232, 232, 74
        self.xy = 0, 0


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


def _get_max_objects(hud=False):
    return


def _init_objects_fishingDerby_ram(hud=False):
    objects = [PlayerOneFishHook(), PlayerTwoFishingHook()]
    return objects


def _detect_objects_fishingDerby_revised(objects, ram_state, hud=False):
    p1h, p2h = objects[0:2]
    p1h.xy = ram_state[32] - 1, p1h.xy[1]
    p2h.xy = ram_state[33] - 1, p2h.xy[1]


def _detect_objects_fishingDerby_raw(info, ram_state):
    return
