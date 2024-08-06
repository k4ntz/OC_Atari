from .game_objects import GameObject
from ._helper_methods import _convert_number
import sys
import numpy as np

"""
RAM extraction for the game GALAXIAN. Supported modes: ram.
"""

MAX_NB_OBJECTS =  {'Player': 1, 'PlayerMissile': 1, 'EnemyMissile': 20, 'EnemyShip': 35, 'DivingEnemy': 10}
MAX_NB_OBJECTS_HUD =  {'Player': 1, 'PlayerMissile': 1, 'EnemyMissile': 20, 'EnemyShip': 35, 'Score': 1, 'Round': 1, 'Lives': 1, 'DivingEnemy': 10}

class Player(GameObject):
    """
    The player figure i.e, the gun.
    """
    
    def __init__(self):
        super().__init__()
        self._xy = 66, 186
        self.wh = 8, 13
        self.rgb = 236, 236, 236
        self.hud = False


class PlayerMissile(GameObject):
    """
    The projectiles fired by the player. 
    """
    
    def __init__(self):
        super().__init__()
        self._xy = 66, 186
        self.wh = 1, 3
        self.rgb = 210, 164, 74
        self.hud = False


class EnemyMissile(GameObject):
    """
    The projectiles fired by the Enemy. 
    """
    
    def __init__(self):
        super().__init__()
        self._xy = 66, 186
        self.wh = 1, 4
        self.rgb = 228, 111, 111
        self.hud = False

class EnemyShip(GameObject):
    """
    The Enemy Ships. 
    """
    
    def __init__(self):
        super().__init__()
        self._xy = 66, 186
        self.wh = 6, 9
        self.rgb = 232, 204, 99
        self.hud = False

class DivingEnemy(GameObject):
    """
    The Enemy which are currently attacing. 
    """
    
    def __init__(self):
        super().__init__()
        self._xy = 66, 186
        self.wh = 8, 11
        self.rgb = 232, 204, 99
        self.hud = False

class Score(GameObject):
    """
    The player's remaining lives (HUD).
    """
    
    def __init__(self):
        super().__init__()
        self.rgb = 232, 204, 99
        self._xy = 63, 4
        self.wh = 39, 7
        self.hud = True

class Round(GameObject):
    """
    The round counter display (HUD).
    """
    
    def __init__(self):
        super().__init__()
        self.rgb = 214, 214, 214
        self._xy = 137, 188
        self.wh = 7, 7
        self.hud = True

class Lives(GameObject):
    """
    The remaining lives of the player (HUD).
    """
    
    def __init__(self):
        super().__init__()
        self.rgb = 214, 214, 214
        self._xy = 19, 188
        self.wh = 13, 7
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
    objects = [Player(), PlayerMissile()]

    # for i in range(MAX_NB_OBJECTS('EnemyMissile')):
    #     missile = EnemyMissile()
    #     objects.append(missile)

    if hud:
        objects.extend([Lives(), Score(), Round()])

    return objects


def _detect_objects_ram(objects, ram_state, hud=False):
    """
       For all objects:
       (x, y, w, h, r, g, b)
    """

    player = objects[0]
    if ram_state[11] != 255: #else player not on screen
        if player is None:
            player = Player()
            objects[0] = player
        player.x, player.y = ram_state[100]+8, 170 
    elif player is not None:
        objects[0] = None

    player_missile = objects[1]
    if ram_state[11] != 255 and ram_state[11] != 151: #else there is no missile
        if player_missile is None:
            player_missile = PlayerMissile()
            objects[1] = player_missile
        player_missile.x, player_missile.y = ram_state[60] + 2, ram_state[11] + 16
    elif player_missile is not None:
        objects[1] = None

    if hud:
        lives = objects[2]
        if ram_state[57] != 0:
            if lives is None:
                lives = Lives()
            lives.w = ram_state[57] * 3 + (ram_state[57] - 1) * 2
            objects[2] = lives
        elif lives is not None:
            objects[2] = None
        

    # ENEMIES
    # enemies deletion from objects:
    enemy_pos = np.where([isinstance(a, EnemyShip) for a in objects])[0]
    if len(enemy_pos) > 0:
        del objects[enemy_pos[0]:enemy_pos[-1] + 1]

    # The 7 rightmost bits of the ram positions 38 to 44 represent a bitmap of the enemies. 
    # Each bit is 1 if there is an enemy in its position and 0 if there is not.
    enemies = []
    for i in range(6):
        row = format(ram_state[38 + i] & 0x7F, '07b') #gets a string of the 7 relevant bits
        row = [int(x) for x in row]
        row_y = 19 + i * 12
        for j in range(len(row)):
            if row[j] == 1:
                enemy_ship = EnemyShip()
                enemy_ship.y = row_y
                enemy_ship.x = 19 + ram_state[36] / 2 + np.ceil(j * 16.5)
                enemies.append(enemy_ship)
    objects.extend(enemies)

    # DIVING ENEMIES
    # enemies deletion from objects:
    enemy_pos = np.where([isinstance(a, DivingEnemy) for a in objects])[0]
    if len(enemy_pos) > 0:
        del objects[enemy_pos[0]:enemy_pos[-1] + 1]

    enemies = []
    for i in range(5):
        x_pos = ram_state[64 + i] + 8
        y_pos = ram_state[69 + i] * 0.75 + 8
        if y_pos > 8 and y_pos < 186: #the diving enemy is in the visible area
            diving_enemy = DivingEnemy()
            diving_enemy.x = x_pos
            diving_enemy.y = y_pos
            enemies.append(diving_enemy)
    objects.extend(enemies)

    # ENEMY MISSILES
    # enemies deletion from objects:
    missile_pos = np.where([isinstance(a, EnemyMissile) for a in objects])[0]
    if len(missile_pos) > 0:
        del objects[missile_pos[0]:missile_pos[-1] + 1]

    missiles = []
    missile_number = 0
    for i in range(8):
        if ram_state[25 + i] == 1:
            missile_number += 1
            enemy_missile = EnemyMissile()
            enemy_missile.x = ram_state[102 + missile_number] + 11
            enemy_missile.y = i * 16 + 80
            missiles.append(enemy_missile)
    objects.extend(missiles)
    

def _detect_objects_galaxian_raw(info, ram_state):
    
    info["score"] = _convert_number(ram_state[44]) * 10000 + _convert_number(ram_state[45]) * 100 + _convert_number(ram_state[46])
    info["lives"] = ram_state[57]
    info["round"] = ram_state[47]


    # -nr 0 or rightclick