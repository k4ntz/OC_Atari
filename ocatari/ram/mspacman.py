from .game_objects import GameObject, ValueObject, NoObject
from ._helper_methods import _convert_number
import math
import sys

"""
RAM extraction for the game Ms. Pac-Man.
"""

# not sure about this one TODO: validate
MAX_NB_OBJECTS = {'Player': 1, 'Ghost': 4,
                  'Fruit': 1, 'PowerPill': 4, 'Pill': 252}
MAX_NB_OBJECTS_HUD = {'Player': 1, 'Ghost': 4, 'Fruit': 1,
                      'PowerPill': 4, 'Pill': 252, 'Score': 3, 'Life': 2}


class Player(GameObject):
    """
    The player figure: Ms. Pac-Man.
    """

    def __init__(self):
        super(Player, self).__init__()
        self._xy = 78, 103
        self.wh = 9, 10
        self.rgb = 210, 164, 74
        self.hud = False


class Ghost(GameObject):
    """
    The Ghosts.
    """

    def __init__(self):
        super(Ghost, self).__init__()
        self._xy = 0, 0
        self.wh = 9, 10
        self.rgb = 200, 72, 72
        self.hud = False


class Fruit(GameObject):
    """
    The collectable fruits.
    """

    def __init__(self):
        super(Fruit, self).__init__()
        self._xy = 125, 173
        self.wh = 9, 10
        self.rgb = 184, 50, 50
        self.hud = False


class PowerPill(GameObject):
    """
    The collectable fruits.
    """

    def __init__(self):
        super(PowerPill, self).__init__()
        self._xy = 125, 173
        self.wh = 4, 7
        self.rgb = 228, 111, 111
        self.hud = False


class Pill(GameObject):
    """
    The collectable fruits.
    """

    def __init__(self, x=0, y=0, i=0, j=0):
        super(Pill, self).__init__()
        self._xy = x, y
        self.wh = 4, 2
        self.rgb = 228, 111, 111
        self.hud = False
        self.grid_ij = i, j


class Score(ValueObject):
    """
    The player's score display (HUD).
    """

    def __init__(self):
        super(Score, self).__init__()
        self._xy = 95, 187
        self.wh = 7, 7
        self.rgb = 195, 144, 61
        self.hud = True
        self.value = 0


