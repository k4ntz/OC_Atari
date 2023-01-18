from ._helper_methods import _convert_number

"""
RAM extraction for the game KANGUROO. Supported modes: raw, revised.

"""

def _augment_info_kangaroo_raw(info, ram_state):
    pass


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
