from .utils import bb_by_color, plot_bounding_boxes


objects_colors = {"player": [210, 164, 74], "ghost_orange": [180, 122, 48], "ghost_cyan": [84, 184, 153],
                  "ghost_pink": [198, 89, 179], "ghost_red": [200, 72, 72], "life_1": [187, 187, 53], "life_2": [187, 187, 53], "life_3": [187, 187, 53],
                  "cherry/strawberry/Apple": [184, 50, 50], "orange/banana": [198, 108, 58], "pretzel": [162, 162, 42],
                  "pear": [110, 156, 66], "cherry/strawberry/Applein_play": [184, 50, 50], "orange/bananain_play": [198, 108, 58], "pretzel_in_play": [162, 162, 42],
                  "pear_in_play": [110, 156, 66], "eatable_ghosts_1": [66,114,194], "eatable_ghosts_2": [66,114,194], "eatable_ghosts_3": [66,114,194], "eatable_ghosts_4": [66,114,194], "player_score": [195, 144, 61]}

#170
def _detect_objects_ms_pacman(info, obs):
    detected = {}
    detected["bbs"] = []
    # detection and filtering
    it = 0
    for k, v, in objects_colors.items():
        bb_by_color(detected, obs, v, k)
        if k == "life_1":
            detected['bbs'] = [bb for bb in detected['bbs'] if
                               bb[5] != "life_1" or bb[1] < 25]
        elif k == "life_2":
            detected['bbs'] = [bb for bb in detected['bbs'] if
                               bb[5] != "life_2" or 25 < bb[1] < 35]
        elif k == "life_3":
            detected['bbs'] = [bb for bb in detected['bbs'] if
                               bb[5] != "life_3" or 35 < bb[1]]                       
        elif 7 < it < 12:
            detected['bbs'] = [bb for bb in detected['bbs'] if
                               bb[5] != k or 170 < bb[0]]
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

        it+=1
    objects = {}
    for obj in detected["bbs"]:
        y, x, h, w, type, name = obj
        r, g, b = objects_colors[name]
        objects[name] = (x, y, w, h, r, g, b)
    info["objects"] = objects
