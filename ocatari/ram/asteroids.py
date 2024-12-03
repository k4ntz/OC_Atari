from ._helper_methods import _convert_number
from .game_objects import GameObject, NoObject
import sys
"""
RAM extraction for the game ASTEROIDS. Supported modes: raw

Revised is missing the x-Position for Asteroids and Player. The RAM states for these values are found (look at raw) but
they were not interpretable. One x Value corresponds to multiple positions on the rendered image. So either there is
another RAM state which separates them into quadrants or the x-Axis is moving.
"""

MAX_NB_OBJECTS = {'Player': 1, 'Asteroid': 30,'PlayerMissile': 2}  # Asteroid count can get really high
MAX_NB_OBJECTS_HUD = {'Player': 1, 'Asteroid': 30,'PlayerMissile': 2, 'Lives': 1, 'PlayerScore': 1}


class Player(GameObject):
    """
    The player figure i.e., the space ship on patrol. 
    """
    
    def __init__(self):
        super().__init__()
        self._xy = 84, 99
        self.wh = 5, 10
        self.rgb = 240, 128, 128
        self.hud = False
        self.orientation = 0

    @property
    def xy(self):
        return self._xy
    
    @xy.setter
    def xy(self, value):
        self._xy = value

    @property
    def _nsrepr(self):
        return self.x, self.y, self.orientation
    
    @property
    def _ns_meaning(self):
        return "x, y, o"

    

class Asteroid(GameObject):
    """
    The asteroid boulders. 
    """
    
    def __init__(self):
        super().__init__()
        self._xy = 8, 87
        self.wh = 16, 28
        self.rgb = 180, 122, 48
        self.hud = False

    @property
    def xy(self):
        return self._xy
    
    @xy.setter
    def xy(self, value):
        self._xy = value


class PlayerMissile(GameObject):
    """
    The photon torpedoes that can be fired from the space ship. 
    """
    
    def __init__(self):
        super().__init__()
        self._xy = 0, 0
        self.wh = 1, 2
        self.rgb = 117, 181, 239
        self.hud = False

    @property
    def xy(self):
        return self._xy
    
    @xy.setter
    def xy(self, value):
        self._xy = value


class PlayerScore(GameObject):
    """
    The player's score display (HUD).
    """
    
    def __init__(self):
        super().__init__()
        self._xy = 68, 5
        self.rgb = 184, 50, 50
        self.wh = 12, 10
        self.hud = True

    @property
    def xy(self):
        return self._xy
    
    @xy.setter
    def xy(self, value):
        self._xy = value

    def __eq__(self, o):
        return isinstance(o, PlayerScore) and self.xy == o.xy


class Lives(GameObject):
    """
    The indicator for remaining lives of the player (HUD). 
    """
    
    def __init__(self):
        super().__init__()
        self._xy = 132, 5
        self.rgb = 184, 50, 50
        self.wh = 12, 10
        self.hud = True

    @property
    def xy(self):
        return self._xy
    
    @xy.setter
    def xy(self, value):
        self._xy = value

class NoObjectPlayer(NoObject):
    """
    A placeholder class for empty slots where no game object is present.
    """
    def __init__(self):
        super().__init__()
        self.orientation = 0

    @property
    def xy(self):
        return self._xy
    
    @xy.setter
    def xy(self, value):
        self._xy = value

    @property
    def _nsrepr(self):
        return self.x, self.y, self.orientation
    
    @property
    def _ns_meaning(self):
        return "x, y, o"


asteroids_colors = {"brown": [180, 122, 48], "purple": [104, 72, 198], "yellow": [136, 146, 62],
                    "lightyellow": [187, 187, 53], "grey": [214, 214, 214], "lightblue": [117, 181, 239],
                    "pink": [184, 70, 162], "red": [184, 50, 50]}

player_missile_colors = {"blue": [117, 181, 239], "red": [240, 128, 128]}

