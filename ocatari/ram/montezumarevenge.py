from .game_objects import GameObject
from ._helper_methods import _convert_number, get_iou
import sys

"""
RAM extraction for the game Montezuma's Revenge.
"""

MAX_NB_OBJECTS =  {'Player': 1, 'Skull': 1, 'Spider': 1, 'Snake': 2, 'Key': 1, 'Amulet': 1, 'Torch': 1, 'Sword': 1,
                      'Barrier': 2, 'Beam': 8, 'Rope': 1, 'Ruby': 3}
MAX_NB_OBJECTS_HUD = {'Player': 1, 'Skull': 2, 'Spider': 1, 'Snake': 2, 'Key': 1, 'Amulet': 1, 'Torch': 1, 'Sword': 1,
                      'Barrier': 2, 'Beam': 8, 'Rope': 1, 'Ruby': 3, 'Key_HUD': 4, 'Amulet_HUD': 1, 'Torch_HUD': 1, 'Sword_HUD': 2,
                      'Score': 6, 'Life': 5}
obj_tracker = {}

class Player(GameObject):
    """
    The player figure: Panama Joe.
    """
    
    def __init__(self):
        super(Player, self).__init__()
        self._xy = 0, 0
        self.wh = 8, 20
        self.rgb = 228, 111, 111
        self.hud = False


class Skull(GameObject):
    """
    The bouncing or rolling skulls.
    """
    
    def __init__(self, *args, **kwargs):
        super(Skull, self).__init__()
        super().__init__(*args, **kwargs)
        self._xy = 79, 57
        self.wh = 7, 13
        self.rgb = 236, 236, 236
        self.hud = False


class Spider(GameObject):
    """
    The moving spiders.
    """
    
    def __init__(self, *args, **kwargs):
        super(Spider, self).__init__()
        super().__init__(*args, **kwargs)
        self._xy = 79, 57
        self.wh = 8, 11
        self.rgb = 92, 186, 92
        self.hud = False


class Snake(GameObject):
    """
    The stationary snakes.
    """
    
    def __init__(self, *args, **kwargs):
        super(Snake, self).__init__()
        super().__init__(*args, **kwargs)
        self._xy = 50, 80
        self.wh = 7, 13
        self.rgb = 192, 192, 192
        self.hud = False


class Key(GameObject):
    """
    The collectable keys.
    """
    
    def __init__(self, *args, **kwargs):
        super(Key, self).__init__()
        super().__init__(*args, **kwargs)
        self._xy = 89, 166
        self.wh = 7, 15
        self.rgb = 232, 204, 99
        self.hud = False


class Amulet(GameObject):
    """
    The collectable amulets, which make enemies disappear temporally.
    """
    
    def __init__(self, *args, **kwargs):
        super(Amulet, self).__init__()
        super().__init__(*args, **kwargs)
        self._xy = 89, 166
        self.wh = 6, 15
        self.rgb = 232, 204, 99
        self.hud = False


class Torch(GameObject):
    """
    The collectable torches for illuminating the rooms of the current game level.
    """
    
    def __init__(self, *args, **kwargs):
        super(Torch, self).__init__()
        super().__init__(*args, **kwargs)
        self._xy = 89, 166
        self.wh = 6, 13
        self.rgb = 204, 216, 110
        self.hud = False


class Sword(GameObject):
    """
    The collectable swords, that can eliminate spiders or skulls upon contact.
    """
    
    def __init__(self, *args, **kwargs):
        super(Sword, self).__init__()
        super().__init__(*args, **kwargs)
        self._xy = 11, 54
        self.wh = 6, 15
        self.rgb = 214, 214, 214
        self.hud = False


class Ruby(GameObject):
    """
    The collectable jewels.
    """
    
    def __init__(self, *args, **kwargs):
        super(Ruby, self).__init__()
        super().__init__(*args, **kwargs)
        self._xy = 89, 166
        self.wh = 7, 12
        self.rgb = 213, 130, 74
        self.hud = False


class Barrier(GameObject):
    """
    The doors that can be unlocked with collectable keys. Unlocking removes the door.
    """
    
    def __init__(self, *args, **kwargs):
        super(Barrier, self).__init__()
        super().__init__(*args, **kwargs)
        self._xy = 20, 54
        self.wh = 4, 37
        self.rgb = 232, 204, 99
        self.hud = False


class Beam(GameObject):
    """
    The flashing laser gates.
    """
    
    def __init__(self, *args, **kwargs):
        super(Beam, self).__init__()
        super().__init__(*args, **kwargs)
        self._xy = 140, 53
        self.wh = 4, 40
        self.rgb = 101, 111, 228
        self.hud = False


class Rope(GameObject):
    """
    The climbing-ropes.
    """
    
    def __init__(self, *args, **kwargs):
        super(Rope, self).__init__()
        super().__init__(*args, **kwargs)
        self._xy = 112, 96
        self.wh = 1, 39
        self.rgb = 232, 204, 99
        self.hud = False


