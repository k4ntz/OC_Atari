from .utils import find_objects, find_mc_objects
from .game_objects import GameObject


objects_colors = {'player': [184, 70, 162],
                  'projectile_friendly': [212, 140, 252], 'projectile_hostile': [252, 144, 144],
                  'live': [240, 128, 128], 'score': [223, 183, 85],
                  'enemy': [
                      [72, 160, 72], 
                      [84, 92, 214], [84, 138, 210], [84, 160, 197], [84, 184, 153], [92, 186, 92],
                      [101, 111, 228], [104, 72, 198], [127, 92, 213], [149, 111, 227], 
                      [181, 108, 224], [195, 144, 61], [197, 124, 238],
                      [212, 108, 195], [213, 130, 74], [214, 92, 92], [214, 214, 214], 
                      [224, 236, 124], [227, 151, 89], [228, 111, 111], 
                            ]}


class Player(GameObject):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.rgb = 184, 70, 162


class Enemy(GameObject):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.rgb = 213, 130, 74


class ProjectileFriendly(GameObject):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.rgb = 212, 140, 252


class ProjectileHostile(GameObject):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.rgb = 252, 144, 144


class Score(GameObject):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.rgb = 223, 183, 85


class Live(GameObject):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.rgb = 240, 128, 128


def _detect_objects(objects, obs, hud=False):
    objects.clear()

    player = find_objects(obs, objects_colors["player"], min_distance=1)
    if len(player) >= 1:
        objects.append(Player(*player[0]))

    # enemy = find_objects(obs, objects_colors["enemy"], min_distance=1)
    enemy = find_mc_objects(obs, objects_colors["enemy"], 
                            closing_dist=4, all_colors=False,
                            size=(14,7), tol_s=(3,3), miny=10, maxy=180)
    enemy += find_mc_objects(obs, objects_colors["enemy"], 
                            closing_dist=1, all_colors=False,
                            size=(7,4), tol_s=(2,2), miny=10, maxy=180)
    # index = 0
    for bb in enemy:
        # name = "enemy"+str(index)
        # index += 1
        objects.append(Enemy(*bb))

    if hud:
        score = find_objects(obs, objects_colors["score"], min_distance=1, closing_dist=5, maxy=20)
        for s in score:
            objects.append(Score(*s))

        live = find_objects(obs, objects_colors["live"], min_distance=1)
        for l1 in live:
            objects.append(Live(*l1))

    proj_friendly = find_objects(obs, objects_colors['projectile_friendly'], min_distance=1)
    for proj in proj_friendly:
        objects.append(ProjectileFriendly(*proj))

    proj_hostile = find_objects(obs, objects_colors['projectile_hostile'], min_distance=1)
    for proj in proj_hostile:
        objects.append(ProjectileHostile(*proj))
