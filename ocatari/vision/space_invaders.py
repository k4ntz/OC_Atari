from .utils import bb_by_color, plot_bounding_boxes

objects_colors = {"player_green": [50, 132, 50], "score_green": [50, 132, 50], "player_yellow": [162, 134, 56],
                  "score_yellow": [162, 134, 56], "aliens": [134, 134, 29], "walls": [181, 83, 40],
                  "satellite_dish": [151, 25, 122], "bullets": [142, 142, 142], "number_lives": [162, 134, 56],
                  "ground": [80, 89, 22], "background": [0, 0, 0]}


# NOT FINISHED
def _detect_objects_skiing(info, obs):
    detected = {}
    detected["bbs"] = []
    # detection and filtering
    for k, v in objects_colors.items():
        bb_by_color(detected, obs, v, k)

        if k == "player_green":
            detected['bbs'] = [bb for bb in detected['bbs'] if
                               bb[0] > 140]

        elif k == "score_green":
            detected['bbs'] = [bb for bb in detected['bbs'] if
                               bb[0] < 140]

        elif k == "player_yellow":
            detected['bbs'] = [bb for bb in detected['bbs'] if
                               bb[0] > 140]

        elif k == "player_yellow":
            detected['bbs'] = [bb for bb in detected['bbs'] if
                               bb[0] < 140]

        # aliens -_-

        # special case! not finished or correct
        elif k == "walls":
            detected['bbs'] = [bb for bb in detected['bbs'] if
                               bb[5] == "wall_1" and 0 < bb[1] < 60]
            detected['bbs'] = [bb for bb in detected['bbs'] if
                               bb[5] == "wall_2" and 60 < bb[1] < 95]
            detected['bbs'] = [bb for bb in detected['bbs'] if
                               bb[5] == "wall_3" and 95 < bb[1] < 150]

    # detection and filtering
    # if y < 70 then yellow is score
    # lives could have the very similar x and y at same time

    '''bb_by_color(detected, obs, objects_colors['player_green'], "player_green")
    detected['bbs'] = [bb for bb in detected['bbs']]
    bb_by_color(detected, obs, objects_colors['score_green'], "score_green")
    detected['bbs'] = [bb for bb in detected['bbs']]
    bb_by_color(detected, obs, objects_colors['player_yellow'], "player_yellow")
    detected['bbs'] = [bb for bb in detected['bbs']]
    bb_by_color(detected, obs, objects_colors['score_yellow'], "score_yellow")
    detected['bbs'] = [bb for bb in detected['bbs']]
    bb_by_color(detected, obs, objects_colors['aliens'], "aliens")
    detected['bbs'] = [bb for bb in detected['bbs']]
    bb_by_color(detected, obs, objects_colors['walls'], "wall_1")
    detected['bbs'] = [bb for bb in detected['bbs']]
    bb_by_color(detected, obs, objects_colors['walls'], "wall_2")
    detected['bbs'] = [bb for bb in detected['bbs']]
    bb_by_color(detected, obs, objects_colors['walls'], "wall_3")
    detected['bbs'] = [bb for bb in detected['bbs']]

    # bb_by_color(detected, obs, objects_colors['bullets'], "bullets")
    # detected['bbs'] = [bb for bb in detected['bbs']] # bullets have same color!
    bb_by_color(detected, obs, objects_colors['number_lives'], "number_lives")
    detected['bbs'] = [bb for bb in detected['bbs']]'''

    if False:
        plot_bounding_boxes(obs, detected["bbs"], objects_colors)
    objects = {}
    for obj in detected["bbs"]:
        y, x, h, w, type, name = obj
        r, g, b = objects_colors[name]
        objects[name] = (x, y, w, h, r, g, b)
    info["objects"] = objects
