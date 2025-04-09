from .game_objects import GameObject, NoObject
from .utils import find_objects, find_mc_objects, most_common_color, match_objects, match_blinking_objects
import numpy as np

objects_colors = {"player_white": [192, 192, 192], "t_orange": [213, 130, 74], "t_red": [214, 92, 92], "t_green": [92, 186, 92], "t_blue1": [84, 160, 197],
                  "t_pink": [164, 89, 208], "t_purple1": [127, 92, 213], "t_purple2": [84, 92, 214], "t_blue2": [84, 138, 210],
                  "f_yellow": [162, 162, 42], "f_orange1": [180, 122, 48], "f_orange2": [139, 108, 58], "f_red": [200, 72, 72], "f_purple1": [104, 72, 198],
                  "f_purple2": [146, 70, 192], "f_pink": [184, 70, 162], "f_blue": [66, 72, 200],
                  "hf_yellow": [134, 134, 29], "hf_orange1": [162, 98, 33], "hf_orange2": [181, 83, 40], "hf_red": [184, 50, 50], "hf_purple1": [78, 50, 181],
                  "hf_purple2": [125, 48, 173], "hf_pink": [168, 48, 143], "hf_blue": [45, 50, 184], "score": [168, 48, 143], "life": [198, 108, 58]}


class Player(GameObject):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.rgb = [192, 192, 192]


class Truck(GameObject):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.rgb = [214, 92, 92]
        self.num_frames_invisible = -1
        self.max_frames_invisible = 3
        self.expected_dist = 2


class Flag(GameObject):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.rgb = [200, 72, 72]
        self.num_frames_invisible = -1
        self.max_frames_invisible = 3
        self.expected_dist = 2


class Collectable(GameObject):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.rgb = [200, 72, 72]
        self.num_frames_invisible = -1
        self.max_frames_invisible = 3
        self.expected_dist = 2


#  ---- HUD -----
class HUD_Flag(GameObject):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.rgb = [210, 164, 74]


class Score(GameObject):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.rgb = [168, 48, 143]


class Life(GameObject):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.rgb = [198, 108, 58]


def _detect_objects(objects, obs, hud=False):

    player = find_mc_objects(obs, [objects_colors["player_white"], [
                             0, 0, 0]], minx=8, miny=26, maxy=193)
    if player:
        if type(objects[0]) is NoObject:
            objects[0] = Player(*player[0])
        objects[0].xywh = player[0]
    else:
        objects[0] = NoObject()

    colors = list(objects_colors.values())
    truck = []
    for i in range(8):
        truck.extend(find_mc_objects(
            obs, [colors[i+1], [0, 0, 0]], minx=8, miny=26, maxy=193))
    
    match_blinking_objects(objects, truck[0:3], 1, 3, Truck)

    hflag = []
    for i in range(8):
        h = find_objects(obs, colors[i+17], miny=14, maxy=26)
        if len(h):
            hflag.extend(h)
        else:
            hflag.append(None)

    col = []
    fla = []

    for i in range(8):
        flag = find_mc_objects(
            obs, [colors[i+9], [0, 0, 0]], size=(7, 16), tol_s=5, minx=8, miny=26, maxy=193)
        if flag:
            if hflag[i] is None:
                col.append(flag[0])
            else:
                fla.append(flag[0])
    
    match_blinking_objects(objects, fla[0:3], 4, 3, Flag)
    match_blinking_objects(objects, col[0:3], 7, 3, Collectable)

    if hud:
        for i in range(8):
            if hflag[i] is not None:
                if type(objects[10+i]) is NoObject:
                    objects[10+i] = HUD_Flag(*hflag[i])
                objects[10+i].xywh = hflag[i]
                objects[10+i].rgb = colors[i+17]
                
        score = find_objects(
            obs, objects_colors["score"], maxx=85, maxy=25, closing_dist=8)
        if score:
            objects[18].xywh = score[0]

        life = find_objects(obs, objects_colors["life"], maxx=46, miny=194)
        if life:
            objects[19].xywh = life[0]
