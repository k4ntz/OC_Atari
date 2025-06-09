from .game_objects import GameObject, ValueObject, NoObject, Orientation, OrientedObject
from ._helper_methods import _convert_number, get_iou
import sys

"""
RAM extraction for the game PrivateEye. Supported modes: ram.

"""

MAX_NB_OBJECTS = {'Player': 1, 'Car': 1, 'Clue': 1, 'Badguy': 1, 'Mud': 2, 'Shatterd_Object': 4,
                  'Knife': 2, 'Dove': 2, 'Lizard': 2, 'Pottet_Plant': 4, 'Brick': 4, 'Barrier': 2,
                  'Passage': 1, 'Money_Bag': 1, 'Gun': 1, 'Button': 1, 'Comb': 1, 'Shoe_Sole': 1,
                  'Vase': 1, 'Necklace': 1, 'Stamp': 1, 'Badguy_Head': 3}
MAX_NB_OBJECTS_HUD = {'Player': 1, 'Car': 1, 'Badguy': 1, 'Clue': 1, 'Mud': 2, 'Shatterd_Object': 4,
                      'Knife': 2, 'Dove': 2, 'Lizard': 2, 'Pottet_Plant': 4, 'Brick': 4, 'Barrier': 2,
                      'Passage': 1, 'Money_Bag': 1, 'Gun': 1, 'Button': 1, 'Comb': 1, 'Shoe_Sole': 1,
                      'Vase': 1, 'Necklace': 1, 'Stamp': 1, 'Badguy_Head': 3, 'Score': 1, 'Clock': 1}
obj_tracker = {}


class Player(OrientedObject):
    """
    The player figure: Pierre Touche.
    """

    def __init__(self):
        super(Player, self).__init__()
        self._xy = 0, 0
        self.wh = 8, 12
        self.orientation = Orientation.E
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


class Badguy(GameObject):
    def __init__(self):
        super(Badguy, self).__init__()
        self._xy = 0, 0
        self.wh = 20, 14
        self.rgb = 0, 0, 148
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


class Passage(GameObject):
    """
    The passages into alleys or park lanes.
    """

    def __init__(self):
        super(Passage, self).__init__()
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
        super(Bank_Sign, self).__init__()
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
        self._xy = 99, 8
        self.wh = 6, 8
        self.rgb = 236, 236, 236
        self.hud = True


class Clock(ValueObject):
    """
    The statue of limitation (game clock display) for the current case.
    """

    def __init__(self, *args, **kwargs):
        super(Clock, self).__init__()
        self._xy = 67, 19
        self.wh = 30, 8
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

    objects.extend([NoObject()] * 37)
    if hud:
        objects.extend([Score(), Clock()])
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
        player.orientation = Orientation.N
        car.orientation = Orientation.N
        car.wh = 8, 14
        if not ram_state[88] & 128:
            if ram_state[58] == 1:
                car.xy = car_x, 150 - (ram_state[88]>>2) + 13
                player.xy = car_x, 150 - (ram_state[88]>>2) - 1
            else:
                car.xy = car_x, 150 + (ram_state[88]>>3) - 14
                player.xy = car_x, 150 + (ram_state[88]>>3) - 28
        else:
            car.xy = car_x, 156 + ((ram_state[88] - 128)>>2) - 24
            player.xy = car_x, 156 + ((ram_state[88] - 128)>>2) - 38

    else:
        if ram_state[58] == 49:
            car_x = ram_state[63] - 3
            car.wh = 20, 14
            player.orientation = Orientation.E
            car.orientation = Orientation.E
        else:   # ram_state[58] == 121:
            car_x = ram_state[63] - 9
            car.wh = 20, 14
            player.orientation = Orientation.W
            car.orientation = Orientation.W

        if not ram_state[84] & 128:
            car.xy = car_x, 150 - (int(ram_state[84]/4)) + 13
        else:
            car.xy = car_x, 156 + (int((ram_state[84] - 128)/4)) - 24


