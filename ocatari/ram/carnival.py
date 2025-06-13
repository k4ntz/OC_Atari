from .game_objects import GameObject, NoObject
from ._helper_methods import _convert_number
from .utils import match_objects
import sys

"""
RAM extraction for the game CARNIVAL. Supported modes: ram.
"""

MAX_NB_OBJECTS = {'Player': 1, 'PlayerMissile': 1, 'Wheel': 1, 'Rabbit': 6,
                  'Duck': 6, 'ExtraBullets': 6, 'Owl': 6, 'FlyingDuck': 6}
MAX_NB_OBJECTS_HUD = {'Player': 1, 'PlayerMissile': 1, 'Wheel': 1, 'Rabbit': 6, 'Duck': 6, 'ExtraBullets': 6,
                      'Owl': 6, 'FlyingDuck': 6, 'AmmoBar': 1, 'BonusSign': 1, 'BonusValue': 1, 'PlayerScore': 1}


class Player(GameObject):
    """
    The player figure i.e, the gun.
    """

    def __init__(self):
        super().__init__()
        self._xy = 66, 186
        self.wh = 6, 13
        self.rgb = 66, 158, 130
        self.hud = False


class PlayerMissile(GameObject):
    """
    Projectiles fired from the player's gun.
    """

    def __init__(self, x=0, y=0, w=6, h=8):
        super().__init__()
        self._xy = x, y
        self.wh = w, h
        self.rgb = 183, 194, 95
        self.hud = False


class Owl(GameObject):
    """
    The owl targets.
    """

    def __init__(self, x=0, y=0, w=8, h=15):
        super().__init__()
        self._xy = x, y
        self.wh = w, h
        self.rgb = 214, 92, 92
        self.hud = False


class Duck(GameObject):
    """
    The duck targets.
    """

    def __init__(self, x=0, y=0, w=8, h=15):
        super().__init__()
        self._xy = x, y
        self.wh = w, h
        self.rgb = 187, 187, 53
        self.hud = False


class FlyingDuck(GameObject):
    """
    The ducks that fly down the screen to eat some of the bullets.
    """

    def __init__(self, x=0, y=0, w=16, h=15):
        super().__init__()
        self._xy = x, y
        self.wh = w, h
        self.rgb = 187, 187, 53
        self.hud = False


class Rabbit(GameObject):
    """
    The rabbit targets.
    """

    def __init__(self, x=0, y=0, w=8, h=15):
        super().__init__()
        self._xy = x, y
        self.wh = w, h
        self.rgb = 192, 192, 192
        self.hud = False


class ExtraBullets(GameObject):
    """
    The extra-bullet boxes.
    """

    def __init__(self, x=0, y=0, w=8, h=9):
        super().__init__()
        self._xy = 0, 0
        self.wh = 8, 9
        self.rgb = 192, 192, 192
        self.hud = False


class PlayerScore(GameObject):
    """
    The player's score display (HUD).
    """

    def __init__(self):
        super().__init__()
        self._xy = 65, 0
        self.rgb = 160, 171, 79
        self.wh = 38, 9
        self.hud = True

    def __eq__(self, o):
        return isinstance(o, PlayerScore) and self.xy == o.xy


class AmmoBar(GameObject):
    """
    The ammunition bar display (HUD).
    """

    def __init__(self):
        super().__init__()
        self._xy = 0, 203
        self.rgb = 24, 59, 157
        self.wh = 152, 5
        self.hud = True


class BonusSign(GameObject):
    """
    The bonus (or penalty) points/ammunition target (HUD).
    """

    def __init__(self):
        super().__init__()
        self._xy = 12, 29
        self.rgb = 214, 92, 92
        self.wh = 6, 9
        self.hud = True


class BonusValue(GameObject):
    """
    The value of the bonus/penalty target.
    """

    def __init__(self):
        super().__init__()
        self._xy = 22, 29
        self.rgb = 214, 92, 92
        self.wh = 22, 9
        self.hud = True


class Wheel(GameObject):
    """
    The spinning pipe target.
    """

    def __init__(self):
        super().__init__()
        self._xy = 70, 15
        self.rgb = 45, 87, 176
        self.wh = 28, 12
        self.hud = False


# Switches color at each level. Every value up to 255 encodes a different color (sometimes one that was already used).
# So if you reach a higher level just extend the dictionary with the RGB-values.
ammo_bar_colors = {1: [24, 59, 157], 2: [0, 68, 0], 3: [125, 48, 173], 4: [144, 72, 17], 5: [144, 72, 17],
                   6: [111, 111, 111], 7: [74, 74, 74], 8: [252, 224, 112], 9: [117, 204, 235], 10: [84, 92, 214],
                   11: [232, 232, 74], 12: [111, 111, 111], 13: [232, 232, 74], 14: [252, 188, 116], 15: [104, 25, 154],
                   16: [149, 111, 227], 17: [252, 188, 116], 18: [240, 170, 103], 19: [187, 187, 53],
                   20: [232, 232, 74], 21: [132, 252, 212], 22: [188, 144, 252], 23: [198, 108, 58],
                   24: [236, 140, 224], 25: [117, 128, 240], 26: [187, 187, 53], 27: [252, 224, 112],
                   28: [188, 144, 252], 29: [236, 236, 236], 30: [132, 200, 252], 31: [252, 224, 112]}
