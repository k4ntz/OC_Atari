from .utils import find_objects


objects_colors = {"player": [210, 164, 74], "ghost_orange": [180, 122, 48], "ghost_cyan": [84, 184, 153],
                  "ghost_pink": [198, 89, 179], "ghost_red": [200, 72, 72], "life_1": [187, 187, 53],
                  "life_2": [187, 187, 53], "life_3": [187, 187, 53],
                  "cherry/strawberry/Apple": [184, 50, 50], "orange/banana": [198, 108, 58],
                  "pretzel": [162, 162, 42], "pear": [110, 156, 66], "cherry/strawberry/Applein_in_play": [184, 50, 50],
                  "orange/bananain_in_play": [198, 108, 58], "pretzel_in_play": [162, 162, 42],
                  "pear_in_play": [110, 156, 66], "eatable_ghosts_1": [66, 114,194], "eatable_ghosts_2": [66, 114, 194],
                   "eatable_ghosts_3": [66, 114, 194], "eatable_ghosts_4": [66, 114, 194], "player_score": [195, 144, 61]}


def _detect_objects_mspacman(info, obs):
    """
        elif k == "eatable_ghosts_1":
            detected['bbs'] = [bb for bb in detected['bbs'] if
                               bb[5] != k]
        elif k == "eatable_ghosts_2":
            detected['bbs'] = [bb for bb in detected['bbs'] if
                               bb[5] != k]
        elif k == "eatable_ghosts_3":
            detected['bbs'] = [bb for bb in detected['bbs'] if
                               bb[5] != k]
        elif k == "eatable_ghosts_4":
            detected['bbs'] = [bb for bb in detected['bbs'] if
                               bb[5] != k]
    """
    objects = {}

    player = [bb for bb in find_objects(obs, objects_colors["player"], min_distance=None)]

    if player:
        objects["player"] = player[0]

    ghost_orange = [bb for bb in find_objects(obs, objects_colors["ghost_orange"], min_distance=None)]

    if ghost_orange:
        objects["ghost_orange"] = ghost_orange[0]

    ghost_cyan = [bb for bb in find_objects(obs, objects_colors["ghost_cyan"], min_distance=None)]

    if ghost_cyan:
        objects["ghost_cyan"] = ghost_cyan[0]

    ghost_pink = [bb for bb in find_objects(obs, objects_colors["ghost_pink"], min_distance=None)]

    if ghost_pink:
        objects["ghost_pink"] = ghost_pink[0]

    ghost_red = [bb for bb in find_objects(obs, objects_colors["ghost_red"], min_distance=None)]

    if ghost_red:
        objects["ghost_red"] = ghost_red[0]

    life_1 = [bb for bb in find_objects['bbs']
              if bb[5] != "life_1" or bb[1] < 25]
    if life_1:
        objects["life_1"] = life_1[0]

    life_2 = [bb for bb in find_objects['bbs']
              if bb[5] != "life_2" or 25 < bb[1] < 35]
    if life_2:
        objects["life_2"] = life_2[0]

    life_3 = [bb for bb in find_objects['bbs']
              if bb[5] != "life_3" or 35 < bb[1]]
    if life_3:
        objects["life_3"] = life_3[0]

    red_fruit = [bb for bb in find_objects['bbs']
                 if bb[5] != "cherry/strawberry/Apple" or 170 < bb[0]]
    if red_fruit:
        objects["cherry/strawberry/Apple"] = red_fruit[0]

    orange_fruit = [bb for bb in find_objects['bbs']
                    if bb[5] != "orange/banana" or 170 < bb[0]]
    if orange_fruit:
        objects["orange/banana"] = orange_fruit[0]

    pretzel = [bb for bb in find_objects['bbs']
               if bb[5] != "pretzel" or 170 < bb[0]]
    if pretzel:
        objects["pretzel"] = pretzel[0]

    pear = [bb for bb in find_objects['bbs']
            if bb[5] != "pear" or 170 < bb[0]]
    if pear:
        objects["pear"] = pear[0]

    red_fruit_in_play = [bb for bb in find_objects['bbs']
                         if bb[5] != "cherry/strawberry/Applein_in_play" or 170 > bb[0]]
    if red_fruit_in_play:
        objects["cherry/strawberry/Applein_in_play"] = red_fruit_in_play[0]

    orange_fruit_in_play = [bb for bb in find_objects['bbs']
                            if bb[5] != "orange/bananain_in_play" or 170 > bb[0]]
    if orange_fruit_in_play:
        objects["orange/bananain_in_play"] = orange_fruit_in_play[0]

    pretzel_in_play = [bb for bb in find_objects['bbs']
                       if bb[5] != "pretzel_in_play" or 170 > bb[0]]
    if pretzel_in_play:
        objects["pretzel_in_play"] = pretzel_in_play[0]

    pear_in_play = [bb for bb in find_objects['bbs']
                    if bb[5] != "pear_in_play" or 170 > bb[0]]
    if pear_in_play:
        objects["pear_in_play"] = pear_in_play[0]

    info["objects"] = objects
