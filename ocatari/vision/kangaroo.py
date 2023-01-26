from .utils import find_objects
from .game_objects import GameObject

objects_colors = {"kangaroo": [223, 183, 85], "bell": [210, 164, 74],
                  "fruit": {"red": [214, 92, 92], "yellow": [195, 144, 61]}, "hud": [160, 171, 79], "enemy": [227,151,89],
                  "projectile": [162, 98, 33]
                  }


class Kangaroo(GameObject):
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


# This is the object falling from the Top onto you or the one thrown at you
class Projectile(GameObject):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.rgb = 162, 98, 33


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


def _detect_objects_kangaroo(objects, obs, hud=True):
    objects.clear()

    kangaroo = find_objects(obs, objects_colors["kangaroo"], min_distance=1)
    for bb in kangaroo:
        objects.append(Kangaroo(*bb))

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

    enemy = find_objects(obs, objects_colors["enemy"], min_distance=1)

    for bb in enemy:
        en = Enemy(*bb)
        objects.append(en)

    proj = find_objects(obs, objects_colors["projectile"], min_distance=0.1, minx=16, maxx= 140, maxy=27)
    
    if len(proj) != 0:
        for bb in proj:
            p = Projectile(*bb)
            objects.append(p)

    proj = find_objects(obs, objects_colors["projectile"], min_distance=0.1, minx=16, maxx= 131, miny=35, maxy=70)
    print(proj)
    if len(proj) != 0:
        for bb in proj:
            p = Projectile(*bb)
            objects.append(p)

    proj = find_objects(obs, objects_colors["projectile"], min_distance=0.1, minx=16, maxx= 140, miny=80, maxy=123)
    if len(proj) != 0:
        for bb in proj:
            p = Projectile(*bb)
            objects.append(p)

    proj = find_objects(obs, objects_colors["projectile"], min_distance=0.1, minx=16, maxx= 140, miny=128, maxy=171)
    if len(proj) != 0:
        for bb in proj:
            p = Projectile(*bb)
            objects.append(p)

    proj = find_objects(obs, objects_colors["projectile"], min_distance=0.1, minx=16, maxx= 140, miny=176)
    if proj:
        for bb in proj:
            p = Projectile(*bb)
            objects.append(p)


    if hud:
        life = find_objects(obs, objects_colors["hud"], min_distance=1, minx=10, maxx= 40)
        for bb in life:
            objects.append(Life(*bb))

        time = find_objects(obs, objects_colors["hud"], min_distance=1, minx=70, maxx= 100)
        for bb in time:
            objects.append(Time(*bb))

        score = find_objects(obs, objects_colors["hud"], min_distance=1, minx=120, maxx= 150)
        for bb in score:
            objects.append(Score(*bb))
