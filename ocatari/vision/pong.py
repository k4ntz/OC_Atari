from .utils import find_objects
from .game_objects import GameObject


objects_colors = {
    "enemy": [213, 130, 74], "player": [92, 186, 92], "ball": [236, 236, 236],
    "background": [144, 72, 17], "player_score": [92, 186, 92],
    "enemy_score": [213, 130, 74], "player_score_2": [92, 186, 92],
    "enemy_score_2": [213, 130, 74]}


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
    objects.clear()
    enemy = find_objects(obs, objects_colors["enemy"], min_distance=1, miny=30)
    for el in enemy:
        if el[1] > 30:
            objects.append(Enemy(*el))
    if hud:
        enemy_score = find_objects(obs, objects_colors["enemy"], min_distance=1, closing_active=False, maxy=30)
        for el in enemy_score:
            objects.append(EnemyScore(*el))
    player = find_objects(obs, objects_colors["player"], min_distance=1, miny=30)
    for el in player:
        objects.append(Player(*el))
    if hud:
        playerscore = find_objects(obs, objects_colors["player"], min_distance=1, closing_active=False, maxy=30)
        for el in playerscore:
            objects.append(PlayerScore(*el))
    ball = find_objects(obs, objects_colors["ball"], min_distance=None)
    for el in ball:
        if el[2] < 20:
            objects.append(Ball(*el))