class Score(GameObject):
    """
    The player's score display (HUD).
    """
    
    def __init__(self, *args, **kwargs):
        super(Score, self).__init__()
        self._xy = 97, 6
        self.wh = 5, 8
        self.rgb = 236, 236, 236
        self.hud = True


class Life(GameObject):
    """
    The player's remaining additional lives (displayed as hats) (HUD).
    """
    
    def __init__(self, *args, **kwargs):
        super(Life, self).__init__()
        self._xy = 88, 15
        self.wh = 7, 5
        self.rgb = 210, 182, 86
        self.hud = True


class Key_HUD(GameObject):
    """
    Keys in the inventory display (HUD).
    """
    
    def __init__(self, *args, **kwargs):
        super(Key_HUD, self).__init__()
        super().__init__(*args, **kwargs)
        self._xy = 56, 28
        self.wh = 7, 15
        self.rgb = 232, 204, 99
        self.hud = True
        
class Amulet_HUD(GameObject):
    """
    Amulets in the inventory display (HUD).
    """
    
    def __init__(self, *args, **kwargs):
        super(Amulet_HUD, self).__init__()
        super().__init__(*args, **kwargs)
        self._xy = 56, 28
        self.wh = 6, 15
        self.rgb = 232, 204, 99
        self.hud = True


class Torch_HUD(GameObject):
    """
    Torches in the inventory display (HUD).
    """
    
    def __init__(self, *args, **kwargs):
        super(Torch_HUD, self).__init__()
        super().__init__(*args, **kwargs)
        self._xy = 56, 28
        self.wh = 6, 13
        self.rgb = 232, 204, 99
        self.hud = True


class Sword_HUD(GameObject):
    """
    Swords in the inventory display (HUD).
    """
    
    def __init__(self, *args, **kwargs):
        super(Sword_HUD, self).__init__()
        super().__init__(*args, **kwargs)
        self._xy = 56, 28
        self.wh = 6, 15
        self.rgb = 232, 204, 99
        self.hud = True


class Platform(GameObject):
    """
    Permanent platforms.
    """
    
    def __init__(self, x=0, y=0, w=8, h=4, *args, **kwargs):
        super(Platform, self).__init__(*args, **kwargs)
        self._xy = x, y
        self._prev_xy = x, y
        self.wh = w, h
        self.rgb = 66, 158, 130
        self.hud = False


class Ladder(GameObject):
    """
    The ladders.
    """
    
    def __init__(self, x=0, y=0, w=8, h=4, *args, **kwargs):
        super(Ladder, self).__init__(*args, **kwargs)
        self._xy = x, y
        self._prev_xy = x, y
        self.wh = w, h
        self.rgb = 66, 158, 130
        self.hud = False


class Conveyer_Belt(GameObject):
    """
    The conveyor belts.
    """
    
    def __init__(self, x=0, y=0, w=8, h=4, *args, **kwargs):
        super(Conveyer_Belt, self).__init__(*args, **kwargs)
        self._xy = x, y
        self._prev_xy = x, y
        self.wh = w, h
        self.rgb = 66, 158, 130
        self.hud = False


class Wall(GameObject):
    """
    A class representing walls.
    """
    
    def __init__(self, x=0, y=0, w=8, h=4, *args, **kwargs):
        super(Wall, self).__init__(*args, **kwargs)
        self._xy = x, y
        self._prev_xy = x, y
        self.wh = w, h
        self.rgb = 66, 158, 130
        self.hud = False


class Disappearing_Platform(GameObject):
    """
    Dis- and reappearing parts of the floor.
    """
    
    def __init__(self, x=0, y=0, w=8, h=4, *args, **kwargs):
        super(Disappearing_Platform, self).__init__(*args, **kwargs)
        self._xy = x, y
        self._prev_xy = x, y
        self.wh = w, h
        self.rgb = 66, 158, 130
        self.hud = False


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

