from ._helper_methods import _convert_number
from .game_objects import GameObject
from termcolor import colored

import matplotlib.pyplot as plt     # noqa
OBS = None


def print_state(state):
    print("-"*10)
    for el in state:
        x, y, type = el
        coord = el[0:2]
        attr = []
        if y > 177 or y < 25 or x == 155:
            attr.append("dark")
        if type == 2:
            print(colored(coord, "blue", attrs=attr))
        elif type == 5:
            print(colored(coord, "grey", attrs=attr))
        elif type == 85:
            print(colored(coord, "green", attrs=attr))
        else:
            print(colored("Error in print_state", "red"))
            exit(1)
    print("-"*10)


TREE_COLOR = {
    2: (110, 156, 66),
    3: (82, 126, 45),
    6: (158, 208, 101),
    7: (72, 160, 72),
}

FLAG_COLOR = {
    0: (10, 10, 255),
    4: (184, 50, 50)
}

MINIMAL_HEIGHT = {
    2: 16,
    5: 24,
    85: -1
}

PREV_RAM_STATE = 0


class Player(GameObject):
    def __init__(self):
        self._xy = 0, 0
        self.wh = 10, 18
        self.rgb = 214, 92, 92
        self.hud = False


class Flag(GameObject):
    def __init__(self, x, y, subtype):
        self.rgb = FLAG_COLOR[subtype]
        self._subtype = subtype
        self._ram_id = 2
        if subtype == 0:
            self._xy = x+1, y+4
        else:
            self._xy = x+4, y+4
        self.wh = 5, min(177-self._xy[1], 14, self._xy[1]-22)

    @property
    def xy(self):
        return self._xy

    @xy.setter
    def xy(self, xy):
        x, y = xy
        self._prev_xy = self._xy
        self._xy = self._prev_xy[0], y+4
        self.wh = 5, min(177-y, 14)

    def __eq__(self, o):
        return isinstance(o, Flag) and abs(self._xy[0] - o._xy[0]) < 5


class Mogul(GameObject):
    def __init__(self, x, y, subtype=None):
        self.rgb = (214, 214, 214)
        self._ram_id = 5
        self._xy = x+2, y+3
        self.wh = 16, min(176-y, 7, y-23)

    @property
    def xy(self):
        return self._xy

    @xy.setter
    def xy(self, xy):
        x, y = xy
        self._prev_xy = self._xy
        self._xy = x+2, y+3
        self.wh = 16, min(176-y, 7, y-23)

    def __eq__(self, o):
        return isinstance(o, Mogul) and abs(self._xy[0] - o._xy[0]) < 5


class Tree(GameObject):
    def __init__(self, x, y, subtype):
        self.rgb = TREE_COLOR[subtype]
        self._subtype = subtype
        self._ram_id = 85
        if x > 158:
            self._xy = 8, y+4
            self.wh = min(164-x, 16), min(175-y, 30)
        else:
            self._xy = x-3, y+4
            self.wh = min(155-x, 16), min(175-y, 30)

    def __eq__(self, o):
        return isinstance(o, Tree) and o._subtype == self._subtype \
            and abs(self._xy[0] - o._xy[0]) < 7

    @property
    def xy(self):
        return self._xy

    @xy.setter
    def xy(self, xy):
        x, y = xy
        if self._xy[0] == x + 2:  # bug correction
            x += 5
        self._prev_xy = self._xy
        if x > 158:
            self._xy = 8, y+4
            self.wh = min(164-x, 16), min(175-y, 30)
        else:
            self._xy = x-3, y+4
        # if abs(self._prev_xy[0] - self._xy[0]) > 10:
        #     import ipdb; ipdb.set_trace()
        self.wh = self.wh[0], min(175-y, 30)


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


TYPE_TO_OBJ = {2: Flag, 5: Mogul, 85: Tree}


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


# import numpy as np
def _detect_objects_skiing_revised(objects, ram_state, hud=False):
    player = objects[0]
    player.xy = (ram_state[25], ram_state[26]-80)
    # info["speed"] = ram_state[14] or ram[20] both seem to have very similar behavior
    # info["time"] = _time_skiing(ram_state)
    offset = 1 if not hud else 11
    # xs = ram_state[62:70]
    # ys = 178-ram_state[86:94]
    # types = ram_state[70:78]
    # state = np.array([xs, ys, types]).T
    # print_state(state)
    for i in range(8):
        height = 75 - ram_state[90+i]
        type = ram_state[70+i]
        subtype = ram_state[78+i]
        x, y = ram_state[62+i], 178-ram_state[86+i]
        if offset < len(objects):
            currobj = objects[offset]
        else:
            currobj = None
        if y > 177 or y < 27 or (y in [27, 28] and height < MINIMAL_HEIGHT[type]):
            if currobj:
                removed_obj = TYPE_TO_OBJ[type](x, y, subtype)
                if currobj == removed_obj:  # object disappeared
                    if isinstance(objects[offset], Flag):
                        objects.pop(offset+1)
                    objects.pop(offset)
            continue
        if type == 2:  # flags
            if currobj is None:
                objects.append(Flag(x, y, subtype))
                objects.append(Flag(x+32, y, subtype))
            else:
                currobj.xy = x, y
                objects[offset+1].xy = x+32, y
                if y <= 28:
                    currobj.wh = currobj.wh[0], height-15
                    objects[offset+1].wh = objects[offset+1].wh[0], height-15
                if currobj._ram_id != 2:
                    if y == 29:  # bug fix
                        continue
                    import ipdb; ipdb.set_trace()   # noqa
            offset += 1
        elif type == 5:     # mogul
            if currobj is None:
                objects.append(Mogul(x, y))
            else:
                if currobj._ram_id != 5:
                    continue
                currobj.xy = x, y
                if y <= 28:
                    currobj.wh = currobj.wh[0], height-23
        elif type == 85:  # tree
            if currobj is None:
                if not y == 28 or y == 27:
                    objects.append(Tree(x, y, subtype))
            else:
                currobj.xy = x, y
                if y <= 28:
                    currobj.wh = currobj.wh[0], height+2
        offset += 1
    # print(objects)


def _detect_objects_skiing_raw(info, ram_state):
    # player starts at x = 76
    relevant_info = ram_state[25:27] + ram_state[62:94]
    # info["player_x"] = ram_state[25]  # can go up to 150 (170 and you are back to the left side)
    # info["player_y"] = ram_state[26]  # constant 120
    info["score"] = _convert_number(ram_state[107])
    # info["speed"] = ram_state[14] or ram[20] both seem to have very similar behavior
    info["time"] = _time_skiing(ram_state)
    info["relavant_ram_info"] = relevant_info
    # info["object_x"] = ram_state[62:69]  # 69 is the newest object, 62 is the oldest
    # info["object_y"] = ram_state[86:94]  # 93 is the newest object, 86 is the oldest
    # info["object_type"] = ram_state[70:78]  # 77 is the newest object, 70 is the oldest | 85 tree | 2 flag | 5 mogul
    # info["object_colour"] = ram_state[79:86]  # 85 is the newest object, 78 is the oldest  |probably not important
    # print(ram_state)


def _time_skiing(ram_state):
    time = {}
    # minutes
    time["minutes"] = _convert_number(ram_state[104])
    # seconds
    time["seconds"] = _convert_number(ram_state[105])
    # milliseconds
    time["milli_seconds"] = _convert_number(ram_state[106])
    return time
