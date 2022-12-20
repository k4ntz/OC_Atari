from .utils import find_objects

objects_colors = {
        "enemy": [117, 128, 240], "player": [240, 128, 128],
        "ball": [236, 236, 236], "ball_shadow": [74, 74, 74],
        "logo": [120, 120, 120], "enemy_score": [90, 100, 200],
        "player_score": [200, 100, 100]
    }

fixed_objects_pos = {
    "player_score" : [39, 4, 16, 8],
    "enemy_score": [104, 4, 16, 8],
    "logo": [39, 193, 33, 7]
}

def _detect_objects_tennis(info, obs, fixed_objects=True):
    objects = {}
    enemy = [bb for bb in find_objects(obs, objects_colors["enemy"], min_distance=None)
                        if 5 < bb[1] < 189 and bb[2] > 10 and bb[3] < 28]
    if enemy:
        objects["enemy"] = enemy[0]
    player = [bb for bb in find_objects(obs, objects_colors["player"], min_distance=None)
                        if 5 < bb[1] < 189 and bb[2] > 10 and bb[3] < 28]
    if player:
        objects["player"] = player[0]
    ball = find_objects(obs, objects_colors["ball"])
    if ball:
        objects["ball"] = ball[0]
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
