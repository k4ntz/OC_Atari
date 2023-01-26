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


# This is the object falling from the Top onto you or the one thrown at you by mokeys
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


# levels: ram_state[36], total of 3 levels: 0,1 and 2
def _detect_objects_kangaroo_revised(objects, ram_state, hud=True):
    kp, kk, m1, m2, m3, m4, p1, p2, f1, f2, f3, bell = objects[:12]

    # player
    kp.xy = ram_state[17] + 15, ram_state[16] * 8 +5

    # kangaroo kid (goal)
    kk.xy = ram_state[83] + 15, 12
    kk.wh = 8, 15

    # enemys/mokeys
    if ram_state[11] != 255:
        m1.visible = True
        m1.xy = ram_state[15] + 16, ram_state[11] * 8 + 5
    else:
        m1.visible = False

    if ram_state[10] != 255:
        m2.visible = True
        m2.xy = ram_state[14] + 16, ram_state[10] * 8 + 5
    else:
        m2.visible = False

    if ram_state[9] != 255:
        m3.visible = True
        m3.xy = ram_state[13] + 16, ram_state[9] * 8 + 5
    else:
        m3.visible = False

    if ram_state[8] != 255:
        m4.visible = True
        m4.xy = ram_state[12] + 16, ram_state[8] * 8 + 5
    else:
        m4.visible = False

    # falling Projectile
    if ram_state[33] != 255:
        p1.visible = True
        p1.xy = ram_state[34] + 14, (ram_state[33] * 8) + 9
    else:
        p1.visible = False

    # thrown by mokeys Projectile

    # This projectiles visual representation seems to differ from its RAM x position,
    # therefor you will see it leaving the bounding box on both left and right depending on the situation
    if ram_state[25] != 255:
        p2.visible = True
        p2.xy = ram_state[28] + 15, (ram_state[25] * 8) + 1
    else:
        p2.visible = False
    
    # fruits
    f1.xy = ram_state[81] + 15, 60  # top
    f1.rgb = _get_fruit_type_kangaroo(ram_state[42])
    f2.xy = ram_state[80] + 15, 84  # mid
    f2.rgb = _get_fruit_type_kangaroo(ram_state[43])
    f3.xy = ram_state[79] + 15, 108  # low
    f3.rgb = _get_fruit_type_kangaroo(ram_state[44])

    bell.xy = ram_state[82] + 15, 36 


    if hud:
        # score
        if ram_state[39] < 16:
            objects[17].visible = False
            if ram_state[39] == 0:
                objects[16].visible = False
                if ram_state[40] < 16:
                    objects[15].visible = False
                    if ram_state[40] == 0:
                        objects[14].visible = False
        objects[13].visible = True
        objects[12].visible = True

        # lives
        for i in range(8):
            if i+1 > ram_state[45]:
                objects[18 + i].visible = False

    return objects



def _detect_objects_kangaroo_raw(info, ram_state):

    # for proper y coordinates you will have to multiply by 8
    # if the coordinates equal 255 they are not visible on screen
    info["player_position"] = ram_state[17], ram_state[16]
    info["kangaroo_child"] = ram_state[83]
    info["monkey_1_position"] = ram_state[15], ram_state[11]
    info["monkey_2_position"] = ram_state[14], ram_state[10]
    info["monkey_3_position"] = ram_state[13], ram_state[9]
    info["monkey_4_position"] = ram_state[12], ram_state[8]
    info["bouncing_projectile_position"] = ram_state[34], ram_state[33]
    info["monkey_projectile_position"] = ram_state[28], ram_state[25]


def _get_fruit_type_kangaroo(ram_state):
    if ram_state < 128:
        if ram_state % 4 == 3:
            return 195, 144, 61
        else:
            return 214, 92, 92
    else:
        return None
