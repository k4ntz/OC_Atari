from .game_objects import GameObject, ValueObject, ValueObject
from ._helper_methods import _convert_number, get_iou
import sys

"""
RAM extraction for the game PrivateEye. Supported modes: ram.

"""

MAX_NB_OBJECTS =  {'Player': 1, 'Car': 1}
MAX_NB_OBJECTS_HUD = {'Player': 1, 'Car': 1, 'Score': 1, 'Clock': 1}
obj_tracker = {}

class Player(GameObject):
    """
    The player figure: Pierre Touche.
    """
    
    def __init__(self):
        super(Player, self).__init__()
        self._xy = 0, 0
        self.wh = 8, 12
        self.orientation = 1
        self.rgb = 210, 210, 64
        self.hud = False


class Car(GameObject):
    """
    The Touche's 1935 Model A with jumping capabilities.
    """
    
    def __init__(self):
        super(Car, self).__init__()
        self._xy = 0, 0
        self.wh = 20, 14
        self.orientation = 1
        self.rgb = 0, 0, 0
        self.hud = False


class Badguy(GameObject):
    def __init__(self):
        super(Badguy, self).__init__()
        self._xy = 0, 0
        self.wh = 20, 14
        self.rgb = 0, 0, 0
        self.hud = False


class Clue(GameObject):
    """
    The questionable characters lurking from the windows.
    """
    
    def __init__(self):
        super(Clue, self).__init__()
        self._xy = 0, 0
        self.wh = 8, 14
        self.rgb = 24, 26, 167
        self.hud = False


class Mud(GameObject):
    """
    The pot holes.
    """
    
    def __init__(self):
        super(Mud, self).__init__()
        self._xy = 0, 0
        self.wh = 8, 4
        self.rgb = 0, 0, 0
        self.hud = False


class Shatterd_Object(GameObject):
    """
    The animation for broken bricks or flowerpots once they've hit the ground.
    """
    
    def __init__(self):
        super(Shatterd_Object, self).__init__()
        self._xy = 0, 0
        self.wh = 8, 4
        self.rgb = 0, 0, 0
        self.hud = False


class Knife(GameObject):
    """
    The daggers thrown at the player, once the first item is collected.
    """
    
    def __init__(self):
        super(Knife, self).__init__()
        self._xy = 0, 0
        self.wh = 8, 4
        self.rgb = 0, 0, 0
        self.hud = False

class Dove(GameObject):
    """
    The birds.
    """
    
    def __init__(self):
        super(Dove, self).__init__()
        self._xy = 0, 0
        self.wh = 8, 6
        self.rgb = 236, 236, 236
        self.hud = False


class Lizard(GameObject):
    """
    The crawling rats.
    """
    
    def __init__(self):
        super(Lizard, self).__init__()
        self._xy = 0, 0
        self.wh = 8, 4
        self.rgb = 210, 210, 64
        self.hud = False


class Pottet_Plant(GameObject):
    """
    The flowerpots thrown from windows.
    """
    
    def __init__(self):
        super(Pottet_Plant, self).__init__()
        self._xy = 0, 0
        self.wh = 6, 16
        self.rgb = 110, 156, 66
        self.hud = False


class Brick(GameObject):
    """
    The bricks, occasionally dropping from the building facades.
    """
    
    def __init__(self):
        super(Brick, self).__init__()
        self._xy = 0, 0
        self.wh = 4, 4
        self.rgb = 184, 50, 50
        self.hud = False


class Barrier(GameObject):
    """
    The roadblocks.
    """
    
    def __init__(self):
        super(Barrier, self).__init__()
        self._xy = 0, 0
        self.wh = 8, 18
        self.rgb = 252, 252, 84
        self.hud = False


class Passge(GameObject):
    """
    The passages into alleys or park lanes.
    """
    
    def __init__(self):
        super(Passge, self).__init__()
        self._xy = 0, 0
        self.wh = 32, 22

        self.rgb = 104, 25, 154
        self.hud = False


class Gun_Sign(GameObject):
    """
    The header of the gunstore.
    """
    
    def __init__(self):
        super(Gun_Sign, self).__init__()
        self._xy = 0, 0
        self.wh = 8, 4
        self.rgb = 252, 252, 84
        self.hud = False


