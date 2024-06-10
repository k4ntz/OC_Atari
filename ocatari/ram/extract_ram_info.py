import sys

from termcolor import colored

from . import choppercommand
from .adventure import _detect_objects_adventure_ram, _init_objects_adventure_ram
from .alien import _init_objects_alien_ram, _detect_objects_alien_ram
from .amidar import _init_objects_amidar_ram, _detect_objects_amidar_ram
from .assault import _detect_objects_assault_raw, _detect_objects_assault_ram, _init_objects_assault_ram
from .asterix import _detect_objects_asterix_ram, _detect_objects_asterix_raw, \
    _init_objects_asterix_ram
from .asteroids import _detect_objects_asteroids_raw, _detect_objects_asteroids_ram, _init_objects_asteroids_ram
from .atlantis import _detect_objects_atlantis_raw, \
    _detect_objects_atlantis_ram, \
    _init_objects_atlantis_ram
from .bankheist import _init_objects_bankheist_ram, _detect_objects_bankheist_ram
from .battlezone import _init_objects_battlezone_ram, _detect_objects_battlezone_ram
from .beamrider import _detect_objects_beamrider_raw, _detect_objects_beamrider_ram, _init_objects_beamrider_ram
from .berzerk import _detect_objects_berzerk_raw, _detect_objects_berzerk_ram, _init_objects_berzerk_ram
from .bowling import _detect_objects_bowling_raw, _detect_objects_bowling_ram, _init_objects_bowling_ram
from .boxing import _detect_objects_boxing_raw, _detect_objects_boxing_ram, _init_objects_boxing_ram
from .breakout import _detect_objects_breakout_raw, _detect_objects_breakout_ram, _init_objects_breakout_ram
from .carnival import _init_objects_carnival_ram, _detect_objects_carnival_raw, _detect_objects_carnival_ram
from .centipede import _detect_objects_centipede_raw, _detect_objects_centipede_ram, _init_objects_centipede_ram
from .choppercommand import _detect_objects_ram, _detect_objects_raw
from .crazyclimber import _init_objects_crazyclimber_ram, _detect_objects_crazyclimber_ram
from .demonattack import _detect_objects_demon_attack_raw, \
    _detect_objects_demon_attack_ram, \
    _init_objects_demon_attack_ram
from .donkeykong import _init_objects_donkeykong_ram, _detect_objects_donkeykong_ram
from .enduro import _init_objects_enduro_ram, _detect_objects_enduro_ram
from .fishingderby import _init_objects_fishingderby_ram, _detect_objects_fishingderby_ram
from .freeway import _detect_objects_freeway_raw, _detect_objects_freeway_ram, _init_objects_freeway_ram
from .frostbite import _init_objects_frostbite_ram, _detect_objects_frostbite_ram
from .galaxian import _init_objects_galaxian_ram, _detect_objects_galaxian_ram
from .gopher import _init_objects_gopher_ram, _detect_objects_gopher_ram
from .hero import _init_objects_hero_ram, _detect_objects_hero_ram
from .icehockey import _init_objects_icehockey_ram, _detect_objects_icehockey_ram
from .jamesbond import _init_objects_jamesbond_ram, _detect_objects_jamesbond_ram
from .kangaroo import _detect_objects_kangaroo_raw, \
    _detect_objects_kangaroo_ram, \
    _init_objects_kangaroo_ram
from .krull import _init_objects_krull_ram, _detect_objects_krull_ram
from .montezumarevenge import _init_objects_montezumarevenge_ram, _detect_objects_montezumarevenge_ram
from .mspacman import _detect_objects_mspacman_raw, \
    _detect_objects_mspacman_ram, \
    _init_objects_mspacman_ram
from .pitfall import _init_objects_pitfall_ram, _detect_objects_pitfall_ram
from .pong import _detect_objects_pong_raw, _detect_objects_pong_ram, _init_objects_pong_ram
from .privateeye import _init_objects_privateeye_ram, _detect_objects_privateeye_ram
from .qbert import _detect_objects_qbert_raw, \
    _detect_objects_qbert_ram, \
    _init_objects_qbert_ram
from .riverraid import _detect_objects_riverraid_raw, _detect_objects_riverraid_ram, _init_objects_riverraid_ram
from .roadrunner import _init_objects_roadrunner_ram, _detect_objects_roadrunner_ram
from .seaquest import _detect_objects_seaquest_raw, _detect_objects_seaquest_ram, _init_objects_seaquest_ram
from .skiing import _detect_objects_skiing_raw, _detect_objects_skiing_ram, _init_objects_skiing_ram
from .spaceinvaders import _detect_objects_spaceinvaders_raw, \
    _detect_objects_spaceinvaders_ram, \
    _init_objects_spaceinvaders_ram
