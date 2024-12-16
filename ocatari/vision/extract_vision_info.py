import sys
from termcolor import colored


def detect_objects_vision(objects, obs, game_name, hud):
    p_module = __name__.split('.')[:-1] + [game_name.lower()]
    game_module = '.'.join(p_module)
    for obj in objects:  # saving the previsous positions
        if obj:
            obj._save_prev()
    try:
        mod = sys.modules[game_module]
        mod._detect_objects
    except KeyError:
        raise NotImplementedError(
            colored(f"Game module does not exist: {game_module}", "red"))
    except AttributeError:
        raise NotImplementedError(
            colored(f"_detect_objects not implemented for game: {game_name}", "red"))
    return mod._detect_objects(objects, obs, hud)
