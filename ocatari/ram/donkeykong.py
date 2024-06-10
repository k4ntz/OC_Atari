from typing import Type, Sequence, Dict

from .game_objects import GameObject, ValueObject, Orientation
from ._helper_methods import _convert_number
import sys

"""
RAM extraction for the game DONKEYKONG. Supported modes: ram.

"""

MAX_ESSENTIAL_OBJECTS = {
    'Player': 1,
}

MAX_OPTIONAL_OBJECTS = {
    'Score': 1,
}

MAX_ALL_OBJECTS = dict(MAX_ESSENTIAL_OBJECTS.items()|MAX_OPTIONAL_OBJECTS.items())

obj_tracker = {}



class Player(GameObject):
    """
    The player figure: Mother Kangaroo.
    """

    def __init__(self):
        super(Player, self).__init__()
        self._xy = 43, 172
        self.wh = 8, 17
        self.rgb = 200, 72, 72
        self.hud = False
        self.crashed = False


class Girlfriend(GameObject):
    """
    Mario's Girlfriend.
    """

    def __init__(self):
        super(Girlfriend, self).__init__()
        self._xy = 63, 18
        self.wh = 8, 16
        self.rgb = 84, 160, 197
        self.hud = False


class Barrel(GameObject):
    """
    The Monkey monkeys.
    """

    def __init__(self):
        super(Barrel, self).__init__()
        super().__init__()
        self._xy = 0, 0
        self.wh = 8, 8
        self.rgb = 236, 200, 96
        self.hud = False


class Hammer(GameObject):
    """
    The collectable fruits.
    """

    def __init__(self):
        super(Hammer, self).__init__()
        self._xy = 39, 68
        self.wh = 4, 7
        self.rgb = 236, 200, 96
        self.hud = False


class Ladder(GameObject):
    """
    The ladders.
    """

    def __init__(self, x=0, y=0):
        super(Ladder, self).__init__()
        self._xy = x, y
        self._prev_xy = x, y
        self.wh = 4, 17
        self.rgb = 181, 108, 224
        self.hud = False


class Platform(GameObject):
    """
    The platforms.
    """

    def __init__(self, x=0, y=0, w=8, h=4):
        super(Platform, self).__init__()
        self._xy = x, y
        self._prev_xy = x, y
        self.wh = w, h
        self.rgb = 162, 98, 33
        self.hud = False


class DonkeyKong(GameObject):
    """
    The donkey kong enemy.
    """

    def __init__(self):
        super(DonkeyKong, self).__init__()
        self._xy = 34, 15
        self.wh = 16, 19
        self.rgb = 181, 83, 40
        self.hud = False


class Score(ValueObject):
    """
    The player's score display (HUD).
    """

    def __init__(self):
        super(Score, self).__init__()
        self._xy = 72, 7
        self.wh = 30, 7
        self.rgb = 158, 208, 201
        self.hud = True
        self.value = 0


class Life(GameObject):
    """
    The player's remaining lives (HUD).
    """

    def __init__(self):
        super(Life, self).__init__()
        self._xy = 116, 23
        self.wh = 12, 8
        self.rgb = 181, 108, 224
        self.hud = True
        self.value = 2


# class Time(ValueObject):
#     """
#     The time indicator (HUD).
#     """

#     def __init__(self):
#         super(Time, self).__init__()
#         self._xy = 80, 191
#         self.wh = 15, 5
#         self.rgb = 160, 171, 79
#         self.hud = False
#         self.value = 20


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
        return fromdict(MAX_ALL_OBJECTS)
    return fromdict(MAX_ESSENTIAL_OBJECTS)


# def _init_all_objects(hud=False):
#     objects = [Player()]
#     # for ppxy in pps:
#     #     objects.append(PowerPill(*ppxy))
#     if hud:
#         objects.extend([Life(), Score()])
#     return objects


ladders = [(108, 176), (48, 148), (80, 148), (88, 120), (108, 120),
           (48, 92), (68, 92), (108, 64), (76, 40), (32, 40)]
def _init_objects_ram(hud=True):
    """
    (Re)Initialize the objects
    """
    # objects[Time][0] = Time()
    objects = [Player(), DonkeyKong(), Girlfriend(), Hammer()] + [None] * 4 + \
        [Ladder(*xy) for xy in ladders]
    if hud:
        objects.extend([Life(), Score()])
    return objects
    # manage_platforms(0, init_obj)
    # global prev_level
    # prev_level = 0
    # if hud:
    #     init_obj.extend([Score()])
    # return init_obj

