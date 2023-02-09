from .game_objects import GameObject
from ._helper_methods import bitfield_to_number, number_to_bitfield
import math


class CentipedeSegment(GameObject):
    def __init__(self):
        super(CentipedeSegment, self).__init__()
        self._xy = 0, 0
        self.wh = 3, 6
        self.rgb = 184, 70, 162
        self.hud = False


class Player(GameObject):
    def __init__(self):
        super(Player, self).__init__()
        self._xy = 0, 0
        self.wh = 4, 8
        self.rgb = 181, 83, 40
        self.hud = False


class Projectile(GameObject):
    def __init__(self):
        super(Projectile, self).__init__()
        self._xy = 0, 0
        self.wh = 1, 8
        self.rgb = 181, 83, 40
        self.hud = False


class Wall(GameObject):
    def __init__(self):
        super(Wall, self).__init__()
        self._xy = 0, 0
        self.wh = 4, 3
        self.rgb = 181, 83, 40
        self.hud = False


class Bug(GameObject):
    def __init__(self):
        super(Bug, self).__init__()
        self._xy = 0, 0
        self.wh = 8, 6
        self.rgb = 146, 70, 192
        self.hud = False


class Crab(GameObject):  # i have no clue what it is supposed to be ...
    def __init__(self):     # some ball thingy with legs
        super(Crab, self).__init__()
        self._xy = 0, 0
        self.wh = 4, 6
        self.rgb = 45, 50, 185
        self.hud = False


class Ghost(GameObject):
    def __init__(self):
        super(Ghost, self).__init__()
        self._xy = 0, 0
        self.wh = 8, 6
        self.rgb = 84, 138, 210
        self.hud = False


class Score(GameObject):
    def __init__(self):
        super(Score, self).__init__()
        self._xy = 96, 7
        self.wh = 7, 7
        self.rgb = 188, 144, 252
        self.hud = True


class Ground(GameObject):
    def __init__(self):
        super(Ground, self).__init__()
        self._xy = 96, 7
        self.wh = 5, 9
        self.rgb = 110, 156, 66
        self.hud = True


class Life(GameObject):
    def __init__(self):
        super(Life, self).__init__()
        self._xy = 0, 0
        self.wh = 3, 5
        self.rgb = 188, 144, 252
        self.hud = True


def _column_to_y(column):
    """
    converts the given column number to a y coordinate
    """
    pad = 9
    return 5 + column * pad


def _number_lowpass(number):
    """
    makes sure the given number is lower than 19 (there are only 19 columns)
    if the given number is higher than 19 this function ignores the more significant bits
    this is important because centipede sometimes stores additional information in the same ram field...
    for example least significant 4 bits are for column and highest is part of score etc.
    """
    if number < 20:
        return number
    bitfield = number_to_bitfield(number)
    for i in range(3):
        bitfield[i] = 0
    ret = bitfield_to_number(bitfield)
    if ret < 20:
        return ret
    bitfield = number_to_bitfield(ret)
    bitfield[4] = 0
    bitfield[5] = 0
    return bitfield_to_number(bitfield)


def _create_walls_from_bitfield(bitfield, offset_x, offset_y, switch=False):
    """
    takes an 8-bit bitfield and returns a list of wall objects with the given offset

    FE bitfield=11111111 would return a list of 8 wall objects all with equal spacing in x direction.
     the first wall has xy = offset_xy

    switch is important in centipede because centipede swaps between reading bits from left to right to
     reading bits from right to left
    """
    ret = []
    pad = 8
    swap = switch
    for i in range(len(bitfield)):
        if bitfield[i] == 1:
            index = int(i/2)
            if swap:
                index = 7 - index
            w = Wall()
            w.xy = offset_x + index * pad, offset_y
            ret.append(w)
        swap = not swap
    return ret


def _create_score_objects(score):
    """
    takes a number and returns a list of score objects with equal spacing at the correct position

    FE score=10 would return a list of 2 score objects
    """
    ret = []
    amount = 0
    if score > 0:
        amount = int(math.log10(score)) + 1
    if amount < 2:
        amount = 2
    basex = 140
    pad = 8
    for i in range(amount):
        s = Score()
        s.xy = basex - i * pad, 187
        ret.append(s)
    return ret


