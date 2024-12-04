from .game_objects import GameObject, NoObject
import sys

MAX_NB_OBJECTS = {"Player": 1, "Gopher": 1, "Carrot": 3, "Empty_block": 38}
MAX_NB_OBJECTS_HUD = {"Player": 1, "Gopher": 1, "Carrot": 3, "Empty_block": 38, "Bird": 1, "Score": 4}

full_list = [(140, 175), (12, 175), (27, 175), (45, 175), (108, 175), (124, 175),
             (140, 168), (12, 168), (27, 168), (45, 168), (108, 168), (124, 168),
             (140, 161), (12, 161), (27, 161), (45, 161), (108, 161), (124, 161)]

for i in [2, 140, 36, 12, 27, 45, 108, 124, 150]:
    full_list.append((i, 183))
for i in [22, 117, 134]:  # narrower blocks
    full_list.append((i, 183))
for i in range(55, 108, 9):
    full_list.append((i, 183))

# (150, 192), (140, 192), (27, 183)
# (12, 167), (12, 173), (28, 161)
global block_list
block_list = []
global ram_70
ram_70 = 0
global life
life = 3


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


class Empty_block(GameObject):
    def __init__(self):
        super().__init__()
        self._xy = 0, 0
        self.wh = (8, 12)
        self.rgb = 223, 183, 85
        self.hud = False


