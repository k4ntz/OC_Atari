from termcolor import colored
from .pong import _detect_objects_pong
from .skiing import _detect_objects_skiing
from .tennis import _detect_objects_tennis
<<<<<<< HEAD
from .freeway import _detect_objects_freeway
from .seaquest import _detect_objects_seaquest
from .demonAttack import _detect_objects_demonAttack
=======
# from .freeway import _detect_objects_freeway
# from .seaquest import _detect_objects_seaquest
# from .bowling import _detect_objects_bowling
from .space_invaders import _detect_objects_space_invaders
>>>>>>> c7179c0c2c47df090660e30191119a0fd87bb220


def detect_objects_vision(objects, obs, game_name, hud=False):
    # if game_name.lower() == "freeway":
    #     return _detect_objects_freeway(objects, obs, hud)
    # elif game_name.lower() == "bowling":
    #     return _detect_objects_bowling(info, obs)
    if game_name.lower() == "pong":
        return _detect_objects_pong(objects, obs, hud)
    # elif game_name.lower() == "seaquest":
    #     return _detect_objects_seaquest(objects, obs, hud)
    elif game_name.lower() == "skiing":
        return _detect_objects_skiing(objects, obs, hud)
    elif game_name.lower() == "tennis":
<<<<<<< HEAD
        return _detect_objects_tennis(info, obs)
    elif game_name.lower() == "demonattack":
        return _detect_objects_demonAttack(info, obs)
=======
        return _detect_objects_tennis(objects, obs, hud)
    elif game_name.lower() == "spaceinvaders":
        return _detect_objects_space_invaders(objects, obs, hud)
>>>>>>> c7179c0c2c47df090660e30191119a0fd87bb220
    else:
        print(colored("Uncovered game in vision mode", "red"))
        exit(1)
