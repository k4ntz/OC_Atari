from .game_objects import GameObject
import sys

"""
RAM extraction for the game KANGUROO. Supported modes: ram.

"""

MAX_NB_OBJECTS = {'Player': 1, 'Player_Projectile':1, 'Torpedos': 1}  # Asteroid count can get really high
MAX_NB_OBJECTS_HUD = {'Life': 1, 'HUD': 1}

class Player(GameObject):
    """
    The player figure i.e., the space ship. 
    """
    
    def __init__(self):
        super(Player, self).__init__()
        self.visible = True
        self._xy = 77, 167
        self.wh = 15, 13
        self.rgb = 210, 210, 64
        self.hud = False


class Player_Projectile(GameObject):
    """
    The laser lariats that can be fired from the space ship. 
    """
    
    def __init__(self):
        super().__init__()
        self.rgb = 198, 108, 58


class Torpedos(GameObject):
    """
    The limited torpedoes that can be fired from the space ship. 
    """
    
    def __init__(self):
        super().__init__()
        self.rgb = 164, 89, 208


class Saucer(GameObject):
    """
    The White Enemy Saucers. 
    """
    
    def __init__(self):
        super().__init__()
        self.visible = True
        self._xy = 0, 0
        self.wh = 8, 5
        self.rgb = 236, 236, 236
        self.hud = False


class Rejuvenator(GameObject):
    """
    The Yellow Rejuvinators occasionally floating through the beam matrix. 
    """
    
    def __init__(self):
        super().__init__()
        self.rgb = 187, 187, 53


class Sentinel(GameObject):
    """
    The Sector Sentinel Ship, which appears once a sector has been cleared. 
    """
    
    def __init__(self):
        super().__init__()
        self.rgb = 184, 50, 50


class Blocker(GameObject):
    """
    The Green Blocker Ships (sector 6). 
    """
    
    def __init__(self):
        super().__init__()
        self.rgb = 135, 183, 84


class Jumper(GameObject):
    def __init__(self):
        super().__init__()
        self.rgb = None


class Charger(GameObject):
    """
    The Blue Chargers (sector 10). 
    """
    
    def __init__(self):
        super().__init__()
        self.rgb = None


class Bouncecraft(GameObject):
    """
    The Green Bounce Craft (sector 8). 
    """
    
    def __init__(self):
        super().__init__()
        self.rgb = None


class Chriper(GameObject):
    """
    The Yellow Chirper Ships (sector 4). 
    """
    
    def __init__(self):
        super().__init__()
        self.rgb = None


class Rock(GameObject):
    """
    The Brown Space Debris (sector 2). 
    """
    
    def __init__(self):
        super().__init__()
        self.rgb = 134, 134, 29


class Torpedos_Available(GameObject):
    """
    The torpedoe availability display.
    """
    
    def __init__(self):
        super().__init__()
        self.rgb = 104, 25, 154


class Enemy_Projectile(GameObject):
    """
    Enemy projectiles. 
    """
    
    def __init__(self):
        super().__init__()
        self.rgb = 164, 89, 208


class HUD(GameObject):
    def __init__(self):
        super().__init__()
        self.rgb = 210, 164, 74


class Enemy_Amount(GameObject):
    """
    The count display for the remaining Enemy Saucers in the current sector. 
    """
    
    def __init__(self):
        super().__init__()
        self.rgb = 82, 126, 45


class Life(GameObject):
    """
    The lives-indicator of the player. 
    """
    
    def __init__(self):
        super().__init__()
        self.rgb = 210, 210, 64


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


def _init_objects_ram(hud=True):
    """
    (Re)Initialize the objects
    """

    objects = [Player()]

    return objects

# levels: ram_state[36], total of 3 levels: 0,1 and 2
def _detect_objects_ram(objects, ram_state, hud=True):
    objects.clear()

    player = Player()
    objects.append(player)
    player.xy = _get_x_position(ram_state[41]), 167

    for i in range(7):
        if ram_state[33+i] != 0:
            enemy = Saucer()
            objects.append(enemy)
            enemy.xy = _get_x_position(ram_state[33+i]), (ram_state[25+i]*0.5) + 15
            enemy.wh = 2, 2

    return objects


def _detect_objects_beamrider_raw(info, ram_state):
    player_x = ram_state[41]
    enemy_x = ram_state[33:40]
    enemy_y = ram_state[25:32]
    projectile_x = ram_state[40]
    projectile_y = ram_state[32]
    # ram_state[42:49]no clue? kills player
    # ram_state[49] projectile; 0 shootable, 35 already shot
    # ram_state[0] sector
    # ram_state[5] lives: renders up to 13
    # ram_state[16] gamestatus: 1 = neutral, 2 = fighting, 3 = sentinel, 4 = transition
    # ram_state[83] torpedo amount
    # ram_state[83] enemy amount
    # 93-95 irgend was mit entfernung von Gegnern. 93 am weitesten entfernt 95 am nächsten
    return player_x + enemy_x, enemy_y + projectile_x, projectile_y


def _get_x_position(ramstate):
    """
    converts the x Position in the RAM to the proper Position on screen
    """
    pos = 26
    for i in range(ramstate-94):
        if i % 2 == 0:
            pos = pos+1
        else:
            pos = pos+2
    return pos
