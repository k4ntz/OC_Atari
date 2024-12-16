from ._helper_methods import number_to_bitfield
from .game_objects import GameObject, ValueObject, NoObject
import sys

MAX_NB_OBJECTS = {"Player": 1, "Bank": 3, "Police": 3, "Dynamite": 1}
MAX_NB_OBJECTS_HUD = {"Player": 1, "Bank": 3, "Police": 3,
                      "Dynamite": 1, "Score": 1, "Life": 6, "Gas_Tank": 1}


class Player(GameObject):
    def __init__(self):
        super(Player, self).__init__()
        self._xy = 0, 160
        self.wh = (8, 7)
        self.rgb = 162, 98, 33
        self.hud = False


class Bank(GameObject):
    def __init__(self):
        super(Bank, self).__init__()
        self._xy = 0, 160
        self.wh = (8, 7)
        self.rgb = 142, 142, 142
        self.hud = False


class Police(GameObject):
    def __init__(self):
        super(Police, self).__init__()
        self._xy = 0, 160
        self.wh = (8, 7)
        self.rgb = 24, 26, 167
        self.hud = False


class Dynamite(GameObject):
    def __init__(self):
        super(Dynamite, self).__init__()
        self._xy = 0, 160
        self.wh = 8, 2
        self.rgb = 255, 255, 255
        self.hud = False


class Score(ValueObject):
    def __init__(self):
        super(Score, self).__init__()
        self._xy = 98, 179
        self.wh = (7, 7)
        self.rgb = 252, 252, 84
        self.hud = True
        self.value = 0


class Life(GameObject):
    def __init__(self):
        super(Life, self).__init__()
        self._xy = 0, 0
        self.wh = (8, 7)
        self.rgb = 162, 98, 33
        self.hud = True


class Gas_Tank(GameObject):
    def __init__(self):
        super(Gas_Tank, self).__init__()
        self._xy = 42, 12
        self.wh = (12, 25)
        self.rgb = 167, 26, 26
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
    objects = [Player()]

    objects.extend([NoObject()] * 8)
    if hud:
        objects.extend([NoObject()]*8)
    return objects


def _detect_objects_ram(objects, ram_state, hud=False):
    """
    For all 3 objects:
    (x, y, w, h, r, g, b)
    """

    # 15&8 == orientation -> 0 == right
    # 28,8 == x,y

    player = objects[0]
    player.xy = ram_state[28], ram_state[8]+37

    for i in range(3):
        if ram_state[9+i]:
            if ram_state[24+i] == 253:
                if type(objects[1+i]) == Bank:
                    obj = objects[1+i]
                else:
                    obj = Bank()
                    objects[1+i] = obj
            else:
                obj = NoObject()
                objects[1+i] = NoObject()
            if not isinstance(obj, NoObject):
                obj.xy = ram_state[29+i], ram_state[9+i]+37
        else:
            objects[1+i] = NoObject()

    for i in range(3):
        if ram_state[9+i]:
            if ram_state[24+i] == 254:
                if type(objects[4+i]) == Police:
                    obj = objects[4+i]
                else:
                    obj = Police()
                    objects[4+i] = obj
            else:
                obj = NoObject()
                objects[4+i] = NoObject()
            if not isinstance(obj, NoObject):
                obj.xy = ram_state[29+i], ram_state[9+i]+37
        else:
            objects[4+i] = NoObject()

    if ram_state[12]:
        if type(objects[7]) == Dynamite:
            obj = objects[7]
        else:
            obj = Dynamite()
            objects[7] = obj
        obj.xy = ram_state[32]-1, ram_state[12]+37
    else:
        if objects[7]:
            objects[7] = NoObject()

    if hud:
        # 88-90 == score
        # Score
        if type(objects[8]) == Score:
            score = objects[8]
        else:
            score = Score()
            objects[8] = score
        if ram_state[88] > 15:
            score.xy = 58, 179
            score.wh = 46, 7
        elif ram_state[89] > 15:
            score.xy = 66, 179
            score.wh = 38, 7
        elif ram_state[89]:
            score.xy = 74, 179
            score.wh = 30, 7
        elif ram_state[90] > 15:
            score.xy = 82, 179
            score.wh = 22, 7
        elif ram_state[90]:
            score.xy = 90, 179
            score.wh = 16, 7
        else:
            score.xy = 98, 179
            score.wh = 5, 7

        # Lives
        for i in range(6):
            if i < ram_state[85]:
                if type(objects[9+i]) == Life:
                    life = objects[9+i]
                else:
                    life = Life()
                    objects[9+i] = life
                if i < 3:
                    life.xy = 90+(i*16), 27
                else:
                    life.xy = 90+((i-3)*16), 15
            else:
                objects[9+i] = NoObject()

        # gas tank
        if type(objects[15]) != Gas_Tank:
            tank = Gas_Tank()
            objects[15] = tank

        objects[15].xy = 42, 12 + ram_state[86]
        objects[15].wh = 8, 25 - ram_state[86]
