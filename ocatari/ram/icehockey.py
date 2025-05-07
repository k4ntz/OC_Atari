from .game_objects import GameObject, NoObject
import sys

"""
RAM extraction for the game Ice Hockey.
"""

MAX_NB_OBJECTS = {"Player": 2, "Enemy": 2, "Ball": 1}
MAX_NB_OBJECTS_HUD = {"Player": 2, "Enemy": 2, "Ball": 1,
                      'PlayerScore': 1, 'EnemyScore': 1, 'Timer': 1}  # 'Score': 1}


class Player(GameObject):
    """
    The player figure i.e., the current hockey player (goalie or forward).
    """

    def __init__(self):
        super().__init__()
        self._xy = 0, 0
        self.wh = 16, 20
        self.rgb = 101, 111, 228
        self.hud = False


class Enemy(GameObject):
    """
    The enemy player(s).
    """

    def __init__(self):
        super().__init__()
        self.rgb = 82, 126, 45
        self._xy = 0, 0
        self.wh = 16, 20
        self.hud = False


class Ball(GameObject):
    """
    The puck.
    """

    def __init__(self):
        super().__init__()
        self.rgb = 0, 0, 0
        self._xy = 0, 0
        self.wh = 2, 2
        self.hud = False


class PlayerScore(GameObject):
    """
    The player's score display (HUD).
    """

    def __init__(self):
        super().__init__()
        self.rgb = 84, 92, 214
        self._xy = 46, 14
        self.wh = 8, 7
        self.hud = True


class EnemyScore(GameObject):
    """
    The enemy's score display (HUD).
    """

    def __init__(self):
        super().__init__()
        self.rgb = 236, 200, 96
        self._xy = 110, 14
        self.wh = 6, 7
        self.hud = True


class Timer(GameObject):
    """
    The game-clock (HUD).
    """

    def __init__(self):
        super().__init__()
        self.rgb = 84, 92, 214
        self._xy = 65, 5
        self.wh = 30, 7 
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
    objects = [Player()]+[Player()] + [Enemy()]+[Enemy()] + [Ball()]
    if hud:
        objects.extend([NoObject()]*3)
    return objects


def _detect_objects_ram(objects, ram_state, hud=False):
    """
    For all 3 objects:
    (x, y, w, h, r, g, b)
    """
    # Player at downside
    player = objects[0]
    player.xy = ram_state[59]-13, 168-ram_state[55]
    # Player at upside
    player2 = objects[1]
    player2.xy = ram_state[57]-13, 168-ram_state[53]
    # Enemy at downside
    enemy_1 = objects[2]
    enemy_1.xy = ram_state[60]-13, 168-ram_state[56]
    # Enenmy at upper side
    enemy_2 = objects[3]
    enemy_2.xy = ram_state[58]-13, 168-ram_state[54]
    # Ball
    ball = objects[4]
    ball.xy = ram_state[52]-10, 188-ram_state[91]

    if hud:
        # scores
        # ram_state[11] for enemy score
        es = EnemyScore()
        es.xy = 110, 14
        es.wh = 6, 7
        if ram_state[11] < 10:
            if ram_state[11]==1:
                es.x = 111
                es.w = 4
        elif ram_state[11]<32:
            es.x = 102
            es.w = 14
            if ram_state[11]==17:
                es.w = 13
        # elif ram_state[11]<30:
        objects[6]=es
            
                
            
        # else:
            
        # # ram_state[10] for player score
        # if ram_state[10] <= 9:
        #     es1 = PlayerScore()
        #     es1.xy = 46, 14
        #     objects[5] = es1
        #     objects[6] = NoObject()
        # else:
        #     es1 = PlayerScore()
        #     es2 = PlayerScore()
        #     es1.xy = 46, 14
        #     es2.xy = 38, 14
        #     objects[5] = es1
        #     objects[6] = es2
        # Timer
        t = Timer()
        t.xy = 65, 5
        t.wh = 30, 7
        objects[7]=t
        # ram_state[6] responsible for seconds place
        # ram_state[7] responsible for minutes's place
        # t1 = objects[9]
        # t2 = objects[10]
        # t3 = objects[11]
        # t1.xy = 89, 5
        # t2.xy = 81, 5
        # t3.xy = 65, 5  # Minute place
        