from .tennis import _detect_objects_tennis_raw, _detect_objects_tennis_ram, _init_objects_tennis_ram
from .venture import _init_objects_venture_ram, _detect_objects_venture_ram
from .crazyclimber import _init_objects_crazyclimber_ram, _detect_objects_crazyclimber_ram
from .amidar import _init_objects_amidar_ram, _detect_objects_amidar_ram
from .battlezone import _init_objects_battlezone_ram, _detect_objects_battlezone_ram
from .pacman import _init_objects_pacman_ram, _detect_objects_pacman_ram
from .timepilot import _init_objects_timepilot_ram, _detect_objects_timepilot_ram
from .upndown import _init_objects_upndown_ram, _detect_objects_upndown_ram
from .videopinball import _init_objects_videopinball_ram, _detect_objects_videopinball_ram
from .yarsrevenge import _init_objects_yarsrevenge_ram, _detect_objects_yarsrevenge_ram

# calls the respective _get_max_objects from the game modules
def get_max_objects(game_name, hud):
    p_module = __name__.split('.')[:-1] + [game_name.lower()]
    game_module = '.'.join(p_module)
    try:
        mod = sys.modules[game_module]
        return mod._get_max_objects(hud)
    except KeyError as err:
        print(colored(f"Game module does not exist: {game_module}", "red"))
        print("->", str(err))
        exit(1)
    except AttributeError as err:
        print(colored(f"max_objects not implemented for game: {game_name}", "red"))
        print("->", str(err))
        exit(1)


