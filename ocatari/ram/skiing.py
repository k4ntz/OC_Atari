import sys
from typing import Tuple
from ._helper_methods import _convert_number
from .game_objects import GameObject, ValueObject, NoObject
import numpy as np
"""
RAM extraction for the game Skiing.
"""

MAX_NB_OBJECTS = {'Player': 1, 'Tree': 6, 'Mogul': 3, 'Flag': 4}
MAX_NB_OBJECTS_HUD = {'Player': 1, 'Tree': 6,
                      'Mogul': 3, 'Flag': 4, 'Score': 1, 'Clock': 1}


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

for i in range(255):
    if i not in TREE_COLOR:
        TREE_COLOR[i] = (0, 0, 0)
    if i not in FLAG_COLOR:
        FLAG_COLOR[i] = (0, 0, 0)


class Player(GameObject):
    """
    The player figure i.e., the skier.
    """

    def __init__(self):
        super().__init__()
        self._xy = 0, 0
        self.wh = 10, 18
        self.rgb = 214, 92, 92
        self.hud = False
        self.orientation = 8

    @property
    def _nsrepr(self):
        return [self.x, self.y, self.orientation]

    @property
    def _ns_meaning(self):
        return ["POSITION", "ORIENTATION"]

    @property
    def _ns_types(self):
        return [Tuple[int, int], Tuple[int]]


class Flag(GameObject):
    """
    The poles (depicted as flags) of the gates.

    :ivar xy: Both positional coordinates x and y in a tuple.
    :type: (int, int)

    """

    def __init__(self, x=0, y=0, subtype=0):
        super().__init__()
        self.rgb = FLAG_COLOR[subtype]
        self._subtype = subtype
        self._ram_id = 2
        if subtype == 0:
            self._xy = x+1, y+4
        else:
            self._xy = x+10, y+4
        self.wh = 5, min(177-self._xy[1], 14, self._xy[1]-22)
        self._highest = False  # highest in the slot

    @property
    def xy(self):
        return self._xy

    @xy.setter
    def xy(self, xy):
        x, y = xy
        self._xy = x, y+4

    def __eq__(self, o):
        return isinstance(o, Flag) and abs(self._xy[1] - o._xy[1]) < 5


class Mogul(GameObject):
    """
    The moguls on the piste.

    :ivar xy: Both positional coordinates x and y in a tuple.
    :type: (int, int)

    """

    def __init__(self, x=0, y=0, subtype=None):
        super().__init__()
        self.rgb = (214, 214, 214)
        self._ram_id = 5
        self._xy = x+2, y+3
        self.wh = 16, min(176-y, 7, y-23)
        self._highest = False  # highest in the slot

    @property
    def xy(self):
        return self._xy

    @xy.setter
    def xy(self, xy):
        x, y = xy
        self._xy = x+2, y+3

    def __eq__(self, o):
        return isinstance(o, Mogul) and abs(self._xy[1] - o._xy[1]) < 5


class Tree(GameObject):
    """
    The trees on the piste.

    :ivar xy: Both positional coordinates x and y in a tuple.
    :type: (int, int)

    """

    def __init__(self, x=0, y=0, subtype=2):
        super().__init__()
        self.rgb = TREE_COLOR[subtype]
        self._subtype = subtype
        self._ram_id = 85
        self._xy = x-3, y+4
        self.wh = min(155-x, 16), min(175-y, 30)
        self._highest = False  # highest in the slot
        if x > 154: # pacman like torus
            self._x = 8
            self.w = min(164-x, 16)
        elif x > 145:
            self.w = min(155-x, 30)

    def __eq__(self, o):
        return isinstance(o, Tree) and o._subtype == self._subtype \
            and abs(self._xy[1] - o._xy[1]) < 7

    @property
    def xy(self):
        return self._xy

    @xy.setter
    def xy(self, xy):
        x, y = xy
        if self._xy[0] == x+2:    # bug correction
            x += 5
        self._x = x
        if x > 158: # pacman like torus
            self._x = 8
        self.y = y+4


class Clock(ValueObject):
    """
    The timer display (HUD).
    """

    def __init__(self, x=0, y=0, w=0, h=0):
        super().__init__()
        self._xy = x, y
        self.wh = w, h
        self.rgb = 0, 0, 0
        self.hud = True


class Score(ValueObject):
    """
    The counter display. This can either be the remaining number of gates (slalom mode)
    or remaining meters (downhill racing) (HUD).
    """

    def __init__(self, ten=False):
        super().__init__()
        self._xy = 67, 6
        self.wh = 14, 7
        self.ten = ten
        self.rgb = 0, 0, 0
        self.hud = True


TYPE_TO_OBJ = {2: Flag, 5: Mogul, 85: Tree}
TREE_N = 0


def _init_objects_ram(hud=False):
    """
    (Re)Initialize the objects
    """
    objects = [Player()] + [NoObject()] * 13
    if hud:
        objects.extend([Score(ten=True),
                        Clock(59, 16, 38, 7)])
    return objects


