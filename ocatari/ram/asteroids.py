from ._helper_methods import _convert_number
from .game_objects import GameObject
import sys

"""
RAM extraction for the game ASTEROIDS. Supported modes: raw

Revised is missing the x-Position for Asteroids and Player. The RAM states for these values are found (look at raw) but
they were not interpretable. One x Value corresponds to multiple positions on the rendered image. So either there is
another RAM state which separates them into quadrants or the x-Axis is moving.
"""

MAX_NB_OBJECTS = {'Player': 1, 'Asteroids':30,'PlayerMissile': 2}  # Asteroid count can get really high
MAX_NB_OBJECTS_HUD = {'Lives': 1, 'PlayerScore': 1}


class Player(GameObject):
    """
    The player figure i.e., the space ship on patrol. 
    """
    
    def __init__(self):
        super(Player, self).__init__()
        self._xy = 84, 99
        self.wh = 5, 10
        self.rgb = 240, 128, 128
        self.hud = False
        self.orientation = 0


class Asteroid(GameObject):
    """
    The asteroid boulders. 
    """
    
    def __init__(self):
        super(Asteroid, self).__init__()
        self._xy = 8, 87
        self.wh = 16, 28
        self.rgb = 180, 122, 48
        self.hud = False


class PlayerMissile(GameObject):
    """
    The photon torpedoes that can be fired from the space ship. 
    """
    
    def __init__(self):
        super(PlayerMissile, self).__init__()
        self._xy = 0, 0
        self.wh = 1, 2
        self.rgb = 117, 181, 239
        self.hud = False


class PlayerScore(GameObject):
    """
    The player's score display (HUD).
    """
    
    def __init__(self):
        super(PlayerScore, self).__init__()
        self._xy = 68, 5
        self.rgb = 184, 50, 50
        self.wh = 12, 10
        self.hud = True

    def __eq__(self, o):
        return isinstance(o, PlayerScore) and self.xy == o.xy


class Lives(GameObject):
    """
    The indicator for remaining lives of the player (HUD). 
    """
    
    def __init__(self):
        super(Lives, self).__init__()
        self._xy = 132, 5
        self.rgb = 184, 50, 50
        self.wh = 12, 10
        self.hud = True


asteroids_colors = {"brown": [180, 122, 48], "purple": [104, 72, 198], "yellow": [136, 146, 62],
                    "lightyellow": [187, 187, 53], "grey": [214, 214, 214], "lightblue": [117, 181, 239],
                    "pink": [184, 70, 162], "red": [184, 50, 50]}

player_missile_colors = {"blue": [117, 181, 239], "red": [240, 128, 128]}


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
    objects = [Player()]
    objects.extend([None] * 33)
    if hud:
        objects.extend([Lives(), PlayerScore()])
    return objects


