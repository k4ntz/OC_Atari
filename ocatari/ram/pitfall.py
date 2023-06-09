from .game_objects import GameObject
import sys 

MAX_NB_OBJECTS = {"Player": 1,"Wall":1,"Logs":5,"StairPit":4,"Pit":3,"Scorpion":1,"Rope":1,"Snake":1,"Tarpit":1,"Waterhole":1,"Crocodile":1,"GoldenBar":1,"Fire":1}
MAX_NB_OBJECTS_HUD = {"LifeCount":3,"PlayerScore":6,"Timer":5}

class Player(GameObject):
    def __init__(self):
        super().__init__()
        self._xy = 0, 0
        self.wh = (7, 20)
        self.rgb = 53,95,24
        self.hud = False

class Wall(GameObject):
    def __init__(self):
        super().__init__()
        self.xy=0,0
        self.wh=(7,35)
        self.rgb = 167,26,26
        self.hud = False

class Logs(GameObject):
    def __init__(self):
        super().__init__()
        self.xy=0,0
        self.wh=(6,14)
        self.rgb = 105,105,15
        self.hud = False

class StairPit(GameObject):
    def __init__(self):
        super().__init__()
        self.xy=0,0
        self.wh=(8,6)
        self.rgb = 0,0,0
        self.hud = False

class Pit(GameObject):
    def __init__(self):
        super().__init__()
        self.xy=0,0
        self.wh=(12,6)
        self.rgb = 252,188,116
        self.hud = False

class Scorpion(GameObject):
    def __init__(self):
        super().__init__()
        self.xy=0,0
        self.wh=(7,10)
        self.rgb = 236,236,236
        self.hud = False

class Rope(GameObject):
    def __init__(self):
        super().__init__()
        self.xy=0,0
        self.wh=(15,15)
        self.rgb = 72,72,0
        self.hud = False

class Snake(GameObject):
    def __init__(self):
        super().__init__()
        self.xy=0,0
        self.wh=(8,14)
        self.rgb = 167,26,26
        self.hud = False

class Tarpit(GameObject):
    def __init__(self):
        super().__init__()
        self.xy=0,0
        self.wh=(64,10)
        self.rgb = 0,0,0
        self.hud = False

class Waterhole(GameObject):
    def __init__(self):
        super().__init__()
        self.xy=0,0
        self.wh=(64,10)
        self.rgb = 45,109,152
        self.hud = False

class Crocodile(GameObject):
    def __init__(self):
        super().__init__()
        self.xy=0,0
        self.wh=(8,8)
        self.rgb = 20,60,0
        self.hud = False

class GoldenBar(GameObject):
    def __init__(self):
        super().__init__()
        self.xy=0,0
        self.wh=(7,13)
        self.rgb = 252,252,84
        self.hud = False

class Fire(GameObject):
    def __init__(self):
        super().__init__()
        self.xy=0,0
        self.wh=(8,14)
        self.rgb = 236,200,96
        self.hud = False

class LifeCount(GameObject):
    def __init__(self):
        super().__init__()
        self.xy=0,0
        self.wh=(1,8)
        self.rgb =214,214,214
        self.hud = True

class PlayerScore(GameObject):
    def __init__(self):
        super().__init__()
        self.xy=0,0
        self.wh=(6,8)
        self.rgb =214,214,214
        self.hud = True

class Timer(GameObject):
    def __init__(self):
        super().__init__()
        self.xy=0,0
        self.wh=(6,8)
        self.rgb =214,214,214
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


def _init_objects_pitfall_ram(hud=False):
    """
    (Re)Initialize the objects
    """
    objects = [Player(),Wall(),Logs(),Logs(),Logs(),StairPit(),StairPit(),Pit(),Pit(),Scorpion()]
    objects.extend([Rope(),Snake(),Tarpit(),Waterhole(),Crocodile(),Crocodile(),Crocodile()])
    objects.extend([GoldenBar(),Fire()])
    if hud:
        objects.extend([LifeCount(),LifeCount(),LifeCount()])
        objects.extend([PlayerScore()]*5)
        objects.extend([Timer()]*4)
    return objects

def _detect_objects_pitfall_revised(objects, ram_state, hud=False):
    """
    For all 3 objects:
    (x, y, w, h, r, g, b)
    """
    # 106 ram_state is somewhat controlling the y of the player when it's dying by sinking
    player,= objects[:1]
    # 0.99 x ram[97] + 0.92 x is
    # Player_y = 1.00 x ram[105] + 72.00
    player.xy =  ram_state[97]+1,ram_state[105]+72
    objects[0]=player
    if ram_state[19]==0:
        l1=Logs()
        l1.xy=(ram_state[98]+2)%160,119
        objects[2]=l1; objects[3]=None; objects[4]=None
    elif ram_state[19]==1:
        l1=Logs()
        l2=Logs()
        l1.xy=(ram_state[98]+2)%160,119
        l2.xy=(ram_state[98]+16+2)%160,119
        objects[2]=l1; objects[3]=l2; objects[4]=None
    elif ram_state[19]==2:
        l1=Logs()
        l2=Logs()
        l1.xy=(ram_state[98]+2)%160,119
        l2.xy=(ram_state[98]+32+2)%160,119
        objects[2]=l1; objects[3]=l2; objects[4]=None
    elif ram_state[19]==3:
        l1=Logs()
        l2=Logs()
        l3=Logs()
        l1.xy=ram_state[98]+2,119
        l2.xy=(ram_state[98]+32+2)%160,119
        l3.xy=(ram_state[98]+64+2)%160,119
        objects[2]=l1; objects[3]=l2; objects[4]=l3
    else:
        objects[2]=None; objects[3]=None; objects[4]=None
    
    # Handling the pits etc
    if ram_state[20]==0:
        # Single stairpit
        objects[5:9]=[None]*4
        objects[10]=None
        objects[12:19]=[None]*7
    elif ram_state[20]==1:
        p1=Pit();p2=Pit()
        p1.xy=48,122
        p2.xy=100,122
        objects[7]=p1; objects[8]=p2
        objects[10]=None
        objects[12:19]=[None]*7
        objects[5:7]=[None]*2
    elif ram_state[20]==2:
        p=Tarpit()
        p.xy=48,120
        objects[12]=p
        objects[7:9]=[None]*2
        objects[10]=None
        objects[13:19]=[None]*6
        objects[5:7]=[None]*2
    elif ram_state[20]==3:
        w=Waterhole()
        w.xy=50,119
        objects[13]=w
        objects[12]=None
        objects[7:9]=[None]*2
        objects[10]=None
        objects[14:19]=[None]*5
        objects[5:7]=[None]*2
    elif ram_state[20]==4:
        w=Waterhole()
        w.xy=50,119
        objects[13]=w
        objects[12]=None
        objects[7:9]=[None]*2
        objects[10]=None
        objects[14]=None
        objects[5:7]=[None]*2
        c1=Crocodile(); c1.xy=60,122
        objects[15]=c1
        c2=Crocodile(); c2.xy=76,122
        objects[16]=c2
        c3=Crocodile(); c3.xy=92,122
        objects[17]=c3
    else:
        pass
    
    # Implementing Scorpion
    # Remove scorpion when there is no pit
    if ram_state[29]==0:
        s=Scorpion()
        s.xy=ram_state[99],170
        objects[9]=s
        objects[1]=None
    elif ram_state[29]==1:
        w=Wall()
        w.xy=ram_state[99],170
        objects[1]=w
        objects[9]=None
    else:
        objects[1]=None; objects[9]=None





    if hud:
        pass


def _detect_objects_pitfall_raw(info, ram_state):
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
