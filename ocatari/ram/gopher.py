from .game_objects import GameObject, NoObject, ValueObject
import sys

MAX_NB_OBJECTS = {"Player": 1, "Gopher": 1,
                  "Carrot": 3, "Hole": 6, 'Floor': 1, 'Bird': 1}
MAX_NB_OBJECTS_HUD = {"Player": 1, "Gopher": 1,
                      "Carrot": 3, "Hole": 6, 'Floor': 1, "Bird": 1, "Score": 1}


class Player(GameObject):
    def __init__(self):
        super().__init__()
        self._xy = 0, 0
        self.wh = (11, 50)
        self.rgb = 101, 111, 228
        self.hud = False


class Gopher(GameObject):
    def __init__(self):
        super().__init__()
        self._xy = 0, 0
        self.wh = (14, 10)
        self.rgb = 72, 44, 0
        self.hud = False


class Carrot(GameObject):
    def __init__(self):
        super().__init__()
        self._xy = 0, 0
        self.wh = (8, 27)
        self.rgb = 162, 98, 33
        self.hud = False


class Bird(GameObject):
    def __init__(self):
        super().__init__()
        self._xy = 0, 0
        self.wh = (15, 18)
        self.rgb = 45, 50, 184
        self.hud = False


class Hole(GameObject):
    def __init__(self):
        super().__init__()
        self._xy = 0, 0
        self.wh = (8, 7)
        self.rgb = 223, 183, 85
        self.hud = False


class Floor(GameObject):
    def __init__(self):
        super().__init__()
        self._xy = 0, 183
        self.wh = (150, 12)
        self.rgb = 223, 183, 85
        self.hud = False


class Score(ValueObject):
    def __init__(self):
        super().__init__()
        self._xy = 98, 10
        self.wh = (5, 9)
        self.rgb = 195, 144, 65
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
    objects = [Player()] + [Gopher()]
    objects.extend([NoObject()]*3)
    objects.extend([NoObject()]*6)  # Maximum number of expected blocks
    # Maximum number of expected blocks
    objects.extend([Floor()]*1+[NoObject()])
    if hud:
        objects.extend([Score()])
    return objects


