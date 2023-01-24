from ._helper_methods import _convert_number
from .game_objects import GameObject

"""
RAM extraction for the game KANGUROO. Supported modes: raw, revised.

"""

class Kangaroo(GameObject):
    def __init__(self):
        super(Kangaroo, self).__init__()
        self.visible = True
        self._xy = 78, 103
        self.wh = 9, 10
        self.rgb = 223, 183, 85
        self.hud = False


class Enemy(GameObject):
    def __init__(self, *args, **kwargs):
        super(Enemy, self).__init__()
        super().__init__(*args, **kwargs)
        self.visible = True
        self._xy = 79, 57
        self.wh = 9, 10
        self.rgb = 227,159,89
        self.hud = False


class Fruit(GameObject):
    def __init__(self, *args, **kwargs):
        super(Fruit, self).__init__()
        self.visible = True
        self._xy = 125, 173
        self.wh = 9, 10
        self.rgb = 214, 92, 92
        self.hud = False


class Bell(GameObject):
    def __init__(self, *args, **kwargs):
        super(Bell, self).__init__()
        self.visible = True
        self._xy = 125, 173
        self.wh = 9, 10
        self.rgb = 210, 164, 74
        self.hud = False


class Score(GameObject):
    def __init__(self, *args, **kwargs):
        super(Score, self).__init__()
        self.visible = True
        self._xy = 95, 187
        self.wh = 7, 7
        self.rgb = 160, 171, 79
        self.hud = True


class Life(GameObject):
    def __init__(self, *args, **kwargs):
        super(Life, self).__init__()
        self.visible = True
        self._xy = 12, 171
        self.wh = 9, 10
        self.rgb = 160, 171, 79
        self.hud = True


def _init_objects_kangaroo_ram(hud=False):
    """
    (Re)Initialize the objects
    """

    objects = [Kangaroo(), Enemy(), Enemy(), Enemy(), Fruit(), Fruit(), Fruit(), Bell()]

    # if hud:
    #     x = 95
    #     for i in range(6):
    #         score = Score()
    #         score.xy = x, 187
    #         objects.append(score)
    #         x -= 8

    #     x = 12
    #     for i in range(3):
    #         life = Life()
    #         life.xy = x, 173
    #         objects.append(life)
    #         x += 15
    #     objects.append(Fruit())

    return objects


def _detect_objects_kangaroo_revised(objects, ram_state, hud=True):
    # player, g1, g2, g3, g4, fruit = objects[:6]

    # player.xy = ram_state[10] - 13, ram_state[16] + 1

    # g1.xy = ram_state[6] - 13, ram_state[12] + 1
    # g1.rgb = 180, 122, 48
    # g2.xy = ram_state[7] - 13, ram_state[13] + 1
    # g2.rgb = 84, 184, 153
    # g3.xy = ram_state[8] - 13, ram_state[14] + 1
    # g3.rgb = 198, 89, 179
    # g4.xy = ram_state[9] - 13, ram_state[15] + 1
    # # no rgb adjustment, since this colour is the default one

    # if ram_state[11] > 0 and ram_state[17] > 0:
    #     fruit.xy = ram_state[11] - 13, ram_state[17] + 1
    #     fruit.rgb = get_fruit_rgb(ram_state[123])
    # else:
    #     fruit.visible = False

    # if hud:
    #     if ram_state[122] < 16:
    #         objects[11].visible = False
    #         if ram_state[122] == 0:
    #             objects[10].visible = False
    #             if ram_state[121] < 16:
    #                 objects[9].visible = False
    #                 if ram_state[121] == 0:
    #                     objects[8].visible = False
    #                     if ram_state[120] < 16:
    #                         objects[7].visible = False

    #     if ram_state[123] <= 2:
    #         objects[14].visible = False
    #         if ram_state[123] <= 1:
    #             objects[13].visible = False
    #             if ram_state[123] == 0:
    #                 objects[12].visible = False

    #     objects[15].rgb = get_fruit_rgb(ram_state[123])
    pass



def _detect_objects_kangaroo_raw(info, ram_state):

    info["player_position"] = ram_state[17], ram_state[16] * 10
    info["player_movable"] = True if ram_state[124] == 188 else False
    info["kangaroo_child"] = ram_state[83]


def _augment_info_kangaroo_revised(info, ram_state):

    """
    For all 3 objects:
    (x, y, w, h, r, g, b)
    """
    objects = {}

    info["time"] = _convert_number(ram_state[59]) * 100
    info["score"] = _convert_number(ram_state[39]) * 10000 + _convert_number(ram_state[40]) * 100
    info["lives"] = ram_state[45]
    info["level"] = ram_state[36]  # total of 3 levels: 0,1 and 2

    info["player_position"] = ram_state[17], ram_state[16] * 10
    info["player_movable"] = True if ram_state[124] == 188 else False
    info["kangaroo_child"] = ram_state[83]

    info["fruit_1_type"] = _get_fruit_type_kangaroo(ram_state[42])  # top
    info["fruit_1_position"] = ram_state[81]
    info["fruit_2_type"] = _get_fruit_type_kangaroo(ram_state[43])  # mid
    info["fruit_2_position"] = ram_state[80]
    info["fruit_3_type"] = _get_fruit_type_kangaroo(ram_state[44])  # low
    info["fruit_3_position"] = ram_state[79]

    info["monkey_1_throw"] = ram_state[118]  # 255 = no throw, 21 = throwing animation, 0 = throw
    info["monkey_1_position"] = ram_state[15], ram_state[11] * 10  # times 10 is still a guess

    info["bouncing_apple_position"] = ram_state[34], ram_state[33] * 10
    info["monkey_apple_position"] = ram_state[28], ram_state[25]  # one state for all apples thrown by monkeys

    info["bell_position"] = ram_state[82]

    info["monkey_sprite"] = ram_state[3]  # or ram_state[7]
    info["player_sprite"] = ram_state[54]
    info["player_movement"] = ram_state[72]
    info["ticker"] = ram_state[57]  # Game starts when this state reaches 158

    info["objects"] = objects


def _get_fruit_type_kangaroo(ram_state):
    if ram_state < 128:
        if ram_state % 4 == 0:
            return "Strawberry"
        elif ram_state % 4 == 1:
            return "Apple"
        elif ram_state % 4 == 2:
            return "Cherry"
        elif ram_state % 4 == 3:
            return "Pineapple"
    else:
        return None
