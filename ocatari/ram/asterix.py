from .game_objects import GameObject


class Player(GameObject):
    pass


def _init_objects_asterix_ram(hud=False):
    """
    (Re)Initialize the objects
    """
    objects = [Player()]
    if hud:
        pass

    return objects


def _detect_objects_asterix_revised(objects, ram_state, hud=False):
    pass


def _detect_objects_asterix_raw(info, ram_state):
    pass