def _detect_objects_ram(objects, ram_state, hud=True):
    player = objects[0]
    if 1 < ram_state[11] < 255: # jumping
        player.xy = ram_state[19]-4, ram_state[27]+24
        player.wh = 8, 15
    else:
        player.xy = ram_state[19]-4, ram_state[27]+22
        player.wh = 8, 17
    hammer = objects[3]
    hammer_used = ram_state[21] == 112 and ram_state[23] == 112
    if hammer_used:
        if hammer is not None:
            objects[3] = None
    else:
        if hammer is None:
            hammer = Hammer()
            objects[3] = hammer
        hammer.xy = ram_state[28]-6, ram_state[23]-73

    barrels = objects[4:8]
    for i, bar in enumerate(barrels):
        if ram_state[0+i] != 0:
            if bar is None:
                bar = Barrel()
                objects[4+i] = bar
            bar.xy = ram_state[65+i]-4, ram_state[0+i]+40
        else:
            if bar is not None:
                objects[4+i] = None
    if hud:
        score = objects[-1]
        score.value = ram_state[36]
        lives = objects[-2]
        nb_lives = ram_state[35]
        if lives is not None and nb_lives != lives.value:
            if nb_lives == 0:
                objects[-2] = None
                return
            else:
                if lives is None:
                    lives = Life()
                    objects[-2] = lives
                lives.value = nb_lives
                lives.xy = 108 + 8 * (3 - nb_lives), 23
                lives.wh = 4 + 8 * (nb_lives-1), 8


# def manage_platforms(current_lvl_val, _):
#     objects[Platform][:2] = [
#         Platform(16, 172, w=128),
#         Platform(16, 28, w=128)
#     ]

#     # There is a total of 3 levels
#     if current_lvl_val == 0:
#         objects[Ladder] = [
#             Ladder(132, 132),
#             Ladder(20, 84),
#             Ladder(132, 36),
#             None,
#             None,
#             None,
#         ]

#         objects[Platform][2:4] = [
#             Platform(16, 76, w=128),
#             Platform(16, 124, w=128),
#         ]

#         for i in range(4, MAX_ESSENTIAL_OBJECTS["Platform"]):
#             _remove_object(Platform, idx=i)

#     elif current_lvl_val == 1:
#         objects[Ladder] = [
#             Ladder(120, 132, h=4),
#             Ladder(24, 116, h=4),
#             Ladder(128, 36, h=4),
#             None,
#             None,
#             None,
#         ]

#         objects[Platform][2:18] = [
#             Platform(16, 124, w=28), Platform(52, 124, w=92),
#             Platform(16, 76, w=60), Platform(84, 76, w=60),
#             Platform(28, 164, w=24), Platform(112, 84, w=24),
#             Platform(120, 44, w=24), Platform(48, 156, w=32),
#             Platform(76, 148, w=32), Platform(104, 140, w=32),
#             Platform(16, 108, w=32), Platform(56, 100, w=20),
#             Platform(84, 92, w=20), Platform(64, 60, w=20),
#             Platform(92, 52, w=20), Platform(28, 68, w=28)
#         ]
#         objects[Platform][18:] = [None, None]

#     else:  # current_lvl_val == 2
#         objects[Ladder] = [
#             Ladder(20, 36, h=28),
#             Ladder(20, 148, h=4),
#             Ladder(36, 116, h=20),
#             Ladder(104, 36, h=20),
#             Ladder(120, 68, h=4),
#             Ladder(132, 84, h=4)
#         ]

#         objects[Platform][2:] = [
#             Platform(88, 140, w=16), Platform(64, 148, w=16), Platform(100, 116, w=16),
#             Platform(48, 100, w=16), Platform(76, 52, w=16), Platform(80, 36, w=16),
#             Platform(104, 132, w=20), Platform(84, 156, w=20), Platform(124, 124, w=20),
#             Platform(52, 84, w=20), Platform(108, 164, w=36), Platform(16, 108, w=80),
#             Platform(16, 92, w=28), Platform(76, 92, w=68), Platform(16, 140, w=32),
#             Platform(96, 60, w=36), Platform(100, 76, w=44), Platform(60, 44, w=12)
#         ]
