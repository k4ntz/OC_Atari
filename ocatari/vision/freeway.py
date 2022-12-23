from .utils import bb_by_color, plot_bounding_boxes


objects_colors = {"car1": [167, 26, 26], "car2": [180, 231, 117], "car3": [105, 105, 15],
                  "car4": [228, 111, 111], "car5": [24, 26, 167], "car6": [162, 98, 33],
                  "car7": [84, 92, 214], "car8": [184, 50, 50], "car9": [135, 183, 84],
                  "car10": [210, 210, 64], "score1": [228, 111, 111], "score2": [228, 111, 111],
                  "logo": [228, 111, 111], "chicken1": [252, 252, 84], "chicken2": [252, 252, 84]
                  }


def _detect_objects_freeway(info, obs):
    detected = {}
    detected["bbs"] = []
    # detection and filtering
    for k, v in objects_colors.items():
        bb_by_color(detected, obs, v, k)
        if k == "car4":
            detected['bbs'] = [bb for bb in detected['bbs'] if
                               bb[5] != "car4" or 60 < bb[0] < 90]
        elif k == "score1":
            detected['bbs'] = [bb for bb in detected['bbs'] if
                               bb[5] != "score1" or (bb[0] < 25 and bb[1] < 80)]
        elif k == "score2":
            detected['bbs'] = [bb for bb in detected['bbs'] if
                               bb[5] != "score2" or (bb[0] < 25 and bb[1] > 80)]
        elif k == "logo":
            detected['bbs'] = [bb for bb in detected['bbs'] if
                               bb[5] != "logo" or (bb[0] > 90)]
        elif k == "chicken1":
            detected['bbs'] = [bb for bb in detected['bbs'] if
                               bb[5] != "chicken1" or (bb[1] < 80 and bb[3] < 10)]
        elif k == "chicken2":
            detected['bbs'] = [bb for bb in detected['bbs'] if
                               bb[5] != "chicken2" or (bb[1] > 80 and bb[3] < 10)]

    objects = {}
    for obj in detected["bbs"]:
        y, x, h, w, type, name = obj
        r, g, b = objects_colors[name]
        objects[name] = (x, y, w, h, r, g, b)
    info["objects"] = objects