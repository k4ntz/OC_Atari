from .game_objects import GameObject
import sys 

MAX_NB_OBJECTS = {"Player": 1, "Enemy": 1, "BirdSeeds": 1, "Truck": 6}
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


class BirdSeeds(GameObject):
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
        self.hud = True


class ThisWaySign(GameObject):
    def __init__(self):
        super().__init__()
        self._xy = 0, 0
        self.wh = (16, 15)
        self.rgb = 0, 0, 0
        self.hud = True


class BirdSeedSign(GameObject):
    def __init__(self):
        super().__init__()
        self._xy = 0, 0
        self.wh = (16, 15)
        self.rgb = 0, 0, 0
        self.hud = True


class CarsAheadSign(GameObject):
    def __init__(self):
        super().__init__()
        self._xy = 0, 0
        self.wh = (16, 15)
        self.rgb = 0, 0, 0
        self.hud = True


class ExitSign(GameObject):
    def __init__(self):
        super().__init__()
        self._xy = 0, 0
        self.wh = (16, 15)
        self.rgb = 0, 0, 0
        self.hud = True


class Bird(GameObject):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.rgb = 252,188,116
        self._xy = 0, 0
        self.wh=(6,8)
        self.hud = True


class PlayerScore(GameObject):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.rgb = 0,0,0
        self._xy = 0,0
        self.wh=(7,5)
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


def _init_objects_roadrunner_ram(hud=False):
    """
    (Re)Initialize the objects
    """
    objects = [Player(), Enemy(), Truck(),BirdSeeds(),BirdSeeds(),BirdSeeds(),BirdSeeds()]
    if hud:
        objects.extend([ThisWaySign(),Bird(),Bird(),Cactus(),Cactus(), PlayerScore(), PlayerScore(), PlayerScore()])
    # if hud:
    #     global plscore
    #     plscore = PlayerScore()
    #     global enscore
    #     enscore = EnemyScore()
    #     objects.extend([plscore, enscore, Logo(),
    #                     Clock(63, 17, 6, 7), Clock(73, 18, 2, 5),
    #                     Clock(79, 17, 6, 7), Clock(87, 17, 6, 7)])
    return objects


