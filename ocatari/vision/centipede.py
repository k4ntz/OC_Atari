from .game_objects import GameObject
from .utils import find_objects


objects_colors = {'centipede': [184, 70, 162], 'player_and_projectile_and_wall': [181, 83, 40],
                  'bug': [146, 70, 192], 'life_and_score': [188, 144, 252], 'ground': [110, 156, 66]}


class CentipedeSegment(GameObject):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.rgb = [184, 70, 162]


class Player(GameObject):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.rgb = [181, 83, 40]


class Projectile(GameObject):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.rgb = [181, 83, 40]


class Wall(GameObject):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.rgb = [181, 83, 40]


class Bug(GameObject):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.rgb = [146, 70, 192]


class Life(GameObject):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.rgb = [188, 144, 252]


class Score(GameObject):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.rgb = [188, 144, 252]


class Ground(GameObject):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.rgb = [110, 156, 66]


def _detect_objects_centipede(objects, obs, hud=False):
    objects.clear()

    centipede = find_objects(obs, objects_colors['centipede'], min_distance=1)
    for bb in centipede:
        objects.append(CentipedeSegment(*bb))

    player_and_walls = find_objects(obs, objects_colors['player_and_projectile_and_wall'], min_distance=1, closing_dist=1)
    for bb in player_and_walls:
        if bb[3] > 4:
            if bb[2] > 3:
                objects.append(Player(*bb))
            else:
                objects.append(Projectile(*bb))
        else:
            objects.append(Wall(*bb))

    bug = find_objects(obs, objects_colors['bug'], min_distance=1)
    for bb in bug:
        objects.append(Bug(*bb))

    if hud:
        life_and_score = find_objects(obs, objects_colors['life_and_score'], min_distance=1)
        for bb in life_and_score:
            if bb[0] < 70:
                objects.append(Life(*bb))

            else:
                objects.append(Score(*bb))

        ground = find_objects(obs, objects_colors['ground'], min_distance=1)
        for bb in ground:
            objects.append(Ground(*bb))

