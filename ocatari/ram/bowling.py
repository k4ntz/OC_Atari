from ._helper_methods import _convert_number
from .game_objects import GameObject

"""
RAM extraction for the game BOWLING. Supported modes: raw, revised.

"""


class Player(GameObject):
    def __init__(self):
        self._xy = 18, 169
        self.wh = 10, 10
        self.rgb = 0, 0, 0
        self.hud = False


class Ball(GameObject):
    def __init__(self):
        self._xy = 22, 139
        self.wh = 4, 10
        self.rgb = 45, 50, 184
        self.hud = False


class Pin(GameObject):
    def __init__(self):
        self.visible = False
        self._xy = None, None
        self.wh = 2, 3
        self.rgb = 45, 50, 184
        self.hud = False


class PlayerScore(GameObject):
    def __init__(self):
        self._xy = 32, 19
        self.rgb = 84, 92, 214
        self.wh = 28, 15
        self.hud = True

    def __eq__(self, o):
        return isinstance(o, PlayerScore) and self.xy == o.xy


class PlayerRound(GameObject):
    def __init__(self):
        self._xy = 40, 7
        self.rgb = 45, 50, 184
        self.wh = 4, 10
        self.hud = True


class Player2Round(GameObject):
    def __init__(self):
        self._xy = 120, 7
        self.rgb = 45, 50, 184
        self.wh = 4, 10
        self.hud = True


def _init_objects_bowling_ram(hud=False):
    """
    (Re)Initialize the objects
    """
    objects = [Player(), Ball(), Pin(), Pin(), Pin(), Pin(), Pin(), Pin(), Pin(), Pin(), Pin(), Pin()]
    if hud:
        objects.extend([PlayerScore(), PlayerRound(), Player2Round()])
    return objects


def _detect_objects_bowling_revised(objects, ram_state, hud=False):
    """
    For all 3 objects:
    (x, y, w, h, r, g, b)
    """

    # set default coord if object does not exist
    player, ball, pin1, pin2, pin3, pin4, pin5, pin6, pin7, pin8, pin9, pin10 = objects[:12]

    # not a perfect shape around the ball because the ram y-value and the rendered image y-position are
    # in no correlation and the ram position encodes the lowest position of the ball and not the middle of the ball
    # thus a rectangle will not perfectly fit the ball
    ball.xy = ram_state[30] + 7, 161 - 2 * (ram_state[41] - 1)
    player.xy = ram_state[29] + 8, 161 - 2 * (ram_state[40] - 1)

    pins = [pin1, pin2, pin3, pin4, pin5, pin6, pin7, pin8, pin9, pin10]
    for i in range(10):
        if ram_state[57 + i] == 255:
            print("hier")
            pins[i].visible = False
        else:
            pins[i].visible = True
        pins[i].xy = pin_location(ram_state[57 + i]) + 9, 170 - 2 * (ram_state[47 + i])

    if hud:
        # round is wider if its not round 1 or its 10
        if _convert_number(ram_state[36]) == 10:
            objects[13].wh = 20, 10
        elif _convert_number(ram_state[36]) != 1:
            objects[13].wh = 12, 10

    print(objects)

    # info["score"] = _convert_number(ram_state[33])
    # info["round"] = _convert_number(ram_state[36])
    # info["pins_standing_count"] = pins_standing_count(ram_state[57:66])
    # info["throw_of_that_round"] = ram_state[18]
    # info["objects"] = objects


def _detect_objects_bowling_raw(info, ram_state):
    relevant_objects = []
    player = [ram_state[29], ram_state[40]]   # player_x, player_y  y: from 1 (down) to 28 (up)
    ball = [ram_state[30], ram_state[41]]  # ball_x, ball_y
    # for the ten pins the x-position from 57:67 and the y-position from 47:57
    pins = [ram_state[47:67]]
    relevant_objects = player + ball + pins
    info["relevant_objects"] = relevant_objects
    info["score"] = _convert_number(ram_state[33])
    info["pins_standing_count"] = pins_standing_count(ram_state[57:66])
    info["round"] = _convert_number(ram_state[36])  # displayed as hexadecimal, up to ten
    info["throw_of_that_round"] = ram_state[18]  # 0: first throw; 1: second throw
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