def _init_objects_ram(hud=False):
    """
    (Re)Initialize the objects
    """
    objects = [Player()]
    objects.extend([NoObject()] * 33)
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
    
    if ram_state[74] != 224:
        if ram_state[60]%16 == 4:
            player.xy = (_x_position(ram_state[73]) - 1, 100 + (2 * (ram_state[74] - 41)))
            player.wh = 6, 10
        elif ram_state[60]%16 == 12:
            player.xy = (_x_position(ram_state[73]) + 1, 100 + (2 * (ram_state[74] - 41)))
            player.wh = 6, 10
        elif 2 > ram_state[60]&8 > 6:
            player.xy = (_x_position(ram_state[73]), 100 + (2 * (ram_state[74] - 41)))
            player.wh = 5, 10
        else:
            player.xy = (_x_position(ram_state[73]), 100 + (2 * (ram_state[74] - 41)))
            player.wh = 6, 10
    else:
        player = NoObjectPlayer()
    
    if isinstance(player, Player):
        player.orientation = ram_state[60]%16

    objects[0] = player

    ast_slots = objects[1:31]
    ast_list = [3,4,5,6,7,8,9,12,13,14,15,16,17,18,19]
    for i in range(len(ast_list)):
        if ram_state[ast_list[i]+18] and not ram_state[ast_list[i]]&128:
            if isinstance(ast_slots[i], NoObject):
                ast_slots[i] = Asteroid()
            ast = ast_slots[i]
            x = int(_x_position(ram_state[ast_list[i]+18]))
            y = 184 - 2 * (80 - ram_state[ast_list[i]])
            ast.xy = (x, y)
            if ram_state[ast_list[i]+36]&127 < 32:
                w, h = 16, 28
                if x >= 160-16:
                    w -= (x+16)-160
                if y >= 194-28:
                    h -= (y+28)-194
                if w < -200 or h < -200:
                    ast_slots[i] = NoObject()
                else:
                    ast.wh = w, h
            elif ram_state[ast_list[i]+36]&127 < 48:
                ast.xy = (x-1, y-2)
                w, h = 8, 15
                if x >= 160-8:
                    w -= (x+7)-160
                if y >= 194-15:
                    h -= (y+13)-194
                if w < -200 or h < -200:
                    ast_slots[i] = NoObject()
                else:
                    ast.wh = w, h
            else:
                ast.xy = (x-1, y-1)
                w, h = 4, 8
                if x >= 160-4:
                    w -= (x+3)-160
                if y >= 194-8:
                    h -= (y+7)-194
                if w < -200 or h < -200:
                    ast_slots[i] = NoObject()
                else:
                    ast.wh = w, h
        else:
            ast_slots[i] = NoObject()
    objects[1:31] = ast_slots
    
    if ram_state[83] and not ram_state[86]&128:
        if isinstance(objects[31], NoObject):
            objects[31] = PlayerMissile()
        miss = objects[31]
        miss.xy = (_x_position(ram_state[83]) + 1, 175 - 2 * (80 - ram_state[86]) + 2)
    else:
        objects[31] = NoObject()


    if ram_state[84] and not ram_state[87]&128:
        if isinstance(objects[32], NoObject):
            objects[32] = PlayerMissile()
        miss = objects[32]
        miss.xy = (_x_position(ram_state[84]) + 1, 175 - 2 * (80 - ram_state[87]) + 2)
    else:
        objects[32] = NoObject()

    if hud:
        if ram_state[61] >= 16:
            if isinstance(objects[33], NoObject):
                objects[33] = PlayerScore()
            score = objects[33]
            score.xy = (4, 5)
            score.wh = 76, 10
        elif ram_state[61]:
            if isinstance(objects[33], NoObject):
                objects[33] = PlayerScore()
            score = objects[33]
            score.xy = (20, 5)
            score.wh = 60, 10
        elif ram_state[62] >= 16:
            if isinstance(objects[33], NoObject):
                objects[33] = PlayerScore()
            score = objects[33]
            score.xy = (36, 5)
            score.wh = 44, 10
        elif ram_state[62]:
            if isinstance(objects[33], NoObject):
                objects[33] = PlayerScore()
            score = objects[33]
            score.xy = (52, 5)
            score.wh = 28, 10
        else:
            if isinstance(objects[33], NoObject):
                objects[33] = PlayerScore()
            score = objects[33]
            score.xy = (68, 5)
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
