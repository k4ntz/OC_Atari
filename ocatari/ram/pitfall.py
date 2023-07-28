from .game_objects import GameObject
import sys 
import numpy as np

"""
RAM extraction for the game Pitfall.

"""

MAX_NB_OBJECTS = {"Player": 1,"Wall":1,"Logs":5,"StairPit":4,"Pit":3,"Scorpion":1,"Rope":1,"Snake":1,"Tarpit":1,"Waterhole":1,"Crocodile":1,"GoldenBar":1,"Fire":1}
MAX_NB_OBJECTS_HUD = {"LifeCount":3,"PlayerScore":6,"Timer":5}

class Player(GameObject):
    """
    The player figure: Pitfall Harry.
    """
    
    def __init__(self):
        super().__init__()
        self._xy = 0, 0
        self.wh = (7, 20)
        self.rgb = 53,95,24
        self.hud = False

class Wall(GameObject):
    """
    The underground brick walls.
    """
    
    def __init__(self):
        super().__init__()
        self.xy=0,0
        self.wh=(7,32)
        self.rgb = 167,26,26
        self.hud = False

class Logs(GameObject):
    """
    The logs.
    """
    
    def __init__(self):
        super().__init__()
        self.xy=0,0
        self.wh=(6,14)
        self.rgb = 105,105,15
        self.hud = False

class StairPit(GameObject):
    """
    The escape shafts from the underground.
    """
    
    def __init__(self):
        super().__init__()
        self.xy=0,0
        self.wh=(8,6)
        self.rgb = 0,0,0
        self.hud = False

class Pit(GameObject):
    """
    The open holes in the ground.
    """
    
    def __init__(self):
        super().__init__()
        self.xy=0,0
        self.wh=(12,6)
        self.rgb = 252,188,116
        self.hud = False

class Scorpion(GameObject):
    """
    The scorpions.
    """
    
    def __init__(self):
        super().__init__()
        self.xy=0,0
        self.wh=(7,10)
        self.rgb = 236,236,236
        self.hud = False

class Rope(GameObject):
    """
    The swinging vines.
    """
    
    def __init__(self):
        super().__init__()
        self.xy=0,0
        self.wh=(1,1)
        self.rgb = 72,72,0
        self.hud = False

class Snake(GameObject):
    """
    The snakes.
    """
    
    def __init__(self):
        super().__init__()
        self.xy=0,0
        self.wh=(8,14)
        self.rgb = 167,26,26
        self.hud = False

class Tarpit(GameObject):
    """
    The tar pits.
    """
    
    def __init__(self):
        super().__init__()
        self.xy=0,0
        self.wh=(64,10)
        self.rgb = 0,0,0
        self.hud = False

class Waterhole(GameObject):
    """
    The swamps.
    """
    
    def __init__(self):
        super().__init__()
        self.xy=0,0
        self.wh=(64,10)
        self.rgb = 45,109,152
        self.hud = False

class Crocodile(GameObject):
    """
    The crocodiles.
    """
    
    def __init__(self):
        super().__init__()
        self.xy=0,0
        self.wh=(8,8)
        self.rgb = 20,60,0
        self.hud = False

class GoldenBar(GameObject):
    """
    The collectable gold bars.
    """
    
    def __init__(self):
        super().__init__()
        self.xy=0,0
        self.wh=(7,13)
        self.rgb = 252,252,84
        self.hud = False

class SilverBar(GameObject):
    """
    The collectable silver bars.
    """
    
    def __init__(self):
        super().__init__()
        self.xy=0,0
        self.wh=(7,13)
        self.rgb = 142,142,142
        self.hud = False

class DiamondRing(GameObject):
    """
    The collectable diamond rings.
    """
    
    def __init__(self):
        super().__init__()
        self.xy=0,0
        self.wh=(7,13)
        self.rgb = 236,236,236
        self.hud = False

class Fire(GameObject):
    """
    The open fires.
    """
    
    def __init__(self):
        super().__init__()
        self.xy=0,0
        self.wh=(8,14)
        self.rgb = 236,200,96
        self.hud = False

class MoneyBag(GameObject):
    """
    The collectable money bags.
    """
    
    def __init__(self):
        super().__init__()
        self.xy=0,0
        self.wh=(7,14)
        self.rgb = 111,111,111
        self.hud = False

class LifeCount(GameObject):
    """
    The indicator for the remaining lives (HUD).
    """
    
    def __init__(self):
        super().__init__()
        self.xy=0,0
        self.wh=(1,8)
        self.rgb =214,214,214
        self.hud = True

class PlayerScore(GameObject):
    """
    The player's score display (HUD).
    """
    
    def __init__(self):
        super().__init__()
        self.xy=0,0
        self.wh=(6,8)
        self.rgb =214,214,214
        self.hud = True

