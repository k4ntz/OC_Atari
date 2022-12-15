from .utils import bb_by_color

objects_colors = {
        "enemy": [117, 128, 240], "player": [240, 128, 128],
        "ball": [236, 236, 236], "ball_shadow": [74, 74, 74],
        "logo": [120, 120, 120], "enemy_score": [90, 100, 200],
        "player_score": [200, 100, 100]
    }


detected = {}
detected['bbs'] = [
    (4, 39, 8, 16, "S", "enemy_score"),
    (4, 104, 8, 16, "S", "player_score"),
    (193, 39, 7, 33, "S", "logo")
]


def _detect_objects_tennis(info, obs):
    bb_by_color(detected, obs, objects_colors['enemy'], "enemy", closing_active=False)
    detected['bbs'] = [bb for bb in detected['bbs'] if bb[5] != "enemy" or 5 < bb[0] < 189 and bb[3] > 10 and bb[2] < 28]
    bb_by_color(detected, obs, objects_colors['player'], "player", closing_active=False)
    detected['bbs'] = [bb for bb in detected['bbs'] if bb[5] != "player" or 5 < bb[0] < 189 and bb[3] > 10 and bb[2] < 28]
    bb_by_color(detected, obs, objects_colors['ball'], "ball")
    bb_by_color(detected, obs, objects_colors['ball_shadow'], "ball_shadow")
    # plot_bounding_boxes(obs, detected["bbs"], objects_colors)
    objects = {}
    for obj in detected["bbs"]:
        y, x, h, w, type, name = obj
        r,g,b = objects_colors[name]
        objects[name] = (x, y, w, h, r, g, b)
    info["objects"] = objects
