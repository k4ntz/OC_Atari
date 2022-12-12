from vision import *
from termcolor import colored


def augment_info_vision(info, obs, game_name):
    if game_name.lower() == "pong":
        return _detect_objects_pong(info, obs)
    elif game_name.lower() == "tennis":
        return _detect_objects_tennis(info, obs)
    else:
        print(colored("Uncovered game", "red"))
