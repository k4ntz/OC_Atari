from .game_objects import GameObject, ValueObject
from ._helper_methods import _convert_number
import sys

MAX_NB_OBJECTS = {"Player": 1, "Oxygen_Boat": 1, "Oxygen_Pipe": 1,
                  "Shark": 1, "Treasure": 1, "Octopus": 1, "Tentacle": 360}
MAX_NB_OBJECTS_HUD = {"Player": 1, "Oxygen_Boat": 1, "Oxygen_Pipe": 1, "Shark": 1,
                      "Treasure": 1, "Octopus": 1, "Tentacle": 360, "Score": 1, "Timer": 1, "Oxygen_Meter": 1}


class Player(GameObject):
    """
    Scubadiver protecting the treasure, by hitting the shark and the octopus tentacles
    """

    def __init__(self):
        super(Player, self).__init__()
        self._xy = 76, 139
        self.wh = (16, 13)
        self.rgb = 92, 186, 92
        self.hud = False


class Shot(GameObject):
    """
    Projectile shot by player
    """

    def __init__(self):
        super(Shot, self).__init__()
        self._xy = 76, 35
        self.wh = (1, 2)
        self.rgb = 170, 170, 170
        self.hud = False


class Oxygen_Boat(GameObject):
    """
    Boate lowering a pipe with oxygen from time to time
    """

    def __init__(self):
        super(Oxygen_Boat, self).__init__()
        self._xy = 76, 9
        self.wh = (16, 14)
        self.rgb = 184, 70, 162
        self.hud = False


class Oxygen_Pipe(GameObject):
    """
    Boate lowering a pipe with oxygen from time to time
    """

    def __init__(self):
        super(Oxygen_Pipe, self).__init__()
        self._xy = 76, 23
        self.wh = (1, 123)
        self.rgb = 170, 170, 170
        self.hud = False


class Shark(GameObject):
    """
    Shark trying to kill the player
    """

    def __init__(self):
        super(Shark, self).__init__()
        self._xy = 76, 35
        self.wh = (16, 12)
        self.rgb = 170, 170, 170
        self.hud = False


class Treasure(GameObject):
    """
    Treasure to be protected. Represents the remaining lives
    """

    def __init__(self):
        super(Treasure, self).__init__()
        self._xy = 72, 163
        self.wh = (16, 6)
        self.rgb = 195, 144, 61
        self.hud = False
        self.value = 3


class Octopus(GameObject):
    """
    Octopus trying to steal the treasure
    """

    def __init__(self):
        super(Octopus, self).__init__()
        self._xy = 20, 29
        self.wh = (120, 33)
        self.rgb = 0, 0, 0
        self.hud = False


class Tentacle(GameObject):
    """
    Tentacles of the octopus
    """

    def __init__(self, x=0, y=0, *args, **kwargs):
        super(Tentacle, self).__init__()
        self._xy = x, y
        self.wh = (4, 6)
        self.rgb = 0, 0, 0
        self.hud = False


class Score(GameObject):
    """
    Score of the game. Increases by hitting the shark or the tentacles
    """

    def __init__(self):
        super(Score, self).__init__()
        self._xy = 0, 0
        self.wh = (0, 0)
        self.rgb = 236, 236, 236
        self.hud = True


class Timer(GameObject):
    """
    Remaining time until the next phase
    """

    def __init__(self):
        super(Timer, self).__init__()
        self._xy = 0, 0
        self.wh = (0, 0)
        self.rgb = 50, 132, 50
        self.hud = True


class Oxygen_Meter(GameObject):
    """
    Remaining Oxygen of the diver. Can be replenished by alighning with the oxygen pipe of the boat
    """

    def __init__(self):
        super(Oxygen_Meter, self).__init__()
        self._xy = 16, 179
        self.wh = (128, 12)
        self.rgb = 198, 108, 58
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
    objects = [Player(), Oxygen_Boat(), Oxygen_Pipe(),
               Shark(), Octopus(), Treasure()]

    objects.extend([None] * 361)

    if hud:
        objects.extend([Score(), Timer(), Oxygen_Meter()])
        # objects.extend([None] * 13)
    return objects


