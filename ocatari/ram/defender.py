from .game_objects import GameObject, ValueObject, NoObject, Orientation, OrientedObject, OrientedNoObject
import sys
import numpy as np
import math

MAX_NB_OBJECTS = {"Player": 1, "Player_Shot": 1, "Enemy_Shot": 1, "Bomber": 2, "Baiter": 2, "Pod": 2, "Swarm": 2, "Lander": 5, "Humanoide_Lander": 5, "Human": 5, "Radar_Player": 1, "Radar_Enemy": 8, "Radar_Human": 5}
MAX_NB_OBJECTS_HUD = {"Player": 1, "Player_Shot": 1, "Enemy_Shot": 1, "Bomber": 1, "Baiter": 1, "Pod": 2, "Swarm": 2, "Lander": 5, "Humanoide_Lander": 5, "Human": 5, "Radar_Player": 1, "Radar_Enemy": 8, "Radar_Human": 5, "Score": 1, "Lives": 1, "Smart_Bomb_Count": 1}


class Player(OrientedObject):
    def __init__(self):
        super(Player, self).__init__()
        self._xy = 0, 0
        self.wh = (7, 5)
        self.rgb = 132, 144, 252
        self.hud = False
        self.orientation = Orientation.E


class Player_Shot(OrientedObject):
    def __init__(self, orientation=Orientation.E):
        super(Player_Shot, self).__init__()
        self._xy = 0, 0
        self.wh = (32, 2)
        self.rgb = 132, 144, 252
        self.hud = False
        self.orientation = orientation


class Enemy_Shot(GameObject):
    def __init__(self, p_x=0, p_y=0):
        super(Enemy_Shot, self).__init__()
        self._xy = 0, 0
        self.pre_xy = p_x, p_y
        self.wh = (2, 2)
        self.rgb = 132, 144, 252
        self.hud = False
        self.frame_count = 0


class Bomber(GameObject):
    def __init__(self, p_x=0, p_y=0):
        super(Bomber, self).__init__()
        self._xy = 0, 0
        self.pre_xy = p_x, p_y
        self.wh = (5, 4)
        self.rgb = 84, 92, 214
        self.hud = False
        self.frame_count = 0


class Baiter(GameObject):
    def __init__(self, p_x=0, p_y=0):
        super(Baiter, self).__init__()
        self._xy = 0, 0
        self.pre_xy = p_x, p_y
        self.wh = (8, 3)
        self.rgb = 132, 144, 252
        self.hud = False
        self.frame_count = 0


class Pod(GameObject):
    def __init__(self, p_x=0, p_y=0):
        super(Pod, self).__init__()
        self._xy = 0, 0
        self.pre_xy = p_x, p_y
        self.wh = (7, 7)
        self.rgb = 252, 224, 112
        self.hud = False
        self.frame_count = 0


class Swarm(GameObject):
    def __init__(self, p_x=0, p_y=0):
        super(Swarm, self).__init__()
        self._xy = 0, 0
        self.pre_xy = p_x, p_y
        self.wh = (8, 7)
        self.rgb = 232, 232, 74
        self.hud = False
        self.frame_count = 0

class Lander(GameObject):
    def __init__(self, p_x=0, p_y=0):
        super(Lander, self).__init__()
        self._xy = 0, 0
        self.pre_xy = p_x, p_y
        self.wh = (8, 7)
        self.rgb = 210, 210, 64
        self.hud = False
        self.frame_count = 0


class Humanoide_Lander(GameObject):
    def __init__(self, p_x=0, p_y=0):
        super(Humanoide_Lander, self).__init__()
        self._xy = 0, 0
        self.pre_xy = p_x, p_y
        self.wh = (8, 7)
        self.rgb = 198, 108, 58
        self.hud = False
        self.frame_count = 0


class Human(GameObject):
    def __init__(self, x=0, y=0, total_x=0, ram_73=0):
        super(Human, self).__init__()
        self._xy = x, y
        self.pre_xy = x, y
        self.wh = (2, 4)
        self.rgb = 132, 144, 252
        self.hud = False
        self.frame_count = 0
        self.total_x = total_x
        self.ram_73 = ram_73


class Radar_Player(GameObject):
    def __init__(self):
        super(Radar_Player, self).__init__()
        self._xy = 0, 0
        self.wh = (4, 2)
        self.rgb = 232, 232, 74
        self.hud = False


class Radar_Enemy(GameObject):
    def __init__(self):
        super(Radar_Enemy, self).__init__()
        self._xy = 0, 0
        self.wh = (2, 2)
        self.hud = False