def _get_highest_idx(slot_list):
    if all(not obj for obj in slot_list):
        return -1
    for i, obj in enumerate(slot_list):
        if obj and obj._highest:
            return i
    raise ValueError("No highest object in slot")


MINIMAL_HEIGHT = {
    2: 16,
    5: 24,
    85: -1
}


# import numpy as np
def _detect_objects_ram(objects, ram_state, hud=False):
    player = objects[0]
    player.xy = (ram_state[25], ram_state[26]-80)
    player.orientation = ram_state[15]
    print(player.orientation)
    tree_slots = objects[1:7]
    mogul_slots = objects[7:10]
    flag_slots = objects[10:14]
    tree_n, mogul_n, flag_n = _get_highest_idx(tree_slots), \
        _get_highest_idx(mogul_slots), _get_highest_idx(flag_slots)
    for i in range(8):
        type = ram_state[70+i]
        subtype = ram_state[78+i]
        x, y = ram_state[62+i], 178-ram_state[86+i]
        height = ram_state[54+i]
        if y > 177 or y < 0 or height == 255:
            continue
        if type == 85:  # Tree
            tree = tree_slots[tree_n]
            if tree_n == -1:  # no tree in any slot
                if height != 0:
                    objects[1] = Tree(x, y, subtype)
                    objects[1]._highest = True
                    tree_n = 0
            elif not tree:  # tree slot is empty
                if height != 0:
                    objects[1+tree_n] = Tree(x, y, subtype)
            tree.xy = x, y
            if x > 154: # pacman like torus
                tree.x = 8
                tree.w = min(164-x, 16)
            elif x > 145:
                tree.w = min(155-x, 30)
            tree.h = min(175-y, height)
            if height == 0 and tree:
                objects[1+tree_n] = NoObject()  # tree disappeared
                next_tree = tree_slots[(tree_n+1) % 6]
                if next_tree:
                    next_tree._highest = True
            tree_n = (tree_n+1) % 6
        elif type == 5:  # Mogul
            if height == 0 and objects[7+mogul_n]: # mogul disappeared
                objects[7+mogul_n] = NoObject()
                next_mogul = mogul_slots[(mogul_n+1) % 3]
                if next_mogul:
                    next_mogul._highest = True
            else:
                if mogul_n == -1:  # no mogul in any slot
                    objects[7] = Mogul(x, y)
                    objects[7]._highest = True
                    mogul_n = 0
                elif not mogul_slots[mogul_n]:  # mogul slot is empty
                    objects[7+mogul_n] = Mogul(x, y)
                    if mogul_n == -1:
                        objects[7]._highest = True
                else:  # update mogul slot
                    mogul = mogul_slots[mogul_n]
                    mogul.xy = x, y
                    mogul.h = min(176-y, height)
                mogul_n = (mogul_n+1) % 3
        elif type == 2:  # Flag
            if height == 0 and objects[10+flag_n]:
                objects[10+flag_n] = NoObject()
                objects[11+flag_n] = NoObject()
                next_flag = flag_slots[(flag_n+2) % 4]
                if next_flag:
                    next_flag._highest = True
            else:
                if flag_n == -1:  # no flag in any slot
                    objects[10] = Flag(x, y, subtype)
                    objects[11] = Flag(x+32, y, subtype)
                    objects[10]._highest = True
                    flag_n = 0
                elif not flag_slots[flag_n]:  # flag slot is empty
                    objects[10+flag_n] = Flag(x, y, subtype)
                    objects[11+flag_n] = Flag(x+32, y, subtype)
                    if flag_n == -1:
                        objects[10]._highest = True
                else:  # update flag slot
                    offset = 3 * (subtype == 4)
                    flag1 = flag_slots[flag_n]
                    flag2 = flag_slots[flag_n+1]
                    flag1.h = min(177-y, height)
                    flag2.h = min(177-y, height)
                    flag1.xy = x+1+offset, y
                    flag2.xy = x+1+offset+32, y
                flag_n = (flag_n+2) % 4


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
    # info["object_colour"] = ram_state[78:86]  # 85 is the newest object, 78 is the oldest  |probably not important


def _time_skiing(ram_state):
    time = {}
    # minutes
    time["minutes"] = _convert_number(ram_state[104])
    # seconds
    time["seconds"] = _convert_number(ram_state[105])
    # milliseconds
    time["milli_seconds"] = _convert_number(ram_state[106])
    return time


def _get_object_state(reference_list, objects):
    return
    temp_ref_list = reference_list.copy()
    state = reference_list.copy()
    for o in objects:  # populate out_vector with object instance
        # at position of first category occurance
        idx = temp_ref_list.index(o.category)
        flat = [item for sublist in o.h_coords for item in sublist]
        state[idx] = flat  # write the slice
        temp_ref_list[idx] = ""  # remove reference from reference list
        if o.category == "Player":
            state.append([o.orientation, o.orientation,
                         o.orientation, o.orientation])
    for i, d in enumerate(temp_ref_list):
        if d != "":  # fill not populated category instances wiht 0.0's
            state[i] = [0.0, 0.0, 0.0, 0.0]
            if d == "Player":
                state.append([0.0, 0.0, 0.0, 0.0])
    return np.asarray(state)
