from .utils import find_objects

objects_colors = {
    "tree1": [158, 208, 101], "tree2": [82, 126, 45],
    "tree3": [110, 156, 66], "rock": [192, 192, 192],
    "tree4": [72, 160, 72],
    "rock2": [214, 214, 214], "flag": [66, 72, 200],
    "player": [214, 92, 92], "logo": [0, 0, 0]
}

fixed_objects_pos = {
    "logo": [65, 187, 32, 7]
}


def _detect_objects_skiing(info, obs, fixed_objects=True):
    objects = {}
    for object in objects_colors:
        found_objects = find_objects(obs, objects_colors[object])
        objects[object] = found_objects
    # if fixed_objects:
    #     fixed_objects_complete = {}
    #     for objn in fixed_objects_pos.keys():
    #         fixed_objects_complete[objn] = [fixed_objects_pos[objn]]
    #     objects.update(fixed_objects_complete)
    info["objects"] = objects
    info["objects_colors"] = objects_colors
