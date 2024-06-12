from .game_objects import GameObject, ValueObject
from ._helper_methods import _convert_number, get_iou
import sys

"""
RAM extraction for the game KANGUROO. Supported modes: ram.

"""

MAX_NB_OBJECTS =  {'Player': 1}
MAX_NB_OBJECTS_HUD = {'Player': 1, 'Score': 1, 'Life': 1}
obj_tracker = {}

class Player(GameObject):
    def __init__(self):
        super(Player, self).__init__()
        self._xy = 0, 0
        self.wh = 1, 2
        self.rgb = 168, 48, 143
        self.hud = False

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
        self._xy = 97, 6
        self.wh = 5, 8
        self.rgb = 170, 170, 170
        self.hud = True


class Life(GameObject):
    def __init__(self, *args, **kwargs):
        super(Life, self).__init__()
        self._xy = 88, 15
        self.wh = 7, 5
        self.rgb = 168, 48, 143
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

def _init_objects_ram(hud=True):
    """
    (Re)Initialize the objects
    """

    objects = [Player()]

    objects.extend([None] * 7)
    if hud:
        objects.extend([None] * 4)
    return objects


# levels: ram_state[36], total of 3 levels: 0,1 and 2
def _detect_objects_ram(objects, ram_state, hud=True):
    player = objects[0]

    # 73 = 128 => invis playern
    player.xy = ram_state[85] - 1, ram_state[26] * 2 + 25
    player.wh = 1, 2

    room = ram_state[90]

# ram 39 => color, 233 => type : invis 0;
# ram 64 offset of dublicate

    # sprite0   
    x0 = ram_state[79] - 1
    y0 = (ram_state[20] * 2 + 26)%255

    if room == 8 or room == 9:
        sprite0 = Hallmonsters()
    elif room != 8:
        sprite0 = Shot()
        player.xy = x0, y0
        player.wh = 8, 12
        x0, y0 = ram_state[85] - 1, ram_state[26] * 2 + 25
    else:
        sprite0 = None
    objects[1] = sprite0
    if sprite0 is not None:
        sprite0.xy = x0, y0


    # spirte1   
    x1 = ram_state[80] - 1
    y1 = (ram_state[21] * 2 + 27)%255

    if room == 8 or room == 9:
        sprite1 = Hallmonsters()
    elif room == 0:
        sprite1 = Skeleton()
    elif room == 1:
        sprite1 = Goblin()
    elif room == 2:
        sprite1 = Serpant()
        y1 += 2
    elif room == 3:
        sprite1 = Wall()
        x1 += 1
    elif room == 4:
        sprite1 = TwoHeaded()
    elif room == 5 and y1 == 33:
        sprite1 = Yellow_Collectable()
        sprite1.wh = 8, 14
    elif room == 6 and y1 == 33:
        sprite1 = Pink_Collectable()
        sprite1.wh = 8, 10
    elif room == 7 and y1 == 63:
        sprite1 = Green_Collectable()
        y1 += 4
    else:
        sprite1 = None
    objects[2] = sprite1
    if sprite1 is not None:
        sprite1.xy = x1, y1


    # sprite2
    x2 = ram_state[81] - 7
    y2 = (ram_state[22] * 2 + 27)%255

    if room == 8 or room == 9:
        sprite2 = Hallmonsters()
    elif room == 0 and y2 == 163:
        sprite2 = Purple_Collectable()
    elif room == 1 and y2 == 163:
        sprite2 = Yellow_Collectable()
    elif room == 2 and y2 == 163:
        sprite2 = Pink_Collectable()
    elif room == 3:
        sprite2 = Wall()
        x2 +=7
        sprite2.wh = 4, 24
    elif room == 4 and y2 == 163:
        sprite2 = Grey_Collectable()
        sprite2.wh = 8, 16
        x2 += 6
    elif room == 5:
        sprite2 = Troll()
        x2 += 6
    elif room == 6:
        sprite2 = Dragon()
        x2 += 6
        y2 += 2
    elif room == 7:
        sprite2 = Spider()
        x2 += 6
        y2 += 2
    else:
        sprite2 = None

    objects[3] = sprite2
    if sprite2 is not None:
        sprite2.xy = x2, y2


    # sprite3
    x3 = ram_state[82] - 1
    y3 = (ram_state[23] * 2 + 26)%255

    if room == 8 or room == 9:
        sprite3 = Hallmonsters()
    elif room == 0:
        sprite3 = Skeleton()
    elif room == 1:
        sprite3 = Goblin()
    elif room == 2:
        sprite3 = Serpant()
        y3 += 2
    elif room == 3 and y3 == 102:
        sprite3 = Grey_Collectable()
    elif room == 4:
        sprite3 = TwoHeaded()
    elif room == 5:
        sprite3 = Troll()
    elif room == 6:
        sprite3 = Dragon()
    elif room == 7:
        sprite3 = Spider()
    else:
        sprite3 = None

    objects[4] = sprite3
    if sprite3 is not None:
        sprite3.xy = x3, y3

    # sprite4
    x4 = ram_state[83] - 1
    y4 = (ram_state[24] * 2 + 27)%255

    if room == 8 or room == 9:
        sprite4 = Hallmonsters()
    elif room == 0:
        sprite4 = Skeleton()
    elif room == 1:
        sprite4 = Goblin()
    elif room == 2:
        sprite4 = Serpant()
        y4 += 2
    elif room == 3:
        sprite4 = Wall()
        x4 += 1
        sprite4.wh = 4, 24
    elif room == 4:
        sprite4 = TwoHeaded()
    elif room == 5:
        sprite4 = Troll()
    elif room == 6:
        sprite4 = Dragon()
    elif room == 7:
        sprite4 = Spider()
    else:
        sprite4 = None

    objects[5] = sprite4
    if sprite4 is not None:
        sprite4.xy = x4, y4  


    # sprite5
    x5 = ram_state[84] - 7
    y5 = (ram_state[25] * 2 + 27)%255

    if room == 8 or room == 9:
        sprite5 = Hallmonsters()
    elif room == 3:
        sprite5 = Wall()
        x5 += 7
    else:
        sprite5 = None

    objects[6] = sprite5
    if sprite5 is not None:
        sprite5.xy = x5, y5


    if hud:
        score = Score()
        objects[8] = score
        score.xy = 1, 9
        score.wh = 46, 8
        score.value = _convert_number(ram_state[71])*100 + _convert_number(ram_state[72])
    
        for i in range(3):
            objects[9+i] = None
        for i in range(ram_state[70]):
            life = Life()
            objects[9+i] = life
            life.xy = 112 + i*8, 9
            life.wh = 4, 8

    return objects


def _detect_objects_venture_raw(info, ram_state):
    pass
