from .game_objects import GameObject, ValueObject, NoObject
from ._helper_methods import _convert_number
import sys

MAX_NB_OBJECTS = {"Player": 1, "Truck": 3, "Flag": 3, "Collectable": 3}
MAX_NB_OBJECTS_HUD = {"Player": 1, "Truck": 3, "Flag": 3, "Collectable": 3, "HUD_Flag": 8, "Score": 1, "Life": 1}  # 'Score': 1}


class Player(GameObject):
    def __init__(self):
        super(Player, self).__init__()
        self._xy = 76, 100
        self.wh = (16, 16)
        self.rgb = 192, 192, 192
        self.hud = False


class Truck(GameObject):
    def __init__(self):
        super(Truck, self).__init__()
        self._xy = 76, 100
        self.wh = (16, 16)
        self.rgb = 213, 130, 74
        self.hud = False


class Flag(GameObject):
    def __init__(self):
        super(Flag, self).__init__()
        self._xy = 76, 100
        self.wh = (7, 16)
        self.rgb = 214, 92, 92
        self.hud = False


class Collectable(GameObject):
    def __init__(self):
        super(Collectable, self).__init__()
        self._xy = 76, 100
        self.wh = (7, 16)
        self.rgb = 214, 92, 92
        self.hud = False


class HUD_Flag(GameObject):
    def __init__(self, x=57, y=7, rgb=(210, 164, 74)):
        super(HUD_Flag, self).__init__()
        self._xy = x, y
        self.wh = (5, 12)
        self.rgb = rgb
        self.hud = True


class Score(ValueObject):
    def __init__(self):
        super(Score, self).__init__()
        self._xy = 57, 6
        self.wh = (5, 7)
        self.rgb = 168, 48, 143
        self.hud = True
        self.value = 0


class Life(ValueObject):
    def __init__(self):
        super(Life, self).__init__()
        self._xy = 16, 196
        self.wh = (4, 8)
        self.rgb = 198, 108, 58
        self.hud = True
        self.value = 3


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
    objects = []

    objects.extend([NoObject()] * 10)
    if hud:
        objects.extend([NoObject()] * 8)
        objects.extend([Score(), Life()])
    return objects


