from .game_objects import GameObject, NoObject
from ._helper_methods import _convert_number
import sys

"""
RAM extraction for the game KANGUROO. Supported modes: ram.

"""

MAX_NB_OBJECTS = {'Player': 1, 'Player_Projectile': 1, 'Saucer': 5, 'Enemy_Projectile': 3}
                #   'Torpedos': 1}  # Asteroid count can get really high
# MAX_NB_OBJECTS_HUD = {'Player': 1, 'Player_Projectile': 1, 'Torpedos': 1, 'Life': 1, 'HUD': 1}
MAX_NB_OBJECTS_HUD = {'Player': 1, 'Player_Projectile': 1, 'Saucer': 5, 'Enemy_Projectile': 3,
                      'PlayerScore': 1, 'Lives': 1, 'Torpedos': 1, 'Remaining_Enemies': 1}
# MAX_NB_OBJECTS = MAX_NB_OBJECTS_HUD

class Player(GameObject):
    """
    The player figure i.e., the space ship.
    """

    def __init__(self):
        super(Player, self).__init__()
        self.visible = True
        self._xy = 77, 167
        self.wh = 15, 16
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


class Remaining_Enemies(GameObject):
    """
    The count display for the remaining Enemy Saucers in the current sector.
    """

    def __init__(self):
        super().__init__()
        self.rgb = 82, 126, 45

class PlayerScore(GameObject):
    """
    The player's score display (HUD).
    """

    def __init__(self):
        super().__init__()
        self.xy = 96, 3
        self.wh = 5, 9
        self.rgb = 236, 236, 236
        self.score = 0
        self.hud = True

    def __eq__(self, o):
        return isinstance(o, PlayerScore) and self.xy == o.xy

class Lives(GameObject):
    """
    The lives-indicator of the player.
    """

    def __init__(self):
        super().__init__()
        self.hud = True
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

    objects = [Player()] + [Player_Projectile()] + [NoObject()]*5 + [Enemy_Projectile()]*3

    if hud:
        objects += [PlayerScore()] + [Lives()] + [Torpedos()] + [Remaining_Enemies()]

    return objects

# levels: ram_state[36], total of 3 levels: 0,1 and 2

def _convert_x(rs):
    rss = [60, 94, 111, 128, 145, 162, 196] # ram_states for each lane
    xus = [40, 62, 73, 83, 93, 104, 126]    # x-pos for start of the lanes (up)
    xds = [-20, 33, 58, 83, 109, 136, 191]  # x-pos for end of the lanes (down)

    for i in range(6):
        if rss[i + 1] >= rs:
            xu = xus[i] + (xus[i + 1] - xus[i]) * (rs - rss[i]) / (rss[i + 1] - rss[i])
            xd = xds[i] + (xds[i + 1] - xds[i]) * (rs - rss[i]) / (rss[i + 1] - rss[i])
            return xu, xd

"""
X positions in BeamRider are indicated using a lane index. For calculating the exact
x position for an object, we need to extract xy positions for the two ends of
the lane (which are constant constant) and also the objects' y position, and then
use some mathematics (more detailed explanations in ram/BeamRider.pdf).

On the other hand, there are not a single cell is associated with the y position
of an object. As you see in the previous implementations for extracting y positions
for Saucers (that works fine for a short time of playing), it seems like the y
position should be extracted from ram_state[90:95], considering the order of numbers
in ram_state[25:31] (e.g. the y position of the enemy with the highest related value in
ram_state[25:31] should be extracted from ram_state[95]). This approach works well
until the player kills ca. 10 enemies. After that, the extracted order for cells in
ram_state[90:95] is not the correct order anymore. (e.g. in BeamRider_Y.png, the y
position for the enemy in the middle of screen has been assigned to another enemy which
has not entered the lane yet, and the y position for enemy projectile has bin considered
for the enemy which is recently entered to the field at the top of screen, between
3rd and 4th lanes)
"""

