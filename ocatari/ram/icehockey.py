from .game_objects import GameObject
import sys 

MAX_NB_OBJECTS = {"Player": 1}
MAX_NB_OBJECTS_HUD = {'Cactus': 6, 'ThisWaySign': 1}# 'Score': 1}

class Player(GameObject):
    def __init__(self):
        super().__init__()
        self._xy = 0, 0
        self.wh = (8, 32)
        self.rgb = 101, 111, 228
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


def _init_objects_icehockey_ram(hud=False):
    """
    (Re)Initialize the objects
    """
    objects = [Player()]
    return objects


def _detect_objects_icehockey_revised(objects, ram_state, hud=False):
    """
    For all 3 objects:
    (x, y, w, h, r, g, b)
    """
    player = objects[0]
    player.xy = ram_state[80], ram_state[3] + 95
    
    if hud:
        # scores
        pass
    # import ipdb; ipdb.set_trace()


def _detect_objects_icehockey_raw(info, ram_state):
    """
    returns unprocessed list with
    ball_x, ball_y, enemy_y, player_y
    """
    info["objects_list"] = ram_state[32:36]