wheel_colors = {0: [45, 87, 176], 1: [26, 102, 26],
                2: [125, 48, 173], 3: [162, 98, 33]}
Y_POS = [89, 89, 68, 68, 47, 47]
x_missile = 0
y_prev_missile = 0

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
    objects = [Player(), PlayerMissile(), Wheel()]
    # for the Rabbit, Duck, ExtraBullets, Owls and FlyingDucks
    objects.extend([NoObject() for _ in range(30)])

    if hud:
        objects.extend([NoObject(), NoObject(), NoObject(), PlayerScore()])

    return objects


def _detect_objects_ram(objects, ram_state, hud=False):
    """
       For all objects
       (x, y, w, h, r, g, b)
    """
    player = objects[0]

    # player
    if ram_state[2] - 4 < 0:
        player.xy = ram_state[2], 186
    else:
        player.xy = ram_state[2] - 4, 186

    # if hud:
    #     del objects[2:]
    # else:
    #     del objects[1:]

    global x_missile
    global y_prev_missile

    # player missile: not perfect, because the RAM does not save the x position of the missile. Thus its based on the
    # player position, but it does not always match.
    missile = objects[1]
    if ram_state[55] != 0 and ram_state[55] > 14:
        if x_missile == 0 or y_prev_missile < ram_state[55]:
            if ram_state[2] - 4 < 0:
                x_missile = ram_state[2]
            else:
                x_missile = ram_state[2] - 6
        missile = missile if type(missile) is PlayerMissile else PlayerMissile()
        if ram_state[55] > 99:
            missile.xy = x_missile, ram_state[55] + 6
            y_prev_missile = ram_state[55] + 6
        else:
            missile.xy = x_missile, ram_state[55]
            y_prev_missile = ram_state[55]
    else:
        missile = NoObject() if missile is not NoObject else missile
        x_missile = 0
    objects[1] = missile

    # targets
    ducks = []
    rabbits = []
    owls = []
    extra_bullets = []
    flying_ducks = []
    for i in range(6):
        x = ram_state[18 + i] - 4
        sprite = ram_state[24 + i * 2]
        if sprite == 0:
            ducks.extend(_calculate_targets(ram_state, 0, x, i))
        elif sprite == 16:
            rabbits.extend(_calculate_targets(ram_state, 1, x, i))
        elif sprite == 32:
            owls.extend(_calculate_targets(ram_state, 2, x, i))
        elif sprite == 48:
            extra_bullets.extend(_calculate_targets(ram_state, 3, x, i))
        elif sprite == 92:  # duck flying down
            if ram_state[1] == 79 or ram_state[1] == 0:
                continue
            else:
                # if len(flying_ducks) >= 0: 
                #     import ipdb; ipdb.set_trace()
                duck = FlyingDuck()
                duck.xy = ram_state[111] - 4, 111 + ram_state[1] - 3
                flying_ducks.append(duck)
        else:
            pass

    match_objects(objects, [(rabbit.xy[0], rabbit.xy[1], rabbit.wh[0], rabbit.wh[1]) for rabbit in rabbits], 3, MAX_NB_OBJECTS['Rabbit'], Rabbit)
    match_objects(objects, [(duck.xy[0], duck.xy[1], duck.wh[0], duck.wh[1]) for duck in ducks], 9, MAX_NB_OBJECTS['Duck'], Duck)
    match_objects(objects, [(extra_bullet.xy[0], extra_bullet.xy[1], extra_bullet.wh[0], extra_bullet.wh[1]) for extra_bullet in extra_bullets], 15, MAX_NB_OBJECTS['ExtraBullets'], ExtraBullets)
    match_objects(objects, [(owl.xy[0], owl.xy[1], owl.wh[0], owl.wh[1]) for owl in owls], 21, MAX_NB_OBJECTS['Owl'], Owl)
    match_objects(objects, [(flying_duck.xy[0], flying_duck.xy[1], flying_duck.wh[0], flying_duck.wh[1]) for flying_duck in flying_ducks], 27, MAX_NB_OBJECTS['FlyingDuck'], FlyingDuck)

    # wheel
    if ram_state[121] != 84 and ram_state[123] != 84:
        wheel = objects[2] if type(objects[2]) is Wheel else Wheel()
        wheel.rgb = wheel_colors.get(ram_state[125])
        objects[2] = wheel
    else:
        objects[2] = NoObject()

    if hud:
        # ammo bar, starts blinking if ten or less but that is not implemented
        if ram_state[3] != 0:
            ammo = objects[-4] if type(objects[-4]) is AmmoBar else AmmoBar()
            ammo.wh = ram_state[3] * 4, 5
            #ammo.xy = ammo.xy[0], 203 
            if ram_state[42] < 32:
                ammo.rgb = ammo_bar_colors.get(ram_state[42])
            else:
                ammo.rgb = [24, 59, 157]
            objects[-4] = ammo
        else: 
            if objects[-4] is not NoObject:
                objects[-4] = NoObject()

        # bonus
        if ram_state[9] != 79:
            sign = objects[-3] if type(objects[-3]) is BonusSign else BonusSign()
            value = objects[-2] if type(objects[-2]) is BonusValue else BonusValue()
            if ram_state[9] == 43:
                value.xy = 20, 29

            objects[-3] = sign
            objects[-2] = value
        else:
            if objects[-3] is not NoObject:
                objects[-3] = NoObject()
            if objects[-2] is not NoObject:
                objects[-2] = NoObject()



