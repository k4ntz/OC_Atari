from .game_objects import GameObject
import numpy as np
import sys
from .utils import _color_conversion
"""
RAM extraction for the game Q*BERT. Supported modes: ram.

"""

MAX_NB_OBJECTS = {'Player': 1, 'Cube': 21, 'Disk': 2,
                  'PurpleBall': 1, 'RedBall': 1, 'GreenBall': 1, 'Coily': 1, 'Sam': 1}
MAX_NB_OBJECTS_HUD = {'Player': 1, 'Cube': 21, 'Disk': 2, 'PurpleBall': 1,
                      'RedBall': 1, 'GreenBall': 1, 'Coily': 1, 'Sam': 1, 'Score': 1, 'Lives': 1}


_cubes_cinfo = [21,               # row of 1
                52,  54,            # row of 2
                83, 85,  87,           # row of 3
                98, 100, 102, 104,       # row of 4
                1,  3,   5,   7,  9,      # row of 5
                32, 34, 36,  38,  40, 42]   # row of 6


_cubes_pos = [(68, 34), (56, 62), (84, 62), (44, 91), (68, 91), (96, 91), (32, 120), (56, 120), (84, 120), (108, 120), (20, 149),
              (44, 149), (68, 149), (96, 149), (120, 149), (8, 178), (32, 178), (56, 178), (84, 178), (108, 178), (132, 178)]

_diskposes = [(12, 138), (140, 138)]


class Player(GameObject):
    """
    The player figure: Q*bert.
    """

    def __init__(self):
        super(Player, self).__init__()
        self._xy = 78, 103
        self.wh = 8, 20
        self.rgb = 181, 83, 40
        self.hud = False


class Cube(GameObject):
    """
    The cubes.
    """

    def __init__(self):
        super().__init__()
        self._xy = (0, 0)
        self.rgb = 45, 87, 176
        self.wh = (20, 5)
        self.hud = False


class Disk(GameObject):
    """
    The lift disks at the sides.
    """

    def __init__(self):
        super().__init__()
        self._xy = (0, 0)
        self.rgb = 24, 59, 157
        self.wh = (8, 2)
        self.hud = False


class PurpleBall(GameObject):
    """
    The purple ball, which hatches Coily when reaching the bottom of the pyramid.
    """

    def __init__(self):
        super(PurpleBall, self).__init__()
        self._xy = 78, 103
        self.wh = 7, 9
        self.rgb = 146, 70, 192
        self.hud = False


class RedBall(GameObject):
    """
    The red ball.
    """

    def __init__(self):
        super(RedBall, self).__init__()
        self._xy = 78, 103
        self.wh = 7, 9
        self.rgb = 223, 183, 85
        self.hud = False


class GreenBall(GameObject):
    """
    The green ball.
    """

    def __init__(self):
        super(GreenBall, self).__init__()
        self._xy = 78, 103
        self.wh = 7, 9
        self.rgb = 50, 132, 50
        self.hud = False


class Coily(GameObject):
    """
    A class representing Coily, one of Q*bert's enemies, who hatches from the purple ball.
    """

    def __init__(self):
        super(Coily, self).__init__()
        self._xy = 78, 103
        self.wh = 8, 21
        self.rgb = 146, 70, 192
        self.hud = False


class Sam(GameObject):
    """
    A class representing Sam, one of Q*bert's enemies, who changes the cubes' color back to original.
    """

    def __init__(self):
        super(Sam, self).__init__()
        self._xy = 78, 103
        self.wh = 8, 18
        self.rgb = 50, 132, 50
        self.hud = False


class Score(GameObject):
    """
    The player score display.
    """

    def __init__(self):
        super(Score, self).__init__()
        self._xy = 34, 6
        self.wh = 37, 7
        self.rgb = 210, 210, 64
        self.hud = True


class Lives(GameObject):
    """
    The indicator for the remaining lives.
    """

    def __init__(self):
        super(Lives, self).__init__()
        self._xy = 33, 16
        self.wh = 24, 12
        self.rgb = 210, 210, 64
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
    for pos in _cubes_pos:
        cub = Cube()
        cub.xy = pos
        objects.append(cub)
    for dpos in _diskposes:
        dis = Disk()
        dis.xy = dpos
        objects.append(dis)

    global coil_prev_x
    global coil_prev_y
    coil_prev_x = 0
    coil_prev_y = 0

    global last_i
    last_i = -1
    global purple_i
    purple_i = -1
    global green_i
    green_i = -1
    global last_74
    last_74 = 0
    global last_lives
    last_lives = 2
    global last_105
    last_105 = 0
    global last_103
    last_103 = 0

    objects.extend([None] * 4)  # Coily, pruple_ball, green_ball, sam
    if hud:
        objects.extend([None] * 2)
    return objects