class Radar_Bomber(Radar_Enemy):
    def __init__(self):
        super(Radar_Bomber, self).__init__()
        self.rgb = 132, 144, 252

class Radar_Baiter(Radar_Enemy):
    def __init__(self):
        super(Radar_Baiter, self).__init__()
        self.rgb = 132, 144, 252

class Radar_Pod(Radar_Enemy):
    def __init__(self):
        super(Radar_Pod, self).__init__()
        self.rgb = 252, 224, 112

class Radar_Swarm(Radar_Enemy):
    def __init__(self):
        super(Radar_Swarm, self).__init__()
        self.rgb = 232, 232, 74

class Radar_Lander(Radar_Enemy):
    def __init__(self):
        super(Radar_Lander, self).__init__()
        self.rgb = 210, 210, 64

class Radar_Humanoide_Lander(Radar_Enemy):
    def __init__(self):
        super(Radar_Humanoide_Lander, self).__init__()
        self.rgb = 198, 108, 58


class Radar_Human(GameObject):
    def __init__(self):
        super().__init__()
        self._xy = 0, 33
        self.wh = (1, 2)
        self.rgb = 232, 232, 74
        self.hud = False


class City_Scape(GameObject):
    def __init__(self):
        super().__init__()
        self._xy = 0, 156
        self.wh = (160, 17)
        self.rgb = 84, 92, 214
        self.hud = False


class Score(ValueObject):
    def __init__(self):
        super(Score, self).__init__()
        self._xy = 88, 177
        self.wh = 7, 5
        self.rgb = 232, 232, 74
        self.hud = True
        self.value = 0


class Lives(ValueObject):
    def __init__(self):
        super(Lives, self).__init__()
        self._xy = 4, 187
        self.wh = 7, 5
        self.rgb = 132, 144, 252
        self.hud = True
        self.value = 0


class Smart_Bomb_Count(ValueObject):
    def __init__(self):
        super(Smart_Bomb_Count, self).__init__()
        self._xy = 115, 187
        self.wh = 6, 3
        self.rgb = 132, 144, 252
        self.hud = True
        self.value = 0

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
    objects = [Player(), OrientedNoObject()]

    objects.extend([NoObject()] * 38)
    objects.extend([City_Scape()])
    if hud:
        objects.extend([Score(), Lives(), Smart_Bomb_Count()])
    return objects

typings = [Bomber, Baiter, Pod, Swarm, Lander, Humanoide_Lander]
offsets = [0, 2, 3, 5, 5, 10]

