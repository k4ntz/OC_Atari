from .game_objects import GameObject
import sys

"""
RAM extraction for the game KANGUROO. Supported modes: raw, revised.

"""

MAX_NB_OBJECTS =  {'Player': 1, 'Child': 1, 'Fruit': 3, 'Bell': 1, 'Platform': 4, 'Scale': 3, 'Projectile_top': 1, 'Enemy': 4, 'Projectile_enemy': 1}
MAX_NB_OBJECTS_HUD = {'Player': 1, 'Child': 1, 'Fruit': 3, 'Bell': 1, 'Platform': 4, 'Scale': 3, 'Projectile_top': 1, 'Enemy': 4, 'Projectile_enemy': 1, 'Score': 1, 'Life': 8, 'Time': 1}

class Player(GameObject):
    def __init__(self):
        super(Player, self).__init__()
        self._xy = 78, 103
        self.wh = 8, 24
        self.rgb = 223, 183, 85
        self.hud = False


class Child(GameObject):
    def __init__(self):
        super(Child, self).__init__()
        self._xy = 78, 12
        self.wh = 8, 15
        self.rgb = 223, 183, 85
        self.hud = False


class Enemy(GameObject):
    def __init__(self, *args, **kwargs):
        super(Enemy, self).__init__()
        super().__init__(*args, **kwargs)
        self._xy = 79, 57
        self.wh = 6, 15
        self.rgb = 227, 159, 89
        self.hud = False


class Fruit(GameObject):
    def __init__(self, *args, **kwargs):
        super(Fruit, self).__init__()
        self._xy = 125, 173
        self.wh = 7, 10
        self.rgb = 214, 92, 92
        self.hud = False


class Scale(GameObject):
    def __init__(self, x, y, w=8, h=35, *args, **kwargs):
        super(Scale, self).__init__(*args, **kwargs)
        self._xy = x, y
        self.wh = w, h
        self.rgb = 162, 98, 33
        self.hud = False


class Platform(GameObject):
    def __init__(self, x, y, w=8, h=4, *args, **kwargs):
        super(Platform, self).__init__(*args, **kwargs)
        self._xy = x, y
        self.wh = w, h
        self.rgb = 162, 98, 33
        self.hud = False


class Projectile_top(GameObject):
    def __init__(self, *args, **kwargs):
        super(Projectile_top, self).__init__()
        self._xy = 0, 0
        self.wh = 2, 3
        self.rgb = 162, 98, 33
        self.hud = False


class Projectile_enemy(GameObject):
    def __init__(self, *args, **kwargs):
        super(Projectile_enemy, self).__init__()
        self._xy = 0, 0
        self.wh = 2, 3
        self.rgb = 227, 159, 89
        self.hud = False


class Bell(GameObject):
    def __init__(self, *args, **kwargs):
        super(Bell, self).__init__()
        self._xy = 126, 173
        self.wh = 6, 11
        self.rgb = 210, 164, 74
        self.hud = False


class Score(GameObject):
    def __init__(self, *args, **kwargs):
        super(Score, self).__init__()
        self._xy = 129, 183
        self.wh = 15, 7
        self.rgb = 160, 171, 79
        self.hud = True


class Life(GameObject):
    def __init__(self, *args, **kwargs):
        super(Life, self).__init__()
        self._xy = 16, 183
        self.wh = 4, 7
        self.rgb = 160, 171, 79
        self.hud = True


class Time(GameObject):
    def __init__(self, *args, **kwargs):
        super(Time, self).__init__()
        self._xy = 80, 191
        self.wh = 15, 5
        self.rgb = 160, 171, 79
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

def _init_objects_kangaroo_ram(hud=True):
    """
    (Re)Initialize the objects
    """

    objects = [Player(), Child(), Enemy(), Enemy(), Enemy(), Enemy(),
               Projectile_top(), Projectile_enemy(), Fruit(), Fruit(), Fruit(), Bell()]

    return objects


