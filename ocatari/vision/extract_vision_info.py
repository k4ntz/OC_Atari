from termcolor import colored
from .pong import _detect_objects_pong
from .skiing import _detect_objects_skiing
from .tennis import _detect_objects_tennis


def augment_info_vision(info, obs, game_name):
    if game_name.lower() == "freeway":
        return _detect_objects_freeway(info, obs)
    elif game_name.lower() == "pong":
        return _detect_objects_pong(info, obs)
    elif game_name.lower() == "seaquest":
        return _detect_objects_seaquest(info, obs)
    elif game_name.lower() == "skiing":
        return _detect_objects_skiing(info, obs)
    elif game_name.lower() == "tennis":
        return _detect_objects_tennis(info, obs)
    else:
        print(colored("Uncovered game in vision mode", "red"))
        exit(1)
