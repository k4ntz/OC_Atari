from .game_objects import GameObject
import sys 
MAX_NB_OBJECTS = {"Player": 1, "Gopher":1, "Carrot":3,"Empty_block":38}
MAX_NB_OBJECTS_HUD = {"Bird":1, "Score":5}

full_list=[(140,175),(12,175),(27,175),(45,175),(108,175),(124,175),
           (140,168),(12,168),(27,168),(45,168),(108,168),(124,168),
           (140,161),(12,161),(27,161),(45,161),(108,161),(124,161)]

for i in [2,140,36,12,27,45,108,124,150]:
    full_list.append((i,183))
for i in [22,117,134]: #narrower blocks
    full_list.append((i,183))
for i in range(55,108,9):
    full_list.append((i, 183))


# (150, 192),(140, 192), (27,183)
# (12,167),(12,173),(28, 161)
global block_list
block_list=[]
global ram_70
ram_70=0
global life 
life=3
class Player(GameObject):
    def __init__(self):
        super().__init__()
        self._xy = 0, 0
        self.wh = (11,50)
        self.rgb = 101, 111, 228
        self.hud = False

class Gopher(GameObject):
    def __init__(self):
        super().__init__()
        self._xy = 0, 0
        self.wh = (14,10)
        self.rgb = 72,44,0
        self.hud = False

class Carrot(GameObject):
    def __init__(self):
        super().__init__()
        self._xy = 0, 0
        self.wh = (8,27)
        self.rgb = 162,98,33
        self.hud = False

class Bird(GameObject):
    def __init__(self):
        super().__init__()
        self._xy = 0, 0
        self.wh = (15,18)
        self.rgb = 45,50,184 
        self.hud = False

class Empty_block(GameObject):
    def __init__(self):
        super().__init__()
        self._xy = 0, 0
        self.wh = (8,12)
        self.rgb = 223,183,85 
        self.hud = False

class Score(GameObject):
    def __init__(self):
        super().__init__()
        self._xy = 0, 0
        self.wh = (5,9)
        self.rgb = 195,144,65 
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


def _init_objects_gopher_ram(hud=False):
    """
    (Re)Initialize the objects
    """
    objects = [Player(),Gopher(),Carrot(),Carrot(),Carrot()]
    objects.extend([Empty_block()]*38) # Maximum number of expeced blocks
    if hud:
        objects.extend([Bird(),Score(),Score(),Score(),Score()])
    return objects