def init_objects(game_name, hud):
    """
    Initialize the object list for the correct game
    """
    if game_name.lower() == "boxing":
        return _init_objects_boxing_ram(hud)
    elif game_name.lower() == "roadrunner":
        return _init_objects_roadrunner_ram(hud)
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
        return _init_objects_spaceinvaders_ram(hud)
    elif game_name.lower() == "tennis":
        return _init_objects_tennis_ram(hud)
    elif game_name.lower() == "bowling":
        return _init_objects_bowling_ram(hud)
    elif game_name.lower() == "donkeykong":
        return _init_objects_donkeykong_ram(hud)
    elif game_name.lower() == "demonattack":
        return _init_objects_demon_attack_ram(hud)
    elif game_name.lower() == "mspacman":
        return _init_objects_mspacman_ram(hud)
    elif game_name.lower() == "pacman":
        return _init_objects_pacman_ram(hud)
    elif game_name.lower() == "centipede":
        return _init_objects_centipede_ram(hud)
    elif game_name.lower() == "carnival":
        return _init_objects_carnival_ram(hud)
    elif game_name.lower() == "kangaroo":
        return _init_objects_kangaroo_ram(hud)
    elif game_name.lower() == "berzerk":
        return _init_objects_berzerk_ram(hud)
    elif game_name.lower() == "beamrider":
        return _init_objects_beamrider_ram(hud)
    elif game_name.lower() == "asterix":
        return _init_objects_asterix_ram(hud)
    elif game_name.lower() == "galaxian":
        return _init_objects_galaxian_ram(hud)
    elif game_name.lower() == "choppercommand":
        return choppercommand._init_objects_ram(hud)
    elif game_name.lower() == "qbert":
        return _init_objects_qbert_ram(hud)
    elif game_name.lower() == "montezumarevenge":
        return _init_objects_montezumarevenge_ram(hud)
    elif game_name.lower() == "atlantis":
        return _init_objects_atlantis_ram(hud)
    elif game_name.lower() == "asteroids":
        return _init_objects_asteroids_ram(hud)
    elif game_name.lower() == "riverraid":
        return _init_objects_riverraid_ram(hud)
    elif game_name.lower() == "assault":
        return _init_objects_assault_ram(hud)
    elif game_name.lower() == "alien":
        return _init_objects_alien_ram(hud)
    elif game_name.lower() == "frostbite":
        return _init_objects_frostbite_ram(hud)
    elif game_name.lower() == "fishingderby":
        return _init_objects_fishingderby_ram(hud)
    elif game_name.lower() == "hero":
        return _init_objects_hero_ram(hud)
    elif game_name.lower() == "pitfall":
        return _init_objects_pitfall_ram(hud)
    elif game_name.lower() == "yarsrevenge":
        return _init_objects_yarsrevenge_ram(hud)
    elif game_name.lower() == "icehockey":
        return _init_objects_icehockey_ram(hud)
    elif game_name.lower() == "privateeye":
        return _init_objects_privateeye_ram(hud)
    elif game_name.lower() == "gopher":
        return _init_objects_gopher_ram(hud)
    elif game_name.lower() == "enduro":
        return _init_objects_enduro_ram(hud)
    elif game_name.lower() == "videopinball":
        return _init_objects_videopinball_ram(hud)
    elif game_name.lower() == "venture":
        return _init_objects_venture_ram(hud)
    elif game_name.lower() == "crazyclimber":
        return _init_objects_crazyclimber_ram(hud)
    elif game_name.lower() == "amidar":
        return _init_objects_amidar_ram(hud)
    elif game_name.lower() == "battlezone":
        return _init_objects_battlezone_ram(hud)
    elif game_name.lower() == "bankheist":
        return _init_objects_bankheist_ram(hud)
    elif game_name.lower() == "adventure":
        return _init_objects_adventure_ram(hud)
    elif game_name.lower() == "jamesbond":
        return _init_objects_jamesbond_ram(hud)
    elif game_name.lower() == "krull":
        return _init_objects_krull_ram(hud)
    elif game_name.lower() == "timepilot":
        return _init_objects_timepilot_ram(hud)
    elif game_name.lower() == "upndown":
        return _init_objects_upndown_ram(hud)
    else:
        raise NotImplementedError(colored("Uncovered init objects", "red"))


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
        _detect_objects_spaceinvaders_ram(info, ram_state)
    elif game_name.lower() == "tennis":
        _detect_objects_tennis_raw(info, ram_state)
        _detect_objects_spaceinvaders_raw(info, ram_state)
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
    # elif game_name.lower() == "galaxian":
    #     _detect_objects_galaxian_raw(info, ram_state)
    elif game_name.lower() == "kangaroo":
        _detect_objects_kangaroo_raw(info, ram_state)
    elif game_name.lower() == "berzerk":
        _detect_objects_berzerk_raw(info, ram_state)
    elif game_name.lower() == "beamrider":
        _detect_objects_beamrider_raw(info, ram_state)
    elif game_name.lower() == "asterix":
        _detect_objects_asterix_raw(info, ram_state)
    elif game_name.lower() == "choppercommand":
        _detect_objects_raw(info, ram_state)
    elif game_name.lower() == "qbert":
        _detect_objects_qbert_raw(info, ram_state)
    elif game_name.lower() == "atlantis":
        _detect_objects_atlantis_raw(info, ram_state)
    elif game_name.lower() == "asteroids":
        _detect_objects_asteroids_raw(info, ram_state)
    elif game_name.lower() == "riverraid":
        _detect_objects_riverraid_raw(info, ram_state)
    elif game_name.lower() == "assault":
        _detect_objects_assault_raw(info, ram_state)
    else:
        print(colored("Uncovered game in raw mode", "red"))
        exit(1)