class Police_Sign(GameObject):
    """
    The header of the police headquaters.
    """
    
    def __init__(self):
        super(Police_Sign, self).__init__()
        self._xy = 0, 0
        self.wh = 8, 4
        self.rgb = 0, 0, 0
        self.hud = False


class Bank_Sign(GameObject):
    """
    The header of the bank building.
    """
    
    def __init__(self):
        super(Police_Sign, self).__init__()
        self._xy = 0, 0
        self.wh = 8, 4
        self.rgb = 82, 126, 45
        self.hud = False


class Money_Bag(GameObject):
    """
    The inventory display for the bag of stolen money (case 1).
    """
    
    def __init__(self):
        super(Money_Bag, self).__init__()
        self._xy = 0, 0
        self.wh = 7, 11
        self.rgb = 236, 236, 236
        self.hud = False


class Gun(GameObject):
    """
    The inventory display for the gun (case 1).
    """
    
    def __init__(self):
        super(Gun, self).__init__()
        self._xy = 0, 0
        self.wh = 8, 8
        self.rgb = 0, 0, 0
        self.hud = False


class Button(GameObject):
    """
    The inventory display for the lost button (case 2).
    """
    
    def __init__(self):
        super(Button, self).__init__()
        self._xy = 0, 0
        self.wh = 7, 9
        self.rgb = 252, 252, 84
        self.hud = False


class Comb(GameObject):
    """
    The inventory display for the comb (case 3).
    """
    
    def __init__(self):
        super(Comb, self).__init__()
        self._xy = 0, 0
        self.wh = 8, 15
        self.rgb = 0, 0, 0
        self.hud = False


class Shoe_Sole(GameObject):
    """
    The inventory display for the shoe sole (case 4).
    """
    
    def __init__(self):
        super(Shoe_Sole, self).__init__()
        self._xy = 0, 0
        self.wh = 8, 11
        self.rgb = 0, 0, 0
        self.hud = False


class Vase(GameObject):
    """
    The inventory display for the ming vase (case 2).
    """
    
    def __init__(self):
        super(Vase, self).__init__()
        self._xy = 0, 0
        self.wh = 8, 14
        self.rgb = 252, 144, 144
        self.hud = False


class Necklace(GameObject):
    """
    The inventory display for the diamond necklace (case 3).
    """
    
    def __init__(self):
        super(Necklace, self).__init__()
        self._xy = 0, 0
        self.wh = 8, 11
        self.rgb = 252, 252, 84
        self.hud = False


class Stamp(GameObject):
    """
    The inventory display for the stamp (case 4).
    """
    
    def __init__(self):
        super(Stamp, self).__init__()
        self._xy = 0, 0
        self.wh = 8, 14
        self.rgb = 132, 252, 212
        self.hud = False


class Badguy_Head(GameObject):
    """
    The thugs lurching out to attack the player.
    """
    
    def __init__(self):
        super(Badguy_Head, self).__init__()
        self._xy = 0, 0
        self.wh = 8, 7
        self.rgb = 24, 26, 167
        self.hud = False


class Score(ValueObject):
    """
    The player's merit score display.
    """
    
    def __init__(self, *args, **kwargs):
        super(Score, self).__init__()
        self._xy = 97, 6
        self.wh = 5, 8
        self.rgb = 236, 236, 236
        self.hud = True


class Clock(ValueObject):
    """
    The statue of limitation (game clock display) for the current case.
    """
    
    def __init__(self, *args, **kwargs):
        super(Clock, self).__init__()
        self._xy = 88, 15
        self.wh = 7, 5
        self.rgb = 236, 236, 236
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

def _init_objects_ram(hud=True):
    """
    (Re)Initialize the objects
    """

    objects = [Player(), Car()]

    objects.extend([None] * 6)
    if hud:
        objects.extend([None] * 2)
    return objects


