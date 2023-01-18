from .utils import find_objects # noqa

objects_colors = {"player_green": [50, 132, 50], "score_green": [50, 132, 50], "player_yellow": [162, 134, 56],
                  "score_yellow": [162, 134, 56], "alien": [134, 134, 29],
                  "wall_1": [181, 83, 40], "wall_2": [181, 83, 40], "wall_3": [181, 83, 40],
                  "satellite_dish": [151, 25, 122], "bullets": [142, 142, 142], "number_lives": [162, 134, 56],
                  "ground": [80, 89, 22], "background": [0, 0, 0]}


def _detect_objects_space_invaders(info, obs):
    objects = {}
    for object in objects_colors:
        found_objects = find_objects(obs, objects_colors[object])
        objects[object] = found_objects
    info["objects"] = objects
    info["objects_colors"] = objects_colors
