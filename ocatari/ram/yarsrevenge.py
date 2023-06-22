from .game_objects import GameObject
import sys 

MAX_NB_OBJECTS = {"Player": 1}
MAX_NB_OBJECTS_HUD = {}# 'Score': 1}

class Player(GameObject):
    def __init__(self):
        super().__init__()
        self._xy = 0, 0
        self.wh = (8, 16)
        self.rgb = 169,128,240
        self.hud = False

class Enemy(GameObject):
    def __init__(self):
        super().__init__()
        self._xy = 0, 0
        self.wh = (8, 18)
        self.rgb = 240,240,240 
        self.hud = False

class Swirl(GameObject):
    def __init__(self):
        super().__init__()
        self._xy = 0, 0
        self.wh = (8, 18)
        self.rgb = 169,128,240 
        self.hud = False

class Enemy_Missile(GameObject):
    def __init__(self):
        super().__init__()
        self._xy = 0, 0
        self.wh = (4,2)
        self.rgb = 169,128,240 
        self.hud = False

class Barrier(GameObject):
    def __init__(self):
        super().__init__()
        self._xy = 0, 0
        self.wh = (28,190)
        self.rgb = 250,250,250
        self.hud = False

class Player_Bullet(GameObject):
    def __init__(self):
        super().__init__()
        self._xy = 0, 0
        self.wh = (1,2)
        self.rgb = 169,128,240
        self.hud = False

class Shield_Block(GameObject):
    def __init__(self):
        super().__init__()
        self._xy = 0, 0
        self.wh = (2,4)
        self.rgb = 163,57,21
        self.hud = False

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


def _init_objects_yarsrevenge_ram(hud=False):
    """
    (Re)Initialize the objects
    """
    objects = [Player(),Enemy_Missile()]
    return objects


def _detect_objects_yarsrevenge_revised(objects, ram_state, hud=False):
    """
    For all 3 objects:
    (x, y, w, h, r, g, b)
    """
    player,= objects[:1]
    player.xy=ram_state[32],ram_state[31]+2
    
    if hud:
        # scores
        pass
    # import ipdb; ipdb.set_trace()

