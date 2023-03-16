from dataclasses import dataclass

from ._helper_methods import number_to_bitfield, bitfield_to_number
from .game_objects import GameObject

# RAM


class Player(GameObject):
    def __init__(self):
        super(Player, self).__init__()
        self._xy = 133, 103     #initially
        self.wh = 16, 9
        self.rgb = 223, 183, 85
        self.hud = False
        self.velocity_x = 0
        self.dying = False


class MiniPlayer(GameObject):
    def __init__(self):
        super(MiniPlayer, self).__init__()
        self._xy = 133, 103  # initially
        self.wh = 2, 2
        self.rgb = 124, 44, 0
        self.hud = False


class Truck(GameObject):
    def __init__(self):
        super(Truck, self).__init__()
        self._xy = 0, 166      #166 immer
        self.wh = 8, 7
        self.rgb = 0, 0, 0
        self.hud = False


class MiniTruck(GameObject):
    def __init__(self):
        super(MiniTruck, self).__init__()
        self._xy = 133, 103  # initially
        self.wh = 2, 2
        self.rgb = 236, 200, 96
        self.hud = False


class EnemyHelicopter(GameObject):
    def __init__(self):
        super(EnemyHelicopter, self).__init__()
        self._xy = 0, 0         #random
        self.wh = 8, 9
        self.rgb = 236, 236, 236
        self.hud = False


class EnemyPlane(GameObject):
    def __init__(self):
        super(EnemyPlane, self).__init__()
        self._xy = 0, 0         #random
        self.wh = 8, 6
        self.rgb = 0, 0, 148
        self.hud = False


class MiniEnemy(GameObject):
    def __init__(self):
        super(MiniEnemy, self).__init__()
        self._xy = 133, 103  # initially
        self.wh = 2, 2
        self.rgb = 236, 200, 96
        self.hud = False


class Bomb(GameObject):
    def __init__(self):
        super(Bomb, self).__init__()
        self._xy = 0, 0         #random
        self.wh = 2, 2          # oder 2,1 wenn gesplittet
        self.rgb = 223, 183, 85
        self.hud = False


class Shot(GameObject):
    def __init__(self):
        super(Shot, self).__init__()
        self._xy = 0, 0         # auf höhe des helis
        self.wh = 0, 1         # höhe = 1, breite random
        self.rgb = 0, 0, 100      #blau ist höher, aber sonst random
        self.hud = False


class Score(GameObject):
    def __init__(self):
        super(Score, self).__init__()
        self._xy = 75, 16
        self.wh = 6, 7
        self.rgb = 223, 183, 85
        self.hud = True


class Life(GameObject):
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
    if hud:
        objects.extend([Score(), Life(), Life()])
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


def _detect_objects_revised(objects, ram_state, hud):
    # player
    player = objects[0]
    player.xy = (ram_state[71], 159-ram_state[72])
    velocity_raw = ram_state[42]
    if velocity_raw > 127:
        velocity_raw = 255-velocity_raw
    player.velocity_x = velocity_raw
    player.direction = number_to_bitfield(ram_state[66])[7]
    player.dying = 97 <= ram_state[97] <= 127

    # mini_player
    mini_player = objects[1]
    b_mini_x = number_to_bitfield(ram_state[71])[:3]
    mini_x = 74+bitfield_to_number(b_mini_x)
    b_mini_y = number_to_bitfield(ram_state[72])[1:4]
    mini_y = 184-bitfield_to_number(b_mini_y)
    mini_player.xy = (mini_x, mini_y)

    tmp = objects[:2]
    objects.clear()
    objects.extend(tmp)

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
    # y~ram_state[23-24]
    # dying might be 30-32
    # existence: ram_state[18:21] and field limit

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
    shot_lines = [ram_state[52], ram_state[55], ram_state[58], ram_state[61], ram_state[64]]
    b_shot_line = number_to_bitfield(ram_state[49])
    for shot_line in shot_lines:
        b_shot_line.extend(number_to_bitfield(shot_line))

    # [0,0,0,0,1,1,0,0,0,0,1,1,1,1,1,0]

    b_shot_line.append(0)   # to see if there is a shot at the end
    bool_shot = False
    shot = None
    pixel = 0
    for i in b_shot_line:
        if i == 1:
            if bool_shot:
                # increases shot size
                x, _ = player.xy
                x += 67
                w = pixel-x+16
                h = 1
                shot.wh = (w, h)
            else:
                # starts shot
                shot = Shot()
                x = pixel
                _, y = player.xy
                y += 5
                shot.xy = (x, y)
            bool_shot = True
        else:
            if bool_shot:
                objects.append(shot)
            bool_shot = False
        pixel += 1

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

