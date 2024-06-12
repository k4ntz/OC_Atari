from .utils import find_objects
from .game_objects import GameObject

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


class Fruit(GameObject):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.rgb = 214, 92, 92


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
class Projectile_top(GameObject):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.rgb = 162, 98, 33


class Projectile_enemy(GameObject):
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


class Life(GameObject):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.rgb = 160, 171, 79


class Time(GameObject):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.rgb = 160, 171, 79


def _detect_objects(objects, obs, hud=True):
    objects.clear()

    player = find_objects(obs, objects_colors["kangaroo"], min_distance=1, miny=28)
    for bb in player:
        objects.append(Player(*bb))

    child = find_objects(obs, objects_colors["kangaroo"], min_distance=1, maxy=27)
    for bb in child:
        objects.append(Child(*bb))

    for i in objects_colors["fruit"]:
        fruit = find_objects(obs, objects_colors["fruit"][i], min_distance=1)
        for bb in fruit:
            if bb[1] < 170:
                fru = Fruit(*bb)
                fru.rgb = objects_colors["fruit"][i]
                objects.append(fru)

    bell = find_objects(obs, objects_colors["bell"], min_distance=1)
    for bb in bell:
        objects.append(Bell(*bb))

    # In this game both the enemy and their Projectile have the same color.
    # Both of them can be positioned at varios spots in the level,
    # which makes it almost impossible to differ between them
    enemy = find_objects(obs, objects_colors["enemy"], min_distance=1)

    for bb in enemy:
        if bb[2] > 5:
            en = Enemy(*bb)
            objects.append(en)

    p_enemy = find_objects(obs, objects_colors["projectile_enemy"], min_distance=1, size=(2, 3), tol_s=2)

    for bb in p_enemy:
        if bb[2] < 5:
            en = Projectile_enemy(*bb)
            objects.append(en)

    proj = find_objects(obs, objects_colors["projectile_top"], min_distance=1, minx=16, maxx=140, miny=3, maxy=27,
                        size=(2, 3), tol_s=2)

    for bb in proj:
        p = Projectile_top(*bb)
        objects.append(p)

    proj = find_objects(obs, objects_colors["projectile_top"], min_distance=1, minx=16, maxx=140, miny=35, maxy=70,
                        size=(2, 3), tol_s=2)

    for bb in proj:
        p = Projectile_top(*bb)
        objects.append(p)

    proj = find_objects(obs, objects_colors["projectile_top"], min_distance=1, minx=16, maxx=140, miny=80, maxy=123,
                        size=(2, 3), tol_s=2)

    for bb in proj:
        p = Projectile_top(*bb)
        objects.append(p)

    proj = find_objects(obs, objects_colors["projectile_top"], min_distance=1, minx=16, maxx=140, miny=128, maxy=171,
                        size=(2, 3), tol_s=2)

    for bb in proj:
        p = Projectile_top(*bb)
        objects.append(p)
    
    objects.append(Platform(16, 172, w=128))  # base platform
    objects.append(Platform(16, 28, w=128))  # top platform
    # if lvl_value < 23:
    objects.append(Ladder(132, 132))
    objects.append(Platform(16, 76, w=128))
    objects.append(Ladder(20, 85))
    objects.append(Platform(16, 124, w=128))
    objects.append(Ladder(132, 37))

    if hud:
        life = find_objects(obs, objects_colors["hud"], min_distance=1, minx=10, maxx=40)
        for bb in life:
            objects.append(Life(*bb))

        time = find_objects(obs, objects_colors["hud"], min_distance=1, minx=70, maxx=100)
        for bb in time:
            objects.append(Time(*bb))

        score = find_objects(obs, objects_colors["hud"], closing_dist=6, minx=100, maxx=150)
        for bb in score:
            objects.append(Score(*bb))
