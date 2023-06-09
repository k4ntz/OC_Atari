from .game_objects import GameObject
import sys

"""
RAM extraction for the game KANGAROO. Supported modes: raw, revised.

"""

MAX_NB_OBJECTS =  {'Player': 1, 'Child': 1, 'Fruit': 3, 'Bell': 1, 'Platform': 4, 'Scale': 3, 'Projectile_top': 1, 'Enemy': 4, 'Projectile_enemy': 1}
MAX_NB_OBJECTS_HUD = {'Player': 1, 'Child': 1, 'Fruit': 3, 'Bell': 1, 'Platform': 4, 'Scale': 3, 'Projectile_top': 1, 'Enemy': 4, 'Projectile_enemy': 1, 'Score': 1, 'Life': 8, 'Time': 1}
obj_tracker = {}

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
    def __init__(self):
        super(Enemy, self).__init__()
        super().__init__()
        self._xy = 79, 57
        self.wh = 6, 15
        self.rgb = 227, 159, 89
        self.hud = False


class Fruit(GameObject):
    def __init__(self):
        super(Fruit, self).__init__()
        self._xy = 125, 173
        self.wh = 7, 10
        self.rgb = 214, 92, 92
        self.hud = False


class Scale(GameObject):
    def __init__(self, x=0, y=0, w=8, h=35):
        super(Scale, self).__init__()
        self._xy = x, y
        self._prev_xy = x, y
        self.wh = w, h
        self.rgb = 162, 98, 33
        self.hud = False


class Platform(GameObject):
    def __init__(self, x=0, y=0, w=8, h=4):
        super(Platform, self).__init__()
        self._xy = x, y
        self._prev_xy = x, y
        self.wh = w, h
        self.rgb = 162, 98, 33
        self.hud = False


class Projectile_top(GameObject):
    def __init__(self):
        super(Projectile_top, self).__init__()
        self._xy = 0, 0
        self.wh = 2, 3
        self.rgb = 162, 98, 33
        self.hud = False


class Projectile_enemy(GameObject):
    def __init__(self):
        super(Projectile_enemy, self).__init__()
        self._xy = 0, 0
        self.wh = 2, 3
        self.rgb = 227, 159, 89
        self.hud = False


class Bell(GameObject):
    def __init__(self):
        super(Bell, self).__init__()
        self._xy = 126, 173
        self.wh = 6, 11
        self.rgb = 210, 164, 74
        self.hud = False


class Score(GameObject):
    def __init__(self):
        super(Score, self).__init__()
        self._xy = 129, 183
        self.wh = 15, 7
        self.rgb = 160, 171, 79
        self.hud = True


class Life(GameObject):
    def __init__(self):
        super(Life, self).__init__()
        self._xy = 16, 183
        self.wh = 4, 7
        self.rgb = 160, 171, 79
        self.hud = True


class Time(GameObject):
    def __init__(self):
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
               Projectile_top(), Projectile_enemy(), Fruit(), Fruit(), Fruit(), Bell(), 
               Platform(16, 172, w=128), Platform(16, 28, w=128)]
    manage_platforms(0, objects)
    global prevval
    prevval = 0
    if hud:
        objects.extend([Score(), Time(), Life(), Life()])
    return objects