def _init_objects_montezumarevenge_ram(hud=True):
    """
    (Re)Initialize the objects
    """

    objects = [Player()]

    global collected
    global rubys_collected
    global enemys_in_room
    global last_room
    global last_inventory
    global last_level
    global hit
    collected = [0, 0, 0, 0, 0, 0, 0]
    rubys_collected = [0, 0, 0, 0, 0, 0, 0]
    enemys_in_room = [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
    last_room = 0
    last_inventory = 0
    last_level = 0
    hit = False

    objects.extend([None] * 35)
    if hud:
        objects.extend([None] * 19)
    return objects


# levels: ram_state[36], total of 3 levels: 0,1 and 2
def _detect_objects_montezumarevenge_ram(objects, ram_state, hud=True):
    player = objects[0]
    item = objects[1]
    ruby, ruby2, ruby3 = objects[2], objects[3], objects[4]
    enemy, enemy2 = objects[5], objects[6]
    barrier, barrier2 = objects[7], objects[8]
    beam0, beam1, beam2, beam3, beam4, beam5, beam6, beam7 = objects[9], objects[10], objects[11], objects[12], objects[13], objects[14], objects[15], objects[16]
    rope = objects[17]
    enviroment_objects = objects[18:36]

    global collected
    global rubys_collected
    global enemys_in_room
    global last_room
    global last_inventory
    global last_level
    global hit
    room = ram_state[3]
    level = ram_state[57]
    # score = _convert_number(ram_state[19]) * 10000 + _convert_number(ram_state[20]) * 100 + _convert_number(ram_state[21])

    if level != last_level:
        last_level = level
        collected = [0, 0, 0, 0, 0, 0, 0]
        rubys_collected = [0, 0, 0, 0, 0, 0, 0]
        enemys_in_room = [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]

    if room != last_room:
        last_inventory = ram_state[65]
        last_room = room

    # player
    player = Player()
    player = objects[0]
    player.xy = ram_state[42] - 1, 255 - ram_state[43] + 53

    for i in range(35):
        objects[i+1] = None

    if room == 0:
        if level == 0:
            # ruby
            if ram_state[67]&16:
                ruby = Ruby()
                ruby.xy = ram_state[44] - 1, 56
                objects[2] = ruby
            else:
                objects[2] = None
        elif level == 1:
                # sword
            if ram_state[67]&16:
                item = Sword()
                item.xy = ram_state[44] - 1, 56
                objects[1] = item
            else:
                objects[1] = None
        elif level == 2:
            # skulls
            if ram_state[67]&16:
                enemy = Skull()
                enemy.xy = ram_state[44] - 1, 55 + (255 - ram_state[45])
                objects[4] = enemy
            else:
                objects[4] = None


        if ram_state[26] != 117:
            beam0 = Beam()
            objects[9] = beam0
            beam1 = Beam()
            beam1.xy = 120, 53
            objects[10] = beam1
            beam2 = Beam()
            beam2.xy = 112, 53
            objects[11] = beam2
            beam3 = Beam()
            beam3.xy = 44, 53
            objects[12] = beam3
            beam4 = Beam()
            beam4.xy = 36, 53
            objects[13] = beam4
            beam5 = Beam()
            beam5.xy = 16, 53
            objects[14] = beam5
        else:
            for i in range(5):
                objects[8+i] = None
        
        objects[18] = Platform(x=4, y=94, w=154, h=1)
        objects[19] = Ladder(x=72, y=94, w=16, h=102)


    elif room == 1:
        # skull
        if ram_state[67]&2:
            enemy = Skull()
            enemy.xy = ram_state[47] + 32, ram_state[46] - 74
            objects[4] = enemy
        else:
            objects[4] = None

        # key
        if ram_state[67]&1:
            item = Key()
            item.xy = ram_state[44] - 1, 98 + (255 - ram_state[45]) 
            objects[1] = item
        else:
            objects[1] = None

        
        # barrier
        if ram_state[26] != 117:
            barrier = Barrier()
            objects[6] = barrier
        else:
            objects[6] = None
        
        if ram_state[28] != 117:
            barrier2 = Barrier()
            _, y = barrier2.xy
            barrier2.xy = 136, y
            objects[7] = barrier2
        else:
            objects[7] = None
        
        rope = Rope()
        objects[17] = rope

        objects[18] = Platform(x=0, y=93, w=55, h=2)
        objects[19] = Platform(x=104, y=93, w=55, h=2)
        objects[20] = Platform(x=68, y=93, w=23, h=2)
        objects[21] = Ladder(x=72, y=93, w=16, h=42)
        objects[22] = Platform(x=76, y=136, w=8, h=5)
        objects[23] = Conveyer_Belt(x=60, y=136, w=15, h=5)
        objects[24] = Conveyer_Belt(x=85, y=136, w=15, h=5)
        objects[25] = Ladder(x=16, y=136, w=16, h=45)
        objects[26] = Ladder(x=128, y=136, w=16, h=45)
        objects[27] = Platform(x=8, y=136, w=28, h=2)
        objects[28] = Platform(x=124, y=136, w=28, h=2)
        objects[29] = Platform(x=16, y=180, w=128, h=1)

    elif room == 2:
        if level == 0:
            # skulls
            if ram_state[68]&16 or ram_state[68]&32:
                enemy = Skull()
                enemy.xy = ram_state[44] - 1, 53 + (255 - ram_state[45])
                objects[4] = enemy
                if ram_state[84] > 0:
                    enemy2 = Skull()
                    enemy2.xy = ram_state[44] + 15, 53 + (255 - ram_state[45])
                    objects[5] = enemy2
                else:
                    objects[5] = None
            else:
                objects[4] = None
                objects[5] = None
        elif level == 1:
            # ruby
            if ram_state[68]&16:
                ruby = Ruby()
                ruby.xy = ram_state[44] - 1, 54
                objects[2] = ruby
            else:
                objects[2] = None
        elif level == 2:
            # snakes
            if ram_state[68]&16:
                enemy = Snake()
                enemy.xy = ram_state[44], 53 + (255 - ram_state[45])
                enemy2 = Snake()
                enemy2.xy = ram_state[44] + 16, 53 + (255 - ram_state[45])
                objects[4] = enemy
                objects[5] = enemy2
            else:
                objects[4] = None
                objects[5] = None

        objects[18] = Platform(x=4, y=93, w=154, h=1)
        objects[19] = Ladder(x=72, y=93, w=16, h=102)

    elif room == 3:
        if level == 0:
            # skulls
            if ram_state[68]&1 or ram_state[68]&2:
                enemy = Skull()
                enemy.xy = ram_state[44] - 1, 53 + (255 - ram_state[45]) 
                objects[4] = enemy
                if ram_state[84] > 0:
                    enemy2 = Skull()
                    enemy2.xy = ram_state[44] + 15, 53 + (255 - ram_state[45])
                    objects[5] = enemy2
                else:
                    objects[5] = None
            else:
                objects[4] = None
                objects[5] = None

        elif level == 1 or level == 2:
            if ram_state[68]&1 or ram_state[68]&2:
                ruby = Ruby()
                ruby.xy = ram_state[44] - 1, 53 + (255 - ram_state[45])
                objects[2] = ruby
                if ram_state[84] > 0:
                    ruby2 = Ruby()
                    ruby2.xy = ram_state[44] + 15, 53 + (255 - ram_state[45])
                    objects[3] = ruby2
                else:
                    objects[3] = None
            else:
                objects[2] = None
                objects[3] = None
        
        objects[18] = Platform(x=4, y=93, w=154, h=1)
        objects[19] = Ladder(x=72, y=93, w=16, h=102)
            
    elif room == 4:
        if level == 0:
            # spider
            if ram_state[69]&16:
                enemy = Spider()
                enemy.xy = ram_state[44] - 1, 53 + (255 - ram_state[45]) 
                objects[4] = enemy
            else:
                objects[4] = None
        elif level == 1:
            # snek
            if ram_state[69]&16:
                enemy = Snake()
                enemy.xy = ram_state[44] , 53 + (255 - ram_state[45]) 
                objects[4] = enemy
            else:
                objects[4] = None
        elif level == 2:
            # snakes
            if ram_state[69]&16:
                enemy = Snake()
                enemy.xy = ram_state[44], 53 + (255 - ram_state[45])
                objects[4] = enemy
            else:
                objects[4] = None
        
        objects[18] = Platform(x=4, y=93, w=154, h=1)
        objects[19] = Ladder(x=72, y=52, w=16, h=39)
        objects[20] = Ladder(x=72, y=93, w=16, h=102)

    elif room == 5:
        if ram_state[69]&1:
            # torch
            item = Torch()
            item.xy = ram_state[44] - 1, 53 + (255 - ram_state[45]) 
            objects[1] = item
        else:
            objects[1] = None

        # skull
        if ram_state[69]&2:
            enemy = Skull()
            enemy.xy = ram_state[47] + 33, 103 + (255 - ram_state[46]) 
            objects[4] = enemy
        else:
            objects[4] = None
        
        # barrier
        if ram_state[26] != 117:
            barrier = Barrier()
            barrier.xy = 56, 135
            barrier.rgb = 66, 158, 130
            objects[6] = barrier
        else:
            objects[6] = None
        
        if ram_state[28] != 117:
            barrier2 = Barrier()
            barrier2.xy = 100, 135
            barrier2.rgb = 66, 158, 130
            objects[7] = barrier2
        else:
            objects[7] = None

        #rope
        rope = Rope()
        rope.rgb = 236, 236, 236
        rope.xy = 41, 97
        rope.wh = 1, 24
        objects[17] = rope
        
        objects[18] = Platform(x=0, y=93, w=48, h=2)
        objects[19] = Platform(x=112, y=93, w=48, h=2)
        objects[20] = Wall(x=32, y=53, w=4, h=40)
        objects[21] = Wall(x=124, y=53, w=4, h=40)
        objects[22] = Wall(x=125, y=95, w=2, h=51)
        objects[23] = Platform(x=48, y=130, w=64, h=3)
        objects[24] = Platform(x=4, y=171, w=154, h=1)
        objects[25] = Ladder(x=72, y=171, w=16, h=26)
        objects[26] = Platform(x=76, y=93, w=8, h=5)
        objects[27] = Conveyer_Belt(x=60, y=93, w=15, h=5)
        objects[28] = Conveyer_Belt(x=85, y=93, w=15, h=5)

    elif room == 6:
        if level == 0:
            # sword
            if ram_state[70]&16:
                item = Sword()
                item.xy = ram_state[44] - 1, 53 + (255 - ram_state[45]) 
                objects[1] = item
            else:
                objects[1] = None
        elif level == 1:
            # skull
            if ram_state[70]&16:
                enemy = Skull()
                enemy.xy = ram_state[44] - 1, 53 + (255 - ram_state[45]) 
                objects[4] = enemy
        elif level == 2:
            # spider
            if ram_state[70]&16:
                enemy = Spider()
                enemy.xy = ram_state[44] - 1, 53 + (255 - ram_state[45]) 
                objects[4] = enemy
        objects[18] = Platform(x=0, y=93, w=160, h=1)
        objects[19] = Ladder(x=72, y=53, w=16, h=38)

    elif room == 7:
        if level == 0 or level == 2:
            # key
            if ram_state[70]&1:
                item = Key()
                item.xy = ram_state[44] - 1, 54 + (255 - ram_state[45]) 
                objects[1] = item
            else:
                objects[1] = None
        elif level == 1:
            if ram_state[70]&1:
                ruby = Ruby()
                ruby.xy = ram_state[44] - 1, 54 + (255 - ram_state[45])
                objects[2] = ruby
            else:
                objects[2] = None

        #beam
        if ram_state[26] != 117:
            beam0 = Beam()
            objects[9] = beam0
            beam1 = Beam()
            beam1.xy = 120, 53
            objects[10] = beam1
            beam2 = Beam()
            beam2.xy = 112, 53
            objects[11] = beam2
            beam3 = Beam()
            beam3.xy = 44, 53
            objects[12] = beam3
            beam4 = Beam()
            beam4.xy = 36, 53
            objects[13] = beam4
            beam5 = Beam()
            beam5.xy = 16, 53
            objects[14] = beam5
        else:
            for i in range(5):
                objects[8+i] = None

        objects[18] = Platform(x=4, y=94, w=154, h=1)
        objects[19] = Ladder(x=72, y=94, w=16, h=102)
    
    elif room == 8:
        if level == 0:
            # key
            if ram_state[71]&16:
                item = Key()
                item.xy = ram_state[44] - 1, 53 + (255 - ram_state[45]) 
                objects[1] = item
            else:
                objects[1] = None
        elif level == 1:
            if ram_state[71]&16:
                ruby = Ruby()
                ruby.xy = ram_state[44] - 1, 53 + (255 - ram_state[45])
                objects[2] = ruby
            else:
                objects[2] = None
        if level == 2:
            # key
            if ram_state[71]&16:
                item = Key()
                item.xy = ram_state[44] - 1, 53 + (255 - ram_state[45]) 
                objects[1] = item
            else:
                objects[1] = None

        #rope
        rope = Rope()
        rope.xy = 80, 96
        rope.wh = 1, 51
        objects[17] = rope

        if ram_state[34] != 144:
            objects[18] = Disappearing_Platform(4, 103, 12, 4)
            objects[19] = Disappearing_Platform(4, 113, 12, 4)
            objects[20] = Disappearing_Platform(4, 123, 12, 4)
            objects[21] = Disappearing_Platform(4, 133, 12, 4)

            objects[22] = Platform(4, 143, 12, 4)

            objects[23] = Disappearing_Platform(4, 153, 12, 4)
            objects[24] = Disappearing_Platform(4, 163, 12, 4)
            
            objects[25] = Disappearing_Platform(144, 103, 12, 4)
            objects[26] = Disappearing_Platform(144, 113, 12, 4)
            objects[27] = Disappearing_Platform(144, 123, 12, 4)
            objects[28] = Disappearing_Platform(144, 133, 12, 4)

            objects[29] = Platform(144, 143, 12, 4)

            objects[30] = Disappearing_Platform(144, 153, 12, 4)
            objects[31] = Disappearing_Platform(144, 163, 12, 4)

        objects[32] = Platform(4, 93, 43, 3)
        objects[33] = Platform(76, 93, 8, 3)
        objects[34] = Platform(112, 93, 48, 3)
        objects[35] = Platform(4, 173, 152, 1)

    elif room == 9:
        if level == 0:
            # snakes
            if ram_state[71]&1 or ram_state[71]&4:
                enemy = Snake()
                enemy.xy = ram_state[44], 53 + (255 - ram_state[45])
                objects[4] = enemy
                if ram_state[84] > 0:
                    enemy2 = Snake()
                    enemy2.xy = ram_state[44] + 32, 53 + (255 - ram_state[45])
                    objects[5] = enemy2
                else:
                    objects[5] = None
            else:
                objects[4] = None
                objects[5] = None
        if level == 1 or level == 2:
            # spider
            if ram_state[71]&1:
                enemy = Spider()
                enemy.xy = ram_state[44] - 1, 53 + (255 - ram_state[45])
                objects[4] = enemy
            else:
                objects[4] = None

        objects[18] = Platform(x=0, y=93, w=158, h=1)
        objects[19] = Ladder(x=72, y=53, w=16, h=38)
        objects[20] = Wall(x=156, y=53, w=3, h=40)

    elif room == 10:
        if level == 0:
            # ruby
            if ram_state[72]&16:
                ruby = Ruby()
                ruby.xy = ram_state[44] - 1, 54
                objects[2] = ruby
            else:
                objects[2] = None
        elif level == 1:
            # key
            if ram_state[72]&16:
                item = Key()
                item.xy = ram_state[44] - 1, 54 
                objects[1] = item
            else:
                objects[1] = None
        elif level == 2:
            # sword
            if ram_state[72]&16:
                item = Sword()
                item.xy = ram_state[44] - 1, 54 
                objects[1] = item
            else:
                objects[1] = None


        objects[18] = Wall(x=0, y=53, w=3, h=40)
        objects[19] = Ladder(x=72, y=53, w=16, h=38)
        objects[20] = Platform(x=0, y=93, w=36, h=1)
        if ram_state[34] != 232:
            objects[21] = Disappearing_Platform(x=36, y=93, w=88, h=7)
        objects[22] = Platform(x=124, y=93, w=36, h=1)

    elif room == 11:
        if level == 0:
            # snakes
            if ram_state[72]&1 or ram_state[72]&8:
                enemy = Snake()
                enemy.xy = ram_state[44], 53 + (255 - ram_state[45])
                objects[4] = enemy
                if ram_state[84] > 0:
                    enemy2 = Snake()
                    enemy2.xy = ram_state[44] + 64, 53 + (255 - ram_state[45])
                    objects[5] = enemy2
                else:
                    objects[5] = None
            else:
                objects[4] = None
                objects[5] = None
        elif level == 1:
            # amulet
            if ram_state[72]&1:
                item = Amulet()
                item.xy = ram_state[44] - 1, 53 + (255 - ram_state[45])
                objects[1] = item
            else:
                objects[1] = None
        if level == 2:
            # skulls
            if ram_state[72]&1:
                enemy = Skull()
                enemy.xy = ram_state[44] - 1, 53 + (255 - ram_state[45])
                enemy2 = Skull()
                enemy2.xy = ram_state[44] - 97, 53 + (255 - ram_state[45])
                
                objects[4] = enemy
                objects[5] = enemy2
            else:
                objects[4] = None
                objects[5] = None

        objects[18] = Platform(x=0, y=93, w=160, h=1)
        objects[19] = Ladder(x=72, y=52, w=16, h=39)
        objects[20] = Ladder(x=72, y=93, w=16, h=102)

    
    elif room == 12:
        #beam
        if ram_state[26] != 117:
            beam0 = Beam()
            beam0.xy = 120, 53
            objects[9] = beam0
            beam1 = Beam()
            beam1.xy = 112, 53
            objects[10] = beam1
            beam2 = Beam()
            beam2.xy = 96, 53
            objects[11] = beam2
            beam3 = Beam()
            beam3.xy = 88, 53
            objects[12] = beam3
            beam4 = Beam()
            beam4.xy = 68, 53
            objects[13] = beam4
            beam5 = Beam()
            beam5.xy = 60, 53
            objects[14] = beam5
            beam6 = Beam()
            beam6.xy = 44, 53
            objects[15] = beam6
            beam7 = Beam()
            beam7.xy = 36, 53
            objects[16] = beam7
        else:
            for i in range(8):
                objects[8+i] = None
        objects[18] = Platform(x=0, y=94, w=160, h=1)

    elif room == 13:
        if level == 0:
            # spider
            if ram_state[73]&1:
                enemy = Spider()
                enemy.xy = ram_state[44] - 1, 53 + (255 - ram_state[45])
                objects[4] = enemy
            else:
                objects[4] = None
        elif level == 1:
            # snakes
            if ram_state[73]&1 or ram_state[73]&8:
                enemy = Snake()
                enemy.xy = ram_state[44], 53 + (255 - ram_state[45]) 
                objects[4] = enemy
                if ram_state[84] > 0:
                    enemy2 = Snake()
                    enemy2.xy = ram_state[44] + 64, 53 + (255 - ram_state[45])
                    objects[5] = enemy2
                else:
                    objects[5] = None
            else:
                objects[4] = None
                objects[5] = None
        elif level == 2:
            # skull
            if ram_state[73]&1:
                enemy = Skull()
                enemy.xy = ram_state[44] - 1, 53 + (255 - ram_state[45])
                objects[4] = enemy
            else:
                objects[4] = None

        objects[18] = Platform(x=0, y=93, w=160, h=1)
        objects[19] = Ladder(x=72, y=52, w=16, h=39)
        objects[20] = Ladder(x=72, y=93, w=16, h=102)
    
    elif room == 14:
        # key
        if ram_state[74]&16:
            if level == 2:
                item = Amulet()
            else:
                item = Key()
            if level == 0 or level == 2:  
                item.xy = ram_state[44] - 1, 57 + (255 - ram_state[45])
            elif level == 1:
                item.xy = ram_state[44] - 1, 53 + (255 - ram_state[45])
            objects[1] = item
        else:
            objects[1] = None
        
        # rope
        rope = Rope()
        rope.xy = 71, 96
        rope.wh = 1, 48
        objects[17] = rope

        objects[18] = Platform(0, 93, 40, 3)
        objects[19] = Platform(68, 93, 24, 3)
        objects[20] = Platform(120, 93, 40, 3)
        objects[21] = Platform(16, 168, 128, 1)
        objects[22] = Ladder(72, 169, 16, 25)
    
    elif room == 15:
        # ruby
        ruby = Ruby()
        ruby.xy = ram_state[44] - 1, 54
        objects[2] = ruby
    
        objects[18] = Platform(x=0, y=94, w=160, h=1)
    
    elif room == 16:
        objects[18] = Platform(x=0, y=93, w=160, h=1)
        
    
    elif room == 17:
        # barrier
        if ram_state[26] != 117:
            barrier = Barrier()
            objects[6] = barrier
        else:
            objects[6] = None
        
        if ram_state[28] != 117:
            barrier2 = Barrier()
            _, y = barrier2.xy
            barrier2.xy = 136, y
            objects[7] = barrier2
        else:
            objects[7] = None

        objects[18] = Platform(x=0, y=94, w=160, h=1)
    
    elif room ==  18:
        # skull
        if ram_state[76]&32:
            enemy = Skull()
            enemy.xy = ram_state[47] - 1, ram_state[46] - 147
            objects[4] = enemy
        else:
            objects[4] = None

        objects[18] = Platform(x=0, y=94, w=36, h=1)
        if ram_state[34] != 232:
            objects[19] = Disappearing_Platform(x=36, y=94, w=88, h=7)
        objects[20] = Platform(x=124, y=94, w=36, h=1)
    
    elif room == 19:
        if level == 0:
            # amulet
            if ram_state[76]&1:
                item = Amulet()
                item.xy = ram_state[44] - 1, 53 + (255 - ram_state[45]) 
                objects[1] = item
            else:
                objects[1] = None
        if level == 1:
            # skull
            if ram_state[76]&1:
                enemy = Skull()
                enemy.xy = ram_state[44] - 1, 53 + (255 - ram_state[45])
                objects[4] = enemy
            else:
                objects[4] = None

        if level == 2:
            # spider
            if ram_state[76]&1:
                enemy = Spider()
                enemy.xy = ram_state[44] - 1, 53 + (255 - ram_state[45])
                objects[4] = enemy
            else:
                objects[4] = None

        objects[18] = Platform(x=0, y=93, w=160, h=1)
        objects[19] = Ladder(x=72, y=53, w=16, h=38)
    
    elif room == 20:
        if level == 0 or level == 1:
            if ram_state[77]&16 or ram_state[77]&128:
                # ruby
                ruby = Ruby()
                ruby.xy = ram_state[44] - 1, 54
                objects[2] = ruby
                if ram_state[84] > 0:
                    ruby2 = Ruby()
                    ruby2.xy = ram_state[44] + 63, 53 + (255 - ram_state[45])
                    objects[3] = ruby2
                else:
                    objects[3] = None
            else:
                    objects[2] = None
                    objects[3] = None    
        elif level == 2:
            # key
            if ram_state[77]&16:
                item = Key()
                item.xy = ram_state[44] - 1, 54 
                objects[1] = item
            else:
                objects[1] = None

        objects[18] = Platform(x=0, y=94, w=36, h=1)
        if ram_state[34] != 232:
            objects[19] = Disappearing_Platform(x=36, y=94, w=88, h=7)
        objects[20] = Platform(x=124, y=94, w=32, h=1)
        objects[21] = Wall(x=156, y=52, w=3, h=42)

    elif room == 21:
        if level == 0:
            # spider
            if ram_state[77]&1:
                enemy = Spider()
                enemy.xy = ram_state[44] - 1, 53 + (255 - ram_state[45])
                objects[4] = enemy
            else:
                objects[4] = None

        elif level == 1:
            # key
            if ram_state[77]&1:
                item = Key() 
                item.xy = ram_state[44] - 1, 53 + (255 - ram_state[45])
                objects[1] = item
            else:
                objects[1] = None
        elif level == 2:
            # snek
            if ram_state[77]&1:
                enemy = Snake()
                enemy.xy = ram_state[44], 53 + (255 - ram_state[45])
                objects[4] = enemy
            else:
                objects[4] = None

        objects[18] = Platform(x=0, y=93, w=158, h=1)
        objects[19] = Ladder(x=72, y=53, w=16, h=38)
        objects[20] = Wall(x=0, y=53, w=3, h=40)
    
    elif room == 22:
        if level == 0:
            # snakes
            if ram_state[78]&16:
                enemy = Snake()
                enemy.xy = ram_state[44], 53 + (255 - ram_state[45]) 
                objects[4] = enemy
            else:
                objects[4] = None
        elif level == 1:
            # spider
            if ram_state[78]&16:
                enemy = Spider()
                enemy.xy = ram_state[44] - 1, 53 + (255 - ram_state[45]) 
                objects[4] = enemy
            else:
                objects[4] = None
        elif level == 2:
            # skull
            if ram_state[78]&16:
                enemy = Skull()
                enemy.xy = ram_state[44] - 1, 53 + (255 - ram_state[45]) 
                objects[4] = enemy
            else:
                objects[4] = None

        objects[18] = Ladder(x=72, y=53, w=16, h=38)
        objects[19] = Platform(x=0, y=93, w=36, h=1)
        if ram_state[34] != 232:
            objects[20] = Disappearing_Platform(x=36, y=93, w=88, h=7)
        objects[21] = Platform(x=124, y=93, w=36, h=1)

    elif room == 23:
        # ruby
        if ram_state[78]&1 or ram_state[78]&2 or ram_state[78]&4:
            ruby = Ruby()
            ruby.xy = ram_state[44] - 1, 54
            objects[2] = ruby
            if ram_state[84] > 0 and ram_state[78]&2:
                ruby2 = Ruby()
                ruby2.xy = ram_state[44] + 15, 53 + (255 - ram_state[45])
                objects[3] = ruby2
                if ram_state[84] > 1 and ram_state[78]&4:
                    ruby3 = Ruby()
                    ruby3.xy = ram_state[44] + 31, 53 + (255 - ram_state[45])
                    objects[4] = ruby3
                else:
                    objects[4] = None
            else:
                    objects[3] = None
                    if ram_state[84] > 0 and ram_state[78]&4:
                        ruby3 = Ruby()
                        ruby3.xy = ram_state[44] + 31, 53 + (255 - ram_state[45])
                        objects[4] = ruby3
                    else:
                        objects[4] = None
        else:
            objects[2] = None
            objects[3] = None
            objects[4] = None

        objects[18] = Wall(x=156, y=53, w=3, h=40)
        objects[19] = Platform(x=0, y=93, w=158, h=1)

    if hud:
        for i in range(19):
            objects[i+36] = None

        x = 56
        y = 28

        torch_h = objects[36]

        sword1_h, sword2_h = objects[37], objects[38]

        key1_h, key2_h, key3_h, key4_h = objects[39], objects[40], objects[41], objects[42]
        
        amulet_h = objects[43]

        if ram_state[65] & 128:
            torch_h = Torch_HUD()
            objects[36] = torch_h
            x = x + 8

        if ram_state[65] & 64:
            sword1_h = Sword_HUD()
            sword1_h.xy = x, y
            objects[37] = sword1_h
            x = x + 8

        if ram_state[65] & 32:
            sword2_h = Sword_HUD()
            sword2_h.xy = x, y
            objects[38] = sword2_h
            x = x + 8

        if ram_state[65] & 16:
            key1_h = Key_HUD()
            key1_h.xy = x, y
            objects[39] = key1_h
            x = x + 8

        if ram_state[65] & 8:
            key2_h = Key_HUD()
            key2_h.xy = x, y
            objects[40] = key2_h
            x = x + 8

        if ram_state[65] & 4:
            key3_h = Key_HUD()
            key3_h.xy = x, y
            objects[41] = key3_h
            x = x + 8

        if ram_state[65] & 2 and x < 104:
            key4_h = Key_HUD()
            key4_h.xy = x, y
            objects[42] = key4_h
            x = x + 8

        if ram_state[65] & 1 and x < 104:
            amulet_h = Amulet_HUD()
            amulet_h.xy = x, y
            objects[43] = amulet_h

        # life
        for i in range(ram_state[58]):
            life = Life()
            life.xy = 56 + (i * 8), 15
            objects[44+i] = life

        # score
        if ram_state[19] > 15:
            for i in range(6):
                score = Score()
                score.xy = 97 - (i * 8), 6
                objects[49+i] = score
        elif ram_state[19] > 0:
            for i in range(5):
                score = Score()
                score.xy = 97 - (i * 8), 6
                objects[49+i] = score
        elif ram_state[20] > 15:
            for i in range(4):
                score = Score()
                score.xy = 97 - (i * 8), 6
                objects[49+i] = score
        elif ram_state[20] > 0:
            for i in range(3):
                score = Score()
                score.xy = 97 - (i * 8), 6
                objects[49+i] = score
        elif ram_state[21] > 15:
            for i in range(2):
                score = Score()
                score.xy = 97 - (i * 8), 6
                objects[49+i] = score
        else:
            score = Score()
            objects[49] = score

    return objects


def _detect_objects_montezumarevenge_raw(info, ram_state):
    pass
