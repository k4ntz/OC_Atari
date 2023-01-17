from ._helper_methods import _convert_number


def _augment_info_mspacman_raw(info, ram_state):
    """
    returns unprocessed list with
    player_x, player_y, ghosts_position_x, enemy_position_y, fruit_x, fruit_y
    """
    objects = {}
    objects["player_x"] = ram_state[10]
    objects["player_y"] = ram_state[16]
    objects["enemy_amount"] = ram_state[19]
    objects["ghosts_position_x"] = {"orange": ram_state[6],
                                    "cyan": ram_state[7],
                                    "pink": ram_state[8],
                                    "red": ram_state[9]
                                    }
    objects["enemy_position_y"] = {"orange": ram_state[12],
                                   "cyan": ram_state[13],
                                   "pink": ram_state[14],
                                   "red": ram_state[15]
                                   }
    objects["fruit_x"] = ram_state[11]
    objects["fruit_y"] = ram_state[17]
    info["object-list"] = objects


def _augment_info_mspacman_revised(info, ram_state):

    """
    There is a total of 4 levels.
    If no more lives are displayed you will lose the game upon the next hit.

    All Objects should have the following values
    (x, y, w, h, r, g, b)
    """
    objects = {}

    info["level"] = ram_state[0]  # there is a total of 4 levels 0-3
    info["score"] = (_convert_number(ram_state[122]) * 10000) + (_convert_number(ram_state[121]) * 100)
    + _convert_number(ram_state[120])

    info["lives"] = ram_state[123]  # If this state is 0 the game will be over upon the next hit

    objects["player"] = ram_state[10], ram_state[16], 9, 10, 210, 164, 74

    info["enemy_amount"] = ram_state[19]
    objects["orange_ghost_position"] = ram_state[6], ram_state[12], 9, 10, 180, 122, 48
    objects["cyan_ghost_position"] = ram_state[7], ram_state[13], 9, 10, 84, 184, 153
    objects["pink_ghost_position"] = ram_state[8], ram_state[14], 9, 10, 198, 89, 179
    objects["red_ghost_position"] = ram_state[9], ram_state[15], 9, 10, 200, 72, 72

    info["enemy_eatable"] = {"orange": ram_state[1] > 139,
                             "cyan": ram_state[2] > 124,
                             "pink": ram_state[3] > 140,
                             "red": ram_state[4] > 130
                             }

    objects["fruit_position"] = ram_state[11], ram_state[17], 184, 50, 50
    info["fruit_in_play"] = not (ram_state[11] == 0 and ram_state[17] == 0)

    info["fruit_type"] = get_fruit_type(ram_state[123])

    info["pac-dots_collected"] = ram_state[119]

    info["objects"] = objects


def get_fruit_type(ram_state):

    """
    every value of 112 and above will result in a glitched fruit
    """

    if ram_state < 16:
        return "cherry"
    elif ram_state < 32:
        return "strawberry"
    elif ram_state < 48:
        return "orange"
    elif ram_state < 64:
        return "pretzel"
    elif ram_state < 80:
        return "apple"
    elif ram_state < 96:
        return "pear"
    elif ram_state < 112:
        return "banana"
