from .game_objects import GameObject
from ._helper_methods import _convert_number
import sys
import numpy as np

"""
RAM extraction for the game GALAXIAN. Supported modes: ram.
"""
#TODO: Enemy Ships could be up to 42, but that does not happen in an unmodified game > which one should be saved?
MAX_NB_OBJECTS =  {'Player': 1, 'PlayerMissile': 1, 'EnemyShip': 35, 'DivingEnemy': 10, 'EnemyMissile': 20}
MAX_NB_OBJECTS_HUD =  {'Player': 1, 'PlayerMissile': 1, 'EnemyShip': 35, 'DivingEnemy': 10, 'EnemyMissile': 20, 'Score': 1, 'Round': 1, 'Lives': 1}

# enemy_missiles saves the enemy missiles according to at which ram position their x positon is saved 
enemy_missiles = [None] * 8

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
        self.y_ram_index = -1

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

#TODO Update to fit current state
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

    #TODO put lives at the end since it is a hud
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
                enemy_ship.x = 19 + ram_state[35] * 0.8 + np.ceil(j * 16.5)
            else:
                enemy_ship = None
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
    # enemy missiles deletion from objects
    missile_pos = np.where([isinstance(a, EnemyMissile) for a in objects])[0]
    if len(missile_pos) > 0:
        del objects[missile_pos[0]:missile_pos[-1] + 1]

    """
    The missiles are setting ram_state[25:32] as they decend, so these are used for the y calculation. 
    The idea here is that the missiles always use the first unused ram of ram_state[102 + i]
    """

    k = 0
    for i in range(25,33):
        nr = ram_state[i]
        nr_of_rockets = bin(nr).count("1")
        for j in range(0,nr_of_rockets):
            if enemy_missiles[k] != None and enemy_missiles[k].y_ram_index >= i and enemy_missiles[k].y_ram_index < i+1 :
                enemy_missiles[k].y_ram_index = enemy_missiles[k].y_ram_index + 0.10
            else:
                enemy_missiles[k] = EnemyMissile()
                enemy_missiles[k].y_ram_index = i
            k+=1

    # update the y 
    enemy_missiles_sorted_by_y = [i for i in enemy_missiles if i is not None]
    enemy_missiles_sorted_by_y.sort(key=lambda missile:missile.y_ram_index)
    generator = (i for i, v in enumerate(ram_state[25:32]) if v != 0)
    for i in range(len(enemy_missiles_sorted_by_y)):
        n = enemy_missiles.index(enemy_missiles_sorted_by_y[i]) # translate index i in the sorted list to the index in the general list
        next_missile_y = next(generator, None)

    for i in range(len(enemy_missiles)):
        if enemy_missiles[i] is None:
            continue
        enemy_missiles[i].y = 188-(33-enemy_missiles[i].y_ram_index) * 11
        enemy_missiles[i].x = ram_state[102 + i] + 11
        if enemy_missiles[i].y >= 184:
            enemy_missiles[i] = None
    objects.extend([i for i in enemy_missiles if i is not None])


def _detect_objects_galaxian_raw(info, ram_state):
    
    info["score"] = _convert_number(ram_state[44]) * 10000 + _convert_number(ram_state[45]) * 100 + _convert_number(ram_state[46])
    info["lives"] = ram_state[57]
    info["round"] = ram_state[47]



"""
Other Information:

ram 12-17 is another bitmap of the rows of enemies, but this time encoded differently:
    if the bits in a ram cell are numbered like this: 8 7 6 5 4 3 2 1 
    then a row of enemies is represented like this: 3 4 1 2 6 7 5 
    example: if a ram cell holds 01111011, the corresponding row of enemies looks like this: ○ ● ● ● ● ● ● (the leftmost one is missing)
    The benefit/use case of this representation in contrast to the other enemy bitmap is not clear at this point

ram 19-24 changes the pose of the enemy rows (the shorter or taller one and sometimes moved by one pixel along the x-axis)

ram 74-77 changes the direction of the diving enemies
ram 79-82 changes direction and color of diving enemies (so most likely the skin)
ram 86 seems to be related to the bitmap of the diving enemies, which is used when multiple enemies fall together and only use one x and y ram (often happens with one white and two red ones at the end of level 1 if only very few are left)
ram 94 affects the "fall rate" of diving enemies

"""