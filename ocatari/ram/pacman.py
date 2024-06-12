from .game_objects import GameObject
from ._helper_methods import _convert_number
import math
import sys

"""
RAM extraction for the game Ms. Pac-Man.
"""

# not sure about this one TODO: validate
MAX_NB_OBJECTS =  {'Player': 1, 'Ghost': 4, 'PowerPill': 4}
MAX_NB_OBJECTS_HUD =  {'Player': 1, 'Ghost': 4, 'PowerPill': 4, 'Score': 3, 'Life': 2}

gcolor = [(111, 111, 215), (144, 144, 252)]
ghost_vulnerable = False


class Player(GameObject):
    """
    The player figure: Ms. Pac-Man.
    """
    def __init__(self):
        super(Player, self).__init__()
        self._xy = 78, 103
        self.wh = 8, 16
        self.rgb = 210, 164, 74
        self.hud = False


class Ghost(GameObject):
    """
    The Ghosts.
    """
    
    def __init__(self):
        super(Ghost, self).__init__()
        super().__init__()
        self._xy = 79, 57
        self.wh = 8, 16
        self.rgb = 252, 144, 200
        self.hud = False


# class Fruit(GameObject):
#     """
#     The collectable fruits.
#     """
    
#     def __init__(self):
#         super(Fruit, self).__init__()
#         self._xy = 125, 173
#         self.wh = 9, 10
#         self.rgb = 252, 144, 200
#         self.hud = False


pps = [(6, 39), (6, 171), (150, 39), (150, 171)]
class PowerPill(GameObject):
    """
    The collectable fruits.
    """
    def __init__(self, x=0, y=0):
        super(PowerPill, self).__init__()
        self._xy = x, y
        self.wh = 4, 10
        self.rgb = 228, 111, 111
        self.hud = False


class Score(GameObject):
    """
    The player's score display (HUD).
    """
    
    def __init__(self):
        super(Score, self).__init__()
        self._xy = 96, 207
        self.wh = 6, 7
        self.rgb = 0, 0, 0
        self.hud = True


class Life(GameObject):
    """
    The indicator for remaining lives (HUD).
    """
    
    def __init__(self):
        super(Life, self).__init__()
        self._xy = 8, 217
        self.wh = 20, 6
        self.rgb = 72, 176, 110
        self.hud = True
        self.value = 3

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

    objects = [Player(), Ghost(), Ghost(), Ghost(), Ghost()]
    for ppxy in pps:
        objects.append(PowerPill(*ppxy))

    if hud:
        objects.extend([Life(), Score()])
    return objects

get_bin = lambda x: format(int(x), 'b').zfill(8)

def _detect_objects_ram(objects, ram_state, hud=True):
    player = objects[0]
    ghosts = objects[1:5]
    pcmn_invsbl = ram_state[59] in [96, 97, 160, 161]
    # player
    if pcmn_invsbl:
        if player is not None:
            objects[0] = None
    else:
        if player is None:
            player = Player()
            objects[0] = player
        player.xy = ram_state[49], 2*ram_state[89]+1
    # ghosts
    ghst_bs = get_bin(ram_state[26])
    global ghost_vulnerable
    for i, gi in enumerate(ghosts):
        gi.xy = ram_state[50+i], 2*ram_state[55+i]+25
    
    if ghst_bs[0] == "1":
        for gi in ghosts:
            gi.rgb = gcolor[int(ghst_bs[1])]
        ghost_vulnerable = True
    elif ghost_vulnerable:
        for gi in ghosts:
            gi.rgb = 252, 144, 200
        ghost_vulnerable = False
    # pps_o = objects[5:9]
    for i in range(4):
        if ghst_bs[2+i] == "0":
            objects[5+i] = None
        elif objects[5+i] == None:
            objects[5+i] = PowerPill(*pps[i])
    if hud:
        life = objects[9]
        nblives = ram_state[24]
        if nblives == 0:
            objects[9] = None
        else:
            if life is None:
                life = Life()
                objects[9] = life
            life.value = nblives
            life.wh = 4 + (nblives - 1) * 8, 6
        scorev = compute_score(ram_state[76], ram_state[78], ram_state[80])
        sco = objects[10]
        sco.value = scorev
        sco_len = 6 + (len(str(scorev))-1) * 8
        sco.wh = sco_len, 7
        sco._xy = 102 - sco_len, 207


def compute_score(units, hund, tenthou):
    un = units % 16
    diz = units // 16
    hun = hund % 16
    tho = hund // 16
    tentho = min(tenthou % 16, 9)
    return un + 10 * diz + 100 * hun + 1000 * tho \
            + 10000 * tentho 
