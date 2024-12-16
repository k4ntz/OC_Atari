from .game_objects import GameObject, NoObject
import numpy as np
from termcolor import colored
import sys

"""
RAM extraction for the game Space Invaders.
"""

MAX_NB_OBJECTS = {'Player': 1, 'Shield': 3,
                  'Bullet': 3, 'Satellite': 1, 'Alien': 36}
MAX_NB_OBJECTS_HUD = {'Player': 1, 'Shield': 3, 'Bullet': 3,
                      'Satellite': 1, 'Alien': 36, 'P1Score': 1, 'P2Score': 1, 'Lives': 1}


def make_bitmap(alien_states):
    emptc = 6 - int(max(alien_states)).bit_length()  # nb empty columns
    return [(format(el, '06b')[emptc:] + "0" * emptc) for el in alien_states], emptc


class Player(GameObject):
    """
    The player figure i.e., the laser cannon.
    """

    def __init__(self, num=1):
        super().__init__()
        if num == 1:
            self.rgb = 92, 186, 92  # green
        else:
            self.rgb = 162, 134, 56  # yellow
        self.player_num = num
        self._xy = 0, 185
        self.wh = 7, 10
        self.hud = False


class Alien(GameObject):
    """
    The Space Invaders.
    """

    def __init__(self):
        super().__init__()
        self.rgb = 134, 134, 29
        self._xy = 0, 0
        self.wh = 8, 10
        self.hud = False


class Satellite(GameObject):
    """
    The Command Alien Ship.
    """

    def __init__(self):
        super().__init__()
        self.rgb = 151, 25, 122
        self._xy = 0, 0
        self.wh = 7, 8
        self.hud = False


class Shield(GameObject):
    """
    The shields between the player's cannon and the Space Invaders.
    """

    def __init__(self):
        super().__init__()
        self.rgb = 181, 83, 40
        self._xy = 0, 0
        self.wh = 8, 18
        self.hud = False


class Bullet(GameObject):
    """
    The player's laser beams and enemy laser bombs.
    """

    def __init__(self):
        super().__init__()
        self.rgb = 142, 142, 142
        self._xy = 0, 0
        self.wh = 1, 10
        self.hud = False


class P1Score(GameObject):
    """
    The player's score display (HUD).
    """

    def __init__(self, x=0):  # , num,
        super().__init__()
        self.rgb = 92, 186, 92
        self._xy = x, 10
        self.wh = 60, 10
        self.hud = True


class P2Score(GameObject):
    """
    The 2nd player's score display (HUD).
    """

    def __init__(self, x=0):  # , num,
        super().__init__()
        self.rgb = 162, 134, 56
        self._xy = x, 10
        self.wh = 60, 10
        self.hud = True


class Lives(GameObject):
    """
    The indicator for the player's remaining lives (HUD).
    """

    def __init__(self):
        super().__init__()
        self.rgb = 162, 134, 56
        self._xy = 84, 185
        self.wh = 12, 10
        self.hud = True


def _detect_objects_spaceinvaders_raw(info, ram_state):
    info["aliens"] = ram_state[16:24]
    info["x_positions"] = ram_state[26:31]
    info["shields"] = ram_state[43:70]
    info["lives"] = ram_state[73]
    info["bullets"] = ram_state[81:89]
    info["value"] = ram_state[90]  # some value changing repeatedly
    info["score"] = ram_state[102:106]
    # info["aliens_y"] = ram_state[16]
    # # ram_state[16] has also y of frame of players with shields together
    #
    # info["number_enemies"] = ram_state[17]  # number of alive aliens. if they are less the make the game quicker
    #
    # # positions of enemies from left to right are the individual, set bits from right to left
    # # rows are counted from bottom
    # # the two msb-bits are to be discarded. they remain 0
    # info["row_1"] = ram_state[18]
    # info["row_2"] = ram_state[19]
    # info["row_3"] = ram_state[20]
    # info["row_4"] = ram_state[21]
    # info["row_5"] = ram_state[22]
    # info["row_6"] = ram_state[23]
    # # ram[32:38] have the same value as ram[17:23] initialized. sense still not known
    #
    # info["visibility_players_shields"] = ram_state[24]  # for player see 72
    #
    # info["aliens_x"] = ram_state[26]  # x of all aliens is common
    # info["shields_x"] = ram_state[27]  # shield_left is reference
    # info["player_green_x"] = ram_state[28]  # begins with 35. (0 < player_x < 255)
    # info["player_yellow_x"] = ram_state[29]  # begins with 117. (0 < player_x < 255)
    # info["satellite_x"] = ram_state[30]
    #
    # info["graphics"] = ram_state[42]  # graphics of players being destroyed and setting ones to score
    #
    # info["shields"] = ram_state[43:70]  # the 3 shields. they are represented in the same order as in the ram (from
    # left to right)
    # info["shield_left"] = ram_state[43:52]  # represented row by row in ram as single cell by another in same order
    # info["shield_middle"] = ram_state[52:61]  # represented row by row in ram as single cell by another in same order
    # info["shield_right"] = ram_state[61:70]  # represented row by row in ram as single cell by another in same order
    #
    # info["objects_colours"] = ram_state[71]  # colours
    # info["changing_symbols_enemies"] = ram_state[72]  # when destroyed
    #
    # info["lives"] = ram_state[73]  # you have 3 lives from beginning. they decrease and after 1 it gets set on 3
    #
    # info["temporal_reference"] = ram_state[74]  # works as temporal reference for the game
    #
    # # bullets
    # info["bullet_1_enemy_y"] = ram_state[81]
    # info["bullet_2_enemy_y"] = ram_state[82]
    # info["bullet_1_enemy_x"] = ram_state[83]
    # info["bullet_2_enemy_x"] = ram_state[84]
    # info["bullet_player_green_y"] = ram_state[85]
    # info["bullet_player_yellow_y"] = ram_state[86]
    # info["bullet_player_green_x"] = ram_state[87]
    # info["bullet_player_yellow_x"] = ram_state[88]
    # # you get able to shoot the other bullet, once the flying one disappears,
    #
    # # for an array-value for score there is two digits and arithmetic transfer(like from ram_state[104]) gets added
    # # to most significant digits (ram_state[102])
    # info["score_player_green"] = {ram_state[102], ram_state[104]}  # score is saved in hexadecimal in this order
    # info["score_player_yellow"] = {ram_state[103], ram_state[105]}  # score is saved in hexadecimal
    # # 200 points for destroying satellite dish
    # # x*5 points for destroying an alien from row_x


