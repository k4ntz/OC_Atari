def _augment_info_boxing_raw(info, ram_state):
    """
    returns unprocessed list with
    ball_x, ball_y, enemy_y, player_y
    """
    info["objects_list"] = ram_state[32:36]


def _augment_info_boxing_revised(info, ram_state):
    """
    For all 3 objects:
    (x, y, w, h, r, g, b)
    """
    objects = {}
    objects["enemy"] = ram_state[33]+4, ram_state[35]+38, 14, 46, 0, 0, 0
    objects["player"] = ram_state[32]+5, ram_state[34]+38, 14, 46, 214, 214, 214
    info["objects"] = objects
