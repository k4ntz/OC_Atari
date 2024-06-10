import math
import sys

import numpy as np

from ._helper_methods import _convert_number
from .game_objects import GameObject

"""
RAM extraction for the game Pitfall.

"""

MAX_NB_OBJECTS = {"Player": 1, "Wall": 1, "Logs": 5, "StairPit": 4, "Pit": 3, "Scorpion": 1, "Rope": 1, "Snake": 1,
                  "Tarpit": 1, "Waterhole": 1, "Crocodile": 1, "GoldenBar": 1, "Fire": 1}
MAX_NB_OBJECTS_HUD = {"LifeCount": 3, "PlayerScore": 6, "Timer": 5}


class Player(GameObject):
    """
    The player figure: Pitfall Harry.
    """

    def __init__(self):
        super().__init__()
        self._xy = 0, 0
        self.wh = (7, 20)
        self.rgb = 53, 95, 24
        self.hud = False


class Wall(GameObject):
    """
    The underground brick walls.
    """

    def __init__(self):
        super().__init__()
        self.xy = 0, 0
        self.wh = (7, 32)
        self.rgb = 167, 26, 26
        self.hud = False


class Logs(GameObject):
    """
    The logs.
    """

    def __init__(self):
        super().__init__()
        self.xy = 0, 0
        self.wh = (6, 14)
        self.rgb = 105, 105, 15
        self.hud = False


class StairPit(GameObject):
    """
    The escape shafts from the underground.
    """

    def __init__(self):
        super().__init__()
        self.xy = 0, 0
        self.wh = (8, 6)
        self.rgb = 0, 0, 0
        self.hud = False


class Pit(GameObject):
    """
    The open holes in the ground.
    """

    def __init__(self):
        super().__init__()
        self.xy = 0, 0
        self.wh = (12, 6)
        self.rgb = 252, 188, 116
        self.hud = False


class Scorpion(GameObject):
    """
    The scorpions.
    """

    def __init__(self):
        super().__init__()
        self.xy = 0, 0
        self.wh = (7, 10)
        self.rgb = 236, 236, 236
        self.hud = False


class Rope(GameObject):
    """
    The swinging vines.
    """

    def __init__(self):
        super().__init__()
        self.xy = 0, 0
        self.wh = (1, 1)
        self.rgb = 72, 72, 0
        self.hud = False


class Snake(GameObject):
    """
    The snakes.
    """

    def __init__(self):
        super().__init__()
        self.xy = 0, 0
        self.wh = (8, 14)
        self.rgb = 167, 26, 26
        self.hud = False


class Tarpit(GameObject):
    """
    The tar pits.
    """

    def __init__(self):
        super().__init__()
        self.xy = 0, 0
        self.wh = (64, 10)
        self.rgb = 0, 0, 0
        self.hud = False


class Waterhole(GameObject):
    """
    The swamps.
    """

    def __init__(self):
        super().__init__()
        self.xy = 0, 0
        self.wh = (64, 10)
        self.rgb = 45, 109, 152
        self.hud = False


class Crocodile(GameObject):
    """
    The crocodiles.
    """

    def __init__(self):
        super().__init__()
        self.xy = 0, 0
        self.wh = (8, 8)
        self.rgb = 20, 60, 0
        self.hud = False


class GoldenBar(GameObject):
    """
    The collectable gold bars.
    """

    def __init__(self):
        super().__init__()
        self.xy = 0, 0
        self.wh = (7, 13)
        self.rgb = 252, 252, 84
        self.hud = False


class SilverBar(GameObject):
    """
    The collectable silver bars.
    """

    def __init__(self):
        super().__init__()
        self.xy = 0, 0
        self.wh = (7, 13)
        self.rgb = 142, 142, 142
        self.hud = False


class DiamondRing(GameObject):
    """
    The collectable diamond rings.
    """

    def __init__(self):
        super().__init__()
        self.xy = 0, 0
        self.wh = (7, 13)
        self.rgb = 236, 236, 236
        self.hud = False


class Fire(GameObject):
    """
    The open fires.
    """

    def __init__(self):
        super().__init__()
        self.xy = 0, 0
        self.wh = (8, 14)
        self.rgb = 236, 200, 96
        self.hud = False


