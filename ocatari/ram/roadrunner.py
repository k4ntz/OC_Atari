from .game_objects import GameObject, NoObject
from .utils import match_objects
import sys

"""
RAM extraction for the game Road Runner.
"""

MAX_NB_OBJECTS = {"Player": 1, "Enemy": 1, "Seed": 4, "Truck": 1, "RoadCrack": 2, "AcmeMine": 4, "SteelShot": 4, "Turret": 1, "TurretBall": 2, "Rock": 2}
MAX_NB_OBJECTS_HUD = {"Player": 1, "Enemy": 1, "Seed": 4, "Truck": 2,"RoadCrack": 2,  "AcmeMine": 4,"SteelShot" :4, "Turret": 1, "TurretBall": 2, "Rock": 2, "Sign":1, 'Cactus': 2, "Lives": 2}


class Player(GameObject):
    """
    The player figure i.e, the Road Runner.
    """

    def __init__(self):
        super().__init__()
        self._xy = 0, 0
        self.wh = (8, 32)
        self.rgb = 101, 111, 228
        self.hud = False


class Enemy(GameObject):
    """
    Wile E. Coyote.
    """

    def __init__(self):
        super().__init__()
        self._xy = 0, 0
        self.wh = (7, 29)
        self.rgb = 198, 108, 58
        self.hud = False


class Seed(GameObject):
    """
    The collectable piles of birdseed on the roadway.
    """

    def __init__(self):
        super().__init__()
        self._xy = 0, 0
        self.wh = (5, 4)
        self.rgb = 84, 92, 214
        self.hud = False


class AcmeMine(GameObject):
    """
    The landmines planted along the road.
    """

    def __init__(self):
        super().__init__()
        self._xy = 0, 0
        self.wh = (4, 4)
        self.rgb = 84, 92, 214
        self.hud = False

#Level 3
class SteelShot(GameObject):
    """
    The landmines planted along the road.
    """
    def __init__(self):
        super().__init__()
        self._xy = 0, 0
        self.wh = (10, 3)
        self.rgb = 84, 92, 214
        self.hud = False


class Truck(GameObject):
    """
    The speeding trucks.
    """

    def __init__(self):
        super().__init__()
        self._xy = 0, 0
        self.wh = (16, 18)
        self.rgb = 198, 108, 58
        self.hud = False


class Cactus(GameObject):
    """
    Cactus in the background (HUD).
    """

    def __init__(self):
        super().__init__()
        self._xy = 0, 0
        self.wh = (8, 8)
        self.rgb = 187, 187, 53
        self.hud = True


class Tree(GameObject):
    """
    Tree in the background (HUD).
    """

    def __init__(self):
        super().__init__()
        self._xy = 0, 0
        self.wh = (5, 8)
        self.rgb = 187, 187, 53
        self.hud = True

#Level 2
class RoadCrack(GameObject):
    """
    Damaged road segments (cliffs??).
    """

    def __init__(self):
        super().__init__()
        self._xy = 0, 0
        self.wh = (14, 32)
        self.rgb = 181, 83, 40
        self.hud = False

#Level 4
class Turret(GameObject):
    """
    Wile E. Coyote's cannons along the road.
    """

    def __init__(self):
        super().__init__()
        self._xy = 0, 0
        self.wh = (12, 8)
        self.rgb = 66, 72, 200
        self.hud = False

class TurretBall(GameObject):
    """
    The projectiles shot from the cannons.
    """

    def __init__(self):
        super().__init__()
        self._xy = 0, 0
        self.wh = (4, 4)
        self.rgb = 198, 108, 58
        self.hud = False

#Level 6
class Rock(GameObject):
    """
    The rocks tumbling down on the road.
    """

    def __init__(self):
        super().__init__()
        self._xy = 0, 0
        self.wh = (8, 11)
        self.rgb = 181, 83, 40
        self.hud = False


class Sign(GameObject):
    """
    The occasional road signs and billboards (HUD).
    """

    def __init__(self):
        super().__init__()
        self._xy = 0, 0
        self.wh = (16, 15)
        self.rgb = 0, 0, 0
        self.hud = True

class Lives(GameObject):
    """
    The birds flying by.
    """

    def __init__(self):
        super().__init__()
        self._xy = 55, 16
        self.wh = (6, 8)
        self.rgb = 252, 188, 116
        self.hud = True


class Score(GameObject):
    """
    The player's score display (HUD).
    """

    def __init__(self):
        super().__init__()
        self._xy = 0, 0
        self.wh = (7, 5)
        self.rgb = 0, 0, 0
        self.hud = True

class Bonus(GameObject):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._xy = 0, 0
        self.wh = (7, 5)
        self.rgb = 0, 0, 0
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
    objects = [Player()]
    objects.extend([NoObject()]) #Enemy
    objects.extend([NoObject()]) #Truck
    objects.extend([NoObject()]*4) #Seeds
    objects.extend([NoObject()]*4) #AcmeMine
    objects.extend([NoObject()]*4) #SteelShot
    objects.extend([NoObject()]*2) #RoadCrack
    objects.extend([NoObject()]) #Turret
    objects.extend([NoObject()]*2) #Turretball
    objects.extend([NoObject()]*2) #Rock
    if hud:
        sign = [NoObject()]
        birds = [NoObject()]*2
        cacs = [NoObject()]*4 #Tree+cactus
        score = [NoObject()]
        bonus = [NoObject()]
        sign =[NoObject()]

        objects.extend(sign+birds+ cacs +score+bonus+sign)
    return objects