# levels: ram_state[36], total of 3 levels: 0,1 and 2
def _detect_objects_kangaroo_revised(objects, ram_state, hud=True):
    objects.clear()

    kp = Player()
    objects.append(kp)
    # player
    kp.xy = ram_state[17] + 15, ram_state[16] * 8 + 5
    if ram_state[19] > 16 and ram_state[19] < 24:
        kp.wh = 8, 13
    elif ram_state[19] == 31:
        kp.wh = 8, 15
    else:
        kp.wh = 8, 24

    kc = Child()
    objects.append(kc)
    # kangaroo child (goal)
    kc.xy = ram_state[83] + 15, 12

    # enemies/monkeys
    m1 = Enemy()
    if ram_state[11] != 255:
        objects.append(m1)
        m1.xy = ram_state[15] + 16, ram_state[11] * 8 + 5

    m2 = Enemy()
    if ram_state[10] != 255:
        objects.append(m2)
        m2.xy = ram_state[14] + 16, ram_state[10] * 8 + 5

    m3 = Enemy()
    if ram_state[9] != 255:
        objects.append(m3)
        m3.xy = ram_state[13] + 16, ram_state[9] * 8 + 5

    m4 = Enemy()
    if ram_state[8] != 255:
        objects.append(m4)
        m4.xy = ram_state[12] + 16, ram_state[8] * 8 + 5

    p1 = Projectile_top()
    objects.append(p1)
    # falling Projectile
    if ram_state[33] != 255:
        p1.xy = ram_state[34] + 14, ((ram_state[33] - (22 * ram_state[36])) * 8) + 9
    else:
        objects.remove(p1)

    # thrown by monkeys Projectile

    # This projectiles visual representation seems to differ from its RAM x position,
    # therefor you will see it leaving the bounding box on both left and right depending on the situation
    p2 = Projectile_enemy()
    objects.append(p2)
    if ram_state[25] != 255:
        p2.xy = ram_state[28] + 15, (ram_state[25] * 8) + 1
    else:
        objects.remove(p2)

    # fruits
    f1 = Fruit()
    objects.append(f1)
    f2 = Fruit()
    objects.append(f2)
    f3 = Fruit()
    objects.append(f3)
    if ram_state[87] == ram_state[86]:
        y1 = (ram_state[84] * 8) + 4
        y2 = (ram_state[85] * 8) + 4
        y3 = (ram_state[86] * 8) + 4
    else:
        y1 = (ram_state[85] * 8) + 4  # top
        y2 = (ram_state[86] * 8) + 4  # mid
        y3 = (ram_state[87] * 8) + 4  # low

    if ram_state[92] == ram_state[91]:
        x1 = ram_state[89] + 15
        x2 = ram_state[90] + 15
        x3 = ram_state[91] + 15
    else:
        x1 = ram_state[90] + 15
        x2 = ram_state[91] + 15
        x3 = ram_state[92] + 15

    f1.xy = x1, y1  # top
    f2.xy = x2, y2  # mid
    f3.xy = x3, y3  # low

    rgb = _get_fruit_type_kangaroo(ram_state[42])
    if rgb is not None:

        f1.rgb = _get_fruit_type_kangaroo(ram_state[42])
    else:
        objects.remove(f1)

    rgb = _get_fruit_type_kangaroo(ram_state[43])
    if rgb is not None:
        f2.rgb = _get_fruit_type_kangaroo(ram_state[43])
    else:
        objects.remove(f2)

    rgb = _get_fruit_type_kangaroo(ram_state[44])
    if rgb is not None:
        f3.rgb = _get_fruit_type_kangaroo(ram_state[44])
    else:
        objects.remove(f3)

    bell = Bell()
    objects.append(bell)
    bell.xy = ram_state[82] + 16, 36

    if hud:
        # score
        score = Score()
        objects.append(score)
        if ram_state[40] != 0:
            score.xy = 121, 183
            score.wh = 23, 7
        if ram_state[40] >= 16:
            score.xy = 113, 183
            score.wh = 31, 7
        if ram_state[39] != 0:
            score.xy = 105, 183
            score.wh = 39, 7
        if ram_state[39] >= 16:
            score.xy = 97, 183
            score.wh = 47, 7

        # lives
        for i in range(8):
            if i < ram_state[45]:
                life = Life()
                life.xy = 16 + (i*8), 183
                objects.append(life)
            else:
                break

        time = Time()
        objects.append(time)
        # time.xy = 80, 191
    add_platforms(ram_state[40], objects)
    return objects