class MoneyBag(GameObject):
    """
    The collectable money bags.
    """

    def __init__(self):
        super().__init__()
        self.xy = 0, 0
        self.wh = (7, 14)
        self.rgb = 111, 111, 111
        self.hud = False


class LifeCount(GameObject):
    """
    The indicator for the remaining lives (HUD).
    """

    def __init__(self):
        super().__init__()
        self.xy = 0, 0
        self.wh = (1, 8)
        self.rgb = 214, 214, 214
        self.hud = True
        self.value = 0


class PlayerScore(GameObject):
    """
    The player's score display (HUD).
    """

    def __init__(self):
        super().__init__()
        self.xy = 0, 0
        self.wh = (6, 8)
        self.rgb = 214, 214, 214
        self.hud = True
        self.value = 0


class Timer(GameObject):
    """
    The 20-minute countdown (HUD).
    """

    def __init__(self):
        super().__init__()
        self.xy = 31, 22
        self.wh = (37, 8)
        self.rgb = 214, 214, 214
        self.value = 0 # in seconds
        self.hud = True


def bcd_to_decimal(bcd):
    decimal_value = 0

    # Process the most significant byte (byte 0)
    msb = bcd >> 8
    msb_units = (msb >> 4) & 0x0F  # Extract the tens place
    msb_ones = msb & 0x0F  # Extract the ones place
    decimal_value += (msb_units * 10) + msb_ones

    # Process the least significant byte (byte 1)
    lsb = bcd & 0xFF
    lsb_units = (lsb >> 4) & 0x0F  # Extract the tens place
    lsb_ones = lsb & 0x0F  # Extract the ones place
    decimal_value += (lsb_units * 10) + lsb_ones

    return decimal_value


def get_pos_rope(ram_state):
    theta_t = -0.0060223306193817605 + 0.003809046734072426 * ram_state[92]
    x_fixation_rope = 78
    y_fixation_rope = 34
    y = 116 - ram_state[18]
    # The length depends on the angle
    length_rope = abs((y - y_fixation_rope) / np.cos(theta_t))
    # This is a better approximation, but it is less understandable
    # length_rope = np.sqrt(5657.0 + -9.333333333333334 * ram_state[92])
    # correction to the formula
    # supplement_y = abs(y - (y_fixation_rope + np.cos(theta_t) * length_rope))
    if ram_state[93] <= 16:
        sign = -1
    else:
        sign = 1
    # return int(x_fixation_rope + np.sin(theta_t) * sign * length_rope + np.arctan(theta_t) * supplement_y), y
    return int(x_fixation_rope + np.sin(theta_t) * sign * length_rope), y

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
    global ram_18
    ram_18 = 10
    global prev_x
    prev_x = 78
    objects = [Player(), Wall(), Logs(), Logs(), Logs(), StairPit(), StairPit(), Pit(), Pit(), Scorpion()]  # 10
    objects.extend([Rope(), Snake(), Tarpit(), Waterhole(), Crocodile(), Crocodile(), Crocodile()])  # 7
    objects.extend([GoldenBar()])
    if hud:
        objects.extend([LifeCount(), LifeCount(), LifeCount()])  # 3
        objects.extend([PlayerScore()])
        objects.extend([Timer()])
        objects.extend([PlayerScore()])
    return objects


