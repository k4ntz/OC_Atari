from .utils import find_objects, plot_bounding_boxes


objects_colors = {"enemy": [213, 130, 74], "player": [92, 186, 92],
                  "ball": [236, 236, 236], "background": [144, 72, 17],
                  "player_score": [92, 186, 92], "enemy_score": [213, 130, 74],
                  "player_score_2": [92, 186, 92], "enemy_score_2": [213, 130, 74],
                  }


def _detect_objects_pong(info, obs):
    objects = {}
    # detection and filtering
    enemy = find_objects(obs, objects_colors["enemy"], min_distance=1)
    for el in enemy:
        if el[1] > 30:
            objects["enemy"] = el
        else:
            if "enemy_score" in objects:
                objects["enemy_score_2"] = el
            else:
                objects["enemy_score"] = el
    player = find_objects(obs, objects_colors["player"], min_distance=1)
    for el in player:
        if el[1] > 30:
            objects["player"] = el
        else:
            if "player_score" in objects:
                objects["player_score_2"] = el
            else:
                objects["player_score"] = el
    ball = find_objects(obs, objects_colors["ball"], min_distance=None)
    for el in ball:
        if el[2] < 20:
            objects["ball"] = el
    # bb_by_color(detected, obs, objects_colors['player'], "player")
    # detected['bbs'] = [bb if bb[5] != "player" or bb[0] > 30 else (*bb[:4], "S", "player_score")
    #                    for bb in detected['bbs']]
    # bb_by_color(detected, obs, objects_colors['enemy'], "enemy")
    # detected['bbs'] = [bb if bb[5] != "enemy" or bb[0] > 30 else (*bb[:4], "S", "enemy_score")
    #                    for bb in detected['bbs']]
    # bb_by_color(detected, obs, objects_colors['ball'], "ball")
    # detected['bbs'] = [bb for bb in detected['bbs'] if bb[5] != "ball" or bb[3] < 20]
    if False:
        plot_bounding_boxes(obs, detected["bbs"], objects_colors)
    info["objects"] = objects