def _detect_objects_roadrunner_revised(objects, ram_state, hud=False):
    """
    For all 3 objects:
    (x, y, w, h, r, g, b)
    """
    player, enemy,truck = objects[:3]
    player.xy = ram_state[80], ram_state[3] + 95
    if ram_state[81] > 145: # Removing the enemy
        objects[1] = None
    elif enemy is None:
        enemy = Enemy()
        objects[1] = enemy
    if enemy is not None:
        enemy.xy = ram_state[81], ram_state[5] + 98
    
    if ram_state[43]==0: # Removing the enemy
        objects[2] = None
    elif truck is None:
        truck = Truck()
        objects[2] = truck
    if truck is not None:
        truck.xy=ram_state[42],157 if (ram_state[43]==1) else 127
    objects[3]=None
    # BirdSeeds
    pos_init=ram_state[89]
    dist1=[-30,-67,-49,18,-59,-22,18,-67]
    dist2=[-30,95,-47,20,-56,-20,20,94]
    loc=ram_state[90]-1
    if ram_state[36]==31: #bottom seed
        seed1=BirdSeeds()
        seed1.xy=correction(pos_init+dist1[loc]+3*dist2[loc]),165
        objects[3]=seed1
    else:
        objects[3]=None
    if ram_state[37]==31: #second bottom seed
        seed2=BirdSeeds()
        seed2.xy=correction(pos_init+dist1[loc]+2*dist2[loc]),151
        objects[4]=seed2
    else:
        objects[4]=None

    if ram_state[38]==31: #second top seed
        seed3=BirdSeeds()
        seed3.xy=correction(pos_init+dist1[loc]+dist2[loc]),137
        objects[5]=seed3
    else:
        objects[5]=None    

    if ram_state[39]==31: #top seed
        seed4=BirdSeeds()
        seed4.xy=correction(pos_init+dist1[loc]),124
        objects[6]=seed4
    else:
        objects[6]=None

    if hud:
        #Signs
        if ram_state[82]>145 or ram_state[82]<=0:
            pass
        else:
            if ram_state[69]==0:
                twss=ThisWaySign()
                twss.xy=ram_state[82], 73
                objects[7]=twss
            elif ram_state[69]==1:
                bs=BirdSeedSign()
                bs.xy=ram_state[82], 73
                objects[7]=bs
            elif ram_state[69]==2:
                bs=CarsAheadSign()
                bs.xy=ram_state[82], 73
                objects[7]=bs
            elif ram_state[69]==16:
                es=ExitSign()
                es.xy=ram_state[82], 73
                objects[7]=es
            else:
                objects[7]=None

        #birds
        if ram_state[68]==32:
            objects[8]=None; objects[9]=None
        elif ram_state[68]==33:
            bird1=Bird()
            bird1.xy=55,16; objects[9]=None
            objects[8]=bird1
        elif ram_state[68]==34:
            bird1=Bird()
            bird1.xy=63,16
            bird2=Bird()
            bird2.xy=55,16; objects[9]=bird2
            objects[8]=bird1
        #cactus
        if ram_state[24]<8 or ram_state[24]>147:
            objects[10]=None
        else:
            u_cac=Cactus()
            u_cac.xy=ram_state[24],46
            objects[10]=u_cac

        if ram_state[83]<8 or ram_state[83]>147:
            objects[11]=None
        else:
            l_cac=Cactus()
            l_cac.xy=ram_state[83],55
            objects[11]=l_cac

        ps1=PlayerScore()
        ps2=PlayerScore()
        ps3=PlayerScore()
        if ram_state[12]==2:
            ps1.xy=80, 182
            ps1.wh=(1, 5)
            ps2.xy=83, 182
            ps2.wh=(3, 5)
            ps3.xy=87, 182
            ps3.wh=(3, 5)
        elif ram_state[12]==1:
            ps1=None
            ps2=None
            ps3=None
        else:
            ps1.xy=80, 182
            ps1.wh=(3, 5)
            ps2.xy=83, 182
            ps2.wh=(3, 5)
            ps3.xy=87, 182
            ps3.wh=(3, 5)
        objects[12]=ps1; objects[13]=ps2; objects[14]=ps3



        # player score info 
        # PlayerScore at (87, 182), (3, 5), PlayerScore at (83, 182), (3, 5), PlayerScore at (80, 182), (1, 5)

def correction(pos):
    pos-=2
    return pos % 160

def _detect_objects_roadrunner_raw(info, ram_state):
    """
    returns unprocessed list with
    ball_x, ball_y, enemy_y, player_y
    """
    info["objects_list"] = ram_state[32:36]


# def _detect_objects_roadrunner_revised_old(info, ram_state, hud=False):
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

    # if ram_state[36]==31: #bottom seed
    #     seed1=BirdSeeds()
    #     if ram_state[90]==1:
    #         seed1.xy=correction(pos_init-60),166
    #     else:
    #         pass
    #     objects[3]=seed1
    # else:
    #     objects[3]=None
    # if ram_state[37]==31: #second bottom seed
    #     seed2=BirdSeeds()
    #     if ram_state[90]==1:
    #         seed2.xy=correction(pos_init-40),152
    #     else:
    #         pass
    #     objects[4]=seed2
    # else:
    #     objects[4]=None

    # if ram_state[38]==31: #second top seed
    #     seed3=BirdSeeds()
    #     if ram_state[90]==1:
    #         seed3.xy=correction(pos_init-20),138
    #     else:
    #         pass
    #     objects[5]=seed3
    # else:
    #     objects[5]=None    

    # if ram_state[39]==31: #top seed
    #     seed4=BirdSeeds()
    #     if ram_state[90]==1:
    #         seed4.xy=correction(pos_init),124
    #     else:
    #         pass
    #     objects[6]=seed4
    # else:
    #     objects[6]=None