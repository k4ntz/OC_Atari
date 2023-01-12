from .utils import find_objects


objects_colors = {'player': [184, 70, 162], 'enemy': [213, 130, 74], 'projectile_friendly': [212, 140, 252],
                  'projectile_hostile': [252, 144, 144], 'live': [101, 111, 228], 'score': [223, 183, 85]}

def _detect_objects_demonAttack(info, obs):
    objects = {}

    for key, value in objects_colors.items():
        obj = find_objects(obs, value, min_distance=1)
        objects[key] = obj


    info['objects_colors'] = objects_colors
    info['objects'] = objects



