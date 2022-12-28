from ._helper_methods import _convert_number


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
    print(info)
    # print(ram_state)


def _augment_info_skiing_revised(info, ram_state):
    objects = {}
    objects["player"] = [(ram_state[25], ram_state[26], 214, 92, 92)]
    info["score"] = _convert_number(ram_state[107])
    # info["speed"] = ram_state[14] or ram[20] both seem to have very similar behavior
    info["time"] = _time_skiing(ram_state)
    for i in range(7):
        x, y = ram_state[62+i]//2, ram_state[86+i]//2
        objects[f"obj_{i}"] = [(x, y, 10, 10, 10)]
    # info["object_x"] = ram_state[62:69]  # 69 is the newest object, 62 is the oldest
    # info["object_y"] = ram_state[86:93]  # 93 is the newest object, 86 is the oldest
    # info["object_type"] = ram_state[70:77]  # 77 is the newest object, 70 is the oldest | 85 tree | 2 flag | 5 mogul
    # info["object_colour"] = ram_state[78:85]  # 85 is the newest object, 78 is the oldest  |probably not important
    info["objects"] = objects


def _time_skiing(ram_state):
    time = {}
    # minutes
    time["minutes"] = _convert_number(ram_state[104])
    # seconds
    time["seconds"] = _convert_number(ram_state[105])
    # milliseconds
    time["milli_seconds"] = _convert_number(ram_state[106])
    return time
