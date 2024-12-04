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
        print(colored(f"Game module does not exist: {game_module}", "red"))
        # raise err
        return {}
    except AttributeError as err:
        print(colored(f"MAX_NB_OBJECTS_HUD not implemented for game: {game_name}", "red"))
        raise err


def get_max_objects(game_name, hud):
    p_module = __name__.split('.')[:-1] + [game_name.lower()]
    game_module = '.'.join(p_module)
    try:
        mod = sys.modules[game_module]
        if hud:
            return mod.MAX_NB_OBJECTS_HUD
        return mod.MAX_NB_OBJECTS
    except KeyError as err:
        print(colored(f"Game module does not exist: {game_module}", "red"))
        # raise err
        return {}
    except AttributeError as err:
        print(colored(f"MAX_NB_OBJECTS(_HUD) not implemented for game: {game_name}", "red"))
        raise err

def use_vision_objects(objects, game_module):
    """
    replaces ram objects with their equivalent vision objects
    """
    game_module_vision = game_module.replace('ram', 'vision')
    mod = sys.modules[game_module_vision]
    for i, obj in enumerate(objects):
        if obj: # skip None objects
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
    for obj in objects:  # saving the previous positions
        if obj:
            obj._save_prev()
    try:
        mod = sys.modules[game_module]
        mod._detect_objects_ram(objects, ram_state, hud)
    except KeyError as err:
        print(colored(f"Game module does not exist: {game_module}", "red"))
        raise err
    except AttributeError as err:
        print(colored(f"_detect_objects_ram not implemented for game: {game_name}", "red"))
        raise err


def get_object_state_size(game_name, hud):
    max_obj = get_max_objects(game_name, hud)
    iobjects = instantiate_max_objects(game_name, max_obj)
    nsrepr_tot = [o._nsrepr for o in iobjects]
    return sum(map(len, nsrepr_tot))
    

def get_object_state(reference_list, objects, game_name):
       
    p_module = __name__.split('.')[:-1] + [game_name.lower()]
    game_module = '.'.join(p_module)
    try:
        mod = sys.modules[game_module]
        state = mod._get_object_state(reference_list, objects)
        return state
    except KeyError as err:
        print(colored(f"Game module does not exist: {game_module}", "red"))
        raise err
    except AttributeError as err:
        #print(colored(f"_get_object_state not implemented for game: {game_name}", "red"))
        #print(colored(f"Try Default get_object_state", "red"))
        try:
            temp_ref_list = reference_list.copy()
            state = reference_list.copy()
            for o in objects: # populate out_vector with object instance
                if not o:
                    continue
                idx = temp_ref_list.index(o.category) # at position of first category occurance
                state[idx] = o.xy # write the slice
                temp_ref_list[idx] = "" # remove reference from reference list
            for i, d in enumerate(temp_ref_list):
                if d != "": #fill not populated category instances wiht 0.0's
                    state[i] = [0.0, 0.0]
            return state
        except AssertionError as err:
            raise err
        
def get_masked_dqn_state(objects):
    try:
        import cv2
    except ModuleNotFoundError:
        print(
            "\nOpenCV is required when using the ALE env wrapper. ",
            "Try `pip install opencv-python`.\n",
        )
    
    state = np.zeros((210,160))
    for o in objects:
        if o is None:
            continue
        x,y,w,h = o.xywh

        if x+w < 0 or y+h < 0 or w < 0 or h < 0:
            continue
            

        for i in range(y, y+h if y+h < 210 else 209):
            for j in range(x, x+w if x+w < 160 else 159):
                state[i][j] = 255
    
    state = cv2.resize(state, (84, 84), interpolation=cv2.INTER_AREA)
    return state

