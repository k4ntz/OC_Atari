from termcolor import colored
from .asterix import _detect_objects_asterix_revised, _detect_objects_asterix_raw,\
    _init_objects_asterix_ram
from .berzerk import _detect_objects_berzerk_raw, _detect_objects_berzerk_revised, _init_objects_berzerk_ram
from .boxing import _detect_objects_boxing_raw, _detect_objects_boxing_revised, _init_objects_boxing_ram
from .freeway import _detect_objects_freeway_raw, _detect_objects_freeway_revised, _init_objects_freeway_ram
from .bowling import _detect_objects_bowling_raw, _detect_objects_bowling_revised, _init_objects_bowling_ram
from .breakout import _detect_objects_breakout_raw, _detect_objects_breakout_revised, _init_objects_breakout_ram
from .pong import _detect_objects_pong_raw, _detect_objects_pong_revised, _init_objects_pong_ram
from .seaquest import _detect_objects_seaquest_raw, _detect_objects_seaquest_revised, _init_objects_seaquest_ram
from .skiing import _detect_objects_skiing_raw, _detect_objects_skiing_revised, _init_objects_skiing_ram
from .space_invaders import _detect_objects_space_invaders_raw, \
                            _detect_objects_space_invaders_revised, \
                            _init_objects_space_invaders_ram
from .tennis import _detect_objects_tennis_raw, _detect_objects_tennis_revised, _init_objects_tennis_ram
from .demonAttack import _detect_objects_demon_attack_raw, \
                         _detect_objects_demon_attack_revised, \
                         _init_objects_demon_attack_ram
from .mspacman import _detect_objects_mspacman_raw, \
                      _detect_objects_mspacman_revised, \
                      _init_objects_mspacman_ram
from .centipede import _detect_objects_centipede_raw, _detect_objects_centipede_revised, _init_objects_centipede_ram
from .carnival import _init_objects_carnival_ram, _detect_objects_carnival_raw, _detect_objects_carnival_revised
from .kangaroo import _detect_objects_kangaroo_raw, \
                      _detect_objects_kangaroo_revised, \
                      _init_objects_kangaroo_ram


def init_objects(game_name, hud):
    """
    Initialize the object list for the correct game
    """
    if game_name.lower() == "boxing":
        return _init_objects_boxing_ram(hud)
    elif game_name.lower() == "freeway":
        return _init_objects_freeway_ram(hud)
    elif game_name.lower() == "breakout":
        return _init_objects_breakout_ram(hud)
    elif game_name.lower() == "pong":
        return _init_objects_pong_ram(hud)
    elif game_name.lower() == "skiing":
        return _init_objects_skiing_ram(hud)
    elif game_name.lower() == "seaquest":
        return _init_objects_seaquest_ram(hud)
    elif game_name.lower() == "spaceinvaders":
        return _init_objects_space_invaders_ram(hud)
    elif game_name.lower() == "tennis":
        return _init_objects_tennis_ram(hud)
    elif game_name.lower() == "bowling":
        return _init_objects_bowling_ram(hud)
    elif game_name.lower() == "demonattack":
        return _init_objects_demon_attack_ram(hud)
    elif game_name.lower() == "mspacman":
        return _init_objects_mspacman_ram(hud)
    elif game_name.lower() == "centipede":
        return _init_objects_centipede_ram(hud)
    elif game_name.lower() == "carnival":
        return _init_objects_carnival_ram(hud)
    elif game_name.lower() == "kangaroo":
        return _init_objects_kangaroo_ram(hud)
    elif game_name.lower() == "berzerk":
        return _init_objects_berzerk_ram(hud)
    elif game_name.lower() == "asterix":
        return _init_objects_asterix_ram(hud)
    else:
        print(colored("Uncovered init objects", "red"))
        exit(1)


