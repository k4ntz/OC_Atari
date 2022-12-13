from .utils import bb_by_color, plot_bounding_boxes


objects_colors = {"enemy": [213, 130, 74], "player": [92, 186, 92],
                  "ball": [236, 236, 236], "background": [144, 72, 17],
                  "player_score": [92, 186, 92], "enemy_score": [213, 130, 74]}


def _detect_objects_pong(info, obs):
    detected = {}
    detected["bbs"] = []
    # detection and filtering
    bb_by_color(detected, obs, objects_colors['player'], "player")
    detected['bbs'] = [bb if bb[5] != "player" or bb[0] > 30 else (*bb[:4], "S", "player_score")
                       for bb in detected['bbs']]
    bb_by_color(detected, obs, objects_colors['enemy'], "enemy")
    detected['bbs'] = [bb if bb[5] != "enemy" or bb[0] > 30 else (*bb[:4], "S", "enemy_score")
                       for bb in detected['bbs']]
    bb_by_color(detected, obs, objects_colors['ball'], "ball")
    detected['bbs'] = [bb for bb in detected['bbs'] if bb[5] != "ball" or bb[3] < 20]
    if False:
        plot_bounding_boxes(obs, detected["bbs"], objects_colors)
    objects = {}
    for obj in detected["bbs"]:
        y, x, h, w, type, name = obj
        objects[name] = (x, y, w, h)
    # if "ball" not in objects:
    #     objects["ball"] = (0, 0, 2, 2)
    # if "enemy" not in objects:
    #     objects["enemy"] = (0, 0, 2, 2)
    info["objects"] = objects
