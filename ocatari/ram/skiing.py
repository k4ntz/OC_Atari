from ._helper_methods import _convert_number
import matplotlib.pyplot as plt

TYPE_TO_COLOR = {
    2: (10, 10, 255),
    5: (214, 214, 214),
    85: (30, 250, 30)
}
SUBTYPE_TO_COLOR = {
    2: (110, 156, 66),
    3: (82, 126, 45),
    6: (158, 208, 101),
    7: (72, 160, 72),
}

PREV_X, PREV_Y = 0, 0


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


def _augment_info_skiing_revised(info, ram_state, hud=False):
    if hud:
        objects = {
            "logo": (65, 187, 31, 6, 0, 0, 0),
            "score1": (67, 6, 6, 7, 0, 0, 0),
            "score2": (75, 6, 6, 7, 0, 0, 0),
            "clock1": (59, 16, 6, 7, 0, 0, 0),
            "clock2": (66, 17, 1, 5, 0, 0, 0),
            "clock3": (68, 16, 6, 7, 0, 0, 0),
            "clock4": (75, 16, 6, 7, 0, 0, 0),
            "clock5": (82, 21, 1, 2, 0, 0, 0),
            "clock6": (84, 16, 6, 7, 0, 0, 0),
            "clock7": (91, 16, 6, 7, 0, 0, 0),
        }
    else:
        objects = {}
    objects["player"] = (ram_state[25], ram_state[26]-80, 10, 18, 214, 92, 92)
    info["score"] = _convert_number(ram_state[107])
    if info["score"] < 10:
        objects["score1"] = (0, 0, 0, 0, 0, 0, 0)
    # print()
    # info["speed"] = ram_state[14] or ram[20] both seem to have very similar behavior
    info["time"] = _time_skiing(ram_state)
    flag_count, tree_count, mogul_count = 0, 0, 0
    for i in range(8):
        height = 75 - ram_state[90+i]
        subtype = ram_state[78+i]
        x, y = ram_state[62+i], 178-ram_state[86+i]
        if y > 177 or y < 25:
            continue
        if x == 155:
            continue
        type = ram_state[70+i]
        color = TYPE_TO_COLOR[type]
        if x > 152:
            if type == 85:  # tree
                w = min(163-x, 16)
                h = min(175-y, 30)
                if w < 5 and h < 20:
                    continue
                color = SUBTYPE_TO_COLOR[subtype]
                objects[f"tree_{tree_count}"] = (8, y+3, w, h, *color)
                tree_count += 1
                continue
        if type == 2:  # flag
            if y == 176 or y < 26:
                continue
            w = min(152-x, 5)
            h = min(175-y, 14, y-15)
            if y == 28 or y == 27:
                h = height - 15
            if h < 1:
                continue
            objects[f"flag_{flag_count}"] = (x+1, y+4, w, h, *color)
            objects[f"flag_{flag_count+1}"] = (x+33, y+4, w, h, *color)
            flag_count += 2
        elif type == 85:  # tree
            color = SUBTYPE_TO_COLOR[subtype]
            w = min(155-x, 16)
            h = min(175-y, 30)
            global PREV_X, PREV_Y
            if tree_count == 0 and PREV_X == x + 5 and abs(PREV_Y-y) <= 1: # bug correction
                # print("CORRECTING BUG")
                x += 5
                PREV_X, PREV_Y = x, y
            elif tree_count == 0:
                PREV_X, PREV_Y = x, y
            if y == 28 or y == 27:
                if height > 0:
                    objects[f"tree_{tree_count}"] = (x-3, y+4, w, height, *color)
                    tree_count += 1
                continue
            if y < 27:
                continue
            if x < 11:
                objects[f"tree_{tree_count}"] = (8, y+4, w, h, *color)
                tree_count += 1
                continue
            objects[f"tree_{tree_count}"] = (x-3, y+4, w, h, *color)
            tree_count += 1
            continue
        elif type == 5:
            h = min(176-y, 7, y-23)
            color = (192, 192, 192)
            objects[f"mogul_{mogul_count}"] = (x+2, y+3, 16, h, *color)
            mogul_count += 1
        else:
            pass
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
