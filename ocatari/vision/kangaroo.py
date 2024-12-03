from .utils import find_objects, match_objects, match_blinking_objects
from .game_objects import GameObject, NoObject

objects_colors = {"kangaroo": [223, 183, 85], "bell": [210, 164, 74],
                  "fruit": {"red": [214, 92, 92], "yellow": [195, 144, 61]},
                  "hud": [160, 171, 79], "enemy": [227, 151, 89],
                  "projectile_enemy": [227, 151, 89], "projectile_top": [162, 98, 33]
                  }


class Player(GameObject):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.rgb = 223, 183, 85


class Child(GameObject):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.rgb = 223, 183, 85


class Enemy(GameObject):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.rgb = 227, 151, 89
        self.num_frames_invisible = -1
        self.max_frames_invisible = 4


class Fruit(GameObject):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.rgb = 214, 92, 92
        self.num_frames_invisible = -1
        self.max_frames_invisible = 4

class Ladder(GameObject):
    def __init__(self, x=0, y=0, w=8, h=35, *args, **kwargs):
        super(Ladder, self).__init__(x, y, w, h, *args, **kwargs)
        self._xy = x, y
        self._prev_xy = x, y
        self.wh = w, h
        self.rgb = 162, 98, 33
        self.hud = False


class Platform(GameObject):
    def __init__(self, x=0, y=0, w=8, h=4, *args, **kwargs):
        super(Platform, self).__init__(x, y, w, h, *args, **kwargs)
        self._xy = x, y
        self._prev_xy = x, y
        self.wh = w, h
        self.rgb = 162, 98, 33
        self.hud = False

# The color of this object matches with the walls, floors and ladders, it can therefore not be detected Properly
class FallingCoconut(GameObject):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.rgb = 162, 98, 33


class ThrownCoconut(GameObject):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.rgb = 227, 159, 89


class Bell(GameObject):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.rgb = 210, 164, 74


class Score(GameObject):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.rgb = 160, 171, 79


class Lives(GameObject):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.rgb = 160, 171, 79


class Time(GameObject):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.rgb = 160, 171, 79


def _detect_objects(objects, obs, hud=False):

    player = find_objects(obs, objects_colors["kangaroo"], min_distance=1, miny=28)
    if player:
        objects[0].xywh = player[0]
        # match_blinking_objects(objects, player, 10, 3, Player)

    child = find_objects(obs, objects_colors["kangaroo"], min_distance=1, maxy=27)
    if child:
        objects[1].xywh = child[0]

    fruit = []
    for i in objects_colors["fruit"]:
        fruit.extend(find_objects(obs, objects_colors["fruit"][i], min_distance=1))
    match_blinking_objects(objects, fruit, 10, 3, Fruit)

    bell = find_objects(obs, objects_colors["bell"], min_distance=1)
    if bell:
        objects[13].xywh = bell[0]

    # In this game both the enemy and their Projectile have the same color.
    # Both of them can be positioned at varios spots in the level,
    # which makes it almost impossible to differ between them
    enemy = find_objects(obs, objects_colors["enemy"], min_distance=1)

    for bb in enemy:
        if bb[2] <= 5:
            enemy.remove(bb)
    match_blinking_objects(objects, enemy, 2, 4, Enemy)

    p_enemy = find_objects(obs, objects_colors["projectile_enemy"], min_distance=1, size=(2, 3), tol_s=2)

    for bb in p_enemy:
        if bb[2] >= 5:
            p_enemy.remove(bb)
    match_objects(objects, p_enemy, 7, 3, ThrownCoconut)

    proj = find_objects(obs, objects_colors["projectile_top"], min_distance=1, minx=16, maxx=140, miny=3, maxy=27,
                        size=(2, 3), tol_s=2)
    proj.extend(find_objects(obs, objects_colors["projectile_top"], min_distance=1, minx=16, maxx=140, miny=35, maxy=70,
                        size=(2, 3), tol_s=2))
    proj.extend(find_objects(obs, objects_colors["projectile_top"], min_distance=1, minx=16, maxx=140, miny=80, maxy=123,
                        size=(2, 3), tol_s=2))
    proj.extend(find_objects(obs, objects_colors["projectile_top"], min_distance=1, minx=16, maxx=140, miny=128, maxy=171,
                        size=(2, 3), tol_s=2))


    if proj:
        if type(objects[6]) is NoObject:
            objects[6] = FallingCoconut(*proj[0])
        else:
            objects[6].xywh = proj[0]
    else:
        objects[6] = NoObject()

    if hud:
        life = find_objects(obs, objects_colors["hud"], closing_dist=8, minx=10, maxx=40)
        objects[-1].xywh = life[0]

        time = find_objects(obs, objects_colors["hud"], min_distance=1, minx=70, maxx=100)
        objects[-2].xywh = time[0]

        score = find_objects(obs, objects_colors["hud"], closing_dist=6, minx=100, maxx=150)
        objects[-3].xywh = score[0]
