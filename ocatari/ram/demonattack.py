from .game_objects import GameObject, NoObject, ValueObject
from ._helper_methods import bitfield_to_number, number_to_bitfield, _convert_number
import math
import sys

"""
RAM extraction for the game Demon Attack.
"""

# TODO: populate
MAX_NB_OBJECTS = {"Player": 1, 'PlayerMissile': 1, 'Enemy': 8, 'EnemyPart': 6, 'EnemyMissile': 10}
MAX_NB_OBJECTS_HUD = dict(MAX_NB_OBJECTS, **{'Score': 1, 'Lives': 1}) 


class Player(GameObject):
    """
    The player figure i.e., the laser cannon.
    """

    def __init__(self):
        super(Player, self).__init__()
        self._xy = 0, 0
        self.wh = 7, 12
        self.rgb = 184, 70, 162
        self.hud = False


class Enemy(GameObject):
    """
    The enemy demons.
    """

    def __init__(self):
        super(Enemy, self).__init__()
        self._xy = 0, 0
        self.wh = 16, 7
        self.rgb = 213, 130, 74
        self.hud = False


class EnemyPart(GameObject):
    """
    The enemy demons.
    """

    def __init__(self):
        super(EnemyPart, self).__init__()
        self._xy = 0, 0
        self.wh = 30, 7
        self.rgb = 127, 92, 213
        self.hud = False


class PlayerMissile(GameObject):
    """
    The projectiles shot from the player's laser cannon.
    """

    def __init__(self):
        super(PlayerMissile, self).__init__()
        self._xy = 0, 0
        self.wh = 1, 8
        self.rgb = 212, 140, 252
        self.hud = False


class EnemyMissile(GameObject):
    """
    Projectiles shot by the enemy demons.
    """

    def __init__(self):
        super(EnemyMissile, self).__init__()
        self._xy = 0, 0
        self.wh = 1, 4
        self.rgb = 252, 144, 144
        self.hud = False


class Score(ValueObject):
    """
    The player's score display (HUD).
    """

    def __init__(self):  # TODO
        super(Score, self).__init__()
        self._xy = 96, 7
        self.wh = 5, 9
        self.rgb = 223, 183, 85
        self.hud = True


class Lives(ValueObject):
    """
    The indicator for remaining additional bunkers (lives) (HUD).
    """

    def __init__(self):
        super(Lives, self).__init__()
        self._xy = 17, 188
        self.wh = 19, 5
        self.rgb = 240, 128, 128
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




def bitfield_to_number_equality(bitfield):
    res = bitfield[0] * 7 - bitfield[1] * 6 - bitfield[2] * \
        3 - bitfield[3]  # not 100% exact but close
    return res


def calc_x(number):
    """
    takes the bitfield (4 bits) and extracts the x of the object
    way too complicated for no reason
    """
    anchor = number % 16
    offset = number >> 4
    if offset > 7:
        offset = 28 - offset  # 23 + 5 (5 being constant offset)
    else:
        offset = 12 - offset  # 7 + 5
    return anchor * 15 + offset


def _get_score_x_and_width(score):
    spacing = 8
    amount = 0
    if score > 0:
        amount = int(math.log10(score))

    width = 5 + amount * spacing
    x = 96 - amount * spacing
    return x, width


def _get_score(ram_state):
    return _convert_number(ram_state[1]) * 10000 + _convert_number(ram_state[3]) * 100 + \
        _convert_number(ram_state[5])


def _init_objects_ram(hud=False):
    """
    (Re)Initialize the objects
    """
    objects = [Player(), PlayerMissile()]
    objects += [NoObject() for _ in range(24)] # 8 enemies, 6 enemy parts, 10 projectiles
    if hud:
        objects.append(Score())
        objects.append(Lives())
    return objects


