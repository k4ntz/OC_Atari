import sys
from termcolor import colored


def detect_objects_vision(objects, obs, game_name, hud):
    p_module = __name__.split('.')[:-1] + [game_name.lower()]
    game_module = '.'.join(p_module)
    try:
        mod = sys.modules[game_module]
        return mod._detect_objects(objects, obs, hud)
    except KeyError:
        raise NotImplementedError(colored(f"Game module does not exist: {game_module}", "red"))
    except AttributeError:
        raise NotImplementedError(colored(f"_detect_objects not implemented for game: {game_name}", "red"))
        
