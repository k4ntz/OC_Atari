from .game_objects import GameObject, ValueObject
from ._helper_methods import number_to_bitfield
import sys 

MAX_NB_OBJECTS = {"Player": 1, "Bank": 3, "Police": 3}
MAX_NB_OBJECTS_HUD = {}# 'Score': 1}

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


class Score(ValueObject):
    def __init__(self):
        super(Score, self).__init__()
        self._xy = 98, 179
        self.wh = (7, 7)
        self.rgb = 252, 252, 84
        self.hud = False


class Life(GameObject):
    def __init__(self):
        super(Life, self).__init__()
        self._xy = 0, 0
        self.wh = (8, 7)
        self.rgb = 162, 98, 33
        self.hud = False


class Gas_Tank(GameObject):
    def __init__(self):
        super(Gas_Tank, self).__init__()
        self._xy = 42, 12
        self.wh = (12, 25)
        self.rgb = 167, 26, 26
        self.hud = False


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

    objects.extend([None] * 3)
    if hud:
        objects.extend([None] * 8)
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
            elif ram_state[24+i] == 254:
                if type(objects[1+i]) == Police:
                    obj = objects[1+i]
                else:
                    obj = Police()
                    objects[1+i] = obj
            else:
                obj = None
                objects[1+i] = None
            if obj is not None:
                obj.xy = ram_state[29+i], ram_state[9+i]+37
        else:
            objects[1+i] = None
  
    if hud:
        
        # 88-90 == score 

        # Score
        if type(objects[4]) == Score:
            score = objects[4]
        else:
            score = Score()
            objects[4] = score
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
                if type(objects[5+i]) == Life:
                    life = objects[5+i]
                else:
                    life = Life()
                    objects[5+i] = life
                if i < 3:
                    life.xy = 90+(i*16), 27
                else:
                    life.xy = 90+((i-3)*16), 15
            else:
                objects[5+i] = None
        
        # gas tank
        if ram_state[86] < 25:
            if type(objects[11]) == Gas_Tank:
                tank = objects[11]
            else:
                tank = Gas_Tank()
                objects[11] = tank
            tank.xy = 42, 12 + ram_state[86]
            tank.wh = 8, 25 - ram_state[86]
        else:
            objects[11] = None