def _detect_objects_kangaroo_revised(objects, ram_state, hud=True):
    # player
    player = objects[0]
    player.xy = ram_state[17] + 15, ram_state[16] * 8 + 5
    if ram_state[19] > 16 and ram_state[19] < 24:
        player.wh = 8, 13
    elif ram_state[19] == 31:
        player.wh = 8, 15
    else:
        player.wh = 8, 24

    # kangaroo child (goal)
    child = objects[1]
    child.xy = ram_state[83] + 15, 12
    enemies = objects[2:6]
    for i, en in enumerate(enemies):
        if ram_state[11-i] != 255 and ram_state[11-i] != 127:
            if en is None:
                en = Enemy()
                objects[2+i] = en
            en.xy = ram_state[15-i] + 16, ram_state[11-i] * 8 + 5
        elif en is not None:
            objects[2+i] = None

    # # falling Projectile
    proj1 = objects[6]
    if ram_state[33] != 255:
        if proj1 is None:
            proj1 = Projectile_top()
            objects[6] = proj1
        proj1.xy = ram_state[34] + 14, ((ram_state[33] - (22 * ram_state[36])) * 8) + 9
    else:
        objects[6] = None
    # thrown by monkeys Projectile
    # This projectiles visual representation seems to differ from its RAM x position,
    # therefor you will see it leaving the bounding box on both left and right depending on the situation
    proj2 = objects[7]
    if ram_state[25] != 255:
        if proj2 is None:
            proj2 = Projectile_enemy()
            objects[7] = proj2
        proj2.xy = ram_state[28] + 15, (ram_state[25] * 8) + 1
    else:
        objects[7] = None

    # # fruits
    fruits = objects[8: 11]
    for i, frt in enumerate(fruits):
        rgb = _get_fruit_type_kangaroo(ram_state[42+i])
        if rgb is not None:
            if frt is None:
                frt = Fruit()
                objects[8+i] = frt
            frt.rgb = rgb
            if ram_state[87] == ram_state[86]:
                y = (ram_state[84+i] * 8) + 4
            else:
                y = (ram_state[85+i] * 8) + 4  
            if ram_state[92] == ram_state[91]:
                x = ram_state[89+i] + 15
            else:
                x = ram_state[90+i] + 15
            frt.xy = x, y 
        else:
            objects[8+i] = None

    # bell
    bell = objects[11]
    bell.xy = ram_state[82] + 16, 36
    # potential lvl change
    curlvlval = ram_state[36]
    global prevval
    if prevval != curlvlval:
        manage_platforms(curlvlval, objects) # ram_state[40]
    prevval = curlvlval

    if hud:
        # score
        score = objects[37]
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

        time = objects[38]
        time.xy = 80, 191

        # lives
        for i in range(2):
            life = objects[39+i]
            if i < ram_state[45]:
                if objects[39+i] is None:
                    life = Life()
                    objects[39+i] = life
                life.xy = 16 + (i*8), 183
            elif life is not None:
                objects[39+i] = None

    # return objects


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

def manage_platforms(current_lvl_val, objects):
    # base platform and top platform are always there
    changing_platforms = objects[13:]
    # levels: ram_state[36], total of 3 levels: 0, 1 and 2
    if current_lvl_val == 0:
        objects[13:37] = [Scale(132, 132), Platform(16, 76, w=128), Scale(20, 85), Platform(16, 124, w=128), Scale(132, 37)] + [None] * 19
    elif current_lvl_val == 1:
        objects[13:37] = [Platform(16, 124, w=28), Platform(52, 124, w=92), Platform(16, 76, w=60), 
                        Platform(84, 76, w=60), Scale(120, 132, h=4), Scale(24, 116, h=4), Scale(128, 36, h=4), 
                        Platform(28, 164, w=24), Platform(112, 84, w=24), Platform(120, 44, w=24), Platform(48, 156, w=32), 
                        Platform(76, 148, w=32), Platform(104, 140, w=32), Platform(16, 108, w=32), Platform(56, 100, w=20), 
                        Platform(56, 100, w=20), Platform(84, 92, w=20), Platform(64, 60, w=20), Platform(92, 52, w=20), 
                        Platform(28, 68, w=28)] +  [None] * 4 # len 20
    else: # current_lvl_val == 2
        objects[13:37] = [Scale(20, 36, h=28), Scale(20, 148, h=4), Scale(36, 116, h=20), Scale(104, 36, h=20), Scale(120, 68, h=4), 
                        Scale(132, 84, h=4), Platform(88, 140, w=16), Platform(64, 148, w=16), Platform(100, 116, w=16), 
                        Platform(48, 100, w=16), Platform(76, 52, w=16), Platform(80, 36, w=16), Platform(104, 132, w=20), 
                        Platform(84, 156, w=20), Platform(124, 124, w=20), Platform(52, 84, w=20), Platform(108, 164, w=36), 
                        Platform(16, 108, w=80), Platform(16, 92, w=28), Platform(76, 92, w=68), Platform(16, 140, w=32), 
                        Platform(96, 60, w=36), Platform(100, 76, w=44), Platform(60, 44, w=12)] # 24