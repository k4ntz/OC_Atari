from .game_objects import GameObject
from ._helper_methods import _convert_number
import math
import sys


MAX_NB_OBJECTS = {"Player":  1, "Enemy": 8,
                  "Reward50": 8, "Reward100": 8, "Reward200": 8, "Reward300": 8, "Reward400": 8, "Reward500": 8,
                  "Cauldron": 8, "Helmet": 8, "Shield": 8, "Lamp": 8, "Apple": 8, "Fish": 8, "Meat": 8, "Mug": 8}

MAX_NB_OBJECTS_HUD = {"Player":  1, "Enemy": 8,
                      "Reward50": 8, "Reward100": 8, "Reward200": 8, "Reward300": 8, "Reward400": 8, "Reward500": 8,
                      "Cauldron": 8, "Helmet": 8, "Shield": 8, "Lamp": 8, "Apple": 8, "Fish": 8, "Meat": 8, "Mug": 8,
                      "Score": 1}


class Player(GameObject):
    def __init__(self):
        super().__init__()
        self.rgb = 187, 187, 53
        self._xy = 0, 0
        # at some point 16, 11. advanced other player (obelix) is (6, 11)
        self.wh = 8, 11
        self.hud = False


class Cauldron(GameObject):
    def __init__(self):
        super().__init__()
        self.rgb = 167, 26, 26
        self._xy = 0, 0
        self.wh = 7, 10
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


class Lives(GameObject):
    def __init__(self):
        super().__init__()
        self.rgb = 187, 187, 53
        self._xy = 0, 0
        self.wh = 6, 7
        self.hud = True


class Helmet(GameObject):
    def __init__(self):
        super().__init__()
        self.rgb = 240, 128, 128
        self._xy = 0, 0
        self.wh = 7, 11
        self.hud = False


class Shield(GameObject):
    def __init__(self):
        super().__init__()
        self.rgb = 214, 214, 214
        self._xy = 0, 0
        self.wh = 5, 11
        self.hud = False


class Lamp(GameObject):
    def __init__(self):
        super().__init__()
        self.rgb = 187, 53, 53
        self._xy = 0, 0
        self.wh = 8, 11
        self.hud = False


class Apple(GameObject):
    def __init__(self):
        super().__init__()
        self.rgb = 184, 50, 50
        self._xy = 0, 0
        self.wh = 8, 11
        self.hud = False


class Fish(GameObject):
    def __init__(self):
        super().__init__()
        self.rgb = 198, 89, 179
        self._xy = 0, 0
        self.wh = 8, 5
        self.hud = False


class Meat(GameObject):
    def __init__(self):
        super().__init__()
        self.rgb = 184, 50, 50
        self._xy = 0, 0
        self.wh = 5, 11
        self.hud = False


class Mug(GameObject):
    def __init__(self):
        super().__init__()
        self.rgb = 184, 50, 50
        self._xy = 0, 0
        self.wh = 7, 11
        self.hud = False


class Reward50(GameObject):
    def __init__(self):
        super().__init__()
        self.rgb = 198, 89, 179
        self._xy = 0, 0
        self.wh = 6, 11
        self.hud = False


class Reward100(GameObject):
    def __init__(self):
        super().__init__()
        self.rgb = 135, 183, 84
        self._xy = 0, 0
        self.wh = 8, 11
        self.hud = False


class Reward200(GameObject):
    def __init__(self):
        super().__init__()
        self.rgb = 195, 144, 61
        self._xy = 0, 0
        self.wh = 8, 11
        self.hud = False


class Reward300(GameObject):
    def __init__(self):
        super().__init__()
        self.rgb = 213, 130, 74
        self._xy = 0, 0
        self.wh = 8, 11
        self.hud = False


class Reward400(GameObject):
    def __init__(self):
        super().__init__()
        self.rgb = 135, 183, 84
        self._xy = 0, 0
        self.wh = 8, 11
        self.hud = False


