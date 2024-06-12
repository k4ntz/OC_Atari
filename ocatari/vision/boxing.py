from .utils import find_objects
from .game_objects import GameObject


objects_colors = {
    "player": [214, 214, 214], "enemy": [0, 0, 0],
    "player_score": [214, 214, 214], "enemy_score": [0, 0, 0],
    "hud_objs": [20, 60, 0]
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
    objects.clear()
    enemy = find_objects(obs, objects_colors["enemy"], min_distance=1, closing_dist=6)
    for el in enemy:
        if el[1] > 30:
            objects.append(Enemy(*el))
        elif hud:
            objects.append(EnemyScore(*el))
    player = find_objects(obs, objects_colors["player"], min_distance=1, closing_dist=6)
    for el in player:
        if el[1] > 30:
            objects.append(Player(*el))
        elif hud:
            objects.append(PlayerScore(*el))
    if hud:
        huds = find_objects(obs, objects_colors["hud_objs"], closing_active=False, maxy=25)
        for el in huds:
            objects.append(Clock(*el))
