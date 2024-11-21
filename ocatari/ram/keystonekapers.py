from .game_objects import GameObject, NoObject

"""
RAM extraction for the game Keystone Kapers.

"""

MAX_NB_OBJECTS = {'Kop': 1, 'Krook': 1, 'Ball': 2}
MAX_NB_OBJECTS_HUD = {'Kop': 1, 'Krook': 1, 'Ball':2}

class Kop(GameObject):
    """
    The player figure i.e., the Kop. 
    """
    
    def __init__(self):
        super().__init__()
        self._xy = 0, 0
        self.wh = 6,20
        self.rgb = 220,175,111
        self.hud = False

class Krook(GameObject):
    """
    A thief.
    """
    def __init__(self):
        super().__init__()
        self._xy = 0, 0
        self.wh = 7,20
        self.rgb = 220,175,11
        self.hud = False


class Ball(GameObject):
    def __init__(self):
        super().__init__()
        self._xy = 0, 0
        self.wh = 6,6
        self.rgb = 137,26,53       


def _init_objects_ram(hud=False):
    """
    (Re)Initialize the objects
    """
    balls = [NoObject()] * 2
    return [Kop(), Krook(), balls]

def _detect_objects_ram(objects, ram_state, hud=False):
    pass