def _init_objects_ram(hud=False):
    """
    (Re)Initialize the objects
    """
    sat = NoObject()
    objects = [Player(1)] + [Shield() for _ in range(3)] + [Bullet() for _ in range(3)] + \
        [sat] + [Alien() for _ in range(36)]

    if hud:
        objects.extend([P1Score(4), P2Score(84), Lives()])

    for i, shield in enumerate(objects[1:4]):
        shield.xy = 42 + i * 32, 157
    return objects


def _detect_objects_ram(objects, ram_state, hud=False):
    player = objects[0]
    shields = objects[1:4]
    bullets = objects[4:7]
    satellite = objects[7]
    aliens = objects[8:44]

    player.xy = ram_state[28] - 1, 185
    # updating positions of aliens
    x, y = ram_state[26], ram_state[16]

    bitmap, emptc = make_bitmap(ram_state[18:24])

    if sum(ram_state[18:24]) == 378:
        for s in shields:
            s.visible = True
    # aliens (permanent) deletion from array aliens:
    for i in range(6):
        for j in range(6):
            # enemies alive are saved in ram_state[18:24]
            if aliens[35 - (i * 6 + j)] and not int(bitmap[i][j]):
                objects[43 - (i * 6 + j)] = NoObject()
            elif not aliens[35 - (i * 6 + j)] and int(bitmap[i][j]):
                # 5 = max(range(6)) so we are counting lines in the other way around
                objects[43 - (i * 6 + j)] = Alien()
    for i in range(6):
        for j in range(6):
            alien = aliens[i * 6 + j]
            if alien:
                aliens[i * 6 + j].xy = x - 1 + \
                    (j - emptc) * 16, 31 + y * 2 + i * 18
                if alien and alien.xy[1] + alien.wh[1] >= 157:
                    for s in range(3):
                        if shields[s]:
                            shields[s].visible = False
    upper_y = 0
    lower_y = 16
    for i in range(3):
        for j in range(9):
            if ram_state[43 + i * 9 + j] != 0:
                upper_y = j * 2
                break
        for j in range(9):
            if ram_state[43 + (i + 1) * 9 - (j + 1)] != 0:
                lower_y = j * 2
                break
        objects[1+i].xy = 42 + i * 32, 157 + upper_y
        objects[1+i].wh = 8, 18 - upper_y - lower_y
    # determining if bullets are visible
    bullets_visible = [False, False, False]
    for i in range(2):
        # and not(ram_state[74] % 2)
        bullets_visible[i] = 20 < bullets[i].xy[1] < 195
    bullets_visible[2] = 20 < bullets[2].xy[1] < 195  # and ram_state[74] % 2
    # appending bullets to objects
    for i in range(3):
        if bullets_visible[i]:
            if not bullets[i]:
                bullet = Bullet()
                objects[4+i] = bullet
                bullets[i] = bullet
        else:
            if bullets[i]:
                objects[4+i] = NoObject()
        if i < 2:
            bullets[i].xy = ram_state[83 + i] - 2, 2 * ram_state[81 + i] + 3
            if bullets[i].xy[1] < 194:
                if bullets[i].xy[1] + bullets[i].wh[1] > 195:
                    bullets[i].wh = bullets[i].wh[0], 195 - \
                        bullets[i].xy[1] - 1
                else:
                    bullets[i].wh = 1, 10
        else:
            bullets[2].xy = ram_state[87] - 2, 2 * \
                ram_state[85] + 3  # for player
    if ram_state[30] and ram_state[30] != 180:
        if not satellite:
            satellite = Satellite()
            objects[7] = satellite
        satellite.xy = ram_state[30] - 1, 12
        if hud:
            for s in range(2):
                objects[44+s].visible = False
    else:
        if satellite in objects:
            objects[7] = NoObject()
        if hud:
            for s in range(2):
                objects[44+s].visible = True
    if hud:
        objects[46].visible = bool(ram_state[120])  # lives appear
        objects[46].value = ram_state[73]  # nb lives
    return objects
