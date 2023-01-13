from ._helper_methods import _convert_number
import matplotlib.pyplot as plt
from .game_objects import GameObject


TREE_COLOR = {
    2: (110, 156, 66),
    3: (82, 126, 45),
    6: (158, 208, 101),
    7: (72, 160, 72),
}

PREV_RAM_STATE = 0


class Player(GameObject):
    def __init__(self):
        self._xy = 0, 0
        self.wh = 10, 18
        self.rgb = 214, 92, 92
        self.hud = False

class Flag(GameObject):
    def __init__(self, x, y):
        self.rgb = (10, 10, 255)
        self._ram_id = 2
        self._xy = x+1, y+4
        self.wh = 5, min(177-self._xy[1], 14, self._xy[1]-22)

    @property
    def xy(self):
        return self._xy

    @xy.setter
    def xy(self, xy):
        x, y = xy
        self._prev_xy = self._xy
        self._xy = x+1, y+4
        self.wh = 5, min(177-y, 14, y+4-25)

class Mogul(GameObject):
    def __init__(self, x, y):
        self.rgb = (214, 214, 214)
        self._ram_id = 5
        self._xy = x, y
        self.wh = 16, min(176-y, 7, y-23)


    @property
    def xy(self):
        return self._xy

    @xy.setter
    def xy(self, xy):
        self._prev_xy = self._xy
        self._xy = xy
        self.wh = 16, min(176-self._xy[1], 7, self._xy[1]-23)


class Tree(GameObject):
    def __init__(self, type):
        self.rgb = TREE_COLOR[type]
        self._type = type
        self._ram_id = 85

    def __eq__(self, o):
        return isinstance(o, Tree) and o._type == self._type \
            and self._xy[0] - o._xy[0] in [0, 5]

    @property
    def xy(self):
        return self._xy

    @xy.setter
    def xy(self, xy):
        if self._prev_xy[0] == self._xy + 5: # bug correction
            xy[0] += 5
        self._prev_xy = self._xy
        self._xy = xy


class Logo(GameObject):
    def __init__(self):
        self._xy = 65, 187
        self.wh = 31, 6
        self.rgb = 0, 0, 0
        self.hud = True


class Clock(GameObject):
    def __init__(self, x, y, w, h):
        self._xy = x, y
        self.wh = w, h
        self.rgb = 0, 0, 0
        self.hud = True


class Score(GameObject):
    def __init__(self, ten=False):
        if ten:
            self._xy = 67, 6
        else:
            self._xy = 75, 6
        self.ten = ten
        self.rgb = 0, 0, 0
        self.wh = 6, 7
        self.hud = True

PREV_X, PREV_Y = 0, 0


def _detect_objects_skiing_raw(info, ram_state):
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


def _init_objects_skiing_ram(hud=False):
    """
    (Re)Initialize the objects
    """
    objects = [Player()]
    if hud:
        objects.extend([Score(), Score(ten=True), Logo(),
                        Clock(59, 16, 6, 7), Clock(66, 17, 1, 5),
                        Clock(68, 16, 6, 7), Clock(75, 16, 6, 7),
                        Clock(82, 21, 1, 2), Clock(84, 16, 6, 7),
                        Clock(91, 16, 6, 7)])
    return objects

import numpy as np
def _detect_objects_skiing_revised(objects, ram_state, hud=False):
    player = objects[0]
    player.xy = (ram_state[25], ram_state[26]-80)
    # info["speed"] = ram_state[14] or ram[20] both seem to have very similar behavior
    # info["time"] = _time_skiing(ram_state)
    # flag_count, tree_count, mogul_count = 0, 0, 0
    offset = 1 if not hud else 11
    #  check if first objects disappeared
    # print(f"Len obj: {len(objects)}")
    # if len(objects) > offset:
    #     while objects[offset]._ram_id != ram_state[70]:
    #         objects.pop(offset)
    #         if len(objects) == offset:
    #             break
    # print(f"Len obj: {len(objects)}")
    print(f"objects = {objects} (b)")
    xs = ram_state[62:70]
    ys = 178-ram_state[86:94]
    types = ram_state[70:78]
    state = np.array([xs, ys, types]).T
    print(state)
    for i in range(8):
        type = ram_state[70+i]
        x, y = ram_state[62+i], 178-ram_state[86+i]
        if offset < len(objects):
            print(f"Reusing {objects[offset]}")
            currobj = objects[offset]
        else:
            if type == 2:
                print(f"NONE {x, y, offset}")
            currobj = None
        if y > 177 or y < 25 or x == 155:
            if currobj and currobj._ram_id == type:  # object disappeared
                print(f"POPPING {objects[offset]}")
                if isinstance(objects[offset], Flag):
                    objects.pop(offset+1)
                objects.pop(offset)
            continue
        if type == 2:  # flags
            # if y > 172 or y < 25:
            #     continue
            if currobj is None:
                objects.append(Flag(x, y))
                objects.append(Flag(x+32, y))
            else:
                currobj.xy = x, y
                objects[offset+1].xy = x+32, y
                if currobj._ram_id != 2:
                    return
            offset += 1
            print("Added one")
            # objects[f"flag_{flag_count}"] = (x+1, y+4, w, h, *color)
            # objects[f"flag_{flag_count+1}"] = (x+33, y+4, w, h, *color)
            # flag_count += 2
        elif type == 85:  # tree
            continue
    #         subtype = ram_state[78+i]
    #         color = TREE_COLOR[subtype]
    #         h = min(175-y, 30)
    #         if x > 152:
    #             w = min(163-x, 16)
    #             if w < 5 and h < 20:
    #                 continue
    #             objects[f"tree_{tree_count}"] = (8, y+3, w, h, *color)
    #             tree_count += 1
    #             continue
    #         w = min(155-x, 16)
    #         global PREV_X, PREV_Y
    #         if tree_count == 0 and PREV_X == x + 5 and abs(PREV_Y-y) <= 1: # bug correction
    #             # print("CORRECTING BUG")
    #             x += 5
    #             PREV_X, PREV_Y = x, y
    #         elif tree_count == 0:
    #             PREV_X, PREV_Y = x, y
    #         if y == 28 or y == 27:
    #             if height > 0:
    #                 objects[f"tree_{tree_count}"] = (x-3, y+4, w, height, *color)
    #                 tree_count += 1
    #             continue
    #         if y < 27:
    #             continue
    #         if x < 11:
    #             objects[f"tree_{tree_count}"] = (8, y+4, w, h, *color)
    #             tree_count += 1
    #             continue
    #         objects[f"tree_{tree_count}"] = (x-3, y+4, w, h, *color)
    #         tree_count += 1
    #         continue
        elif type == 5:
            if currobj is None:
                objects.append(Mogul(x+2, y+3))
                # objects[f"mogul_{mogul_count}"] = (x+2, y+3,  *color)
            else:
                if currobj._ram_id != 5:
                    print("WRONG")
                    import ipdb; ipdb.set_trace()
                currobj.xy = x+2, y+3
        offset += 1
    print(f"objects = {objects}")
    #     else:
    #         pass
    # if hud:
    #     if info["score"] < 10:
    #         objects["score1"] = (0, 0, 0, 0, 0, 0, 0)


def _detect_objects_skiing_revised_old(info, ram_state, hud=True):
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
                color = TREE_COLOR[subtype]
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
            color = TREE_COLOR[subtype]
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