def _detect_objects_ram(objects, ram_state, hud=True):
    player = objects[0]
    cubes = objects[1:22]
    for cube, ccinf in zip(cubes, _cubes_cinfo):
        cube.rgb = _color_conversion[ram_state[ccinf]//2]
    if 16 < ram_state[67] < 210:
        if player is None:
            player = Player()
            objects[0] = player
        if ram_state[59] == 255:  # falling
            player.xy = player.xy[0], ram_state[33] - 52
        elif ram_state[67] < 70:
            player.xy = ram_state[43] - 3, ram_state[67] - 8
        elif ram_state[67] < 100:
            player.xy = ram_state[43] - 3, ram_state[67] - 7
        else:
            player.xy = ram_state[43] - 3, ram_state[67] - 6
    else:
        objects[0] = None
    for diskpos, rs, position in zip([22, 23], [112, 122], _diskposes):  # disks
        if ram_state[rs] == 0:
            if objects[diskpos] is not None:
                objects[diskpos] = None
        else:
            if objects[diskpos] is None:
                disk = Disk()
                objects[diskpos] = disk
                disk.xy = position
            objects[diskpos].rgb = _color_conversion[ram_state[rs]//2]

    global coil_prev_x, coil_prev_y
    coily = objects[24]
    if ram_state[39] != 255:
        if coily is None:
            coily = Coily()
            objects[24] = coily
        # The x value switches too early in the RAM, therfore we use the
        # y value changes as a trigger for the Position switch
        if coil_prev_y != ram_state[39]:
            if ram_state[56] > 8:
                coily.xy = _calc_enemy_x(
                    ram_state[71]), (ram_state[39] * 30) + 6
                coily.wh = 8, 21
            elif ram_state[56] > 6:
                coily.xy = _calc_enemy_x(
                    ram_state[71]), (ram_state[39] * 30) + 9
                coily.wh = 8, 18
            elif ram_state[56] > 3:
                coily.xy = _calc_enemy_x(
                    ram_state[71]), (ram_state[39] * 30) + 11
                coily.wh = 8, 16
            elif ram_state[56] == 1:
                coily.xy = _calc_enemy_x(
                    ram_state[71]), (ram_state[39] * 30) + 6
                coily.wh = 8, 21
            else:
                coily.xy = _calc_enemy_x(
                    ram_state[71]), (ram_state[39] * 30) + 9
                coily.wh = 8, 18
        else:  # Else the position remains the same as before
            if ram_state[56] > 8:
                coily.xy = coil_prev_x, (ram_state[39] * 30) + 6
                coily.wh = 8, 21
            elif ram_state[56] > 6:
                coily.xy = coil_prev_x, (ram_state[39] * 30) + 9
                coily.wh = 8, 18
            elif ram_state[56] > 3:
                coily.xy = coil_prev_x, (ram_state[39] * 30) + 11
                coily.wh = 8, 16
            elif ram_state[56] == 1:
                coily.xy = coil_prev_x, (ram_state[39] * 30) + 6
                coily.wh = 8, 21
            else:
                coily.xy = coil_prev_x, (ram_state[39] * 30) + 9
                coily.wh = 8, 18
        x, _ = coily.xy
        coil_prev_x = x
        coil_prev_y = ram_state[39]
    else:
        objects[24] = None
        coil_prev_x = 0
        coil_prev_y = 0

    # The object y values are not part of the RAM, instead the game
    # interprets the RAM position 75 as the highest  y position an object can be at and 79 as the lowest.
    # The x value of the object are the respective RAM values at these Positions.
    # E.g: RAM 79 has value 0: The object is on the bottem left corner of the pyramid.
    #      RAM 75 has value 6: The object is one to the right of the tip of the pyramid (second row right platform)
    # With each step an object takes they will go down one row and the next RAM position in line determins their x
    # and y position.
    # The big problem with this is that the RAM values stay the same even if there is no object on the specified
    # platform anymore.
    # (You might be able to find a RAM value carrying information when the next step is taken by an object)

    global last_i
    global purple_i
    global green_i
    global last_74
    global last_105
    global last_103
    global last_lives

    purple_ball, green_ball, sam = objects[25], objects[26], objects[27]

    # if ram_state[59] == 255:
    if last_lives != ram_state[8]:
        green_i = -1
        purple_i = -1
        last_i = -1
        last_lives = ram_state[8]
        last_74 = ram_state[74]
        objects[25], objects[26], objects[27] = None, None, None
    elif ram_state[74]:
        if last_74 != ram_state[74]:
            last_74 = ram_state[74]
            if last_i >= 0:
                last_i = last_i + 1
            if purple_i >= 0:
                purple_i = purple_i + 1
            if green_i >= 0:
                green_i = green_i + 1

        if last_103 != ram_state[103]:
            if ram_state[103] == 17:
                green_i = 0
            last_103 = ram_state[103]
        elif green_i > 4:
            green_i = -1
        if green_i >= 0 and green_i < 5:
            if green_ball is None:
                green_ball = GreenBall()
                objects[26] = green_ball
            if player is not None:
                b_x, b_y = _calc_enemy_x(
                    ram_state[75 + green_i]), ((green_i + 1) * 30) + 7 - green_i
                p_x, p_y = player.xy
                if (b_x - p_x) < 9 and (b_x - p_x) > -9 and (b_y - p_y) < 9 and (b_y - p_y) > -9:
                    objects[27] = None
                    green_i = -1
            if ram_state[56] < 7:
                green_ball.xy = _calc_enemy_x(
                    ram_state[75 + green_i]) + 1, ((green_i + 1) * 30) + 23 - green_i
                green_ball.wh = 7, 6
            else:
                green_ball.xy = _calc_enemy_x(
                    ram_state[75 + green_i]) + 1, ((green_i + 1) * 30) + 9 - green_i
                green_ball.wh = 7, 9
        else:
            objects[26] = None

        if ram_state[119] != 0:
            objects[25] = None
            purple_i = -1
        elif ram_state[119] == 0 and purple_i < 0 and objects[24] is None:
            purple_i = 0
        elif purple_i > 4:
            purple_i = -1
        if purple_i >= 0 and purple_i < 5:
            if green_i != purple_i:
                if purple_ball is None:
                    purple_ball = PurpleBall()
                    objects[25] = purple_ball
                if ram_state[56] < 7:
                    purple_ball.xy = _calc_enemy_x(
                        ram_state[75 + purple_i]) + 1, ((purple_i + 1) * 30) + 23 - purple_i
                    purple_ball.wh = 7, 6
                else:
                    purple_ball.xy = _calc_enemy_x(
                        ram_state[75 + purple_i]) + 1, ((purple_i + 1) * 30) + 9 - purple_i
                    purple_ball.wh = 7, 9
            else:
                purple_i = -1
        else:
            objects[25] = None

        if last_105 != ram_state[105]:
            if ram_state[105] == 6:
                last_i = 0
            last_105 = ram_state[105]
        if last_i >= 0 and last_i < 5:
            if sam is None:
                sam = Sam()
                objects[27] = sam
            if player is not None:
                s_x, s_y = _calc_enemy_x(
                    ram_state[75 + last_i]), ((last_i + 1) * 30) + 12 - last_i
                p_x, p_y = player.xy
                if (s_x - p_x) < 7 and (s_x - p_x) > -7 and (s_y - p_y) < 7 and (s_y - p_y) > -7:
                    objects[27] = None
                    last_i = -1
            sam.xy = _calc_enemy_x(
                ram_state[75 + last_i]), ((last_i + 1) * 30) + 12 - last_i
        else:
            objects[27] = None
        if last_i > 4:
            last_i = -1

    if hud:
        score, lives = objects[28], objects[29]
        score = Score()
        objects[28] = score
        if ram_state[8] == 2:
            lives = Lives()
        elif ram_state[8] == 1:
            lives = Lives()
            lives.wh = 16, 12
        elif ram_state[8] == 0:
            lives = Lives()
            lives.wh = 8, 12
        else:
            lives = None
        objects[29] = lives

    return objects


def _detect_objects_qbert_raw(info, ram_state):
    player = ram_state[43], ram_state[67]
    enemy = ram_state[47], ram_state[46]

    # 69 105
    # ram[56] timer
    # ram_state[126] maybe sprite 171 = jump and 201 normal
    # ram[41]: 0 ball, 7 coily
    # ram[75:80]: enemy spawn

    info["ram-slice"] = player + enemy


def _calc_enemy_x(value):
    """
    Calculates the enemy x position from the RAM value
    """
    res = 0
    for i in range(value + 1):
        if i <= 1:
            res = res + 13
        elif i == 6:
            res = res + 16
        else:
            res = res + 12
    return res


# def _calc_enemy_pos(slice):
#     """
#     Converts a RAM slice of 5 into the enemy positions
#     """
#     global last_i

#     x = None
#     y = None
#     typ = 0

#     res = []

#     if last_i is not None and last_i < 4 and slice[last_i + 1] + 1 == slice[last_i]:
#         xi = _calc_enemy_x(slice[last_i + 1])
#         yi = ((last_i + 2) * 30) + 12
#         last_i += 1
#         res.append([(xi, yi), typ])

#     for i in range(5):
#         if slice[i] == 0:
#             break
#         if slice[i+1] == 7:
#             typ = 7
#         x = _calc_enemy_x(slice[i])
#         y = ((i + 1) * 30) + 12
#         last_i = i
#         if i < 4 and slice[i] != slice[i] + 1:
#             break

#     res.append([(x, y), typ])

#     return res
