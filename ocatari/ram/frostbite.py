from .game_objects import GameObject
import sys 

MAX_NB_OBJECTS = {"Player": 1, "Enemy": 1}
MAX_NB_OBJECTS_HUD = {}# 'Score': 1}

class Player(GameObject):
    def __init__(self):
        super().__init__()
        self._xy = 0, 0
        self.wh = (8, 17)
        self.rgb = 198,108,58
        self.hud = False


class GreenFish(GameObject):
    def __init__(self):
        super().__init__()
        self.rgb = 111,210,111
        self.wh = (8, 6)
        self.hud = False
        self._xy = 0, 0

class FrostBite(GameObject):
    def __init__(self):
        super().__init__()
        self.rgb = 84,38,210
        self.hud = False
        self.wh = (8, 17)
        self._xy = 0, 0


class WhitePlate(GameObject):
    def __init__(self):
        super().__init__()
        self.rgb = 214,214,214
        self.hud = False
        self.wh = (24, 7)
        self._xy = 0, 0

class BluePlate(GameObject):
    def __init__(self):
        super().__init__()
        self.rgb = 84,138,210
        self.hud = False
        self.wh = (24, 7)
        self._xy = 0, 0

class Bird(GameObject):
    def __init__(self):
        super().__init__()
        self.rgb = 132,144,252
        self.hud = False
        self.wh = (8, 7)
        self._xy = 0, 0

class Bear(GameObject):
    def __init__(self):
        super().__init__()
        self.rgb = 0,0,0
        self.hud = False
        self.wh = (14, 15)
        self._xy = 0, 0

class Crab(GameObject):
    def __init__(self):
        super().__init__()
        self.rgb = 23,130,74
        self.hud = False
        self.wh = (8, 18)
        self._xy = 0, 0

class Clam(GameObject):
    def __init__(self):
        super().__init__()
        self.rgb = 210,210,64
        self.hud = False
        self._xy = 0, 0
        self.wh=(2,3)

class House(GameObject):
    def __init__(self):
        super().__init__()
        self.rgb = 142,142,142
        self.hud = False
        self.wh = (8, 18)
        self._xy = 0, 0

class CompletedHouse(GameObject):
    def __init__(self):
        super().__init__()
        self.rgb = 0,0,0
        self.hud = False
        self.wh = (34,20)
        self._xy = 0, 0

class Logo(GameObject):
    def __init__(self):
        super().__init__()
        self.rgb = 214,214,214
        self.hud = True
        self.wh = (50,8)
        self._xy = 20,191


class LifeCount(GameObject):
    def __init__(self):
        super().__init__()
        self.rgb =132,144,252
        self.hud = True
        self.wh = (8, 18)
        self._xy = 0, 0


class Score(GameObject):
    def __init__(self):
        super().__init__()
        self.rgb =132,144,252
        self.hud = True
        self.wh = (8, 18)
        self._xy = 0, 0

class Degree(GameObject):
    def __init__(self):
        super().__init__()
        self.rgb =132,144,252
        self.hud = True
        self.wh = (8, 18)
        self._xy = 0, 0


class PlayerScore(GameObject):
    def __init__(self):
        super().__init__()
        self.rgb = 0,0,0
        self.hud = True
        self.wh = (8, 18)
        self._xy = 0, 0


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


def _init_objects_frostbite_ram(hud=False):
    """
    (Re)Initialize the objects
    """
    objects = [Player()]
    if hud:
        objects.append(Logo())
    # if hud:
    #     global plscore
    #     plscore = PlayerScore()
    #     global enscore
    #     enscore = EnemyScore()
    #     objects.extend([plscore, enscore, Logo(),
    #                     Clock(63, 17, 6, 7), Clock(73, 18, 2, 5),
    #                     Clock(79, 17, 6, 7), Clock(87, 17, 6, 7)])
    return objects


def _detect_objects_frostbite_revised(objects, ram_state, hud=False):
    """
    For all 3 objects:
    (x, y, w, h, r, g, b)
    """
    player,= objects[:1]
    player.xy =  ram_state[102] -1,ram_state[100]+30
    if hud:
        pass


def _detect_objects_frostbite_raw(info, ram_state):
    """
    returns unprocessed list with
    ball_x, ball_y, enemy_y, player_y
    """
    info["objects_list"] = ram_state[32:36]


# def _detect_objects_frostbite_revised_old(info, ram_state, hud=False):
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