# 2 branch, 4 brick, 7 bricks, 8 curtain, 9 hydrant, 20 gun, 21 button, 22 comb, 23 shoe sole,24 money, 25 vase, 26 necklace, 27 stamp, 28 badguy body, 29,30 badguy head, 31 Questionmark, 32 knife

    idx = []

    # interactable Objects1
    if ram_state[41] != 0:
        if ram_state[41] == 1:
            if type(objects[25]) is NoObject:
                objects[25] = Barrier()
            objects[25].xy = 15 + ram_state[47], 165 - ram_state[38]
            idx.append(25)
        elif ram_state[41] == 3:
            if type(objects[17]) is NoObject:
                objects[17] = Pottet_Plant()
            x = 15 + ram_state[47]
            objects[17].xy = x, 167 - ram_state[38]
            idx.append(17)
            if ram_state[44]:
                if type(objects[18]) is NoObject:
                    objects[18] = Pottet_Plant()
                objects[18].xy = x + 16*ram_state[44], 167 - ram_state[38]
                idx.append(18)
        elif ram_state[41] == 4:
            if type(objects[21]) is NoObject:
                objects[21] = Brick()
            x = 17 + ram_state[47]
            objects[21].xy = x, 179 - ram_state[38]
            idx.append(21)
            if ram_state[44]:
                if type(objects[22]) is NoObject:
                    objects[22] = Brick()
                objects[22].xy = x + 16*ram_state[44], 179 - ram_state[38]
                idx.append(22)
        elif ram_state[41] == 5 or ram_state[41] == 6:
            if type(objects[27]) is NoObject:
                objects[27] = Passage()
            objects[27].xy = 16 + ram_state[47], 161 - ram_state[38]
            idx.append(27)
        elif ram_state[41] == 10:
            if type(objects[5]) is NoObject:
                objects[5] = Mud()
            objects[5].xy = 15 + ram_state[47], 179 - ram_state[38]
            idx.append(5)
        elif ram_state[41] == 11 or ram_state[41] == 12 or ram_state[41] == 13:
            if type(objects[7]) is NoObject:
                objects[7] = Shatterd_Object()
            x = 15 + ram_state[47]
            objects[7].xy = x, 179 - ram_state[38]
            idx.append(7)
            if ram_state[44]:
                if type(objects[8]) is NoObject:
                    objects[8] = Shatterd_Object()
                objects[8].xy = x + 16*ram_state[44], 179 - ram_state[38]
                idx.append(8)
        elif ram_state[41] == 14 or ram_state[41] == 15:
            if type(objects[13]) is NoObject:
                objects[13] = Dove()
            objects[13].xy = 15 + ram_state[47], 177 - ram_state[38]
            idx.append(13)
        elif ram_state[41] == 16 or ram_state[41] == 17:
            if type(objects[15]) is NoObject:
                objects[15] = Lizard()
            objects[15].xy = 15 + ram_state[47], 179 - ram_state[38]
            idx.append(15)
        elif ram_state[41] == 29:
            if type(objects[36]) is NoObject:
                objects[36] = Badguy_Head()
            objects[36].xy = 15 + ram_state[47], 177 - ram_state[38]
            idx.append(36)
        elif ram_state[41] == 32:
            if type(objects[11]) is NoObject:
                objects[11] = Knife()
            objects[11].xy = 15 + ram_state[47], 179 - ram_state[38]
            idx.append(11)

    # Interactable Objects2
    if ram_state[42] != 0:
        if ram_state[42] == 1:
            if type(objects[26]) is NoObject:
                objects[26] = Barrier()
            objects[26].xy = 15 + ram_state[48], 165 - ram_state[39]
            idx.append(26)
        elif ram_state[42] == 3:
            if type(objects[19]) is NoObject:
                objects[19] = Pottet_Plant()
            x = 15 + ram_state[48]
            objects[19].xy = x, 167 - ram_state[39]
            idx.append(19)
            if ram_state[44]:
                if type(objects[20]) is NoObject:
                    objects[20] = Pottet_Plant()
                objects[20].xy = x + 16*ram_state[44], 167 - ram_state[39]
                idx.append(20)
        elif ram_state[42] == 4:
            if type(objects[23]) is NoObject:
                objects[23] = Brick()
            x = 17 + ram_state[48]
            objects[23].xy = x, 179 - ram_state[39]
            idx.append(23)
            if ram_state[44]:
                if type(objects[24]) is NoObject:
                    objects[24] = Brick()
                objects[24].xy = x + 16*ram_state[44], 179 - ram_state[39]
                idx.append(24)
        elif ram_state[42] == 10:
            if type(objects[6]) is NoObject:
                objects[6] = Mud()
            objects[6].xy = 15 + ram_state[48], 179 - ram_state[39]
            idx.append(6)
        elif ram_state[42] == 11 or ram_state[42] == 12 or ram_state[42] == 13:
            if type(objects[9]) is NoObject:
                objects[9] = Shatterd_Object()
            x = 15 + ram_state[48]
            objects[9].xy = x, 179 - ram_state[39]
            idx.append(9)
            if ram_state[44]:
                if type(objects[10]) is NoObject:
                    objects[10] = Shatterd_Object()
                objects[10].xy = x + 16*ram_state[44], 179 - ram_state[38]
                idx.append(10)
        elif ram_state[42] == 14 or ram_state[42] == 15:
            if type(objects[14]) is NoObject:
                objects[14] = Dove()
            objects[14].xy = 15 + ram_state[48], 177 - ram_state[39]
            idx.append(14)
        elif ram_state[42] == 16 or ram_state[42] == 17:
            if type(objects[16]) is NoObject:
                objects[16] = Lizard()
            objects[16].xy = 15 + ram_state[48], 179 - ram_state[39]
            idx.append(16)
        elif ram_state[42] == 28:
            if type(objects[4]) is NoObject:
                objects[4] = Badguy()
            objects[4].xy = 15 + ram_state[48], 169 - ram_state[39] + ram_state[51]
            objects[4].wh = 8, 14 - ram_state[51]
            idx.append(4)
        elif ram_state[42] == 29:
            if type(objects[37]) is NoObject:
                objects[37] = Badguy_Head()
            objects[37].xy = 15 + ram_state[48], 177 - ram_state[39]
            idx.append(37)
        elif ram_state[42] == 32:
            if type(objects[12]) is NoObject:
                objects[12] = Knife()
            objects[12].xy = 15 + ram_state[48], 179 - ram_state[39]
            idx.append(12)

    # clues and additional env objects
    if ram_state[43] == 30 or ram_state[43] == 31:
        if type(objects[3]) is NoObject:
            objects[3] = Clue()
        objects[3].xy = 15 + ram_state[49], 169 - ram_state[40]
    else:
        objects[3] = NoObject()

    # 20 gun, 21 button, 22 comb, 23 shoe sole,24 money, 25 vase, 26 necklace, 27 stamp, 28 badguy body, 29,30 badguy head
    if ram_state[60]:
        x = 140
        obj = None
        if ram_state[60] == 20:
            if type(objects[29]) is NoObject:
                objects[29] = Gun()
            obj = objects[29]
            idx.append(29)
        elif ram_state[60] == 21:
            if type(objects[30]) is NoObject:
                objects[30] = Button()
            obj = objects[30]
            idx.append(30)
            x = 141
        elif ram_state[60] == 22:
            if type(objects[31]) is NoObject:
                objects[31] = Comb()
            obj = objects[31]
            idx.append(31)
        elif ram_state[60] == 23:
            if type(objects[32]) is NoObject:
                objects[32] = Shoe_Sole()
            obj = objects[32]
            idx.append(32)
        elif ram_state[60] == 24:
            if type(objects[28]) is NoObject:
                objects[28] = Money_Bag()
            obj = objects[28]
            idx.append(28)
        elif ram_state[60] == 25:
            if type(objects[33]) is NoObject:
                objects[33] = Vase()
            obj = objects[33]
            idx.append(29)
        elif ram_state[33] == 26:
            if type(objects[34]) is NoObject:
                objects[34] = Necklace()
            obj = objects[34]
            idx.append(34)
        elif ram_state[60] == 27:
            if type(objects[35]) is NoObject:
                objects[35] = Stamp()
            obj = objects[35]
            idx.append(35)
        elif ram_state[60] == 29 or ram_state[60] == 30:
            if type(objects[38]) is NoObject:
                objects[38] = Badguy_Head()
            obj = objects[38]
            idx.append(38)
        if obj:
            obj.xy = x, 45-obj.h
        
    no_obj = [i for i in range(4, 39) if i not in idx]
    for i in no_obj:
        objects[i] = NoObject()

    if hud:
        
        # score
        x, w = 99, 6
        if ram_state[72] > 15:
            x, w = 59, 46
        elif ram_state[72] != 0:
            x, w = 67, 38
        elif ram_state[73] > 15:
            x, w = 75, 30
        elif ram_state[73] != 0:
            x, w = 83, 22
        elif ram_state[74] > 15:
            x, w = 91, 14

        objects[39].xywh = x, 8, w, 8
        objects[39].value = _convert_number(
            ram_state[72])*10000 + _convert_number(ram_state[73])*100 + _convert_number(ram_state[74])

        # time
        objects[40].value = _convert_number(
            ram_state[67])*60 + _convert_number(ram_state[69])

    return objects


def _detect_objects_privateeye_raw(info, ram_state):
    pass
