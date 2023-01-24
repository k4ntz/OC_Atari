from termcolor import colored
from .pong import _detect_objects_pong
from .skiing import _detect_objects_skiing
from .tennis import _detect_objects_tennis
# from .freeway import _detect_objects_freeway
from .seaquest import _detect_objects_seaquest
from .bowling import _detect_objects_bowling
from .demonAttack import _detect_objects_demon_attack
from .breakout import _detect_objects_breakout
from .space_invaders import _detect_objects_space_invaders


def detect_objects_vision(objects, obs, game_name, hud=False):
    # if game_name.lower() == "freeway":
    #     return _detect_objects_freeway(objects, obs, hud)
    if game_name.lower() == "bowling":
        return _detect_objects_bowling(objects, obs, hud)
    elif game_name.lower() == "pong":
        return _detect_objects_pong(objects, obs, hud)
    elif game_name.lower() == "seaquest":
        return _detect_objects_seaquest(objects, obs, hud)
    elif game_name.lower() == "skiing":
        return _detect_objects_skiing(objects, obs, hud)
    elif game_name.lower() == "tennis":
        return _detect_objects_tennis(objects, obs, hud)
    elif game_name.lower() == "spaceinvaders":
        return _detect_objects_space_invaders(objects, obs, hud)
    elif game_name.lower() == "demonattack":
        return _detect_objects_demon_attack(objects, obs, hud)
    elif game_name.lower() == "breakout":
        return _detect_objects_breakout(objects, obs, hud)
    else:
        print(colored("Uncovered game in vision mode", "red"))
        exit(1)
