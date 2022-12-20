from .utils import bb_by_color, find_objects

objects_colors = {
        "enemy": [117, 128, 240], "player": [240, 128, 128],
        "ball": [236, 236, 236], "ball_shadow": [74, 74, 74],
        "logo": [120, 120, 120], "enemy_score": [90, 100, 200],
        "player_score": [200, 100, 100]
    }


detected = {}
detected['bbs'] = []
# detected['bbs'] = [
#     (4, 39, 8, 16, "S", "enemy_score"),
#     (4, 104, 8, 16, "S", "player_score"),
#     (193, 39, 7, 33, "S", "logo")
# ]


fixed_objects_pos = {
    "player_score" : [39, 4, 16, 8],
    "enemy_score": [104, 4, 16, 8],
    "logo": [39, 193, 33, 7]
}

def _detect_objects_tennis(info, obs, fixed_objects=True):
    bb_by_color(detected, obs, objects_colors['enemy'], "enemy", closing_active=False)
    detected['bbs'] = [bb for bb in detected['bbs'] if bb[5] != "enemy" or 5 < bb[0] < 189 and bb[3] > 10 and bb[2] < 28]
    bb_by_color(detected, obs, objects_colors['player'], "player", closing_active=False)
    detected['bbs'] = [bb for bb in detected['bbs'] if bb[5] != "player" or 5 < bb[0] < 189 and bb[3] > 10 and bb[2] < 28]
    bb_by_color(detected, obs, objects_colors['ball'], "ball")
    objects = {}
    for obj in detected["bbs"]:
        y, x, h, w, type, name = obj
        objects[name] = (x, y, w, h)
    bshadow = find_objects(obs, objects_colors["ball_shadow"])
    if bshadow:
        assert len(bshadow) == 1
        objects['ball_shadow'] = bshadow[0]
    if fixed_objects:
        fixed_objects_complete = {}
        for objn in fixed_objects_pos.keys():
            fixed_objects_complete[objn] = fixed_objects_pos[objn] + objects_colors[objn]
        objects.update(fixed_objects_complete)
    info["objects"] = objects
