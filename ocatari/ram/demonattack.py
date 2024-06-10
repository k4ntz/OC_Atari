from .game_objects import GameObject
from ._helper_methods import bitfield_to_number, number_to_bitfield, _convert_number
import math
import sys

"""
RAM extraction for the game Demon Attack.
"""

# TODO: populate 
MAX_NB_OBJECTS =  {"Player": 1}
MAX_NB_OBJECTS_HUD = {}

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


class ProjectileFriendly(GameObject):
    """
    The projectiles shot from the player's laser cannon. 
    """
    
    def __init__(self):
        super(ProjectileFriendly, self).__init__()
        self._xy = 0, 0
        self.wh = 1, 8
        self.rgb = 212, 140, 252
        self.hud = False


class ProjectileHostile(GameObject):
    """
    Projectiles shot by the enemy demons. 
    """
    
    def __init__(self):
        super(ProjectileHostile, self).__init__()
        self._xy = 0, 0
        self.wh = 1, 4
        self.rgb = 252, 144, 144
        self.hud = False


class Score(GameObject):
    """
    The player's score display (HUD).
    """
    
    def __init__(self):  # TODO
        super(Score, self).__init__()
        self._xy = 96, 7
        self.wh = 5, 9
        self.rgb = 223, 183, 85
        self.hud = True


class Live(GameObject):
    """
    The indicator for remaining additional bunkers (lives) (HUD).
    """
    
    def __init__(self):
        super(Live, self).__init__()
        self._xy = 0, 0
        self.wh = 3, 5
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

def calculate_small_projectiles_from_bitmap(bitmap, basex):
    result = []
    offset_column = 8

    current_y = 183
    for number in bitmap:
        bitfield = number_to_bitfield(number)

        index = 0
        for b in bitfield:
            if b == 1:
                proj = ProjectileHostile()
                proj.xy = basex - 3 + index, current_y - 4 # projectiles are only one pixel wide
                result.append(proj)
            index += 1

        current_y -= offset_column

    return result


def bitfield_to_number_equality(bitfield):
    res = bitfield[0] * 7 - bitfield[1] * 6 - bitfield[2] * 3 - bitfield[3]  # not 100% exact but close
    return res


def calc_x(number):
    """
    takes the bitfield(4 bits) and extracts the x of the object
    way too complicated for no reason
    """
    anchor = number % 16
    offset = number >> 4
    if offset > 7:
        offset = 28 - offset # 23 + 5 (5 being constant offset)
    else:
        offset = 12 - offset # 7 + 5
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
    objects = [Player(), ProjectileFriendly()]
    if hud:
        objects.append(Score())
        base_x = 17
        for i in range(3):
            live = Live()
            live.xy = base_x, 188
            objects.append(live)
            base_x += 8

    return objects


def _detect_objects_ram(objects, ram_state, hud=False):
    player, proj_friendly = objects[:2]
    if hud:
        score = objects[2]

    player.xy = calc_x(ram_state[16]), 174

    if 90 <= ram_state[21]:
        proj_friendly.xy = 2 + calc_x(ram_state[22]), 176 - ram_state[21]
    else:
        proj_friendly.xy = 2 + calc_x(ram_state[22]), 178 - ram_state[21]

    objects.clear()  # giga ugly but i didnt find a better solution
    objects.extend([player, proj_friendly, score])
    objects.extend(calculate_small_projectiles_from_bitmap(ram_state[37:47], 3 + calc_x(ram_state[20])))

    for i in range(3):
        if not ram_state[13 + i] == 0:
            enemy = Enemy()
            x_left = calc_x(ram_state[13 + i])
            x_right = calc_x(ram_state[17 + i])
            if 5 < abs(x_left - x_right) < 9: # to wings are together
                x = x_left
                if i == 2:
                    x = x + 1
                enemy.xy = x, 175 - ram_state[69 + i]
                if ram_state[29+i] != 0:
                    objects.append(enemy)

    if hud:
        base_x = 17
        for i in range(ram_state[114]):
            live = Live()
            live.xy = base_x, 188
            objects.append(live)
            base_x += 8

        x, w = _get_score_x_and_width(_get_score(ram_state))
        score.xy = x, score.y
        score.w = w


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
