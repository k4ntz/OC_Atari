from dataclasses import dataclass

from ._helper_methods import number_to_bitfield, _convert_number
from .game_objects import GameObject, ValueObject, NoObject, Orientation, OrientedObject
from ..vision.game_objects import NoObject as v_No
from .utils import match_objects
import sys
from math import ceil

"""
RAM extraction for the game Chopper Command.
"""

MAX_NB_OBJECTS = {'Player': 1, 'Shot': 1, 'Truck': 3, 'EnemyPlane': 3, 'EnemyHelicopter': 3, 'Bomb': 2,
                  'MiniPlayer': 1, 'MiniTruck': 9, 'MiniEnemy': 12}
MAX_NB_OBJECTS_HUD = {'Player': 1, 'Shot': 1, 'Truck': 3, 'EnemyPlane': 3, 'EnemyHelicopter': 3, 'Bomb': 2,
                      'MiniPlayer': 1, 'MiniTruck': 9, 'MiniEnemy': 12, 'Score': 4, 'Life': 2}


class Player(OrientedObject):
    """
    The player figure i.e., the helicopter gunship.
    """

    def __init__(self):
        super(Player, self).__init__()
        self._xy = 133, 103  # initially
        self.wh = 16, 9
        self.orientation = Orientation.E
        self.rgb = 223, 183, 85
        self.hud = False


class MiniPlayer(GameObject):
    """
    The blip for the player's helicopter on the Long Range Scanner.
    """

    def __init__(self):
        super(MiniPlayer, self).__init__()
        self._xy = 133, 103  # initially
        self.wh = 2, 2
        self.rgb = 124, 44, 0
        self.hud = False


class Truck(GameObject):
    """
    The trucks of the convoy, which need to be protected.
    """

    def __init__(self, x=0, y=0, w=8, h=7):
        super(Truck, self).__init__()
        self._xy = x, y
        self.wh = w, h
        self.rgb = 0, 0, 0
        self.hud = False


class MiniTruck(GameObject):
    """
    The blips for the trucks on the Long Range Scanner.
    """

    def __init__(self, x=0, y=0, w=1, h=2):
        super(MiniTruck, self).__init__()
        self._xy = x, y  # initially
        self.wh = w, h
        self.rgb = 236, 200, 96
        self.hud = False


class EnemyHelicopter(GameObject):
    """
    The enemy helicopters.
    """

    def __init__(self):
        super(EnemyHelicopter, self).__init__()
        self._xy = 0, 0  # random
        self.wh = 8, 9
        self.rgb = 236, 236, 236
        self.hud = False


class EnemyPlane(GameObject):
    """
    The enemy planes.
    """

    def __init__(self):
        super(EnemyPlane, self).__init__()
        self._xy = 0, 0  # random
        self.wh = 8, 6
        self.rgb = 0, 0, 148
        self.hud = False


class MiniEnemy(GameObject):
    """
    The blips for the enemy aircraft on the Long Range Scanner.
    """

    def __init__(self, x=0, y=0, w=2, h=2):
        super(MiniEnemy, self).__init__()
        self._xy = x, y  # initially
        self.wh = w, h
        self.rgb = 236, 200, 96
        self.hud = False


class Bomb(GameObject):
    """
    The multi-warhead missiles deployed by enemy aircraft.
    """

    def __init__(self):
        super(Bomb, self).__init__()
        self._xy = 0, 0  # random
        self.wh = 2, 2          # oder 2,1 wenn gesplittet
        self.rgb = 223, 183, 85
        self.hud = False


class Shot(GameObject):
    """
    The projectiles shot from the helicopter's laser cannon.
    """

    def __init__(self):
        super(Shot, self).__init__()
        self._xy = 0, 0
        self.wh = 0, 1
        self.rgb = 0, 0, 100
        self.hud = False


class Score(ValueObject):
    """
    The player's score display (HUD).
    """

    def __init__(self):
        super(Score, self).__init__()
        self._xy = 75, 16
        self.wh = 6, 7
        self.rgb = 223, 183, 85
        self.hud = True


