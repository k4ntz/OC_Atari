from .game_objects import GameObject, ValueObject, NoObject
from ._helper_methods import _convert_number, get_iou
import sys

"""
RAM extraction for the game Montezuma's Revenge.
"""

MAX_NB_OBJECTS = {'Player': 1, 'Key': 1, 'Amulet': 1, 'Sword': 1, 'Torch': 1, 'Ruby': 3, 'Skull': 2, 'Spider': 1, 'Snake': 2,
                  'Barrier': 2, 'Beam': 8, 'Rope': 2, 'Wall': 4, 'Ladder': 3, 'Platform': 7, 'Disappearing_Platform': 12, 'Conveyer_Belt': 2, 'Key_HUD': 4, 'Amulet_HUD': 1, 'Torch_HUD': 1, 'Sword_HUD': 2}
MAX_NB_OBJECTS_HUD = {'Player': 1, 'Skull': 2, 'Spider': 1, 'Snake': 2, 'Key': 1, 'Amulet': 1, 'Torch': 1, 'Sword': 1,
                      'Barrier': 2, 'Beam': 8, 'Rope': 2, 'Ruby': 3, 'Wall': 4, 'Ladder': 2, 'Platform': 7, 'Disappearing_Platform': 12, 'Conveyer_Belt': 2, 'Key_HUD': 4, 'Amulet_HUD': 1, 'Torch_HUD': 1, 'Sword_HUD': 2,
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

    def __init__(self, x=89, y=166, *args, **kwargs):
        super(Key, self).__init__()
        super().__init__(*args, **kwargs)
        self._xy = x, y
        self.wh = 7, 15
        self.rgb = 232, 204, 99
        self.hud = False


class Amulet(GameObject):
    """
    The collectable amulets, which make enemies disappear temporally.
    """

    def __init__(self, x=89, y=166, *args, **kwargs):
        super(Amulet, self).__init__()
        super().__init__(*args, **kwargs)
        self._xy = x, y
        self.wh = 6, 15
        self.rgb = 232, 204, 99
        self.hud = False


class Torch(GameObject):
    """
    The collectable torches for illuminating the rooms of the current game level.
    """

    def __init__(self, x=89, y=166, *args, **kwargs):
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

    def __init__(self, x=89, y=166, *args, **kwargs):
        super(Sword, self).__init__()
        super().__init__(*args, **kwargs)
        self._xy = x, y
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

    def __init__(self, x=112, y=96, w=1, h=39, *args, **kwargs):
        super(Rope, self).__init__()
        super().__init__(*args, **kwargs)
        self._xy = x, y
        self.wh = w, h
        self.rgb = 232, 204, 99
        self.hud = False


class Score(ValueObject):
    """
    The player's score display (HUD).
    """

    def __init__(self, *args, **kwargs):
        super(Score, self).__init__()
        self._xy = 97, 6
        self.wh = 5, 8
        self.rgb = 236, 236, 236
        self.hud = True
        self.value


class Life(ValueObject):
    """
    The player's remaining additional lives (displayed as hats) (HUD).
    """

    def __init__(self, *args, **kwargs):
        super(Life, self).__init__()
        self._xy = 56, 15
        self.wh = 7, 5
        self.rgb = 210, 182, 86
        self.hud = True
        self.value = 5


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
        self.hud = False


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
        self.hud = False


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
        self.hud = False


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
        self.hud = False


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

    def __init__(self, x=0, y=0, w=8, h=4, rgb=(66, 158, 130), *args, **kwargs):
        super(Wall, self).__init__(*args, **kwargs)
        self._xy = x, y
        self._prev_xy = x, y
        self.wh = w, h
        self.rgb = rgb
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


def _init_objects_ram(hud=True):
    """
    (Re)Initialize the objects
    """

    objects = [Player()]

    objects.extend([NoObject()] * 60)
    if hud:
        objects.extend([NoObject(), Score()])
    return objects


# levels: ram_state[36], total of 3 levels: 0,1 and 2
def _detect_objects_ram(objects, ram_state, hud=True):
    player = objects[0]
    key = objects[1]
    amulet = objects[2]
    sword = objects[3]
    torch = objects[4]
    ruby, ruby2, ruby3 = objects[5], objects[6], objects[7]
    enemy, enemy2 = objects[8], objects[9]
    barrier, barrier2 = objects[13], objects[14]
    beam0, beam1, beam2, beam3, beam4, beam5, beam6, beam7 = objects[15], objects[
        16], objects[17], objects[18], objects[19], objects[20], objects[21], objects[22]
    rope, rope2 = objects[23], objects[24]
    wall1, wall2, wall3, wall4 = objects[25], objects[26], objects[27], objects[28]
    ladder1, ladder2 = objects[29], objects[30]

    enviroment_objects = objects[18:36]

    room = ram_state[3]
    level = ram_state[57]
    # score = _convert_number(ram_state[19]) * 10000 + _convert_number(ram_state[20]) * 100 + _convert_number(ram_state[21])

    # player
    player = Player()
    player = objects[0]
    player.xy = ram_state[42] - 1, 255 - ram_state[43] + 53

    # for i in range(45):
    #     objects[i+1] = NoObject()

    if room < 16 or ram_state[65] & 128 or ram_state[49] == 5 or 8 < ram_state[49] < 11:
        # Check if items are present
        if 0 < ram_state[49] < 5 or ram_state[49] == 6:
            objects[5], objects[6] = NoObject(), NoObject()
            x = ram_state[44] - 1
            if room == 0:
                y = 55 + (255 - ram_state[45])
            elif room == 1:
                y = 98 + (255 - ram_state[45])
            elif room == 7:
                y = 54 + (255 - ram_state[45])
            else:
                y = 53 + (255 - ram_state[45])

            if ram_state[45] < 216:
                y += 4

            # Check if items are rubies
            if ram_state[49] == 1:
                if type(objects[5]) is NoObject:
                    objects[5] = Ruby()
                    objects[5].xy = x, y
                if ram_state[84] & 1:
                    if type(objects[6]) is NoObject:
                        objects[6] = Ruby()
                        objects[6].xy = x+16, y
                elif ram_state[84] & 4:
                    if type(objects[6]) is NoObject:
                        objects[6] = Ruby()
                        objects[6].xy = x+64, y
                else:
                    objects[6] = NoObject()
                if ram_state[84] & 2:
                    if type(objects[7]) is NoObject:
                        objects[7] = Ruby()
                        objects[7].xy = x+32, y
                else:
                    objects[7] = NoObject()
                # remove all items
                objects[1], objects[2], objects[3], objects[4] = NoObject(
                ), NoObject(), NoObject(), NoObject()
            else:
                # Else determine item and remove all rupies
                objects[5], objects[6], objects[7] = NoObject(
                ), NoObject(), NoObject()
                if ram_state[49] == 2:
                    if type(objects[3]) is NoObject:
                        objects[3] = Sword(x=x, y=y)
                        objects[1], objects[2], objects[4] = NoObject(
                        ), NoObject(), NoObject()

                elif ram_state[49] == 3:
                    if type(objects[2]) is NoObject:
                        objects[2] = Amulet(x=x, y=y)
                        objects[1], objects[3], objects[4] = NoObject(
                        ), NoObject(), NoObject()

                elif ram_state[49] == 4:
                    if type(objects[1]) is NoObject:
                        objects[1] = Key(x=x, y=y)
                        objects[2], objects[3], objects[4] = NoObject(
                        ), NoObject(), NoObject()

                elif ram_state[49] == 6:
                    if type(objects[4]) is NoObject:
                        objects[4] = Torch(x=x, y=y)
                        objects[1], objects[2], objects[3] = NoObject(
                        ), NoObject(), NoObject()

        # Check if enemies are present
        elif 4 < ram_state[49] < 11:
            # remove items
            for i in range(1, 8):
                objects[i] = NoObject()
            objects[1], objects[2], objects[3], objects[4] = NoObject(
            ), NoObject(), NoObject(), NoObject()
            x = ram_state[44] - 1
            if room == 0:
                y = 55 + (255 - ram_state[45])
            elif room == 1:
                y = 98 + (255 - ram_state[45])
            elif room == 7:
                y = 54 + (255 - ram_state[45])
            else:
                y = 53 + (255 - ram_state[45])

            if ram_state[45] < 216:
                y += 4

            if ram_state[45] < 216:
                y += 4

            idx = 8
            if ram_state[49] == 5:
                if type(objects[8]) is NoObject:
                    enemy = Skull()
                    objects[8] = enemy
            elif ram_state[49] < 9:
                if type(objects[11]) is NoObject:
                    enemy = Snake()
                    objects[11] = enemy
                x += 1
                idx = 11
            elif ram_state[49] < 11:
                if type(objects[11]) is NoObject:
                    enemy = Spider()
                    objects[10] = enemy
                idx = 10
            if ram_state[84]:
                if type(objects[idx+1]) is NoObject:
                    objects[idx+1] = type(enemy)()
                if ram_state[84] & 1:
                    objects[idx+1].xy = x+16, y
                if ram_state[84] & 2:
                    objects[idx+1].xy = x+32, y
                if ram_state[84] & 4:
                    objects[idx+1].xy = x+64, y
            else:
                objects[idx+1] = NoObject()

            objects[idx].xy = x, y
        else:
            for i in range(1, 13):
                objects[i] = NoObject()

    if room < 16 or ram_state[65] & 128:
        if room == 0:
            if ram_state[26] != 117:
                if type(beam0) is NoObject:
                    beam0 = Beam()
                    objects[15] = beam0
                    beam1 = Beam()
                    beam1.xy = 120, 53
                    objects[16] = beam1
                    beam2 = Beam()
                    beam2.xy = 112, 53
                    objects[17] = beam2
                    beam3 = Beam()
                    beam3.xy = 44, 53
                    objects[18] = beam3
                    beam4 = Beam()
                    beam4.xy = 36, 53
                    objects[19] = beam4
                    beam5 = Beam()
                    beam5.xy = 16, 53
                    objects[20] = beam5
            else:
                for i in range(6):
                    objects[15+i] = NoObject()

            if type(objects[25]) is NoObject or objects[25].xywh != (0, 53, 4, 42):
                for i in range(1, 53):
                    objects[i] = NoObject()
                objects[25] = Wall(x=0, y=53, w=4, h=42, rgb=(101, 111, 228))
                objects[29] = Ladder(x=72, y=94, w=16, h=102)
                objects[32] = Platform(x=4, y=94, w=154, h=1)

        elif room == 1:
            if type(objects[23]) is NoObject:
                for i in range(1, 53):
                    objects[i] = NoObject()
                objects[23] = Rope()

                objects[25] = Wall(x=0, y=96, w=8, h=40)
                objects[26] = Wall(x=0, y=136, w=16, h=45)
                objects[27] = Wall(x=152, y=96, w=8, h=40)
                objects[28] = Wall(x=144, y=136, w=16, h=45)

                objects[29] = Ladder(x=72, y=93, w=16, h=42)
                objects[30] = Ladder(x=16, y=136, w=16, h=45)
                objects[31] = Ladder(x=128, y=136, w=16, h=45)

                objects[32] = Platform(x=0, y=93, w=56, h=2)
                objects[33] = Platform(x=104, y=93, w=56, h=2)
                objects[34] = Platform(x=68, y=93, w=23, h=2)
                objects[35] = Platform(x=76, y=136, w=8, h=5)
                objects[36] = Platform(x=8, y=136, w=28, h=2)
                objects[37] = Platform(x=124, y=136, w=28, h=2)
                objects[38] = Platform(x=16, y=180, w=128, h=1)

                objects[51] = Conveyer_Belt(x=60, y=136, w=15, h=5)
                objects[52] = Conveyer_Belt(x=85, y=136, w=15, h=5)
            # skull
            if ram_state[67] & 2:
                if type(objects[8]) is NoObject:
                    objects[8] = Skull()
                objects[8].xy = ram_state[47] + 32, 406 - \
                    ram_state[46]  # ram_state[46] - 74 # 240 -> 166
            else:
                objects[8] = NoObject()

            # barrier
            if ram_state[26] != 117:
                if type(objects[13]) is NoObject:
                    objects[13] = Barrier()
            else:
                objects[13] = NoObject()

            if ram_state[28] != 117:
                if type(objects[14]) is NoObject:
                    barrier2 = Barrier()
                    _, y = barrier2.xy
                    barrier2.xy = 136, y
                    objects[14] = barrier2
            else:
                objects[14] = NoObject()

        elif room == 2:
            if type(objects[25]) is NoObject or objects[25].xy != (156, 52):
                for i in range(1, 53):
                    objects[i] = NoObject()
                objects[25] = Wall(x=156, y=52, w=4, h=42)
                objects[29] = Ladder(x=72, y=93, w=16, h=102)
                objects[32] = Platform(x=4, y=93, w=154, h=1)

        elif room == 3:
            if type(objects[25]) is NoObject or objects[25].xywh != (0, 53, 4, 41):
                for i in range(1, 53):
                    objects[i] = NoObject()
                objects[25] = Wall(x=0, y=53, w=4, h=41)
                objects[29] = Ladder(x=72, y=93, w=16, h=102)
                objects[32] = Platform(x=4, y=93, w=154, h=1)

        elif room == 4:
            if type(objects[29]) is NoObject or type(objects[30]) is NoObject:
                for i in range(1, 53):
                    objects[i] = NoObject()
                objects[29] = Ladder(x=72, y=52, w=16, h=39)
                objects[30] = Ladder(x=72, y=93, w=16, h=102)
                objects[32] = Platform(x=4, y=93, w=154, h=1)

        elif room == 5:
            if type(objects[23]) is NoObject or objects[23].xy != (41, 97):
                for i in range(1, 53):
                    objects[i] = NoObject()
                # rope
                rope = Rope()
                rope.rgb = 236, 236, 236
                rope.xy = 41, 97
                rope.wh = 1, 24
                objects[23] = rope
                objects[24] = Rope(x=125, y=95, w=2, h=52)

                objects[25] = Wall(x=32, y=53, w=4, h=40)
                objects[26] = Wall(x=124, y=53, w=4, h=40)
                objects[27] = Wall(x=0, y=96, w=4, h=77)
                objects[28] = Wall(x=156, y=96, w=4, h=77)

                objects[29] = Ladder(x=72, y=171, w=16, h=26)

                objects[32] = Platform(x=0, y=93, w=48, h=2)
                objects[33] = Platform(x=112, y=93, w=48, h=2)
                objects[34] = Platform(x=48, y=130, w=64, h=3)
                objects[35] = Platform(x=4, y=171, w=154, h=1)
                objects[36] = Platform(x=76, y=93, w=8, h=5)
                objects[51] = Conveyer_Belt(x=60, y=93, w=15, h=5)
                objects[52] = Conveyer_Belt(x=85, y=93, w=15, h=5)

            # skull
            if ram_state[69] & 2:
                if type(objects[8]) is NoObject:
                    objects[8] = Skull()
                objects[8].xy = ram_state[47] + 33, 103 + (255 - ram_state[46])
            else:
                objects[8] = NoObject()

            # barrier
            if ram_state[26] != 117:
                if type(objects[13]) is NoObject:
                    objects[13] = Barrier()
                objects[13].xy = 56, 135
                objects[13].rgb = 66, 158, 130
            else:
                objects[13] = NoObject()

            if ram_state[28] != 117:
                if type(objects[14]) is NoObject:
                    objects[14] = Barrier()
                objects[14].xy = 100, 135
                objects[14].rgb = 66, 158, 130
            else:
                objects[14] = NoObject()

        elif room == 6:
            if type(objects[29]) is NoObject or objects[29].xy != (72, 53):
                for i in range(1, 53):
                    objects[i] = NoObject()
                objects[29] = Ladder(x=72, y=53, w=16, h=38)
                objects[32] = Platform(x=0, y=93, w=160, h=1)

        elif room == 7:
            if type(objects[25]) is NoObject or objects[25].xy != (156, 53):
                for i in range(1, 53):
                    objects[i] = NoObject()
                objects[25] = Wall(x=156, y=53, w=4, h=42, rgb=(101, 111, 228))
                objects[29] = Ladder(x=72, y=94, w=16, h=102)
                objects[32] = Platform(x=4, y=94, w=154, h=1)

            # beam
            if ram_state[26] != 117:
                if type(objects[15]) is NoObject:
                    beam0 = Beam()
                    objects[15] = beam0
                    beam1 = Beam()
                    beam1.xy = 120, 53
                    objects[16] = beam1
                    beam2 = Beam()
                    beam2.xy = 112, 53
                    objects[17] = beam2
                    beam3 = Beam()
                    beam3.xy = 44, 53
                    objects[18] = beam3
                    beam4 = Beam()
                    beam4.xy = 36, 53
                    objects[19] = beam4
                    beam5 = Beam()
                    beam5.xy = 16, 53
                    objects[20] = beam5
            else:
                for i in range(6):
                    objects[15+i] = NoObject()

        elif room == 8:

            if type(objects[23]) is NoObject or objects[23].wh != (1, 51):
                for i in range(1, 53):
                    objects[i] = NoObject()
            # rope
                rope = Rope()
                rope.xy = 80, 96
                rope.wh = 1, 51
                objects[23] = Rope()

                objects[25] = Wall(x=0, y=53, w=4, h=121)
                objects[26] = Wall(x=156, y=97, w=4, h=77)

                objects[32] = Platform(4, 143, 12, 4)
                objects[33] = Platform(144, 143, 12, 4)

                objects[34] = Platform(4, 93, 43, 3)
                objects[35] = Platform(76, 93, 8, 3)
                objects[36] = Platform(112, 93, 48, 3)
                objects[37] = Platform(4, 173, 152, 1)

            if ram_state[34] != 144:
                if type(ram_state[36]) is NoObject:
                    objects[39] = Disappearing_Platform(4, 103, 12, 4)
                    objects[40] = Disappearing_Platform(4, 113, 12, 4)
                    objects[41] = Disappearing_Platform(4, 123, 12, 4)
                    objects[42] = Disappearing_Platform(4, 133, 12, 4)

                    objects[43] = Disappearing_Platform(4, 153, 12, 4)
                    objects[44] = Disappearing_Platform(4, 163, 12, 4)

                    objects[45] = Disappearing_Platform(144, 103, 12, 4)
                    objects[46] = Disappearing_Platform(144, 113, 12, 4)
                    objects[47] = Disappearing_Platform(144, 123, 12, 4)
                    objects[48] = Disappearing_Platform(144, 133, 12, 4)

                    objects[49] = Disappearing_Platform(144, 153, 12, 4)
                    objects[50] = Disappearing_Platform(144, 163, 12, 4)
            else:
                for i in range(36, 48):
                    objects[i] = NoObject()

        elif room == 9:
            if type(objects[25]) is NoObject or objects[25].xy != (156, 52):
                for i in range(1, 53):
                    objects[i] = NoObject()
                objects[25] = Wall(x=156, y=52, w=3, h=41)
                objects[29] = Ladder(x=72, y=53, w=16, h=38)
                objects[32] = Platform(x=0, y=93, w=158, h=1)

        elif room == 10:
            if type(objects[25]) is NoObject or objects[25].xy != (0, 53):
                for i in range(1, 53):
                    objects[i] = NoObject()
                objects[25] = Wall(x=0, y=53, w=3, h=40)
                objects[29] = Ladder(x=72, y=53, w=16, h=38)
                objects[32] = Platform(x=0, y=93, w=36, h=1)
                objects[33] = Platform(x=124, y=93, w=36, h=1)
            if ram_state[34] != 232:
                objects[39] = Disappearing_Platform(x=36, y=93, w=88, h=7)
            else:
                objects[39] = NoObject()

        elif room == 11:
            if type(objects[29]) is NoObject or type(objects[30]) is NoObject or objects[30].xy != (72, 93):
                for i in range(1, 53):
                    objects[i] = NoObject()
                objects[29] = Ladder(x=72, y=52, w=16, h=39)
                objects[30] = Ladder(x=72, y=93, w=16, h=102)
                objects[32] = Platform(x=0, y=93, w=160, h=1)

        elif room == 12:
            if type(objects[38]) is NoObject or objects[38].xy != (0, 94):
                for i in range(1, 53):
                    objects[i] = NoObject()
                objects[38] = Platform(x=0, y=94, w=160, h=1)

            # beam
            if ram_state[26] != 117:
                if type(objects[15]) is NoObject:
                    beam0 = Beam()
                    beam0.xy = 120, 53
                    objects[15] = beam0
                    beam1 = Beam()
                    beam1.xy = 112, 53
                    objects[16] = beam1
                    beam2 = Beam()
                    beam2.xy = 96, 53
                    objects[17] = beam2
                    beam3 = Beam()
                    beam3.xy = 88, 53
                    objects[18] = beam3
                    beam4 = Beam()
                    beam4.xy = 68, 53
                    objects[19] = beam4
                    beam5 = Beam()
                    beam5.xy = 60, 53
                    objects[20] = beam5
                    beam6 = Beam()
                    beam6.xy = 44, 53
                    objects[21] = beam6
                    beam7 = Beam()
                    beam7.xy = 36, 53
                    objects[22] = beam7
            else:
                for i in range(15, 23):
                    objects[i] = NoObject()

        elif room == 13:
            if type(objects[29]) is NoObject or type(objects[30]) is NoObject or objects[30].xy != (72, 93):
                for i in range(1, 53):
                    objects[i] = NoObject()
                objects[29] = Ladder(x=72, y=52, w=16, h=39)
                objects[30] = Ladder(x=72, y=93, w=16, h=102)
                objects[32] = Platform(x=0, y=93, w=160, h=1)

        elif room == 14:
            if type(objects[23]) is NoObject or type(objects[24]) is NoObject or objects[23].xy != (71, 96):
                for i in range(1, 53):
                    objects[i] = NoObject()
                # rope
                objects[23] = Rope(x=71, y=96, w=1, h=48)
                objects[24] = Rope(x=87, y=97, w=2, h=33)

                objects[29] = Ladder(72, 169, 16, 25)

                objects[32] = Platform(0, 93, 40, 3)
                objects[33] = Platform(68, 93, 24, 3)
                objects[34] = Platform(120, 93, 40, 3)
                objects[35] = Platform(16, 168, 128, 1)
                objects[36] = Platform(x=0, y=97, w=16, h=73)
                objects[37] = Platform(x=144, y=97, w=16, h=73)

        elif room == 15:
            if type(objects[38]) is NoObject or objects[38].xy != (0, 94):
                for i in range(1, 53):
                    objects[i] = NoObject()
                objects[38] = Platform(x=0, y=94, w=160, h=1)

        elif room == 16:
            if type(objects[38]) is NoObject or objects[38].xy != (0, 93):
                for i in range(1, 53):
                    objects[i] = NoObject()
                objects[38] = Platform(x=0, y=93, w=160, h=1)

        elif room == 17:
            if type(objects[38]) is NoObject or objects[38].xy != (0, 94):
                for i in range(1, 53):
                    objects[i] = NoObject()
                objects[38] = Platform(x=0, y=94, w=160, h=1)

            # barrier
            if ram_state[26] != 117:
                if type(objects[13]) is NoObject:
                    objects[13] = Barrier()
            else:
                objects[6] = NoObject()

            if ram_state[28] != 117:
                if type(objects[14]) is NoObject:
                    objects[14] = Barrier()
                    _, y = objects[14].xy
                    objects[14].xy = 136, y
            else:
                objects[14] = NoObject()

        elif room == 18:
            if type(objects[33]) is NoObject or objects[33].xy != (124, 94) or type(objects[25]) is not NoObject:
                for i in range(1, 53):
                    objects[i] = NoObject()
                objects[32] = Platform(x=0, y=94, w=36, h=1)
                objects[33] = Platform(x=124, y=94, w=36, h=1)

            # skull
            if ram_state[76] & 32:
                if type(objects[8]) is NoObject():
                    objects[8] = Skull()
                objects[8].xy = ram_state[47] - 1, ram_state[46] - 147
            else:
                objects[8] = NoObject()

            if ram_state[34] != 232:
                objects[39] = Disappearing_Platform(x=36, y=94, w=88, h=7)
            else:
                objects[39] = NoObject()

        elif room == 19:
            if type(objects[29]) is NoObject or type(objects[30]) is not NoObject:
                for i in range(1, 53):
                    objects[i] = NoObject()
                objects[29] = Ladder(x=72, y=53, w=16, h=38)
                objects[32] = Platform(x=0, y=93, w=160, h=1)

        elif room == 20:
            if type(objects[33]) is NoObject or objects[33].xy != (124, 94) or type(objects[25]) is NoObject:
                for i in range(1, 53):
                    objects[i] = NoObject()
                objects[29] = Wall(x=156, y=52, w=3, h=42)
                objects[32] = Platform(x=0, y=94, w=36, h=1)
                objects[33] = Platform(x=124, y=94, w=32, h=1)

            if ram_state[34] != 232:
                objects[39] = Disappearing_Platform(x=36, y=94, w=88, h=7)
            else:
                objects[39] = NoObject()

        elif room == 21:
            if type(objects[29]) is NoObject or type(objects[30]) is not NoObject or type(objects[25]) is NoObject:
                for i in range(1, 53):
                    objects[i] = NoObject()
                objects[25] = Wall(x=0, y=53, w=3, h=40)
                objects[29] = Ladder(x=72, y=53, w=16, h=38)
                objects[32] = Platform(x=0, y=93, w=158, h=1)

        elif room == 22:
            if type(objects[33]) is NoObject or objects[33].xy != (124, 94) or type(objects[29]) is NoObject:
                for i in range(1, 53):
                    objects[i] = NoObject()
                objects[29] = Ladder(x=72, y=53, w=16, h=38)
                objects[32] = Platform(x=0, y=93, w=36, h=1)
                objects[33] = Platform(x=124, y=93, w=36, h=1)

            if ram_state[34] != 232:
                objects[39] = Disappearing_Platform(x=36, y=93, w=88, h=7)
            else:
                objects[39] = NoObject()

        elif room == 23:
            if type(objects[37]) is NoObject or objects[37].xy != (0, 93) or type(objects[25]) is NoObject:
                for i in range(1, 53):
                    objects[i] = NoObject()
                objects[25] = Wall(x=156, y=53, w=3, h=40)
                objects[37] = Platform(x=0, y=93, w=158, h=1)

    else:
        if room == 16:
            if type(objects[32]) is not NoObject or type(objects[37]) is not NoObject or type(objects[38]) is not NoObject:
                for i in range(1, 53):
                    objects[i] = NoObject()

        elif room == 17:
            if type(objects[32]) is not NoObject or type(objects[37]) is not NoObject or type(objects[38]) is not NoObject:
                for i in range(1, 53):
                    objects[i] = NoObject()

        elif room == 18:
            if type(objects[32]) is not NoObject or type(objects[37]) is not NoObject or type(objects[38]) is not NoObject:
                for i in range(1, 53):
                    objects[i] = NoObject()
            # skull
            if ram_state[76] & 32:
                if type(objects[8]) is NoObject:
                    objects[8] = Skull()
                objects[8].xy = ram_state[47] - 1, ram_state[46] - 147
            else:
                objects[8] = NoObject()

            if ram_state[34] != 214:
                objects[39] = Disappearing_Platform(x=36, y=94, w=88, h=7)
            else:
                objects[39] = NoObject()

        elif room == 19:
            if type(objects[32]) is not NoObject or type(objects[37]) is not NoObject or type(objects[38]) is not NoObject:
                for i in range(1, 53):
                    objects[i] = NoObject()

        elif room == 20:
            if type(objects[32]) is not NoObject or type(objects[37]) is not NoObject or type(objects[38]) is not NoObject:
                for i in range(1, 53):
                    objects[i] = NoObject()
            if ram_state[34] != 214:
                objects[39] = Disappearing_Platform(x=36, y=94, w=88, h=7)
            else:
                objects[39] = NoObject()

        elif room == 21:
            if type(objects[32]) is not NoObject or type(objects[37]) is not NoObject or type(objects[38]) is not NoObject:
                for i in range(1, 53):
                    objects[i] = NoObject()

        elif room == 22:
            if type(objects[32]) is not NoObject or type(objects[37]) is not NoObject or type(objects[38]) is not NoObject:
                for i in range(1, 53):
                    objects[i] = NoObject()
            if ram_state[34] != 214:
                objects[39] = Disappearing_Platform(x=36, y=93, w=88, h=7)
            else:
                objects[39] = NoObject()

        elif room == 23:
            if type(objects[32]) is not NoObject or type(objects[37]) is not NoObject or type(objects[38]) is not NoObject:
                for i in range(1, 53):
                    objects[i] = NoObject()

    x = 56
    y = 28

    torch_h = objects[58]

    sword1_h, sword2_h = objects[59], objects[60]

    key1_h, key2_h, key3_h, key4_h = objects[53], objects[54], objects[55], objects[56]

    amulet_h = objects[57]

    if ram_state[65] & 128:
        if type(objects[58]) is NoObject:
            objects[58] = Torch_HUD()
        x = x + 8
    else:
        objects[58] = NoObject()

    if ram_state[65] & 64:
        if type(objects[59]) is NoObject:
            objects[59] = Sword_HUD()
        objects[59].xy = x, y
        x = x + 8
    else:
        objects[59] = NoObject()

    if ram_state[65] & 32:
        if type(objects[60]) is NoObject:
            objects[60] = Sword_HUD()
        objects[60].xy = x, y
        x = x + 8
    else:
        objects[60] = NoObject()

    if ram_state[65] & 16:
        if type(objects[53]) is NoObject:
            objects[53] = Key_HUD()
        objects[53].xy = x, y
        x = x + 8
    else:
        objects[53] = NoObject()

    if ram_state[65] & 8:
        if type(objects[54]) is NoObject:
            objects[54] = Key_HUD()
        objects[54].xy = x, y
        x = x + 8
    else:
        objects[54] = NoObject()

    if ram_state[65] & 4:
        if type(objects[55]) is NoObject:
            objects[55] = Key_HUD()
        objects[55].xy = x, y
        x = x + 8
    else:
        objects[55] = NoObject()

    if ram_state[65] & 2 and x < 104:
        if type(objects[56]) is NoObject:
            objects[56] = Key_HUD()
        objects[56].xy = x, y
        x = x + 8
    else:
        objects[56] = NoObject()

    if ram_state[65] & 1 and x < 104:
        if type(objects[57]) is NoObject:
            objects[57] = Amulet_HUD()
        objects[57].xy = x, y
    else:
        objects[57] = NoObject()

    if hud:
        for i in range(11):
            objects[i+46] = NoObject()

        # life
        if ram_state[58]:
            if type(objects[61]) is NoObject:
                objects[61] = Life()
            objects[61].wh = 7 + ((ram_state[58]-1) * 8), 5
            objects[61].value = ram_state[58]
        else:
            objects[61] = NoObject()
            objects[61].value = 0

        # score
        scr = 0
        value = 0
        for i in range(3):
            if ram_state[19+i] > 15:
                scr = 5-2*i
                break
            elif ram_state[19+i] > 0:
                scr = 4-2*i
                break

        objects[62].xywh = 97 - (scr * 8), 6, 5 + (scr * 8), 8
        objects[62].value = _convert_number(ram_state[19]) * 10000 + _convert_number(ram_state[20]) * 100 +\
            _convert_number(ram_state[21])

    return objects


def _detect_objects_montezumarevenge_raw(info, ram_state):
    pass
