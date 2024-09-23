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
        self.wh = 6, 6
        self.rgb = 110, 156, 66
        self.hud = False

def _init_objects_ram(hud=False):
    """
    (Re)Initialize the objects
    """
    
    return [Frog()]