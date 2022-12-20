from .utils import bb_by_color, plot_bounding_boxes


objects_colors = {"enemy": [92, 186, 92], "player": [187, 187, 53],
                  "diver": [66, 72, 200], "background": [0, 28, 136],
                  "player_score": [210, 210, 64], "oxygen_bar": [214, 214, 214], "lives": [210, 210, 64]}


def _detect_objects_seaquest(info, obs):
    detected = {}
    detected["bbs"] = []
    # detection and filtering
    bb_by_color(detected, obs, objects_colors['player'], "player")
    detected['bbs'] = [bb for bb in detected['bbs']]
    bb_by_color(detected, obs, objects_colors['enemy'], "enemy")
    detected['bbs'] = [bb for bb in detected['bbs']]
    bb_by_color(detected, obs, objects_colors['diver'], "diver")
    detected['bbs'] = [bb for bb in detected['bbs']]
    bb_by_color(detected, obs, objects_colors['oxygen_bar'], "oxygen_bar")
    detected['bbs'] = [bb for bb in detected['bbs']]
    bb_by_color(detected, obs, objects_colors['player_score'], "player_score")
    detected['bbs'] = [bb for bb in detected['bbs']]
    bb_by_color(detected, obs, objects_colors['lives'], "lives")
    detected['bbs'] = [bb for bb in detected['bbs'] if bb[0] != 99]
    if False:
        plot_bounding_boxes(obs, detected["bbs"], objects_colors)
    objects = {}
    for obj in detected["bbs"]:
        y, x, h, w, type, name = obj
        r, g, b = objects_colors[name]
        objects[name] = (x, y, w, h, r, g, b)
    info["objects"] = objects
