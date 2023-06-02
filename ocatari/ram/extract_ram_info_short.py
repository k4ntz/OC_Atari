import sys
from termcolor import colored


def get_max_objects(game_name, hud):
    p_module = __name__.split('.')[:-1] + [game_name.lower()]
    game_module = '.'.join(p_module)
    try:
        mod = sys.modules[game_module]
        return mod._get_max_objects(hud)
    except KeyError:
        print(colored(f"Game module does not exist: {game_module}", "red"))
        exit(1)
    except AttributeError:
        print(colored(f"_get_max_objects not implemented for game: {game_name}", "red"))
        exit(1)


def init_objects(game_name, hud):
    p_module = __name__.split('.')[:-1] + [game_name.lower()]
    game_module = '.'.join(p_module)
    print(game_module)

    try:
        mod = sys.modules[game_module]
        return mod._init_objects_ram(hud)
    except KeyError:
        print(colored(f"Game module does not exist: {game_module}", "red"))
        exit(1)
    except AttributeError:
        print(colored(f"_init_objects_ram not implemented for game: {game_name}", "red"))
        exit(1)

def detect_objects_raw(info, ram_state, game_name):
    p_module = __name__.split('.')[:-1] + [game_name.lower()]
    game_module = '.'.join(p_module)

    try:
        mod = sys.modules[game_module]
        mod._detect_objects_raw(info, ram_state)
    except KeyError:
        print(colored(f"Game module does not exist: {game_module}", "red"))
        exit(1)
    except AttributeError:
        print(colored(f"_detect_objects_raw not implemented for game: {game_name}", "red"))
        exit(1)

def detect_objects_revised(objects, ram_state, game_name, hud):
    p_module = __name__.split('.')[:-1] + [game_name.lower()]
    game_module = '.'.join(p_module)

    try:
        mod = sys.modules[game_module]
        mod._detect_objects_revised(objects, ram_state, hud)
    except KeyError:
        print(colored(f"Game module does not exist: {game_module}", "red"))
        exit(1)
    except AttributeError:
        print(colored(f"_detect_objects_revised not implemented for game: {game_name}", "red"))
        exit(1)