def _detect_objects_ram(objects, ram_state, hud=False):
    """
    For all 3 objects:
    (x, y, w, h, r, g, b)
    """
    # Detecting player
    player = objects[0]
    player.xy = ram_state[31] - 10, 96

    # Detecting gopher
    gopher = objects[1]
    if ram_state[85] <= 5:
        gopher.xy = ram_state[41] - 2, 184
        gopher.wh = (14, 10)
    elif ram_state[85] == 35:
        gopher.xy = ram_state[41] - 2, 149
        gopher.wh = (14, 10)
    else:
        gopher.xy = ram_state[41] - 3, 184 - ram_state[85]
        gopher.wh = (7, 23)

    # Detecting carrots
    for i in range(0, 3):
        ram_value = pow(2, i)
        carrot = objects[2+i]
        if ram_state[52] & ram_value == ram_value:
            if carrot:
                objects[2+i] = carrot
            else:
                objects[2+i] = Carrot()
                objects[2+i].xy = (92-16*i, 151)
        else:
            if carrot:
                objects[2+i] = NoObject()

    def update_hole(ram_cond, obj_index, xy, wh=(8, 14), wh_alt=(8, 7), delobj=False):
        index = obj_index
        if ram_cond:
            if objects[index]:
                objects[index].xy = xy
                objects[index].wh = wh
            else:
                hole = Hole()
                objects[index] = hole
                hole.xy = xy
                hole.wh = wh_alt
        elif delobj:
            if objects[index]:
                objects[index] = NoObject()

    # Define the conditions and corresponding attributes for each object
    ram_conditions = [
        (ram_state[17] & 24 == 24, 10, (140, 176), (8, 7), (8, 7), True),
        (ram_state[16] % 2 == 1 and ram_state[17] %
         2 == 1, 9, (124, 176), (8, 7), (8, 7),  True),
        (ram_state[16] & 24 == 24, 8, (108, 176), (8, 7), (8, 7), True),
        (ram_state[11] & 24 == 24, 10, (140, 169), (8, 14), (8, 7)),
        (ram_state[10] % 2 == 1 and ram_state[11] %
         2 == 1, 9, (124, 169), (8, 14), (8, 7)),
        (ram_state[10] & 24 == 24, 8, (108, 169), (8, 14), (8, 7)),
        #
        ((ram_state[13] % 128) % 2 == 1 and (ram_state[14]) %
         2 == 1, 7, (44, 176), (8, 7), (8, 7), True),
        ((ram_state[13] % 127) & 24 == 24, 6,
         (28, 176), (8, 7), (8, 7),  True),
        ((ram_state[12] % 127) % 2 == 1 and (ram_state[13] & 128)
         == 128, 5, (12, 176), (8, 7), (8, 7), True),
        ((ram_state[7] % 128) % 2 == 1 and (ram_state[8]) %
         2 == 1, 7, (44, 169), (8, 14), (8, 7)),
        ((ram_state[7] % 127) & 24 == 24, 6, (28, 169), (8, 14), (8, 7)),
        ((ram_state[6] % 127) % 2 == 1 and (ram_state[7] & 128)
         == 128, 5, (12, 169), (8, 14), (8, 7)),

    ]

    for cond in ram_conditions:
        update_hole(*cond)

    ram_conditions_2 = [
        (ram_state[5] & 24 == 24, 10, (140, 161), (8, 22) if objects[10]
         and objects[10].wh[1] > 13 else (8, 15), (8, 8)),
        (ram_state[4] % 2 == 1 and ram_state[5] % 2 == 1, 9, (124, 161),
         (8, 22) if objects[9] and objects[9].wh[1] > 13 else (8, 15), (8, 8)),
        (ram_state[4] & 24 == 24, 8, (108, 161), (8, 22) if objects[8]
         and objects[8].wh[1] > 13 else (8, 15), (8, 8)),
        ((ram_state[1] % 128) % 2 == 1 and (ram_state[2]) % 2 == 1, 7, (44, 161),
         (8, 22) if objects[7] and objects[7].wh[1] > 13 else (8, 15), (8, 8)),
        ((ram_state[1] % 127) & 24 == 24, 6, (28, 161), (8, 22)
         if objects[6] and objects[6].wh[1] > 13 else (8, 15), (8, 8)),
        ((ram_state[0] % 127) % 2 == 1 and (ram_state[1] & 128) == 128, 5, (12, 161),
         (8, 22) if objects[5] and objects[5].wh[1] > 13 else (8, 15), (8, 8))
    ]

    for cond in ram_conditions_2:
        update_hole(*cond)

    if ram_state[28] < 147:
        if objects[12]:
            bird = objects[43]
        else:
            bird = Bird()
        bird.xy = ram_state[28] - 12, 30
    else:
        if objects[12]:
            objects[12] = NoObject()

    if hud:
        if ram_state[49] == 0 and ram_state[50] <= 9:
            # Right most bounding box only
            objects[13].value = ram_state[50]
        elif ram_state[49] == 0 and ram_state[50] > 9:
            # Two bounding boxes
            objects[13].xy = 90, 10
            objects[13].wh = 14, 9
            objects[13].value = ram_state[50]
        elif ram_state[49] <= 9:
            # Three bounding boxes
            objects[13].xy = 82, 10
            objects[13].wh = 22, 9
            objects[13].value = ram_state[50] + ram_state[49]*100
        elif ram_state[49] > 9:
            # Four bounding boxes
            objects[13].xy = 74, 10
            objects[13].wh = 30, 9
            objects[13].value = ram_state[50] + ram_state[49]*100
