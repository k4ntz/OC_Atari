from .game_objects import GameObject
from .utils import find_objects, find_mc_objects, most_common_color
import numpy as np

objects_colors = {'black': [0, 0, 0], 'skin_1': [228, 111, 111], 'skin_2': [200, 72, 72], 'white': [236, 236, 236],
                  'yellow_1': [162,162, 42], 'yellow_2': [210, 210, 64], 'yellow_3': [168, 168, 51], 'yellow_4': [252, 252, 84],
                  'blue_1': [24, 26, 167], 'blue_2': [0, 0, 148], 'blue_3': [132, 144, 252], 'blue_4': [66, 72, 200],
                  'white': [236, 236, 236], 'grey': [188, 188, 188], 'green_1': [110, 156, 66], 'green_2': [82, 126, 45],
                  'brown': [163, 57, 21], 'red': [184, 50, 50], 'pink': [236, 140, 224],
                  'playercolors': [[0, 0, 0], [228, 111, 111]], 'necklace_colors': [[252, 252, 84], [236, 236, 236]],
                  'playercolors2': [[0, 0, 0], [200, 72, 72], [228, 111, 111], [162, 162, 42], [210, 210, 64], [252, 252, 64], [24, 26, 167]],
                  'vase_colors': [[236, 140, 224], [252, 144, 144], [240, 170, 103], [240, 128, 128], [224, 124, 210],
                                 [197, 124, 238], [169, 128, 240]],
                  'stamp_colors': [[204, 216, 110], [183, 194, 95], [224, 236, 124], [200, 252, 132],
                                   [144, 252, 144], [132, 252, 212]]}


class Player(GameObject):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.rgb = [210, 210, 64]


class Car(GameObject):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.rgb = [0, 0, 0]


class Badguy(GameObject):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.rgb = [24, 26, 167]


class Clue(GameObject):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.rgb = [24, 26, 167]


class Mud(GameObject):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.rgb = [0, 0, 0]


class Dove(GameObject):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.rgb = [236, 236, 236]


class Lizard(GameObject):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.rgb = [210, 210, 64]


class Pottet_Plant(GameObject):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.rgb = [210, 210, 64]


class Brick(GameObject):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.rgb = [184, 50, 50]


class Barrier(GameObject):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.rgb = [252, 252, 84]


class Gun_Sign(GameObject):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.rgb = [132, 144, 252]


class Police_Sign(GameObject):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.rgb = [236, 236, 236]


class Bank_Sign(GameObject):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.rgb = [82, 126, 45]


class Money_Bag(GameObject):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.rgb = [236, 236, 236]


class Gun(GameObject):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.rgb = [0, 0, 0]


class Button(GameObject):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.rgb = [252, 252, 84]


class Comb(GameObject):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.rgb = [0, 0, 0]


class Shoe_Sole(GameObject):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.rgb = [0, 0, 0]


class Vase(GameObject):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.rgb = [252, 144, 144]


class Necklace(GameObject):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.rgb = [252, 252, 84]


class Stamp(GameObject):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.rgb = [132, 252, 212]


class Badguy_Head(GameObject):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.rgb = [24, 26, 167]


#  ---- HUD -----
class Clock(GameObject):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.rgb = [236, 236, 236]


class Score(GameObject):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.rgb = [236, 236, 236]

global static_bricks
static_bricks = None

