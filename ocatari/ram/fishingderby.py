from .game_objects import GameObject, NoObject

"""
RAM extraction for the game Fishing Derby.
"""

MAX_NB_OBJECTS = {"PlayerOneHook": 1,
                  "PlayerTwoHook": 1, "Fish": 6, "Shark": 1}
MAX_NB_OBJECTS_HUD = {"PlayerOneHook": 1, "PlayerTwoHook": 1, "Fish": 6, "Shark": 1, "ScorePlayerOne": 1,
                      "ScorePlayerTwo": 1}


class Fish(GameObject):
    """
    The fish.

    :ivar hooked: Wether the fish is currently hooked
    :type: bool
    """

    def __init__(self):
        super().__init__()
        self.rgb = 232, 232, 74
        self.xy = 0, 0
        self.wh = 8, 10
        self.hooked: bool = False


class Shark(GameObject):
    """
    The shark.
    """

    def __init__(self):
        super().__init__()
        self.rgb = 232, 232, 74
        self.xy = 0, 0
        self.wh = 35, 13
        self.is_going_left_to_right = True  # is the shark going from left to right
        self.previous_pos = 0


class PlayerOneHook(GameObject):
    """
    The hook of player one.
    """

    # ram_state[15] gives what input was played by player 1
    def __init__(self):
        super().__init__()
        self.rgb = 232, 232, 74
        self.xy = 0, 37
        self.wh = 0, 0
        self.hooking: bool = False
        self.hook_position = 0, 0


class ScorePlayerOne(GameObject):
    """
    The score display of player one (HUD).
    """

    def __init__(self):
        super().__init__()
        self.rgb = 167, 26, 26
        self.xy = 49, 8
        self.wh = 6, 8
        self.value = 0


class PlayerTwoHook(GameObject):
    """
    The hook of player two.
    """

    # to deactivate player two -> turn ram_state[0] to 1
    def __init__(self):
        super().__init__()
        self.rgb = 0, 0, 0
        self.xy = 0, 37
        self.wh = 0, 0
        self.hooking: bool = False
        self.hook_position = 0, 0


class ScorePlayerTwo(GameObject):
    """
    The score display of player two (HUD).
    """

    def __init__(self):
        super().__init__()
        self.rgb = 167, 26, 26
        self.xy = 113, 8
        self.wh = 6, 8
        self.value = 0


def _get_max_objects(hud=False):
    return


def _init_objects_ram(hud=False):
    objects = [PlayerOneHook(), PlayerTwoHook(), Fish(), Fish(), Fish(),
               Fish(), Fish(), Fish(), Shark()]
    if hud:
        objects += [ScorePlayerOne(), ScorePlayerTwo()]
    return objects


def _detect_objects_ram(objects, ram_state, hud=False):
    # Ram state of the fishing poles
    p1s, p2s = objects[0:2]
    coeff_1 = 1
    coeff_2 = 1

    if ram_state[30] == 16:
        # orientation of the rope till the hook (right or left)
        coeff_1 = -coeff_1

    if ram_state[31] == 16:
        coeff_2 = -coeff_2

    p1s.xy = -2 + ram_state[23] + coeff_1 * ram_state[34] + \
        int(coeff_1 > 0) * 3, int(ram_state[65] * 2.3) + 78
    p2s.xy = 2 + ram_state[24] + coeff_2 * ram_state[35] + \
        int(coeff_2 > 0) * 3, int(ram_state[66] * 2.3) + 78
    p1s.hook_position = -2 + \
        ram_state[23] + coeff_1 * ram_state[34], int(ram_state[65] * 2.3) + 81
    p2s.hook_position = 2 + ram_state[24] + coeff_2 * \
        ram_state[35], int(ram_state[66] * 2.3) + 81

    p1s.wh = 3, 3
    p2s.wh = 3, 3

    # Considering that the first fish is the one at the top layer and
    fishes_hooked = []
    if ram_state[112] != 0:
        fishes_hooked.append(6 - ram_state[112])
    if ram_state[113] != 0:
        fishes_hooked.append(6 - ram_state[113])

    for i in range(6):
        if i in fishes_hooked:
            objects[2 + i].hooked = True
        else:
            objects[2 + i].hooked = False
        if not objects[2 + i].hooked:
            objects[2 + i].xy = ram_state[74 - i], int(97 + 16 * i)
        else:
            if 6 - ram_state[112] == i:
                # it means the fish was caught by the player 1 thus its position is
                # the position of p1's hook + half the height of a fish
                objects[2 + i].xy = ram_state[74 - i], p1s.hook_position[1] - 4
            else:
                objects[2 + i].xy = ram_state[74 - i], p2s.hook_position[1] - 4

    # shark
    if ram_state[103] == 80:
        objects[8] = NoObject()
    else:
        if type(objects[8]) is NoObject:
            objects[8] = Shark()
        objects[8].previous_pos = objects[8].xy[0]
        objects[8].xy = ram_state[75], 80
        objects[8].is_right_to_left = objects[8].xy[0] - \
            objects[8].previous_pos > 0
    if hud:
        objects[9].value = ram_state[61]
        objects[9].value = ram_state[62]


def _detect_objects_fishingderby_raw(info, ram_state):
    return
