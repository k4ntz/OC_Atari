from .utils import find_objects, find_mc_objects
from .game_objects import GameObject


objects_colors = {'player': [184, 70, 162], 'enemy': [[104, 72, 198], [213, 130, 74], [214, 92, 92], [92, 186, 92]],
                  'projectile_friendly': [212, 140, 252], 'projectile_hostile': [252, 144, 144],
                  'live': [240, 128, 128], 'score': [223, 183, 85]}


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


def _detect_objects_demon_attack(objects, obs, hud=False):
    objects.clear()

    player = find_objects(obs, objects_colors["player"], min_distance=1)
    if len(player) >= 1:
        objects.append(Player(*player[0]))

    # enemy = find_objects(obs, objects_colors["enemy"], min_distance=1)
    enemy = find_mc_objects(obs, objects_colors["enemy"])
    # index = 0
    for bb in enemy:
        # name = "enemy"+str(index)
        # index += 1
        objects.append(Enemy(*bb))

    if hud:
        score = find_objects(obs, objects_colors["score"], min_distance=1, closing_dist=5)
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
