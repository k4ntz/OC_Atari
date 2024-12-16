from typing import Type, Sequence, Dict

from .game_objects import GameObject, ValueObject, NoObject
from ._helper_methods import _convert_number
import sys

"""
RAM extraction for the game DONKEYKONG. Supported modes: ram.
"""

MAX_NB_OBJECTS = {
    'Player': 1, 'DonkeyKong': 1, 'Girlfriend': 1, 'Hammer': 1, 'Barrel': 4, 'Ladder': 10
}

MAX_NB_OBJECTS_HUD = {
    'Player': 1, 'DonkeyKong': 1, 'Girlfriend': 1, 'Hammer': 1, 'Barrel': 4, 'Ladder': 10,
    'Score': 1, 'Life': 1,
}

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


ladders = [(108, 176), (48, 148), (80, 148), (88, 120), (108, 120),
           (48, 92), (68, 92), (108, 64), (76, 40), (32, 40)]


def _init_objects_ram(hud=True):
    """
    (Re)Initialize the objects
    """
    objects = [Player(), DonkeyKong(), Girlfriend(), Hammer()] + \
        [NoObject()] * 4 + [Ladder(*xy) for xy in ladders]
    if hud:
        objects.extend([Life(), Score()])
    return objects


def _detect_objects_ram(objects, ram_state, hud=True):
    player = objects[0]
    if 1 < ram_state[11] < 255:  # jumping
        player.xy = ram_state[19]-4, ram_state[27]+24
        player.wh = 8, 15
    else:
        player.xy = ram_state[19]-4, ram_state[27]+22
        player.wh = 8, 17

    hammer_used = ram_state[21] == 112 and ram_state[23] == 112
    hammer = objects[3]
    if hammer_used:
        if not isinstance(hammer, NoObject):
            objects[3] = NoObject()
    else:
        if isinstance(hammer, NoObject):
            hammer = Hammer()
            hammer.xy = ram_state[28]-6, ram_state[23]-73
            objects[3] = hammer

    barrels = objects[4:8]
    for i, bar in enumerate(barrels):
        if ram_state[0+i] != 0:
            if isinstance(bar, NoObject):
                bar = Barrel()
            bar.xy = ram_state[65+i]-4, ram_state[0+i]+40
            objects[4+i] = bar
        else:
            if not isinstance(bar, NoObject):
                objects[4+i] = NoObject()

    if hud:
        score = objects[-1]
        score.value = ram_state[36]
        lives = objects[-2]
        nb_lives = ram_state[35]
        if not isinstance(lives, NoObject) and nb_lives != lives.value:
            if nb_lives == 0:
                objects[-2] = NoObject()
                return
            else:
                if isinstance(lives, NoObject):
                    lives = Life()
                    objects[-2] = lives
                lives.value = nb_lives
                lives.xy = 108 + 8 * (3 - nb_lives), 23
                lives.wh = 4 + 8 * (nb_lives-1), 8