# levels: ram_state[36], total of 3 levels: 0,1 and 2
def _detect_objects_ram(objects, ram_state, hud=True):
    player = objects[0]

    if ram_state[97] == 0:
        player.wh = 8, 12
    else:
        player.wh = 8, 25
    player._xy = ram_state[63], 150 - ram_state[97]
    player._xy = ram_state[63], 150 - ram_state[97]
    
    car = objects[1]
    if ram_state[58] == 1 or ram_state[58] == 5:
        car_x = ram_state[63]
        player.orientation = 2
        car.orientation = 2
        car.wh = 8, 14
        if not ram_state[88] & 128:
            if ram_state[58] == 1:
                car.xy = car_x, 150 - (int(ram_state[88]/4)) + 13
                player.xy = car_x, 150 - (int(ram_state[88]/4)) -1
            else:
                car.xy = car_x, 150 + (int(ram_state[88]/8)) - 14
                player.xy = car_x, 150 + (int(ram_state[88]/8)) - 28
        else:
            car.xy = car_x, 156 + (int((ram_state[88] - 128)/4)) - 24
            player.xy = car_x, 156 + (int((ram_state[88] - 128)/4)) - 38

    else:
        if ram_state[58] == 49:
            car_x = ram_state[63] - 3
            car.wh = 20, 14
            player.orientation = 1
            car.orientation = 1
        else:   # ram_state[58] == 121:
            car_x = ram_state[63] - 9
            car.wh = 20, 14
            player.orientation = 0
            car.orientation = 0

        if not ram_state[84] & 128:
            car.xy = car_x, 150 - (int(ram_state[84]/4)) + 13
        else:
            car.xy = car_x, 156 + (int((ram_state[84] - 128)/4)) - 24
    