class Life(ValueObject):
    """
    The indicator for helicopter rerves (lifes) (HUD).
    """

    def __init__(self):
        super(Life, self).__init__()
        self._xy = 33, 24           # and 41, 24 and so on
        self.wh = 8, 9
        self.rgb = 223, 183, 85
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


def _init_objects_ram(hud):
    """
    (Re)Initialize the objects
    """
    objects = [Player()]
    objects.extend([NoObject()] * 12)
    objects.extend([MiniPlayer()])
    objects.extend([NoObject()] * 21)
    if hud:
        objects.extend([Score(), Life()])

    return objects


def _detect_objects_ram(objects, ram_state, hud):

    # player
    player = objects[0]
    if ram_state[97]:
        player.xy = (ram_state[71] + 2, 159-ram_state[72])
    else:
        player.xy = (ram_state[71], 159-ram_state[72])
    player.orientation = Orientation.E if ram_state[66] else Orientation.W
    print(player.orientation)

    # mini_player
    objects[13].xy = 74+(ram_state[71]>>5), 184-((ram_state[72]>>4)&7)

    if ram_state[2] != 240:
        if -1 <= ram_state[94] - ram_state[95] <= 1:
            bomb = objects[11]
            if type(bomb) is NoObject:
                bomb = Bomb()
            bomb.xy = ram_state[70] - 1, 167 - ram_state[2]
            bomb.wh = 2, 2
            objects[11] = bomb 
            objects[12] = NoObject()
        else:
            if ram_state[94] != 240:
                bomb = objects[11]
                if type(bomb) is NoObject:
                    bomb = Bomb()
                bomb.xy = ram_state[70] + 1, 167 - ram_state[94] + 2
                bomb.wh = 2, 1
                objects[11] = bomb 
            else:
                objects[11] = NoObject()
            if ram_state[95] != 240:
                bomb = objects[12]
                if type(bomb) is NoObject:
                    bomb = Bomb()
                bomb.xy = ram_state[70] + 1, 167 - ram_state[95] - 2
                bomb.wh = 2, 1
                objects[12] = bomb 
            else:
                objects[12] = NoObject()
    else:
        objects[11] = NoObject()
        objects[12] = NoObject()

    # mid_mid_group = number_to_bitfield(ram_state[7])[2:8]
    # [68] counts down and [67] counts 1 up after [68] reaching 0 and jumping to 159 (one frame width)
    # the first bit of [68] decides the x_position of the player being locked to a side
    # backplate = ram_state[68]+backplate_offset

    # truck
    # x~ram_state[7], behavior of the camera takes part => ram_state[66] and the movement of the trucks (maybe backplate
    # at ram_state[68])
    # b_truck = mid_mid_group[:3] # first 3
    # existence: ram_state[7]
    # truck_distance = 32
    # for i in b_truck:
    # if b_truck[i] == 1:
    # truck = Truck()
    # x = i*truck_distance+backplate
    # truck.xy = (x, 166)     # y is constant
    # objects.append(truck)

    trucks = []

    if ram_state[17]:
        x = ram_state[17]
        if ram_state[17] > 222:
            x = (x + 32)%255
            
        elif ram_state[17] > 160:
            x = (x + 64)%255

        trucks.append((x, 160, 8, 7))

        if ram_state[21]&2:
            trucks.append(((x + 32) % 255, 160, 8, 7))

        if ram_state[21]&4:
            trucks.append(((x + 64) % 255, 160, 8, 7))
    
    match_objects(objects, trucks, 2, 3, Truck)

    # mid-mid-mini_enemy: mid_mid_group[:-3]
    # last 3 bits decide the location given by its int representation
    # BUT also the backplates offset and the group offset influences that

    # mini_truck
    # groups dividing into left/middle/right
    # x~ram_state[6:9]  (6-8)
    # y is constant
    # existence: ram_state[6:9]

    # enemy
    # dividing into bot/mid/top
    # x~ram_state[18:21]
    # y~ram_state[22-24]
    # dying might be 30-32
    # existence: ram_state[18:21] and field limit

    for i in range(3):
        if ram_state[30+i] != 96 or ram_state[18+i] == 8:
            if (int(ram_state[18+i]) + int(ram_state[68])) < 160:
                x = ram_state[18+i] + ram_state[68]
            else:
                x = ram_state[18+i] - (160 - ram_state[68])
            if not ram_state[66]:
                x-=2

            if 5 < ram_state[34+i] < 8:
                if type(objects[5+i]) is NoObject:
                    objects[5+i] = EnemyPlane()
                    objects[8+i] = NoObject()
                objects[5+i].xy = x, 161 - ram_state[22+i]
            elif 7 < ram_state[34+i] < 12:
                if type(objects[8+i]) is NoObject:
                    objects[8+i] = EnemyHelicopter()
                    objects[5+i] = NoObject()
                objects[8+i].xy = x, 158 - ram_state[22+i]
            else:
                objects[5+i] = NoObject()
                objects[8+i] = NoObject()

        else:
            objects[5+i] = NoObject()
            objects[8+i] = NoObject()


    # mini_enemy
    # [10]-[12] divided in left/middle/right with encoding of 3 last bits for the upper
    # and 3 previous bits for the lower
    # [6]-[8] divided in left/middle/right with encoding of 3 last bits for the middle enemies
    # and 3 previous bits for mini_trucks
    # x~ram_state[6:9] and [10:13]
    # y could be constant
    # existence: ram_state[6:9] and [10:13]

    # bombs: 37-39, 70,73,74,94,95  but no idea what's going on there

    # shot
    # continuos 1-bit in 49,52,55,58,61,64 => new shot
    # in 45 might contain the color gradient
    # shot_lines = [ram_state[52], ram_state[55], ram_state[58], ram_state[61], ram_state[64]]
    # b_shot_line = number_to_bitfield(ram_state[49])
    shot_lines = [ram_state[52], ram_state[55],
                  ram_state[58], ram_state[61], ram_state[64]]
    b_shot_line = number_to_bitfield(ram_state[52])
    for i in range(6):
        del b_shot_line[2]
    i = 0
    for shot_line in shot_lines:
        b_shot_line.extend(number_to_bitfield(shot_line))

    for i in range(4):
        tmp = b_shot_line[10+i]
        b_shot_line[10+i] = b_shot_line[17-i]
        b_shot_line[17-i] = tmp
        tmp = b_shot_line[34+i]
        b_shot_line[34+i] = b_shot_line[41-i]
        b_shot_line[41-i] = tmp

    for i in range(4):
        del b_shot_line[22]

    # [0,0,0,0,1,1,0,0,0,0,1,1,1,1,1,0]

    b_shot_line.append(0)   # to see if there is a shot at the end
    x = 8
    w = 0

    for s in b_shot_line:
        if s:
            w = w + 4
        elif w > 0:
            if type(objects[1]) is NoObject:
                objects[1] = Shot()
            objects[1].xy = x-w, 210-ram_state[65]-43
            objects[1].wh = w, 1
            break
        x = x + 4
    else:
        objects[1] = NoObject()


    # RADAR

    truck_x = ram_state[68]//20

    trucks = []
    lane1 = []
    lane2 = []
    lane3 = []

    for i in range(4):
        
        x0 = 99 - (16*i) + (truck_x + 1) + ((ram_state[67]&1) * 8)

        truck_bits = (ram_state[5+i]&56)>>3
        if truck_bits == 3:
            truck_bits = 4
        elif truck_bits == 4:
            truck_bits = 3

        if truck_bits and 55 < x0 < 104:
            for b in range(3):
                if truck_bits&(2**(2-b)):
                    xb = x0+(2*b)
                    if xb > 103:
                        xb = (xb%104) + 56
                        trucks.append((xb, 185, 1, 2))
                    else:
                        trucks.append((xb, 185, 1, 2))

        x1 = 99 - (16*i) + ((ram_state[9+i]&56)>>3) + (truck_x - 3) + ((ram_state[67]&1) * 8)
        
        if ram_state[9+i]&56 and 55 < x1 < 104:
            lane1.append((x1, 183, 2, 2))

        x2 = 99 - (16*i) + (ram_state[5+i]&7) + (truck_x - 3) + ((ram_state[67]&1) * 8)

        if ram_state[5+i]&7 and 55 < x2 < 104:
            lane2.append((x2, 181, 2, 2))

        x3 = 99 - (16*i) + (ram_state[9+i]&7) + (truck_x - 3) + ((ram_state[67]&1) * 8)

        if ram_state[9+i]&7 and 55 < x3 < 104:
            lane3.append((x3, 179, 2, 2))

    match_objects(objects, trucks, 14, 9, MiniTruck)
    match_objects(objects, lane1, 23, 4, MiniEnemy)
    match_objects(objects, lane2, 27, 4, MiniEnemy)
    match_objects(objects, lane3, 31, 4, MiniEnemy)

    if hud:

        if ram_state[100] - 1:
            if type(objects[36]) is NoObject:
                objects[36] = Life()
            objects[36].wh = 8*(ram_state[100]-1), 9
        else:
            objects[36] = NoObject()
        # score
        w = 6


        if ram_state[108] > 15:
            w+= 5*8
        elif ram_state[108] > 0:
            w+= 4*8
        elif ram_state[110] > 15:
            w+= 3*8
        elif ram_state[110] > 0:
            w+= 2*8
        elif ram_state[112] > 15:
            w+= 8

        objects[35].xywh = 81-w, 16, w, 7
        objects[35].value = _convert_number(ram_state[108]) * 10000 + _convert_number(
            ram_state[110]) * 100 + _convert_number(ram_state[112])

    # score
    # x: value 35+i*8
    # y: value 16
    # value: computable by 33,108,110,112
    # 33: score update
    # 108: hundred- and ten-thousands
    # 110: thousands and hundreds
    # 112: tens and ones

    # Life 97, 100
    # x: value=33+i*8
    # y: value constant 24
    # existence given by 97

