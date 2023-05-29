from .game_objects import GameObject
import sys 

MAX_NB_OBJECTS = {"Player": 1, "Enemy": 1, "BirdSeeds": 1, "Truck": 6}
MAX_NB_OBJECTS_HUD = {'Cactus': 6, 'Sign': 1}# 'Score': 1}


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

class RoadCrack(GameObject):
    def __init__(self):
        super().__init__()
        self._xy = 0, 0
        self.rgb =181, 83,40
        self.hud = False
        self.wh = (14,32)

class AcmeMine(GameObject):
    def __init__(self):
        super().__init__()
        self.rgb = 255,255,255#84,92,214
        self.hud = False
        self._xy = 0, 0
        self.wh = (4,3)

class Turret(GameObject):
    def __init__(self):
        super().__init__()
        self.rgb = 66,72,200
        self.hud = False
        self._xy = 0, 0
        self.wh = (12, 8)

class TurretBall(GameObject):
    def __init__(self):
        super().__init__()
        self.rgb = 198,108,58
        self.hud = False
        self._xy = 0, 0
        self.wh = (4,4)

class Stone(GameObject):
    def __init__(self):
        super().__init__()
        self.rgb = 181,83,40
        self.hud = False
        self._xy = 0, 0
        self.wh = (8, 11)

class Cactus(GameObject):
    def __init__(self):
        super().__init__()
        self._xy = 0, 0
        self.wh = (8, 8)
        self.rgb = 187, 187, 53
        self.hud = True


class Sign(GameObject):
    def __init__(self):
        super().__init__()
        self._xy = 0, 0
        self.wh = (16, 15)
        self.rgb = 0, 0, 0
        self.hud = True

class Bird(GameObject):
    def __init__(self):
        super().__init__()
        self.rgb = 252,188,116
        self._xy = 0, 0
        self.wh=(6,8)
        self.hud = True


class PlayerScore(GameObject):
    def __init__(self):
        super().__init__()
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
    objects = [Player(), Enemy(), Truck(),BirdSeeds(),BirdSeeds(),BirdSeeds(),BirdSeeds(), RoadCrack(), AcmeMine()]
    if hud:
        objects.extend([Sign(),Bird(),Bird(),Cactus(),Cactus(), PlayerScore(), PlayerScore(), PlayerScore()])
    return objects


def _detect_objects_roadrunner_revised(objects, ram_state, hud=False):
    """
    For all 3 objects:
    (x, y, w, h, r, g, b)
    """
    player, enemy,truck = objects[:3]
    player.xy = ram_state[80], ram_state[3] + 95
    if ram_state[81] > 150: # Removing the enemy
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
    
    # RoadCrack
    if ram_state[82]>150 or ram_state[82]<=8:
        objects[7]=None
    else:
        if ram_state[69]<=18 and ram_state[69]>=5:
            rc=RoadCrack()
            rc.xy=ram_state[82]-5, 125
            objects[7]=rc
        else:
            objects[7]=None

    #AcmeMine
    if ram_state[89]>150 or ram_state[89]<=8:
        objects[8]=None
    else:
            am=AcmeMine()
            if ram_state[55]==0:
                am.xy=ram_state[89]-4, 147
                objects[8]=am
            elif ram_state[55]==1:
                am.xy=ram_state[89]-4, 131
                objects[8]=am
            else:
                objects[8]=None


    if hud:
        #Signs
        if ram_state[82]>145 or ram_state[82]<=0:
            pass
        else:
            if ram_state[69]==0 or ram_state[69]==1 or ram_state[69]==2 or ram_state[69]==16:
                twss=Sign()
                twss.xy=ram_state[82], 73
                objects[9]=twss
            else:
                objects[9]=None

        #birds
        if ram_state[68]==32:
            objects[10]=None; objects[11]=None
        elif ram_state[68]==33:
            bird1=Bird()
            bird1.xy=55,16; objects[11]=None
            objects[10]=bird1
        elif ram_state[68]==34:
            bird1=Bird()
            bird1.xy=63,16
            bird2=Bird()
            bird2.xy=55,16; objects[11]=bird2
            objects[10]=bird1
        #cactus
        if ram_state[24]<8 or ram_state[24]>147:
            objects[12]=None
        else:
            u_cac=Cactus()
            u_cac.xy=ram_state[24],46
            objects[12]=u_cac

        if ram_state[83]<8 or ram_state[83]>147:
            objects[13]=None
        else:
            l_cac=Cactus()
            l_cac.xy=ram_state[83],55
            objects[13]=l_cac

        print(ram_state[13:15])
        ps1=PlayerScore()
        ps2=PlayerScore()
        ps3=PlayerScore()
        if ram_state[13]==2:
            ps1.xy=80, 182
            ps1.wh=(1, 5)
            ps2.xy=83, 182
            ps2.wh=(3, 5)
            ps3.xy=87, 182
            ps3.wh=(3, 5)
        elif ram_state[14]==1:
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
        objects[14]=ps1; objects[15]=ps2; objects[16]=ps3



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