from .game_objects import GameObject
import sys 

"""
RAM extraction for the game Frostbite.
"""

MAX_NB_OBJECTS = {"Player": 1, "Bird": 8, "Crab":8, "Clam":8,"GreenFish":8,"WhitePlate":24, "BluePlate":24,"Bear":1, "House":1,"CompletedHouse":1,"FrostBite":1}
MAX_NB_OBJECTS_HUD = {"LifeCount":1, "PlayerScore":4, "Degree":2}# 'Score': 1}

class Player(GameObject):
    """
    The player figure: Frostbite Bailey.
    """
    
    def __init__(self):
        super().__init__()
        self._xy = 0, 0
        self.wh = (8, 17)
        self.rgb = 198,108,58
        self.hud = False


class GreenFish(GameObject):
    """
    The fresh fish swimming by regularly.
    """
    
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
    """
    The white, untouched ice floes.
    """
    
    def __init__(self):
        super().__init__()
        self.rgb = 214,214,214
        self.hud = False
        self.wh = (24, 7)
        self._xy = 0, 0

class BluePlate(GameObject):
    """
    The ice floes that have turned blue by jumping on them.
    """
    
    def __init__(self):
        super().__init__()
        self.rgb = 84,138,210
        self.hud = False
        self.wh = (24, 7)
        self._xy = 0, 0

class Bird(GameObject):
    """
    The wild snowgeese.
    """
    
    def __init__(self):
        super().__init__()
        self.rgb = 132,144,252
        self.hud = False
        self.wh = (8, 7)
        self._xy = 0, 0

class Bear(GameObject):
    """
    The dangerous grizzly polar bears on the shore (level 4).
    """
    
    def __init__(self):
        super().__init__()
        self.rgb = 0,0,0
        self.hud = False
        self.wh = (14, 15)
        self._xy = 0, 0

class Crab(GameObject):
    """
    The dangerous Alaskan king crabs.
    """
    
    def __init__(self):
        super().__init__()
        self.rgb = 213,130,74
        self.hud = False
        self.wh = (8, 7)
        self._xy = 0, 0

class Clam(GameObject):
    """
    The dangerous clams.
    """
    
    def __init__(self):
        super().__init__()
        self.rgb = 210,210,64
        self.hud = False
        self._xy = 0, 0
        self.wh=(8, 7)

class House(GameObject):
    """
    The igloo Frostbite Bailey is trying to build.
    """
    
    def __init__(self):
        super().__init__()
        self.rgb = 142,142,142
        self.hud = False
        self.wh = (8, 18)
        self._xy = 0, 0

class CompletedHouse(GameObject):
    """
    The finished igloo.
    """
    
    def __init__(self):
        super().__init__()
        self.rgb = 0,0,0
        self.hud = False
        self.wh = (34,20)
        self._xy = 0, 0


class LifeCount(GameObject):
    """
    The indicator for the player's lives.
    """
    
    def __init__(self):
        super().__init__()
        self.rgb =132,144,252
        self.hud = True
        self.wh = (8, 18)
        self._xy = 0, 0


# class Score(GameObject):
#     def __init__(self):
#         super().__init__()
#         self.rgb =132,144,252
#         self.hud = True
#         self.wh = (8, 18)
#         self._xy = 0, 0

class Degree(GameObject):
    """
    The temperature display.
    """
    
    def __init__(self):
        super().__init__()
        self.rgb =132,144,252
        self.hud = True
        self.wh = (8, 18)
        self._xy = 0, 0


class PlayerScore(GameObject):
    """
    The player's score display.
    """
    
    def __init__(self):
        super().__init__()
        self.rgb =132,144,252
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


def _init_objects_ram(hud=False):
    """
    (Re)Initialize the objects
    """
    objects = [Player()]
    objects.extend([Bird()]*4)
    objects.extend([Bear()])
    objects.extend([None]*24) #for the plates
    objects.extend([None]*12) #for bird clams and crabs
    objects.extend([House(),CompletedHouse(),None]) # None was frostbite before
    if hud:
        objects.extend([LifeCount(),Degree(),Degree(),PlayerScore(),PlayerScore(),PlayerScore(),PlayerScore()])
    return objects