def get_ram_states(index, ram_state):
    result = list()
    for i in index:
        result.append(ram_state[i])
    return result


def _detect_objects_raw(info, ram_state):
    relevant_objects = list()
    relevant_objects.extend(ram_state[71:73])
    relevant_objects.extend(ram_state[42:44])
    relevant_objects.append(ram_state[66])
    relevant_objects.append(ram_state[97])
    relevant_objects.extend(ram_state[6:9])
    relevant_objects.extend(ram_state[10:13])
    relevant_objects.extend(ram_state[18:21])
    relevant_objects.extend(ram_state[23:25])
    relevant_objects.append(ram_state[68])
    relevant_objects.extend(ram_state[37:40])
    relevant_objects.append(ram_state[70])
    relevant_objects.extend(ram_state[73:75])
    relevant_objects.extend(ram_state[94:96])
    relevant_objects.append(ram_state[45])
    relevant_objects.append(ram_state[49])
    relevant_objects.append(ram_state[52])
    relevant_objects.append(ram_state[55])
    relevant_objects.append(ram_state[58])
    relevant_objects.append(ram_state[61])
    relevant_objects.append(ram_state[64])

    info["Player"] = get_ram_states((71, 72, 42, 43, 97, 66), ram_state)
    relevant_objects.extend(info["Player"])
    info["MiniPlayer"] = get_ram_states((71, 72), ram_state)
    relevant_objects.extend(info["Player"])
    info["Truck"] = get_ram_states((7, 66, 97), ram_state)
    relevant_objects.extend(info["Player"])
    info["MiniTruck"] = get_ram_states((6, 7, 8), ram_state)
    relevant_objects.extend(info["Player"])
    info["Enemy"] = get_ram_states((18, 19, 20, 23, 24, 68), ram_state)
    relevant_objects.extend(info["Player"])
    info["MiniEnemy"] = get_ram_states((6, 7, 8, 10, 11, 12), ram_state)
    relevant_objects.extend(info["Player"])
    info["Bomb"] = get_ram_states((37, 38, 39, 70, 73, 74, 94, 95), ram_state)
    relevant_objects.extend(info["Player"])
    info["Shot"] = get_ram_states((45, 49, 52, 55, 58, 61, 64), ram_state)
    relevant_objects.extend(info["Player"])
    # info["Score"] = get_ram_states((33, 108, 110, 112), ram_state)
    # info["Life"] = get_ram_states((97, 100), ram_state)

    info["relevant_objects"] = relevant_objects
