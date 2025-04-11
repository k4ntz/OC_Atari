from .game_objects import GameObject, ValueObject, NoObject
from ._helper_methods import _convert_number
import sys

MAX_NB_OBJECTS = {"Player": 1, "Player_Shot": 1, "Enemy_Green": 8, "Enemy_Green_Shot": 2, "Enemy_Black": 8, "Enemy_Black_Shot": 2,
                  "Enemy_Yellow": 8, "Enemy_Yellow_Shot": 2, "Enemy_Blue": 8, "Enemy_Blue_Shot": 2, "Enemy_Orange": 8, "Enemy_Orange_Shot": 2}
MAX_NB_OBJECTS_HUD = {"Player": 1, "Player_Shot": 1, "Enemy_Green": 8, "Enemy_Green_Shot": 2, "Enemy_Black": 8, "Enemy_Black_Shot": 2,
                  "Enemy_Yellow": 8, "Enemy_Yellow_Shot": 2, "Enemy_Blue": 8, "Enemy_Blue_Shot": 2, "Enemy_Orange": 8, "Enemy_Orange_Shot": 2, "Score": 1, "Life": 4}  # 'Score': 1}


class Player(GameObject):
    def __init__(self):
        super(Player, self).__init__()
        self._xy = 76, 100
        self.wh = (8, 9)
        self.rgb = 84, 92, 214
        self.hud = False


class Player_Shot(GameObject):
    def __init__(self):
        super(Player_Shot, self).__init__()
        self._xy = 0, 160
        self.wh = (1, 2)
        self.rgb = 84, 92, 214
        self.hud = False


class Enemy_Green(GameObject):
    def __init__(self):
        super(Enemy_Green, self).__init__()
        self._xy = 0, 160
        self.wh = (8, 7)
        self.rgb = 135, 183, 84
        self.hud = False


class Enemy_Green_Shot(GameObject):
    def __init__(self):
        super(Enemy_Green_Shot, self).__init__()
        self._xy = 0, 160
        self.wh = (1, 2)
        self.rgb = 135, 183, 84
        self.hud = False


class Enemy_Black(GameObject):
    def __init__(self):
        super(Enemy_Black, self).__init__()
        self._xy = 0, 160
        self.wh = (8, 7)
        self.rgb = 1, 1, 1
        self.hud = False


class Enemy_Black_Shot(GameObject):
    def __init__(self):
        super(Enemy_Black_Shot, self).__init__()
        self._xy = 0, 160
        self.wh = (1, 2)
        self.rgb = 1, 1, 1
        self.hud = False


class Enemy_Yellow(GameObject):
    def __init__(self):
        super(Enemy_Yellow, self).__init__()
        self._xy = 0, 160
        self.wh = (8, 7)
        self.rgb = 187, 187, 53
        self.hud = False


class Enemy_Yellow_Shot(GameObject):
    def __init__(self):
        super(Enemy_Yellow_Shot, self).__init__()
        self._xy = 0, 160
        self.wh = (1, 2)
        self.rgb = 187, 187, 53
        self.hud = False


class Enemy_Blue(GameObject):
    def __init__(self):
        super(Enemy_Blue, self).__init__()
        self._xy = 0, 160
        self.wh = (8, 7)
        self.rgb = 84, 138, 210
        self.hud = False


class Enemy_Blue_Shot(GameObject):
    def __init__(self):
        super(Enemy_Blue_Shot, self).__init__()
        self._xy = 0, 160
        self.wh = (1, 2)
        self.rgb = 84, 138, 210
        self.hud = False


class Enemy_Orange(GameObject):
    def __init__(self):
        super(Enemy_Orange, self).__init__()
        self._xy = 0, 160
        self.wh = (8, 7)
        self.rgb = 180, 122, 48
        self.hud = False


class Enemy_Orange_Shot(GameObject):
    def __init__(self):
        super(Enemy_Orange_Shot, self).__init__()
        self._xy = 0, 160
        self.wh = (1, 2)
        self.rgb = 180, 122, 48
        self.hud = False


class Score(ValueObject):
    def __init__(self):
        super(Score, self).__init__()
        self._xy = 57, 7
        self.wh = (46, 10)
        self.rgb = 210, 164, 74
        self.hud = True
        self.value = 0


