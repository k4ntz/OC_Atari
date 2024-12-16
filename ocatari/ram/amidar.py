import pdb
from .game_objects import GameObject, ValueObject, NoObject
from ._helper_methods import number_to_bitfield
from .utils import match_objects
import sys

MAX_NB_OBJECTS = {"Player": 1, "Warrior": 6,
                  "Pig": 6, "Shadow": 6, "Chicken": 6}
MAX_NB_OBJECTS_HUD = {"Player": 1, "Warrior": 6, "Pig": 6,
                      "Shadow": 6, "Chicken": 6, "Score": 1, "Life": 3}


class Player(GameObject):
    def __init__(self):
        super(Player, self).__init__()
        self._xy = 0, 160
        self.wh = (7, 7)
        self.rgb = 252, 252, 84
        self.hud = False


class Warrior(GameObject):
    def __init__(self, x=0, y=160, w=7, h=7):
        super(Warrior, self).__init__()
        self._xy = x, y
        self.wh = (w, h)
        self.rgb = 135, 183, 84
        self.hud = False


class Pig(GameObject):
    def __init__(self, x=0, y=160, w=7, h=7):
        super(Pig, self).__init__()
        self._xy = x, y
        self.wh = (w, h)
        self.rgb = 214, 92, 92
        self.hud = False


class Shadow(GameObject):
    def __init__(self, x=0, y=160, w=7, h=7):
        super(Shadow, self).__init__()
        self._xy = x, y
        self.wh = (w, h)
        self.rgb = 0, 0, 0
        self.hud = False


class Chicken(GameObject):
    def __init__(self, x=0, y=160, w=7, h=7):
        super(Chicken, self).__init__()
        self._xy = x, y
        self.wh = (w, h)
        self.rgb = 252, 252, 84
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
    objects = [Player()] + [Warrior() for _ in range(6)]
    # for the pigs, shadows and chickens
    objects.extend([NoObject() for _ in range(18)])
    if hud:
        # objects.extend([NoObject()] * 4)
        objects.extend([Score(), Life(), Life(), Life()])
    return objects


def _detect_objects_ram(objects, ram_state, hud=False):
    """
    For all 3 objects:
    (x, y, w, h, r, g, b)
    """
    # x == 66-72; y == 59-65; type 73-79
    k = 0
    warrior_bb, pig_bb = [], []
    enemy_type = Warrior
    chicken_bb = []
    bitmap_warrior = 0b00100000
    bitmap_pig = 0b00110000
    bitmap_chicken = 0b01110000
    for i in range(7):
        if ram_state[73+i] & bitmap_chicken == bitmap_chicken:
            fig = Chicken()
            fig.xy = ram_state[66+i]+9, ram_state[59+i]+7
            chicken_bb.append(fig.xywh)
        elif ram_state[73+i] & bitmap_pig == bitmap_pig:
            fig = Pig()
            enemy_type = Pig
            fig.xy = ram_state[66+i]+9, ram_state[59+i]+7
            pig_bb.append(fig.xywh)
        elif ram_state[73+i] & bitmap_warrior == bitmap_warrior:
            fig = Warrior()
            enemy_type = Warrior
            fig.xy = ram_state[66+i]+9, ram_state[59+i]+7
            warrior_bb.append(fig.xywh)
        else:  # the object is the player
            fig = objects[0]
            fig.xy = ram_state[66+i]+9, ram_state[59+i]+7

    match_objects(objects, warrior_bb, 1, 6, Warrior)

    match_objects(objects, pig_bb, 7, 6, Pig)

    match_objects(objects, chicken_bb, 19, 6, Chicken)

    # insert or remove the shadows; if (ram_state[51] == 103) all the enemies are shadows because of jumping,
    # if there is at least one chicken, any enemy is a chicken which has been caught and therefore also a shadow
    # the shadows are inserted at the position of the enemy they replace, ond then the enemy (which is detected again each frame) is removed
    if len(chicken_bb) > 0 or (ram_state[51] == 103):
        for i, enemy in enumerate(objects[1:13]):
            if not isinstance(enemy, NoObject):
                coresponding_shadow_index = 13+((i-1) % 6)
                if isinstance(objects[coresponding_shadow_index], Shadow):
                    objects[coresponding_shadow_index].xywh = (
                        enemy.xy[0], enemy.xy[1], enemy.wh[0], enemy.wh[1])
                else:
                    objects[coresponding_shadow_index] = Shadow(
                        enemy.xy[0], enemy.xy[1], enemy.wh[0], enemy.wh[1])
                objects[1+i] = NoObject()
    else:
        for i in range(6):
            if objects[13+i] is not NoObject:
                objects[13+i] = NoObject()

    if hud:
        score = objects[-4]
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
            life = objects[-1-i]
            if i < ram_state[86] & 3:
                if not life:
                    life = Life()
                    objects[-1-i] = life
                    life.xy = 148-(i*16), 175
            else:
                objects[-1-i] = NoObject()