class Life(ValueObject):
    """
    The indicator for remaining lives (HUD).
    """

    def __init__(self):
        super(Life, self).__init__()
        self._xy = 12, 173
        self.wh = 7, 10
        self.rgb = 187, 187, 53
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

    objects = [Player()] + [NoObject()] * 9

    # Pills
    objects.extend([NoObject()]*252)

    global GRID1, GRID2
    GRID1 = [
        [1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1],
        [1, 0, 0, 1, 0, 1, 0, 0, 0, 0, 0, 0, 1, 0, 1, 0, 0, 1],
        [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
        [0, 1, 0, 1, 0, 0, 1, 0, 0, 0, 0, 1, 0, 0, 1, 0, 1, 0],
        [1, 1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1, 1],
        [0, 1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1, 0],
        [0, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 0],
        [0, 1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1, 0],
        [1, 1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1, 1],
        [0, 1, 0, 1, 0, 1, 0, 1, 0, 0, 1, 0, 1, 0, 1, 0, 1, 0],
        [1, 1, 1, 1, 0, 1, 0, 1, 1, 1, 1, 0, 1, 0, 1, 1, 1, 1],
        [1, 0, 0, 1, 0, 1, 1, 1, 0, 0, 1, 1, 1, 0, 1, 0, 0, 1],
        [1, 0, 0, 1, 0, 0, 0, 1, 0, 0, 1, 0, 0, 0, 1, 0, 0, 1],
        [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
    ]

    GRID2 = [
        [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
        [1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1],
        [1, 1, 0, 1, 1, 1, 0, 1, 1, 1, 1, 0, 1, 1, 1, 0, 1, 1],
        [0, 1, 0, 1, 0, 1, 0, 1, 0, 0, 1, 0, 1, 0, 1, 0, 1, 0],
        [0, 1, 0, 1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1, 0, 1, 0],
        [1, 1, 1, 1, 0, 0, 1, 0, 0, 0, 0, 1, 0, 0, 1, 1, 1, 1],
        [1, 0, 0, 1, 1, 1, 1, 0, 0, 0, 0, 1, 1, 1, 1, 0, 0, 1],
        [1, 0, 0, 1, 0, 0, 1, 0, 0, 0, 0, 1, 0, 0, 1, 0, 0, 1],
        [1, 0, 0, 1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1, 0, 0, 1],
        [1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1],
        [0, 0, 1, 0, 0, 1, 0, 1, 1, 1, 1, 0, 1, 0, 0, 1, 0, 0],
        [1, 1, 1, 1, 0, 1, 1, 1, 0, 0, 1, 1, 1, 0, 1, 1, 1, 1],
        [1, 0, 0, 1, 0, 1, 0, 0, 0, 0, 0, 0, 1, 0, 1, 0, 0, 1],
        [1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1]
    ]

    if hud:
        objects.extend([Fruit(), Score(), NoObject()])
    return objects


def _detect_objects_ram(objects, ram_state, hud=True):
    player, g1, g2, g3, g4, f, pp1, pp2, pp3, pp4 = objects[:10]

    # ram[56] == orientation (up 0, right 1, down 2, left 3)
    player._xy = ram_state[10] - 13, ram_state[16] + 1

    if ram_state[47] > 0:
        if type(g1) is NoObject:
            objects[1] = Ghost()
        g1.xy = ram_state[6] - 13, ram_state[12] + 1
        g1.rgb = 180, 122, 48
        if ram_state[19] > 0:
            if type(g2) is NoObject:
                objects[2] = Ghost()
            g2.xy = ram_state[7] - 13, ram_state[13] + 1
            g2.rgb = 84, 184, 153
        else:
            objects[2] = NoObject()
        if ram_state[19] > 1:
            if type(g3) is NoObject:
                objects[3] = Ghost()
            g3.xy = ram_state[8] - 13, ram_state[14] + 1
            g3.rgb = 198, 89, 179
        else:
            objects[3] = NoObject()
        if ram_state[19] > 2:
            if type(g4) is NoObject:
                objects[4] = Ghost()
            g4.xy = ram_state[9] - 13, ram_state[15] + 1
        else:
            objects[4] = NoObject()
        # no rgb adjustment, since this color is the default one
    else:
        objects[1], objects[2], objects[3], objects[4] = NoObject(
        ), NoObject(), NoObject(), NoObject()

    if ram_state[11] > 0 and ram_state[17] > 0:
        if type(f) is NoObject:
            objects[5] = Fruit()
        f.xy = ram_state[11] - 13, ram_state[17] + 1
        f.rgb = get_fruit_rgb(ram_state[123])
    else:
        objects[5] = NoObject()

    if ram_state[117] & 4:
        if type(pp1) is NoObject:
            objects[6] = PowerPill()
        pp1.xy = 148, 146
    else:
        objects[6] = NoObject()

    if ram_state[117] & 8:
        if type(pp2) is NoObject:
            objects[7] = PowerPill()
        pp2.xy = 148, 14
    else:
        objects[7] = NoObject()

    if ram_state[117] & 16:
        if type(pp3) is NoObject:
            objects[8] = PowerPill()
        pp3.xy = 8, 147
    else:
        objects[8] = NoObject()

    if ram_state[117] & 32:
        if type(pp4) is NoObject:
            objects[9] = PowerPill()
        pp4.xy = 8, 15
    else:
        objects[9] = NoObject()

    state = 59
    global GRID1, GRID2
    if ram_state[0] == 0:
        grid = GRID1
    else:
        grid = GRID2

    for i in range(14):
        if ram_state[state] & 16 and grid[i][17]:
            if type(objects[27+(i*18)]) is NoObject:
                objects[27+(i*18)] = Pill(148, 7+(12*i), i, 17)
        else:
            objects[27+(i*18)] = NoObject()
        if ram_state[state] & 64 and grid[i][0]:
            if type(objects[10+(i*18)]) is NoObject:
                objects[10+(i*18)] = Pill(8, 7+(12*i), i, 0)
        else:
            objects[10+(i*18)] = NoObject()

        state += 1
        for j in range(8):
            if ram_state[state] & (2**j):
                if j & 1 and grid[i][4-(j >> 1)]:
                    if type(objects[14-(j >> 1)+(i*18)]) is NoObject:
                        objects[14-(j >> 1)+(i*18)] = Pill(40 -
                                                           (8*(j >> 1)), 7+(12*i), i, 4-(j >> 1))
                elif not j & 1 and grid[i][12-(j >> 1)]:
                    if type(objects[22-(j >> 1)+(i*18)]) is NoObject:
                        objects[22-(j >> 1)+(i*18)] = Pill(108 -
                                                           (8*(j >> 1)), 7+(12*i), i, 12-(j >> 1))
            else:
                if j & 1:
                    objects[14-(j >> 1)+(i*18)] = NoObject()
                else:
                    objects[22-(j >> 1)+(i*18)] = NoObject()
        state += 1

        for j in range(8):
            if ram_state[state] & (2**j):
                if not j & 1 and grid[i][5+(j >> 1)]:
                    if type(objects[15+(j >> 1)+(i*18)]) is NoObject:
                        objects[15+(j >> 1)+(i*18)] = Pill(48 +
                                                           (8*(j >> 1)), 7+(12*i), i, 5+(j >> 1))
                elif j & 1 and grid[i][13+(j >> 1)]:
                    if type(objects[23+(j >> 1)+(i*18)]) is NoObject:
                        objects[23+(j >> 1)+(i*18)] = Pill(116 +
                                                           (8*(j >> 1)), 7+(12*i), i, 13+(j >> 1))
            else:
                if not j & 1:
                    objects[15+(j >> 1)+(i*18)] = NoObject()
                else:
                    objects[23+(j >> 1)+(i*18)] = NoObject()
        state += 1

    if hud:

        objects[-3].rgb = get_fruit_rgb(ram_state[123])

        score = _convert_number(ram_state[122]) * 10000 + _convert_number(ram_state[121]) * 100 +\
            _convert_number(ram_state[120])
        sc = objects[-2]
        if ram_state[122] > 15:
            sc.xy = 55, 187
            sc.wh = 47, 7
        elif ram_state[122]:
            sc.xy = 63, 187
            sc.wh = 39, 7
        elif ram_state[121] > 15:
            sc.xy = 71, 187
            sc.wh = 31, 7
        elif ram_state[121]:
            sc.xy = 79, 187
            sc.wh = 23, 7
        elif ram_state[120] > 15:
            sc.xy = 87, 187
            sc.wh = 15, 7
        elif ram_state[120]:
            sc.xy = 95, 187
            sc.wh = 7, 7
        sc.value = score
        objects[-2] = sc

        # lives
        n_lives = ram_state[123] % 4
        if n_lives > 0:
            if type(objects[-1]) is NoObject:
                objects[-1] = Life()
            w = 7 + (n_lives-1)*16
            objects[-1].wh = w, 10
            objects[-1].value = n_lives
        else:
            objects[-1] = NoObject()


def _detect_objects_mspacman_raw(info, ram_state):
    """
    returns unprocessed list with
    player_x, player_y, ghosts_position_x, enemy_position_y, fruit_x, fruit_y
    """
    object_info = {}
    object_info["player_x"] = ram_state[10]
    object_info["player_y"] = ram_state[16]
    object_info["enemy_amount"] = ram_state[19]
    object_info["ghosts_position_x"] = {"orange": ram_state[6],
                                        "cyan": ram_state[7],
                                        "pink": ram_state[8],
                                        "red": ram_state[9]
                                        }
    object_info["ghosts_position_y"] = {"orange": ram_state[12],
                                        "cyan": ram_state[13],
                                        "pink": ram_state[14],
                                        "red": ram_state[15]
                                        }
    object_info["fruit_x"] = ram_state[11]
    object_info["fruit_y"] = ram_state[17]
    info["object-list"] = object_info


def get_fruit_rgb(ram_state):
    """
    every value of 112 and above will result in a glitched fruit
    """

    if ram_state < 16:
        return 184, 50, 50   # "cherry"
    elif ram_state < 32:
        return 184, 50, 50   # "strawberry"
    elif ram_state < 48:
        return 198, 108, 58  # "orange"
    elif ram_state < 64:
        return 162, 162, 42  # "pretzel"
    elif ram_state < 80:
        return 184, 50, 50   # "apple"
    elif ram_state < 96:
        return 110, 156, 66  # "pear"
    elif ram_state < 112:
        return 198, 108, 58  # "banana"