class Timer(GameObject):
    """
    The 20-minute countdown (HUD).
    """
    
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
    global ram_18
    ram_18=10
    global prev_x
    prev_x=78
    objects = [Player(),Wall(),Logs(),Logs(),Logs(),StairPit(),StairPit(),Pit(),Pit(),Scorpion()] #10
    objects.extend([Rope(),Snake(),Tarpit(),Waterhole(),Crocodile(),Crocodile(),Crocodile()]) #7
    objects.extend([GoldenBar()])
    if hud:
        objects.extend([LifeCount(),LifeCount(),LifeCount()]) #3
        objects.extend([PlayerScore()]*4)
        objects.extend([Timer()]*4)
        objects.extend([PlayerScore()])
    return objects

def _detect_objects_pitfall_revised(objects, ram_state, hud=False):
    """
    For all 3 objects:
    (x, y, w, h, r, g, b)
    """
    # There are 8 treasures; Define all the classes and at the time of detection replace with GoldenBar index 
    player,= objects[:1]
    objects[:]=[None]*24    # snapshot = pickle.load(open("/home/anurag/Desktop/HiWi_OC/OC_Atari/pit_4.pkl", "rb"))
    # env._env.env.env.ale.restoreState(snapshot)
    player.xy =  ram_state[97]+1,ram_state[105]+72
    objects[0]=player
    
    
    # Implementing Pits,waterholes etc
    objects[5:17]=[None]*12
    if ram_state[20]==0:
        s=StairPit()
        s.xy=76,122
        objects[6]=s
        objects[5]=None
    
    elif ram_state[20]==1:
        s=StairPit(); s.xy=76,122
        p1=Pit(); p2=Pit()
        p1.xy=48,122
        p2.xy=100,122
        objects[7]=p1; objects[8]=p2
        objects[5]=s
        objects[6]=None
        
    elif ram_state[20]==2:
        t=Tarpit()
        t.xy=48,120
        objects[12]=t

    elif ram_state[20]==4: 
        w=Waterhole(); w.xy=48,120
        objects[13]=w
        y1=122 if ram_state[46]==255 else 119
        wh1=(8,6) if ram_state[46]==255 else (8,9)
        c1=Crocodile(); c1.xy=60,y1
        c1.wh=wh1
        objects[15]=c1
        c2=Crocodile(); c2.xy=76,y1
        c2.wh=wh1
        objects[16]=c2
        c3=Crocodile(); c3.xy=92,y1
        c3.wh=wh1
        objects[17]=c3
    
    # Waterhole 
    elif ram_state[20]==3:
        w=Waterhole()
        w.xy=48,120
        objects[13]=w
    
    # Disappearing Waterhole
    elif ram_state[20]==7:
        w=Waterhole()
        if ram_state[32]==1 and ram_state[33]==3 and ram_state[34]==15 and ram_state[35]==127:
            w.xy=52,121
            w.wh=(56,9)
        if ram_state[32]==0 and ram_state[33]==1 and ram_state[34]==3 and ram_state[35]==15:
            w.xy=48,120
            w.wh=(64,10)
        if ram_state[32]==255 and ram_state[33]==255 and ram_state[34]==255 and ram_state[35]==255:
            objects[13]=None
        else:
            objects[13]=w
    # Disappearig Tarpit
    elif ram_state[20]==6:
        t=Tarpit()
        if ram_state[32]==1 and ram_state[33]==3 and ram_state[34]==15 and ram_state[35]==127:
            t.xy=52,121
            t.wh=(56,9)
        if ram_state[32]==0 and ram_state[33]==1 and ram_state[34]==3 and ram_state[35]==15:
            t.xy=48,120
            t.wh=(64,10)
        if ram_state[32]==255 and ram_state[33]==255 and ram_state[34]==255 and ram_state[35]==255:
            objects[12]=None
        else:
            objects[12]=t
    elif ram_state[20]==5:
        t=Tarpit()
        g=GoldenBar()
        g.xy=124,118
        if ram_state[32]==1 and ram_state[33]==3 and ram_state[34]==15 and ram_state[35]==127:
            t.xy=52,121
            t.wh=(56,9)
        if ram_state[32]==0 and ram_state[33]==1 and ram_state[34]==3 and ram_state[35]==15:
            t.xy=48,120
            t.wh=(64,10)
        if ram_state[32]==255 and ram_state[33]==255 and ram_state[34]==255 and ram_state[35]==255:
            objects[12]=None
        else:
            objects[12]=t


    # Implementing Scorpion
    # Remove scorpion when there is no pit
    if ram_state[29]==0:    
        s=Scorpion()
        s.xy=ram_state[99],(170 if ram_state[65]==160 else 169)
        s.wh=(7,8) if ram_state[65]==160 else (8,9)
        objects[9]=s
        objects[1]=None
    elif ram_state[29] in [1,255]:
        w=Wall()
        w.xy=ram_state[99],148
        objects[1]=w
        objects[9]=None
    else:
        objects[1]=None; objects[9]=None
    
    # Implementing Fire,snake and Treasures
    if ram_state[19]==6:
        f=Fire()
    elif ram_state[19]==7:
        f=Snake()
    
    elif ram_state[19]>=8:
        if ram_state[19]%4==0:
            f=MoneyBag()
        elif ram_state[19]%4==1:
            f=SilverBar()
        elif ram_state[19]%4==2:
            f=GoldenBar()
        elif ram_state[19]%4==3:
            f=DiamondRing()
    else:
        f=None
    if f is not None:
        f.xy=124,118
    objects[11]=f
    if objects[15] is None:
        if ram_state[19]==0 and ram_state[20]!=4: #bug in pit_10.pkl
            l1=Logs()
            l1.xy=(ram_state[98]+1)%160,118
            objects[2]=l1; objects[3]=None; objects[4]=None
        elif ram_state[19]==1:
            l1=Logs(); l2=Logs()
            l1.xy=(ram_state[98]+1)%160,118
            l2.xy=(ram_state[98]+16+1)%160,118
            objects[2]=l1; objects[3]=l2; objects[4]=None
        elif ram_state[19]==2:
            l1=Logs(); l2=Logs()
            l1.xy=(ram_state[98]+1)%160,118
            l2.xy=(ram_state[98]+32+1)%160,118
            objects[2]=l1; objects[3]=l2; objects[4]=None
        elif ram_state[19]==3:
            l1=Logs(); l2=Logs(); l3=Logs()
            l1.xy=ram_state[98]+1,119
            l2.xy=(ram_state[98]+32+1)%160,118
            l3.xy=(ram_state[98]+64+1)%160,118
            objects[2]=l1; objects[3]=l2; objects[4]=l3
        elif ram_state[19]==4 and ram_state[20]!=4:
            l1=Logs()
            l1.xy=(ram_state[98]+1)%160,118
            objects[2]=l1; objects[3]=None; objects[4]=None
        # elif ram_state[19]==0 and ram_state[29]
        else:
            objects[2]=None; objects[3]=None; objects[4]=None

    # Adding Rope
    # When does Rope come in? Disable for all other scenarios 
    rope_visible=False
    rope_list=[2,3,6,10,11,12,14,17]
    try:
        index=rope_list.index(ram_state[20])
        rope_visible=True
    except:
        pass
    if ram_state[19]==2 and ram_state[20]==4:
        rope_visible=True
    # import ipdb; ipdb.set_trace()
    if rope_visible:
        r=Rope()
        y=116-ram_state[18]
        # Quadratic estimates
        x_1=int(76.5-np.sqrt((y-49)*(112-y)))
        x_2=int(76.5+np.sqrt((y-49)*(112-y)))
        # Estimates from directly substituting vision found values
        x_right=[109,107,105,104,99,99,99,97,95,93,91]
        x_left=[47,49,51,52,54,55,60,60,61,63,65]
        x_2=x_right[20-ram_state[18]]
        x_1=x_left[20-ram_state[18]]
        global ram_18
        global prev_x
        increment=2
        if ram_state[18]!=ram_18:
            prev_x=x_1 if ram_state[93]==16 else x_2
        else:
            if ram_state[18]==10:
                if ram_state[94]>=96 and ram_state[94]<=168:
                    increment=4
                else:
                    increment=-4
                prev_x=prev_x+increment      
        ram_18=ram_state[18]
        r.xy=prev_x,y
        objects[10]=r




    if hud:
        objects.extend([None]*10)
        # PlayerScores related to ram_state 86 and 87
        p1=PlayerScore()
        p1.xy=62,9
        objects[21]=p1
        p2=PlayerScore()
        p2.xy=54,9
        objects[22]=p2
        p3=PlayerScore()
        p3.xy=46,9
        objects[23]=p3
        p4=PlayerScore()
        p4.xy=39,9
        objects[24]=p4
        if ram_state[85]!=0:
            p5=PlayerScore()
            p5.xy=31,9
            objects[31]=p5
        else:
            objects[31]=None
            if ram_state[86]<=9:
                objects[24]=None
            if ram_state[86]==0:
                objects[24]=None
                objects[23]=None
        # LifeCounts
        if ram_state[0]==160:
            l1=LifeCount()
            l1.xy=23,22
            l2=LifeCount()
            l2.xy=21,22
            objects[25]=l1; objects[26]=l2
        elif ram_state[0]==128:
            l1=LifeCount()
            l1.xy=21,22
            objects[25]=l1; objects[26]=None
        else:
            objects[25]=None; objects[26]=None

        # Timer
        t1=Timer(); t2=Timer(); t3=Timer(); t4=Timer()
        t1.xy=62,22
        t2.xy=54,22
        t3.xy=38,22
        t4.xy=31,22
        objects[27]=t1; objects[28]=t2; objects[29]=t3; objects[30]=t4
        if ram_state[88]<=9:
            objects[30]=None #making the first digit vanish if minute is single digit 
        # import ipdb; ipdb.set_trace()
        



def _detect_objects_pitfall_raw(info, ram_state):
    """
    returns unprocessed list with
    ball_x, ball_y, enemy_y, player_y
    """
    info["objects_list"] = ram_state[32:36]


