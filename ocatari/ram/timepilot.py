from .game_objects import GameObject, ValueObject
from ._helper_methods import number_to_bitfield
import sys

MAX_NB_OBJECTS = {"Player": 1, "Player_Shot": 1, "Enemy_Green": 8, "Enemy_Green_Shot": 1, "Enemy_Black": 8, "Enemy_Black_Shot": 1,
                  "Enemy_Yellow": 8, "Enemy_Yellow_Shot": 1, "Enemy_Blue": 8, "Enemy_Blue_Shot": 1, "Enemy_Orange": 8, "Enemy_Orange_Shot": 1}
MAX_NB_OBJECTS_HUD = {"Player": 1, "Player_Shot": 1, "Enemy_Green": 8, "Enemy_Green_Shot": 1, "Enemy_Black": 8, "Enemy_Black_Shot": 1, "Enemy_Yellow": 8,
                      "Enemy_Yellow_Shot": 1, "Enemy_Blue": 8, "Enemy_Blue_Shot": 1, "Enemy_Orange": 8, "Enemy_Orange_Shot": 1, "Score": 1, "Life": 4}  # 'Score': 1}


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
        self.rgb = 0, 0, 0
        self.hud = False


class Enemy_Black_Shot(GameObject):
    def __init__(self):
        super(Enemy_Black_Shot, self).__init__()
        self._xy = 0, 160
        self.wh = (1, 2)
        self.rgb = 0, 0, 0
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
        self.rgb = 0, 0, 0
        self.hud = False


class Enemy_Blue_Shot(GameObject):
    def __init__(self):
        super(Enemy_Blue_Shot, self).__init__()
        self._xy = 0, 160
        self.wh = (1, 2)
        self.rgb = 0, 0, 0
        self.hud = False


class Enemy_Orange(GameObject):
    def __init__(self):
        super(Enemy_Orange, self).__init__()
        self._xy = 0, 160
        self.wh = (8, 7)
        self.rgb = 187, 187, 53
        self.hud = False


class Enemy_Orange_Shot(GameObject):
    def __init__(self):
        super(Enemy_Orange_Shot, self).__init__()
        self._xy = 0, 160
        self.wh = (1, 2)
        self.rgb = 187, 187, 53
        self.hud = False


class Score(ValueObject):
    def __init__(self):
        super(Score, self).__init__()
        self._xy = 57, 7
        self.wh = (46, 10)
        self.rgb = 210, 164, 74
        self.hud = True


class Life(GameObject):
    def __init__(self):
        super(Life, self).__init__()
        self._xy = 0, 0
        self.wh = (8, 10)
        self.rgb = 101, 111, 228
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


def _init_objects_ram(hud=False):
    """
    (Re)Initialize the objects
    """
    objects = []

    objects.extend([None] * 12)
    if hud:
        objects.extend([None] * 5)
    return objects