def _detect_objects_ram(objects, ram_state, hud=True):

    player = Player()
    player.xy = int(ram_state[41]*1.5)-115, 164
    objects[0] = player
    
    player_projectile = NoObject()
    if ram_state[49] == 35:
        player_projectile = Player_Projectile()
        y = ram_state[78] + 28
        xu, xd = _convert_x(ram_state[40])
        perspective_ratio = (y - 43) / 122
        x = xu + (xd - xu) * perspective_ratio
        player_projectile.xy = int(x - 3), int(y)
        player_projectile.wh = 8, 6
    objects[1] = player_projectile

    y_positions = ram_state[25:31]
    state_positions = range(0, 5)
    y_positions = [y_pos for y_pos in y_positions if y_pos < 255]
    y_positions = list(zip(y_positions, state_positions))
    y_positions.sort()
    # The x pos of the center line has the RAM value 128, that translates to 80 (gained from using the pure number value of the hex value, works like the score)
    # When enemies move forward, their position moves further outwards, while the RAM stays the same
    # Enemies always move down one of the lines, if they are not at the top
    # lanes from left to right
    #  1    2    3    4    5   6   7
    #  60   94  111  128  145 162 196
    for i in range(5):
        if ram_state[33+i] != 0:
            enemy = Saucer()

            lane = ram_state[33+i]
            
            y_pos = [x for x, y in enumerate(y_positions) if y[1] == i]
            if len(y_pos):
                y = 165 - ram_state[93+y_pos[0]]
            else:
                y = 43
            
            perspective_ratio = (y - 43) / 122
            
            if lane > 196:
                x = _convert_number(lane)
            else:
                xu, xd = _convert_x(lane)
                x = xu + (xd - xu) * perspective_ratio
            
            enemy.wh = round(10 * perspective_ratio) + 1, round(7 * perspective_ratio) + 1
            enemy.xy = round(x - 5 * perspective_ratio), y
            objects[2+i] = enemy
    
    for i in range(3):
        enemy_projectile = NoObject()
        if ram_state[30+i] < 255:
            enemy_projectile = Enemy_Projectile()

            lane = ram_state[38+i]
            # x = 0
            
            y = ram_state[30+i] - 61
            
            perspective_ratio = (y - 43) / 122
            
            if lane > 196:
                x = _convert_number(lane)
            else:
                xu, xd = _convert_x(lane)
                x = xu + (xd - xu) * perspective_ratio
            
            enemy_projectile.xy = int(x), int(y)
            enemy_projectile.wh = 2, 5
        objects[7+i] = enemy_projectile
    
    if hud:
        player_score = PlayerScore()
        player_score.score = _convert_number(ram_state[9]) \
            + 100 * _convert_number(ram_state[10]) \
            + 10000 * _convert_number(ram_state[11])
        player_score.xy = 61, 10
        player_score.wh = 46, 8
        objects[9] = player_score

        lives = NoObject()
        if ram_state[5] == 2:
            lives = Lives()
            lives.xy = 32, 183
            lives.wh = 14, 7
        elif ram_state[5] == 1:
            lives = Lives()
            lives.xy = 32, 183
            lives.wh = 5, 7
        objects[10] = lives

        torpedos = NoObject()
        if ram_state[83] == 3:
            torpedos = Torpedos()
            torpedos.xy = 128, 32
            torpedos.wh = 20, 8
        elif ram_state[83] == 2:
            torpedos = Torpedos()
            torpedos.xy = 136, 32
            torpedos.wh = 12, 8
        elif ram_state[83] == 1:
            torpedos = Torpedos()
            torpedos.xy = 144, 32
            torpedos.wh = 4, 8
        objects[11] = torpedos

        remaining_enemies = NoObject()
        if ram_state[84] >= 10 and ram_state[84] <= 15:
            remaining_enemies = Remaining_Enemies()
            remaining_enemies.xy = 20, 32
            remaining_enemies.wh = 11, 8
        elif ram_state[84] >= 0 and ram_state[84] <= 9:
            remaining_enemies = Remaining_Enemies()
            remaining_enemies.xy = 25, 32
            remaining_enemies.wh = 6, 8
        objects[12] = remaining_enemies


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
