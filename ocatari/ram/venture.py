from .game_objects import GameObject, ValueObject, NoObject, Orientation, OrientedObject
from ._helper_methods import _convert_number, get_iou
import numpy as np
import sys

"""
RAM extraction for the game KANGUROO. Supported modes: ram.

"""

MAX_NB_OBJECTS = {'Player': 1, 'Shot': 1, 'Hallmonsters': 6, 'Goblin': 3, 'Serpant': 3, 'Skeleton': 3, 'Wall': 4,
                  'TwoHeaded': 3, 'Troll': 3, 'Dragon': 3, 'Spider': 3, 'Yellow_Collectable': 1, 'Pink_Collectable': 1,
                  'Grey_Collectable': 1, 'Purple_Collectable': 1, 'Green_Collectable': 1}
MAX_NB_OBJECTS_HUD = {'Player': 1, 'Shot': 1, 'Hallmonsters': 6, 'Goblin': 3, 'Serpant': 3, 'Skeleton': 3, 'Wall': 4,
                      'TwoHeaded': 3, 'Troll': 3, 'Dragon': 3, 'Spider': 3, 'Yellow_Collectable': 1, 'Pink_Collectable': 1,
                      'Grey_Collectable': 1, 'Purple_Collectable': 1, 'Green_Collectable': 1, 'Score': 1, 'Life': 1}


class Player(OrientedObject):
    def __init__(self):
        super(Player, self).__init__()
        self._xy = 0, 0
        self.wh = 1, 2
        self.rgb = 168, 48, 143
        self.hud = False
        self.orientation = Orientation.N


class Shot(GameObject):
    def __init__(self):
        super(Shot, self).__init__()
        self._xy = 0, 0
        self.wh = 1, 1
        self.rgb = 168, 48, 143
        self.hud = False


class Hallmonsters(GameObject):
    def __init__(self):
        super(Hallmonsters, self).__init__()
        self._xy = 0, 0
        self.wh = 5, 8
        self.rgb = 82, 126, 45
        self.hud = False


class Goblin(GameObject):
    def __init__(self):
        super(Goblin, self).__init__()
        self._xy = 0, 0
        self.wh = 8, 16
        self.rgb = 78, 50, 181
        self.hud = False


class Serpant(GameObject):
    def __init__(self):
        super(Serpant, self).__init__()
        self._xy = 0, 0
        self.wh = 8, 12
        self.rgb = 82, 126, 45
        self.hud = False


class Skeleton(GameObject):
    def __init__(self):
        super(Skeleton, self).__init__()
        self._xy = 0, 0
        self.wh = 8, 16
        self.rgb = 111, 111, 111
        self.hud = False


class Wall(GameObject):
    def __init__(self):
        super(Wall, self).__init__()
        self._xy = 0, 0
        self.wh = 20, 8
        self.rgb = 181, 83, 40
        self.hud = False


class TwoHeaded(GameObject):
    def __init__(self):
        super(TwoHeaded, self).__init__()
        self._xy = 0, 0
        self.wh = 7, 15
        self.rgb = 184, 50, 50
        self.hud = False


class Troll(GameObject):
    def __init__(self):
        super(Troll, self).__init__()
        self._xy = 0, 0
        self.wh = 8, 15
        self.rgb = 111, 111, 111
        self.hud = False


class Dragon(GameObject):
    def __init__(self):
        super(Dragon, self).__init__()
        self._xy = 0, 0
        self.wh = 8, 14
        self.rgb = 134, 134, 29
        self.hud = False


class Spider(GameObject):
    def __init__(self):
        super(Spider, self).__init__()
        self._xy = 0, 0
        self.wh = 8, 14
        self.rgb = 181, 83, 40
        self.hud = False


class Yellow_Collectable(GameObject):
    def __init__(self):
        super(Yellow_Collectable, self).__init__()
        self._xy = 0, 0
        self.wh = 8, 12
        self.rgb = 134, 134, 29
        self.hud = False


class Pink_Collectable(GameObject):
    def __init__(self):
        super(Pink_Collectable, self).__init__()
        self._xy = 0, 0
        self.wh = 7, 13
        self.rgb = 151, 25, 122
        self.hud = False


class Grey_Collectable(GameObject):
    def __init__(self):
        super(Grey_Collectable, self).__init__()
        self._xy = 0, 0
        self.wh = 7, 12
        self.rgb = 111, 111, 111
        self.hud = False


class Purple_Collectable(GameObject):
    def __init__(self):
        super(Purple_Collectable, self).__init__()
        self._xy = 0, 0
        self.wh = 8, 16
        self.rgb = 78, 50, 181
        self.hud = False


class Green_Collectable(GameObject):
    def __init__(self):
        super(Green_Collectable, self).__init__()
        self._xy = 0, 0
        self.wh = 8, 6
        self.rgb = 50, 132, 50
        self.hud = False