def _detect_objects_ram(objects, ram_state, hud=False):
    """
    For all 3 objects:
    (x, y, w, h, r, g, b)
    """

    # if ram_state[61]&128 -> orientation right

    # player moving x + 1
    objects[0].xy = ram_state[99]-1, 139
    # Boat
    objects[1].xy = ram_state[100]-1, 9

    # Oxygen pipe present if ram[117] != 0
    if ram_state[117]:
        if objects[2] is None:
            objects[2] = Oxygen_Pipe()
        objects[2].xy = ram_state[100]+6, 23
    else:
        objects[2] = None

    # Shark y always + 15 per state
    y = 7
    for i in range(7):
        if ram_state[59-i]:
            y = i
            break
    if y == 7:
        objects[3].xy = objects[0].xy
        objects[0].xy = ram_state[99]+3, 147
        objects[0].wh = 11, 11
    else:
        objects[3].xy = ram_state[60]-1, 35+(y*14)
        objects[0].wh = 16, 13

    # ram[71] == remaining treasure
    try:
        if ram_state[71] % 4 == 3:
            objects[5].xy = 72, 163
            objects[5].wh = 16, 6
            objects[5].value = 3

        elif ram_state[71] % 4 == 2:
            objects[5].xy = 74, 165
            objects[5].wh = 10, 4
            objects[5].value = 2

        elif ram_state[71] % 4 == 1:
            objects[5].xy = 78, 167
            objects[5].wh = 4, 2
            objects[5].value = 1

        else:
            objects[5] = None
    except:
        objects[5] = Treasure()

    # ram[51], ram[50] == shot x, y
    # 80 == 122, 23 == 54
    if ram_state[50]:
        if objects[6] is None:
            objects[6] = Shot()
        objects[6].xy = ram_state[51] - \
            2, ((ram_state[50]) + 30) + \
            (ram_state[50] >> 5) + (ram_state[50] >> 3)
    else:
        objects[6] = None

    # ram[0-49] octopus-tentacles bitrepresentation. Colum wise ram[0] has highest y and ram[9] lowest y,ram[10-19] is the second colum
    # 128 most left, 1 most right in colum -> ram[0] == 128 -> xywh == 16, 126, 4, 6

    # ram 10 == 128 -> x == 76, ram 10 == 1 -> x = 48
    # ram 20 == 128 -> x == 92, ram 20 == 1 -> no block => ram 10 == 16 -> x = 80 (only 4 blocks this colum)
    # ram 30 == 128 -> x == 96, ram 30 == 1 -> x = 124
    # ram 40 == 128 -> x == 156, ram 40 == 1 -> x = 128

    base_x = 16
    # bit read direction starting from msb
    msb = True
    base_list = 7
    for i in range(5):
        base_state = i*10
        for j in range(10):
            y = 126 - (7*j)
            if i == 2:
                msb == True
                for b in range(4):
                    if ram_state[base_state+j] & (2**(b+4)):
                        objects[base_list + j*4 +
                                b] = Tentacle(base_x+(4*b), y)
                    else:
                        objects[base_list + j*4 + b] = None
            else:
                for b in range(8):
                    if msb:
                        if ram_state[base_state+j] & (2**(7-b)):
                            objects[base_list + j*8 +
                                    b] = Tentacle(base_x+(4*b), y)
                        else:
                            objects[base_list + j*8 + b] = None
                    else:
                        if ram_state[base_state+j] & (2**(b)):
                            objects[base_list + j*8 +
                                    b] = Tentacle(base_x+(4*b), y)
                        else:
                            objects[base_list + j*8 + b] = None

        if i == 2:
            base_list += 40
            base_x += 16
        else:
            msb = not msb
            base_list += 80
            base_x += 32

    if hud:
        # x diff 8 pixels
        if ram_state[65] > 6:
            x, y, w, h = 97, 181, 5, 8
            if ram_state[68] > 15:
                x, w = 57, 45
            elif ram_state[68]:
                x, w = 65, 37
            elif ram_state[69] > 15:
                x, w = 73, 29
            elif ram_state[69]:
                x, w = 81, 21
            elif ram_state[70] > 15:
                x, w = 90, 13

            objects[-3].xy = x, y
            objects[-3].wh = w, h

            if ram_state[114]:
                x, y, w, h = 16, 175, 128, 4
                for i in range(8):
                    if ram_state[114] & 2**(7-i):
                        break
                    else:
                        x += 4
                        w -= 8
                objects[-2].xy = x, y
                objects[-2].wh = w, h
            else:
                x, y, w, h = 48, 175, 64, 4
                for i in range(8):
                    if ram_state[115] & 2**(i):
                        break
                    else:
                        x += 4
                        w -= 8
                objects[-2].xy = x, y
                objects[-2].wh = w, h

        # ram[112-113] oxygen bar blocks according to bit representation
        # x == 16 y == 179, w = 4 pro block, h == 12
        if ram_state[112]:
            x, y, w, h = 16, 179, 128, 12
            for i in range(8):
                if ram_state[112] & 2**(7-i):
                    break
                else:
                    x += 4
                    w -= 8
            objects[-1].xy = x, y
            objects[-1].wh = w, h
        else:
            x, y, w, h = 48, 179, 64, 12
            for i in range(8):
                if ram_state[113] & 2**(i):
                    break
                else:
                    x += 4
                    w -= 8
            objects[-1].xy = x, y
            objects[-1].wh = w, h