# 2 branch, 4 brick, 7 bricks, 8 curtain, 9 hydrant, 20 gun, 21 button, 22 comb, 23 shoe sole,24 money, 25 vase, 26 necklace, 27 stamp, 28 badguy body, 29,30 badguy head, 31 Questionmark, 32 knife

    #interactable Objects1
    if ram_state[41] != 0:
        objects[4] = None
        if ram_state[41] == 1:
            obj = Barrier()
            obj.xy = 15 + ram_state[47], 165 - ram_state[38]
        elif ram_state[41] == 3:
            obj = Pottet_Plant()
            x = 15 + ram_state[47]
            obj.xy = x, 167 - ram_state[38]
            if ram_state[44]:
                obj2 = Pottet_Plant()
                obj2.xy = x + 16*ram_state[44], 167 - ram_state[38]
                objects[4] = obj2
            else:
                objects[4] = None
        elif ram_state[41] == 4:
            obj = Brick()
            x = 17 + ram_state[47]
            obj.xy = x, 179 - ram_state[38]
            if ram_state[44]:
                obj2 = Brick()
                obj2.xy = x + 16*ram_state[44], 179 - ram_state[38]
                objects[4] = obj2
            else:
                objects[4] = None
        elif ram_state[41] == 5 or ram_state[41] == 6:
            obj = Passge()
            obj.xy = 16 + ram_state[47], 161 - ram_state[38]
        elif ram_state[41] == 10:
            obj = Mud()
            obj.xy = 15 + ram_state[47], 179 - ram_state[38]
        elif ram_state[41] == 11 or ram_state[41] == 12 or ram_state[41] == 13:
            obj = Shatterd_Object()
            x = 15 + ram_state[47]
            obj.xy = x, 179 - ram_state[38]
            if ram_state[44]:
                obj2 = Shatterd_Object()
                obj2.xy = x + 16*ram_state[44], 179 - ram_state[38]
                objects[4] = obj2
            else:
                objects[4] = None
        elif ram_state[41] == 14 or ram_state[41] == 15:
            obj = Dove()
            obj.xy = 15 + ram_state[47], 177 - ram_state[38]
        elif ram_state[41] == 16 or ram_state[41] == 17:
            obj = Lizard()
            obj.xy = 15 + ram_state[47], 179 - ram_state[38]
        elif ram_state[41] == 29:
            obj = Badguy_Head()
            obj.xy = 15 + ram_state[47], 177 - ram_state[38]
        elif ram_state[41] == 32:
            obj = Knife()
            obj.xy = 15 + ram_state[47], 179 - ram_state[38]
        else:
            obj = None
        objects[2] = obj
    else:
        objects[2] = None
        objects[4] = None

    # Interactable Objects2 
    if ram_state[42] != 0:
        objects[5] = None
        if ram_state[42] == 1:
            obj = Barrier()
            obj.xy = 15 + ram_state[48], 165 - ram_state[39]
        elif ram_state[42] == 3:
            obj = Pottet_Plant()
            x = 15 + ram_state[48]
            obj.xy = x, 167 - ram_state[39]
            if ram_state[44]:
                obj2 = Pottet_Plant()
                obj2.xy = x + 16*ram_state[44], 167 - ram_state[39]
                objects[5] = obj2
            else:
                objects[5] = None
        elif ram_state[42] == 4:
            obj = Brick()
            x = 17 + ram_state[48]
            obj.xy = x, 179 - ram_state[39]
            if ram_state[44]:
                obj2 = Brick()
                obj2.xy = x + 16*ram_state[44], 179 - ram_state[39]
                objects[5] = obj2
            else:
                objects[5] = None
        elif ram_state[42] == 10:
            obj = Mud()
            obj.xy = 15 + ram_state[48], 179 - ram_state[39]
        elif ram_state[42] == 11 or ram_state[42] == 12 or ram_state[42] == 13:
            obj = Shatterd_Object()
            x = 15 + ram_state[48]
            obj.xy = x, 179 - ram_state[39]
            if ram_state[44]:
                obj2 = Shatterd_Object()
                obj2.xy = x + 16*ram_state[44], 179 - ram_state[38]
                objects[5] = obj2
            else:
                objects[4] = None
        elif ram_state[42] == 14 or ram_state[42] == 15:
            obj = Dove()
            obj.xy = 15 + ram_state[48], 177 - ram_state[39]
        elif ram_state[42] == 16 or ram_state[42] == 17:
            obj = Lizard()
            obj.xy = 15 + ram_state[48], 179 - ram_state[39]
        elif ram_state[42] == 29:
            obj = Badguy_Head()
            obj.xy = 15 + ram_state[48], 177 - ram_state[39]
        elif ram_state[42] == 32:
            obj = Knife()
            obj.xy = 15 + ram_state[48], 179 - ram_state[39]
        else:
            obj = None
        objects[3] = obj
    else:
        objects[3] = None
        objects[5] = None

    # clues and additional env objects
    if ram_state[43] == 30 or ram_state[43] == 31:
        obj = Clue()
        obj.xy = 15 + ram_state[49], 169 - ram_state[40]
        objects[6] = obj
    else:
        objects[6] = None

    # 20 gun, 21 button, 22 comb, 23 shoe sole,24 money, 25 vase, 26 necklace, 27 stamp, 28 badguy body, 29,30 badguy head
    if ram_state[60]:
        obj = None
        x = 140
        if ram_state[60] == 20:
            obj = Gun()
        elif ram_state[60] == 21:
            obj = Button()
            x = 141
        elif ram_state[60] == 22:
            obj = Comb()
        elif ram_state[60] == 23:
            obj = Shoe_Sole()
        elif ram_state[60] == 24:
            obj = Money_Bag()
        elif ram_state[60] == 25:
            obj = Vase()
        elif ram_state[60] == 26:
            obj = Necklace()
        elif ram_state[60] == 27:
            obj = Stamp()
        elif ram_state[60] == 29 or ram_state[60] == 30:
            obj = Badguy_Head()
        objects[7] = obj
        if obj is not None:
            obj.xy = x, 45-obj.h
    else:
        objects[7] = None

    if hud:
        score = Score()
        objects[8] = score
        if ram_state[72] > 15:
            score.xy = 59, 8
            score.wh = 46, 8
        elif ram_state[72] != 0:
            score.xy = 67, 8
            score.wh = 38, 8
        elif ram_state[73] > 15:
            score.xy = 75, 8
            score.wh = 30, 8
        elif ram_state[73] != 0:
            score.xy = 83, 8
            score.wh = 22, 8
        elif ram_state[74] > 15:
            score.xy = 91, 8
            score.wh = 14, 8
        else:
            score.xy = 99, 8
            score.wh = 6, 8
        score.value = _convert_number(ram_state[72])*10000 + _convert_number(ram_state[73])*100 + _convert_number(ram_state[74])
        
        clock = Clock()
        objects[9] = clock
        clock.xy = 67, 19
        clock.wh = 30, 8
        clock.value = _convert_number(ram_state[67])*60 + _convert_number(ram_state[69])

    return objects


def _detect_objects_privateeye_raw(info, ram_state):
    pass
