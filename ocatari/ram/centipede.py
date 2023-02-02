from .game_objects import GameObject
from ._helper_methods import bitfield_to_number, number_to_bitfield, _convert_number
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


class Score(GameObject):
    def __init__(self):
        super(Score, self).__init__()
        self._xy = 96, 7
        self.wh = 5, 9
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


def _column_to_y(column): #returns the y cord of given column
    pad = 9
    return 5 + column * pad


def _number_lowpass(number):  # returns a number from 0-19
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


def _create_walls_from_bitfield(bitmap, offset_x, offset_y, switch=False):
    ret = []
    pad = 8
    swap = switch
    for i in range(len(bitmap)):
        if bitmap[i] == 1:
            index = int(i/2)
            if swap:
                index = 7 - index
            w = Wall()
            w.xy = offset_x + index * pad, offset_y
            ret.append(w)
        swap = not swap
    return ret


def _init_objects_centipede_ram(hud=False):
    """
    (Re)Initialize the objects
    """
    objects = [Player(), Projectile(), Bug()]
    for i in range(9):
        objects.append(CentipedeSegment())
    if hud:
        # objects.append(Score())
        base_x = 17
        for i in range(2):
            live = Life()
            live.xy = base_x, 188
            objects.append(live)
            base_x += 8

    return objects


def _detect_objects_centipede_revised(objects, ram_state, hud=False):
    player, projectile, bug = objects[:3]
    centipede = objects[3:13]
    walls = objects[13:]

    player.xy = 16 + ram_state[111], int(ram_state[113] * 3.08)
    projectile.xy = 16 + ram_state[110], _number_lowpass(ram_state[112]) * 9 - 8
    if ram_state[124] == 255:
        bug.visible = False
    else:
        bug.visible = True
    bug.xy = 16 + ram_state[123], _column_to_y(19 - _number_lowpass(ram_state[124]))

    for i in range(9):
        centipede[i].xy = 17 + ram_state[100+i], _column_to_y(19 - _number_lowpass(ram_state[91+i]))
        if centipede[i].dx == 0:
            centipede[i].visible = False
        else:
            centipede[i].visible = True

    objects.clear()
    objects.extend([player, projectile, bug])
    objects.extend(centipede)

    for i in range(19):   # way too complicated
        offset_y = _column_to_y(i) + 2
        for u in range(2):
            offset_x = 16 + u * 64
            swap = i % 2 == 0
            if swap:
                offset_x += 4
            objects.extend(_create_walls_from_bitfield(number_to_bitfield(ram_state[45 + i * 2 + u]), offset_x, offset_y, swap))


def _detect_objects_centipede_raw(info, ram_state):
    info["blocks"] = ram_state[45:83]  # this is a bitmapt [111...111] means every block is currently on the screen
    info["bug_x"] = ram_state[123]
    info["bug_y_column"] = ram_state[124]  # 0 - 19  0 is lowest column 19 is highest
    info["player_x"] = ram_state[111]
    info["player_y"] = ram_state[113]
    info["projectile_x"] = ram_state[110]
    info["projectile_y"] = ram_state[112]   #4 -19 19 is lowest column 0 is highest
    info["centipede_y_column"] = ram_state[91:100] # 0 - 19  0 is lowest column 19 is highest
    # 91 is the entire centipede 99 is only the front, 98 is the two frontmost pieces etc.
    info["centipede_x"] = ram_state[100:109]
    info["centipede_length"] = ram_state[114]  # 0 - 8
    level_and_life_bitfield = number_to_bitfield(109)
    info["life"] = level_and_life_bitfield[1] * 4 + level_and_life_bitfield[2] * 2 + level_and_life_bitfield[3]
    level = bitfield_to_number(level_and_life_bitfield[4:])
    info["level"] = level
    info["ghost_enabled"] = level >= 3

