from termcolor import colored
from vision.pong import _detect_objects_pong
from vision.tennis import _detect_objects_tennis

def augment_info_vision(info, obs, game_name):
    if game_name.lower() == "pong":
        return _detect_objects_pong(info, obs)
    elif game_name.lower() == "tennis":
        return _detect_objects_tennis(info, obs)
    else:
        print(colored("Uncovered game", "red"))
