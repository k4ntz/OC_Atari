from .game_objects import GameObject
import sys 

MAX_NB_OBJECTS = {"Player": 2, "Enemy":2, "Ball":1}
MAX_NB_OBJECTS_HUD = {'PlayerScore':2, 'EnemyScore':2, 'Timer':3}# 'Score': 1}

class Player(GameObject):
    def __init__(self):
        super().__init__()
        self._xy = 0, 0
        self.wh = (16,20)
        self.rgb = 101, 111, 228
        self.hud = False

class Enemy(GameObject):
    def __init__(self):
        super().__init__()
        self.rgb = 82,126,45
        self._xy = 0, 0
        self.wh = (16,20)
        self.hud = False

class Ball(GameObject):
    def __init__(self):
        super().__init__()
        self.rgb = 0,0,0
        self._xy = 0, 0
        self.wh = (2,2)
        self.hud = False

class PlayerScore(GameObject):
    def __init__(self):
        super().__init__()
        self.rgb = 84,92,214
        self._xy = 0, 0
        self.wh = (8, 7)
        self.hud = True

class EnemyScore(GameObject):
    def __init__(self):
        super().__init__()
        self.rgb = 236,200,96
        self._xy = 0, 0
        self.wh = (8, 7)
        self.hud = True

class Timer(GameObject):
    def __init__(self):
        super().__init__()
        self.rgb = 84,92,214
        self._xy = 0, 0
        self.wh = (8, 7)
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


def _init_objects_icehockey_ram(hud=False):
    """
    (Re)Initialize the objects
    """
    objects = [Player(),Player(),Enemy(),Enemy(),Ball()]
    if hud:
        objects.extend([PlayerScore(),PlayerScore(),EnemyScore(),EnemyScore(),Timer(),Timer(),Timer()])
    return objects


def _detect_objects_icehockey_revised(objects, ram_state, hud=False):
    """
    For all 3 objects:
    (x, y, w, h, r, g, b)
    """
    # Player at downside
    player = objects[0]
    player.xy = ram_state[59]-13, 168-ram_state[55]
    # Player at upside
    player2=objects[1]
    player2.xy=ram_state[57]-13,168-ram_state[53]
    # Enemy at downside 
    enemy_1=objects[2]
    enemy_1.xy=ram_state[60]-13,168-ram_state[56]
    # Enenmy at upper side
    enemy_2=objects[3]
    enemy_2.xy=ram_state[58]-13,168-ram_state[54]

    # Ball

    ball=objects[4]
    ball.xy=ram_state[52]-10,188-ram_state[91]
    
    if hud:
        # scores
        pass


