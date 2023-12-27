import sys


def _get_max_objects(hud=False):
    def fromdict(max_obj_dict):
        objects = []
        mod = sys.modules[__name__]
        for k, v in max_obj_dict.items():
            for _ in range(0, v):
                objects.append(getattr(mod, k)())
        return objects

    if hud:
        return
    return


def _init_objects_adventure_ram(hud=False):
    """
    (Re)Initialize the objects
    """
    objects = []

    objects.extend([None] * 150)
    if hud:
        objects.extend([None] * 7)
    return []


def _detect_objects_adventure_revised(objects, ram_state, hud=False):


    if hud:
        return
    return objects
