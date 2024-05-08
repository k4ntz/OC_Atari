from dataclasses import dataclass

from ._helper_methods import number_to_bitfield, bitfield_to_number, _convert_number
from .game_objects import GameObject, ValueObject
import sys
from math import ceil

"""
RAM extraction for the game Chopper Command.
"""

MAX_NB_OBJECTS =  {'Player': 1, 'MiniPlayer': 1, 'Truck': 3, 'MiniTruck': 9, 'MiniEnemy': 12, 'Shot': 1, 'EnemyPlane': 3, 'EnemyHelicopter': 3, 'Bomb': 3}
MAX_NB_OBJECTS_HUD =  {'Player': 1, 'Truck': 3, 'MiniPlayer': 1, 'MiniEnemy': 12, 'MiniTruck': 9, 'Shot': 1, 'EnemyPlane': 3, 'EnemyHelicopter': 3, 'Bomb': 3, 'Score': 4, 'Life': 2 }


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

class Player(GameObject):
    """
    The player figure i.e., the helicopter gunship. 
    """
    
    def __init__(self):
        super(Player, self).__init__()
        self._xy = 133, 103     #initially
        self.wh = 16, 9
        self.orientation = 1
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
    
    def __init__(self):
        super(Truck, self).__init__()
        self._xy = 0, 166      #166 immer
        self.wh = 8, 7
        self.rgb = 0, 0, 0
        self.hud = False


class MiniTruck(GameObject):
    """
    The blips for the trucks on the Long Range Scanner. 
    """
    
    def __init__(self):
        super(MiniTruck, self).__init__()
        self._xy = 133, 185  # initially
        self.wh = 1, 2
        self.rgb = 236, 200, 96
        self.hud = False


class EnemyHelicopter(GameObject):
    """
    The enemy helicopters. 
    """
    
    def __init__(self):
        super(EnemyHelicopter, self).__init__()
        self._xy = 0, 0         #random
        self.wh = 8, 9
        self.rgb = 236, 236, 236
        self.hud = False


class EnemyPlane(GameObject):
    """
    The enemy planes. 
    """
    
    def __init__(self):
        super(EnemyPlane, self).__init__()
        self._xy = 0, 0         #random
        self.wh = 8, 6
        self.rgb = 0, 0, 148
        self.hud = False


class MiniEnemy(GameObject):
    """
    The blips for the enemy aircraft on the Long Range Scanner. 
    """
    
    def __init__(self):
        super(MiniEnemy, self).__init__()
        self._xy = 133, 103  # initially
        self.wh = 2, 2
        self.rgb = 236, 200, 96
        self.hud = False


class Bomb(GameObject):
    """
    The multi-warhead missiles deployed by enemy aircraft. 
    """
    
    def __init__(self):
        super(Bomb, self).__init__()
        self._xy = 0, 0         #random
        self.wh = 2, 2          # oder 2,1 wenn gesplittet
        self.rgb = 223, 183, 85
        self.hud = False


class Shot(GameObject):
    """
    The projectiles shot from the helicopter's laser cannon. 
    """
    
    def __init__(self):
        super(Shot, self).__init__()
        self._xy = 0, 0         # auf höhe des helis
        self.wh = 0, 1         # höhe = 1, breite random
        self.rgb = 0, 0, 100      #blau ist höher, aber sonst random
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


class Life(GameObject):
    """
    The indicator for helicopter rerves (lifes) (HUD).
    """
    
    def __init__(self):
        super(Life, self).__init__()
        self._xy = 33, 24           # and 41, 24 and so on
        self.wh = 8, 9
        self.rgb = 223, 183, 85
        self.hud = True

@dataclass
class MiniPlayArea:
    (minx, miny, maxx, maxy) = (56, 178, 103, 187)


@dataclass
class PlayArea:
    (minx, miny, maxx, maxy) = (18, 64, 150, 163)


def _init_objects_ram(hud):
    #gibt Liste von GameObjects zurück
    """
    (Re)Initialize the objects
    """
    objects = [Player(), MiniPlayer()]
    objects.extend([None] * 34)
    if hud:
        objects.extend([None] * 12)
    
    global last_30
    global last_31
    global last_32
    global truck_4
    global truck_x
    global last_68
    global last_y
    last_30 = 96
    last_31 = 96
    last_32 = 96
    truck_4 = 0
    truck_x = 10
    last_68 = 0
    last_y = 0

    return objects


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


