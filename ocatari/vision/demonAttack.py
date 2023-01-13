from .utils import find_objects


objects_colors = {'player': [184, 70, 162], 'enemy': [213, 130, 74], 'projectile_friendly': [212, 140, 252],
                  'projectile_hostile': [252, 144, 144], 'live': [101, 111, 228], 'score': [223, 183, 85]}

def _detect_objects_demonAttack(info, obs):
    objects = {}

    player = find_objects(obs, objects_colors["player"], min_distance=1)
    if len(player) >= 1:
        objects["player"] = player[0]

    enemy = find_objects(obs, objects_colors["enemy"], min_distance=1)
    index = 0
    for bb in enemy:
        name = "enemy"+str(index)
        index += 1
        objects[name] = bb

    score = find_objects(obs, objects_colors["score"], min_distance=1)
    if len(score) >= 1:
        objects["score"] = score[0]

    for name in ['projectile_friendly', 'projectile_hostile', 'live']:
        obj = find_objects(obs, objects_colors[name], min_distance=1)
        objects[name] = obj


    info['objects_colors'] = objects_colors
    info['objects'] = objects



