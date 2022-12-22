from .utils import bb_by_color, plot_bounding_boxes


objects_colors = {"player": [50, 132, 50], "aliens": [134, 134, 29], "walls": [181, 83, 40]}


def _detect_objects_skiing(info, obs):
    detected = {}
    detected["bbs"] = []
    # detection and filtering
    bb_by_color(detected, obs, objects_colors['player'], "player")
    detected['bbs'] = [bb for bb in detected['bbs']]
    bb_by_color(detected, obs, objects_colors['score'], "score")
    detected['bbs'] = [bb for bb in detected['bbs']]
    if False:
        plot_bounding_boxes(obs, detected["bbs"], objects_colors)
    objects = {}
    for obj in detected["bbs"]:
        y, x, h, w, type, name = obj
        r, g, b = objects_colors[name]
        objects[name] = (x, y, w, h, r, g, b)
    info["objects"] = objects