class Life(ValueObject):
    def __init__(self):
        super(Life, self).__init__()
        self._xy = 0, 0
        self.wh = (8, 10)
        self.rgb = 101, 111, 228
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
    objects = []

    objects.extend([NoObject()] * 52)
    if hud:
        objects.extend([NoObject()] * 5)
    return objects

player_rgb = [(84, 92, 214), (50, 132, 50), (167, 26, 26), (0, 0, 0), (84, 92, 214)]

def _detect_objects_ram(objects, ram_state, hud=False):
    """
    For all 3 objects:
    (x, y, w, h, r, g, b)
    """
    # r11 == player_color(4msb) lives(4lsb)
    # level 0 == 4, level 1 == 20, level 2 == 36, level 3 == 52, level 4 == 68
    # r21 for setting levels

    level = ram_state[21]
    if ram_state[36] != 140:
        if type(objects[0]) is NoObject:
            objects[0] = Player()
            objects[0].rgb = player_rgb[level]
        player = objects[0]
        # orientation 44, 60, 76, 92, 108
        if ram_state[36] & 16:
            player.xy = 76, 100
            player.wh = 8, 10
        elif ram_state[36] & 32:
            player.xy = 76, 98
            player.wh = 7, 14
        else:
            player.xy = 76, 100
            player.wh = 8, 9
    else:
        objects[0] = NoObject()

    # player shot
    # there are 2 x and 2 y states, the shot flickers, I do not know when which one is displayed
    if ram_state[73]:
        if type(objects[1]) is NoObject:
            objects[1] = Player_Shot()
        if ram_state[1] & 1:
            objects[1].xy = ram_state[73] - 5, 176 - ram_state[75]
        else:
            objects[1].xy = ram_state[74] - 5, 176 - ram_state[76]
    else:
        objects[1] = NoObject()

    if level == 0:
        if ram_state[36] != 140:
            # player color
            player.rgb = 84, 92, 214

        # Enemy position
        for i in range(4):
            if ram_state[37+i]:
                if type(objects[2+i]) is NoObject:
                    objects[2+i] = Enemy_Green()
                enemy = objects[2+i]

                x, y = ram_state[37+i] - 4, 165 - ram_state[41+i]
                w, h = 8, 7

                if ram_state[45+i] % 8 == 0 or ram_state[45+i] % 8 == 4:
                    y += 1
                    h += 2
                elif ram_state[45+i] % 8 == 1 or ram_state[45+i] % 8 == 7:
                    h += 3
                elif ram_state[45+i] % 8 == 2 or ram_state[45+i] % 8 == 6:
                    y += 2
                elif ram_state[45+i] % 8 == 3:
                    x += 1
                    w -= 1
                    h += 4
                elif ram_state[45+i] % 8 == 5:
                    w -= 1
                    h += 4

                enemy.xy = x, y
                enemy.wh = w, h

                # if enemy out of bounds, will appear at the opposing border
                if 0 < y < 33 or x < 0:

                    enemy2 = Enemy_Green()
                    objects[6+i] = enemy2
                    x2, y2 = x, y
                    w2, h2 = w, h

                    if x < 4:
                        x2 = 160+x
                        w2 = -x
                        w += x
                        x = 0
                    if y < 33:
                        y2 = y + 144
                        h2 = 33 - y
                        h -= (33-y)
                        y = 33

                    enemy2.xy = x2, y2
                    enemy2.wh = w2, h2

                else:
                    objects[6+i] = NoObject()
                
            else:
                objects[2+i] = NoObject()
                objects[6+i] = NoObject()

        # Enemy shots
        for i in range(2):
            if ram_state[88+i] and ram_state[1] & 1 != i:
                if type(objects[10+i]) is NoObject:
                    objects[10+i] = Enemy_Green_Shot()
                objects[10+i].xy = ram_state[88+i] - 5,  176 - ram_state[90+i]
            else:
                objects[10+i] = NoObject()

    elif level == 1:
        if ram_state[36] != 140:
            player.rgb = 50, 132, 50

        # Enemy position
        for i in range(4):
            if ram_state[37+i]:
                if type(objects[12+i]) is NoObject:
                    objects[12+i] = Enemy_Black()
                enemy = objects[12+i]

                x, y = ram_state[37+i] - 4, 165 - ram_state[41+i]
                w, h = 8, 7

                if ram_state[45+i] % 8 == 0 or ram_state[45+i] % 8 == 4:
                    y += 1
                    w -= 1
                    h += 2
                elif ram_state[45+i] % 8 == 1 or ram_state[45+i] % 8 == 7:
                    y += 2
                elif ram_state[45+i] % 8 == 2 or ram_state[45+i] % 8 == 6:
                    y += 2
                    h -= 1
                elif ram_state[45+i] % 8 == 3:
                    x += 1
                    w -= 1
                    h += 3
                elif ram_state[45+i] % 8 == 5:
                    w -= 1
                    h += 3

                enemy.xy = x, y
                enemy.wh = w, h

                # if enemy out of bounds, will appear at the opposing border
                if 0 < y < 33 or x < 0:
                    if type(objects[16+i]) is NoObject:
                        objects[16+i] = Enemy_Black()
                    enemy2 = objects[16+i]

                    x2, y2 = x, y
                    w2, h2 = w, h

                    if x < 4:
                        x2 = 160+x
                        w2 = -x
                        w += x
                        x = 0
                    if y < 33:
                        y2 = y + 144
                        h2 = 33 - y
                        h -= (33-y)
                        y = 33

                    enemy2.xy = x2, y2
                    enemy2.wh = w2, h2
                else:
                    objects[16+i] = NoObject()

            else:
                objects[12+i] = NoObject()
                objects[16+i] = NoObject()

        # Enemy shots
        for i in range(2):
            if ram_state[88+i] and ram_state[1] & 1 != i:
                if type(objects[20+i]) is NoObject:
                    objects[20+i] = Enemy_Black_Shot()
                objects[20+i].xy = ram_state[88+i] - 5,  176 - ram_state[90+i]
            else:
                objects[20+i] = NoObject()

    elif level == 2:
        if ram_state[36] != 140:
            player.rgb = 167, 26, 26

        # Enemy position
        for i in range(4):
            if ram_state[37+i]:
                if type(objects[22+i]) is NoObject:
                    objects[22+i] = Enemy_Yellow()
                enemy = objects[22+i]

                x, y = ram_state[37+i] - 4, 165 - ram_state[41+i]
                w, h = 8, 7

                if ram_state[45+i] % 8 == 0 or ram_state[45+i] % 8 == 4:
                    y += 1
                    h += 1
                elif ram_state[45+i] % 8 == 1 or ram_state[45+i] % 8 == 7:
                    h += 2
                elif ram_state[45+i] % 8 == 2 or ram_state[45+i] % 8 == 6:
                    y += 2
                elif ram_state[45+i] % 8 == 3 or ram_state[45+i] % 8 == 5:
                    h += 2

                enemy.xy = x, y
                enemy.wh = w, h

                # if enemy out of bounds, will appear at the opposing border
                if 0 < y < 33 or x < 0:
                    if type(objects[26+i]) is NoObject:
                        objects[26+i] = Enemy_Yellow()
                    enemy2 = objects[26+i]

                    x2, y2 = x, y
                    w2, h2 = w, h

                    if x < 4:
                        x2 = 160+x
                        w2 = -x
                        w += x
                        x = 0
                    if y < 33:
                        y2 = y + 144
                        h2 = 33 - y
                        h -= (33-y)
                        y = 33
                    enemy2.xy = x2, y2
                    enemy2.wh = w2, h2
                else:
                    objects[26+i] = NoObject()
            else:
                objects[22+i] = NoObject()
                objects[26+i] = NoObject()

        # Enemy shots
        for i in range(2):
            if ram_state[88+i] and ram_state[1] & 1 != i:
                if type(objects[30+i]) is NoObject:
                    objects[30+i] = Enemy_Yellow_Shot()
                objects[30+i] = enemy
                objects[30+i].xy = ram_state[88+i] - 5,  176 - ram_state[90+i]
            else:
                objects[30+i] = NoObject()

    elif level == 3:
        if ram_state[36] != 140:
            player.rgb = 0, 0, 0

        # Enemy position
        for i in range(4):
            if ram_state[37+i]:
                if type(objects[32+i]) is NoObject:
                    objects[32+i] = Enemy_Blue()
                enemy = objects[32+i]

                x, y = ram_state[37+i] - 4, 165 - ram_state[41+i]
                w, h = 8, 7

                if ram_state[45+i] % 8 == 0:
                    x += 1
                    y += 1
                    w -= 1
                    h += 2
                elif ram_state[45+i] % 8 == 1 or ram_state[45+i] % 8 == 7:
                    y += 2
                elif ram_state[45+i] % 8 == 2 or ram_state[45+i] % 8 == 6:
                    y += 2
                    h -= 1
                elif ram_state[45+i] % 8 == 3:
                    x += 1
                    y += 2
                    w -= 1
                elif ram_state[45+i] % 8 == 4:
                    y += 1
                    w -= 1
                    h += 2
                elif ram_state[45+i] % 8 == 5:
                    y += 2
                    w -= 1

                enemy.xy = x, y
                enemy.wh = w, h

                # if enemy out of bounds, will appear at the opposing border
                if 0 < y < 33 or x < 0:
                    if type(objects[36+i]) is NoObject:
                        objects[36+i] = Enemy_Blue()
                    enemy2 = objects[36+i]

                    x2, y2 = x, y
                    w2, h2 = w, h

                    if x < 4:
                        x2 = 160+x
                        w2 = -x
                        w += x
                        x = 0
                    if y < 33:
                        y2 = y + 144
                        h2 = 33 - y
                        h -= (33-y)
                        y = 33

                    enemy2.xy = x2, y2
                    enemy2.wh = w2, h2
                else:
                    objects[36+i] = NoObject()

            else:
                objects[32+i] = NoObject()
                objects[36+i] = NoObject()

        # Enemy shots
        for i in range(2):
            if ram_state[88+i] and ram_state[1] & 1 != i:
                if type(objects[40+i]) is NoObject:
                    objects[40+i] = Enemy_Blue_Shot()
                objects[40+i].xy = ram_state[88+i] - 5,  176 - ram_state[90+i]
            else:
                objects[40+i] = NoObject()

    elif level == 4:
        if ram_state[36] != 140:
            player.rgb = 84, 92, 214

        # Enemy position
        for i in range(4):
            if ram_state[37+i]:
                if type(objects[42+i]) is NoObject:
                    objects[42+i] = Enemy_Orange()
                enemy = objects[42+i]

                x, y = ram_state[37+i] - 4, 165 - ram_state[41+i]
                w, h = 8, 7

                if ram_state[45+i] % 8 != 0 or ram_state[45+i] % 8 != 4:
                    y += 2

                enemy.xy = x, y
                enemy.wh = w, h

                # if enemy out of bounds, will appear at the opposing border
                if 0 < y < 33 or x < 0:
                    if type(objects[46+i]) is NoObject:
                        objects[46+i] = Enemy_Orange()
                    enemy2 = objects[46+i]

                    x2, y2 = x, y
                    w2, h2 = w, h

                    if x < 4:
                        x2 = 160+x
                        w2 = -x
                        w += x
                        x = 0
                    if y < 33:
                        y2 = y + 144
                        h2 = 33 - y
                        h -= (33-y)
                        y = 33

                    enemy2.xy = x2, y2
                    enemy2.wh = w2, h2
                else:
                    objects[46+i] = NoObject()

            else:
                objects[42+i] = NoObject()
                objects[46+i] = NoObject()

        # Enemy shots
        for i in range(2):
            if ram_state[88+i] and ram_state[1] & 1 != i:
                if type(objects[50+i]) is NoObject:
                    objects[50+i] = Enemy_Orange_Shot()
                objects[50+i].xy = ram_state[88+i] - 5,  176 - ram_state[90+i]
            else:
                objects[50+i] = NoObject()

    idx = list(range(2+10*level, 12+10*level))
    no_obj = [i for i in range(2, 52) if i not in idx]

    for i in no_obj:
        objects[i] = NoObject()

    if hud:
        if ram_state[0] > 1:
            # Score
            if type(objects[-2]) is NoObject:
                objects[-2] = Score()

            objects[-2].value = _convert_number(ram_state[13]) * 100 + _convert_number(ram_state[15]) * 10000

            # Lives
            if ram_state[11] & 15 == 1:
                if type(objects[-1]) is NoObject:
                    objects[-1] = Life()
                objects[-1].xy = 80, 18
                objects[-1].wh = 8, 10
                objects[-1].value = 1
            elif ram_state[11] & 15:
                if type(objects[-1]) is NoObject:
                    objects[-1] = Life()
                objects[-1].xy = 96-((ram_state[11]&15) * 8), 18
                objects[-1].wh = (ram_state[11]&15) * 8, 10
                objects[-1].value = ram_state[11] & 15
            else:
                objects[-1] = NoObject()
        else:
            objects[-1] = NoObject()
            objects[-2] = NoObject()
