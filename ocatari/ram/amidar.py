from .game_objects import GameObject, ValueObject
from ._helper_methods import number_to_bitfield
import sys 

MAX_NB_OBJECTS = {"Player": 1, "Moster": 6}
MAX_NB_OBJECTS_HUD = {}# 'Score': 1}

class Player(GameObject):
    def __init__(self):
        super(Player, self).__init__()
        self._xy = 0, 160
        self.wh = (7, 7)
        self.rgb = 252, 252, 84
        self.hud = False


class Monster_green(GameObject):
    def __init__(self):
        super(Monster_green, self).__init__()
        self._xy = 0, 160
        self.wh = (7, 7)
        self.rgb = 135, 183, 84
        self.hud = False


class Monster_yellow(GameObject):
    def __init__(self):
        super(Monster_yellow, self).__init__()
        self._xy = 0, 160
        self.wh = (7, 7)
        self.rgb = 252, 252, 84
        self.hud = False


class Monster_red(GameObject):
    def __init__(self):
        super(Monster_red, self).__init__()
        self._xy = 0, 160
        self.wh = (7, 7)
        self.rgb = 214, 92, 92
        self.hud = False


class Score(ValueObject):
    def __init__(self):
        super(Score, self).__init__()
        self._xy = 0, 0
        self.wh = (7, 7)
        self.rgb = 252, 252, 84
        self.hud = False


class Life(GameObject):
    def __init__(self):
        super(Life, self).__init__()
        self._xy = 0, 0
        self.wh = (1, 8)
        self.rgb = 252, 252, 84
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
    objects = [Player(), Monster_green(), Monster_green(), Monster_green(), Monster_green(), Monster_green(), Monster_green()]

    if hud:
        objects.extend([None] * 4)
    return objects


def _detect_objects_ram(objects, ram_state, hud=False):
    """
    For all 3 objects:
    (x, y, w, h, r, g, b)
    """

    # x == 66-72; y == 59-65; type 73-79
    k = 0
    for i in range(7):
        objects[1+i] = None
        if ram_state[73+i]&16 and ram_state[73+i]&32:
            fig = Monster_red()
            objects[1+i] = fig
            fig.xy = ram_state[66+i]+9, ram_state[59+i]+7
            k+=1
        elif ram_state[73+i]&32:
            fig = Monster_green()
            objects[1+k] = fig
            fig.xy = ram_state[66+i]+9, ram_state[59+i]+7
            k+=1
        # elif ram_state[73+i]&16:
        #     fig = Monster_yellow()
        #     objects[1+i] = fig
        #     fig.xy = ram_state[66+i]+9, ram_state[59+i]+7
        else:
            fig = objects[0]
            fig.xy = ram_state[66+i]+9, ram_state[59+i]+7

    # 6-49 purple lines; first 4 ==> lines, remaining ==> pillars
    # even numbers are inverted

    # for i in range(6):
    #     for j in range(4):
    #         line = number_to_bitfield(ram_state[6+(i*8)+j])
    #         if not i%2:
    #             line.reverse()
            


    if hud:

        # Score
        score = Score()
        objects[7] = score
        if ram_state[91] > 15:
            score.xy = 57, 176
            score.wh = 46, 7
        elif ram_state[91]:
            score.xy = 65, 176
            score.wh = 38, 7
        elif ram_state[90] > 15:
            score.xy = 73, 176
            score.wh = 30, 7
        elif ram_state[90]:
            score.xy = 81, 176
            score.wh = 22, 7
        elif ram_state[89] > 15:
            score.xy = 89, 176
            score.wh = 16, 7
        else:
            score.xy = 97, 176
            score.wh = 7, 7
        
        # Lives 86
        for i in range(3):
            if i < ram_state[86]&3:
                life = Life()
                objects[8+i] = life
                life.xy = 148-(i*16), 175
            else:
                objects[8+i] = None
