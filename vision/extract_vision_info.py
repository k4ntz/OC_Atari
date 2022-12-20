from termcolor import colored
from .pong import _detect_objects_pong
from .tennis import _detect_objects_tennis
from .seaquest import _detect_objects_seaquest
from .skiing import _detect_objects_skiing


def augment_info_vision(info, obs, game_name):
    if game_name.lower() == "pong":
        return _detect_objects_pong(info, obs)
    elif game_name.lower() == "tennis":
        return _detect_objects_tennis(info, obs)
    elif game_name.lower() == "seaquest":
        return _detect_objects_seaquest(info, obs)
    elif game_name.lower() == "skiing":
        return _detect_objects_skiing(info, obs)
    else:
        print(colored("Uncovered game", "red"))
