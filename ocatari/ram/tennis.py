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
    objects["logo"] = 39, 193, 33, 7, 240, 128, 128
    field_orientation = ram_state[80]  # stores the orientation of the field
    if field_orientation == 0:  # player up
        objects["enemy"] = ram_state[27]-1, 166-ram_state[25], 16, 22, 117, 128, 240  # DOWN player
        objects["player"] = ram_state[26]-1, 166-ram_state[24], 16, 22, 240, 128, 128  # UP player
    elif field_orientation == 1:  # player down
        objects["player"] = ram_state[27]-1, 166-ram_state[25], 16, 22, 240, 128, 128  # UP player
        objects["enemy"] = ram_state[26]-1, 166-ram_state[24], 16, 22, 117, 128, 240  # DOWN player
    else:
        raise TypeError("Couldn't find the game field_orientation")
    enemy_score = min(15 * ram_state[70], 40)
    player_score = min(15 * ram_state[69], 40)
    # enemy_sets = ram_state[72]
    if enemy_score == 0:
        objects["enemy_scores"] = 113, 5, 6, 7, 117, 128, 240
    elif enemy_score == 15:
        objects["enemy_scores"] = 106, 5, 13, 7, 117, 128, 240
    else:  # 30 or 40
        objects["enemy_scores"] = 105, 5, 14, 7, 117, 128, 240
    if player_score == 0:
        objects["player_score"] = 49, 5, 6, 7, 240, 128, 128
    elif player_score == 15:
        objects["player_score"] = 42, 5, 13, 7, 240, 128, 128
    else:  # 30 or 40
        objects["player_score"] = 41, 5, 14, 7, 240, 128, 128
    bx, by = ram_state[16]-2, 190-ram_state[54]
    if by < 99:
        by -= 1
    if bx < 32 or bx > 127 or by < 99 or by > 112:  # not behind the net
        objects["ball"] = bx, by, 2, 2, 236, 236, 236
    b_shadow_x = ram_state[16]-2
    b_shadow_y = 190-ram_state[55]
    if b_shadow_y < 99:
        b_shadow_y -= 1
    if b_shadow_x < 32 or b_shadow_x > 127 or b_shadow_y < 99 or \
            b_shadow_y > 112 or (b_shadow_x == bx and b_shadow_y == by):  # not behind the net
        objects["ball_shadow"] = b_shadow_x, b_shadow_y, 2, 2, 74, 74, 74
    info["objects"] = objects
