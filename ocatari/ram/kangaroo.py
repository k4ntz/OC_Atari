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

    info["fruit_1"] = _get_fruit_type_kangaroo(ram_state[42])  # top
    info["fruit_2"] = _get_fruit_type_kangaroo(ram_state[43])  # mid
    info["fruit_3"] = _get_fruit_type_kangaroo(ram_state[44])  # low

    info["monkey_sprite"] = ram_state[3]  # or ram_state[7]
    info["player_sprite"] = ram_state[54]
    info["ticker"] = ram_state[57] # Game starts when this state reaches 158

    info["objects"] = objects

def _get_fruit_type_kangaroo(ram_state):
    if ram_state < 128:
        if ram_state%4 == 0:
            return "Strawberry"
        elif ram_state%4 == 1:
            return "Apple"
        elif ram_state%4 == 2:
            return "Cherry"
        elif ram_state%4 == 3:
            return "Pineapple"
    else:
        return None