class Reward500(GameObject):
    def __init__(self):
        super().__init__()
        self.rgb = 163, 57, 21
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


def _init_objects_asterix_ram(hud=False):
    """
    (Re)Initialize the objects
    """
    objects = [Player()]
    if hud:
        objects.extend([Score(), Lives(), Lives()])

    objects += [None for i in range(8)]
    return objects


def _detect_objects_asterix_raw(info, ram_state):
    # 41 for player, 42 for obj in upper lane...
    info["x_positions"] = ram_state[41:50]
    info["y_player"] = ram_state[39]  # from 0 to 7 (8 lanes)
    # on ram in decimal/ on screen in hex(like other 2 games)
    info["score"] = ram_state[94:97]
    info["score_dec"] = ram_state[94:97]
    info["lives"] = ram_state[83]
    info["kind_of_visible_objs"] = ram_state[54] % 8
    info["rewards_visible"] = ram_state[73:81]
    info["enemy_or_eatable_object"] = ram_state[29:37] % 2  # = 1 for enemy

    # info["maybe_useful"] = ram_state[10:18], ram_state[40], ram_state[19:27], ram_state[29:37], ram_state[87],
    # ram_state[7]
    # not known what they are for exactly


def _detect_objects_asterix_revised(objects, ram_state, hud=False):
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
    player.rgb = 187, 187, 53

    lives_nr = ram_state[83]
    reward_class = (Reward50, Reward100, Reward200, Reward300,
                    Reward400, Reward500)  # , Reward500, Reward500)
    eatable_class = (Cauldron, Helmet, Shield, Lamp, Apple, Fish, Meat, Mug)
    # get lanes
    if hud:
        offset = 1 + lives_nr
    else:
        offset = 1
    lanes = objects[offset:]
    const = ram_state[54] % 8
    reward_lanes = []
    for i in range(8):
        if ram_state[18-i] == 11:
            objects[offset + i] = None
        elif ram_state[73 + i]:  # set to lane number if there is reward in that lane
            reward_lanes.append(i)  # 0-7 instead actual 1-8
            if type(lanes[i]) not in reward_class:
                if const == 0:  # 50 reward
                    rew = Reward50()
                elif const == 1:  # 100 reward
                    rew = Reward100()
                elif const == 2:  # 200 reward
                    rew = Reward200()
                elif const == 3:  # 300 reward
                    rew = Reward300()
                elif const == 4:  # 400 reward
                    rew = Reward400()
                else:  # 500 reward
                    rew = Reward500()
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
            if type(lanes[i]) not in eatable_class:
                if const == 0:
                    instance = Cauldron()
                elif const == 1:
                    instance = Helmet()
                elif const == 2:
                    instance = Shield()
                elif const == 3:
                    instance = Lamp()
                elif const == 4:
                    instance = Apple()
                elif const == 5:
                    instance = Fish()
                elif const == 6:
                    instance = Meat()
                elif const == 7:
                    instance = Mug()
                objects[offset + i] = instance
            else:
                instance = lanes[i]
            instance.xy = ram_state[42 + i] + 1, 26 + i * 16 + 1

    if hud:
        score = objects[1]
        dec_value = _convert_number(ram_state[94]) * 10000 + _convert_number(ram_state[95]) * 100 + _convert_number(
            ram_state[96])
        if dec_value == 0:
            score.xy = 96, 184
            score.wh = 6, 7
        else:
            digits = int(math.log10(dec_value))
            score.xy = 96 - digits * 8, 184
            score.wh = 6 + digits * 8, 7

        if lives_nr >= 2:
            lives = objects[2]
            lives.xy = 60, 169
            lives.wh = 8, 11
        elif isinstance(objects[2], Lives):
            del objects[2]
        if lives_nr >= 3:
            lives = objects[3]
            lives.xy = 60 + 16, 169
            lives.wh = 8, 11
        elif isinstance(objects[3], Lives):
            del objects[3]
