from .game_objects import GameObject, NoObject
from .utils import match_objects
from ._helper_methods import _convert_number
import sys
import math


"""
RAM extraction for the game Enduro.
"""

MAX_NB_OBJECTS = {"Player": 1, "Car": 7}
MAX_NB_OBJECTS_HUD = {"Player": 1, "Car": 7,
                      "NumberOfCars": 1, "CoveredDistance": 1, "Level": 1}


class Player(GameObject):

    def __init__(self):
        super().__init__()
        self._xy = 0, 0
        self.wh = (16, 11)
        self.rgb = 192, 192, 192
        self.hud = False


class Car(GameObject):
    def __init__(self, x=0, y=0, w=16, h=10):
        super().__init__()
        self._xy = x, y
        self.wh = w, h
        self.rgb = 192, 192, 192
        self.hud = False


class CoveredDistance(GameObject):
    def __init__(self):
        super().__init__()
        self._xy = 0, 0
        self.wh = (16, 10)
        self.rgb = 255, 255, 255
        self.distance = 0
        self.hud = True


class NumberOfCars(GameObject):
    def __init__(self):
        super().__init__()
        self._xy = 0, 0
        self.wh = (16, 10)
        self.rgb = 255, 255, 255
        self.num = 200
        self.hud = True


class Level(GameObject):
    def __init__(self):
        super().__init__()
        self._xy = 0, 0
        self.wh = (16, 10)
        self.rgb = 255, 255, 255
        self.level = 1
        self.hud = True


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
    objects = [Player()] + [NoObject()]*7
    if hud:
        objects.extend(
            [NumberOfCars()] + [CoveredDistance()] + [Level()]
        )
    return objects

def get_road_edges(lc, lr, rc, rr, y, td):
    ldx = math.sqrt(lr**2 - (y - lc[1])**2)
    if td >= 0:
        lx = lc[0] - ldx
    else:
        lx = lc[0] + ldx
    
    rdx = math.sqrt(rr**2 - (y - rc[1])**2)
    if td > 0:
        rx = rc[0] - rdx
    else:
        rx = rc[0] + rdx
    
    return lx, rx

def find_center(a, b, r, right_turn):
    m = (a[0] + b[0]) / 2, (a[1] + b[1]) / 2
    d = math.sqrt((a[0] - b[0]) ** 2 + (a[1] - b[1]) ** 2)
    h = math.sqrt(r ** 2 - (d / 2) ** 2)

    s = (a[1] - b[1]) / (math.copysign(max(1, abs(a[0] - b[0])), a[0] - b[0]))

    dy = math.sqrt(h**2 / (1 + s**2))
    dx = 0 - math.sqrt((s*h)**2 / (1 + s**2))
    if right_turn:
        c = round(m[0] - dx), round(m[1] + dy)
    else:
        c = round(m[0] + dx), round(m[1] + dy)
    
    return c

def _detect_objects_ram(objects, ram_state, hud=False):
    """
    For all 3 objects:
    (x, y, w, h, r, g, b)
    """
    # 106 ram_state is somewhat controlling the y of the player when it's dying by sinking
    # ram 54 was the previous x position migh be important for turns

    x = 77
    if ram_state[46] & 128:
        _x = 255 - ram_state[46]
        x = 77 + round(_x * 17 / 26)
    else:
        _x = ram_state[46]
        x = 77 - round(_x * 13 / 25)
    objects[0].xy = x, 89 + ram_state[52]

    
    # ppd: player perspective drift
    if ram_state[46] & 128:
        ppd = round((x - 77) * 27 / 17)
    else:
        ppd = round((x - 77) * 32 / 17)
    
    # td: turns drift
    if ram_state[34] & 128:
        td = 0 - (255 - ram_state[34])
    else:
        td = ram_state[34]
    
    # end point: 87 + td - ppd, 51
    # left start point: 37 - ppd, 154
    # right start point: 138 - ppd, 154

    # finding the roads edge curves, assuming they are parts of two circles
    if td == 0:
        rr = 4500
        lr = 4500
    else:
        rr = abs(min(96 / td, 225 / td)) * 50
        lr = abs(max(96 / td, 225 / td)) * 50
    lc = find_center((87 + td - ppd, 51), (37 - ppd, 154), lr, td >= 0)
    rc = find_center((87 + td - ppd, 51), (138 - ppd, 154), rr, td > 0)
    
    xs = []
    ys = []
    for i in range(7):
        if ram_state[27+i]:
            y = 150 - int(1.2*((18-i)*i) + ((ram_state[59] >> 3)*(0.9**i)))
            ys.append(y)
            xs.append(ram_state[27+i])
    
    ys = sorted(ys, reverse=True)
    _xs = [20, 80, 130]
    cars_bb = []
    for i in range(len(xs)):
        lx, rx = get_road_edges(lc, lr, rc, rr, ys[i], td)
        w = 16 * (ys[i] - 50) / 103 + 1
        h = 10 * (ys[i] - 50) / 103 + 1
        if xs[i]%32 == 22:
            x = lx + (rx - lx) * 0.25
        elif xs[i]%32 == 23:
            x = lx + (rx - lx) * 0.75
        else:
            x = lx + (rx - lx) * 0.5
        cars_bb.append((round(x - w / 2), ys[i], round(w), round(h)))
    
    match_objects(objects, cars_bb, 1, 7, Car)

    if hud:
        num_of_cars = NumberOfCars()
        num_of_cars.num = _convert_number(ram_state[44]) * 100 + \
            _convert_number(ram_state[43])
        if num_of_cars.num == 200:
            num_of_cars.xy = 81, 180
            num_of_cars.wh = 22, 7
        elif num_of_cars.num >= 100:
            num_of_cars.xy = 82, 180
            num_of_cars.wh = 21, 7
        elif num_of_cars.num >= 20:
            num_of_cars.xy = 89, 180
            num_of_cars.wh = 14, 7
        elif num_of_cars.num >= 10:
            num_of_cars.xy = 90, 180
            num_of_cars.wh = 13, 7
        elif num_of_cars.num >= 2:
            num_of_cars.xy = 97, 180
            num_of_cars.wh = 6, 7
        elif num_of_cars.num == 1:
            num_of_cars.xy = 98, 180
            num_of_cars.wh = 4, 7
        elif num_of_cars.num == 0:
            num_of_cars.xy = 73, 180
            num_of_cars.wh = 31, 8
        objects[8] = num_of_cars

        cd = CoveredDistance()
        cd.distance = _convert_number(ram_state[42]) * 10000
        cd.distance += _convert_number(ram_state[41]) * 100
        cd.distance += _convert_number(ram_state[40])
        if cd.distance >= 200000:
            cd.xy = 57, 165
            cd.wh = 46, 7
        elif cd.distance >= 100000:
            cd.xy = 58, 165
            cd.wh = 45, 7
        else:
            cd.xy = 65, 165
            cd.wh = 38, 7
        objects[9] = cd
        
        level = Level()
        level.level = ram_state[45]
        if level.level == 1:
            level.xy = 58, 180
            level.wh = 4, 7
        else:
            level.xy = 57, 180
            level.wh = 6, 7
        objects[10] = level
