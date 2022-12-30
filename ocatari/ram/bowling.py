from ._helper_methods import _convert_number

"""
RAM extraction for the game BOWLING. Supported modes: raw, revised.

"""


def _augment_info_bowling_raw(info, ram_state):
    info["player_x"] = ram_state[29]
    info["player_y"] = ram_state[40]  # from 1 (down) to 28 (up)
    info["ball_x"] = ram_state[30]  # 138 right
    info["ball_y"] = ram_state[41]
    info["pin_1"] = pin_location(ram_state[57]), ram_state[47]  # first pin; x = 255 if pin knocked down
    info["pin_2"] = pin_location(ram_state[58]), ram_state[48]  # upper pin second column
    info["pin_3"] = pin_location(ram_state[59]), ram_state[49]
    info["pin_4"] = pin_location(ram_state[60]), ram_state[50]  # upper pin third column
    info["pin_5"] = pin_location(ram_state[61]), ram_state[51]
    info["pin_6"] = pin_location(ram_state[62]), ram_state[52]
    info["pin_7"] = pin_location(ram_state[63]), ram_state[53]  # upper pin fourth column
    info["pin_8"] = pin_location(ram_state[64]), ram_state[54]
    info["pin_9"] = pin_location(ram_state[65]), ram_state[55]
    info["pin_10"] = pin_location(ram_state[66]), ram_state[56]
    info["score"] = _convert_number(ram_state[33])  # displayed as hexadecimal
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
    print(ram_state)


def _augment_info_bowling_revised(info, ram_state):
    """
        For all 3 objects:
        (x, y, w, h, r, g, b)
        """
    objects = {}
    info["player"] = ram_state[29] + 10, 170 - ram_state[40], 4, 15, 0, 0, 0
    info["ball"] = ram_state[30] + 7, 151 - ram_state[41], 4, 10, 45, 50, 184
    if ram_state[57] != 255:    # else pin knocked down
        objects["pin1"] = 1, 1, 1, 1, 45, 50, 184
    # objects["ball"] =

    info["score"] = _convert_number(ram_state[33])
    info["round"] = _convert_number(ram_state[36])
    info["pins_standing_count"] = pins_standing_count(ram_state[57:66])
    info["throw_of_that_round"] = ram_state[18]
    info["objects"] = objects


def pin_location(ram_state):
    """
    Method to get the x-position for each pin.
    """
    if ram_state != 255:
        return 126 - 2 * ram_state
    else:
        return 255


def pins_standing_count(ram_state):
    count = 10
    for x in ram_state:
        if x == 255:
            count = count - 1
    return count
