def _augment_info_tennis_raw(info, ram_state):
    """
    returns unprocessed list with
    ball_x, ball_y, enemy_y, player_y
    """
    info["objects_list"] = ram_state[32:36]


def _augment_info_tennis_revised(info, ram_state):
    """
    For all 3 objects:
    (x, y, w, h, r, g, b)
    """
    objects = {}
    # objects["enemy"] = ram_state[27]+0, ram_state[25], 14, 46, 0, 0, 0
    # objects["player"] = ram_state[26], ram_state[24], 14, 46, 214, 214, 214
    objects["ball"] = ram_state[16], ram_state[17], 5, 5, 236, 236, 236
    info["objects"] = objects
