from .game_objects import GameObject, NoObject
from .utils import match_objects
import sys

"""
RAM extraction for the game Frostbite.
"""

MAX_NB_OBJECTS = {"Player": 1, "Bear": 1, "House": 1, "Door": 1,
                  "Bird": 8, "Crab": 8, "Clam": 8, "GreenFish": 8, "FloatingBlock": 24}
MAX_NB_OBJECTS_HUD = {"Player": 1, "Bear": 1, "House": 1, "Door": 1, "Bird": 8, "Crab": 8, "Clam": 8, "GreenFish": 8, "FloatingBlock": 24,
                      "Lives": 1, "Temperature": 1, "Score": 1}


class Player(GameObject):
    """
    The player figure: Frostbite Bailey.
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._xy = 0, 0
        self.wh = (8, 18)
        self.rgb = 198, 108, 58
        self.hud = False


class Bear(GameObject):
    """
    The dangerous grizzly polar bears on the shore (level 4).
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.rgb = 111, 111, 111
        self.hud = False
        self.wh = (14, 16)
        self._xy = 0, 0


class House(GameObject):
    """
    The igloo Frostbite Bailey is trying to build.
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.rgb = 142, 142, 142
        self.hud = False
        self.wh = (8, 18)
        self._xy = 0, 0


class Door(GameObject):
    """
    The finished igloo.
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._xy = 123, 47
        self.rgb = 0, 0, 0
        self.hud = False
        self.wh = 8, 8


class FloatingBlock(GameObject):
    """
    The white, untouched ice floes, turning blue once jumped over.
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.rgb = 214, 214, 214
        self.hud = False
        self.wh = 24, 7
        self._xy = 0, 0

class Bird(GameObject):
    """
    The wild snowgeese.
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.rgb = 132, 144, 252
        self.hud = False
        self.wh = (8, 7)
        self._xy = 0, 0


class Crab(GameObject):
    """
    The dangerous Alaskan king crabs.
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.rgb = 213, 130, 74
        self.hud = False
        self.wh = (8, 7)
        self._xy = 0, 0


class GreenFish(GameObject):
    """
    The fresh fish swimming by regularly.
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.rgb = 111, 210, 111
        self.wh = (8, 6)
        self.hud = False
        self._xy = 0, 0


class Clam(GameObject):
    """
    The dangerous clams.
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.rgb = 210, 210, 64
        self.hud = False
        self._xy = 0, 0
        self.wh = (8, 7)


class Lives(GameObject):
    """
    The indicator for the player's lives.
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._xy = 63, 22
        self.rgb = 132, 144, 252
        self.hud = True
        self.wh = 6, 8


class Temperature(GameObject):
    """
    The temperature display.
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._xy = 23, 22
        self.wh = 18, 8
        self.rgb = 132, 144, 252
        self.hud = True


class Score(GameObject):
    """
    The player's score display.
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._xy = 63, 10
        self.rgb = 132, 144, 252
        self.hud = True
        self.wh = 6, 8


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
    objects.extend([NoObject()])
    objects.extend([NoObject(), NoObject()])  # House/Door
    # for bird, clams, crabs and greenfishes
    objects.extend([NoObject() for _ in range(32)])
    objects.extend([NoObject() for _ in range(24)])  # for the plates
    if hud:
        objects.extend([Lives(), Temperature(), Score()])
    return objects


