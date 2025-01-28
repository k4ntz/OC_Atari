from .utils import find_objects, find_mc_objects, find_rope_segments, match_objects
from .game_objects import GameObject, NoObject
import numpy as np
import matplotlib as plt


objects_colors = {
    "logs": [105, 105, 15], "smallpit": [0, 0, 0], "scorpion": [236, 236, 236], "rope": [72, 72, 0], "waterhole": [45, 109, 152],
    "crocodile": [20, 60, 0], "hud_objs": [214, 214, 214]
}

playercolors = [[105, 105, 15], [228, 111, 111], [92, 186, 92], [53, 95, 24]]
wallcolors = [[167, 26, 26], [142, 142, 142]]
snakecolors = [[167, 26, 26], [0, 0, 0], [111, 111, 111]]
goldenbarcolors = [[252, 252, 84], [236, 236, 236]]
firecolors = [[236, 200, 96], [252, 188, 116], [72, 72, 0]]
moneybagcolors = [[111, 111, 111], [105, 105, 15]]
silverbarcolors = [[142, 142, 142], [236, 236, 236]]
diamondringcolors = [[236, 236, 236], [252, 252, 84]]


class Player(GameObject):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.rgb = 53, 95, 24
        self.hud = False


class Wall(GameObject):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.rgb = 167, 26, 26
        self.hud = False


class Logs(GameObject):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.rgb = 105, 105, 15
        self.hud = False


class StairPit(GameObject):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.rgb = 0, 0, 0
        self.hud = False


