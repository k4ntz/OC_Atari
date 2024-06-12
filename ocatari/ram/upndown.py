from .game_objects import GameObject, ValueObject
from ._helper_methods import number_to_bitfield
import sys 

MAX_NB_OBJECTS = {"Player": 1}
MAX_NB_OBJECTS_HUD = {}# 'Score': 1}

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


class HUD_Flag(ValueObject):
    def __init__(self):
        super(HUD_Flag, self).__init__()
        self._xy = 57, 7
        self.wh = (5, 12)
        self.rgb = 210, 164, 74
        self.hud = True


class Score(ValueObject):
    def __init__(self):
        super(Score, self).__init__()
        self._xy = 57, 6
        self.wh = (5, 7)
        self.rgb = 168, 48, 143
        self.hud = True


class Life(GameObject):
    def __init__(self):
        super(Life, self).__init__()
        self._xy = 16, 196
        self.wh = (4, 8)
        self.rgb = 198, 108, 58
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
    objects = []

    objects.extend([None] * 20)
    if hud:
        objects.extend([None] * 13)
    return objects


def _detect_objects_ram(objects, ram_state, hud=False):
    """
    For all 3 objects:
    (x, y, w, h, r, g, b)
    """

    # type == r36-r39; x, y == r40-r43, r56-r59

    for i in range(4):
        x, y = ram_state[40+i], ram_state[56+i] + 16
        if ram_state[36+i] == 23:
            objects[i] = None
        elif ram_state[36+i] == 16:
            player = Player()
            objects[i] = player
            player.xy = x, y
        elif ram_state[36+i] < 8:
            w, h = 16, 16
            truck = Truck()
            objects[i] = truck

            # truck colors and offsets
            if ram_state[36+i] == 0:
                truck.rgb = 213, 130, 74
            elif ram_state[36+i] == 1:
                truck.rgb = 214, 92, 92
                x+=2
                w-=2
            elif ram_state[36+i] == 2:
                truck.rgb = 92, 186, 92
                y+=1
                h-=1
            elif ram_state[36+i] == 3:
                truck.rgb = 84, 160, 197
            elif ram_state[36+i] == 4:
                truck.rgb = 164, 89, 208
            elif ram_state[36+i] == 5:
                truck.rgb = 127, 92, 213
                w-=2
            elif ram_state[36+i] == 6:
                truck.rgb = 84, 92, 214
                y+=2
                h-=2
            elif ram_state[36+i] == 7:
                truck.rgb = 84, 138, 210
            truck.xy = x, y
            truck.wh = w, h
        elif ram_state[36+i] < 16 or 23 < ram_state[36+i] < 31:

            # is flag or collectable; they have the same colors
            if ram_state[36+i] < 16:
                col = Flag()
            else:
                col = Collectable()
            objects[i] = col
            if ram_state[36+i]%16 == 8:
                col.rgb = 104, 72, 198
            elif ram_state[36+i]%16 == 9:
                col.rgb = 162, 162, 42
            elif ram_state[36+i]%16 == 10:
                col.rgb = 146, 70, 192
            elif ram_state[36+i]%16 == 11:
                col.rgb = 184, 70, 162
            elif ram_state[36+i]%16 == 12:
                col.rgb = 200, 72, 72
            elif ram_state[36+i]%16 == 13:
                col.rgb = 139, 108, 58
            elif ram_state[36+i]%16 == 14:
                col.rgb = 180, 122, 48
            elif ram_state[36+i]%16 == 15:
                col.rgb = 66, 72, 200
            col.xy = x, y - 1
        else:
            objects[i] = None

    if hud:
        if not ram_state[4]&1:
            hf = HUD_Flag()
            objects[-13] = hf
            hf.rgb = 78, 50, 181
            hf.xy = 91, 14
            hf.wh = 5, 12
        else:
            objects[-13] = None
        if not ram_state[4]&2:
            hf = HUD_Flag()
            objects[-12] = hf
            hf.rgb = 134, 134, 29
            hf.xy = 19, 14
            hf.wh = 5, 12
        else:
            objects[-12] = None
        if not ram_state[4]&4:
            hf = HUD_Flag()
            objects[-11] = hf
            hf.rgb = 125, 48, 173
            hf.xy = 107, 14
            hf.wh = 5, 12
        else:
            objects[-11] = None
        if not ram_state[4]&8:
            hf = HUD_Flag()
            objects[-10] = hf
            hf.rgb = 168, 48, 143
            hf.xy = 127, 14
            hf.wh = 5, 12
        else:
            objects[-10] = None
        if not ram_state[4]&16:
            hf = HUD_Flag()
            objects[-9] = hf
            hf.rgb = 184, 50, 50
            hf.xy = 71, 14
            hf.wh = 5, 12
        else:
            objects[-9] = None
        if not ram_state[4]&32:
            hf = HUD_Flag()
            objects[-8] = hf
            hf.rgb = 181, 83, 40
            hf.xy = 55, 14
            hf.wh = 5, 12
        else:
            objects[-8] = None
        if not ram_state[4]&64:
            hf = HUD_Flag()
            objects[-7] = hf
            hf.rgb = 162, 98, 33
            hf.xy = 35, 14
            hf.wh = 5, 12
        else:
            objects[-7] = None
        if not ram_state[4]&128:
            hf = HUD_Flag()
            objects[-6] = hf
            hf.rgb = 45, 50, 184
            hf.xy = 143, 14
            hf.wh = 5, 12
        else:
            objects[-6] = None

        # Score
        score = Score()
        objects[-5] = score
        x, w= 57, 5
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
        
        score.xy = x, 6
        score.wh = w, 7
        
            
        # Lives r6
        for i in range(4):
            if ram_state[6]%5 > i:
                life = Life()
                objects[-4+i] = life
                life.xy = 16+(8*i), 196
            else:
                objects[-4+i] = None
