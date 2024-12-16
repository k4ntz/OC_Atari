from .utils import find_objects
from .game_objects import GameObject


objects_colors = {
    "player": [214, 214, 214], "enemy": [0, 0, 0],
    "player_score": [214, 214, 214], "enemy_score": [0, 0, 0],
    "clock": [20, 60, 0]
}


class Player(GameObject):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.rgb = 214, 214, 214
        self.hud = False


class Enemy(GameObject):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.rgb = 0, 0, 0
        self.hud = False


class Clock(GameObject):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.rgb = 20, 60, 0
        self.hud = True


class PlayerScore(GameObject):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.rgb = 214, 214, 214
        self.hud = True


class EnemyScore(GameObject):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.rgb = 0, 0, 0
        self.hud = True


def _detect_objects(objects, obs, hud=False):
    # detection and filtering
    player, enemy = objects[:2]
    player_bb = find_objects(
        obs, objects_colors["player"], min_distance=1, closing_dist=6, miny=30)
    if player_bb:
        player.xywh = player_bb[0]
    enemy_bb = find_objects(
        obs, objects_colors["enemy"], min_distance=1, closing_dist=6, miny=30)
    if enemy_bb:
        enemy.xywh = enemy_bb[0]
    if hud:
        player_score, enemy_score, clock = objects[2:5]
        playersc_bb = find_objects(
            obs, objects_colors["player"], min_distance=1, closing_dist=6, maxy=30)
        if playersc_bb:
            player_score.xywh = playersc_bb[0]
        enemysc_bb = find_objects(
            obs, objects_colors["enemy"], min_distance=1, closing_dist=6, maxy=30)
        if enemysc_bb:
            enemy_score.xywh = enemysc_bb[0]
        clock_bb = find_objects(
            obs, objects_colors["clock"], closing_active=True, maxy=25, closing_dist=15)
        if clock_bb:
            clock.xywh = clock_bb[0]
