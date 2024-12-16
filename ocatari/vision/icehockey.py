from .utils import find_objects, find_mc_objects
from .game_objects import GameObject

objects_colors = {"ball": [0, 0, 0], "enemyscore": [
    236, 200, 96], "playerscore": [84, 92, 214], "timer": [84, 92, 214]}
hud_color = [132, 144, 252]
player_colors = [[45, 50, 184], [200, 72, 72], [184, 50, 50]]
enemy_colors = [[200, 72, 72], [210, 182, 86], [232, 204, 99], [82, 126, 45]]


class Player(GameObject):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.rgb = 45, 50, 184
        self.hud = False


class Enemy(GameObject):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.rgb = 82, 126, 45
        self.hud = False


class Ball(GameObject):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.rgb = 0, 0, 0
        self.hud = False


class PlayerScore(GameObject):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.rgb = 84, 92, 214
        self.hud = True


class EnemyScore(GameObject):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.rgb = 236, 200, 96
        self.hud = True


class Timer(GameObject):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.rgb = 84, 92, 214
        self.hud = True


def _detect_objects(objects, obs, hud=False):
    # detection and filtering
    objects.clear()
    player = find_mc_objects(obs, player_colors, size=(
        16, 20), tol_s=10, closing_dist=3)
    for p in player:
        objects.append(Player(*p))

    enemy = find_mc_objects(obs, enemy_colors, size=(
        16, 20), tol_s=10, closing_dist=3)
    for e in enemy:
        objects.append(Enemy(*e))

    ball = find_objects(obs, objects_colors["ball"], size=(
        2, 2), minx=32, maxx=127, miny=46, maxy=182, tol_s=1, min_distance=1)
    for b in ball:
        objects.append(Ball(*b))

    if hud:
        playerscore = find_objects(obs, objects_colors["playerscore"], size=(
            8, 7), minx=30, maxx=60, miny=11, maxy=22, tol_s=2)
        for p in playerscore:
            objects.append(PlayerScore(*p))

        enemyscore = find_objects(obs, objects_colors["enemyscore"], size=(
            8, 7), minx=100, maxx=120, miny=11, maxy=22, tol_s=2)
        for e in enemyscore:
            objects.append(EnemyScore(*e))

        timer = find_objects(obs, objects_colors["timer"], size=(
            8, 7), maxy=12, tol_s=4, closing_dist=1)
        for t in timer:
            objects.append(Timer(*t))
