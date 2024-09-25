from .game_objects import GameObject

"""
RAM extraction for the game Frogger.

"""

MAX_NB_OBJECTS = {'Frog': 1}
MAX_NB_OBJECTS_HUD = {'Frog': 1}

class Frog(GameObject):
    """
    The player figure i.e., the frog. 
    """
    
    def __init__(self):
        super(Frog, self).__init__()
        self._xy = 0, 0
        self.wh = 7, 7
        self.rgb = 110, 156, 66
        self.hud = False

def _init_objects_ram(hud=False):
    """
    (Re)Initialize the objects
    """
    return [Frog()]

def _detect_objects_ram(objects, ram_state, hud=False):
    """
    For all objects:
    (x, y, w, h, r, g, b)
    """
    f = objects[0]
    print(f.orientation)
    f.x = ram_state[48] - 1
    if ram_state[44] == 255:
        f.y = 171
    elif ram_state[44] == 5:
        f.y = 95
    else:
        f.y = - 13 * ram_state[44] + 161