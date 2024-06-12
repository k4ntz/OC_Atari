from .game_objects import GameObject, ValueObject
from ._helper_methods import _convert_number
import sys 

MAX_NB_OBJECTS = {"Player_Small": 1, "Player_Big": 1, "Opponent_Small": 1, "Opponent_Big": 1, "Ball": 1, "Basket": 1, "Backboard": 1}
MAX_NB_OBJECTS_HUD = {"Player_Small": 1, "Player_Big": 1, "Opponent_Small": 1, "Opponent_Big": 1, "Ball": 1, "Basket": 1, "Backboard": 1, "Player_Score": 1, "Opponent_Score": 1}

class Player_Small(GameObject):
    def __init__(self):
        super(Player_Small, self).__init__()
        self._xy = 76, 100
        self.wh = (8, 19)
        self.rgb = 45, 129, 105
        self.hud = False

class Player_Big(GameObject):
    def __init__(self):
        super(Player_Big, self).__init__()
        self._xy = 76, 100
        self.wh = (8, 23)
        self.rgb = 45, 129, 105
        self.hud = False

class Opponent_Small(GameObject):
    def __init__(self):
        super(Opponent_Small, self).__init__()
        self._xy = 76, 100
        self.wh = (8, 19)
        self.rgb = 236, 236, 236
        self.hud = False

class Opponent_Big(GameObject):
    def __init__(self):
        super(Opponent_Big, self).__init__()
        self._xy = 76, 100
        self.wh = (8, 23)
        self.rgb = 236, 236, 236
        self.hud = False

class Ball(GameObject):
    def __init__(self):
        super(Ball, self).__init__()
        self._xy = 76, 100
        self.wh = (4, 4)
        self.rgb = 144, 72, 17
        self.hud = False

class Basket(GameObject):
    def __init__(self):
        super(Basket, self).__init__()
        self._xy = 76, 42
        self.wh = (8, 9)
        self.rgb = 162, 162, 42
        self.hud = False

class Backboard(GameObject):
    def __init__(self):
        super(Backboard, self).__init__()
        self._xy = 68, 28
        self.wh = (24, 16)
        self.rgb = 214, 214, 214
        self.hud = False


class Player_Score(ValueObject):
    def __init__(self):
        super(Player_Score, self).__init__()
        self._xy = 46, 9
        self.wh = (5, 7)
        self.rgb = 45, 129, 105
        self.hud = True
        self.value = 0

class Opponent_Score(GameObject):
    def __init__(self):
        super(Opponent_Score, self).__init__()
        self._xy = 110, 9
        self.wh = (5, 7)
        self.rgb = 236, 236, 236
        self.hud = True
        self.value = 0


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
    objects = [Player_Small(), Player_Big(), Opponent_Small(), Opponent_Big(), Ball(), Basket(), Backboard()]

    # objects.extend()
    if hud:
        objects.extend([Player_Score(), Opponent_Score()])
        # objects.extend([None] * 13)
    return objects


def _detect_objects_ram(objects, ram_state, hud=False):
    """
    For all 3 objects:
    (x, y, w, h, r, g, b)
    """

    # ram[37-40] == x, ram[33-36] == y, odd player, even enemy
    # x == 69 -> 80, x == 80 -> 91
    # y == 100 -> 59, y == 99 -> 60

    objects[0].xy = ram_state[39] + 11, 163 - ram_state[35]
    objects[1].xy = ram_state[37] + 11, 159 - ram_state[33]
    objects[2].xy = ram_state[40] + 11, 163 - ram_state[36]
    objects[3].xy = ram_state[38] + 11, 159 - ram_state[34]

    # ram[46] == ball_y, ram[47] == ball_x
    objects[4].xy = ram_state[47] + 12, 178 - ram_state[46]

    if hud:
        if ram_state[118] > 15:
            objects[7].xy = 38, 9
            objects[7].wh = 13, 7
            try:
                objects[7].value = _convert_number(ram_state[118])
            except:
                pass
        if ram_state[119] > 15:
            objects[8].xy = 102, 9
            objects[8].wh = 13, 7
            try:
                objects[8].value = _convert_number(ram_state[119])
            except:
                pass
