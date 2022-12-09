from termcolor.termcolor import colored
from vision.pong import _detect_objects_pong


def augment_info_vision(info, obs, game_name):
    if game_name.lower() == "pong":
        return _detect_objects_pong(info, obs)
    else:
        print(colored("Uncovered game", "red"))