def _detect_objects_ram(objects, ram_state, hud):

    global last_30
    global last_31
    global last_32
    global truck_4
    global truck_x
    global last_68
    global last_y

    # player
    player = objects[0]
    if ram_state[97]:
        player.xy = (ram_state[71] + 2, 159-ram_state[72])
    else:
        player.xy = (ram_state[71], 159-ram_state[72])
    player.orientation = ram_state[66]
    # velocity_raw = ram_state[42]
    # if velocity_raw > 127:
    #     velocity_raw = 255-velocity_raw
    # player.velocity_x = velocity_raw
    # player.direction = number_to_bitfield(ram_state[66])[7]
    # player.dying = 97 <= ram_state[97] <= 127

    # mini_player
    mini_player = objects[1]
    b_mini_x = number_to_bitfield(ram_state[71])[:3]
    mini_x = 74+bitfield_to_number(b_mini_x)
    b_mini_y = number_to_bitfield(ram_state[72])[1:4]
    mini_y = 184-bitfield_to_number(b_mini_y)
    mini_player.xy = mini_x, mini_y

    if ram_state[2] != 240:
        bomb = Bomb()
        objects[10] = bomb
        if -1 <= (ram_state[94] - ram_state[95]) <= 1:
            bomb.xy = ram_state[70] - 1, 167 - ram_state[2]
            bomb.wh = 2,2
            objects[11] = None
        elif ram_state[94] != 240 and ram_state[95] != 240:
            bomb.xy = ram_state[70] + 1, 167 - ram_state[94] + 2
            bomb2 = Bomb()
            objects[11] = bomb2
            bomb2.xy = ram_state[70] + 1, 167 - ram_state[95] - 2
            bomb.wh = 2,1
            bomb2.wh = 2,1
        elif ram_state[94] != 240:
            bomb.xy = ram_state[70] + 1, 167 - ram_state[94] + 2
            bomb.wh = 2,1
            objects[11] = None
        elif ram_state[95] != 240:
            bomb.xy = ram_state[70] + 1, 167 - ram_state[95] - 2
            bomb.wh = 2,1
            objects[11] = None
        else:
            objects[10] = None
            objects[11] = None
        
    else:
        objects[10] = None
        objects[11] = None

    mid_mid_group = number_to_bitfield(ram_state[7])[2:8]
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

    if ram_state[17]:
        truck = Truck()
        objects[7] = truck
        truck.xy = ram_state[17], 160
        if ram_state[21] == 0 and ram_state[17] > 160:
            objects[8] = None
            objects[9] = None
            if truck_4 or ram_state[17] < 222:
                truck.xy = (ram_state[17] + 64)%255 - 1, 160
            else:
                truck.xy = (ram_state[17] + 32)%255 - 1, 160
        if ram_state[21] == 2:
            objects[9] = None
            truck_4 = 0
            truck2 = Truck()
            objects[8] = truck2
            truck2.xy = (ram_state[17] + 32)%255, 160
            if ram_state[17] > 160:
                truck.xy = (ram_state[17] + 32)%255 - 1, 160
                truck2.xy = (ram_state[17] + 64)%255 - 1, 160
        elif ram_state[21] == 4:
            truck_4 = 1
            truck2 = Truck()
            objects[8] = truck2
            truck2.xy = (ram_state[17] + 64)%255, 160
            objects[9] = None
        elif ram_state[21] == 6:
            truck_4 = 0
            truck2 = Truck()
            objects[8] = truck2
            truck2.xy = (ram_state[17] + 32)%255, 160
            truck3 = Truck()
            objects[9] = truck3
            truck3.xy = (ram_state[17] + 64)%255, 160

    else:
        objects[7] = None
        objects[8] = None
        objects[9] = None
        truck_4 = 0

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

    # low lane
    if ram_state[30] != 96 or last_30 != 96:
        if ram_state[34] == 6 or ram_state[34] == 7:
            enemy = EnemyPlane()
        else:
            enemy = EnemyHelicopter()
        _, h = enemy.wh
        objects[4] = enemy
        if (int(ram_state[18]) + int(ram_state[68])) < 160:
            if ram_state[66]:
                enemy.xy = ram_state[18] + ram_state[68], 167 - ram_state[22] - h
            else:
                enemy.xy = ram_state[18] + ram_state[68] - 2, 167 - ram_state[22] - h
        else:
            if ram_state[66]:
                enemy.xy = ram_state[18] - (160 - ram_state[68]), 167 - ram_state[22] - h
            else:
                enemy.xy = ram_state[18] - (160 - ram_state[68]) - 2, 167 - ram_state[22] - h
    else:
        objects[4] = None

    last_30 = ram_state[30]

    # mid lane
    if ram_state[31] != 96 or last_31 != 96:
        if ram_state[35] == 6 or ram_state[35] == 7:
            enemy = EnemyPlane()
        else:
            enemy = EnemyHelicopter()
        _, h = enemy.wh
        objects[5] = enemy
        if (int(ram_state[19]) + int(ram_state[68])) < 160:
            if ram_state[66]:
                enemy.xy = ram_state[19] + ram_state[68], 167 - ram_state[23] - h
            else:
                enemy.xy = ram_state[19] + ram_state[68] - 2, 167 - ram_state[23] - h
        else:
            if ram_state[66]:
                enemy.xy = ram_state[19] - (160 - ram_state[68]), 167 - ram_state[23] - h
            else:
                enemy.xy = ram_state[19] - (160 - ram_state[68]) - 2, 167 - ram_state[23] - h
    else:
        objects[5] = None

    last_31 = ram_state[31]

    # high lane
    if ram_state[32] != 96 or last_32 != 96:
        if ram_state[36] == 6 or ram_state[36] == 7:
            enemy = EnemyPlane()
        else:
            enemy = EnemyHelicopter()
        _, h = enemy.wh
        objects[6] = enemy
        if (int(ram_state[20]) + int(ram_state[68])) < 160:
            if ram_state[66]:
                enemy.xy = ram_state[20] + ram_state[68], 167 - ram_state[24] - h
            else:
                enemy.xy = ram_state[20] + ram_state[68] - 2, 167 - ram_state[24] - h
        else:
            if ram_state[66]:
                enemy.xy = ram_state[20] - (160 - ram_state[68]), 167 - ram_state[24] - h
            else:
                enemy.xy = ram_state[20] - (160 - ram_state[68]) - 2, 167 - ram_state[24] - h
    else:
        objects[6] = None

    last_32 = ram_state[32]

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
    shot_lines = [ram_state[52], ram_state[55], ram_state[58], ram_state[61], ram_state[64]]
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

    global last_y
    # if objects[3] == None:
    #     last_y = player.y + 5

    objects[3] = None

    for s in b_shot_line:
        if s:
            w = w + 4
        elif w > 0:
            shot = Shot()
            shot.xy = x-w, 210-ram_state[65]-43 # player.y + 5 # last_y
            shot.wh = w, 1
            objects[3] = shot
            w = 0
        x = x + 4

    if ram_state[97] <= 100 and ram_state[97] >= 95:
        truck_x = 10

    if ceil((ram_state[68]+1)/20) != ceil((last_68+1)/20):
        if ram_state[66]:
            truck_x = (truck_x + 1)%15
        else:
            truck_x = (truck_x - 1)%15

    # Minitrucks and mid air lane

    if ram_state[5]:
        t_lane = ram_state[5]&56
        t_lane = t_lane >> 3
        if ram_state[66]:
            x = 115 - truck_x + 1
        else:
            x = 115 - truck_x
        if ram_state[97]:
            x -= 1
        lane_2 = ram_state[5]&7
        if lane_2 and x + lane_2 - 3 <= 103:
                m_enemy = MiniEnemy()
                objects[23] = m_enemy
                m_enemy.xy = x + lane_2 - 4, 181
        else:
            objects[23] = None

        if x <= 103:
            if t_lane == 7 or t_lane == 6:
                m_truck1 = MiniTruck()
                objects[18] = m_truck1
                m_truck1.xy = x, 185
                if x <= 101:
                    m_truck2 = MiniTruck()
                    objects[19] = m_truck2
                    m_truck2.xy = x+2, 185
            elif t_lane == 5:
                m_truck1 = MiniTruck()
                objects[18] = m_truck1
                m_truck1.xy = x, 185
                if x <= 101:
                    objects[19] = None
            elif (t_lane == 4 or t_lane == 2) and x <= 101:
                m_truck1 = MiniTruck()
                objects[18] = m_truck1
                m_truck1.xy = x+2, 185
                objects[19] = None
            elif t_lane == 3:
                m_truck1 = MiniTruck()
                objects[18] = m_truck1
                m_truck1.xy = x, 185
                if x <= 101:
                    objects[19] = None
        else:
            objects[18] = None
            objects[19] = None
            objects[23] = None

    if ram_state[6]:
        t_lane = ram_state[6]&56
        t_lane = t_lane >> 3
        if ram_state[66]:
            x = 99 - truck_x + 1
        else:
            x = 99 - truck_x
        if ram_state[97]:
            x -= 1
        lane_2 = ram_state[6]&7
        if lane_2:
            m_enemy = MiniEnemy()
            objects[21] = m_enemy
            m_enemy.xy = x + lane_2 - 4, 181
        else:
            objects[21] = None

        if t_lane == 7:
            m_truck1 = MiniTruck()
            m_truck2 = MiniTruck()
            m_truck3 = MiniTruck()
            objects[12] = m_truck1
            objects[13] = m_truck2
            objects[14] = m_truck3
            m_truck1.xy = x, 185
            m_truck2.xy = x+2, 185
            m_truck3.xy = x+4, 185
        elif t_lane == 6:
            m_truck1 = MiniTruck()
            m_truck2 = MiniTruck()
            objects[12] = m_truck1
            objects[13] = m_truck2
            objects[14] = None
            m_truck1.xy = x, 185
            m_truck2.xy = x+2, 185
        elif t_lane == 5:
            m_truck1 = MiniTruck()
            m_truck2 = MiniTruck()
            objects[12] = m_truck1
            objects[13] = m_truck2
            objects[14] = None
            m_truck1.xy = x, 185
            m_truck2.xy = x+4, 185
        elif t_lane == 4:
            m_truck1 = MiniTruck()
            m_truck2 = MiniTruck()
            objects[12] = m_truck1
            objects[13] = m_truck2
            objects[14] = None
            m_truck1.xy = x+2, 185
            m_truck2.xy = x+4, 185
        elif t_lane == 3:
            m_truck1 = MiniTruck()
            objects[12] = m_truck1
            objects[13] = None
            objects[14] = None
            m_truck1.xy = x, 185
        elif t_lane == 2:
            m_truck1 = MiniTruck()
            objects[12] = m_truck1
            objects[13] = None
            objects[14] = None
            m_truck1.xy = x+2, 185
        elif t_lane == 1:
            m_truck1 = MiniTruck()
            objects[12] = m_truck1
            objects[13] = None
            objects[14] = None
            m_truck1.xy = x+4, 185
    else:
        objects[12] = None
        objects[13] = None
        objects[14] = None
        objects[21] = None

    if ram_state[7]:
        t_lane = ram_state[7]&56
        t_lane = t_lane >> 3
        if ram_state[66]:
            x = 83 - truck_x + 1
        else:
            x = 83 - truck_x
        if ram_state[97]:
            x -= 1
        lane_2 = ram_state[7]&7
        if lane_2:
            m_enemy = MiniEnemy()
            objects[22] = m_enemy
            m_enemy.xy = x + lane_2 - 4, 181
        else:
            objects[22] = None

        if t_lane == 7:
            m_truck1 = MiniTruck()
            m_truck2 = MiniTruck()
            m_truck3 = MiniTruck()
            objects[15] = m_truck1
            objects[16] = m_truck2
            objects[17] = m_truck3
            m_truck1.xy = x, 185
            m_truck2.xy = x+2, 185
            m_truck3.xy = x+4, 185
        elif t_lane == 6:
            m_truck1 = MiniTruck()
            m_truck2 = MiniTruck()
            objects[15] = m_truck1
            objects[16] = m_truck2
            objects[17] = None
            m_truck1.xy = x, 185
            m_truck2.xy = x+2, 185
        elif t_lane == 5:
            m_truck1 = MiniTruck()
            m_truck2 = MiniTruck()
            objects[15] = m_truck1
            objects[16] = m_truck2
            objects[17] = None
            m_truck1.xy = x, 185
            m_truck2.xy = x+4, 185
        elif t_lane == 4:
            m_truck1 = MiniTruck()
            m_truck2 = MiniTruck()
            objects[15] = m_truck1
            objects[16] = m_truck2
            objects[17] = None
            m_truck1.xy = x+2, 185
            m_truck2.xy = x+4, 185
        elif t_lane == 3:
            m_truck1 = MiniTruck()
            objects[15] = m_truck1
            objects[16] = None
            objects[17] = None
            m_truck1.xy = x, 185
        elif t_lane == 2:
            m_truck1 = MiniTruck()
            objects[15] = m_truck1
            objects[16] = None
            objects[17] = None
            m_truck1.xy = x+2, 185
        elif t_lane == 1:
            m_truck1 = MiniTruck()
            objects[15] = m_truck1
            objects[16] = None
            objects[17] = None
            m_truck1.xy = x+4, 185
    else:
        objects[15] = None
        objects[16] = None
        objects[17] = None
        objects[22] = None

    if ram_state[8]:
        t_lane = ram_state[8]&56
        t_lane = t_lane >> 3
        if ram_state[66]:
            x = 67 - truck_x + 1
        else:
            x = 67 - truck_x
        if ram_state[97]:
            x -= 1
        lane_2 = ram_state[8]&7
        if lane_2 and x + lane_2 - 4 >= 55:
            m_enemy = MiniEnemy()
            objects[23] = m_enemy
            m_enemy.xy = x + lane_2 - 4, 181

        if t_lane == 7:
            m_truck3 = MiniTruck()
            objects[20] = m_truck3
            if x >= 56:
                m_truck1 = MiniTruck()
                objects[18] = m_truck1
                m_truck1.xy = x, 185
            if x + 2 >= 56:
                m_truck2 = MiniTruck()
                objects[19] = m_truck2
                m_truck2.xy = x+2, 185
            m_truck3.xy = x+4, 185
        elif t_lane == 6:
            objects[20] = None
            if x >= 56:
                m_truck1 = MiniTruck()
                objects[18] = m_truck1
                m_truck1.xy = x, 185
            if x + 2 >= 56:
                m_truck2 = MiniTruck()
                objects[19] = m_truck2
                m_truck2.xy = x+2, 185
        elif t_lane == 5:
            m_truck2 = MiniTruck()
            objects[19] = None
            objects[20] = m_truck2
            if x >= 56:
                m_truck1 = MiniTruck()
                objects[18] = m_truck1
                m_truck1.xy = x, 185
            m_truck2.xy = x+4, 185
        elif t_lane == 4:
            m_truck2 = MiniTruck()
            objects[18] = None
            objects[20] = m_truck2
            if x + 2 >= 56:
                m_truck1 = MiniTruck()
                objects[19] = m_truck1
                m_truck1.xy = x+2, 185
            m_truck2.xy = x+4, 185
        elif t_lane == 3:
            objects[19] = None
            objects[20] = None
            if x >= 56:
                m_truck1 = MiniTruck()
                objects[18] = m_truck1
                m_truck1.xy = x, 185
        elif t_lane == 2:
            objects[18] = None
            objects[20] = None
            if x + 2 >= 56:
                m_truck1 = MiniTruck()
                objects[19] = m_truck1
                m_truck1.xy = x+2, 185
        elif t_lane == 1:
            m_truck1 = MiniTruck()
            objects[18] = None
            objects[19] = None
            objects[20] = m_truck1
            m_truck1.xy = x+4, 185
    else:
        objects[20] = None
        objects[23] = None

    # Enemy in the air top lane + bottom lane

    if ram_state[9]:
        lane_3 = ram_state[9]&56
        lane_3 = lane_3 >> 3
        lane_1 = ram_state[9]&7
        if ram_state[66]:
            x = 115 - truck_x - 3
        else:
            x = 115 - truck_x - 4
        if ram_state[97]:
            x -= 1
        if lane_3 and x + lane_3 + 1<= 103:
                m_enemy = MiniEnemy()
                objects[24] = m_enemy
                m_enemy.xy = x + lane_3, 183
        else:
            objects[24] = None
        if lane_1 and x + lane_1 + 1<= 103:
                m_enemy = MiniEnemy()
                objects[25] = m_enemy
                m_enemy.xy = x + lane_1, 179
        else:
            objects[25] = None
    else:
        objects[24] = None
        objects[25] = None

    if ram_state[10]:
        lane_3 = ram_state[10]&56
        lane_3 = lane_3 >> 3
        lane_1 = ram_state[10]&7
        if ram_state[66]:
            x = 99 - truck_x - 3
        else:
            x = 99 - truck_x - 4
        if ram_state[97]:
            x -= 1
        if lane_3:
                m_enemy = MiniEnemy()
                objects[26] = m_enemy
                m_enemy.xy = x + lane_3, 183
        else:
            objects[26] = None
        if lane_1:
                m_enemy = MiniEnemy()
                objects[27] = m_enemy
                m_enemy.xy = x + lane_1, 179
        else:
            objects[27] = None
    else:
        objects[26] = None
        objects[27] = None

    if ram_state[11]:
        lane_3 = ram_state[11]&56
        lane_3 = lane_3 >> 3
        lane_1 = ram_state[11]&7
        if ram_state[66]:
            x = 83 - truck_x - 3
        else:
            x = 83 - truck_x - 4
        if ram_state[97]:
            x -= 1
        if lane_3:
                m_enemy = MiniEnemy()
                objects[28] = m_enemy
                m_enemy.xy = x + lane_3, 183
        else:
            objects[28] = None
        if lane_1:
                m_enemy = MiniEnemy()
                objects[29] = m_enemy
                m_enemy.xy = x + lane_1, 179
        else:
            objects[29] = None
    else:
        objects[28] = None
        objects[29] = None

    if ram_state[12]:
        lane_3 = ram_state[12]&56
        lane_3 = lane_3 >> 3
        lane_1 = ram_state[12]&7
        if ram_state[66]:
            x = 67 - truck_x - 3
        else:
            x = 67 - truck_x - 4
        if ram_state[97]:
            x -= 1
        if lane_3 and x + lane_3 >= 55:
                m_enemy = MiniEnemy()
                objects[30] = m_enemy
                m_enemy.xy = x + lane_3, 183
        else:
            objects[30] = None
        if lane_1 and x + lane_1>= 55:
                m_enemy = MiniEnemy()
                objects[31] = m_enemy
                m_enemy.xy = x + lane_1, 179
        else:
            objects[31] = None
    else:
        objects[30] = None
        objects[31] = None
        

    last_68 = ram_state[68]

    if hud:
        
        for i in range(12):
            objects[36+i] = None

        for i in range(ram_state[100] - 1):
            life = Life()
            life.xy = 33 + (8 * i), 24
            objects[36+i] = life
        
        # score
        if ram_state[108] > 15:
            for i in range(6):
                score = Score()
                score.xy = 75 - (i * 8), 16
                objects[42+i] = score
        elif ram_state[108] > 0:
            for i in range(5):
                score = Score()
                score.xy = 75 - (i * 8), 16
                objects[42+i] = score
        elif ram_state[110] > 15:
            for i in range(4):
                score = Score()
                score.xy = 75 - (i * 8), 16
                objects[42+i] = score
        elif ram_state[110] > 0:
            for i in range(3):
                score = Score()
                score.xy = 75 - (i * 8), 16
                objects[42+i] = score
        elif ram_state[112] > 15:
            for i in range(2):
                score = Score()
                score.xy = 75 - (i * 8), 16
                objects[42+i] = score
        else:
            score = Score()
            objects[42] = score
        try:
            score.value = _convert_number(ram_state[108]) * 10000 + _convert_number(ram_state[110]) * 100 + _convert_number(ram_state[112])
        except:
            pass

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