class Score(GameObject):
    def __init__(self):
        super().__init__()
        self._xy = 0, 0
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
    objects.extend([NoObject()]*38)  # Maximum number of expected blocks
    if hud:
        objects.extend([Bird(), Score(), Score(), Score(), Score()])
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
    carrot1, carrot2, carrot3 = Carrot(), Carrot(), Carrot()
    carrot1.xy = 92, 151
    carrot2.xy = 76, 151
    carrot3.xy = 60, 151
    if ram_state[36] == 0 and ram_state[37] == 0 and ram_state[38] == 3:
        objects[2:5] = carrot1, carrot2, carrot3
    elif ram_state[36] == 0 and ram_state[37] == 0 and ram_state[38] == 1:
        objects[2:5] = carrot2, carrot3, NoObject()
    elif ram_state[36] == 0 and ram_state[37] == 0 and ram_state[38] == 0:
        objects[2:5] = carrot3, NoObject(), NoObject()
    elif ram_state[36] == 128 and ram_state[37] == 32 and ram_state[38] == 1:
        objects[2:5] = carrot2, carrot1, NoObject()
    elif ram_state[36] == 127 and ram_state[37] == 16 and ram_state[38] == 0:
        objects[2:5] = carrot1, NoObject(), NoObject()
    elif ram_state[36] == 128 and ram_state[37] == 32 and ram_state[38] == 0:
        objects[2:5] = carrot2, NoObject(), NoObject()

    
    # adding top row 
    # A dictionary with ram state and corresponding box coordinates (Multiple possible as well) [ram_state[0,1,2]:[box coordinates]]
    dict_top_left_row={(128,128,0):[(12,161)],(0,24,0):[(27,161)],(0,1,1):[(45,161)],
                  (128,152,0):[(12,161),(27,161)],(0,25,1):[(27,161),(45,161)],(128,129,1):[(12,161),(45,161)],
                  (128,153,1):[(12,161),(27,161),(45,161)],(0,0,0):[]
                  }
    
    dict_top_right_row={(0,24):[(140,161)],(1,1):[(124,161)],(24,0):[(108,161)],
                        (1,25):[(124,161),(140,161)],(24,24):[(108,161),(140,161)],(25,1):[(108,161),(124,161)],
                        (25,25):[(108,161),(124,161),(140,161)],(0,0):[]
                        }
    dict_mid_left_row={(128,128,0):[(12,168)],(0,24,0):[(27,168)],(0,1,1):[(45,168)],
                  (128,152,0):[(12,168),(27,168)],(0,25,1):[(27,168),(45,168)],(128,129,1):[(12,168),(45,168)],
                  (128,153,1):[(12,168),(27,168),(45,168)],(0,0,0):[]
                  }
    dict_mid_right_row={(0,24):[(140,168)],(1,1):[(124,168)],(24,0):[(108,168)],
                        (1,25):[(124,168),(140,168)],(24,24):[(108,168),(140,168)],(25,1):[(108,168),(124,168)],
                        (25,25):[(108,168),(124,168),(140,168)],(0,0):[]
                        }
    dict_bot_left_row={(128,128,0):[(12,175)],(0,24,0):[(27,175)],(0,1,1):[(45,175)],
                  (128,152,0):[(12,175),(27,175)],(0,25,1):[(27,175),(45,175)],(128,129,1):[(12,175),(45,175)],
                  (128,153,1):[(12,175),(27,175),(45,175)],(0,0,0):[]
                  }
    dict_bot_right_row={(0,24):[(140,175)],(1,1):[(124,175)],(24,0):[(108,175)],
                        (1,25):[(124,175),(140,175)],(24,24):[(108,175),(140,175)],(25,1):[(108,175),(124,175)],
                        (25,25):[(108,175),(124,175),(140,175)],(0,0):[]
                        }
    
    # Adding blocks using ram indices
    count = 0  # variable to keep track of number of blocks being pushed
    for item in dict_top_left_row[(ram_state[0], ram_state[1], ram_state[2])]:
        b = Empty_block()
        b.xy = item
        b.wh = (8, 6)
        objects[5 + count] = b
        count += 1

    for item in dict_top_right_row[(ram_state[4], ram_state[5])]:
        b = Empty_block()
        b.xy = item
        b.wh = (8, 6)
        objects[5 + count] = b
        count += 1

    # Adding middle row
    for item in dict_mid_left_row[(ram_state[6], ram_state[7], ram_state[8])]:
        b = Empty_block()
        b.xy = item
        b.wh = (8, 6)
        objects[5 + count] = b
        count += 1

    for item in dict_mid_right_row[(ram_state[10], ram_state[11])]:
        b = Empty_block()
        b.xy = item
        b.wh = (8, 6)
        objects[5 + count] = b
        count += 1

    # Adding bottom row
    for item in dict_bot_left_row[(ram_state[12], ram_state[13], ram_state[14])]:
        b = Empty_block()
        b.xy = item
        b.wh = (8, 6)
        objects[5 + count] = b
        count += 1

    for item in dict_bot_right_row[(ram_state[16], ram_state[17])]:
        b = Empty_block()
        b.xy = item
        b.wh = (8, 6)
        objects[5 + count] = b
        count += 1

    if hud:
        # Score hundreds and thousands depend on ram_state[49] and score ones and tens depend on ram_state[50]
        bound1, bound2, bound3, bound4 = Score(), Score(), Score(), Score()
        bound1.xy = 75, 10
        bound2.xy = 82, 10
        bound3.xy = 90, 10
        bound4.xy = 98, 10
        if ram_state[49] == 0 and ram_state[50] <= 9:
            # Right most bounding box only
            objects[44] = bound4
            objects[45:48] = [NoObject()] * 3
        elif ram_state[49] == 0 and ram_state[50] > 9:
            # Two bounding boxes
            objects[44:46] = bound4, bound3
            objects[46:48] = [NoObject()] * 2
        elif ram_state[49] <= 9:
            # Three bounding boxes
            objects[44:47] = bound4, bound3, bound2
            objects[47] = NoObject()
        elif ram_state[49] > 9:
            # Four bounding boxes
            objects[44:48] = bound4, bound3, bound2, bound1

        if ram_state[28] < 147:
            bird = Bird()
            bird.xy = ram_state[28] - 12, 30
            objects[43] = bird
        else:
            objects[43] = NoObject()