def _detect_objects_ram(objects, ram_state, hud=False):
    """
    For all 3 objects:
    (x, y, w, h, r, g, b)
    """
    if ram_state[11]&4:
        objects[0].xy = ram_state[37] + 1, 177 - ram_state[45] if ram_state[45] < 134 else 44
        objects[0].orientation = Orientation.E
    else:
        objects[0].xy = ram_state[37], 177 - ram_state[45] if ram_state[45] < 134 else 44
        objects[0].orientation = Orientation.W

    if ram_state[102]:
        if type(objects[1]) is OrientedNoObject:
            objects[1] = Player_Shot(orientation=objects[0].orientation)
        if ram_state[11]&4:
            objects[1].xy = ram_state[102] - 6, 179 - ram_state[45]
        else:
            objects[1].xy = ram_state[102] + 8, 179 - ram_state[45]

    else:
        objects[1] = OrientedNoObject()

    if ram_state[39] and ram_state[43] < 134:
        if type(objects[2]) is NoObject:
            objects[2] = Enemy_Shot(p_x=ram_state[39], p_y=(170-ram_state[43]))
        
        objects[2].xy = objects[2].pre_xy
        objects[2].pre_xy = ram_state[39], 170 - ram_state[43]
        objects[2].frame_count = 0
    else:
        if type(objects[2]) is not NoObject:
            objects[2].xy = objects[2].pre_xy
            objects[2].frame_count += 1
            if objects[2].frame_count > 3:
                objects[2] = NoObject()


    # enemies ram[50]: bomber == 8, baiter == 16, pod == 24, swamers == 32, lander == 40, humanoid_lander == 48, level number == 49
    if ram_state[55] != 255 and 0 < ram_state[50] < 49:
        enemy_type = (ram_state[50]>>3) - 1
        index = offsets[enemy_type] + ram_state[55]
        
        if type(objects[3+index]) is not typings[enemy_type]:
            objects[3+index] = typings[enemy_type](p_x=ram_state[38], p_y=172 - ram_state[48] if ram_state[48] < 129 else 44)

        if ram_state[20]:
            objects[3+index].xy = ram_state[38], 172 - ram_state[48] if ram_state[48] < 129 else 44
        else:
            objects[3+index].xy = objects[3+index].pre_xy
            objects[3+index].pre_xy = ram_state[38], 172 - ram_state[48] if ram_state[48] < 129 else 44

        objects[3+index].frame_count = 0

        for i in range(3, 21):
            if type(objects[i]) is not NoObject:
                objects[i].frame_count += 1
                if objects[i].frame_count > 8:
                    objects[i] = NoObject()
                    objects[i].frame_count = 0
    else:
        for i in range(3, 21):
            objects[i] = NoObject()
                
    # updates human position based on scroll to have constant positioning despite flickering
    for i in range(21, 26):
        if type(objects[i]) is not NoObject:
            if objects[i].frame_count > 6:
                objects[i] = NoObject()
            else:
                offset = objects[i].ram_73 - np.int8(ram_state[73])
                if 0 < objects[i].x + offset < 160:
                    objects[i].xy = objects[i].pre_xy
                    objects[i].pre_xy = objects[i].x - offset*2, objects[i].y
                    objects[i].ram_73 = np.int8(ram_state[73])
                    objects[i].frame_count += 1
                else:
                    objects[i] = NoObject()

    # humans x, y == 36, 47 (y from 168)
    # ram 78 == which human appears in the next frame

    if ram_state[36] and ram_state[78] < 5:
        idx = 21 + ram_state[78]
        if type(objects[idx]) is NoObject:
            objects[idx] = Human(x=ram_state[36], y=169, total_x=ram_state[36] - np.int8(ram_state[73])*2, ram_73=np.int8(ram_state[73]))
        objects[idx].xy = objects[idx].pre_xy
        objects[idx].pre_xy = ram_state[36], 169 if ram_state[42] == 1 else 168-ram_state[47]
        objects[idx].frame_count = 0


    # radar enemy_xy == ram 40, 44 where x = ram[40] and if ram[44] == 0 -> 36 so y = 36 - 2 * ram[44]
    # radar typings == ram 16, where 0 == NoObject, 26 == lander, 29 == swarm, 55 == humanoid-lander, 136 == bomber, 143 == baiter, 255 == pod, 
    # radar index == ram 59

    if ram_state[16]:
        if type(objects[27+ram_state[59]]) is NoObject:
            if ram_state[16] == 26:
                objects[27+ram_state[59]] = Radar_Lander()
            elif ram_state[16] == 29:
                objects[27+ram_state[59]] = Radar_Swarm()
            elif ram_state[16] == 55:
                objects[27+ram_state[59]] = Radar_Humanoide_Lander()
            elif ram_state[16] == 136:
                objects[27+ram_state[59]] = Radar_Bomber()
            elif ram_state[16] == 143:
                objects[27+ram_state[59]] = Radar_Baiter()
            elif ram_state[16] == 255:
                objects[27+ram_state[59]] = Radar_Pod()

        objects[27+ram_state[59]].xy = ram_state[40], 36 - 2 * ram_state[44]
    else:
        objects[27+ram_state[59]] = NoObject()

    if ram_state[78] < 5:
        if ram_state[41]:
            if type(objects[35+ram_state[78]]) is NoObject:
                objects[35+ram_state[78]] = Radar_Human()
            objects[35+ram_state[78]].xy = ram_state[41], 35 - 2 * ram_state[42]
        else:
            objects[35+ram_state[78]] = NoObject()
    elif ram_state[78] == 255:
        if type(objects[26]) is NoObject:
            objects[26] = Radar_Player()
        objects[26].xy = ram_state[41], 35 - 2 * ram_state[42]

    if hud:
        x, w = 88, 14
        for i in range(4):
            if ram_state[30+i] != 170:
                x-=8
                w+=8
        objects[-3].xy = x, 177
        objects[-3].wh = w, 7
        objects[-3].value = sum([10**(2+i)*(ram_state[30+i]&15) if ram_state[30+i] < 170 else 0 for i in range(4)]) + (ram_state[29]&15) * 10

        if ram_state[66]:
            lives = ram_state[66] if ram_state[66] < 4 else 3
            objects[-2].wh = 7 + (lives-1) * 16, 5
            objects[-2].value = ram_state[66]

        if ram_state[68]:
            bombs = ram_state[68] if ram_state[68] < 4 else 3
            objects[-1].wh = 6 + (bombs-1) * 16, 3
            objects[-1].value = ram_state[68]
        else:
            objects[-1].wh = 0, 0
            objects[-1].value = 0


