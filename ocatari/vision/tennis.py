from .utils import find_objects
from .game_objects import GameObject

objects_colors = {
    "enemy": [117, 128, 240], "player": [240, 128, 128], "ball": [236, 236, 236], "ball_shadow": [74, 74, 74],
    "logo": [240, 128, 128], "enemy_score": [117, 128, 240], "player_score": [240, 128, 128]}

fixed_objects_pos = {
    "player_score": [39, 4, 16, 8],
    "enemy_score": [104, 4, 16, 8],
    "logo": [39, 193, 33, 7]
}


class Player(GameObject):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.rgb = 240, 128, 128


class Enemy(GameObject):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.rgb = 117, 128, 240


class Ball(GameObject):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.rgb = 236, 236, 236


class BallShadow(GameObject):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.rgb = 74, 74, 74


class EnemyScore(GameObject):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.rgb = 117, 128, 240


class PlayerScore(GameObject):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.rgb = 240, 128, 128


def _detect_objects(objects, obs, hud):
    objects.clear()

    player = find_objects(obs, objects_colors["player"], min_distance=1, closing_dist=1)
    for p in player:
        if 5 < p[1] < 189 and p[2] > 10 and p[3] < 28:
            objects.append(Player(*p))

    enemy = find_objects(obs, objects_colors["enemy"], min_distance=1, closing_dist=1)
    for en in enemy:
        if 5 < en[1] < 189 and en[2] > 10 and en[3] < 28:
            objects.append(Enemy(*en))

    ball = find_objects(obs, objects_colors["ball"], min_distance=1)
    for b in ball:
        objects.append(Ball(*b))

    ball_shadow = find_objects(obs, objects_colors["ball_shadow"], min_distance=1)
    for b in ball_shadow:
        objects.append(BallShadow(*b))

    if hud:
        enemy_score = find_objects(obs, objects_colors["enemy_score"], min_distance=1, closing_dist=5)
        for enscr in enemy_score:
            if enscr[1] < 14:
                objects.append(EnemyScore(*enscr))

        player_score = find_objects(obs, objects_colors["player_score"], min_distance=1, closing_dist=5)
        for plrscr in player_score:
            if plrscr[1] < 14:
                objects.append(PlayerScore(*plrscr))
