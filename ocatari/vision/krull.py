from .game_objects import GameObject, NoObject
from .utils import find_objects, find_mc_objects, most_common_color, match_objects
import numpy as np

objects_colors = {"orange1": [213, 130, 74], "orange2": [198, 108, 58], "orange3": [181, 83, 40], "orange4": [227, 151, 89],
                  "red1": [214, 92, 92], "pink1": [198, 89, 179], "purple1": [164, 89, 208], "purple2": [127, 92, 213],
                  "blue1": [84, 92, 214], "blue2": [84, 138, 210], "blue3": [84, 160, 197], "green1": [84, 184, 153],
                  "green2": [45, 129, 105], "blue4": [45, 109, 152], "blue5": [45, 87, 176], "blue6": [45, 50, 184],
                  "purple3": [78, 50, 181], "purple4": [125, 48, 173], "pink2": [168, 48, 143], "red2": [184, 50, 50],
                  "white": [236, 236, 236], "green3": [92, 186, 92], "yellow1": [224, 236, 124], "orange5": [162, 98, 33],
                  "orange6": [144, 72, 17], "red3": [167, 26, 26], "pink3": [236, 140, 224], "pink4": [184, 70, 162],
                  "pink5": [151, 25, 122], "pink6": [224, 124, 210], "pink7": [132, 0, 100], "pink8": [212, 108, 195],
                  "yellow2": [0, 48, 100], "yellow3": [210, 182, 86], "yellow4": [134, 134, 29], "yellow5": [210, 210, 64],
                  "grey1": [74, 74, 74], "grey2": [170, 170, 170], "brown1": [105, 77, 20]}


class Player(GameObject):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.rgb = [198, 108, 58]


class Lyssa(GameObject):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.rgb = [198, 89, 179]


class Slayers(GameObject):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.rgb = [45, 109, 152]


class Slayer_Shot(GameObject):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.rgb = [0, 48, 100]


class Fire_Mare(GameObject):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.rgb = [213, 130, 74]


class Spider(GameObject):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.rgb = [236, 236, 236]


class Weapon(GameObject):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.rgb = [92, 186, 92]


class Enemy_Weapon(GameObject):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.rgb = [184, 70, 162]


class Beast(GameObject):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.rgb = [144, 72, 17]


class Wall(GameObject):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.rgb = [162, 98, 33]


class Window(GameObject):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.rgb = [142, 142, 142]


class Star(GameObject):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.rgb = [236, 236, 236]


class Castle(GameObject):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.rgb = [162, 98, 33]


class Life(GameObject):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.rgb = [92, 186, 92]


#  ---- HUD -----
class Sun(GameObject):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.rgb = [236, 236, 236]


class Hour_Glass(GameObject):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.rgb = [214, 92, 92]


class Score(GameObject):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.rgb = [224, 236, 124]


class Life_HUD(GameObject):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.rgb = [92, 186, 92]


class Weapon_HUD(GameObject):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.rgb = [92, 186, 92]


