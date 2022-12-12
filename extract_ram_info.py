from termcolor import colored
from ram.boxing import _augment_info_boxing_raw
from ram.boxing import _augment_info_boxing_revised
from ram.breakout import _augment_info_breakout_raw
from ram.breakout import _augment_info_breakout_revised
from ram.pong import _augment_info_pong_revised
from ram.pong import _augment_info_pong_raw
from ram.seaquest import _augment_info_seaquest_raw
from ram.seaquest import _augment_info_seaquest_revised
from ram.skiing import _augment_info_skiing_raw
from ram.skiing import _augment_info_skiing_revised
from ram.tennis import _augment_info_tennis_raw
from ram.tennis import _augment_info_tennis_revised


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
    else:
        print(colored("Uncovered game", "red"))
        exit(1)
