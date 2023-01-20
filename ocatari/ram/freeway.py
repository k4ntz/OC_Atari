from ._helper_methods import _convert_number


def _detect_objects_freeway_raw(info, ram_state):
    info["chicken1_y"] = ram_state[14]
    info["chicken2_y"] = ram_state[15]
    info["score1"] = _convert_number(ram_state[103])
    info["score2"] = _convert_number(ram_state[104])
    info["car_x"] = ram_state[108:117]


car_colors = {"car1": [167, 26, 26], "car2": [180, 231, 117], "car3": [105, 105, 15],
              "car4": [228, 111, 111], "car5": [24, 26, 167], "car6": [162, 98, 33],
              "car7": [84, 92, 214], "car8": [184, 50, 50], "car9": [135, 183, 84],
              "car10": [210, 210, 64]
              }


def _detect_objects_freeway_revised(info, ram_state):
    """
    For all objects:
    (x, y, w, h, r, g, b)
    """
    objects = {}

    y = 27
    for i in range(10):
        cstr = "car" + str(i + 1)
        r, g, b = car_colors[cstr]
        objects[cstr] = ram_state[117 - i] - 2, y, 7, 10, r, g, b
        y += 16

    objects["chicken1"] = 44, 193 - ram_state[14], 6, 8, 252, 252, 84
    objects["chicken2"] = 108, 193 - ram_state[15], 6, 8, 252, 252, 84

    info["objects"] = objects