def _detect_objects(objects, obs, hud=False):
    objects.clear()

    car = find_objects(obs, objects_colors['black'], minx=8, miny=130, maxx=159, maxy=182, size=(20, 14), tol_s=5, min_distance=2, closing_dist=2)
    for bb in car:
        objects.append(Car(*bb))

    players = find_mc_objects(obs, colors=objects_colors['playercolors'], minx=8, miny=50, maxx=159, maxy=162, size=(8, 10), tol_s=3, closing_dist=5)
    for bb in players:
        ply = Player(*bb)
        if bb[1] < 140:
            ply.wh = 8, 25
        objects.append(ply)

    clue = find_mc_objects(obs, colors=[objects_colors['black'], objects_colors['blue_1'], objects_colors['white']], minx=8, miny=30, maxx=159, maxy=162, size=(8,13), tol_s=5, all_colors=True)
    for bb in clue:
        cl = Clue(*bb)
        cl.xy = bb[0] - int(np.ceil((8-bb[2])/2)), bb[1]
        cl.wh = 8, bb[3]
        objects.append(cl)

    mud = find_objects(obs, objects_colors['black'], minx=8, miny=160, maxx=159, maxy=182, size=(8, 4), tol_s=1, min_distance=2, closing_dist=1)
    for bb in mud:
        objects.append(Mud(*bb))

    plant = find_mc_objects(obs, colors=[objects_colors['yellow_2'], objects_colors['green_1'], objects_colors['brown']], minx=8, miny=30, maxx=159, maxy=162, closing_dist=3, all_colors=True)
    for bb in plant:
        objects.append(Pottet_Plant(*bb))

    global static_bricks
    brick = find_objects(obs, objects_colors['red'], minx=8, miny=30, maxx=159, maxy=182, closing_dist=1, size=(4,4), tol_s=2)
    for bb in brick:
        if bb not in static_bricks:
            objects.append(Brick(*bb))
    static_bricks = brick

    barrier = find_mc_objects(obs, colors=[objects_colors['black'], objects_colors['yellow_4']], miny=50, maxy=182, size=(8,17), tol_s=4,all_colors=True)
    for bb in barrier:
        objects.append(Barrier(*bb))

    # gun_sign = find_mc_objects(obs, [objects_colors['blue_3'], objects_colors['blue_4']], minx=62, miny=28, maxx=96, maxy=51)
    # for bb in gun_sign:
    #     objects.append(Gun_Sign(*bb))

    # police_sign = find_mc_objects(obs, [objects_colors['white'], objects_colors['black']], minx=62, miny=28, maxx=96, maxy=51)
    # for bb in police_sign:
    #     objects.append(Police_Sign(*bb))

    # bank_sign = find_mc_objects(obs, [objects_colors['green_2'], objects_colors['pink']], minx=62, miny=29, maxx=96, maxy=50)
    # for bb in bank_sign:
    #     objects.append(Bank_Sign(*bb))
    
    dove = find_objects(obs, objects_colors['white'], minx=8, miny=30, maxx=159, maxy=182, size=(8,6), tol_s=2)
    for bb in dove:
        objects.append(Dove(*bb))
    
    lizard = find_objects(obs, objects_colors['yellow_2'], minx=8, miny=30, maxx=159, maxy=182, size=(8,6), tol_s=2)
    for bb in lizard:
        objects.append(Lizard(*bb))

    # mccolor = most_common_color(obs[0:182, :, :])

    # if mccolor == (135, 183, 84):

    #     badguy = find_mc_objects(obs, colors=[objects_colors['blue_2'], objects_colors['black'], objects_colors['yellow_4']], minx=8, miny=60, maxx=159, maxy=162, closing_dist=5, size=(8,10), tol_s=5, all_colors=True)
    #     for bb in badguy:
    #         objects.append(Badguy(*bb))

    money = find_objects(obs, objects_colors['white'], minx=138, miny=27, maxx=159, maxy=46, size=(8, 11), tol_s=1)
    for bb in money:
        objects.append(Money_Bag(*bb))

    gun = find_objects(obs, objects_colors['black'], minx=138, miny=27, maxx=159, maxy=46, size=(8,8), tol_s=1)
    for bb in gun:
        objects.append(Gun(*bb))

    button = find_objects(obs, objects_colors['yellow_4'], minx=138, miny=27, maxx=159, maxy=46, size=(7,9), tol_s=1)
    for bb in button:
        objects.append(Button(*bb))

    comb = find_objects(obs, objects_colors['black'], minx=138, miny=27, maxx=159, maxy=46, size=(8,15), tol_s=1)
    for bb in comb:
        objects.append(Comb(*bb))

    sole = find_objects(obs, objects_colors['black'], minx=138, miny=27, maxx=159, maxy=46, size=(8,11), tol_s=1)
    for bb in sole:
        objects.append(Shoe_Sole(*bb))
    
    vase = find_mc_objects(obs, colors=objects_colors['vase_colors'], minx=138, miny=27, maxx=159, maxy=46, size=(8,14), tol_s=1, all_colors=True)
    for bb in vase:
        objects.append(Vase(*bb))
    
    necklace = find_mc_objects(obs, colors=objects_colors['necklace_colors'], minx=138, miny=27, maxx=159, maxy=46, size=(8,11), tol_s=1, all_colors=True)
    for bb in necklace:
        objects.append(Necklace(*bb))
    
    stamp = find_mc_objects(obs, colors=objects_colors['stamp_colors'], minx=138, miny=27, maxx=159, maxy=46, size=(8,14), tol_s=1, all_colors=True)
    for bb in stamp:
        objects.append(Stamp(*bb))
    
    badguy_head = find_mc_objects(obs, colors=[objects_colors['blue_1'], objects_colors['black'], objects_colors['yellow_4']], minx=138, miny=27, maxx=159, maxy=46, size=(8,7), tol_s=1, all_colors=True)
    for bb in badguy_head:
        objects.append(Badguy_Head(*bb))

    if hud:

        scores = find_objects(obs, objects_colors['white'], maxy=16, closing_dist=8)
        for bb in scores:
            objects.append(Score(*bb))

        time = find_objects(obs, objects_colors['white'], miny=19, maxy=27, closing_dist=8)
        for bb in time:
            objects.append(Clock(*bb))
