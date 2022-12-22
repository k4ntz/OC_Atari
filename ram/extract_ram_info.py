from termcolor import colored
from .boxing import _augment_info_boxing_raw
from .boxing import _augment_info_boxing_revised
from .breakout import _augment_info_breakout_raw
from .breakout import _augment_info_breakout_revised
from .pong import _augment_info_pong_revised
from .pong import _augment_info_pong_raw
from .seaquest import _augment_info_seaquest_raw
from .seaquest import _augment_info_seaquest_revised
from .skiing import _augment_info_skiing_raw
from .skiing import _augment_info_skiing_revised
from .tennis import _augment_info_tennis_raw
from .tennis import _augment_info_tennis_revised
from .freeway import _augment_info_freeway_raw, _augment_info_freeway_revised
from .space_invaders import _augment_info_space_invaders_raw
from .space_invaders import _augment_info_space_invaders_revised


def augment_info_raw(info, ram_state, game_name):
    """
    Augment the info dictionary with object centric information
    """
    if game_name.lower() == "boxing":
        _augment_info_boxing_raw(info, ram_state)
    elif game_name.lower() == "breakout":
        _augment_info_breakout_raw(info, ram_state)
    elif game_name.lower() == "skiing":
        _augment_info_skiing_raw(info, ram_state)
    elif game_name.lower() == "seaquest":
        _augment_info_seaquest_raw(info, ram_state)
    elif game_name.lower() == "pong":
        _augment_info_pong_raw(info, ram_state)
    elif game_name.lower() == "tennis":
        _augment_info_tennis_raw(info, ram_state)
    elif game_name.lower() == "freeway":
        _augment_info_freeway_raw(info, ram_state)
    elif game_name.lower() == "spaceInvaders-v4":
        _augment_info_space_invaders_raw(info, ram_state)
    else:
        print(colored("Uncovered game", "red"))
        exit(1)


def augment_info_revised(info, ram_state, game_name):
    """
    Augment the info dictionary with object centric information
    """
    if game_name.lower() == "boxing":
        _augment_info_boxing_revised(info, ram_state)
    elif game_name.lower() == "breakout":
        _augment_info_breakout_revised(info, ram_state)
    elif game_name.lower() == "skiing":
        _augment_info_skiing_revised(info, ram_state)
    elif game_name.lower() == "seaquest":
        _augment_info_seaquest_revised(info, ram_state)
    elif game_name.lower() == "pong":
        _augment_info_pong_revised(info, ram_state)
    elif game_name.lower() == "tennis":
        _augment_info_tennis_revised(info, ram_state)
    elif game_name.lower() == "freeway":
        _augment_info_freeway_revised(info, ram_state)
    elif game_name.lower() == "spaceInvaders-v4":
        _augment_info_space_invaders_revised(info, ram_state)
    else:
        print(colored("Uncovered game", "red"))
        exit(1)
