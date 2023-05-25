from .game_objects import GameObject
import sys

MAX_NB_OBJECTS = {"Player1FishingString": 1, "Player2FishingString": 1, "Fish": 50, "Shark": 1}
MAX_NB_OBJECTS_HUD = {"Player1FishingString": 1, "Player2FishingString": 1, "Fish": 50, "Shark": 1, "ScoreP1": 1,
                      "ScoreP2": 1}


class Fish(GameObject):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.rgb = 232, 232, 74
        self.hooked: bool = False


class Shark(GameObject):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.rgb = 232, 232, 74
        self.is_going_right_to_left = True  # is the shark going from left to right
        self.previous_pos = 0


class PlayerOneFishString(GameObject):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.rgb = 232, 232, 74
        self.xy = 0, 0
        self.wh = 0, 0
        self.hooking: bool = False
        self.hook_position = 0, 0


class ScorePlayerTwo(GameObject):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.rgb = 167, 26, 26
        self.value = 0


class PlayerTwoFishingString(GameObject):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.rgb = 0, 0, 0
        self.xy = 0, 0
        self.wh = 0, 0
        self.hooking: bool = False
        self.hook_position = 0, 0


class ScorePlayerOne(GameObject):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.rgb = 167, 26, 26
        self.value = 0


def _get_max_objects(hud=False):
    return


def _init_objects_fishingDerby_ram(hud=False):
    objects = [PlayerOneFishString(), PlayerTwoFishingString(), Fish(), Fish(), Fish(), Fish(), Fish(), Fish(), Shark(),
               ScorePlayerOne(), ScorePlayerTwo()]
    return objects


def _detect_objects_fishingDerby_revised(objects, ram_state, hud=False):

    #Ram state of the fishing poles
    p1h, p2h = objects[0:2]
    p1h.xy = ram_state[32] - 1, p1h.xy[1]
    p2h.xy = ram_state[33] - 1, p2h.xy[1]

    # Considering that the first fish is the one at the top layer and
    fishes_hooked = []
    if ram_state[112] != 0:
        fishes_hooked.append(5 - ram_state[112])
    if ram_state[113] != 0:
        fishes_hooked.append(5 - ram_state[113])
    for i in range(6):
        if i in [fishes_hooked]:
            objects[2 + i].hooked = True
        if not objects[6 - i].hooked:
            objects[2 + i].xy = ram_state[74 - i], 97 + 16 * i
        else:
            objects[2 + i].xy = ram_state[74 - i], objects[2 + i].xy[1] - 6.8


    objects[8].previous_pos = objects[8].xy[0]
    objects[8].xy = ram_state[75], 79
    objects[8].is_right_to_left = objects[8].xy[0] - objects[8].previous_pos > 0
    objects[9].value = ram_state[61]
    objects[9].value = ram_state[62]


def _detect_objects_fishingDerby_raw(info, ram_state):
    return
