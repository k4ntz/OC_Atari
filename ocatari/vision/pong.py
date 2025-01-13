from .utils import find_objects
from .game_objects import GameObject, NoObject


objects_colors = {
    "enemy": [213, 130, 74], "player": [92, 186, 92], "ball": [236, 236, 236],
    "background": [144, 72, 17], "player_score": [92, 186, 92],
    "enemy_score": [213, 130, 74]}


class Player(GameObject):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.rgb = 92, 186, 92


class Enemy(GameObject):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.rgb = 213, 130, 74


class Ball(GameObject):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.rgb = 236, 236, 236


class PlayerScore(GameObject):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.rgb = 92, 186, 92
        self.hud = True


class EnemyScore(GameObject):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.rgb = 213, 130, 74
        self.hud = True


def _detect_objects(objects, obs, hud=False):
    # detection and filtering
    player, ball, enemy = objects[:3]
    
    player_bb = find_objects(
        obs, objects_colors["player"], min_distance=1, miny=30)
    if player_bb:
        player.xywh = player_bb[0]
    
    ball_bb = find_objects(
        obs, objects_colors["ball"], min_distance=None, miny=34, maxy=194)
    if ball_bb:
        if not ball:
            ball = Ball(*ball_bb[0])
            objects[1] = ball
        ball.xywh = ball_bb[0]
    else:
        objects[1] = NoObject()

    enemy_bb = find_objects(
        obs, objects_colors["enemy"], min_distance=1, miny=30)
    if enemy_bb:
        if not enemy:
            enemy = Enemy(*enemy_bb[0])
            objects[2] = enemy
        enemy.xywh = enemy_bb[0]
    else:
        objects[2] = NoObject()
    if hud:
        player_score, enemy_score = objects[3:5]
        player_score_bb = find_objects(
            obs, objects_colors["player"], closing_dist=16, closing_active=True, maxy=30)
        if player_score_bb:
            player_score.xywh = player_score_bb[0]
        enemy_score_bb = find_objects(
            obs, objects_colors["enemy"], closing_dist=10, closing_active=True, maxy=30)
        if enemy_score_bb:
            enemy_score.xywh = enemy_score_bb[0]
