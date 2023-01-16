from .utils import find_objects


objects_colors = {"player": [210, 164, 74], "lives": [187, 187, 53], "player_score": [195, 144, 61],
                  "ghost_orange": [180, 122, 48], "ghost_cyan": [84, 184, 153],
                  "ghost_pink": [198, 89, 179], "ghost_red": [200, 72, 72], 
                  "cherry/strawberry/Apple": [184, 50, 50], "pretzel": [162, 162, 42],
                  "orange/banana": [198, 108, 58], "pear": [110, 156, 66],
                  "eatable_ghosts": [66, 114, 194], "player_score": [195, 144, 61]}

# fixed_objects_pos = { }

def _detect_objects_mspacman(info, obs):
    objects = {}

    for object in objects_colors:
        found_objects = find_objects(obs, objects_colors[object])
        objects[object] = found_objects

    # fixed_objects_complete = {}
    # for objn in fixed_objects_pos.keys():
    #     fixed_objects_complete[objn] = [fixed_objects_pos[objn]]
    # objects.update(fixed_objects_complete)

    info["objects"] = objects
    info["objects_colors"] = objects_colors