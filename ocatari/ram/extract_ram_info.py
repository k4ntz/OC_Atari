import sys
from termcolor import colored
import numpy as np
from ocatari.vision.game_objects import NoObject


# parses MAX_NB* dicts, returns default init list of objects
def instantiate_max_objects(game_name, max_obj_dict):
    objects = []
    p_module = __name__.split('.')[:-1] + [game_name.lower()]
    game_module = '.'.join(p_module)
    try:
        mod = sys.modules[game_module]
    except KeyError as err:
        return []
    for k, v in max_obj_dict.items():
        for _ in range(0, v):
            objects.append(getattr(mod, k)())
    return objects


def get_class_dict(game_name):
    p_module = __name__.split('.')[:-1] + [game_name.lower()]
    game_module = '.'.join(p_module)
    try:
        mod = sys.modules[game_module]
        classes = {}
        for name, number in mod.MAX_NB_OBJECTS_HUD.items():
            classes[name] = getattr(mod, name)
        return classes
    except KeyError as err:
        raise KeyError(f"Game module does not exist: {game_module}")
    except AttributeError as err:
        raise AttributeError(
            f"MAX_NB_OBJECTS_HUD not implemented for game: {game_name}")


def get_max_objects(game_name, hud):
    p_module = __name__.split('.')[:-1] + [game_name.lower()]
    game_module = '.'.join(p_module)
    try:
        mod = sys.modules[game_module]
        if hud:
            return mod.MAX_NB_OBJECTS_HUD
        return mod.MAX_NB_OBJECTS
    except KeyError as err:
        raise KeyError(f"Game module does not exist: {game_module}")
    except AttributeError as err:
        raise AttributeError(
            f"MAX_NB_OBJECTS_HUD not implemented for game: {game_name}")


def use_vision_objects(objects, game_module):
    """
    replaces ram objects with their equivalent vision objects
    """
    game_module_vision = game_module.replace('ram', 'vision')
    mod = sys.modules[game_module_vision]
    for i, obj in enumerate(objects):
        if obj:  # skip None objects
            objects[i] = getattr(mod, objects[i].category)(*obj.xywh)
        else:
            objects[i] = NoObject()
    return objects


def init_objects(game_name, hud, vision=False):
    p_module = __name__.split('.')[:-1] + [game_name.lower()]
    game_module = '.'.join(p_module)
    try:
        mod = sys.modules[game_module]
        if vision:
            return use_vision_objects(mod._init_objects_ram(hud), game_module)
        return mod._init_objects_ram(hud)
    except KeyError as err:
        raise KeyError(f"Game module does not exist: {game_module}")
    except AttributeError as err:
        raise AttributeError(
            f"init_objects not implemented for game: {game_name}")


def detect_objects_raw(info, ram_state, game_name):
    p_module = __name__.split('.')[:-1] + [game_name.lower()]
    game_module = '.'.join(p_module)

    try:
        mod = sys.modules[game_module]
        mod._detect_objects_raw(info, ram_state)
    except KeyError as err:
        raise KeyError(f"Game module does not exist: {game_module}")
    # except AttributeError as err:
    #     raise AttributeError(
    #         f"detect_objects_raw not implemented for game: {game_name}")


def detect_objects_ram(objects, ram_state, game_name, hud):
    p_module = __name__.split('.')[:-1] + [game_name.lower()]
    game_module = '.'.join(p_module)
    for obj in objects:  # saving the previous positions
        if obj:
            obj._save_prev()
    try:
        mod = sys.modules[game_module]
        mod._detect_objects_ram(objects, ram_state, hud)
    except KeyError as err:
        raise KeyError(f"Game module does not exist: {game_module}")
    # except AttributeError as err:
    #     raise AttributeError(
    #         f"_detect_objects_ram not implemented for game: {game_name}")


def get_object_state_size(game_name, hud):
    max_obj = get_max_objects(game_name, hud)
    iobjects = instantiate_max_objects(game_name, max_obj)
    nsrepr_tot = [o._nsrepr for o in iobjects]
    return sum(map(len, nsrepr_tot))


def get_object_state(reference_list, objects, game_name):
    import warnings
    warnings.warn(
        "get_object_state is deprecated and will be removed in the next major release. Use the new obj_representation")
    p_module = __name__.split('.')[:-1] + [game_name.lower()]
    game_module = '.'.join(p_module)
    try:
        mod = sys.modules[game_module]
        state = mod._get_object_state(reference_list, objects)
        return state
    except KeyError as err:
        raise KeyError(f"Game module does not exist: {game_module}")
    except AttributeError as err:
        try:
            temp_ref_list = reference_list.copy()
            state = reference_list.copy()
            for o in objects:  # populate out_vector with object instance
                if not o:
                    continue
                # at position of first category occurance
                idx = temp_ref_list.index(o.category)
                state[idx] = o.xy  # write the slice
                temp_ref_list[idx] = ""  # remove reference from reference list
            for i, d in enumerate(temp_ref_list):
                if d != "":  # fill not populated category instances wiht 0.0's
                    state[i] = [0.0, 0.0]
            return state
        except AssertionError as err:
            raise err
