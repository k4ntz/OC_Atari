from ._helper_methods import _convert_number
from .game_objects import GameObject, ValueObject
import sys

"""
RAM extraction for the game ASSAULT. Supported modes: ram.
"""

MAX_NB_OBJECTS = {'Player': 1, 'PlayerMissileVertical': 1, 'PlayerMissileHorizontal': 1, 'MotherShip': 1,
                  'Enemy': 9, 'EnemyMissile': 1}
MAX_NB_OBJECTS_HUD = {'PlayerScore': 6, 'Lives': 3, 'Health': 1}


class Player(GameObject):
    """
    The player figure i.e., the cannon. 
    """
    
    def __init__(self):
        super().__init__()
        self.visible = True
        self._xy = 0, 0
        self.wh = 8, 8
        self.rgb = 214, 214, 214
        self.hud = False


class PlayerMissileVertical(GameObject):
    """
    The projectile shot in the vertical direction from the cannon. 
    """
    
    def __init__(self):
        super().__init__()
        self.visible = True
        self._xy = 0, 0
        self.wh = 1, 8
        self.rgb = 236, 236, 236
        self.hud = False


class PlayerMissileHorizontal(GameObject):
    """
    The projectiles shot in the horizontal direction from the cannon. 
    """
     
    def __init__(self):
        super().__init__()
        self.visible = True
        self._xy = 0, 0
        self._prev_xy = None
        self.wh = 4, 2
        self.rgb = 214, 214, 214
        self.hud = False


class MotherShip(GameObject):
    """
    The mother ship at the top, that continually deploys the smaller drones. 
    """
    
    def __init__(self):
        super().__init__()
        self.visible = True
        self._xy = 0, 0
        self.wh = 32, 16
        self.rgb = 72, 160, 72
        self.hud = False


class Enemy(GameObject):
    """
    The enemy drones deployed by the mother ship. 
    """
    
    def __init__(self):
        super().__init__()
        self.visible = True
        self._xy = 0, 0
        self.wh = 16, 8
        self.rgb = 167, 26, 26
        self.hud = False


class EnemyMissile(GameObject):
    """
    The projectiles shot at the player by the enemy drones.
    """
    
    def __init__(self):
        super().__init__()
        self.visible = True
        self._xy = 0, 0
        self.wh = 1, 6
        self.rgb = 255, 255, 255
        self.hud = False


class PlayerScore(ValueObject):
    """
    The player's score display (HUD). 
    """
    
    def __init__(self):
        super().__init__()
        self.visible = True
        self._xy = 0, 0
        self.rgb = 195, 144, 61
        self.wh = 6, 8
        self.hud = True
        self.score = 0

    def __eq__(self, o):
        return isinstance(o, PlayerScore) and self.xy == o.xy


class Lives(GameObject):
    """
    The indicator for the remaining lives of the player (HUD). 
    """

    def __init__(self):
        super().__init__()
        self.visible = True
        self._xy = 0, 0
        self.rgb = 170, 170, 170
        self.wh = 8, 8
        self.hud = True


class Health(GameObject):
    """
    The temperature meter of the cannon (HUD). 
    """
    
    def __init__(self):
        super().__init__()
        self.visible = True
        self._xy = 96, 192
        self.rgb = 72, 160, 72
        self.wh = 8, 8
        self.hud = True


def _init_objects_ram(hud=False):
    """
    (Re)Initialize the objects
    """
    objects = [] #Player(), PlayerMissileVertical(), Enemy(), EnemyMissile(), MotherShip()
    objects.extend([None] * 8)
    if hud:
        objects.extend([None] * 15) #[PlayerScore(), Health(), Lives()]
    return objects


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


# position of objects if value 0 to 16. 17 to 32 uses these values but -1 and so on.
player_x_pos = [3, 3, 15, 30, 45, 60, 75, 90, 105, 120, 135, 150, 3, 3, 3, 3]
player_x_pos_128 = [11, 11, 23, 38, 53, 68, 83, 98, 113, 128, 143, 158, 11, 11, 11, 11]     # after value 128 it differs
horizontal_pos = 0
enemy_missile_x = 0