def detect_objects_raw(info, ram_state, game_name):
    """
    Augment the info dictionary with object centric information
    """
    if game_name.lower() == "boxing":
        _detect_objects_boxing_raw(info, ram_state)
    elif game_name.lower() == "breakout":
        _detect_objects_breakout_raw(info, ram_state)
    elif game_name.lower() == "freeway":
        _detect_objects_freeway_raw(info, ram_state)
    elif game_name.lower() == "pong":
        _detect_objects_pong_raw(info, ram_state)
    elif game_name.lower() == "skiing":
        _detect_objects_skiing_raw(info, ram_state)
    elif game_name.lower() == "seaquest":
        _detect_objects_seaquest_raw(info, ram_state)
    elif game_name.lower() == "spaceinvaders":
        _detect_objects_space_invaders_revised(info, ram_state)
    elif game_name.lower() == "tennis":
        _detect_objects_tennis_raw(info, ram_state)
        _detect_objects_space_invaders_raw(info, ram_state)
    elif game_name.lower() == "tennis":
        _detect_objects_tennis_raw(info, ram_state)
    elif game_name.lower() == "bowling":
        _detect_objects_bowling_raw(info, ram_state)
    elif game_name.lower() == "demonattack":
        _detect_objects_demon_attack_raw(info, ram_state)
    elif game_name.lower() == "mspacman":
        _detect_objects_mspacman_raw(info, ram_state)
    elif game_name.lower() == "centipede":
        _detect_objects_centipede_raw(info, ram_state)
    elif game_name.lower() == "carnival":
        _detect_objects_carnival_raw(info, ram_state)
    elif game_name.lower() == "kangaroo":
        _detect_objects_kangaroo_raw(info, ram_state)
    elif game_name.lower() == "kangaroo":
        _detect_objects_berzerk_raw(info, ram_state)
    elif game_name.lower() == "asterix":
        _detect_objects_asterix_raw(info, ram_state)
    else:
        print(colored("Uncovered game in raw mode", "red"))
        exit(1)


def detect_objects_revised(objects, ram_state, game_name, hud):
    """
    Augment the info dictionary with object centric information
    """
    if game_name.lower() == "boxing":
        _detect_objects_boxing_revised(objects, ram_state, hud)
    elif game_name.lower() == "breakout":
        _detect_objects_breakout_revised(objects, ram_state, hud)
    elif game_name.lower() == "freeway":
        _detect_objects_freeway_revised(objects, ram_state, hud)
    elif game_name.lower() == "pong":
        _detect_objects_pong_revised(objects, ram_state, hud)
    elif game_name.lower() == "skiing":
        _detect_objects_skiing_revised(objects, ram_state, hud)
    elif game_name.lower() == "seaquest":
        _detect_objects_seaquest_revised(objects, ram_state, hud)
    elif game_name.lower() == "spaceinvaders":
        _detect_objects_space_invaders_revised(objects, ram_state, hud)
    elif game_name.lower() == "tennis":
        _detect_objects_tennis_revised(objects, ram_state, hud)
    elif game_name.lower() == "bowling":
        _detect_objects_bowling_revised(objects, ram_state, hud)
    elif game_name.lower() == "demonattack":
        _detect_objects_demon_attack_revised(objects, ram_state, hud)
    elif game_name.lower() == "mspacman":
        _detect_objects_mspacman_revised(objects, ram_state, hud)
    elif game_name.lower() == "centipede":
        _detect_objects_centipede_revised(objects, ram_state, hud)
    elif game_name.lower() == "carnival":
        _detect_objects_carnival_revised(objects, ram_state, hud)
    elif game_name.lower() == "kangaroo":
        _detect_objects_kangaroo_revised(objects, ram_state, hud)
    elif game_name.lower() == "berzerk":
        _detect_objects_berzerk_revised(objects, ram_state, hud)
    elif game_name.lower() == "asterix":
        _detect_objects_asterix_revised(objects, ram_state, hud)
    else:
        print(colored("Uncovered game in revised mode", "red"))
        exit(1)
