from vision import *


def augment_info_vision(info, obs, game_name):
    if game_name.lower() == "pong":
        return _detect_objects_pong(info, obs)
    else:
        print(colored("Uncovered game", "red"))
