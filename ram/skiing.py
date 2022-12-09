def _augment_info_skiing_raw(info, ram_state):
    # player starts at x = 76
    info["player_x"] = ram_state[25]  # can go up to 150 (170 and you are back to the left side)
    info["player_y"] = ram_state[26]  # constant 120
    info["score"] = _convert_number(ram_state[107])
    # info["speed"] = ram_state[14] or ram[20] both seem to have very similar behavior
    info["time"] = _time_skiing(ram_state)
    info["object_x"] = ram_state[62:69]  # 69 is the newest object, 62 is the oldest
    info["object_y"] = ram_state[86:93]  # 93 is the newest object, 86 is the oldest
    info["object_type"] = ram_state[70:77]  # 77 is the newest object, 70 is the oldest | 85 tree | 2 flag | 5 mogul
    info["object_colour"] = ram_state[78:85]  # 85 is the newest object, 78 is the oldest  |probably not important
    print(ram_state)


def _augment_info_skiing_revised(info, ram_state):
    pass


def _time_skiing(ram_state):
    time = {}
    # minutes
    time["minutes"] = _convert_number(ram_state[104])
    # seconds
    time["seconds"] = _convert_number(ram_state[105])
    # milliseconds
    time["milli_seconds"] = _convert_number(ram_state[106])
    return time


def _convert_number(number):
    """
    The game SKIING displays the time/score in hexadecimal numbers, while the ram extraction displays it as an integer.
    This results in a required conversion from the extracted ram number (in dec) to a hex number, which we then display
    as a dec number.

    e.g.: game shows 10 seconds, but the ram display saves it as 16
    """
    number_str = str(hex(number))
    number_list = [*number_str]
    number_str = ""
    count = 0
    for x in number_list:
        if count > 1:
            number_str += x
        count += 1
    return int(number_str)
