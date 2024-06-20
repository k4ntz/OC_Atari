import sys
from ._helper_methods import _convert_number
from .game_objects import GameObject
import numpy as np
"""
RAM extraction for the game Skiing.
"""

MAX_NB_OBJECTS =  {'Player': 1, 'Tree': 4, 'Mogul': 3, 'Flag': 4}
MAX_NB_OBJECTS_HUD =  {'Player': 1, 'Tree': 4, 'Mogul': 3, 'Flag': 4, 'Score': 2, 'Clock': 8}


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
        if self._xy[0] == x + 2:    # bug correction
            x += 5
        self._prev_xy = self._xy
        if x > 158:
            self._xy = 8, y+4
            self.wh = min(164-x, 16), min(175-y, 30)
        else:
            self._xy = x-3, y+4
        self.wh = self.wh[0], min(175-y, 30)


class Clock(GameObject):
    """
    The timer display (HUD).
    """
    
    def __init__(self, x=0, y=0, w=0, h=0):
        super().__init__()
        self._xy = x, y
        self.wh = w, h
        self.rgb = 0, 0, 0
        self.hud = True


class Score(GameObject):
    """
    The counter display. This can either be the remaining number of gates (slalom mode) 
    or remaining meters (downhill racing) (HUD).
    """
    
    def __init__(self, ten=False):
        super().__init__()
        if ten:
            self._xy = 67, 6
        else:
            self._xy = 75, 6
        self.ten = ten
        self.rgb = 0, 0, 0
        self.wh = 6, 7
        self.hud = True


TYPE_TO_OBJ = {2: Flag, 5: Mogul, 85: Tree}

# parses MAX_NB* dicts, returns default init list of objects
def _get_max_objects(hud=False):

    def fromdict(max_obj_dict):
        objects = []
        mod = sys.modules[__name__]
        for k, v in max_obj_dict.items():
            for _ in range(0, v):
                objects.append(getattr(mod, k)())    
        return objects

    if hud:
        return fromdict(MAX_NB_OBJECTS_HUD)
    return fromdict(MAX_NB_OBJECTS)

def _init_objects_ram(hud=False):
    """
    (Re)Initialize the objects
    """
    objects = [Player()]
    if hud:
        objects.extend([Score(), Score(ten=True),
                        Clock(59, 16, 6, 7), Clock(66, 17, 1, 2),
                        Clock(66, 20, 1, 2),
                        Clock(68, 16, 6, 7), Clock(75, 16, 6, 7),
                        Clock(82, 21, 1, 2), Clock(84, 16, 6, 7),
                        Clock(91, 16, 6, 7)])
    return objects


# import numpy as np
def _detect_objects_ram(objects, ram_state, hud=False):
    player = objects[0]
    player.xy = (ram_state[25], ram_state[26]-80)
    player.orientation = ram_state[15]
    offset = 1 if not hud else 11
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

def _get_object_state_size(hud):
    objects = _get_max_objects(hud)
    additional_feature = ["orientation"]
    return len(objects)+len(additional_feature)

def _get_object_state(reference_list, objects):

    #import ipdb; ipdb.set_trace()
    temp_ref_list = reference_list.copy()
    state = reference_list.copy()
    for o in objects: # populate out_vector with object instance
        idx = temp_ref_list.index(o.category) #at position of first category occurance
        flat = [item for sublist in o.h_coords for item in sublist]
        state[idx] = flat #write the slice
        temp_ref_list[idx] = "" #remove reference from reference list
        if o.category is "Player":
            state.append([o.orientation, o.orientation, o.orientation, o.orientation])    
    for i, d in enumerate(temp_ref_list):
        if d != "": #fill not populated category instances wiht 0.0's
            state[i] = [0.0, 0.0, 0.0, 0.0]
            if d == "Player":
                state.append([0.0,0.0,0.0,0.0])
    return np.asarray(state)
    
    