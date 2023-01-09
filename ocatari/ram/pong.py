def _augment_info_pong_raw(info, ram_state):
    """
    returns unprocessed list with
    ball_x, ball_y, enemy_y, player_y
    """
    info["objects_list"] = [ram_state[49], ram_state[54], ram_state[50], ram_state[51]]


def _augment_info_pong_revised(info, ram_state, hud=False):
    """
    For all 3 objects:
    (x, y, w, h, r, g, b)
    """
    objects = {}
    enemy_score = ram_state[13]
    player_score = ram_state[14]
    # set defauld coord if object does not exist
    if ram_state[54] != 0:  # otherwise no ball
        objects["ball"] = ram_state[49]-49, ram_state[54]-14, 2, 3, 236, 236, 236
    else:
        objects["ball"] = (0, 0, 0, 0, 0, 0, 0)
    # same for enemy
    if ram_state[50] > 18 or ram_state[50] != 0:  # otherwise no enemy
        objects["enemy"] = 16, ram_state[50]-15, 4, 15, 213, 130, 74
    else:
        objects["enemy"] = (0, 0, 0, 0, 0, 0, 0)
    objects["player"] = 140, ram_state[51]-13, 4, 15, 92, 186, 92
    if hud:
        # scores
        if ram_state[13] < 10: # enemy score
            objects["enemy_score"] = 0, 0, 0, 0, 0, 0, 0
        else:
            objects["enemy_score"] = 20, 1, 12, 20, 213, 130, 74
        objects["enemy_score_2"] = 36, 1, 12, 20, 213, 130, 74
        if ram_state[14] < 10: # player score
            objects["player_score"] = (0, 0, 0, 0, 0, 0, 0)
        else:
            objects["player_score"] = 100, 1, 12, 20, 92, 186, 92
        objects["player_score_2"] = 116, 1, 12, 20, 92, 186, 92
    info["objects"] = objects