def _detect_objects_ram(objects, ram_state, hud=False):
    """
    For all objects:
    (x, y, w, h, r, g, b)
    """

    # player
    player = Player()
    objects[0] = player
    x_mod = ram_state[16]
    x_diff = (x_mod // 16) % 8
    if ram_state[16] < 128:
        x = player_x_pos[ram_state[16] % 16] - x_diff   # formula for position
        if x < 0:
            x = 160 + x
        player.xy = x, 178
    else:
        player.xy = player_x_pos_128[ram_state[16] % 16] - x_diff, 178

    # player missile
    missile = PlayerMissileVertical()
    if 7 < ram_state[67] < 119:
        val = ram_state[39]
        x_diff = (val // 16) % 8
        if ram_state[39] < 128:
            x = player_x_pos[ram_state[39] % 16] - x_diff
            if x < 0:
                x = 160 + x
            if ram_state[67] < 25:
                y = ram_state[67] + 36
            elif ram_state[67] < 32:
                y = ram_state[67] + 45
            elif ram_state[67] < 50:
                y = ram_state[67] + 53
            else:
                y = ram_state[67] + 64

            if ram_state[67] == 47:
                missile.wh = 1, 3
            elif ram_state[67] == 55:
                missile.wh = 1, 23
                y = y - 15
            elif ram_state[67] == 39:
                missile.wh = 1, 18
                y = y - 10
            elif ram_state[67] == 31:
                missile.wh = 1, 6
            elif ram_state[67] == 23:
                missile.wh = 1, 16
                y = y - 9

            missile.xy = x - 1, y
        else:
            x = player_x_pos_128[ram_state[39] % 16] - x_diff
            if ram_state[67] < 23:
                y = ram_state[67] + 36
            elif ram_state[67] < 32:
                y = ram_state[67] + 45
            elif ram_state[67] < 50:
                y = ram_state[67] + 53
            else:
                y = ram_state[67] + 64

            if ram_state[67] == 47:
                missile.wh = 1, 3
            elif ram_state[67] == 55:
                missile.wh = 1, 23
                y = y - 15
            elif ram_state[67] == 39:
                missile.wh = 1, 18
                y = y - 10
            elif ram_state[67] == 31:
                missile.wh = 1, 6
            elif ram_state[67] == 23:
                missile.wh = 1, 16
                y = y - 9

            missile.xy = x - 1, y
        objects[1] = missile
    else:
        objects[1] = None

    global horizontal_pos
    global horizontal_pos_right
    global horizontal_pos_left

    # player missile horizontal
    if ram_state[24] == 88:
        mis = PlayerMissileHorizontal()
        mis_offset = 2
        #if horizontal_pos == 0 or horizontal_pos > 130 or horizontal_pos < 20:
        #    horizontal_pos = player.x
        if horizontal_pos == 0:
            horizontal_pos_right = player.x + player.w + mis_offset
            horizontal_pos_left = player.x

        if ram_state[26] == 128:    # shot to the right
            
            horizontal_pos_right =  horizontal_pos_right + 8
            horizontal_pos = horizontal_pos_right
            mis.xy = horizontal_pos_right, 181   

        elif ram_state[26] == 64:   # shot to the left

            horizontal_pos_left = horizontal_pos_left - 8
            horizontal_pos = horizontal_pos_left
            mis.xy = horizontal_pos_left, 181
        
        objects[2] = mis
        
    else:
        objects[2] = None
        horizontal_pos = 0

    # mother ship
    mother_ship = MotherShip()
    x_mother = ram_state[69]
    x_mother_diff = (x_mother // 16) % 8
    if ram_state[69] < 128:
        x_val = player_x_pos[(ram_state[69] - 1) % 16] - x_mother_diff
        if x_val < 0:
            x_val = 160 + x_val
        mother_ship.xy = x_val, 18
    else:
        mother_ship.xy = player_x_pos_128[(ram_state[69] - 1) % 16] - x_mother_diff, 18

    if ram_state[11] == 112:    # mother ship changes color
        mother_ship.rgb = 184, 70, 162
    objects[3] = mother_ship

    # enemy
    global enemy_missile_x
    for en in range(3):
        enemy_appearance = ram_state[54 + en]
        if enemy_appearance == 0:   # enemy not visible in this case
            continue

        if enemy_appearance != 96:
            enemy = Enemy()
            x_enemy = ram_state[33 + en]
            x_enemy_diff = (x_enemy // 16) % 8

            if ram_state[33 + en] < 128:
                x_val = player_x_pos[(ram_state[33 + en]) % 16] - x_enemy_diff
                if x_val < 0:
                    x_val = 160 + x_val

                if ram_state[43] == 25:
                    enemy.xy = x_val, 103 - 25 * en
                elif ram_state[43] == 145:
                    enemy.xy = x_val, 93 - 25 * en

            else:   # take pos_128
                x_val = player_x_pos_128[(ram_state[33 + en]) % 16] - x_enemy_diff
                if x_val < 0:
                    x_val = 160 + x_val

                if ram_state[43] == 25:
                    enemy.xy = x_val, 103 - 25 * en
                elif ram_state[43] == 145:
                    enemy.xy = x_val, 93 - 25 * en

            if enemy_appearance == 160:
                enemy.wh = 8, 8

            if ram_state[40] == 196:  # set enemy color
                enemy.rgb = 72, 160, 72
            elif ram_state[40] == 204:  # set enemy color
                enemy.rgb = 84, 138, 210
            elif ram_state[40] == 212:  # set enemy color
                enemy.rgb = 105, 77, 20

        if enemy_appearance == 224 or enemy_appearance == 96:   # 96 only right part shown
            if enemy_appearance == 224:     # 224 means two enemies are shown
                enemy.wh = 8, 8
            enemy2 = Enemy()
            x_enemy2 = ram_state[36 + en]
            x_enemy_diff2 = (x_enemy2 // 16) % 8

            if ram_state[36 + en] < 128:
                x_val2 = player_x_pos[(ram_state[36 + en]) % 16] - x_enemy_diff2
                if x_val2 < 0:
                    x_val2 = 160 + x_val2

                if ram_state[43] == 25:
                    enemy2.xy = x_val2, 103 - 25 * en
                elif ram_state[43] == 145:
                    enemy2.xy = x_val2, 93 - 25 * en

            else:  # take pos_128
                x_val2 = player_x_pos_128[(ram_state[36 + en]) % 16] - x_enemy_diff2
                if x_val2 < 0:
                    x_val2 = 160 + x_val2

                if ram_state[43] == 25:
                    enemy2.xy = x_val2, 103 - 25 * en
                elif ram_state[43] == 145:
                    enemy2.xy = x_val2, 93 - 25 * en

            enemy2.wh = 8, 8

            if ram_state[40] == 196:  # set enemy color
                enemy2.rgb = 72, 160, 72
            elif ram_state[40] == 204:  # set enemy color
                enemy2.rgb = 84, 138, 210
            elif ram_state[40] == 212:  # set enemy color
                enemy2.rgb = 105, 77, 20

            objects[4+en] = enemy2

        if enemy_appearance != 96:
            objects[4+en] = enemy

        if en == 0 and enemy_missile_x == 0 and ram_state[75] == 128\
                and (enemy_appearance == 192 or enemy_appearance == 160 or enemy_appearance == 224):
            enemy_missile_x = enemy.x
        elif en == 0 and enemy_missile_x == 0 and ram_state[75] == 128 and enemy_appearance == 96:
            enemy_missile_x = enemy2.x

    # enemy missile
    if ram_state[75] == 128:
        missile = EnemyMissile()

        if ram_state[40] == 212:    # brown enemy, with red missile
            missile.xy = enemy_missile_x + 8, 30 + ram_state[73]
            missile.wh = 8, 7
            missile.rgb = 214, 92, 92
        elif ram_state[40] == 204:
            missile.xy = enemy_missile_x + 8, 102 + ram_state[73]
            missile.rgb = 92, 186, 92
            missile.wh = 9, 16
        elif ram_state[40] == 196:
            if 55 + ram_state[110] > 166:
                missile.xy = enemy_missile_x + 8, 166
            else:
                missile.xy = enemy_missile_x + 7, 55 + ram_state[110]
            missile.rgb = 84, 138, 210
            if missile.y + 30 > 186:
                missile.wh = 1, 20
            else:
                missile.wh = 1, 30
        else:
            missile.xy = enemy_missile_x, 60 + ram_state[110]
            missile.rgb = 187, 187, 53

        objects[7] = missile
    else:
        enemy_missile_x = 0

    if hud:
        # score
        for i in range(6):
            sc = PlayerScore()
            sc.xy = 96 - 8 * i, 2
            objects[8+i] = sc

        # lives
        for i in range(ram_state[101] - 1):
            liv = Lives()
            liv.xy = 15 + 16 * i, 192
            objects[14+i] = liv

        # health
        health = Health()
        if ram_state[28] == 192 and ram_state[29] == 0:
            health.wh = 8, 8
        elif ram_state[28] == 224 and ram_state[29] == 0:
            health.wh = 12, 8
        elif ram_state[28] == 240 and ram_state[29] == 0:
            health.wh = 16, 8
        elif ram_state[28] == 248 and ram_state[29] == 0:
            health.wh = 20, 8
        elif ram_state[28] == 252 and ram_state[29] == 0:
            health.wh = 24, 8
        elif ram_state[28] == 254 and ram_state[29] == 0:
            health.wh = 28, 8
        elif ram_state[28] == 255 and ram_state[29] == 0:
            health.wh = 32, 8
        elif ram_state[28] == 255 and ram_state[29] == 1:
            health.wh = 36, 8
        elif ram_state[28] == 255 and ram_state[29] == 3:
            health.wh = 40, 8
        elif ram_state[28] == 255 and ram_state[29] == 7:
            health.wh = 44, 8
        elif ram_state[28] == 255 and ram_state[29] == 15:
            health.wh = 48, 8
        elif ram_state[28] == 255 and ram_state[29] == 31:
            health.wh = 52, 8
        elif ram_state[28] == 255 and ram_state[29] == 63:
            health.wh = 56, 8
        elif ram_state[28] == 255 and ram_state[29] == 127:
            health.wh = 60, 8
        elif ram_state[28] == 255 and ram_state[29] == 255:
            health.wh = 64, 8

        if ram_state[21] == 70:
            health.rgb = 200, 72, 72
        objects[14+ram_state[101]] = health


def _detect_objects_assault_raw(info, ram_state):
    """
    O: NOP
    1:
    2: shoot
    3: move right
    4: move left
    5: shoot to the right
    6: shoot to the left
    """

    info["score"] = _convert_number(ram_state[0]) * 10000 + _convert_number(ram_state[1]) * 100 + _convert_number(ram_state[2])     # noqa
    info["player_x"] = ram_state[16]    # start at x = 134
    info["player_missile_x"] = ram_state[39]    # start at x = 182
    info["player_missile_y"] = ram_state[67]
    info["vertic_missile"] = ram_state[24:27]
    info["maybe_enemy_missile_visible"] = ram_state[75]     # enemy missile visible at 128
    info["enemy_x_part_1"] = ram_state[33:36]  # 33 most downwards enemy
    info["enemy_x_part_2"] = ram_state[36:39]
    info["enemy_appearance"] = ram_state[54:57]     # 192 = normal, 224 = split in two, 160 and 96 only one smaller part
    info["enemy_type"] = ram_state[40]
    info["mother_ship_color"] = ram_state[11:13]
    info["mother_ship_x"] = ram_state[69]
    info["health_color"] = ram_state[21]     # 198 = green, 70 = red
    info["health"] = ram_state[28:30]
    info["player_sprite"] = ram_state[30]
    info["lives"] = ram_state[101]