def _detect_objects_ram(objects, ram_state, hud=False):
    """
    For all 3 objects:
    (x, y, w, h, r, g, b)
    """
    # There are 8 treasures; Define all the classes and at the time of detection replace with GoldenBar index 
    player, = objects[:1]
    objects[:] = [None] * 24  # snapshot = pickle.load(open("/home/anurag/Desktop/HiWi_OC/OC_Atari/pit_4.pkl", "rb"))
    # env._env.env.env.ale.restoreState(snapshot)
    player.xy = ram_state[97] + 1, ram_state[105] + 72
    objects[0] = player

    # Implementing Pits,waterholes etc
    objects[5:17] = [None] * 12
    if ram_state[20] == 0:
        s = StairPit()
        s.xy = 76, 122
        objects[6] = s
        objects[5] = None

    elif ram_state[20] == 1:
        s = StairPit();
        s.xy = 76, 122
        p1 = Pit();
        p2 = Pit()
        p1.xy = 48, 122
        p2.xy = 100, 122
        objects[7] = p1;
        objects[8] = p2
        objects[5] = s
        objects[6] = None

    elif ram_state[20] == 2:
        t = Tarpit()
        t.xy = 48, 120
        objects[12] = t

    elif ram_state[20] == 4:
        w = Waterhole();
        w.xy = 48, 120
        objects[13] = w
        y1 = 122 if ram_state[46] == 255 else 119
        wh1 = (8, 6) if ram_state[46] == 255 else (8, 9)
        c1 = Crocodile();
        c1.xy = 60, y1
        c1.wh = wh1
        objects[15] = c1
        c2 = Crocodile();
        c2.xy = 76, y1
        c2.wh = wh1
        objects[16] = c2
        c3 = Crocodile();
        c3.xy = 92, y1
        c3.wh = wh1
        objects[17] = c3

    # Waterhole 
    elif ram_state[20] == 3:
        w = Waterhole()
        w.xy = 48, 120
        objects[13] = w

    # Disappearing Waterhole
    elif ram_state[20] == 7:
        w = Waterhole()
        if ram_state[32] == 1 and ram_state[33] == 3 and ram_state[34] == 15 and ram_state[35] == 127:
            w.xy = 52, 121
            w.wh = (56, 9)
        if ram_state[32] == 0 and ram_state[33] == 1 and ram_state[34] == 3 and ram_state[35] == 15:
            w.xy = 48, 120
            w.wh = (64, 10)
        if ram_state[32] == 255 and ram_state[33] == 255 and ram_state[34] == 255 and ram_state[35] == 255:
            objects[13] = None
        else:
            objects[13] = w
    # Disappearig Tarpit
    elif ram_state[20] == 6:
        t = Tarpit()
        if ram_state[32] == 1 and ram_state[33] == 3 and ram_state[34] == 15 and ram_state[35] == 127:
            t.xy = 52, 121
            t.wh = (56, 9)
        if ram_state[32] == 0 and ram_state[33] == 1 and ram_state[34] == 3 and ram_state[35] == 15:
            t.xy = 48, 120
            t.wh = (64, 10)
        if ram_state[32] == 255 and ram_state[33] == 255 and ram_state[34] == 255 and ram_state[35] == 255:
            objects[12] = None
        else:
            objects[12] = t
    elif ram_state[20] == 5:
        t = Tarpit()
        g = GoldenBar()
        g.xy = 124, 118
        if ram_state[32] == 1 and ram_state[33] == 3 and ram_state[34] == 15 and ram_state[35] == 127:
            t.xy = 52, 121
            t.wh = (56, 9)
        if ram_state[32] == 0 and ram_state[33] == 1 and ram_state[34] == 3 and ram_state[35] == 15:
            t.xy = 48, 120
            t.wh = (64, 10)
        if ram_state[32] == 255 and ram_state[33] == 255 and ram_state[34] == 255 and ram_state[35] == 255:
            objects[12] = None
        else:
            objects[12] = t

    # Implementing Scorpion
    # Remove scorpion when there is no pit
    if ram_state[29] == 0:
        s = Scorpion()
        s.xy = ram_state[99], (170 if ram_state[65] == 160 else 169)
        s.wh = (7, 8) if ram_state[65] == 160 else (8, 9)
        objects[9] = s
        objects[1] = None
    elif ram_state[29] in [1, 255]:
        w = Wall()
        w.xy = ram_state[99], 148
        objects[1] = w
        objects[9] = None
    else:
        objects[1] = None;
        objects[9] = None

    # Implementing Fire,snake and Treasures
    if ram_state[19] == 6:
        f = Fire()
    elif ram_state[19] == 7:
        f = Snake()

    elif ram_state[19] >= 8:
        if ram_state[19] % 4 == 0:
            f = MoneyBag()
        elif ram_state[19] % 4 == 1:
            f = SilverBar()
        elif ram_state[19] % 4 == 2:
            f = GoldenBar()
        elif ram_state[19] % 4 == 3:
            f = DiamondRing()
    else:
        f = None
    if f is not None:
        f.xy = 124, 118
    objects[11] = f
    if objects[15] is None:
        if ram_state[19] == 0 and ram_state[20] != 4:  # bug in pit_10.pkl
            l1 = Logs()
            l1.xy = (ram_state[98] + 1) % 160, 118
            objects[2] = l1;
            objects[3] = None;
            objects[4] = None
        elif ram_state[19] == 1:
            l1 = Logs();
            l2 = Logs()
            l1.xy = (ram_state[98] + 1) % 160, 118
            l2.xy = (ram_state[98] + 16 + 1) % 160, 118
            objects[2] = l1;
            objects[3] = l2;
            objects[4] = None
        elif ram_state[19] == 2:
            l1 = Logs();
            l2 = Logs()
            l1.xy = (ram_state[98] + 1) % 160, 118
            l2.xy = (ram_state[98] + 32 + 1) % 160, 118
            objects[2] = l1;
            objects[3] = l2;
            objects[4] = None
        elif ram_state[19] == 3:
            l1 = Logs();
            l2 = Logs();
            l3 = Logs()
            l1.xy = ram_state[98] + 1, 119
            l2.xy = (ram_state[98] + 32 + 1) % 160, 118
            l3.xy = (ram_state[98] + 64 + 1) % 160, 118
            objects[2] = l1;
            objects[3] = l2;
            objects[4] = l3
        elif ram_state[19] == 4 and ram_state[20] != 4:
            l1 = Logs()
            l1.xy = (ram_state[98] + 1) % 160, 118
            objects[2] = l1;
            objects[3] = None;
            objects[4] = None
        # elif ram_state[19]==0 and ram_state[29]
        else:
            objects[2] = None;
            objects[3] = None;
            objects[4] = None

    # Adding Rope
    # When does Rope come in? Disable for all other scenarios 
    rope_visible = False
    # to know if the rope is visible, the assembly code based itself on whether the value in the register X is greater
    # than the value in the ram_state[18] --> but we don't have a
    rope_list = [2, 3, 6, 10, 11, 12, 14, 17]
    try:
        index = rope_list.index(ram_state[20])
        rope_visible = True
    except:
        pass
    if ram_state[19] in [2,3] and ram_state[20] == 4:
        rope_visible = True
    # import ipdb; ipdb.set_trace()
    if rope_visible:
        r = Rope()
        r.xy = get_pos_rope(ram_state)
        # r.xy = 78,106
        # if r.xy == (109,96):
        #     get_pos_rope(25, 67, 4)
        objects[10] = r

    if hud:
        objects.extend([None] * 10)
        # PlayerScores related to ram_state 86 and 87
        p1 = PlayerScore()
        p1.value = _convert_number(ram_state[85])*1000 + _convert_number(ram_state[86]) * 100 + _convert_number(ram_state[87])
        size = 0
        if p1.value != 0:
            size = math.ceil(np.log10(p1.value)) * 8 - int(0.5*math.ceil(np.log10(p1.value)))
        else:
            size = 0
        p1.xy = 68 - size, 9
        p1.wh = size, p1.h
        objects[21] = p1
        # LifeCounts
        # number of lives remaining, stored as displayed pattern ($a0 = 2, $80 = 1, $00 = 0)
        if ram_state[0] == 160:
            l1 = LifeCount()
            l1.xy = 23, 22
            l2 = LifeCount()
            l2.xy = 21, 22
            objects[22] = l1;
            objects[23] = l2
        elif ram_state[0] == 128:
            l1 = LifeCount()
            l1.xy = 21, 22
            objects[22] = l1;
            objects[23] = None
        else:
            objects[22] = None;
            objects[23] = None

        # Timer
        t1 = Timer();
        t1.value = _convert_number(ram_state[88])*60+_convert_number(ram_state[89]) + ram_state[90]/60
        if ram_state[88] <= 9:
            t1.wh = 32, t1.h
            t1.xy = 37, t1.y
        objects[24] = t1
        # import ipdb; ipdb.set_trace()


def _detect_objects_pitfall_raw(info, ram_state):
    """
    returns unprocessed list with
    ball_x, ball_y, enemy_y, player_y
    """
    info["objects_list"] = ram_state[32:36]