def _detect_objects_ram(objects, ram_state, hud=False):
    """
    For all 3 objects:
    (x, y, w, h, r, g, b)
    """
    # 106 ram_state is somewhat controlling the y of the player when it's dying by sinking
    player = objects[0]
    if ram_state[106] == 26:
        if player:
            objects[0] = NoObject()
    else:
        if not player:
            player = Player()
            objects[0] = player
    player.xy = ram_state[102], ram_state[100]+29
    if 0 < ram_state[107] < 18:
        sink = ram_state[107]
        player.y += sink
        player.h = 18 - sink
    elif 18 <= ram_state[107]:  # sunk
        objects[0] = NoObject()

    # Bear
    if ram_state[104] == 140:
        if objects[1]:
            objects[1] = NoObject()
    else:
        if not objects[1]:
            bear = Bear()
            objects[1] = bear
        else:
            bear = objects[1]
        bear.xy = ram_state[104]+3, 58
        objects[1] = bear

    # House
    position_list = [(112, 51), (112, 51), (112, 51), (112, 51), (112, 47), (112, 47), (112, 47), (
        112, 47), (112, 42), (112, 42), (112, 42), (112, 42), (112, 39), (112, 39), (112, 35), (112, 35)]
    size_list = [(8, 4), (16, 4), (24, 4), (32, 4), (32, 8), (32, 8), (32, 8), (32, 8),
                 (32, 13), (32, 13), (32, 13), (32, 13), (32, 16), (32, 16), (32, 20), (32, 20)]
    if ram_state[77] == 255:
        if objects[2]:
            objects[2] = NoObject()
    else:
        if not objects[2]:
            house = House()
            objects[2] = house
        else:
            house = objects[2]
        house.xy = position_list[ram_state[77]]
        house.wh = size_list[ram_state[77]]

    # Door
    if ram_state[77] == 15:
        if not objects[3]:
            door = Door()
            objects[3] = door
        else:
            door = objects[3]
    elif objects[3]:
        objects[3] = NoObject()

    # # Birds, Crabs, Clams, GreenFish
    if ram_state[107] == 0 and ram_state[103] == 64:  # reset
        for i in range(24):
            if objects[4+i]:
                objects[4+i] = NoObject()
    for i in range(4):
        if 0 < ram_state[84+i] < 160 or ram_state[88+i]:
            type = ram_state[35+i]
            if type in [18, 26]:
                Otype = Bird
                offset = 0
            elif 33 < type < 39 or 49 < type < 55:
                Otype = Crab
                offset = 1
            elif 65 < type < 71 or 93 < type < 99:
                Otype = Clam
                offset = 2
            elif 108 < type < 114 or 123 < type < 129:
                Otype = GreenFish
                offset = 3
            else:
                raise AttributeError(
                    f"THe type at position {35+i} is {type} and unknown")
            idx = 4 + offset*8 + i
            if isinstance(objects[idx], Otype):
                obj = objects[idx]
            else:
                obj = Otype()
                objects[idx] = obj
            obj.xy = ram_state[84+i], 160 - 26 * i
            idx2 = 8 + offset*8 + i
            if ram_state[88+i]:  # 2 objects
                if isinstance(objects[idx2], Otype):
                    obj2 = objects[idx2]
                else:
                    obj2 = Otype()
                    objects[idx2] = obj2
                obj2.xy = ram_state[84+i] + 32, 160 - 26 * i
            else:
                if objects[idx2]:
                    objects[idx2] = NoObject()
        else:
            for offset in range(4):
                if objects[4+offset*8+i]:
                    objects[4+offset*8+i] = NoObject()

    # # Adding the Plates
    for i in range(4):
        if ram_state[30] == 8:  # single plates
            num_plates = 3
            pwidth = 24
            for j in range(12):
                if objects[48+j]:
                    objects[48+j] = NoObject()
        else:
            num_plates = 6
            pwidth = 16
        sep = 32 if ram_state[30] == 8 else 16
        for plat in range(num_plates):
            space = abs(ram_state[30]-8)
            idx = 36 + i*num_plates + plat
            if objects[idx]:
                obj = objects[idx]
            else:
                obj = FloatingBlock()
                objects[idx] = obj
            if num_plates == 3:
                obj.xy = (ram_state[31+i] + plat*sep - 8) % 160, 174 - 26*i
            else:
                if plat % 2 == 0:
                    xoffset = max(0, space-4)
                    obj.xy = (ram_state[31+i] + plat*sep -
                              8 - xoffset) % 160, 174 - 26*i
                else:
                    xoffset = min(space, 4)
                    obj.xy = (ram_state[31+i] + plat*sep -
                              16 + xoffset) % 160, 174 - 26*i
            # white or blue plate
            obj.rgb = (
                214, 214, 214) if ram_state[43+i] == 12 else (84, 138, 210)
            obj.w = pwidth
    if hud:
        # LifeCount
        if ram_state[76] != 0:
            lives = objects[60]
            if not lives:
                lives = Lives()
                objects[60] = lives
            lives.xy = 63, 22
        else:
            objects[60] = NoObject()

        # Temperature
        temp = objects[61]
        if ram_state[101] <= 9:
            temp.xy = 31, 22
            temp.wh = 10, 8
        else:
            temp.xy = 23, 22
            temp.wh = 18, 8

        # Player Score
        score = objects[62]
        svalue = 0
        if ram_state[72] != 0:
            if ram_state[72] < 10:
                score.xy = 31, 10
                score.wh = 38, 8
            else:
                score.xy = 23, 10
                score.wh = 46, 8
        elif ram_state[73] != 0:
            if ram_state[73] < 10:
                score.xy = 47, 10
                score.wh = 22, 8
            else:
                score.xy = 39, 10
                score.wh = 30, 8
        elif ram_state[74] != 0:
            if ram_state[74] < 10:
                score._xy = 63, 10
                score.wh = 6, 8
            else:
                score.xy = 55, 10
                score.wh = 14, 8
        svalue += int(hex(ram_state[72])[2:]) * 10000
        svalue += int(hex(ram_state[73])[2:]) * 100
        svalue += int(hex(ram_state[74])[2:])


def _detect_objects_frostbite_raw(info, ram_state):
    """
    returns unprocessed list with
    ball_x, ball_y, enemy_y, player_y
    """
    info["objects_list"] = ram_state[32:36]