def _detect_objects_ram(objects, ram_state, hud=False):
    """
    For all 3 objects:
    (x, y, w, h, r, g, b)
    """
    # r11 == levels(4msb) lives(4lsb)
    # level 0 == 4, level 1 == 20, level 2 == 36, level 3 == 52, level 4 == 68

    level = ram_state[11] >> 4
    if ram_state[36] != 140:
        player = Player()
        objects[0] = player
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
        objects[0] = None

    # player shot
    # there are 2 x and 2 y states, the shot flickers, I do not know when which one is displayed
    if ram_state[73]:
        pshot = Player_Shot()
        objects[1] = pshot
        if ram_state[1] & 1:
            pshot.xy = ram_state[73] - 5, 176 - ram_state[75]
        else:
            pshot.xy = ram_state[74] - 5, 176 - ram_state[76]
    else:
        objects[1] = None

    if level == 0:
        if ram_state[36] != 140:
            # player color
            player.rgb = 84, 92, 214

        # Enemy position
        for i in range(4):
            if ram_state[37+i]:
                enemy = Enemy_Green()
                objects[3+i] = enemy
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

                # if enemy out of bounds, will appear at the opposing border
                if 0 < y < 33 or x < 0:
                    enemy2 = Enemy_Green()
                    objects[9+i] = enemy2
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
                    objects[9+i] = None
                enemy.xy = x, y
                enemy.wh = w, h
            else:
                objects[3+i] = None
                objects[9+i] = None

        # Enemy shots
        for i in range(2):
            if ram_state[88+i] and ram_state[1] & 1 != i:
                eshot = Enemy_Green_Shot()
                objects[7+i] = eshot
                eshot.xy = ram_state[88+i] - 5,  176 - ram_state[90+i]
            else:
                objects[7+i] = None

    elif level == 1:
        if ram_state[36] != 140:
            player.rgb = 50, 132, 50

        # Enemy position
        for i in range(4):
            if ram_state[37+i]:
                enemy = Enemy_Black()
                objects[3+i] = enemy
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

                # if enemy out of bounds, will appear at the opposing border
                if 0 < y < 33 or x < 0:
                    enemy2 = Enemy_Green()
                    objects[9+i] = enemy2
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
                    objects[9+i] = None
                enemy.xy = x, y
                enemy.wh = w, h
            else:
                objects[3+i] = None
                objects[9+i] = None

        # Enemy shots
        for i in range(2):
            if ram_state[88+i] and ram_state[1] & 1 != i:
                eshot = Enemy_Black_Shot()
                objects[7+i] = eshot
                eshot.xy = ram_state[88+i] - 5,  176 - ram_state[90+i]
            else:
                objects[7+i] = None
    elif level == 2:
        if ram_state[36] != 140:
            player.rgb = 167, 26, 26

        # Enemy position
        for i in range(4):
            if ram_state[37+i]:
                enemy = Enemy_Yellow()
                objects[3+i] = enemy
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

                # if enemy out of bounds, will appear at the opposing border
                if 0 < y < 33 or x < 0:
                    enemy2 = Enemy_Green()
                    objects[9+i] = enemy2
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
                    objects[9+i] = None
                enemy.xy = x, y
                enemy.wh = w, h
            else:
                objects[3+i] = None
                objects[9+i] = None

        # Enemy shots
        for i in range(2):
            if ram_state[88+i] and ram_state[1] & 1 != i:
                eshot = Enemy_Yellow_Shot()
                objects[7+i] = eshot
                eshot.xy = ram_state[88+i] - 5,  176 - ram_state[90+i]
            else:
                objects[7+i] = None
    elif level == 3:
        if ram_state[36] != 140:
            player.rgb = 0, 0, 0

        # Enemy position
        for i in range(4):
            if ram_state[37+i]:
                enemy = Enemy_Blue()
                objects[3+i] = enemy
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

                # if enemy out of bounds, will appear at the opposing border
                if 0 < y < 33 or x < 0:
                    enemy2 = Enemy_Green()
                    objects[9+i] = enemy2
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
                    objects[9+i] = None
                enemy.xy = x, y
                enemy.wh = w, h
            else:
                objects[3+i] = None
                objects[9+i] = None

        # Enemy shots
        for i in range(2):
            if ram_state[88+i] and ram_state[1] & 1 != i:
                eshot = Enemy_Blue_Shot()
                objects[7+i] = eshot
                eshot.xy = ram_state[88+i] - 5,  176 - ram_state[90+i]
            else:
                objects[7+i] = None
    elif level == 4:
        if ram_state[36] != 140:
            player.rgb = 84, 92, 214

        # Enemy position
        for i in range(4):
            if ram_state[37+i]:
                enemy = Enemy_Orange()
                objects[3+i] = enemy
                x, y = ram_state[37+i] - 4, 165 - ram_state[41+i]
                w, h = 8, 7
                if ram_state[45+i] % 8 != 0 or ram_state[45+i] % 8 != 4:
                    y += 2

                # if enemy out of bounds, will appear at the opposing border
                if 0 < y < 33 or x < 0:
                    enemy2 = Enemy_Green()
                    objects[9+i] = enemy2
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
                    objects[9+i] = None
                enemy.xy = x, y
                enemy.wh = w, h
            else:
                objects[3+i] = None
                objects[9+i] = None

        # Enemy shots
        for i in range(2):
            if ram_state[88+i] and ram_state[1] & 1 != i:
                eshot = Enemy_Orange_Shot()
                objects[7+i] = eshot
                eshot.xy = ram_state[88+i] - 5,  176 - ram_state[90+i]
            else:
                objects[7+i] = None

    if hud:
        if ram_state[0] > 1:
            # Score
            objects[-5] = Score()

            # Lives
            if ram_state[11] & 15 == 1:
                life = Life()
                objects[-4] = life
                life.xy = 80, 18
                for i in range(3):
                    objects[-3+i] = None
            else:
                for i in range(4):
                    if i < int(ram_state[11] & 15):
                        life = Life()
                        objects[-4+i] = life
                        life.xy = 88-(i*8), 18
                    else:
                        objects[-4+i] = None
        else:
            for i in range(5):
                objects[-5+i] = None
