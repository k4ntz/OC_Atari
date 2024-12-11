from .game_objects import GameObject, NoObject
from .utils import match_objects
import sys 

"""
RAM extraction for the game Frostbite.
"""

MAX_NB_OBJECTS = {"Player": 1, "Bear": 1, "House": 1, "Door": 1, "Bird": 8, "Crab": 8, "Clam": 8, "GreenFish": 8, "FloatingBlock": 24}
MAX_NB_OBJECTS_HUD = {"Player": 1, "Bear": 1, "House": 1, "Door": 1, "Bird": 8, "Crab": 8, "Clam": 8, "GreenFish": 8, "FloatingBlock": 24, "LifeCount": 1, "Degree": 1, "PlayerScore": 1}

class Player(GameObject):
    """
    The player figure: Frostbite Bailey.
    """
    
    def __init__(self):
        super().__init__()
        self._xy = 0, 0
        self.wh = (8, 18)
        self.rgb = 198, 108, 58
        self.hud = False


class Bear(GameObject):
    """
    The dangerous grizzly polar bears on the shore (level 4).
    """
    
    def __init__(self):
        super().__init__()
        self.rgb = 111, 111, 111
        self.hud = False
        self.wh = (14, 16)
        self._xy = 0, 0


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


class Door(GameObject):
    """
    The finished igloo.
    """
    
    def __init__(self):
        super().__init__()
        self._xy = 123, 47
        self.rgb = 0, 0, 0
        self.hud = False
        self.wh = 8, 8

class FloatingBlock(GameObject):
    """
    The white, untouched ice floes, turning blue once jumped over.
    """
    
    def __init__(self):
        super().__init__()
        self.rgb = 214, 214, 214
        self.hud = False
        self.wh = 24, 7
        self._xy = 0, 0

# class BluePlate(GameObject):
#     """
#     The ice floes that have turned blue by jumping on them.
#     """
    
#     def __init__(self):
#         super().__init__()
#         self.rgb = 84, 138, 210
#         self.hud = False
#         self.wh = (24, 7)
#         self._xy = 0, 0

class Bird(GameObject):
    """
    The wild snowgeese.
    """
    
    def __init__(self):
        super().__init__()
        self.rgb = 132, 144, 252
        self.hud = False
        self.wh = (8, 7)
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


class LifeCount(GameObject):
    """
    The indicator for the player's lives.
    """
    
    def __init__(self):
        super().__init__()
        self.rgb = 132, 144, 252
        self.hud = True
        self.wh = (8, 18)
        self._xy = 0, 0

class Degree(GameObject):
    """
    The temperature display.
    """
    
    def __init__(self):
        super().__init__()
        self.rgb = 132, 144, 252
        self.hud = True
        self.wh = (8, 18)
        self._xy = 0, 0


class PlayerScore(GameObject):
    """
    The player's score display.
    """
    
    def __init__(self):
        super().__init__()
        self.rgb = 132, 144, 252
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
    objects.extend([NoObject()])
    objects.extend([NoObject(), NoObject()]) #House/Door # None was frostbite before
    objects.extend([NoObject() for _ in range(24)]) #for bird, clams, crabs and greenfishes
    objects.extend([NoObject() for _ in range(24)]) #for the plates
    # if hud:
    #     objects.extend([LifeCount(), Degree(), PlayerScore()])
    return objects

