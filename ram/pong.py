def _augment_info_pong_raw(info, ram_state):
    """
    returns unprocessed list with
    ball_x, ball_y, enemy_y, player_y
    """
    info["objects_list"] = [ram_state[49], ram_state[54], ram_state[50], ram_state[51]]


def _augment_info_pong_revised(info, ram_state):
    """
    For all 3 objects:
    (x, y, w, h, r, g, b)
    """
    objects = {}
    # set defauld coord if object does not exist
    x, y = 0, 0
    if ram_state[54] != 0:  # otherwise no ball
        x, y = ram_state[49]-49, ram_state[54]-14
    objects["ball"] = x, y, 2, 3, 236, 236, 236
    # same for enemy
    x, y = 0, 0
    if ram_state[50] != 0:  # otherwise no enemy
        x, y = 16, ram_state[50]-15
    objects["enemy"] = x, y, 4, 15, 213, 130, 74
    objects["player"] = 140, ram_state[51]-13, 4, 15, 92, 186, 92
    info["objects"] = objects
