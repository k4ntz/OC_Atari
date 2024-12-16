import sys
from ._helper_methods import _convert_number
from .game_objects import GameObject, NoObject

"""
RAM extraction for the game BOWLING. Supported modes: ram
"""

MAX_NB_OBJECTS = {'Player': 1, 'Ball': 1, 'Pin': 10}
MAX_NB_OBJECTS_HUD = {'Player': 1, 'Ball': 1, 'Pin': 10,
                      'PlayerScore': 1, 'PlayerRound': 1, 'Player2Round': 1}

_initial_pin_positions = [(121, 137), (125, 131), (125, 143), (129, 125), (
    129, 137), (129, 149), (133, 119), (133, 131), (133, 143), (133, 155)]


class Player(GameObject):
    """
    The player figure.
    """

    def __init__(self):
        super().__init__()
        self._xy = 0, 0
        self.wh = 8, 32
        self.rgb = 84, 92, 214
        self.hud = False


class Ball(GameObject):
    """
    The bowling ball.
    """

    def __init__(self):
        super().__init__()
        self._xy = 22, 139
        self.wh = 4, 10
        self.rgb = 45, 50, 184
        self.hud = False


class Pin(GameObject):
    """
    The pins.
    """

    def __init__(self):
        super().__init__()
        self._xy = 0, 0
        self.wh = 2, 4
        self.rgb = 45, 50, 184
        self.hud = False


class PlayerScore(GameObject):
    """
    The player's score display (HUD).
    """

    def __init__(self):
        super().__init__()
        self._xy = 32, 19
        self.rgb = 84, 92, 214
        self.wh = 28, 15
        self.hud = True

    def __eq__(self, o):
        return isinstance(o, PlayerScore) and self.xy == o.xy


class PlayerRound(GameObject):
    """
    The round display for the first player (HUD).
    """

    def __init__(self):
        super().__init__()
        self._xy = 40, 7
        self.rgb = 45, 50, 184
        self.wh = 4, 10
        self.hud = True


class Player2Round(GameObject):
    """
    The round display for the second player (HUD).
    """

    def __init__(self):
        super().__init__()
        self._xy = 120, 7
        self.rgb = 45, 50, 184
        self.wh = 4, 10
        self.hud = True


# parses MAX_NB* dicts, returns default init list of objects
def _get_max_objects(hud=False):

    def fromdict(max_obj_dict):
        objects = []
        mod = sys.modules[__name__]
        for k, v in max_obj_dict.items():
            for _ in range(0, v):
                objects.append(getattr(mod, k)())
        return objects

    if hud:
        return fromdict(MAX_NB_OBJECTS_HUD)
    return fromdict(MAX_NB_OBJECTS)


def _init_objects_ram(hud=False):
    """
    (Re)Initialize the objects
    """
    objects = [Player(), Ball()]

    for i in range(10):
        pin = Pin()
        pin.xy = _initial_pin_positions[i]
        objects.append(pin)
    if hud:
        objects.extend([PlayerScore(), PlayerRound(), Player2Round()])
    return objects


def _detect_objects_ram(objects, ram_state, hud=False):
    """
    For all objects:
    (x, y, w, h, r, g, b)
    """

    # set default coord if object does not exist
    player, ball = objects[:2]
    player.xy = ram_state[29] + 8, 139 - 2 * (ram_state[40] - 1)
    ball.xy = ram_state[30] + 7, 161 - 2 * (ram_state[41] - 1)

    for i in range(10):
        pin = objects[2 + i]
        if ram_state[57 + i] < 250:    # pin is knocked down in this case
            if not pin:
                pin = Pin()
                objects[2 + i] = pin
            pin.xy = pin_location(
                ram_state[57 + i]) + 9, 169 - 2 * (ram_state[47 + i])
        else:
            if pin:
                objects[2 + i] = NoObject()

    if hud:
        p1s, p1r, p2r = objects[12:]
        # score
        sc = _convert_number(ram_state[33])
        # ones digit is a one
        if ram_state[38] != 0:  # hundreds
            if ram_state[38] == 1:
                p1s.xy = 24, 19
                p1s.wh = 36, 15
            else:
                p1s.xy = 16, 19
                p1s.wh = 44, 15
        else:
            if sc == 1:
                p1s.xy = 56, 19
                p1s.wh = 4, 15
            elif sc < 10:
                p1s.xy = 48, 19
                p1s.wh = 12, 15
            elif sc < 20:
                p1s.xy = 40, 19
                p1s.wh = 20, 15
            else:
                p1s.xy = 32, 19
                p1s.wh = 28, 15
        # round
        if _convert_number(ram_state[36]) == 10:
            p1r.xy = 24, 7
            p1r.wh = 20, 10
        elif _convert_number(ram_state[36]) != 1:
            p1r.xy = 32, 7
            p1r.wh = 12, 10


def _detect_objects_bowling_raw(info, ram_state):
    # player_x, player_y  y: from 1 (down) to 28 (up)
    player = [ram_state[29], ram_state[40]]
    ball = [ram_state[30], ram_state[41]]  # ball_x, ball_y
    # for the ten pins the x-position from 57:67 and the y-position from 47:57
    pins = ram_state[47:67]
    relevant_objects = player + ball + pins.tolist()

    # additional info
    info["relevant_objects"] = relevant_objects
    info["score"] = ram_state[38] * 100 + _convert_number(ram_state[33])
    info["pins_standing_count"] = pins_standing_count(ram_state[57:66])
    # displayed as hexadecimal, up to ten
    info["round"] = _convert_number(ram_state[36])
    # 0: first throw; 1: second throw
    info["throw_of_that_round"] = ram_state[18]
    info["states_of_throw"] = ram_state[13]
    # 0: not throwing, player can freely move up and down
    # 1: start of throwing the ball, the player cant move up and down anymore, the character goes into a squat position
    # 2: the character swings his arm back
    # 3: the player moves forward
    # 4: the character throws the ball
    # 5: the ball rolls, the player can give the ball an upper or lower direction once
    # 6: the ball returns to the player


def pin_location(ram_state):
    """
    Method to get the x-position for each pin.
    """
    if ram_state <= 120:
        return 126 - 2 * ram_state
    else:
        return 255


def pins_standing_count(ram_state):
    """
    Calculate the number of pins that are still standing
    """
    count = 10
    for x in ram_state:
        if x == 255:
            count = count - 1
    return count
