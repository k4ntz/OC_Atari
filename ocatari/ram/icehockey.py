from .game_objects import GameObject, NoObject, Orientation, OrientedObject
import sys
from math import dist

"""
RAM extraction for the game Ice Hockey.
"""

MAX_NB_OBJECTS = {"Player": 2, "Enemy": 2, "Ball": 1}
MAX_NB_OBJECTS_HUD = {"Player": 2, "Enemy": 2, "Ball": 1,
                      'PlayerScore': 1, 'EnemyScore': 1, 'Timer': 1}  # 'Score': 1}


class Player(OrientedObject):
    """
    The player figure i.e., the current hockey player (goalie or forward).
    """

    def __init__(self):
        super().__init__()
        self._xy = 0, 0
        self.wh = 10, 20
        self.rgb = 101, 111, 228
        self.stick = False
        self.hud = False
        self.orientation = Orientation.E


class Enemy(OrientedObject):
    """
    The enemy player(s).
    """

    def __init__(self):
        super().__init__()
        self.rgb = 82, 126, 45
        self._xy = 0, 0
        self.wh = 10, 20
        self.hud = False
        self.orientation = Orientation.E


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
    player1 = objects[0]
    if ram_state[84] == 255:
        player1.wh = (16,20)
        player1.xy = ram_state[59]-9, 169-ram_state[55]
    elif ram_state[84] == 31:
        player1.wh = (15,20)
        player1.xy = ram_state[59]-16, 169-ram_state[55]
    else:
        player1.wh = (10, 20)
        player1.xy = ram_state[59]-10, 168-ram_state[55]
    player1.orientation = Orientation.W if ram_state[63] else Orientation.E
        
    # Player at upside #82
    player2 = objects[1] 
    if ram_state[82] == 255:
        player2.wh = (16,20)
        player2.xy = ram_state[57]-9, 169-ram_state[53]
    elif ram_state[82] == 31:
        player2.wh = (15,20)
        player2.xy = ram_state[57]-16, 169-ram_state[53]
    else:
        player2.wh = (10, 20)
        player2.xy = ram_state[57]-10, 168-ram_state[53]
    player2.orientation = Orientation.W if ram_state[61] else Orientation.E
         
    # Enemy at downside
    enemy1 = objects[2]
    if ram_state[85] == 255:
        enemy1.wh = (16,21)
        enemy1.xy = ram_state[60]-9, 168-ram_state[56]
    elif ram_state[85] == 31:
        enemy1.wh = (15,21)
        enemy1.xy = ram_state[60]-16, 168-ram_state[56]
    else:
        enemy1.wh = (10, 20)
        enemy1.xy = ram_state[60]-10, 168-ram_state[56]
    enemy1.orientation = Orientation.W if ram_state[64] else Orientation.E
    
    # Enenmy at upper side
    enemy2 = objects[3]
    if ram_state[83] == 255:
        enemy2.wh = (16,21)
        enemy2.xy = ram_state[58]-9, 168-ram_state[54]
    elif ram_state[83] == 31:
        enemy2.wh = (15,21)
        enemy2.xy = ram_state[58]-16, 168-ram_state[54]
    else:
        enemy2.wh = (10, 20)
        enemy2.xy = ram_state[58]-10, 168-ram_state[54]
    enemy2.orientation = Orientation.W if ram_state[62] else Orientation.E

    # Ball
    ball = objects[4]
    ball.xy = ram_state[52]-10, 188-ram_state[91]
        

    if hud:
        # scores
        # ram_state[11] for enemy score
        es = EnemyScore()
        es.xy = 110, 14
        es.wh = 6, 7
        objects[5]=es
        if ram_state[11] < 10:
            if ram_state[11]==1:
                es.x = 111
                es.w = 4
        elif ram_state[11]<26:
            es.x = 102
            es.w = 14
            if ram_state[11]==17:
                es.w = 13
        else:
            es.x = 101
            es.w = 16
            if ram_state[10]% 16 == 1:
                es.w = 14
            
            
        # ram_state[10] for player score
        ps = PlayerScore()
        ps.xy = 46, 14
        ps.wh = 6, 7
        objects[6] = ps
        if ram_state[10] < 10:
            if ram_state[10]==1:
                ps.x = 47
                ps.w = 4
        elif ram_state[10]<32:
            ps.x = 38
            ps.w = 14
            if ram_state[10]==17:
                ps.w = 13
        else:
            ps.x = 37
            ps.w = 16
            if ram_state[10]% 16 == 1:
                ps.w = 14
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
        
