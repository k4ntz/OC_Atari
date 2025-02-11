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
        self.expected_dist = 12


class Fruit(GameObject):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.rgb = 214, 92, 92
        self.num_frames_invisible = -1
        self.max_frames_invisible = 2
        self.expected_dist = 1


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
        self.hud = True


class Lives(GameObject):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.rgb = 160, 171, 79
        self.hud = True


class Time(GameObject):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.rgb = 160, 171, 79
        self.hud = True


def _detect_objects(objects, obs, hud=False):

    player = find_objects(
        obs, objects_colors["kangaroo"], min_distance=1, miny=28)
    if player:
        objects[0].xywh = player[0]
        # match_blinking_objects(objects, player, 10, 3, Player)

    child = find_objects(
        obs, objects_colors["kangaroo"], min_distance=1, maxy=27)
    if child:
        objects[1].xywh = child[0]

    fruit = []
    for i in objects_colors["fruit"]:
        fruit.extend(find_objects(
            obs, objects_colors["fruit"][i], min_distance=1))
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
    # match_objects(objects, enemy, 2, 4, Enemy)
    match_blinking_objects(objects, enemy, 2, 4, Enemy)

    p_enemy = find_objects(
        obs, objects_colors["projectile_enemy"], min_distance=1, size=(2, 3), tol_s=2)

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

    platform = None
    if obs[124][45][0] == 162:
        if type(objects[14]) is not Ladder() or objects[14].xy != (132, 132):
            platform = manage_platforms(0, objects)
    elif obs[142][44][0] == 162:
        if type(objects[14]) is not Ladder() or objects[14].xy != (120, 132):
            platform = manage_platforms(2, objects)
    elif obs[148][76][0] == 162:
        if type(objects[14]) is not Ladder() or objects[14].xy != (20, 36):
            platform = manage_platforms(1, objects)

    if platform is not None:
        for i in range(26):
            if platform[i]:
                objects[14+i] = platform[i]
            else:
                objects[14+i] = NoObject()

    if hud:
        life = find_objects(
            obs, objects_colors["hud"], closing_dist=8, minx=10, maxx=40)
        objects[-1].xywh = life[0]

        time = find_objects(
            obs, objects_colors["hud"], min_distance=1, minx=70, maxx=100)
        objects[-2].xywh = time[0]

        score = find_objects(
            obs, objects_colors["hud"], closing_dist=6, minx=100, maxx=150)
        objects[-3].xywh = score[0]


def manage_platforms(current_lvl_val, _):
    platforms = []

    # There is a total of 3 levels
    if current_lvl_val == 0:
        platforms = [
            Ladder(132, 132),
            Ladder(20, 85),
            Ladder(132, 37),
            NoObject(),
            NoObject(),
            NoObject(),
            Platform(16, 172, w=128), Platform(16, 28, w=128),
            Platform(16, 76, w=128),
            Platform(16, 124, w=128),
        ]
        platforms.extend([NoObject()]*16)

    elif current_lvl_val == 1:
        platforms = [
            Ladder(120, 132, h=4),
            Ladder(24, 116, h=4),
            Ladder(128, 36, h=4),
            NoObject(),
            NoObject(),
            NoObject(),
            Platform(16, 172, w=128), Platform(16, 28, w=128),
            Platform(16, 124, w=28), Platform(52, 124, w=92),
            Platform(16, 76, w=60), Platform(84, 76, w=60),
            Platform(28, 164, w=24), Platform(112, 84, w=24),
            Platform(120, 44, w=24), Platform(48, 156, w=32),
            Platform(76, 148, w=32), Platform(104, 140, w=32),
            Platform(16, 108, w=32), Platform(56, 100, w=20),
            Platform(84, 92, w=20), Platform(64, 60, w=20),
            Platform(92, 52, w=20), Platform(28, 68, w=28)
        ]
        platforms.extend([NoObject()]*2)

    else:  # current_lvl_val == 2
        platforms = [
            Ladder(20, 36, h=28),
            Ladder(20, 148, h=4),
            Ladder(36, 116, h=20),
            Ladder(104, 36, h=20),
            Ladder(120, 68, h=4),
            Ladder(132, 84, h=4), Platform(
                16, 172, w=128), Platform(16, 28, w=128),
            Platform(88, 140, w=16), Platform(
                64, 148, w=16), Platform(100, 116, w=16),
            Platform(48, 100, w=16), Platform(
                76, 52, w=16), Platform(80, 36, w=16),
            Platform(104, 132, w=20), Platform(
                84, 156, w=20), Platform(124, 124, w=20),
            Platform(52, 84, w=20), Platform(
                108, 164, w=36), Platform(16, 108, w=80),
            Platform(16, 92, w=28), Platform(
                76, 92, w=68), Platform(16, 140, w=32),
            Platform(96, 60, w=36), Platform(
                100, 76, w=44), Platform(60, 44, w=12)
        ]

    return platforms
