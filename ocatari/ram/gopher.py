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
        self.wh = (8,27)
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
    # Detecting player
    player = objects[0]
    player.xy = ram_state[31]-10, 96
    # Detecting gopher
    gopher=objects[1]
    if ram_state[85]<=5:
        gopher.xy=ram_state[41]-2,184
        gopher.wh=(14,10)
    elif ram_state[85]==35:
        gopher.xy=ram_state[41]-2,149
        gopher.wh=(14,10)
    else:
        gopher.xy=ram_state[41]-3,184-(ram_state[85])
        gopher.wh=(7,23)
    
    # Detecting carrots
    # Carrot at (92, 151), (8, 27), Carrot at (76, 151), (8, 27), Carrot at (60, 151), (8, 27)
    carrot1,carrot2,carrot3=Carrot(),Carrot(),Carrot()
    carrot1.xy=92,151; carrot2.xy=76,151; carrot3.xy=60,151
    if ram_state[36]==0 and ram_state[37]==0 and ram_state[38]==3:
        objects[2:5]=carrot1,carrot2,carrot3
    elif ram_state[36]==0 and ram_state[37]==0 and ram_state[38]==1:
        objects[2]=carrot2; objects[3]=carrot3; objects[4]=None
    elif ram_state[36]==0 and ram_state[37]==0 and ram_state[38]==0:
        objects[2]=carrot3; objects[3]=None; objects[4]=None
    elif ram_state[36]==128 and ram_state[37]==32 and ram_state[38]==1:
        objects[2]=carrot2; objects[3]=carrot1; objects[4]=None
    elif ram_state[36]==127 and ram_state[37]==16 and ram_state[38]==0:
        objects[2]=carrot1; objects[3]=None; objects[4]=None
    elif ram_state[36]==128 and ram_state[37]==32 and ram_state[38]==0:
        objects[2]=carrot2; objects[3]=None; objects[4]=None

    if hud:
        # Score hundreds and thousands depend on ram_state[49] and score ones and tens depend on ram_state[50]
        bound1,bound2,bound3,bound4=Score(),Score(),Score(),Score()
        # Score at (98, 10), (5, 9), Score at (90, 10), (5, 9), Score at (82, 10), (5, 9), Score at (75, 10), (3, 9)]
        bound1.xy=75,10
        bound2.xy=82,10
        bound3.xy=90,10
        bound4.xy=98,10
        if ram_state[49]==0 and ram_state[50]<=9:
            # Right most bounding box only
            objects[-1]=bound4
            objects[-2]=None; objects[-3]=None; objects[-4]=None
        elif ram_state[49]==0 and ram_state[50]>9:
            # two bounding boxes
            objects[-1]=bound4
            objects[-2]=bound3
            objects[-3]=None; objects[-4]=None
        elif ram_state[49]<=9:
            # 3 bounding boxes
            objects[-1:-4]=bound4,bound3,bound2
            objects[-4]=None
        elif ram_state[49]>9:
            # 4 bounding boxes
            objects[-1:-5]=bound4,bound3,bound2,bound1