def _detect_objects_ram(objects, ram_state, hud=False):
    """
    For all 3 objects:
    (x, y, w, h, r, g, b)
    """

    # type == r36-r39; x, y == r40-r43, r56-r59
    if ram_state[36] == 16:
        if type(objects[0]) is NoObject:
            objects[0] = Player()
        objects[0].xy = ram_state[40], ram_state[56] + 16
    else:
        objects[0] = NoObject()

    for i in range(3):
        x, y = ram_state[41+i], ram_state[57+i] + 16
        if ram_state[37+i] == 23:
            objects[1+i] = NoObject()
            objects[4+i] = NoObject()
            objects[7+i] = NoObject()
        elif ram_state[37+i] < 8:
            objects[4+i] = NoObject()
            objects[7+i] = NoObject()
            w, h = 16, 16
            if type(objects[1+i]) is NoObject:
                objects[1+i] = Truck()
            truck = objects[1+i]
            # truck colors and offsets
            if ram_state[37+i] == 0:
                truck.rgb = 213, 130, 74
            elif ram_state[37+i] == 1:
                truck.rgb = 214, 92, 92
                x += 2
                w -= 2
            elif ram_state[37+i] == 2:
                truck.rgb = 92, 186, 92
                y += 1
                h -= 1
            elif ram_state[37+i] == 3:
                truck.rgb = 84, 160, 197
            elif ram_state[37+i] == 4:
                truck.rgb = 164, 89, 208
            elif ram_state[37+i] == 5:
                truck.rgb = 127, 92, 213
                w -= 2
            elif ram_state[37+i] == 6:
                truck.rgb = 84, 92, 214
                y += 2
                h -= 2
            elif ram_state[37+i] == 7:
                truck.rgb = 84, 138, 210
            truck.xy = x, y
            truck.wh = w, h
        elif ram_state[37+i] < 16 or 23 < ram_state[37+i] < 31:
            objects[1+i] = NoObject()
            # is flag or collectable; they have the same colors
            if ram_state[37+i] < 16:
                if type(objects[4+i]) is NoObject:
                    objects[4+i] = Flag()
                col = objects[4+i]
                objects[7+i] = NoObject()
            else:
                if type(objects[7+i]) is NoObject:
                    objects[7+i] = Collectable()
                col = objects[7+i]
                objects[4+i] = NoObject()
            if ram_state[37+i] % 16 == 8:
                col.rgb = 104, 72, 198
            elif ram_state[37+i] % 16 == 9:
                col.rgb = 162, 162, 42
            elif ram_state[37+i] % 16 == 10:
                col.rgb = 146, 70, 192
            elif ram_state[37+i] % 16 == 11:
                col.rgb = 184, 70, 162
            elif ram_state[37+i] % 16 == 12:
                col.rgb = 200, 72, 72
            elif ram_state[37+i] % 16 == 13:
                col.rgb = 139, 108, 58
            elif ram_state[37+i] % 16 == 14:
                col.rgb = 180, 122, 48
            elif ram_state[37+i] % 16 == 15:
                col.rgb = 66, 72, 200
            col.xy = x, y - 1
        else:
            objects[1+i] = NoObject()
            objects[4+i] = NoObject()
            objects[7+i] = NoObject()

    if hud:
        if not ram_state[4] & 1:
            if type(objects[10]) is NoObject:
                objects[10] = HUD_Flag(91, 14, (78, 50, 181))
        else:
            objects[10] = NoObject()

        if not ram_state[4] & 2:
            if type(objects[11]) is NoObject:
                objects[11] = HUD_Flag(19, 14, (134, 134, 29))
        else:
            objects[11] = NoObject()

        if not ram_state[4] & 4:
            if type(objects[12]) is NoObject:
                objects[12] = HUD_Flag(107, 14, (125, 48, 173))
        else:
            objects[12] = NoObject()

        if not ram_state[4] & 8:
            if type(objects[13]) is NoObject:
                objects[13] = HUD_Flag(127, 14, (168, 48, 143))
        else:
            objects[13] = NoObject()

        if not ram_state[4] & 16:
            if type(objects[14]) is NoObject:
                objects[14] = HUD_Flag(71, 14, (184, 50, 50))
        else:
            objects[14] = NoObject()

        if not ram_state[4] & 32:
            if type(objects[15]) is NoObject:
                objects[15] = HUD_Flag(55, 14, (181, 83, 40))
        else:
            objects[15] = NoObject()

        if not ram_state[4] & 64:
            if type(objects[16]) is NoObject:
                objects[16] = HUD_Flag(35, 14, (162, 98, 33))
        else:
            objects[16] = NoObject()

        if not ram_state[4] & 128:
            if type(objects[17]) is NoObject:
                objects[17] = HUD_Flag(143, 14, (45, 50, 184))
        else:
            objects[17] = NoObject()

        # Score
        x, w = 57, 5
        if ram_state[0] > 16:
            x, w = 17, 45
        elif ram_state[0]:
            x, w = 25, 37
        elif ram_state[1] > 16:
            x, w = 33, 29
        elif ram_state[1]:
            x, w = 41, 21
        elif ram_state[2]:
            x, w = 49, 13

        objects[18].xywh = x, 6, w, 7
        objects[18].value = _convert_number(ram_state[0]) * 10000 + _convert_number(ram_state[1]) * 100 + _convert_number(ram_state[2])
        
        # Lives r6
        objects[19].wh = 4 + (8 * ((ram_state[6] % 5) - 1)), 8
        objects[19].value = ram_state[6] % 5
