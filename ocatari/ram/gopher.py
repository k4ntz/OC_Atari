from .game_objects import GameObject
import sys 

MAX_NB_OBJECTS = {"Player": 2}
MAX_NB_OBJECTS_HUD = {}

class Player(GameObject):
    def __init__(self):
        super().__init__()
        self._xy = 0, 0
        self.wh = (11,50)
        self.rgb = 101, 111, 228
        self.hud = False

class Gopher(GameObject):
    def __init__(self):
        super().__init__()
        self._xy = 0, 0
        self.wh = (14,10)
        self.rgb = 72,44,0
        self.hud = False

class Carrot(GameObject):
    def __init__(self):
        super().__init__()
        self._xy = 0, 0
        self.wh = (12,27)
        self.rgb = 162,98,33
        self.hud = False

class Bird(GameObject):
    def __init__(self):
        super().__init__()
        self._xy = 0, 0
        self.wh = (15,18)
        self.rgb = 45,50,184 
        self.hud = False

class Empty_block(GameObject):
    def __init__(self):
        super().__init__()
        self._xy = 0, 0
        self.wh = (8,12)
        self.rgb = 223,183,85 
        self.hud = False

class Score(GameObject):
    def __init__(self):
        super().__init__()
        self._xy = 0, 0
        self.wh = (5,9)
        self.rgb = 195,144,65 
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


def _init_objects_gopher_ram(hud=False):
    """
    (Re)Initialize the objects
    """
    objects = [Player(),Gopher(),Carrot(),Carrot(),Carrot()]
    if hud:
        objects.extend([Bird(),Score(),Score(),Score(),Score()])
    return objects


def _detect_objects_gopher_revised(objects, ram_state, hud=False):
    """
    For all 3 objects:
    (x, y, w, h, r, g, b)
    """
    player = objects[0]
    player.xy = ram_state[59]-13, 168-ram_state[55]
    
    if hud:
        pass






