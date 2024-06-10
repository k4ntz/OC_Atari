from .game_objects import GameObject
from .utils import find_objects, find_mc_objects, most_common_color
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

class Flag(GameObject):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.rgb = [200, 72, 72]

class Collectable(GameObject):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.rgb = [200, 72, 72]



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
    objects.clear()

    player = find_mc_objects(obs, [objects_colors["player_white"], [0, 0, 0]], minx=8, miny=26, maxy=193)
    for bb in player:
        objects.append(Player(*bb))
    
    colors = list(objects_colors.values())
    for i in range(8):
        truck = find_mc_objects(obs, [colors[i+1], [0, 0, 0]], minx=8, miny=26, maxy=193)
        for bb in truck:
            t = Truck(*bb)
            t.rgb = colors[i+1]
            objects.append(t)
    
    hflag = []
    for i in range(8):
        h = find_objects(obs, colors[i+17], miny=14, maxy=26)
        if len(h):
            hflag.extend(h)
        else:
            hflag.append(None)
    
    for i in range(8):
        flag = find_mc_objects(obs, [colors[i+9], [0, 0, 0]], size=(7,16), tol_s=5, minx=8, miny=26, maxy=193)
        for bb in flag:
            if hflag[i] is None:
                f = Collectable(*bb)
                f.rgb = colors[i+9]
                objects.append(f)
            else:
                f = Flag(*bb)
                f.rgb = colors[i+9]
                objects.append(f)

    if hud:
        for i in range(8):
            if hflag[i] is not None:
                hf = HUD_Flag(*hflag[i])
                hf.rgb = colors[i+17]
                objects.append(hf)
        score = find_objects(obs, objects_colors["score"],maxx=85, maxy=25, closing_dist=8)
        for bb in score:
            objects.append(Score(*bb))
        
        life = find_objects(obs, objects_colors["life"],maxx= 46, miny=194)
        for bb in life:
            objects.append(Life(*bb))