def detect_objects_ram(objects, ram_state, game_name, hud):
    """
    Augment the info dictionary with object centric information
    """
    for obj in objects:  # saving the previsous positions
        if obj is not None:
            obj._save_prev()
    if game_name.lower() == "boxing":
        _detect_objects_boxing_ram(objects, ram_state, hud)
    elif game_name.lower() == "breakout":
        _detect_objects_breakout_ram(objects, ram_state, hud)
    elif game_name.lower() == "freeway":
        _detect_objects_freeway_ram(objects, ram_state, hud)
    elif game_name.lower() == "pong":
        _detect_objects_pong_ram(objects, ram_state, hud)
    elif game_name.lower() == "skiing":
        _detect_objects_skiing_ram(objects, ram_state, hud)
    elif game_name.lower() == "donkeykong":
        _detect_objects_donkeykong_ram(objects, ram_state, hud)
    elif game_name.lower() == "seaquest":
        _detect_objects_seaquest_ram(objects, ram_state, hud)
    elif game_name.lower() == "spaceinvaders":
        _detect_objects_spaceinvaders_ram(objects, ram_state, hud)
    elif game_name.lower() == "tennis":
        _detect_objects_tennis_ram(objects, ram_state, hud)
    elif game_name.lower() == "bowling":
        _detect_objects_bowling_ram(objects, ram_state, hud)
    elif game_name.lower() == "demonattack":
        _detect_objects_demon_attack_ram(objects, ram_state, hud)
    elif game_name.lower() == "mspacman":
        _detect_objects_mspacman_ram(objects, ram_state, hud)
    elif game_name.lower() == "pacman":
        _detect_objects_pacman_ram(objects, ram_state, hud)
    elif game_name.lower() == "centipede":
        _detect_objects_centipede_ram(objects, ram_state, hud)
    elif game_name.lower() == "carnival":
        _detect_objects_carnival_ram(objects, ram_state, hud)
    elif game_name.lower() == "kangaroo":
        _detect_objects_kangaroo_ram(objects, ram_state, hud)
    elif game_name.lower() == "berzerk":
        _detect_objects_berzerk_ram(objects, ram_state, hud)
    elif game_name.lower() == "beamrider":
        _detect_objects_beamrider_ram(objects, ram_state, hud)
    elif game_name.lower() == "asterix":
        _detect_objects_asterix_ram(objects, ram_state, hud)
    elif game_name.lower() == "choppercommand":
        _detect_objects_ram(objects, ram_state, hud)
    elif game_name.lower() == "qbert":
        _detect_objects_qbert_ram(objects, ram_state, hud)
    elif game_name.lower() == "montezumarevenge":
        return _detect_objects_montezumarevenge_ram(objects, ram_state, hud)
    elif game_name.lower() == "atlantis":
        _detect_objects_atlantis_ram(objects, ram_state, hud)
    elif game_name.lower() == "asteroids":
        _detect_objects_asteroids_ram(objects, ram_state, hud)
    elif game_name.lower() == "riverraid":
        _detect_objects_riverraid_ram(objects, ram_state, hud)
    elif game_name.lower() == "assault":
        _detect_objects_assault_ram(objects, ram_state, hud)
    elif game_name.lower() == "roadrunner":
        _detect_objects_roadrunner_ram(objects, ram_state, hud)
    elif game_name.lower() == "frostbite":
        _detect_objects_frostbite_ram(objects, ram_state, hud)
    elif game_name.lower() == "fishingderby":
        _detect_objects_fishingderby_ram(objects, ram_state, hud)
    elif game_name.lower() == "hero":
        _detect_objects_hero_ram(objects, ram_state, hud)
    elif game_name.lower() == "pitfall":
        _detect_objects_pitfall_ram(objects, ram_state, hud)
    elif game_name.lower() == "yarsrevenge":
        _detect_objects_yarsrevenge_ram(objects, ram_state, hud)
    elif game_name.lower() == "icehockey":
        _detect_objects_icehockey_ram(objects, ram_state, hud)
    elif game_name.lower() == "privateeye":
        _detect_objects_privateeye_ram(objects, ram_state, hud)
    elif game_name.lower() == "galaxian":
        _detect_objects_galaxian_ram(objects, ram_state, hud)
    elif game_name.lower() == "gopher":
        _detect_objects_gopher_ram(objects, ram_state, hud)
    elif game_name.lower() == "enduro":
        _detect_objects_enduro_ram(objects, ram_state, hud)
    elif game_name.lower() == "videopinball":
        _detect_objects_videopinball_ram(objects, ram_state, hud)
    elif game_name.lower() == "venture":
        _detect_objects_venture_ram(objects, ram_state, hud)
    elif game_name.lower() == "alien":
        _detect_objects_alien_ram(objects, ram_state, hud)
    elif game_name.lower() == "crazyclimber":
        _detect_objects_crazyclimber_ram(objects, ram_state, hud)
    elif game_name.lower() == "amidar":
        _detect_objects_amidar_ram(objects, ram_state, hud)
    elif game_name.lower() == "battlezone":
        _detect_objects_battlezone_ram(objects, ram_state, hud)
    elif game_name.lower() == "bankheist":
        _detect_objects_bankheist_ram(objects, ram_state, hud)
    elif game_name.lower() == "adventure":
        _detect_objects_adventure_ram(objects, ram_state, hud)
    elif game_name.lower() == "jamesbond":
        _detect_objects_jamesbond_ram(objects, ram_state, hud)
    elif game_name.lower() == "krull":
        _detect_objects_krull_ram(objects, ram_state, hud)
    elif game_name.lower() == "timepilot":
        _detect_objects_timepilot_ram(objects, ram_state, hud)
    elif game_name.lower() == "upndown":
        _detect_objects_upndown_ram(objects, ram_state, hud)
    else:
        print(colored("Uncovered game in ram mode", "red"))
        exit(1)
