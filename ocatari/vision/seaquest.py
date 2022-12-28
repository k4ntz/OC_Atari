from .utils import find_objects

objects_colors = {"enemy": [92, 186, 92], "player": [187, 187, 53],
                  "diver": [66, 72, 200], "background": [0, 28, 136],
                  "player_score": [210, 210, 64], "oxygen_bar": [214, 214, 214], "lives": [210, 210, 64]}

fixed_objects_pos = {

}


# TODO: fix
def _detect_objects_seaquest(info, obs):
    objects = {}
    enemy = [bb for bb in find_objects(obs, objects_colors["enemy"], min_distance=None)
             if 5 < bb[1] < 189 and bb[2] > 10 and bb[3] < 28]
    if enemy:
        objects["enemy"] = enemy[0]
    player = [bb for bb in find_objects(obs, objects_colors["player"], min_distance=None)
              if 5 < bb[1] < 189 and bb[2] > 10 and bb[3] < 28]
    if player:
        objects["player"] = player[0]
    diver = find_objects(obs, objects_colors["diver"])
    if diver:
        objects["diver"] = diver[0]
    info["objects"] = objects