def _detect_objects(objects, obs, hud=False):

    player = find_mc_objects(obs, [objects_colors["orange1"], objects_colors["orange2"],
                             objects_colors["orange3"], objects_colors["orange4"]], miny=12, maxy=174)
    for bb in player:
        if bb[3] > 5 and bb[3] > 12 and bb[3] < 17:
            objects[0].xywh = bb
            break
    else:
        mare = find_objects(obs, objects_colors["orange1"])
        for bb in mare:
            if bb[3] > 7:
                objects[0].xywh = bb

    lyssa = find_mc_objects(obs, [objects_colors["red1"], objects_colors["pink1"], objects_colors["purple1"], objects_colors["purple2"],
                            objects_colors["blue1"], objects_colors["blue2"], objects_colors["blue3"], objects_colors["green1"]], miny=12, maxy=175, size=(7, 16), tol_s=3)
    if lyssa:
        if type(objects[1]) is NoObject:
            objects[1] = Lyssa(*lyssa[0])
        objects[1].xywh = lyssa[0]
    else:
        objects[1] = NoObject()

    slayers = find_mc_objects(obs, [objects_colors["green2"], objects_colors["blue4"], objects_colors["blue5"], objects_colors["blue6"],
                              objects_colors["purple3"], objects_colors["purple4"], objects_colors["pink2"], objects_colors["red2"]], miny=12, maxy=173)
    match_objects(objects, slayers, 2, 15, Slayers)

    star = find_objects(obs, objects_colors["white"], size=(
        3, 4), tol_s=2, miny=12, maxy=174)
    if star:
        if type(objects[89]) is NoObject:
            objects[89] = Star(*star[0])
        objects[89].xywh = star[0]
    else:
        objects[89] = NoObject()

    spider = find_objects(obs, objects_colors["white"], size=(
        8, 9), tol_s=2, miny=12, maxy=174)
    if spider:
        if type(objects[90]) is NoObject:
            objects[90] = Spider(*spider[0])
        objects[90].xywh = spider[0]
    else:
        objects[90] = NoObject()

    pick_up = find_objects(obs, objects_colors["green3"], size=(
        8, 9), tol_s=2, miny=12, maxy=174)

    if pick_up:
        if pick_up[0][2] < 7:
            objects[86] = NoObject()
            if type(objects[87]) is NoObject:
                objects[87] = Life(*pick_up[0])
            objects[87].xywh = pick_up[0]
        else:
            if type(objects[86]) is NoObject:
                objects[86] = Weapon(*pick_up[0])
            objects[86].xywh = pick_up[0]
            objects[87] = NoObject()
    else:
        objects[86] = NoObject()
        objects[87] = NoObject()

    beast = find_mc_objects(
        obs, [objects_colors["orange6"], objects_colors["red3"]], miny=12, maxy=173)
    
    if beast:
        if type(objects[19]) is NoObject:
            objects[19] = Beast(*beast[0])
        objects[19].xywh = beast[0]
    else:
        objects[19] = NoObject()

    wall = find_objects(obs, objects_colors["orange5"], miny=12, maxy=75)
    match_objects(objects, wall, 21, 64, Wall)

    weapon = find_objects(obs, objects_colors["yellow1"], miny=12, maxy=173)
    for bb in weapon:
        if bb[3] > 1:
            if type(objects[18]) is NoObject:
                objects[18] = Weapon(*bb)
            objects[18].xywh = bb
            break
    else:
        objects[18] = NoObject()

    if len(beast) != 0:
        e_weapon = find_objects(
            obs, objects_colors["pink1"], miny=60, maxy=173)
        e_weapon.extend(find_objects(
            obs, objects_colors["pink2"], miny=60, maxy=173))
        e_weapon.extend(find_objects(
            obs, objects_colors["pink3"], miny=60, maxy=173))
        e_weapon.extend(find_objects(
            obs, objects_colors["pink4"], miny=60, maxy=173))
        e_weapon.extend(find_objects(
            obs, objects_colors["pink5"], miny=60, maxy=173))
        e_weapon.extend(find_objects(
            obs, objects_colors["pink6"], miny=60, maxy=173))
        e_weapon.extend(find_objects(
            obs, objects_colors["pink7"], miny=60, maxy=173))
        e_weapon.extend(find_objects(
            obs, objects_colors["pink8"], miny=60, maxy=173))
        if e_weapon:
            if type(objects[20]) is NoObject:
                objects[20] = Enemy_Weapon(*e_weapon[0])
            objects[20].xywh = e_weapon[0]
        else:
            objects[20] = NoObject()
        
    window = False
    if obs[23, 76, 0] == 142 and obs[23, 76, 0] == 142 and obs[23, 76, 0] == 142:
        window = True
        bb = (76, 23, 8, 26)
        if type(objects[91]) is NoObject:
            objects[91] = Window(*bb)
    else:
        objects[91] = NoObject()

    if (obs[147, 47, 0] == 0 and obs[147, 47, 1] == 0 and obs[147, 47, 2] == 0) and (obs[147, 48, 0] != 0 or obs[147, 48, 1] != 0 or obs[147, 48, 2] != 0) and not window:
        # minx = 48, maxx = 111, miny = 97, maxy = 147
        upper_border = 147
        for i in range(50):
            if obs[147-i, 48, 0] != 0 or obs[147-i, 48, 1] != 0 or obs[147-i, 48, 2] != 0:
                upper_border = 147-i
        bb = (48, upper_border, 64, 148 - upper_border)
        if type(objects[88]) is NoObject:
            objects[88] = Castle(*bb)
        objects[88].xywh = bb
    else:
        objects[88] = NoObject()

    if hud:
        sun = find_objects(obs, objects_colors["white"], maxy=11)
        if sun:
            if type(objects[-5]) is NoObject:
                objects[-5] = Sun(*sun[0])
            objects[-5].xywh = sun[0]
        else:
            objects[-5] = NoObject()

        time = find_objects(obs, objects_colors["red1"], maxy=11)
        if time:
            if type(objects[-4]) is NoObject:
                objects[-4] = Hour_Glass(*time[0])
            objects[-4].xywh = time[0]
        else:
            objects[-4] = NoObject()

        score = find_objects(
            obs, objects_colors["yellow1"], miny=174, closing_dist=8)
        if score:
            if type(objects[-3]) is NoObject:
                objects[-3] = Score(*score[0])
            objects[-3].xywh = score[0]
        else:
            objects[-3] = NoObject()

        life = find_objects(
            obs, objects_colors["green3"], miny=186, maxx=78, closing_dist=8)
        if life:
            if type(objects[-2]) is NoObject:
                objects[-2] = Life_HUD(*life[0])
            objects[-2].xywh = life[0]
        else:
            objects[-2] = NoObject()

        w_hub = find_objects(
            obs, objects_colors["green3"], miny=186, minx=78, closing_dist=8)
        if w_hub:
            if type(objects[-1]) is NoObject:
                objects[-1] = Weapon_HUD(*w_hub[0])
            objects[-1].xywh = w_hub[0]
        else:
            objects[-1] = NoObject()