def _detect_objects_ram(objects, ram_state, hud=False):
    """
    For all 3 objects:
    (x, y, w, h, r, g, b)
    """

    level = ram_state[22]
    y_offset = 95
    if level == 1:
        y_offset = 102
    elif level == 3:
        y_offset = 85
    elif level == 5:
        y_offset = 125
    elif level == 7:
        y_offset = 84

    # player
    if ram_state[80] < 150:
        if type(objects[0]) is NoObject:
            objects[0] = Player()
        player = objects[0]
        if ram_state[3]:
            player.xy = ram_state[80], ram_state[3] + y_offset
        else:
            player.xy = ram_state[80], ram_state[10] + y_offset
        player.wh = (8, 24) if ram_state[41] == 6 else (8, 32)
    else:
        objects[0] = None

    # enemy
    if 8 < ram_state[81] < 144:
        if type(objects[1]) is NoObject:
            objects[1] = Enemy()

        enemy = objects[1]

        if level&1:
            y_offset-=2
        else:
            y_offset+=3
        
        if not ram_state[43] and (109 < ram_state[1] < 121 or 179 < ram_state[1] < 191): # sitting on rocket racer 
            enemy.xy = ram_state[81] + 3, (ram_state[5]&127) + y_offset + 8
            enemy.wh = 12, 24
        else:
            enemy.xy = ram_state[81] + 1, (ram_state[5]&127) + y_offset
            enemy.wh = 7, 29
    else:
        objects[1] = NoObject()
    
    # truck
    if ram_state[43]:
        if type(objects[2]) is NoObject:
            objects[2] = Truck()
        objects[2].xy = ram_state[42] - 2, 157 if (ram_state[43] == 1) else 127
    else:
        objects[2] = NoObject()
    
    # Seed or AcmeMine
    if not level&1:

        # position lookups
        pos_init = ram_state[89]
        dist1 = [-30, -67, -49, 18, -59, -22, 18, -67]
        dist2 = [-30, 95, -47, 20, -56, -20, 20, 94]
        loc = ram_state[90]-1

        for i in range(4):
            if ram_state[36+i] == 31:  # bottom seed or AcmeMine
                if type(objects[3+i]) is NoObject:
                    objects[3+i] = Seed()
                    objects[7+i] = NoObject()
                    objects[11+i] = NoObject()
                objects[3+i].xy = (pos_init + dist1[loc] + (3-i) * dist2[loc] - 2)%160, 165 - (i*14)
            elif ram_state[36+i] == 47:
                if type(objects[7+i]) is NoObject:
                    objects[3+i] = NoObject()
                    objects[7+i] = AcmeMine()
                    objects[11+i] = NoObject()
                objects[7+i].xy = (pos_init + dist1[loc] + (3-i) * dist2[loc] + 2)%160, 164 - (i*14)
            elif ram_state[36+i] == 63:
                if type(objects[11+i]) is NoObject:
                    objects[3+i] = NoObject()
                    objects[7+i] = NoObject()
                    objects[11+i] = SteelShot()
                objects[11+i].xy = (pos_init + dist1[loc] + (3-i) * dist2[loc])%160, 165 - (i*14)
            else:
                objects[3+i] = NoObject()
                objects[7+i] = NoObject()
                objects[11+i] = NoObject()
    elif level > 1:
        
        # position lookups
        pos_init = ram_state[89]
        dist1 = [-25, -53, -39, 10, -46, -17, 11, -17]
        dist2 = [-11, -39, -25, 24, -32, -3, 25, -3]
        loc = ram_state[90]-1

        for i in range(4):
            dist = -2
            if i == 1:
                objects[4] = NoObject()
                objects[8] = NoObject()
                objects[12] = NoObject()
                continue
            elif i == 2:
                dist = dist1[loc]
            elif i == 0:
                dist = dist2[loc]

            if ram_state[36+i] == 31:  # bottom seed or AcmeMine
                if type(objects[3+i]) is NoObject:
                    objects[3+i] = Seed()
                    objects[7+i] = NoObject()
                    objects[11+i] = NoObject()
                objects[3+i].xy = (pos_init + dist - 2)%160, 138 - (i*11)
            elif ram_state[36+i] == 47:
                if type(objects[7+i]) is NoObject:
                    objects[3+i] = NoObject()
                    objects[7+i] = AcmeMine()
                    objects[11+i] = NoObject()
                objects[7+i].xy = (pos_init + dist + 1)%160, 138 - (i*11)
            elif ram_state[36+i] == 63:
                if type(objects[11+i]) is NoObject:
                    objects[3+i] = NoObject()
                    objects[7+i] = NoObject()
                    objects[11+i] = SteelShot()
                objects[11+i].xy = (pos_init + dist)%160, 139 - (i*11)
            else:
                objects[3+i] = NoObject()
                objects[7+i] = NoObject()
                objects[11+i] = NoObject()
    else:
        # On second level remove all the birdseeds
        objs = list(range(4, 7))
        objs.extend(list(range(8, 15)))
        for i in objs:
            objects[i] = NoObject()

        if 8 < ram_state[89] < 151:
            if ram_state[39] == 31:  # bottom seed or AcmeMine
                if type(objects[3]) is NoObject:
                    objects[3] = Seed()
                    objects[7] = NoObject()
                objects[3].xy = ram_state[89] - 6, 146 - (16*ram_state[55])
            elif ram_state[39] == 47:
                if type(objects[7]) is NoObject:
                    objects[3] = NoObject()
                    objects[7] = AcmeMine()
                objects[7].xy = ram_state[89] - 4, 146 - (16*ram_state[55])
            else:
                objects[3] = NoObject()
                objects[7] = NoObject()
        else:
            objects[3] = NoObject()
            objects[7] = NoObject()

    # RoadCrack
    if level == 1:
        if 8 < ram_state[82] < 151:
            if type(objects[15]) is NoObject:
                objects[15] = RoadCrack()
            objects[15].xy = ram_state[82] - 7, 124
        else:
            objects[15] = NoObject()

        if ram_state[46]:
            if type(objects[16]) is NoObject:
                objects[16] = RoadCrack()
            objects[16].xy = (ram_state[82] + 64 - 7)%160, 124
        else:
            objects[16] = NoObject()
    else:
        objects[15] = NoObject()
        objects[16] = NoObject()

    # Turret
    if level in [3, 7] and ram_state[48] and 8 < ram_state[55] < 145:
        if type(objects[17]) is NoObject:
            objects[17] = Turret()
        x = ram_state[55]-6 if ram_state[91] == 33 else ram_state[55]-1
        objects[17].xy = x, 128
    else:
        objects[17] = NoObject()
    
    # TurretBall
    if level in [3, 7] and 8 < ram_state[42] < 151:
        if type(objects[2]) is NoObject:
            if type(objects[18]) is NoObject:
                objects[18] = TurretBall()
            objects[18].xy = ram_state[42]- 1, 128
        else:
            objects[18] = NoObject()
    else:
        objects[18] = NoObject()

    if level == 5 and 0 < ram_state[48] < 100:
        rock_offsets  = [(21, 29), (-9, -15), (15, 20), (-1, -4), (-7, -13), (-5, -10), (7, 8), (5, 5), (16, 19)]
        if type(objects[19]) is NoObject:
            objects[19] = Rock()
            objects[20] = Rock()
        offsets = rock_offsets[(ram_state[56]>>1)]
        objects[19].xy = ram_state[82] + ram_state[91] + offsets[0] - 2, ram_state[48] + 94
        objects[20].xy = ram_state[82] + ram_state[91] + offsets[1] - 2, ram_state[48] + 108
    else:
        objects[19] = NoObject()
        objects[20] = NoObject()

    if hud:
        # Signs
        if not level&1 and 0 < ram_state[82] < 146 and ram_state[69] in [0, 1, 2, 16]:
            if type(objects[-4]) is NoObject:
                objects[-4] = Sign()
            objects[-4].xy = ram_state[82], 73
        else:
            objects[-4] = NoObject()

        # cactus
        if 7 < ram_state[83] < 148:
            if type(objects[-3]) is NoObject:
                objects[-3] = Cactus()
            objects[-3].xy = ram_state[24], 46
        else:
            objects[-3] = NoObject()

        if 7 < ram_state[83] < 148:
            if type(objects[-2]) is NoObject:
                objects[-2] = Cactus()
            objects[-2].xy = ram_state[83], 55
        else:
            objects[-2] = NoObject()

        # life
        life = ram_state[68]&31
        if life:
            if type(objects[-1]) is NoObject:
                objects[-1] = Lives()
            objects[-1].wh = 6 + 8*(life-1), 8
        else:
            objects[-1] = NoObject()
        # Removing player score since they are not really needed and they create problems in some levels
        # ps1=PlayerScore()
        # ps2=PlayerScore()
        # ps3=PlayerScore()
        # if ram_state[13]==2:
        #     ps1.xy=80, 182
        #     ps1.wh=(1, 5)
        #     ps2.xy=83, 182
        #     ps2.wh=(3, 5)
        #     ps3.xy=87, 182
        #     ps3.wh=(3, 5)
        # elif ram_state[14]==1:
        #     ps1=None
        #     ps2=None
        #     ps3=None
        # else:
        #     ps1.xy=80, 182
        #     ps1.wh=(3, 5)
        #     ps2.xy=83, 182
        #     ps2.wh=(3, 5)
        #     ps3.xy=87, 182
        #     ps3.wh=(3, 5)
        # objects[14]=ps1; objects[15]=ps2; objects[16]=ps3

        # player score info
        # PlayerScore at (87, 182), (3, 5), PlayerScore at (83, 182), (3, 5), PlayerScore at (80, 182), (1, 5)

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