def _detect_objects_ram(objects, ram_state, hud=False):
    """
    For all 3 objects:
    (x, y, w, h, r, g, b)
    """
    # 106 ram_state is somewhat controlling the y of the player when it's dying by sinking
    player = objects[0]
    if ram_state[106] == 26:
        if player:
            objects[0] = NoObject()
    else:
        if not player:
            player = Player()
            objects[0] = player
    player.xy =  ram_state[102], ram_state[100]+29
    if 0 < ram_state[107] < 18:
        sink = ram_state[107]
        player.y += sink
        player.h = 18 - sink
    elif 18 <= ram_state[107]: # sunk
        objects[0] = NoObject()

    # Bear
    if ram_state[104] == 140:
        if objects[1]:
            objects[1] = NoObject()
    else:
        if not objects[1]:
            bear = Bear()
            objects[1] = bear
        else:
            bear = objects[1]
        bear.xy = ram_state[104]+3, 58
        objects[1] = bear

    # House 
    position_list = [(112, 51), (112, 51), (112, 51), (112, 51), (112, 47), (112, 47), (112, 47), (112, 47), (112, 42), (112, 42), (112, 42), (112, 42), (112, 39), (112, 39), (112, 35), (112, 35)]
    size_list = [(8, 4), (16, 4), (24, 4), (32, 4), (32, 8), (32, 8), (32, 8), (32, 8), (32, 13), (32, 13), (32, 13), (32, 13), (32, 16), (32, 16), (32, 20), (32, 20)]
    if ram_state[77] == 255:
        if objects[2]:
            objects[2] = NoObject()
    else:
        if not objects[2]:
            house = House()
            objects[2] = house
        else:
            house = objects[2]
        house.xy = position_list[ram_state[77]]
        house.wh = size_list[ram_state[77]]

    # Door
    if ram_state[77] == 15:
        if not objects[3]:
            door = Door()
            objects[3] = door
        else:
            door = objects[3]
    elif objects[3]:
            objects[3] = NoObject()

    # # Birds
    # bird1, bird2, bird3, bird4 = objects[4:8]
    for i in range(4):
        if 0 < ram_state[84+i] < 160 or ram_state[88+i]:
            type = ram_state[35+i]
            if type in [18, 26]:
                Otype = Bird
            elif 33 < type < 39 or 49 < type < 55:
                Otype = Crab
            elif 65 < type < 71 or 93 < type < 99:
                Otype = Clam
            elif 108 < type < 114 or 123 < type < 129:
                Otype = GreenFish
            else:
                print(type)
                import ipdb; ipdb.set_trace()
            if isinstance(objects[4+i], Otype):
                obj = objects[4+i]
            else:
                obj = Otype()
                objects[4+i] = obj
            obj.xy = ram_state[84+i], 160 - 26 * i
            if ram_state[88+i]: # 2 objects
                if isinstance(objects[8+i], Otype):
                    obj2 = objects[8+i]
                else:
                    obj2 = Otype()
                    objects[8+i] = obj2
                obj2.xy = ram_state[84+i] + 32, 160 - 26 * i
            else:
                objects[8+i] = NoObject()
        else:
            objects[4+i] = NoObject()
    
    # # Adding the Plates
    # for i in range(4):

    # num_plates = 3 if ram_state[30] == 8 else 6
    # start_loc = 9 if ram_state[30] == 8 else 13
    # plate_diff = 32 if ram_state[30] == 8 else 16
    # size_plates = (24, 7) if ram_state[30] == 8 else (16, 7)
    # ram_list = [31, 32, 33, 34]
    # pos_list = [174, 148, 122, 96]
    # which_plate = [43, 44, 45, 46]
    # for i in range(num_plates*4):
    #     t = whichPlate(ram_state[which_plate[int(i/num_plates)]])
    #     temp = objects[6+i]
    #     if type(temp) != t:
    #         temp = t()
    #     temp.xy = correction(ram_state[ram_list[int(i/num_plates)]]+int(i%num_plates)*plate_diff-start_loc), pos_list[int(i/num_plates)]
    #     temp.wh = size_plates
    #     objects[6+i] = temp
    

    # if hud:
    #     # LifeCount
    #     if ram_state[76] != 0:
    #         l = objects[45]
    #         if type(l) != LifeCount:
    #             l = LifeCount()
    #         l.xy = 63, 22
    #         l.wh = (6, 10)
    #         objects[45] = l
    #     else:
    #         objects[45] = NoObject()

    #     # Time or degrees
    #     if ram_state[101] <= 9:
    #         d1 = objects[47]
    #         if type(d1) != Degree:
    #             d1 = Degree()
    #         d1 = Degree()
    #         d1.xy = 31, 22
    #         d1.wh = (6, 8)
    #         objects[46] = NoObject()
    #         objects[47] = d1
    #     else:
    #         d1 = objects[47]
    #         d2 = objects[46]
    #         if type(d1) != Degree:
    #             d1 = Degree()
    #         if type(d2) != Degree:
    #             d2 = Degree()
    #         d1.xy = 31, 22
    #         d1.wh = (6, 8)
    #         d2.xy = 23, 22
    #         d2.wh = (6, 8)
    #         objects[46] = d2
    #         objects[47] = d1
        
    #     # Player Score
    #     if ram_state[73] ==0 and ram_state[74] == 0:
    #         p = objects[51]
    #         if type(p) != PlayerScore:
    #             p = PlayerScore()
    #         p.xy = 63, 10
    #         p.wh = (6, 8)
    #         objects[51] = p

    #         objects[50] = NoObject() ; objects[49] = NoObject() ; objects[48] = NoObject()

    #     elif ram_state[73] == 0 and ram_state[74] != 0:
    #         p1 = objects[51]
    #         if type(p1) != PlayerScore:
    #             p1 = PlayerScore()
            
    #         p2 = objects[50]
    #         if type(p2) != PlayerScore:
    #             p2 = PlayerScore()

    #         p1.xy = 63, 10
    #         p1.wh = (6, 8)
    #         objects[51] = p1

    #         p2.xy = 55, 10
    #         p2.wh = (6, 8)
    #         objects[50] = p2

    #         objects[49] = NoObject(); objects[48] = NoObject()
    #     elif ram_state[72] == 0 and ram_state[73] != 0:
    #         p1 = objects[51]
    #         if type(p1) != PlayerScore:
    #             p1 = PlayerScore()
            
    #         p2 = objects[50]
    #         if type(p2) != PlayerScore:
    #             p2 = PlayerScore()
            
    #         p3 = objects[49]
    #         if type(p3) != PlayerScore:
    #             p3 = PlayerScore()

    #         p1.xy = 63, 10
    #         p1.wh = (6, 8)
    #         objects[51] = p1
            
    #         p2.xy = 55, 10
    #         p2.wh = (6, 8)
    #         objects[50] = p2
            
    #         p3.xy = 48, 10
    #         p3.wh = (6, 8)
    #         objects[49] = p3

    #         objects[48] = NoObject()


def whichPlate(pos):
    # Make decision whether to return Whiteplate or BluepLate
    if pos == 12:
        return WhitePlate
    else:
        return BluePlate

def correction(pos):
    return pos%160

def WhatObject(pos):
    if pos==143:
        return Bird
    elif pos==56:
        return Crab
    elif pos==202:
        return GreenFish
    elif pos==26:
        return Clam

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
