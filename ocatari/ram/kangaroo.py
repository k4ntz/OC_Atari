from ._helper_methods import _convert_number
from .game_objects import GameObject

"""
RAM extraction for the game KANGUROO. Supported modes: raw, revised.

"""

class Kangaroo(GameObject):
    def __init__(self):
        super(Kangaroo, self).__init__()
        self.visible = True
        self._xy = 78, 103
        self.wh = 8, 24
        self.rgb = 223, 183, 85
        self.hud = False


class Enemy(GameObject):
    def __init__(self, *args, **kwargs):
        super(Enemy, self).__init__()
        super().__init__(*args, **kwargs)
        self.visible = True
        self._xy = 79, 57
        self.wh = 7, 15
        self.rgb = 227,159,89
        self.hud = False


class Fruit(GameObject):
    def __init__(self, *args, **kwargs):
        super(Fruit, self).__init__()
        self.visible = True
        self._xy = 125, 173
        self.wh = 7, 10
        self.rgb = 214, 92, 92
        self.hud = False


# This is the object falling from the Top onto you or the one thrown at you
class Projectile(GameObject):
    def __init__(self, *args, **kwargs):
        super(Projectile, self).__init__()
        self.visible = True
        self._xy = 0, 0
        self.wh = 2, 3
        self.rgb = 162, 98, 33
        self.hud = False


class Bell(GameObject):
    def __init__(self, *args, **kwargs):
        super(Bell, self).__init__()
        self.visible = True
        self._xy = 125, 173
        self.wh = 8, 11
        self.rgb = 210, 164, 74
        self.hud = False


class Score(GameObject):
    def __init__(self, *args, **kwargs):
        super(Score, self).__init__()
        self.visible = True
        self._xy = 137, 183
        self.wh = 7, 7
        self.rgb = 160, 171, 79
        self.hud = True


class Life(GameObject):
    def __init__(self, *args, **kwargs):
        super(Life, self).__init__()
        self.visible = True
        self._xy = 16, 183
        self.wh = 3, 7
        self.rgb = 160, 171, 79
        self.hud = True


class Time(GameObject):
    def __init__(self, *args, **kwargs):
        super(Time, self).__init__()
        self.visible = True
        self._xy = 92, 191
        self.wh = 3, 5
        self.rgb = 160, 171, 79
        self.hud = True


def _init_objects_kangaroo_ram(hud=True):
    """
    (Re)Initialize the objects
    """

    objects = [Kangaroo(), Kangaroo(), Enemy(), Enemy(), Enemy(), Enemy(), Projectile(), Projectile(), Fruit(), Fruit(), Fruit(), Bell()]

    objects[3].visible = False
    objects[4].visible = False
    objects[5].visible = False

    if hud:
        x = 137
        for i in range(6):
            score = Score()
            score.xy = x, 183
            objects.append(score)
            x -= 8

        x = 16
        for i in range(8):
            life = Life()
            life.xy = x, 183
            objects.append(life)
            x += 8

        x = 92
        for i in range(4):
            time = Time()
            time.xy = x, 191
            objects.append(time)
            x -= 4

    return objects


def _detect_objects_kangaroo_revised(objects, ram_state, hud=True):
    kp, kk, m1, m2, m3, m4, p1, p2, f1, f2, f3, bell = objects[:12]

    kp.xy = ram_state[17] + 15, ram_state[16] * 8 +5

    kk.xy = ram_state[83] + 15, 12
    kk.wh = 8, 15

    if ram_state[11] != 255:
        m1.visible = True
        m1.xy = ram_state[15] + 16, ram_state[11] * 8 + 5
    else:
        m1.visible = False

    if ram_state[33] != 255:
        p1.visible = True
        p1.xy = ram_state[34] + 14, (ram_state[33] * 8) + 9
    else:
        p1.visible = False

    # This projectiles visual representation seems to differ from its RAM x position,
    # therefor you will see it leaving the bounding box on both left and right depending on the situation
    if ram_state[25] != 255:
        p2.visible = True
        p2.xy = ram_state[28] + 15, (ram_state[25] * 8) + 1
    else:
        p2.visible = False

    f1.xy = ram_state[81] + 15, 60  # top
    f2.xy = ram_state[80] + 15, 84  # mid
    f3.xy = ram_state[79] + 15, 108  # low
    bell.xy = ram_state[82] + 15, 36 


    if hud:
        if ram_state[39] < 16:
            objects[16].visible = False
            if ram_state[39] == 0:
                objects[15].visible = False
                if ram_state[40] < 16:
                    objects[14].visible = False
                    if ram_state[40] == 0:
                        objects[13].visible = False
        objects[7].visible = True
        objects[6].visible = True

        for i in range(8):
            if i+1 > ram_state[45]:
                objects[17 + i].visible = False

    return objects



def _detect_objects_kangaroo_raw(info, ram_state):

    info["player_position"] = ram_state[17], ram_state[16] * 10
    info["player_movable"] = True if ram_state[124] == 188 else False
    info["kangaroo_child"] = ram_state[83]


def _augment_info_kangaroo_revised(info, ram_state):

    """
    For all 3 objects:
    (x, y, w, h, r, g, b)
    """
    objects = {}

    info["time"] = _convert_number(ram_state[59]) * 100
    info["score"] = _convert_number(ram_state[39]) * 10000 + _convert_number(ram_state[40]) * 100
    info["lives"] = ram_state[45]
    info["level"] = ram_state[36]  # total of 3 levels: 0,1 and 2

    info["player_position"] = ram_state[17], ram_state[16] * 10
    info["player_movable"] = True if ram_state[124] == 188 else False
    info["kangaroo_child"] = ram_state[83]

    info["fruit_1_type"] = _get_fruit_type_kangaroo(ram_state[42])  # top
    info["fruit_1_position"] = ram_state[81]
    info["fruit_2_type"] = _get_fruit_type_kangaroo(ram_state[43])  # mid
    info["fruit_2_position"] = ram_state[80]
    info["fruit_3_type"] = _get_fruit_type_kangaroo(ram_state[44])  # low
    info["fruit_3_position"] = ram_state[79]

    info["monkey_1_throw"] = ram_state[118]  # 255 = no throw, 21 = throwing animation, 0 = throw
    info["monkey_1_position"] = ram_state[15], ram_state[11] * 10  # times 10 is still a guess

    info["bouncing_apple_position"] = ram_state[34], ram_state[33] * 10
    info["monkey_apple_position"] = ram_state[28], ram_state[25]  # one state for all apples thrown by monkeys

    info["bell_position"] = ram_state[82]

    info["monkey_sprite"] = ram_state[3]  # or ram_state[7]
    info["player_sprite"] = ram_state[54]
    info["player_movement"] = ram_state[72]
    info["ticker"] = ram_state[57]  # Game starts when this state reaches 158

    info["objects"] = objects


def _get_fruit_type_kangaroo(ram_state):
    if ram_state < 128:
        if ram_state % 4 == 0:
            return "Strawberry"
        elif ram_state % 4 == 1:
            return "Apple"
        elif ram_state % 4 == 2:
            return "Cherry"
        elif ram_state % 4 == 3:
            return "Pineapple"
    else:
        return None
