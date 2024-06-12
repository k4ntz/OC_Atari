from .game_objects import GameObject
from ._helper_methods import _convert_number
import math
import sys


MAX_NB_OBJECTS = {"Player" :  1, "Enemy": 8, "Reward" : 8, "Consumable" : 8}
MAX_NB_OBJECTS_HUD = {"Player" :  1, "Enemy": 8, "Reward" : 8, "Consumable" : 8, "Score" : 1}


class Player(GameObject):
    def __init__(self):
        super().__init__()
        self.rgb = 187, 187, 53
        self._xy = 0, 0
        self.wh = 8, 11  # at some point 16, 11. advanced other player (obelix) is (6, 11)
        self.hud = False

class Enemy(GameObject):
    def __init__(self):
        super().__init__()
        self.rgb = 228, 111, 111
        self._xy = 0, 0
        self.wh = 7, 11
        self.hud = False


class Score(GameObject):
    def __init__(self):
        super().__init__()
        self.rgb = 187, 187, 53
        self._xy = 0, 0
        self.wh = 8, 11
        self.hud = True
        self.value = 0


class Lives(GameObject):
    def __init__(self):
        super().__init__()
        self.rgb = 187, 187, 53
        self._xy = 0, 0
        self.wh = 6, 7
        self.hud = True

class Consumable(GameObject):
    def __init__(self):
        super().__init__()
        self.rgb = 200, 200, 200 #can have different colors
        self._xy = 0, 0
        self.wh = 7, 11
        self.hud = False

class Reward(GameObject):
    def __init__(self):
        super().__init__()
        self.rgb = 200, 200, 200 #can have different colors
        self._xy = 0, 0
        self.wh = 8, 11
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


def _init_objects_ram(hud=False):
    """
    (Re)Initialize the objects
    """
    objects = [Player()]
    if hud:
        objects.extend([Score(), Lives(), Lives()])

    objects += [None for i in range(8)]
    return objects


def _detect_objects_asterix_raw(info, ram_state):
    info["x_positions"] = ram_state[41:50]  # 41 for player, 42 for obj in upper lane...
    info["y_player"] = ram_state[39]  # from 0 to 7 (8 lanes)
    info["score"] = ram_state[94:97]  # on ram in decimal/ on screen in hex(like other 2 games)
    info["score_dec"] = ram_state[94:97]
    info["lives"] = ram_state[83]
    info["kind_of_visible_objs"] = ram_state[54] % 8
    info["rewards_visible"] = ram_state[73:81]
    info["enemy_or_eatable_object"] = ram_state[29:37] % 2  # = 1 for enemy

    # info["maybe_useful"] = ram_state[10:18], ram_state[40], ram_state[19:27], ram_state[29:37], ram_state[87],
    # ram_state[7]
    # not known what they are for exactly

def _detect_objects_ram(objects, ram_state, hud=False):
    # player
    player = objects[0]
    player.xy = ram_state[41], 26 + ram_state[39] * 16
    if ram_state[71] < 82:
        if ram_state[54] < 5:  # asterix playing
            player.wh = 8, 11
        else:  # obelix playing
            player.wh = 6, 11
    else:  # player is wide (is dying)
        player.wh = 16, 11

    lives_nr = ram_state[83]
    #reward_class = (Reward50, Reward100, Reward200, Reward300, Reward400, Reward500)  # , Reward500, Reward500)
    #eatable_class = (Cauldron, Helmet, Shield, Lamp, Apple, Fish, Meat, Mug)
    # get lanes
    if hud:
        offset = 1 + lives_nr
    else:
        offset = 1
    lanes = objects[offset:]
    #const = ram_state[54] % 8
    reward_lanes = []
    for i in range(8):
        if ram_state[18-i] == 11:
            objects[offset + i] = None
        elif ram_state[73 + i]:  # set to lane number if there is reward in that lane
            reward_lanes.append(i)  # 0-7 instead actual 1-8
            if type(lanes[i]) is not Reward:
                rew = Reward()
                objects[offset + i] = rew
            else:
                rew = lanes[i]
            rew.xy = ram_state[42 + i], 26 + i * 16
        elif ram_state[29 + i] % 2 == 1:
            if not isinstance(lanes[i], Enemy):
                en = Enemy()
                objects[offset + i] = en
            else:
                en = lanes[i]
            en.xy = ram_state[42 + i], 26 + i * 16
        else:
            if type(lanes[i]) is not Consumable:
                instance = Consumable()
                objects[offset + i] = instance
            else:
                instance = lanes[i]
            instance.xy = ram_state[42 + i] + 1, 26 + i * 16 + 1
    
    if hud:
        score = objects[1]
        dec_value = _convert_number(ram_state[94]) * 10000 + _convert_number(ram_state[95]) * 100 + _convert_number(
            ram_state[96])
        score.value = dec_value
        if dec_value == 0:
            score.xy = 96, 184
            score.wh = 6, 7
        else:
            digits = int(math.log10(dec_value))
            score.xy = 96 - digits * 8, 184
            score.wh = 6 + digits * 8, 7
        if lives_nr >= 2:
            lives = objects[2]
            if lives is None:
                lives = Lives()
                objects[2] = lives
            lives.xy = 60, 169
            lives.wh = 8, 11
        elif isinstance(objects[2], Lives):
            del objects[2]
        if lives_nr >= 3:
            lives = objects[3]
            if lives is None:
                lives = Lives()
                objects[3] = lives
            lives.xy = 60 + 16, 169
            lives.wh = 8, 11
        elif isinstance(objects[3], Lives):
            del objects[3]
