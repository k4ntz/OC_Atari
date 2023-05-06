from .game_objects import GameObject
import numpy as np
import sys

"""
RAM extraction for the game Q*BERT. Supported modes: raw, revised.

"""

MAX_NB_OBJECTS =  {'Player': 1, 'PurpleBall': 1, 'RedBall': 1, 'GreenBall': 1, 'Coily': 1, 'Sam': 1, 'FlyingDiscs': 1}
MAX_NB_OBJECTS_HUD = {'Player': 1, 'PurpleBall': 1, 'RedBall': 1, 'GreenBall': 1, 'Coily': 1, 'Sam': 1, 'FlyingDiscs': 1, 'Score': 1, 'Lives': 1}


class Player(GameObject):
    def __init__(self):
        super(Player, self).__init__()
        self._xy = 78, 103
        self.wh = 8, 20
        self.rgb = 181, 83, 40
        self.hud = False


class PurpleBall(GameObject):
    def __init__(self):
        super(PurpleBall, self).__init__()
        self._xy = 78, 103
        self.wh = 8, 24
        self.rgb = 146, 70, 192
        self.hud = False


class RedBall(GameObject):
    def __init__(self):
        super(RedBall, self).__init__()
        self._xy = 78, 103
        self.wh = 8, 24
        self.rgb = 223, 183, 85
        self.hud = False


class GreenBall(GameObject):
    def __init__(self):
        super(GreenBall, self).__init__()
        self._xy = 78, 103
        self.wh = 8, 24
        self.rgb = 50, 132, 50
        self.hud = False


# The purple snake that hatches from the purple ball
class Coily(GameObject):
    def __init__(self):
        super(Coily, self).__init__()
        self._xy = 78, 103
        self.wh = 8, 24
        self.rgb = 146, 70, 192
        self.hud = False


# The green Object appearing
class Sam(GameObject):
    def __init__(self):
        super(Sam, self).__init__()
        self._xy = 78, 103
        self.wh = 8, 18
        self.rgb = 50, 132, 50
        self.hud = False


class FlyingDiscs(GameObject):
    def __init__(self):
        super(FlyingDiscs, self).__init__()
        self._xy = 78, 103
        self.wh = 8, 24
        self.rgb = 223, 183, 85
        self.hud = False


class Score(GameObject):
    def __init__(self):
        super(Score, self).__init__()
        self._xy = 34, 6
        self.wh = 37, 7
        self.rgb = 210, 210, 64
        self.hud = False


class Lives(GameObject):
    def __init__(self):
        super(Lives, self).__init__()
        self._xy = 33, 16
        self.wh = 24, 12
        self.rgb = 210, 210, 64
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

def _init_objects_qbert_ram(hud=True):
    """
    (Re)Initialize the objects
    """

    objects = [Player()]

    global coil_prev_x
    global coil_prev_y
    coil_prev_x = 0
    coil_prev_y = 0

    global last_i
    last_i = -1
    global purple_i
    purple_i = -1
    global last_74
    last_74 = 0

    return objects


def _detect_objects_qbert_revised(objects, ram_state, hud=True):
    objects.clear()

    if ram_state[67] != 0 and ram_state[43] != 0 and ram_state[67] < 190:
        player = Player()
        if ram_state[67] < 70:
            player.xy = ram_state[43] - 3, ram_state[67] - 8
        elif ram_state[67] < 100:
            player.xy = ram_state[43] - 3, ram_state[67] - 7
        else:
            player.xy = ram_state[43] - 3, ram_state[67] - 6
        objects.append(player)

    global coil_prev_x, coil_prev_y
    if ram_state[39] != 255:
        coily = Coily()
        # The x value switches too early in the RAM, therfore we use the
        # y value changes as a trigger for the Position switch
        if coil_prev_y != ram_state[39]:
            coily.xy = _calc_enemy_x(ram_state[71]), (ram_state[39] * 30) + 3
        else:  # Else the position remains the same as before
            coily.xy = coil_prev_x, (ram_state[39] * 30) + 3
        coil_prev_x = coily.x
        coil_prev_y = ram_state[39]
        objects.append(coily)

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
    # res = _calc_enemy_pos(ram_state[75:80])
    # x, y = None, None  # res[0][0]
    # if not (x is None or y is None):
    #     for i in range(len(res)):
    #         x, y = res[i][0]
    #         typ = res[i][1]
    #         if typ == 0:
    #             obj = Sam()
    #         elif typ == 7:
    #             obj = PurpleBall()
    #         obj.xy = x, y
    #         objects.append(obj)
    global last_i
    global last_74
    global purple_i

    if ram_state[74]:
        if last_74 != ram_state[74]:
            last_74 = ram_state[74]
            if last_i >= 0:
                last_i = last_i + 1
            if purple_i >= 0:
                purple_i = purple_i + 1
        if ram_state[39] == 255:
            if ram_state[76] == 7 and purple_i < 0:
                purple_i = 0
            if purple_i >= 0 and purple_i < 5:
                ball = PurpleBall()
                ball.xy = _calc_enemy_x(ram_state[75 + purple_i]), ((purple_i + 1) * 30) + 12 - purple_i
                objects.append(ball)
        elif purple_i > 4:
            purple_i = -1
        if ram_state[105] == 6:
            last_i = 0
        if last_i >= 0 and last_i < 5:
            obj = Sam()
            obj.xy = _calc_enemy_x(ram_state[75 + last_i]), ((last_i + 1) * 30) + 12 - last_i
            objects.append(obj)
        elif last_i > 4:
            last_i = -1
        

    if hud:
        objects.append(Score())
        objects.append(Lives())

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
