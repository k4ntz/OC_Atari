from termcolor import colored
from .pong import _detect_objects_pong
from .skiing import _detect_objects_skiing
from .tennis import _detect_objects_tennis


def detect_objects_vision(objects, obs, game_name, hud=False):
    # if game_name.lower() == "freeway":
    #     return _detect_objects_freeway(objects, obs, hud)
    if game_name.lower() == "pong":
        return _detect_objects_pong(objects, obs, hud)
    # elif game_name.lower() == "seaquest":
    #     return _detect_objects_seaquest(objects, obs, hud)
    elif game_name.lower() == "skiing":
        return _detect_objects_skiing(objects, obs, hud)
    elif game_name.lower() == "tennis":
        return _detect_objects_tennis(objects, obs, hud)
    else:
        print(colored("Uncovered game in vision mode", "red"))
        exit(1)