class Stair(GameObject):
    """
    The escape shafts from the underground.
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.rgb = 134, 134, 29
        self.hud = False



class Pit(GameObject):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.rgb = 252, 188, 116
        self.hud = False


class Scorpion(GameObject):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.rgb = 236, 236, 236
        self.hud = False


class Rope(GameObject):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.rgb = 72, 72, 0
        self.hud = False


class Snake(GameObject):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.rgb = 167, 26, 26
        self.hud = False


class Tarpit(GameObject):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.rgb = 0, 0, 0
        self.hud = False


class Waterhole(GameObject):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.rgb = 45, 109, 152
        self.hud = False


class Crocodile(GameObject):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.rgb = 20, 60, 0
        self.hud = False


class GoldenBar(GameObject):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.rgb = 252, 252, 84
        self.hud = False


class SilverBar(GameObject):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.rgb = 142, 142, 142
        self.hud = False


class Fire(GameObject):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.rgb = 236, 200, 96
        self.hud = False


class MoneyBag(GameObject):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.rgb = 111, 111, 111
        self.hud = False


class DiamondRing(GameObject):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.rgb = 236, 236, 236
        self.hud = False


class Platform(GameObject):
    """
    Permanent platforms.
    """
    
    def __init__(self, *args, **kwargs):
        super(Platform, self).__init__(*args, **kwargs)
        # x=0, y=0, w=8, h=4, 
        # self._xy = x, y
        # self._prev_xy = x, y
        # self.wh = w, h
        self.rgb = 167, 26, 26
        self.hud = False


class LifeCount(GameObject):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.rgb = 214, 214, 214
        self.hud = True


class PlayerScore(GameObject):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.rgb = 214, 214, 214
        self.hud = True


class Timer(GameObject):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.rgb = 214, 214, 214
        self.hud = True


def _detect_objects(objects, obs, hud=False):
    # detection and filtering
    # objects.clear()
    # Rope and wall is not working
    player = objects[0]

    player_bb = find_mc_objects(obs, playercolors, size=(7, 20), tol_s=4)
    # player_rope_bb = find_mc_objects(obs, playercolors_on_rope, size=(7, 20), tol_s=4)
    # print(player_rope_bb)
    if player_bb:
        player.xywh = player_bb[0]
    # elif player_rope_bb:
    #     player.xywh = player_rope_bb[0]


    wall = objects[1]
    wall_bb = find_mc_objects(obs, wallcolors, size=(
        7, 35), tol_s=5, closing_dist=5)  # ,miny=140,maxy=190,
    if wall_bb:
        if not wall:
            wall = Wall(*wall_bb[0])
            objects[1] = wall
        wall.xywh = wall_bb[0]
    else:
        objects[1] = NoObject()
    # for w in wall_bb:
    #     objects.append(Wall(*w))

    logs_bb = find_objects(obs, objects_colors["logs"],
                           size=(6, 14), tol_s=2, maxy=132, miny=114)
    match_objects(objects, logs_bb, 2, 3, Logs)


    # for l in logs:
    #     objects.append(Logs(*l))

    
    sp_bb = find_objects(obs, objects_colors["smallpit"], size=(
        8, 6), tol_s=1, maxy=130, miny=114)
    
    match_objects(objects, sp_bb, 5, 1, StairPit)
    # for s in sp:
    #     objects.append(StairPit(*s))


    sc_bb = find_objects(obs, objects_colors["scorpion"], size=(
        7, 10), tol_s=3, maxy=178, miny=160)
    match_objects(objects, sc_bb, 9, 1, Scorpion)
    # for s in sc:
    #     objects.append(Scorpion(*s))

    rope_slices = find_rope_segments(obs, objects_colors["rope"], seg_height=(
        1, 45), maxy=120, miny=70, minx=40, maxx=112)
    if rope_slices:
        lowest = max(rope_slices, key=lambda x: x[1])
        if lowest[3] > 1:
            lowest[1] = lowest[1]+lowest[3]-1
            lowest[3] = 1
        lowest = [tuple(lowest)]
        match_objects(objects, lowest, 10, 1, Rope)
    # if rope_slices:
    #     lowest = max(rope_slices, key=lambda x: x[1])
    #     if lowest[3] > 1:
    #         lowest[1] = lowest[1]+lowest[3]-1
    #         lowest[3] = 1
    #     objects.append(Rope(*lowest))
       

    snake_bb = find_mc_objects(obs, snakecolors, size=(
        8, 14), tol_s=5, maxy=132, miny=114)
    match_objects(objects, snake_bb, 11, 1, Snake)
    # for s in snake:
    #     objects.append(Snake(*s))

    
    tp_bb = find_objects(obs, objects_colors["smallpit"], size=(
        64, 10), tol_s=10, maxy=130, miny=114)  # same color as small pit
    match_objects(objects, tp_bb, 12, 1, Tarpit)
    # for s in tp:
    #     objects.append(Tarpit(*s))

    
    pp_bb = find_objects(obs, objects_colors["smallpit"], size=(
        12, 6), tol_s=1, maxy=130, miny=114)  # same color as small pit
    match_objects(objects, pp_bb, 7, 2, Pit)
    # for p in pp:
    #     objects.append(Pit(*p))

    
    wh_bb = find_objects(obs, objects_colors["waterhole"], size=(
        64, 10), tol_s=10, maxy=130, miny=114)
    match_objects(objects, wh_bb, 12, 1, Waterhole)
    # for w in wh:
    #     objects.append(Waterhole(*w))

    gold_bb = find_mc_objects(obs, goldenbarcolors, size=(
        7, 13), tol_s=3, maxy=132, miny=114, closing_dist=4)
    match_objects(objects, gold_bb, 20, 1, GoldenBar)
    # for g in gold:
    #     objects.append(GoldenBar(*g))

    sc_bb = find_objects(obs, objects_colors["crocodile"], size=(
        8, 8), tol_s=2, maxy=132, miny=114)
    match_objects(objects, sc_bb, 13, 3, Crocodile)
    # for c in sc:
    #     objects.append(Crocodile(*c))

    fire_bb = find_mc_objects(obs, firecolors, size=(
        8, 14), tol_s=3, maxy=132, miny=114, closing_dist=4)
    match_objects(objects, fire_bb, 17, 1, Fire)
    # for f in fire:
    #     objects.append(Fire(*f))

    mb_bb = find_mc_objects(obs, moneybagcolors, size=(
        7, 14), tol_s=3, maxy=132, miny=114, closing_dist=4)
    match_objects(objects, mb_bb, 18, 1, MoneyBag)
    # for b in mb:
    #     objects.append(MoneyBag(*b))

    gold_bb = find_mc_objects(obs, silverbarcolors, size=(
        7, 13), tol_s=3, maxy=132, miny=114, closing_dist=4)
    match_objects(objects, gold_bb, 19, 1, SilverBar)
    # for g in gold:
    #     objects.append(SilverBar(*g))

    gold_bb = find_mc_objects(obs, diamondringcolors, size=(
        7, 13), tol_s=3, maxy=132, miny=114, closing_dist=4)
    match_objects(objects, gold_bb, 20, 1, DiamondRing)
    # for g in gold:
    #     objects.append(DiamondRing(*g))

    if hud:
        lc = find_objects(obs, objects_colors['hud_objs'], size=(1, 8), tol_s=1, maxy=30, miny=20, minx=15, maxx=26, closing_active=False)
        match_objects(objects, lc, 23, 3, LifeCount)

        ps = find_objects(obs, objects_colors["hud_objs"], maxy=18, miny=7, minx=16, maxx=70, closing_dist=8)
        match_objects(objects, ps, 26, 2, PlayerScore)

        ts = find_objects(obs, objects_colors["hud_objs"], maxy=30, miny=20, minx=28, maxx=69, closing_dist=8)
        match_objects(objects, ps, 28, 1, Timer)
    """
    if hud:
        lc = find_objects(obs, objects_colors["hud_objs"], size=(1, 8), tol_s=1, maxy=30, miny=20, minx=15, maxx=26,
                          closing_active=False)
        for l in lc:
            objects.append(LifeCount(*l))
        ps = find_objects(
            obs, objects_colors["hud_objs"], maxy=18, miny=7, minx=16, maxx=70, closing_dist=8)
        for p in ps:
            objects.append(PlayerScore(*p))
        ts = find_objects(
            obs, objects_colors["hud_objs"], maxy=30, miny=20, minx=28, maxx=69, closing_dist=8)
        for t in ts:
            objects.append(Timer(*t))

        """