def _create_life_objects(life):
    """
    takes a number and returns a list of correctly positioned life objects (len=number)
    """
    ret = []
    basex = 17
    pad = 8
    for i in range(life):
        s = Life()
        s.xy = basex + i * pad, 188
        ret.append(s)
    return ret


def _init_objects_centipede_ram(hud=False):
    """
    (Re)Initialize the objects
    """
    objects = [Player(), Projectile()]  # , Bug(), Ghost(), Crab()
    for i in range(9):
        objects.append(CentipedeSegment())
    if hud:
        # objects.append(Score())
        objects.extend(_create_score_objects(0))
        objects.extend(_create_life_objects(2))

    return objects


prev_centipede_x = [0, 0, 0, 0, 0, 0, 0, 0, 0]


def _detect_objects_centipede_revised(objects, ram_state, hud=False):
    player, projectile = objects[:2]  # bug, ghost, crab1, crab2, crab3

    player.xy = 16 + ram_state[111], int(ram_state[113] * 3.08)
    projectile.xy = 16 + ram_state[110], _number_lowpass(ram_state[112]) * 9 - 8

    objects.clear()
    objects.extend([player, projectile])

    small_bugs = [Bug(), Ghost(), Crab()]
    for i in range(3):
        if ram_state[124 - 2 * i] != 255:
            b = small_bugs[i]
            b.xy = 16 + ram_state[123 - 2 * i], _column_to_y(19 - _number_lowpass(ram_state[124 - 2 * i]))
            objects.append(b)

    for i in range(9):
        x = 17 + ram_state[100 + i]
        dx = prev_centipede_x[i] - x
        if dx != 0:
            centipede_segment = CentipedeSegment()
            centipede_segment.xy = x, _column_to_y(19 - _number_lowpass(ram_state[91 + i]))
            prev_centipede_x[i] = centipede_segment.x
            objects.append(centipede_segment)

    for i in range(19):   # way too complicated
        offset_y = _column_to_y(i) + 2
        for u in range(2):
            offset_x = 16 + u * 64
            swap = i % 2 == 0
            if swap:
                offset_x += 4
            objects.extend(_create_walls_from_bitfield(number_to_bitfield(ram_state[45 + i * 2 + u]),
                                                       offset_x, offset_y, swap))
    level_and_life_bitfield = number_to_bitfield(ram_state[109])
    if hud:
        score = ram_state[118] + ram_state[117] * 100 + ram_state[116] * 10000
        objects.extend(_create_score_objects(score))
        life = level_and_life_bitfield[1] * 4 + level_and_life_bitfield[2] * 2 + level_and_life_bitfield[3]
        objects.extend(_create_life_objects(life))


def _detect_objects_centipede_raw(info, ram_state):
    # info["blocks"] = ram_state[45:83]  # this is a bitmapt [111...111] means every block is currently on the screen
    # info["bug_x"] = ram_state[123]
    # info["bug_y_column"] = ram_state[124]  # 0 - 19  0 is lowest column 19 is highest
    # info["ghost_x"] = ram_state[121]
    # info["ghost_y_column"] = ram_state[122]  # 0 - 19  0 is lowest column 19 is highest
    # info["crab_x"] = ram_state[119]
    # info["crab_y_column"] = ram_state[120]  # 0 - 19  0 is lowest column 19 is highest
    # info["player_x"] = ram_state[111]
    # info["player_y"] = ram_state[113]
    # info["projectile_x"] = ram_state[110]
    # info["projectile_y"] = ram_state[112]   # 4 -19 19 is lowest column 0 is highest
    # info["centipede_y_column"] = ram_state[91:100]  # 0 - 19  0 is lowest column 19 is highest
    # # 91 is the entire centipede 99 is only the front, 98 is the two frontmost pieces etc.
    # info["centipede_x"] = ram_state[100:109]
    # info["centipede_length"] = ram_state[114]  # 0 - 8
    # level_and_life_bitfield = number_to_bitfield(ram_state[109])
    # info["life"] = level_and_life_bitfield[1] * 4 + level_and_life_bitfield[2] * 2 + level_and_life_bitfield[3]
    # level = bitfield_to_number(level_and_life_bitfield[4:])
    # info["level"] = level
    # info["ghost_enabled"] = level >= 3
    # info["score"] = ram_state[118] + ram_state[117] * 100 + ram_state[116] * 10000

    info["relavant_ram_info"] = ram_state[45:83] + ram_state[91:115] + ram_state[116:125]
