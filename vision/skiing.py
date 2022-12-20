from .utils import bb_by_color, plot_bounding_boxes


objects_colors = {"player": [214, 92, 92], "gate_flag": [66, 72, 200], "background": [236, 236, 236],
                  "tree_1": [72, 160, 72], "tree_2": [158, 208, 101], "tree_3": [82, 126, 45], "tree_4": [110, 156, 66],
                  "mogul": [214, 214, 214], "player_score": [0, 0, 0]}


def _detect_objects_skiing(info, obs):
    detected = {}
    detected["bbs"] = []
    # detection and filtering
    bb_by_color(detected, obs, objects_colors['player'], "player")
    detected['bbs'] = [bb for bb in detected['bbs']]
    bb_by_color(detected, obs, objects_colors['tree_1'], "tree_1")
    detected['bbs'] = [bb for bb in detected['bbs']]
    bb_by_color(detected, obs, objects_colors['tree_2'], "tree_2")
    detected['bbs'] = [bb for bb in detected['bbs']]
    bb_by_color(detected, obs, objects_colors['tree_3'], "tree_3")
    detected['bbs'] = [bb for bb in detected['bbs']]
    bb_by_color(detected, obs, objects_colors['tree_4'], "tree_4")
    detected['bbs'] = [bb for bb in detected['bbs']]
    bb_by_color(detected, obs, objects_colors['mogul'], "mogul")
    detected['bbs'] = [bb for bb in detected['bbs']]
    bb_by_color(detected, obs, objects_colors['gate_flag'], "gate_flag")
    detected['bbs'] = [bb for bb in detected['bbs']]
    bb_by_color(detected, obs, objects_colors['player_score'], "player_score")
    detected['bbs'] = [bb for bb in detected['bbs']]
    if False:
        plot_bounding_boxes(obs, detected["bbs"], objects_colors)
    objects = {}
    for obj in detected["bbs"]:
        y, x, h, w, type, name = obj
        r, g, b = objects_colors[name]
        objects[name] = (x, y, w, h, r, g, b)
    info["objects"] = objects