def _detect_objects_ram(objects, ram_state, hud=False):
    """
       For all objects:
       (x, y, w, h, r, g, b)
    """

    # rotation == 60 16pos
    # x position 4ls bits are set x positions 
    # 4ms bits are off sets 1000 == x+8, 0101 ==  x - 5, 1111 == x + 8 -7-> x+1

    player = Player()
    objects[0] = player

    if ram_state[74] != 224:
        if ram_state[60]%16 == 4:
            player.xy = _x_position(ram_state[73])-1, 100 + (2 * (ram_state[74] - 41))
            player.wh = 6, 10
        elif ram_state[60]%16 == 12:
            player.xy = _x_position(ram_state[73])+1, 100 + (2 * (ram_state[74] - 41))
            player.wh = 6, 10
        elif 2 > ram_state[60]&8 > 6:
            player.xy = _x_position(ram_state[73]), 100 + (2 * (ram_state[74] - 41))
            player.wh = 5, 10
        else:
            player.xy = _x_position(ram_state[73]), 100 + (2 * (ram_state[74] - 41))
            player.wh = 6, 10
    else:
        objects[0] = None
    
    player.orientation = ram_state[60]%16

    ast_list = [3,4,5,6,7,8,9,12,13,14,15,16,17,18,19]
    for i in range(len(ast_list)):
        # if not ram_state[ast_list[i]] == 224:
        # 0010 1111
        # 1111 0010
        if ram_state[ast_list[i]+18] and not ram_state[ast_list[i]]&128:
            ast2 = None
            ast = Asteroid()
            objects[1+i] = ast
            x = int(_x_position(ram_state[ast_list[i]+18]))
            y = 184 - 2 * (80 - ram_state[ast_list[i]])
            if ram_state[ast_list[i]+36]&127 < 32:
                split = False
                ast.xy = x, y
                w, h = 16, 28
                if x >= 160-16:
                    w -= (x+16)-160
                    split = True
                if y >= 194-28:
                    h -= (y+28)-194
                    split = True
                if w < 0 or h < 0:
                    ast = None
                else:
                    ast.wh = w, h
                if split and 16-w > 0 and 28-h > 0:
                    ast2 = Asteroid()
                    objects[16+i] = ast2
                    if w == 16:
                        ast2.xy = x, 18
                        ast2.wh = 16, 28-h
                    elif h == 28:
                        ast2.xy = 0, y
                        ast2.wh = 16-w, 28
                    else:
                        ast2.xy = 0, 18
                        ast2.wh = 16-w, 28-h
                else:
                    objects[16+i] = None

            elif ram_state[ast_list[i]+36]&127 < 48:
                split = False
                ast.xy = x-1, y-2
                w, h = 8, 15
                if x >= 160-8:
                    w -= (x+7)-160
                    split = True
                if y >= 194-15:
                    h -= (y+13)-194
                    split = True
                if w < 0 or h < 0:
                    ast = None
                else:
                    ast.wh = w, h
                if split and 8-w > 0 and 15-h > 0:
                    ast2 = Asteroid()
                    objects[16+i] = ast2
                    if w == 8:
                        ast2.xy = x-1, 18
                        ast2.wh = 8, 15-h
                    elif h == 15:
                        ast2.xy = 0, y-2
                        ast2.wh = 8-w, 15
                    else:
                        ast2.xy = 0, 18
                        ast2.wh = 8-w, 15-h
                else:
                    objects[16+i] = None
            else:
                split = False
                ast.xy = x-1, y-1
                w, h = 4, 8
                if x >= 160-4:
                    w -= (x+3)-160
                    split = True
                if y >= 194-8:
                    h -= (y+7)-194
                    split = True
                if w < 0 or h < 0:
                    ast = None
                else:
                    ast.wh = w, h
                if split and 4-w > 0 and 8-h > 0:
                    ast2 = Asteroid()
                    objects[16+i] = ast2
                    if w == 4:
                        ast2.xy = x-1, 18
                        ast2.wh = 4, 15-h
                    elif h == 8:
                        ast2.xy = 0, y-1
                        ast2.wh = 8-w, 8
                    else:
                        ast2.xy = 0, 18
                        ast2.wh = 4-w, 8-h
                else:
                    objects[16+i] = None
            if ast is not None:
                w1, h1 = ast.wh
                if w1 < 0:
                    print(w1, "wtf w1?")
                if h1 < 0:
                    print(h1, "wtf h1?")
            if ast2 is not None:
                w2, h2 = ast2.wh
                if w2 < 0:
                    print(w2, "wtf w2?")
                if h2 < 0:
                    print(h2, "wtf h2?")
        else:
            objects[1+i] = None
            objects[16+i] = None
    
    if ram_state[83] and not ram_state[86]&128:
        miss = PlayerMissile()
        objects[16] = miss
        miss.xy = _x_position(ram_state[83]) + 1, 175 - 2 * (80 - ram_state[86]) + 2
    else:
        objects[16] = None


    if ram_state[84] and not ram_state[87]&128:
        miss = PlayerMissile()
        objects[17] = miss
        miss.xy = _x_position(ram_state[84]) + 1, 175 - 2 * (80 - ram_state[87]) + 2
    else:
        objects[17] = None

    if hud:
        if ram_state[61] >= 16:
            score = PlayerScore()
            objects[-1] = score
            score.xy = 4, 5
            score.wh = 76, 10
        elif ram_state[61]:
            score = PlayerScore()
            objects[-1] = score
            score.xy = 20, 5
            score.wh = 60, 10
        elif ram_state[62] >= 16:
            score = PlayerScore()
            objects[-1] = score
            score.xy = 36, 5
            score.wh = 44, 10
        elif ram_state[62]:
            score = PlayerScore()
            objects[-1] = score
            score.xy = 52, 5
            score.wh = 28, 10
        else:
            score = PlayerScore()
            objects[-1] = score
            score.xy = 68, 5
            score.wh = 12, 10



