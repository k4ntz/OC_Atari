import sys
from termcolor import colored

def get_max_objects(game_name, hud):
    p_module = __name__.split('.')[:-1] + [game_name.lower()]
    game_module = '.'.join(p_module)
    try:
        mod = sys.modules[game_module]
        return mod._get_max_objects(hud)
    except KeyError as err:
        print(colored(f"Game module does not exist: {game_module}", "red"))
        raise err
    except AttributeError as err:
        print(colored(f"_get_max_objects not implemented for game: {game_name}", "red"))
        raise err


def init_objects(game_name, hud):
    p_module = __name__.split('.')[:-1] + [game_name.lower()]
    game_module = '.'.join(p_module)

    try:
        mod = sys.modules[game_module]
        return mod._init_objects_ram(hud)
    except KeyError as err:
        print(colored(f"Game module does not exist: {game_module}", "red"))
        raise err
    except AttributeError as err:
        print(colored(f"_init_objects_ram not implemented for game: {game_name}", "red"))
        raise err

def detect_objects_raw(info, ram_state, game_name):
    p_module = __name__.split('.')[:-1] + [game_name.lower()]
    game_module = '.'.join(p_module)

    try:
        mod = sys.modules[game_module]
        mod._detect_objects_raw(info, ram_state)
    except KeyError as err:
        print(colored(f"Game module does not exist: {game_module}", "red"))
        raise err
    except AttributeError as err:
        print(colored(f"_detect_objects_raw not implemented for game: {game_name}", "red"))
        raise err

def detect_objects_ram(objects, ram_state, game_name, hud):
    p_module = __name__.split('.')[:-1] + [game_name.lower()]
    game_module = '.'.join(p_module)

    try:
        mod = sys.modules[game_module]
        mod._detect_objects_ram(objects, ram_state, hud)
    except KeyError as err:
        print(colored(f"Game module does not exist: {game_module}", "red"))
        raise err
    except AttributeError as err:
        print(colored(f"_detect_objects_ram not implemented for game: {game_name}", "red"))
        raise err