def _detect_objects_ram(objects, ram_state, hud=False):
    player, pmissile = objects[:2]
    player.xy = calc_x(ram_state[16]), 174

    if 90 <= ram_state[21]:
        pmissile.xy = 2 + calc_x(ram_state[22]), 176 - ram_state[21]
    else:
        pmissile.xy = 2 + calc_x(ram_state[22]), 178 - ram_state[21]
    
    # enemies
    for i in range(3):
        enemy = objects[2+2*i]
        enemy2 = objects[3+2*i]
        lft_p = objects[10+2*i]
        rgt_p = objects[11+2*i]
        x_left = calc_x(ram_state[13 + i])
        x_right = calc_x(ram_state[17 + i])
        if ram_state[29+i] > 24: # 2 active enemies
            if not enemy:
                enemy = Enemy()
                objects[2+2*i] = enemy
            if ram_state[33+i] > 3: # right enemy is alive
                if not enemy2:
                    enemy2 = Enemy()
                    objects[3+2*i] = enemy2
            else:
                objects[3+2*i] = NoObject()
            if lft_p:
                objects[10+2*i] = NoObject()
                objects[11+2*i] = NoObject()
            enemy.xy = x_left, 175 - ram_state[69 + i]
            enemy2.xy = x_right, 175 - ram_state[69 + i]
            enemy.w = 8
            enemy2.w = 8
        elif ram_state[29+i] > 3 : # enemy is alive, and in one piece
            # if i == 2:
            #     import ipdb; ipdb.set_trace()
            if not enemy:
                enemy = Enemy()
                objects[2+2*i] = enemy
            if enemy2:
                objects[3+2*i] = NoObject()
            if lft_p:
                objects[10+2*i] = NoObject()
                objects[11+2*i] = NoObject()
            enemy.xy = x_left, 175 - ram_state[69 + i]
            enemy.w = 16
        elif ram_state[29+i] > 0: # enemy spawning
            if enemy:
                objects[2+2*i] = NoObject()
            if enemy2:
                objects[3+2*i] = NoObject()
            if not lft_p:
                lft_p = EnemyPart()
                objects[10+2*i] = lft_p
                rgt_p = EnemyPart()
                objects[11+2*i] = rgt_p
            lft_p.xy = x_left, 175 - ram_state[69 + i]
            rgt_p.xy = x_right, 175 - ram_state[69 + i]
        elif ram_state[47+i] >> 6: # left enemy dead
            if enemy:
                objects[2+2*i] = NoObject()
            if not enemy2:
                enemy2 = Enemy()
                objects[3+2*i] = enemy2
            if lft_p:
                objects[10+2*i] = NoObject()
                objects[11+2*i] = NoObject()
            enemy2.xy = x_right, 175 - ram_state[69 + i]
            enemy2.w = 8
        else: # both enemy dead
            if enemy:
                objects[2+2*i] = NoObject()
            if enemy2:
                objects[3+2*i] = NoObject()
            if lft_p:
                objects[10+2*i] = NoObject()
                objects[10+2*i+1] = NoObject()
    # falling enemy
    falling_en = objects[8]
    if ram_state[51] and ram_state[50] >> 6:
        if not falling_en:
            falling_en = Enemy()
            objects[8] = falling_en
        falling_en.xy = calc_x(ram_state[20]), 177 - ram_state[72]
        falling_en.w = 8
    elif objects[8]:
        objects[8] = NoObject()
    # projectiles
    offset_column = 8
    basex = calc_x(ram_state[20]) + 3
    current_y = 183
    proj_i = 0
    proj = objects[16]
    for number in ram_state[37:47]:
        bitfield = number_to_bitfield(number)
        index = 0
        for b in bitfield:
            if b == 1:
                if not proj:
                    proj = EnemyMissile()
                    objects[16] = proj
                proj.xy = basex - 3 + index, current_y - \
                    4  # projectiles are only one pixel wide
                proj_i += 1
                if proj_i == 8: # max number of projectiles
                    break
                proj = objects[16 + proj_i]
            index += 1
        current_y -= offset_column
    # remove potential old projectiles
    while proj_i < 10:
        objects[16 + proj_i] = NoObject()
        proj_i += 1
    if hud:
        score, live = objects[-2:]
        nb_lives = ram_state[114]
        x, w = _get_score_x_and_width(_get_score(ram_state))
        score.xy = x, score.y
        score.w = w
        score.value = _get_score(ram_state)
        if nb_lives:
            if not live:
                live = Lives()
                objects[-1] = live
            live.value = nb_lives
            live.w = 3 + (nb_lives-1) * 8
        elif live:
            objects[-1] = NoObject()
    return objects


def _detect_objects_demon_attack_raw(info, ram_state):
    info["lives"] = ram_state[114]  # 0-3 but renders correctly till 6
    info["player_x"] = ram_state[16]
    info["enemy_y"] = ram_state[69:72]  # 69 is topmost enemy 71 is lowest
    info["enemy_x"] = ram_state[13:16]  # 13 is topmost enemy 15 is lowest
    info["enemy_projectile_y"] = ram_state[37:46]
    # kind of like a bit map. If a value is 0 then there is no projectile
    # at that position the higher the value the thicker / more projectiles
    # at that position 46(ram) is highest possible enemy_position_y(lowest enemy)
    # 37(ram) is player position_y
    info["player_projectile_y"] = ram_state[21]
    info["player_projectile_x"] = ram_state[22]
    info["score"] = _get_score(ram_state)
    # ram [60] explosion and white screen