def _x_position(value):
    ls = value&15
    add = 8*((value>>7)&1)
    sub = (value>>4)&7
    if value == 0:
        return 64
    elif value == 1:
        return 4
    elif ls%2 == 0:
        mult = (ls/2)-1
        return 97 + 15 * mult + add - sub
    elif ls%2 == 1:
        mult = ((ls-1)/2)-1
        return 10 + 15 * mult + add - sub

def _augment_info_asteroids_ram(info, ram_state):
    """
    For all objects:
    (x, y, w, h, r, g, b)
    """
    objects = {}
    if ram_state[74] <= 80:
        objects["player"] = 81 - (2 * (ram_state[77])), 100 + (2 * (ram_state[74] - 41)), 10, 10, 240, 128, 128
        print("Player Pos: " + str(81 - round(1.5 * ram_state[77])) + " " + str(100))

    for i in range(16):
        if ram_state[3 + i] != 0 and ram_state[21 + 1] != 0:
            if ram_state[21 + i] <= 160:
                prev_y = ram_state[3 + i] % 80
                x, y = ram_state[21 + i], 210 - round(prev_y * 2.5)
                # print("x: " + str(x) + " y: " + str(y) + " i: " + str(i))
                objects[f"asteroi_{i}"] = x, y, 16, 28, 255
    # objects["asteroid"] = 0, round(ram_state[3] * 2.625), 16, 28, 0, 0, 0
    info["score"] = _convert_number(ram_state[61]) * 1000 + _convert_number(ram_state[62]) * 10
    info["objects"] = objects


def _detect_objects_asteroids_raw(info, ram_state):
    """
    Actions:
    0: NOP
    1: shoot
    2: move  forward
    3: rotate right
    4: rotate left
    5: random teleport
    y = 0 top
    y = 85 bottom
    """
    info["player_x"] = ram_state[73]    # starts at x = 29
    info["player_y"] = ram_state[74]    # starts at y = 41
    info["diff_to_start_x"] = ram_state[77]     # starts at 255, goes down if go to right and up to the left
    info["player_direction"] = ram_state[60]    # 64: looking up, 78: up and right, 76: to the right, 74: down and right
    # 72: down, 70: down and left, 68: left, 66: up and left
    info["score_high"] = _convert_number(ram_state[61])
    info["score_low"] = _convert_number(ram_state[62])  # 153 = 990 at 160 again 0
    info["score"] = _convert_number(ram_state[61]) * 1000 + _convert_number(ram_state[62]) * 10
    info["player_missile_1_x"] = ram_state[83]  # beginning x = 253, y = 224
    info["player_missile_2_x"] = ram_state[84]  # blue one
    info["player_missile_1_y"] = ram_state[86]
    info["player_missile_2_y"] = ram_state[87]
    info["player_missile_1_dir"] = ram_state[89]    # 0 if not flying
    info["player_missile_2_dir"] = ram_state[90]
    info["asteroid_1"] = {ram_state[21]: ram_state[3]}
    info["asteroid_2"] = {ram_state[22]: ram_state[4]}
    info["asteroid_3"] = {ram_state[23]: ram_state[5]}
    info["asteroid_4"] = {ram_state[24]: ram_state[6]}
    info["asteroid_5"] = {ram_state[25]: ram_state[7]}
    info["asteroid_6"] = {ram_state[26]: ram_state[8]}
    info["asteroid_7"] = {ram_state[27]: ram_state[9]}
    info["asteroid_8"] = {ram_state[28]: ram_state[10]}
    info["asteroid_9"] = {ram_state[29]: ram_state[11]}
    info["asteroid_10"] = {ram_state[30]: ram_state[12]}
    info["asteroid_11"] = {ram_state[31]: ram_state[13]}
    info["asteroid_12"] = {ram_state[32]: ram_state[14]}
    info["asteroid_13"] = {ram_state[33]: ram_state[15]}
    info["asteroid_14"] = {ram_state[34]: ram_state[16]}
    info["asteroid_15"] = {ram_state[35]: ram_state[17]}
    info["asteroid_16"] = {ram_state[36]: ram_state[18]}
    info["asteroid_17"] = {ram_state[37]: ram_state[19]}
    info["asteroid_variation"] = ram_state[39:57]