class Score(ValueObject):
    def __init__(self, *args, **kwargs):
        super(Score, self).__init__()
        self._xy = 1, 9
        self.wh = 46, 8
        self.rgb = 170, 170, 170
        self.hud = True


class Life(ValueObject):
    def __init__(self, *args, **kwargs):
        super(Life, self).__init__()
        self._xy = 112, 9
        self.wh = 4, 8
        self.rgb = 168, 48, 143
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


def _init_objects_ram(hud=True):
    """
    (Re)Initialize the objects
    """

    objects = [Player()]

    objects.extend([NoObject()] * 37)
    if hud:
        objects.extend([Score(), Life()])
    return objects

orientations = [Orientation.N, Orientation.S, None, Orientation.W, Orientation.NW, Orientation.SW, None, Orientation.E, Orientation.NE, Orientation.SE]

# levels: ram_state[36], total of 3 levels: 0,1 and 2
def _detect_objects_ram(objects, ram_state, hud=True):

    # 73 = 128 => invis playern
    objects[0].xy = ram_state[85] - 1, ram_state[26] * 2 + 25
    objects[0].wh = 1, 2


    room = ram_state[90]

# ram 39 => color, 233 => type : invis 0;
# ram 64 offset of dublicate
# if y state == 81 enemy gone
    
    idx = []

    # sprite0
    x0 = ram_state[79] - 1
    y0 = (ram_state[20] * 2 + 26) % 255

    if room == 8 or room == 9:
        if type(objects[2]) is NoObject:
            objects[2] = Hallmonsters()
        objects[2].xy = x0, y0
        objects[1] = NoObject()
    elif room != 8:
        if type(objects[1]) is NoObject:
            objects[1] = Shot()
            
        # ram 28 == orientation E, W, S, N inverted bits
        # np.uint8(np.log2(((~ram_state[41])>>4)))
        orientation = (~ram_state[28])>>4
        objects[0].xy = x0, y0
        objects[0].wh = 8, 12
        if orientation:
            objects[0].orientation = orientations[orientation-1]
        print(objects[0].orientation)
        objects[1].xy = ram_state[85] - 1, ram_state[26] * 2 + 25
        objects[2] = NoObject()

    # spirte1
    x1 = ram_state[80] - 1
    y1 = (ram_state[21] * 2 + 27) % 255
    idx1 = None

    if room == 8 or room == 9:
        if type(objects[3]) is NoObject:
            objects[3] = Hallmonsters()
        idx1 = 3
    elif ram_state[21] == 81:
        pass
    elif room == 0:
        if type(objects[14]) is NoObject:
            objects[14] = Skeleton()
        idx1 = 14
    elif room == 1:
        if type(objects[8]) is NoObject:
            objects[8] = Goblin()
        idx1 = 8
    elif room == 2:
        if type(objects[11]) is NoObject:
            objects[11] = Serpant()
        idx1 = 11
        y1 += 2
    elif room == 3:
        if type(objects[17]) is NoObject:
            objects[17] = Wall()
        idx1 = 17
        x1 += 1
    elif room == 4:
        if type(objects[21]) is NoObject:
            objects[21] = TwoHeaded()
        idx1 = 21
    elif room == 5 and y1 == 33:
        if type(objects[33]) is NoObject:
            objects[33] = Yellow_Collectable()
        idx1 = 33
        objects[33].wh = 8, 14
    elif room == 6 and y1 == 33:
        if type(objects[34]) is NoObject:
            objects[34] = Pink_Collectable()
        idx1 = 34
        objects[34].wh = 8, 10
    elif room == 7 and y1 == 63:
        if type(objects[37]) is NoObject:
            objects[37] = Green_Collectable()
        idx1 = 37
        
    if idx1 is not None:
        objects[idx1].xy = x1, y1
        idx.append(idx1)

    # sprite2
    x2 = ram_state[81] - 7
    y2 = (ram_state[22] * 2 + 27) % 255

    idx2 = None

    if room == 8 or room == 9:
        if type(objects[4]) is NoObject:
            objects[4] = Hallmonsters()
        idx2 = 4
    elif ram_state[22] == 81:
        pass
    elif room == 0 and y2 == 163:
        if type(objects[36]) is NoObject:
            objects[36] = Purple_Collectable()
        idx2 = 36
    elif room == 1 and y2 == 163:
        if type(objects[33]) is NoObject:
            objects[33] = Yellow_Collectable()
        idx2 = 33
    elif room == 2 and y2 == 163:
        if type(objects[34]) is NoObject:
            objects[34] = Pink_Collectable()
        idx2 = 34
    elif room == 3:
        if type(objects[18]) is NoObject:
            objects[18] = Wall()
        idx2 = 18
        x2 += 7
        objects[18].wh = 4, 24
    elif room == 4 and y2 == 163:
        if type(objects[35]) is NoObject:
            objects[35] = Grey_Collectable()
        idx2 = 35
        objects[35].wh = 8, 16
        x2 += 6
    elif room == 5:
        if type(objects[24]) is NoObject:
            objects[24] = Troll()
        idx2 = 24
        x2 += 6
    elif room == 6:
        if type(objects[27]) is NoObject:
            objects[27] = Dragon()
        idx2 = 27
        x2 += 6
        y2 += 2
    elif room == 7:
        if type(objects[30]) is NoObject:
            objects[30] = Spider()
        idx2 = 30
        x2 += 6
        y2 += 2
        
    if idx2 is not None:
        objects[idx2].xy = x2, y2
        idx.append(idx2)

    # sprite3
    x3 = ram_state[82] - 1
    y3 = (ram_state[23] * 2 + 26) % 255
    idx3 = None

    if room == 8 or room == 9:
        if type(objects[5]) is NoObject:
            objects[5] = Hallmonsters()
        idx3 = 5
    elif ram_state[23] == 81:
        pass
    elif room == 0:
        if type(objects[15]) is NoObject:
            objects[15] = Skeleton()
        idx3 = 15
    elif room == 1:
        if type(objects[9]) is NoObject:
            objects[9] = Goblin()
        idx3 = 9
    elif room == 2:
        if type(objects[12]) is NoObject:
            objects[12] = Serpant()
        idx3 = 12
        y3 += 2
    elif room == 3 and y3 == 102:
        if type(objects[35]) is NoObject:
            objects[35] = Grey_Collectable()
        idx2 = 35
    elif room == 4:
        if type(objects[22]) is NoObject:
            objects[22] = TwoHeaded()
        idx3 = 22
    elif room == 5:
        if type(objects[25]) is NoObject:
            objects[25] = Troll()
        idx3 = 25
    elif room == 6:
        if type(objects[28]) is NoObject:
            objects[28] = Dragon()
        idx3 = 28
    elif room == 7:
        if type(objects[31]) is NoObject:
            objects[31] = Spider()
        idx3 = 31
        
    if idx3 is not None:
        objects[idx3].xy = x3, y3
        idx.append(idx3)

    # sprite4
    x4 = ram_state[83] - 1
    y4 = (ram_state[24] * 2 + 27) % 255
    idx4 = None

    if room == 8 or room == 9:
        if type(objects[6]) is NoObject:
            objects[6] = Hallmonsters()
        idx4 = 6
    elif ram_state[24] == 81:
        pass
    elif room == 0:
        if type(objects[16]) is NoObject:
            objects[16] = Skeleton()
        idx4 = 16
    elif room == 1:
        if type(objects[10]) is NoObject:
            objects[10] = Goblin()
        idx4 = 10
    elif room == 2:
        if type(objects[13]) is NoObject:
            objects[13] = Serpant()
        idx4 = 13
        y4 += 2
    elif room == 3:
        if type(objects[19]) is NoObject:
            objects[19] = Wall()
        idx4 = 19
        x4 += 1
        objects[19].wh = 4, 24
    elif room == 4:
        if type(objects[23]) is NoObject:
            objects[23] = TwoHeaded()
        idx4 = 23
    elif room == 5:
        if type(objects[26]) is NoObject:
            objects[26] = Troll()
        idx4 = 26
    elif room == 6:
        if type(objects[29]) is NoObject:
            objects[29] = Dragon()
        idx4 = 29
    elif room == 7:
        if type(objects[32]) is NoObject:
            objects[32] = Spider()
        idx4 = 32
        
    if idx4 is not None:
        objects[idx4].xy = x4, y4
        idx.append(idx4)

    # sprite5
    x5 = ram_state[84] - 7
    y5 = (ram_state[25] * 2 + 27) % 255

    if room == 8 or room == 9:
        if type(objects[7]) is NoObject:
            objects[7] = Hallmonsters()
        objects[7].xy = x5, y5
        idx.append(7)
    elif room == 3:
        if type(objects[20]) is NoObject:
            objects[20] = Wall()
        objects[20] = x5 + 7, y5
        idx.append(20)
    
    no_obj = [i for i in range(3, 38) if i not in idx]

    for i in no_obj:
        objects[i] = NoObject()

    if hud:
        objects[38].value = _convert_number(
            ram_state[71])*100 + _convert_number(ram_state[72])

        if ram_state[70]:
            if type(objects[39]) is NoObject:
                objects[39] = Life()
            objects[39].wh = 4 + 8 * (ram_state[70] - 1), 8
            objects[39].value = ram_state[70]
        else:
            objects[39] = NoObject()

def _detect_objects_venture_raw(info, ram_state):
    pass
