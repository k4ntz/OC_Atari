from .utils import find_objects

objects_colors = {"player_head": [198, 89, 179], "player_shoes": [0, 0, 0], "ball": [45, 50, 184],
                  "background": [180, 122, 48], "player_score": [84, 92, 214], "round_player_1": [45, 50, 184],
                  "round_player_2": [45, 50, 184], "pins": [45, 50, 184]}

fixed_objects_pos = {

}


def _detect_objects_bowling(info, obs):
    objects = {}
    ball = [bb for bb in find_objects(obs, objects_colors["ball"], min_distance=None)
            if bb[2] < 160 and 100 < bb[1] < 175 and bb[3] < 20]
    if ball:
        objects["ball"] = ball

    pins = [bb for bb in find_objects(obs, objects_colors["pins"], min_distance=None)
            if bb[2] < 160 and 100 < bb[1] < 175 and bb[3] > 10]
    if pins:
        objects["pins"] = pins[0]

    round_player_1 = [bb for bb in find_objects(obs, objects_colors["round_player_1"], min_distance=None)
                      if bb[2] < 160 and bb[1] < 100 and bb[0] < 50]
    if round_player_1:
        objects["round_player_1"] = round_player_1[0]

    round_player_2 = [bb for bb in find_objects(obs, objects_colors["round_player_2"], min_distance=None)
                      if bb[2] < 160 and bb[1] < 100 and bb[0] > 110]
    if round_player_2:
        objects["round_player_2"] = round_player_2[0]

    player_score = [bb for bb in find_objects(obs, objects_colors["player_score"], min_distance=None)
                    if bb[1] < 20]
    if player_score:
        objects["player_score"] = player_score[0]
    player_head = [bb for bb in find_objects(obs, objects_colors["player_head"], min_distance=None)]
    if player_head:
        objects["player_head"] = player_head[0]
    player_shoes = [bb for bb in find_objects(obs, objects_colors["player_shoes"], min_distance=None)]
    if player_shoes:
        objects["player_shoes"] = player_shoes[0]
    info["objects"] = objects