def _detect_objects_gopher_revised(objects, ram_state, hud=False):
    """
    For all 3 objects:
    (x, y, w, h, r, g, b)
    """
    # Detecting player 
    player = objects[0]
    player.xy = ram_state[31]-10, 96
    # Detecting gopher
    gopher=objects[1]
    if ram_state[85]<=5:
        gopher.xy=ram_state[41]-2,184
        gopher.wh=(14,10)
    elif ram_state[85]==35:
        gopher.xy=ram_state[41]-2,149
        gopher.wh=(14,10)
    else:
        gopher.xy=ram_state[41]-3,184-(ram_state[85])
        gopher.wh=(7,23)
    
    # Detecting carrots
    # Carrot at (92, 151), (8, 27), Carrot at (76, 151), (8, 27), Carrot at (60, 151), (8, 27)
    carrot1,carrot2,carrot3=Carrot(),Carrot(),Carrot()
    carrot1.xy=92,151; carrot2.xy=76,151; carrot3.xy=60,151
    temp_life=3
    if ram_state[36]==0 and ram_state[37]==0 and ram_state[38]==3:
        objects[2:5]=carrot1,carrot2,carrot3
        temp_life=3
    elif ram_state[36]==0 and ram_state[37]==0 and ram_state[38]==1:
        objects[2]=carrot2; objects[3]=carrot3; objects[4]=None
        temp_life=2
    elif ram_state[36]==0 and ram_state[37]==0 and ram_state[38]==0:
        objects[2]=carrot3; objects[3]=None; objects[4]=None
        temp_life=2
    elif ram_state[36]==128 and ram_state[37]==32 and ram_state[38]==1:
        objects[2]=carrot2; objects[3]=carrot1; objects[4]=None
        temp_life=2
    elif ram_state[36]==127 and ram_state[37]==16 and ram_state[38]==0:
        objects[2]=carrot1; objects[3]=None; objects[4]=None
        temp_life=1
    elif ram_state[36]==128 and ram_state[37]==32 and ram_state[38]==0:
        objects[2]=carrot2; objects[3]=None; objects[4]=None
        temp_life=1
    
    # Making all the blocks empty
    objects[5:43]=[None]*38
    # Adding empty_blocks intuition
    # max number of blocks as obtained from vision
    # Maintain three lists: possible, gopher, player
    # Add gopher blocks using MSE
    # Remove player blocks 
    global block_list
    # Adding blocks 
    gopher_x=ram_state[41]-3
    gopher_y=184-(ram_state[85])
    for block in full_list:
        if (abs(block[0]-gopher_x)<=10 and abs(block[1]-gopher_y)<=7) or (abs(block[0]-gopher_x)<=10 and ram_state[85]>=10) or (block[1]<183 and abs(block[0]-gopher_x)<=10 and ram_state[85]!=135 and abs(block[1]-gopher_y)<=10) :
            # If the block is not in existing list add it
            flag=True
            for block2 in block_list:
                if block[0]==block2[0] and block[1]==block2[1]:
                    flag=False
            if flag:
                block_list.append(block)     
               
    
    
    # Removing blocks
    # Get position of player 
    # extract objects below it
    # When the player presses handle remove the one with lowest y only if there are blocks other than the lowest position
    player_mid=ram_state[31]-10+5
    remove_block=[]
    for block in block_list:
        if abs(block[0]+4-player_mid)<=5:
            remove_block.append(block)
    global ram_70
    if ram_state[70]==255 and ram_70==0:
        flag2=False
        if len(remove_block)!=0:
            lowest_block=remove_block[0]
        for block in remove_block:
            if block[1]==161:
                flag2=True
            if block[1]>lowest_block[1]:
                lowest_block=block
        if flag2:
            block_list.remove(lowest_block)
    ram_70=ram_state[70]
    global life
    if life!=temp_life:
        block_list=[]
        life=temp_life
    # import ipdb; ipdb.set_trace()
    count=0
    # processing differenet sizes
    for block in block_list:
        b=Empty_block()
        b.xy=block
        if block[1]<183:
            b.wh=(8,6)
        if block[0] in [22,117,134]:
            b.wh=(4,12)
        objects[5+count]=b
        count+=1
    # import ipdb; ipdb.set_trace()
    if hud:
        # Score hundreds and thousands depend on ram_state[49] and score ones and tens depend on ram_state[50]
        bound1,bound2,bound3,bound4=Score(),Score(),Score(),Score()
        # Score at (98, 10), (5, 9), Score at (90, 10), (5, 9), Score at (82, 10), (5, 9), Score at (75, 10), (3, 9)]
        bound1.xy=75,10
        bound2.xy=82,10
        bound3.xy=90,10
        bound4.xy=98,10
        if ram_state[49]==0 and ram_state[50]<=9:
            # Right most bounding box only
            objects[44]=bound4
            objects[45]=None; objects[46]=None; objects[47]=None
        elif ram_state[49]==0 and ram_state[50]>9:
            # two bounding boxes
            objects[44]=bound4
            objects[45]=bound3
            objects[46]=None; objects[47]=None
        elif ram_state[49]<=9:
            # 3 bounding boxes
            objects[44:47]=bound4,bound3,bound2
            objects[47]=None
        elif ram_state[49]>9:
            # 4 bounding boxes
            objects[44:48]=bound4,bound3,bound2,bound1

        if ram_state[28]<147:
            b=Bird()
            b.xy=ram_state[28]-12,30
            objects[43]=b
        else:
            objects[43]=None







