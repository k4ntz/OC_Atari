'''
from .utils import bb_by_color

objects_colors = {"player_green": [50, 132, 50], "score_green": [50, 132, 50], "player_yellow": [162, 134, 56],
                  "score_yellow": [162, 134, 56], "alien": [134, 134, 29],
                  "wall_1": [181, 83, 40], "wall_2": [181, 83, 40], "wall_3": [181, 83, 40],
                  "satellite_dish": [151, 25, 122], "bullets": [142, 142, 142], "number_lives": [162, 134, 56],
                  "ground": [80, 89, 22], "background": [0, 0, 0]}

detected = {}
detected['bbs'] = []

# NOT FINISHED
def _detect_objects_space_invaders(info, obs):
    # detected = {"bbs": []}
    # detection and filtering
    for k, v in objects_colors.items():

        bb_by_color(detected, obs, v, k)

        if k == "player_green":
            detected['bbs'] = [bb for bb in detected['bbs'] if
                               bb[5] != "player_green" or bb[0] > 140]

        # dangerous. all digits get detected but its not expected because of separation. same for yellow
        elif k == "score_green":
            detected['bbs'] = [bb for bb in detected['bbs'] if
                               bb[5] != "score_green" or bb[0] < 140]

        elif k == "player_yellow":
            detected['bbs'] = [bb for bb in detected['bbs'] if
                               bb[5] != "player_yellow" or bb[0] > 140]

        elif k == "score_yellow":
            detected['bbs'] = [bb for bb in detected['bbs'] if
                               bb[5] != "score_yellow" or bb[0] < 140]

        # special case!
        elif k == "wall_1":
            detected['bbs'] = [bb for bb in detected['bbs'] if
                               bb[5] != "wall_1" or 0 < bb[1] < 60]
        elif k == "wall_2":
            detected['bbs'] = [bb for bb in detected['bbs'] if
                               bb[5] != "wall_2" or 60 < bb[1] < 95]
        elif k == "wall_3":
            detected['bbs'] = [bb for bb in detected['bbs'] if
                               bb[5] != "wall_3" or 95 < bb[1] < 150]
        # bullets
        # one of the problems for bullets is that they could be in same position

    objects = {}
    alien_x = 0
    for obj in detected["bbs"]:

        y, x, h, w, type, name = obj
        r, g, b = objects_colors[name]
        if name == "alien":
            alien_str = "alien_" + str(alien_x)
            objects[alien_str] = (x, y, w, h, r, g, b)
            alien_x += 1

        else:
            objects[name] = (x, y, w, h, r, g, b)
    info["objects"] = objects
    '''
