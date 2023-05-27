from .game_objects import GameObject

MAX_NB_OBJECTS = {"Player1FishingString": 1, "Player2FishingString": 1, "Fish": 6, "Shark": 1}
MAX_NB_OBJECTS_HUD = {"Player1FishingString": 1, "Player2FishingString": 1, "Fish": 6, "Shark": 1, "ScoreP1": 1,
                      "ScoreP2": 1}


class Fish(GameObject):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.rgb = 232, 232, 74
        self.xy = 0, 0
        self.wh = 8, 8
        self.hooked: bool = False


class Shark(GameObject):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.rgb = 232, 232, 74
        self.xy = 0, 0
        self.wh = 35, 17
        self.is_going_left_to_right = True  # is the shark going from left to right
        self.previous_pos = 0


class PlayerOneFishString(GameObject):
    # ram_state[15] gives what input was played by player 1
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.rgb = 232, 232, 74
        self.xy = 0, 37
        self.wh = 0, 0
        self.hooking: bool = False
        self.hook_position = 0, 0


class ScorePlayerOne(GameObject):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.rgb = 167, 26, 26
        self.xy = 49, 8
        self.wh = 6, 8
        self.value = 0


class PlayerTwoFishingString(GameObject):
    # to deactivate player two -> turn ram_state[0] to 1
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.rgb = 0, 0, 0
        self.xy = 0, 37
        self.wh = 0, 0
        self.hooking: bool = False
        self.hook_position = 0, 0


class ScorePlayerTwo(GameObject):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.rgb = 167, 26, 26
        self.xy = 113, 8
        self.wh = 6, 8
        self.value = 0


def _get_max_objects(hud=False):
    return


def _init_objects_fishingDerby_ram(hud=False):
    if hud:
        objects = [PlayerOneFishString(), PlayerTwoFishingString(), Fish(), Fish(), Fish(), Fish(), Fish(), Fish(),
                   Shark(),
                   ScorePlayerOne(), ScorePlayerTwo()]
    else:
        objects = [PlayerOneFishString(), PlayerTwoFishingString(), Fish(), Fish(), Fish(), Fish(), Fish(), Fish(),
                   Shark()]
    return objects


def _detect_objects_fishingDerby_revised(objects, ram_state, hud=False):
    # Ram state of the fishing poles
    p1s, p2s = objects[0:2]
    coeff_1 = 1
    coeff_2 = 1
    p1s.xy = int(20 + (-14.294117647058826 + 0.23529411764705885 * ram_state[21] + 0.9411764705882354 * ram_state[23])), \
        p1s.xy[1]
    p2s.xy = int(144 - (-0.97 * ram_state[24] + 141.52)), p2s.xy[1]
    print(ram_state[30], ram_state[34])
    if ram_state[30] == 240:
        p1s.xy = p1s.xy[0] - ram_state[34], p1s.xy[1]
        coeff_1 = -coeff_1

    if ram_state[31] == 16:
        p2s.xy = p2s.xy[0] - ram_state[35], p2s.xy[1]
        coeff_2 = -coeff_2

    p1s.hook_position = \
        int(15.5 + (-14.294117647058826 + 0.23529411764705885 * ram_state[21] + 0.9411764705882354 * ram_state[
            23]) + coeff_1 * ram_state[34]), \
            int(ram_state[65] * 2.276 + 82)
    p2s.hook_position = int(144 - (-0.97 * ram_state[24] + 141.52) + coeff_2 * ram_state[35]), int(
        ram_state[66] * 2.276 + 82)

    p1s.wh = int(ram_state[34] * abs(coeff_1)), abs(p1s.xy[1] - p1s.hook_position[1])
    p2s.wh = int(ram_state[35] * abs(coeff_1)), abs(p2s.xy[1] - p2s.hook_position[1])

    # Considering that the first fish is the one at the top layer and
    fishes_hooked = []
    if ram_state[112] != 0:
        fishes_hooked.append([6 - ram_state[112]])
    if ram_state[113] != 0:
        fishes_hooked.append(6 - ram_state[113])

    for i in range(6):
        if i in fishes_hooked:
            objects[2 + i].hooked = True
        else:
            objects[2 + i].hooked = False
        if not objects[2 + i].hooked:
            objects[2 + i].xy = ram_state[74 - i], int(97 + 16.5 * i)
        else:
            if 6 - ram_state[112] == i:
                # it means the fish was caught by the player 1 thus its position is
                # the position of p1's hook + half the height of a fish
                objects[2 + i].xy = ram_state[74 - i], p1s.hook_position[1] - 4
            else:
                objects[2 + i].xy = ram_state[74 - i], p2s.hook_position[1] - 4

    objects[8].previous_pos = objects[8].xy[0]
    objects[8].xy = ram_state[75], 79
    objects[8].is_right_to_left = objects[8].xy[0] - objects[8].previous_pos > 0
    if hud:
        objects[9].value = ram_state[61]
        objects[9].value = ram_state[62]


def _detect_objects_fishingDerby_raw(info, ram_state):
    return
