def _init_objects_space_invaders_ram(hud=False):
    """
    (Re)Initialize the objects
    """
    objects = []
    if hud:
        objects.extend([])
    return objects


def _detect_objects_space_invaders_raw(info, ram_state):
    info["aliens"] = ram_state[16:24]
    info["x_positions"] = ram_state[26:31]
    info["walls"] = ram_state[43:69]
    info["lives"] = ram_state[73]
    info["bullet_1_enemy_y"] = ram_state[81:89]
    info["score"] = ram_state[102:106]  # score is saved in hexadecimal

    print(ram_state)


def _detect_objects_space_invaders_revised(info, ram_state):
    info["aliens_y"] = ram_state[16] % 32  # taking only the first 5 bits on the right
    # ram_state[16] has also y of frame of players with walls together

    info["number_enemies"] = ram_state[17]  # number of alive aliens. if they are less the make the game quicker

    # positions of enemies from left to right are the individual, set bits from right to left
    # rows are counted from bottom
    # the two msb-bits are to be discarded. they remain 0
    info["row_1"] = ram_state[18]  #
    info["row_2"] = ram_state[19]  #
    info["row_3"] = ram_state[20]  #
    info["row_4"] = ram_state[21]  #
    info["row_5"] = ram_state[22]  #
    info["row_6"] = ram_state[23]  #
    # ram[32:38] have the same value as ram[17:23] initialized. sense still not known

    info["visibility_players_walls"] = ram_state[24]

    info["aliens_x"] = ram_state[26]  # x of all aliens is common
    info["walls_x"] = ram_state[27]  # wall_left is reference
    info["player_green_x"] = ram_state[28]  # begins with 35. (0 < player_x < 255)
    info["player_yellow_x"] = ram_state[29]  # begins with 117. (0 < player_x < 255)
    info["satellite_dish_x"] = ram_state[30]

    info["graphics"] = ram_state[42]  # graphics of players being destroyed and visibility of score

    info["walls"] = ram_state[43:69]  # the 3 walls. they are represented in the same order as in the ram(from left
    # to right)
    info["wall_left"] = ram_state[43:51]  # represented row by row in ram as single cell by another in same order
    info["wall_middle"] = ram_state[52:60]  # represented row by row in ram as single cell by another in same order
    info["wall_right"] = ram_state[61:69]  # represented row by row in ram as single cell by another in same order

    info["objects_colours"] = ram_state[71]  # colours
    info["changing_symbols_enemies"] = ram_state[72]  # when destroyed

    info["lives"] = ram_state[73]  # you have 3 lives from beginning. they decrease and after 1 it gets set on 3

    info["temporal_reference"] = ram_state[74]  # works as temporal reference for the game

    # bullets
    info["bullet_1_enemy_y"] = ram_state[81]
    info["bullet_2_enemy_y"] = ram_state[82]
    info["bullet_1_enemy_x"] = ram_state[83]
    info["bullet_2_enemy_x"] = ram_state[84]
    info["bullet_player_green_y"] = ram_state[85]
    info["bullet_player_yellow_y"] = ram_state[86]
    info["bullet_player_green_x"] = ram_state[87]
    info["bullet_player_yellow_x"] = ram_state[88]
    # you get able to shoot the other bullet, once the flying one disappears,

    # for an array-value for score there is two digits and arithmetic transfer(like from ram_state[104]) gets added
    # to most significant digits (ram_state[102])
    info["score_player_green"] = {ram_state[102], ram_state[104]}  # score is saved in hexadecimal in this order
    info["score_player_yellow"] = {ram_state[103], ram_state[105]}  # score is saved in hexadecimal
    # 200 points for destroying satellite dish
    # x*5 points for destroying an alien from row_x

    print(ram_state)