def _detect_objects_ram(objects, ram_state, hud=False):
    """
    For all 3 objects:
    (x, y, w, h, r, g, b)
    """
    # 106 ram_state is somewhat controlling the y of the player when it's dying by sinking
    player,bird1,bird2,bird3,bird4= objects[:5]
    player.xy =  ram_state[102] -1,ram_state[100]+30
    objects[0]=player
    # if ram_state[101]==0:
    #     f=FrostBite()
    #     f.xy=ram_state[102]-1,ram_state[100]+30
    #     objects[44]=f
    # else:
    #     objects[44]=None
    # Tackling enemies/birds here
    if ram_state[35]<30 and ram_state[36]<30 and ram_state[37]<30 and ram_state[38]<30:
        if ram_state[84]>7 and ram_state[84]<155:
            bird1=WhatObject(ram_state[39])
            bird1.xy=ram_state[84],160
            bird1.wh=(8,7) if ram_state[35]!=26 else (7,6)
            objects[1]=bird1
        else:
            objects[1]=None
        if ram_state[85]>7 and ram_state[85]<155:
            bird2=WhatObject(ram_state[40])
            bird2.xy=ram_state[85],134
            bird2.wh=(8,7) if ram_state[36]!=26 else (7,6)
            objects[2]=bird2
        else:
            objects[2]=None
        if ram_state[86]>7 and ram_state[86]<155:
            bird3=WhatObject(ram_state[41])
            bird3.xy=ram_state[86],108
            bird3.wh=(8,7) if ram_state[37]!=26 else (7,6)
            objects[3]=bird3
        else:
            objects[3]=None
        if ram_state[87]>7 and ram_state[86]<155:
            bird4=WhatObject(ram_state[42])
            bird4.xy=ram_state[87],82
            bird4.wh=(8,7) if ram_state[38]!=26 else (7,6)
            objects[4]=bird4
        else:
            objects[4]=None
    else:
        objects[1]=None; objects[2]=None; objects[3]=None;objects[4]=None

        ram_state_list=[84,85,86,87]
        object_list=[39,40,41,42]
        wh_list=[35,36,37,38]
        y_list=[160,134,108,82]
        for i in range(4):
            if ram_state[ram_state_list[i]]>7 and ram_state[ram_state_list[i]]<155:
                if ram_state[ram_state_list[i]]<35 or ram_state[ram_state_list[i]]>120:
                    bird1=WhatObject(ram_state[object_list[i]])
                    bird1.xy=ram_state[ram_state_list[i]],y_list[i]
                    bird1.wh=(8,7) if ram_state[wh_list[i]]!=26 else (7,6)
                    objects[30+2*i]=bird1
                    objects[31+2*i]=None
                else:
                    bird1=WhatObject(ram_state[object_list[i]])
                    bird1.xy=ram_state[ram_state_list[i]],y_list[i]
                    bird1.wh=(8,7) if ram_state[wh_list[i]]!=26 else (7,6)
                    bird2=WhatObject(ram_state[object_list[i]])
                    bird2.xy=ram_state[ram_state_list[i]]+33,y_list[i]
                    bird2.wh=(8,7) if ram_state[wh_list[i]]!=26 else (7,6)
                    objects[30+2*i]=bird1
                    objects[31+2*i]=bird2
            else:
                objects[30+2*i]=None
                objects[31+2*i]=None 


    # Adding the bear
    if ram_state[104]==140:
        objects[5]=None
    else:
        bear=Bear()
        bear.xy=ram_state[104]+3,58
        objects[5]=bear
    
    # Adding the Plates
    num_plates=3 if ram_state[30]==8 else 6
    start_loc=9 if ram_state[30]==8 else 13
    plate_diff=32 if ram_state[30]==8 else 16
    size_plates=(24,7) if ram_state[30]==8 else (16,7)
    ram_list=[31,32,33,34]
    pos_list=[174,148,122,96]
    which_plate=[43,44,45,46]
    for i in range(num_plates*4):
        temp=whichPlate(ram_state[which_plate[int(i/num_plates)]])
        temp.xy=correction(ram_state[ram_list[int(i/num_plates)]]+int(i%num_plates)*plate_diff-start_loc),pos_list[int(i/num_plates)]
        temp.wh=size_plates
        objects[6+i]=temp
    
    # House 
    position_list=[(112,51),(112,51),(112,51),(112,51),(112,47),(112,47),(112,47),(112,47),(112,42),(112,42),(112,42),(112,42),(112,39),(112,39),(112,35)]
    size_list=[(8,4),(16,4),(24,4),(32,4),(32,8),(32,8),(32,8),(32,8),(32,13),(32,13),(32,13),(32,13),(32,16),(32,16),(32,20)]
    if ram_state[77]==255 or ram_state[77]==15:
        objects[42]=None
    else:
        h=House()
        h.xy=position_list[ram_state[77]]
        h.wh=size_list[ram_state[77]]
        objects[42]=h

    # Completed House
    if ram_state[77]==15:
        c=CompletedHouse()
        c.xy=112,35
        c.wh=32,20
        objects[43]=c
    else:
        objects[43]=None

    if hud:
        # LifeCount
        if ram_state[76]!=0:
            l=LifeCount()
            l.xy=63,22
            l.wh=(6,10)
            objects[45]=l
        else:
            objects[45]=None
        # Time or degrees
        if ram_state[101]<=9:
            d1=Degree()
            d1.xy=31,22
            d1.wh=(6,8)
            objects[46]=None
            objects[47]=d1
        else:
            d1=Degree()
            d1.xy=31,22
            d1.wh=(6,8)
            d2=Degree()
            d2.xy=23,22
            d2.wh=(6,8)
            objects[46]=d2
            objects[47]=d1
        
        # Player Score
        if ram_state[73]==0 and ram_state[74]==0:
            p=PlayerScore()
            p.xy=63,10
            p.wh=(6,8)
            objects[51]=p
            objects[50]=None ; objects[49]=None ; objects[48]=None 
        elif ram_state[73]==0 and ram_state[74]!=0:
            p1=PlayerScore()
            p1.xy=63,10
            p1.wh=(6,8)
            objects[51]=p1
            p2=PlayerScore()
            p2.xy=55,10
            p2.wh=(6,8)
            objects[50]=p2
            objects[49]=None; objects[48]=None
        elif ram_state[72]==0 and ram_state[73]!=0:
            p1=PlayerScore()
            p1.xy=63,10
            p1.wh=(6,8)
            objects[51]=p1
            p2=PlayerScore()
            p2.xy=55,10
            p2.wh=(6,8)
            objects[50]=p2
            p3=PlayerScore()
            p3.xy=48,10
            p3.wh=(6,8)
            objects[49]=p3
            objects[48]=None


def whichPlate(pos):
    # Make decision whether to return Whiteplate or BluepLate
    if pos==12:
        return WhitePlate()
    else:
        return BluePlate()

def correction(pos):
    return pos%160

def WhatObject(pos):
    if pos==143:
        return Bird()
    elif pos==56:
        return Crab()
    elif pos==202:
        return GreenFish()
    elif pos==26:
        return Clam()

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
