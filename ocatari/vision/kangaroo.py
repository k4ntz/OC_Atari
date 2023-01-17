from .utils import find_objects

objects_colors = {"Kangaroo": [223, 183, 85], "Bell": [210, 164, 74], "Fruit": [214, 92, 92], "HUD": [160, 171, 79] }


def _detect_objects_kangaroo(info, obs):
    objects = {}
    
    info["objects"] = objects
