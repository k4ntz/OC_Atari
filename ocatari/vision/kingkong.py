from .utils import find_mc_objects, find_objects, match_objects
from .game_objects import GameObject


object_colors = {
    'player': [[207, 175, 92], [201, 154, 92], [92, 197, 135], [50, 50, 176], [151, 151, 151]],
    'enemy': [150, 113, 26],
    'girlfriend': [[207, 175, 92], [201, 154, 92], [92, 197, 135], [50, 50, 176]],
    'bombs': {
        'bomb_1': [[207, 175, 92], [140, 172, 72], [50, 142, 142], [132, 26, 116], [160, 107, 50], [190, 156, 72]],
        'bomb_2': [[223, 192, 111], [92, 184, 184], [95, 50, 171], [26, 128, 53], [47, 117, 160], [92, 92, 210]]
    },
    'ladder': [201, 92, 135],
    'bonus_points': [160, 194, 92],
    'score': [160, 194, 92]
}


class Player(GameObject):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.rgb = 92, 197, 135


class Girlfriend(GameObject):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.rgb = 201, 154, 92


class Enemy(GameObject):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.rgb = 150, 113, 26


class Bomb(GameObject):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


class Ladder(GameObject):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.rgb = 201, 92, 135


class Score(GameObject):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


class BonusPoints(GameObject):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


def _detect_objects(objects, obs, hud=False):

    player = objects[0]
    player_bb = find_mc_objects(
        obs, object_colors['player'], size=(8, 20), maxy=260)
    if player_bb:
        player.xywh = player_bb[0]

    enemy = objects[1]
    enemy_bb = find_objects(
        obs, object_colors['enemy'], size=(15, 33), maxy=260)
    if enemy_bb:
        enemy.xywh = enemy_bb[0]

    girlfriend = objects[2]
    girlfriend_bb = find_mc_objects(
        obs, object_colors['girlfriend'], size=(6, 17), all_colors=True, tol_s=2)
    if girlfriend_bb:
        girlfriend.xywh = girlfriend_bb[0]

    bombs_bb = []
    for i in object_colors['bombs']:
        bombs_bb.extend([list(bb) + object_colors['bombs'][i]
                        for bb in find_mc_objects(obs, object_colors['bombs'][i], maxy=260)])
    match_objects(objects, bombs_bb, 3, 8, Bomb)

    if hud:
        score_bb = find_objects(
            obs, object_colors['score'], closing_dist=5, maxx=80)
        match_objects(objects, score_bb, len(objects)-2, 1, Score)

        bonus_points_bb = find_objects(
            obs, object_colors['bonus_points'], closing_dist=5, minx=81)
        match_objects(objects, bonus_points_bb, len(objects)-1, 1, BonusPoints)
