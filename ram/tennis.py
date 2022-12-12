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
    print("TODO: separate object based on orientation")
    if True:  # player up
        objects["enemy"] = ram_state[27]-1, 166-ram_state[25], 16, 22, 117, 128, 240 # DOWN player
        objects["player"] = ram_state[26]-1, 166-ram_state[24], 16, 22, 240, 128, 128 # UP player
        objects["ball"] = ram_state[16]-2, 189-ram_state[54], 2, 2, 236, 236, 236
        info["objects"] = objects
    else:  # player down
        pass
