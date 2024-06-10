from .game_objects import GameObject
import sys 

"""
RAM extraction for the game Enduro.
"""

MAX_NB_OBJECTS = {"Player": 1, "Car": 24}
MAX_NB_OBJECTS_HUD = {"NumberOfCars":4, "PlayerScore":6, "Level":1}# 'Score': 1}

class Player(GameObject):
    
    def __init__(self):
        super().__init__()
        self._xy = 0, 0
        self.wh = (16,10)
        self.rgb = 192,192,192
        self.hud = False

class Car(GameObject):
    def __init__(self):
        super().__init__()
        self._xy = 0, 0
        self.wh = (16,10)
        self.rgb = 192,192,192
        self.hud = False

class PlayerScore(GameObject):
    def __init__(self):
        super().__init__()
        self._xy = 0, 0
        self.wh = (16,10)
        self.rgb =132,144,252
        self.hud = True

class NumberOfCars(GameObject):
    def __init__(self):
        super().__init__()
        self._xy = 0, 0
        self.wh = (16,10)
        self.rgb =0,0,0
        self.hud = True 

class Level(GameObject):
    def __init__(self):
        super().__init__()
        self._xy = 0, 0
        self.wh = (16,10)
        self.rgb =0,0,0
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


def _init_objects_ram(hud=False):
    """
    (Re)Initialize the objects
    """
    objects = [Player()]
    if hud:
        objects.extend([])
    return objects

def _detect_objects_ram(objects, ram_state, hud=False):
    """
    For all 3 objects:
    (x, y, w, h, r, g, b)
    """
    # 106 ram_state is somewhat controlling the y of the player when it's dying by sinking
    player,= objects[:1]
    player.xy=int(-0.566*ram_state[54]+146),144

    if hud:
        # ram_state[45] indicates the level 
        pass
