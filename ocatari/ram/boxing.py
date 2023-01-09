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
    objects["enemy_score"] = 111, 5, 6, 7, 0, 0, 0
    if ram_state[19] < 10:
        objects["enemy_score2"] = 0, 0, 0, 0, 0, 0, 0
    else:
        objects["enemy_score2"] = 103, 5, 6, 7, 0, 0, 0
    objects["player"] = ram_state[32]+5, ram_state[34]+38, 14, 46, 214, 214, 214
    objects["player_score"] = 47, 5, 6, 7, 214, 214, 214
    if ram_state[18] < 10:
        objects["player_score2"] = 0, 0, 0, 0, 0, 0, 0
    else:
        objects["player_score2"] = 39, 5, 6, 7, 214, 214, 214
    objects["logo"] = 62, 189, 32, 7, 20, 60, 0
    objects["time1"] = 63, 17, 6, 7, 20, 60, 0
    objects["time2"] = 73, 18, 2, 5, 20, 60, 0
    objects["time3"] = 79, 17, 6, 7, 20, 60, 0
    objects["time4"] = 87, 17, 6, 7, 20, 60, 0
    info["objects"] = objects
