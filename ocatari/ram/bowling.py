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


def _augment_info_bowling_revised(info, ram_state):
    """
    For all 3 objects:
    (x, y, w, h, r, g, b)
     """
    objects = {}
    objects["player"] = ram_state[29] + 8, y_pos_for_vision(ram_state[40]), 10, 10, 0, 0, 0
    # not a perfect shape around the ball because the ram y-value and the rendered image y-position are
    # in no correlation and the ram position encodes the lowest position of the ball and not the middle of the ball
    # thus a rectangle will not perfectly fit the ball
    objects["ball"] = ram_state[30] + 7, y_pos_for_vision(ram_state[41]), 4, 12, 45, 50, 184
    if ram_state[57] <= 120:    # else pin knocked down
        objects["pin1"] = pin_location(ram_state[57]) + 9, y_pos_for_vision(ram_state[47]), 2, 3, 45, 50, 184
    if ram_state[58] <= 120:    # else pin knocked down
        objects["pin2"] = pin_location(ram_state[58]) + 9, y_pos_for_vision(ram_state[48]), 2, 3, 45, 50, 184
    if ram_state[59] <= 120:    # else pin knocked down
        objects["pin3"] = pin_location(ram_state[59]) + 9, y_pos_for_vision(ram_state[49]), 2, 3, 45, 50, 184
    if ram_state[60] <= 120:    # else pin knocked down
        objects["pin4"] = pin_location(ram_state[60]) + 9, y_pos_for_vision(ram_state[50]), 2, 3, 45, 50, 184
    if ram_state[61] <= 120:    # else pin knocked down
        objects["pin5"] = pin_location(ram_state[61]) + 9, y_pos_for_vision(ram_state[51]), 2, 3, 45, 50, 184
    if ram_state[62] <= 120:    # else pin knocked down
        objects["pin6"] = pin_location(ram_state[62]) + 9, y_pos_for_vision(ram_state[52]), 2, 3, 45, 50, 184
    if ram_state[63] <= 120:    # else pin knocked down
        objects["pin7"] = pin_location(ram_state[63]) + 9, y_pos_for_vision(ram_state[53]), 2, 3, 45, 50, 184
    if ram_state[64] <= 120:    # else pin knocked down
        objects["pin8"] = pin_location(ram_state[64]) + 9, y_pos_for_vision(ram_state[54]), 2, 3, 45, 50, 184
    if ram_state[65] <= 120:    # else pin knocked down
        objects["pin9"] = pin_location(ram_state[65]) + 9, y_pos_for_vision(ram_state[55]), 2, 3, 45, 50, 184
    if ram_state[66] <= 120:    # else pin knocked down
        objects["pin10"] = pin_location(ram_state[66]) + 9, y_pos_for_vision(ram_state[56]), 2, 3, 45, 50, 184
    info["score"] = _convert_number(ram_state[33])
    info["round"] = _convert_number(ram_state[36])
    info["pins_standing_count"] = pins_standing_count(ram_state[57:66])
    info["throw_of_that_round"] = ram_state[18]
    info["objects"] = objects


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


def y_pos_for_vision(ram_state):
    """
    Get an estimated y-position for the rendered image based on the ram value for the objects y-posiition.
    Hard coded because no correlation was found.
    """
    match ram_state:
        case 1:
            return 161
        case 2:
            return 160
        case 3:
            return 159
        case 4:
            return 158
        case 5:
            return 157
        case 6:
            return 156
        case 7:
            return 155
        case 8:
            return 153
        case 9:
            return 151
        case 10:
            return 150
        case 11:
            return 148
        case 12:
            return 144
        case 13:
            return 144
        case 14:
            return 142
        case 15:
            return 140
        case 16:
            return 138
        case 17:
            return 136
        case 18:
            return 134
        case 19:
            return 132
        case 20:
            return 130
        case 21:
            return 127
        case 22:
            return 125
        case 23:
            return 123
        case 24:
            return 122
        case 25:
            return 120
        case 26:
            return 116
        case 27:
            return 114
        case 28:
            return 112
        case 29:
            return 110
        case 30:
            return 106
        case 31:
            return 104
        case 32:
            return 102
        case 33:
            return 98
        case 34:
            return 95
        case 35:
            return 92
        case 36:
            return 88
        case 37:
            return 85
        case 38:
            return 83
        case 39:
            return 82
        case 40:
            return 80
        case _:
            raise IndexError("Not a valid y-position")