def _detect_objects_kangaroo_raw(info, ram_state):

    # for proper y coordinates you will have to multiply by 8
    # if the coordinates equal 255 they are not visible on screen
    info["ram_slice"] = ram_state[0:18] + ram_state[25], ram_state[28], ram_state[33:35], ram_state[83]

    # info["player_position"] = ram_state[17], ram_state[16]
    # info["kangaroo_child"] = ram_state[83]
    # info["monkey_1_position"] = ram_state[15], ram_state[11]
    # info["monkey_2_position"] = ram_state[14], ram_state[10]
    # info["monkey_3_position"] = ram_state[13], ram_state[9]
    # info["monkey_4_position"] = ram_state[12], ram_state[8]
    # info["bouncing_projectile_position"] = ram_state[34], ram_state[33]
    # info["monkey_projectile_position"] = ram_state[28], ram_state[25]
    # info["level"] = ram_state[36] takes values 0-2


def _get_fruit_type_kangaroo(ram_state):
    """
    Returns the RGB value for fruits depending on the ram-state given
    """

    if ram_state < 128:
        if ram_state % 4 == 3:
            return 195, 144, 61
        else:
            return 214, 92, 92
    else:
        return None

def add_platforms(lvl_value, objects):
    objects.append(Platform(16, 172, w=128))  # base platform
    objects.append(Platform(16, 28, w=128))  # top platform
    if lvl_value < 23:
        objects.append(Scale(132, 132))
        objects.append(Platform(16, 76, w=128))
        objects.append(Scale(20, 85))
        objects.append(Platform(16, 124, w=128))
        objects.append(Scale(132, 37))
    elif lvl_value < 46:
        objects.append(Platform(16, 124, w=28))
        objects.append(Platform(52, 124, w=92))
        objects.append(Platform(16, 76, w=60))
        objects.append(Platform(84, 76, w=60))
        objects.append(Scale(120, 132, h=4))
        objects.append(Scale(24, 116, h=4))
        objects.append(Scale(128, 36, h=4))
        objects.append(Platform(28, 164, w=24))
        objects.append(Platform(112, 84, w=24))
        objects.append(Platform(120, 44, w=24))
        objects.append(Platform(48, 156, w=32))
        objects.append(Platform(76, 148, w=32))
        objects.append(Platform(104, 140, w=32))
        objects.append(Platform(16, 108, w=32))
        objects.append(Platform(56, 100, w=20))
        objects.append(Platform(56, 100, w=20))
        objects.append(Platform(84, 92, w=20))
        objects.append(Platform(64, 60, w=20))
        objects.append(Platform(92, 52, w=20))
        objects.append(Platform(28, 68, w=28))
    else:
        objects.append(Scale(20, 36, h=28))
        objects.append(Scale(20, 148, h=4))
        objects.append(Scale(36, 116, h=20))
        objects.append(Scale(104, 36, h=20))
        objects.append(Scale(120, 68, h=4))
        objects.append(Scale(132, 84, h=4))
        objects.append(Platform(88, 140, w=16))
        objects.append(Platform(64, 148, w=16))
        objects.append(Platform(100, 116, w=16))
        objects.append(Platform(48, 100, w=16))
        objects.append(Platform(76, 52, w=16))
        objects.append(Platform(80, 36, w=16))
        objects.append(Platform(104, 132, w=20))
        objects.append(Platform(84, 156, w=20))
        objects.append(Platform(124, 124, w=20))
        objects.append(Platform(52, 84, w=20))
        objects.append(Platform(108, 164, w=36))
        objects.append(Platform(16, 108, w=80))
        objects.append(Platform(16, 92, w=28))
        objects.append(Platform(76, 92, w=68))
        objects.append(Platform(16, 140, w=32))
        objects.append(Platform(96, 60, w=36))
        objects.append(Platform(100, 76, w=44))
        objects.append(Platform(60, 44, w=12))