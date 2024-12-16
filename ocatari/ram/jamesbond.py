from .game_objects import GameObject, ValueObject
from ._helper_methods import number_to_bitfield
import sys

MAX_NB_OBJECTS = {"Player": 1}
MAX_NB_OBJECTS_HUD = {}  # 'Score': 1}


class Player(GameObject):
    def __init__(self):
        super(Player, self).__init__()
        self._xy = 0, 160
        self.wh = (8, 4)
        self.rgb = 227, 151, 89
        self.hud = False


class Player_Shot(GameObject):
    def __init__(self):
        super(Player_Shot, self).__init__()
        self._xy = 0, 160
        self.wh = (1, 4)
        self.rgb = 227, 151, 89
        self.hud = False


class Helicopter(GameObject):
    def __init__(self):
        super(Helicopter, self).__init__()
        self._xy = 0, 160
        self.wh = (8, 6)
        self.rgb = 167, 26, 26
        self.hud = False


class Hornet(GameObject):
    def __init__(self):
        super(Hornet, self).__init__()
        self._xy = 0, 160
        self.wh = (8, 14)
        self.rgb = 170, 170, 170
        self.hud = False


class Enemy_Shot(GameObject):
    def __init__(self):
        super(Enemy_Shot, self).__init__()
        self._xy = 0, 160
        self.wh = (1, 4)
        self.rgb = 252, 224, 112
        self.hud = False


class Ice(GameObject):
    def __init__(self):
        super(Ice, self).__init__()
        self._xy = 0, 160
        self.wh = (8, 12)
        self.rgb = 45, 87, 176
        self.hud = False


class Fire_Hole(GameObject):
    def __init__(self):
        super(Fire_Hole, self).__init__()
        self._xy = 0, 160
        self.wh = (16, 48)
        self.rgb = 72, 44, 0
        self.hud = False


class Eruption(GameObject):
    def __init__(self):
        super(Eruption, self).__init__()
        self._xy = 0, 125
        self.wh = (32, 15)
        self.rgb = 26, 102, 26
        self.hud = False


class Diver(GameObject):
    def __init__(self):
        super(Diver, self).__init__()
        self._xy = 0, 125
        self.wh = (7, 20)
        self.rgb = 26, 102, 26
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
        self.wh = (8, 4)
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
    objects = [Player()]

    objects.extend([None] * 5)
    if hud:
        objects.extend([None] * 4)
    return objects


def _detect_objects_ram(objects, ram_state, hud=False):
    """
    For all 3 objects:
    (x, y, w, h, r, g, b)
    """

    # player x,y == r27 - 1, 50 + r25
    player = objects[0]
    player.xy = ram_state[27] - 1, 50 + ram_state[25]

    # row1 x,y == r61, 57
    if ram_state[49] != 255:
        if objects[1] is None:
            if ram_state[49] == 6:
                row1 = Helicopter()
            else:
                row1 = Ice()
            objects[1] = row1
        else:
            row1 = objects[1]
        row1.xy = ram_state[61] - 1, 57
    else:
        objects[1] = None

    # row2 x,y == r59, 57
    if ram_state[50] != 255:
        if objects[2] is None:
            # if ram_state[50] == 140:
            row2 = Hornet()
            objects[2] = row2
        else:
            row2 = objects[2]
        row2.xy = ram_state[59] - 2, 75
    else:
        objects[2] = None

    # pshot xy = r38, r31
    if ram_state[31] != 128:
        p_shot = Player_Shot()
        objects[3] = p_shot
        p_shot.xy = ram_state[38] - 11, 55 + ram_state[31]
    else:
        objects[3] = None

    # eshot xy = r39, r30
    if ram_state[30] != 128:
        e_shot = Enemy_Shot()
        objects[4] = e_shot
        e_shot.xy = ram_state[39] - 11, 55 + ram_state[30]
    else:
        objects[4] = None

    # fire hole x == 43
    # erupt == r51; x == r60; size == r109, 86 == small, 102 == big
    if ram_state[51] == 54 and ram_state[108] == 251:
        erup = Eruption()
        objects[5] = erup
        if ram_state[109] == 86:
            erup.xy = ram_state[60] + 4, 125
            erup.wh = 20, 7
        else:
            erup.xy = ram_state[60], 125
            erup.wh = 32, 15
    elif ram_state[51] == 48:
        div = Diver()
        objects[5] = div
        div.xy = ram_state[60] - 1, 131
    elif ram_state[108] == 250:
        if type(objects[5]) == Fire_Hole:
            hole = objects[5]
        else:
            hole = Fire_Hole()
            objects[5] = hole
        hole.xy = ram_state[43], 122
    else:
        objects[5] = None

    if hud:
        # Score
        score = Score()
        objects[6] = score
        if ram_state[94] > 15:
            score.xy = 55, 15
            score.wh = 46, 7
        elif ram_state[94]:
            score.xy = 63, 15
            score.wh = 38, 7
        elif ram_state[93] > 15:
            score.xy = 71, 15
            score.wh = 30, 7
        elif ram_state[93]:
            score.xy = 79, 15
            score.wh = 22, 7
        elif ram_state[92] > 15:
            score.xy = 87, 15
            score.wh = 14, 7
        else:
            score.xy = 95, 15
            score.wh = 6, 7

        # Lives 86
        for i in range(3):
            if i < ram_state[111]:
                life = Life()
                objects[7+i] = life
                life.xy = 9+(i*16), 184
            else:
                objects[7+i] = None
