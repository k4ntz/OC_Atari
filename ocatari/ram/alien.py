from .game_objects import GameObject
import sys 

MAX_NB_OBJECTS = {"Player": 1, "Enemy": 1, "Birdseeds": 1, "Truck": 6}
MAX_NB_OBJECTS_HUD = {'Cactus': 6, 'ThisWaySign': 1}# 'Score': 1}

class Player(GameObject):
    def __init__(self):
        super().__init__()
        self._xy = 0, 0
        self.wh = (8, 32)
        self.rgb = 101, 111, 228
        self.hud = False


class Enemy(GameObject):
    def __init__(self):
        super().__init__()
        self._xy = 0, 0
        self.wh = (7, 29)
        self.rgb = 198, 108, 58
        self.hud = False


class Birdseeds(GameObject):
    def __init__(self):
        super().__init__()
        self._xy = 0, 0
        self.wh = (5, 3)
        self.rgb = 84, 92, 214
        self.hud = False


class Truck(GameObject):
    def __init__(self):
        super().__init__()
        self._xy = 0, 0
        self.wh = (16, 18)
        self.rgb = 198, 108, 58
        self.hud = False


class Cactus(GameObject):
    def __init__(self):
        super().__init__()
        self._xy = 0, 0
        self.wh = (8, 8)
        self.rgb = 187, 187, 53
        self.hud = False

class ThisWaySign(GameObject):
    def __init__(self):
        super().__init__()
        self._xy = 0, 0
        self.wh = (16, 15)
        self.rgb = 0, 0, 0
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


def _init_objects_alien_ram(hud=False):
    """
    (Re)Initialize the objects
    """
    objects = [Player(), Enemy(), Truck()]
    return objects


def _detect_objects_alien_revised(objects, ram_state, hud=False):
    """
    For all 3 objects:
    (x, y, w, h, r, g, b)
    """
    player, enemy, truck = objects[:4]
    player.xy = ram_state[80], ram_state[3] + 95
    if ram_state[81] > 145: # Removing the enemy
        objects[1] = None
    elif enemy is None:
        enemy = Enemy()
        objects[1] = enemy
    if enemy is not None:
        enemy.xy = ram_state[81], ram_state[5] + 98
    if truck is not None:
        truck.xy=ram_state[42]-2, ram_state[46]-15
    
    if hud:
        # scores
        global plscore
        if ram_state[18] > 10:  # player score
            plscore.tenify()
        else:
            plscore.detenify()
    # import ipdb; ipdb.set_trace()


def _detect_objects_alien_raw(info, ram_state):
    """
    returns unprocessed list with
    ball_x, ball_y, enemy_y, player_y
    """
    info["objects_list"] = ram_state[32:36]


# def _detect_objects_alien_revised_old(info, ram_state, hud=False):
#     """
#     For all 3 objects:
#     (x, y, w, h, r, g, b)
#     """
#     objects = {}
#     objects["player"] = ram_state[32]+5, ram_state[34]+38, 14, 46, 214, 214, 214
#     objects["enemy"] = ram_state[33]+4, ram_state[35]+38, 14, 46, 0, 0, 0
#     if hud:
#         objects["enemy_score"] = 111, 5, 6, 7, 0, 0, 0
#         if ram_state[19] < 10:
#             objects["enemy_score2"] = 0, 0, 0, 0, 0, 0, 0
#         else:
#             objects["enemy_score2"] = 103, 5, 6, 7, 0, 0, 0
#         objects["player_score"] = 47, 5, 6, 7, 214, 214, 214
#         if ram_state[18] < 10:
#             objects["player_score2"] = 0, 0, 0, 0, 0, 0, 0
#         else:
#             objects["player_score2"] = 39, 5, 6, 7, 214, 214, 214
#         objects["logo"] = 62, 189, 32, 7, 20, 60, 0
#         objects["time1"] = 63, 17, 6, 7, 20, 60, 0
#         objects["time2"] = 73, 18, 2, 5, 20, 60, 0
#         objects["time3"] = 79, 17, 6, 7, 20, 60, 0
#         objects["time4"] = 87, 17, 6, 7, 20, 60, 0
#     info["objects"] = objects
