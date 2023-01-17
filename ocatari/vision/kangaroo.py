from .utils import find_objects

objects_colors = {"kangaroo": [223, 183, 85], "bell": [210, 164, 74],
                  "fruit": [214, 92, 92], "hud": [160, 171, 79]
                  }


def _detect_objects_kangaroo(info, obs):
    objects = {}
    for object in objects_colors:
        found_objects = find_objects(obs, objects_colors[object])
        objects[object] = found_objects
    """if fixed_objects:
        fixed_objects_complete = {}
        for objn in fixed_objects_pos.keys():
            fixed_objects_complete[objn] = [fixed_objects_pos[objn]]
        objects.update(fixed_objects_complete)"""
    info["objects"] = objects
    info["objects_colors"] = objects_colors