def _calculate_targets(ram_state, target_num, x, i):
    """
    Calculate targets type and location for the different variations of appearance.
    """
    targets = []

    # define targets type
    y = Y_POS[i]
    if target_num == 0:
        obj1 = Duck()
        obj2 = Duck()
        obj3 = Duck()
    elif target_num == 1:
        obj1 = Rabbit()
        obj2 = Rabbit()
        obj3 = Rabbit()
    elif target_num == 2:
        obj1 = Owl()
        obj2 = Owl()
        obj3 = Owl()
    elif target_num == 3:
        obj1 = ExtraBullets()
        obj2 = ExtraBullets()
        obj3 = ExtraBullets()
        y = y + 6
    else:
        pass

    # set position of targets relative to the leftmost target of that specific type
    if ram_state[36 + i] == 0:  # only one target
        pass
    elif ram_state[36 + i] == 1:    # two targets
        obj1.xy = (x + 16) % 160, y
        targets.append(obj1)
    elif ram_state[36 + i] == 2:    # two targets but one extra space between them
        obj1.xy = (x + 32) % 160, y
        targets.append(obj1)
    elif ram_state[36 + i] == 3:    # three targets
        obj1.xy = (x + 16) % 160, y
        targets.append(obj1)
        obj2.xy = (x + 32) % 160, y
        targets.append(obj2)
    elif ram_state[36 + i] == 4:    # two targets with extra large space between them
        obj1.xy = (x + 64) % 160, y
        targets.append(obj1)
    elif ram_state[36 + i] == 5:    # one wide target
        obj3.wh = 16, 15
    elif ram_state[36 + i] == 6:    # three targets with space between them
        obj1.xy = (x + 32) % 160, y
        targets.append(obj1)

        obj2.xy = (x + 64) % 160, y
        targets.append(obj2)
    elif ram_state[36 + i] == 7:    # one even wider target
        obj3.wh = 32, 15
    else:
        pass
    if x >= 0:
        obj3.xy = x, y
        targets.append(obj3)

    return targets


def _detect_objects_carnival_raw(info, ram_state):
    """
    0: NOP
    1: Fire
    2: Move right
    3: Move left
    4: fire once + move right
    5: fire once + move left
    """
    player = ram_state[2]   # player_x start at 87, right side = 150, left side = 12; player_y fix
    missile = ram_state[55]     # missile_y: 0 if not shot
    ammo_count = ram_state[3]   # max and start = 40
    # 18, 19 for first row, 20, 21 for second row and 22, 23 for third row
    targets_x = ram_state[18:24]
    flying_duck_x = ram_state[111]
    flying_duck_y = ram_state[1]
    relevant_objects = player + missile + ammo_count + \
        targets_x.tolist() + flying_duck_x + flying_duck_y
    info["relevant_objects"] = relevant_objects

    # additional info
    # 0 = duck, 16 = rabbit, 32 = owl, 48 = extra bullets,
    info["targets_sprites_first_row"] = ram_state[24:28]
    # 92 = flying duck
    info["targets_sprites_second_row"] = ram_state[28:32]
    info["targets_sprites_third_row"] = ram_state[32:36]
    info["targets_first_row_variation"] = ram_state[36:38]
    info["targets_second_row_variation"] = ram_state[38:40]
    info["targets_third_row_variation"] = ram_state[40:42]
    # info["score_thousands"] = ram_state[80]
    info["level"] = ram_state[42]   # starts at level 1
    info["bonus_sprites"] = ram_state[8:12]     # either ammo or score
    info["score"] = _convert_number(
        ram_state[45]) * 1000 + _convert_number(ram_state[46]) * 10
    info["wheel_sprites"] = ram_state[121:125]
    # 0 = blue, 1 = green, 2 = purple, 3 = orange
    info["wheel_color"] = ram_state[125]
