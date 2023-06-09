from .game_objects import GameObject
from ._helper_methods import _convert_number
import math
import sys

# not sure about this one TODO: validate
MAX_NB_OBJECTS =  {'Player': 1, 'Ghost': 4}
MAX_NB_OBJECTS_HUD =  {'Player': 1, 'Ghost': 4, 'Fruit': 1, 'Score': 3, 'Life': 2}

class Player(GameObject):
    def __init__(self):
        super(Player, self).__init__()
        self._xy = 78, 103
        self.wh = 9, 10
        self.rgb = 210, 164, 74
        self.hud = False


class Ghost(GameObject):
    def __init__(self):
        super(Ghost, self).__init__()
        super().__init__()
        self._xy = 79, 57
        self.wh = 9, 10
        self.rgb = 200, 72, 72
        self.hud = False


class Fruit(GameObject):
    def __init__(self):
        super(Fruit, self).__init__()
        self._xy = 125, 173
        self.wh = 9, 10
        self.rgb = 184, 50, 50
        self.hud = False


class Score(GameObject):
    def __init__(self):
        super(Score, self).__init__()
        self._xy = 95, 187
        self.wh = 7, 7
        self.rgb = 195, 144, 61
        self.hud = True


class Life(GameObject):
    def __init__(self):
        super(Life, self).__init__()
        self._xy = 12, 171
        self.wh = 7, 10
        self.rgb = 187, 187, 53
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

def _create_score_from_number(number):
    """
    returns a list a list with number * Score objects at the correct position
    """
    score = 1
    if number > 0:
        score = int(math.log10(number)) + 1

    ret = []
    x = 95
    for i in range(score):
        score = Score()
        score.xy = x, 187
        ret.append(score)
        x -= 8
    return ret


def _create_lifes_from_number(number):
    """
    returns a list a list with number * Life objects at the correct position
    """
    ret = []
    x = 12
    for i in range(number):
        life = Life()
        life.xy = x, 173
        ret.append(life)
        x += 15
    return ret


def _init_objects_mspacman_ram(hud=False):
    """
    (Re)Initialize the objects
    """

    objects = [Player(), Ghost(), Ghost(), Ghost(), Ghost()]

    if hud:
        objects.append(Fruit())
        objects.extend(_create_score_from_number(100000))

        objects.extend(_create_lifes_from_number(3))

    return objects


def _detect_objects_mspacman_revised(objects, ram_state, hud=True):
    player, g1, g2, g3, g4 = objects[:5]
    if hud:
        fruit_hud = objects[5]
        fruit_hud.rgb = get_fruit_rgb(ram_state[123])

    player.xy = ram_state[10] - 13, ram_state[16] + 1

    g1.xy = ram_state[6] - 13, ram_state[12] + 1
    g1.rgb = 180, 122, 48
    g2.xy = ram_state[7] - 13, ram_state[13] + 1
    g2.rgb = 84, 184, 153
    g3.xy = ram_state[8] - 13, ram_state[14] + 1
    g3.rgb = 198, 89, 179
    g4.xy = ram_state[9] - 13, ram_state[15] + 1
    # no rgb adjustment, since this colour is the default one

    objects.clear()
    objects.extend([player, g1, g2, g3, g4])
    if hud:
        objects.append(fruit_hud)

    if ram_state[11] > 0 and ram_state[17] > 0:
        fruit = Fruit()
        fruit.xy = ram_state[11] - 13, ram_state[17] + 1
        fruit.rgb = get_fruit_rgb(ram_state[123])
        objects.append(fruit)

    if hud:
        score = _convert_number(ram_state[122]) * 10000 + _convert_number(ram_state[121]) * 100 +\
                _convert_number(ram_state[120])
        sc = Score()
        nb_digits = len(str(score))
        sc.xy = 103 - 8 * nb_digits, 187
        sc.wh = nb_digits * 8 - 1, 7
        objects.append(sc)
        # if ram_state[122] < 16:
        #     objects[11].visible = False
        #     if ram_state[122] == 0:
        #         objects[10].visible = False
        #         if ram_state[121] < 16:
        #             objects[9].visible = False
        #             if ram_state[121] == 0:
        #                 objects[8].visible = False
        #                 if ram_state[120] < 16:
        #                     objects[7].visible = False

        lifes = _create_lifes_from_number(ram_state[123])
        objects.extend(lifes)


def _detect_objects_mspacman_raw(info, ram_state):
    """
    returns unprocessed list with
    player_x, player_y, ghosts_position_x, enemy_position_y, fruit_x, fruit_y
    """
    object_info = {}
    object_info["player_x"] = ram_state[10]
    object_info["player_y"] = ram_state[16]
    object_info["enemy_amount"] = ram_state[19]
    object_info["ghosts_position_x"] = {"orange": ram_state[6],
                                        "cyan": ram_state[7],
                                        "pink": ram_state[8],
                                        "red": ram_state[9]
                                        }
    object_info["enemy_position_y"] = {"orange": ram_state[12],
                                       "cyan": ram_state[13],
                                       "pink": ram_state[14],
                                       "red": ram_state[15]
                                       }
    object_info["fruit_x"] = ram_state[11]
    object_info["fruit_y"] = ram_state[17]
    info["object-list"] = object_info


def get_fruit_rgb(ram_state):

    """
    every value of 112 and above will result in a glitched fruit
    """

    if ram_state < 16:
        return 184, 50, 50   # "cherry"
    elif ram_state < 32:
        return 184, 50, 50   # "strawberry"
    elif ram_state < 48:
        return 198, 108, 58  # "orange"
    elif ram_state < 64:
        return 162, 162, 42  # "pretzel"
    elif ram_state < 80:
        return 184, 50, 50   # "apple"
    elif ram_state < 96:
        return 110, 156, 66  # "pear"
    elif ram_state < 112:
        return 198, 108, 58  # "banana"
