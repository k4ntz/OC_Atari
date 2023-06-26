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
    objects = [Player(),Enemy(),Swirl(),Enemy_Missile(),Barrier(),Player_Bullet()]
    return objects


def _detect_objects_yarsrevenge_revised(objects, ram_state, hud=False):
    """
    For all 3 objects:
    (x, y, w, h, r, g, b)
    """
    objects[3:]=[None]*3
    player,= objects[:1]
    player.xy=ram_state[32],ram_state[31]+2
    if ram_state[43]>=145:
        enemy=Enemy()
        enemy.xy=ram_state[43],ram_state[42]+3
        objects[2]=None
        objects[1]=enemy
    else:
        swirl=Swirl()
        swirl.xy=ram_state[43]+4,ram_state[42]+3
        objects[2]=swirl
        objects[1]=None
    # Enemy Missile 
    e_m=Enemy_Missile()
    e_m.xy=ram_state[47],ram_state[46]+2
    objects[3]=e_m
    # Player Missile
    if abs(ram_state[38]-3-ram_state[32])>5 and abs(ram_state[37]-ram_state[31])>5:
        p_m=Player_Bullet()
        p_m.xy=ram_state[38]-1,ram_state[37]+3
        objects[5]=p_m
    else:
        objects[5]=None
    
    # Adding Barrier
    if ram_state[53]==164:
        b=Barrier()
        b.xy=52,4
        objects[4]=b
    else:
        objects[4]=None
    if hud:
        # scores
        pass
    # import ipdb; ipdb.set_trace()

