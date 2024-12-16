from .utils import find_objects, find_mc_objects
from .game_objects import GameObject

objects_colors = {
    "Player": [236, 236, 236],
    "DivingEnemy": [[135, 183, 84], [181, 108, 224]],
    "PlayerMissile": [210, 164, 74],
    "EnemyMissile": [228, 111, 111],
    "EnemyShip": [[[110, 156, 66], [232, 204, 99], [192, 192, 192]],
                  [[84, 92, 214], [232, 204, 99], [184, 70, 162]],
                  [[184, 50, 50], [232, 204, 99], [213, 130, 74]],
                  [[236, 236, 236], [232, 204, 99]]
                  ],
    "Score": [232, 204, 99],
    "Lives": [214, 214, 214],
    "Round": [214, 214, 214]
}


class Player(GameObject):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.rgb = 236, 236, 236


class DivingEnemy(GameObject):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.rgb = 135, 183, 84


class PlayerMissile(GameObject):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.rgb = 210, 164, 74


class EnemyMissile(GameObject):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.rgb = 228, 111, 111


class EnemyShip(GameObject):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.rgb = 232, 204, 99


class Score(GameObject):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.rgb = 232, 204, 99


class Lives(GameObject):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.rgb = 214, 214, 214


class Round(GameObject):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.rgb = 214, 214, 214


def _detect_objects(objects, obs, hud=True):
    objects.clear()
    player = find_objects(
        obs, objects_colors["Player"], miny=166, maxy=185, minx=15, maxx=142)
    for play in player:
        objects.append(Player(*play))
    for color in objects_colors["DivingEnemy"]:
        diving_enemies = find_objects(
            obs, color, miny=16, minx=15, maxx=142, maxy=185)
        for sent in diving_enemies:
            objects.append(DivingEnemy(*sent))
        player_missiles = find_objects(obs, objects_colors["PlayerMissile"], size=(
            1, 3), tol_s=2, miny=16, minx=15, maxx=142, maxy=170)
    for missile in player_missiles:
        objects.append(PlayerMissile(*missile))
    enemy_missiles = find_objects(obs, objects_colors["EnemyMissile"], size=(
        1, 4), tol_s=2, miny=16, minx=15, maxx=142, maxy=170)
    for missile in enemy_missiles:
        objects.append(EnemyMissile(*missile))
    for color in objects_colors["EnemyShip"]:
        enemy_ships = find_mc_objects(
            obs, color, closing_dist=2, miny=16, minx=15, maxx=142, maxy=90)
        for enemy in enemy_ships:
            objects.append(EnemyShip(*enemy))
    if hud:
        scores = find_objects(
            obs, objects_colors["Score"], maxy=16, closing_dist=5)
        for score in scores:
            objects.append(Score(*score))
        lives = find_objects(
            obs, objects_colors["Lives"], maxy=195, miny=186, maxx=35)
        for live in lives:
            objects.append(Lives(*live))
        rounds = find_objects(
            obs, objects_colors["Round"], maxy=195, miny=186, minx=110)
        for round in rounds:
            objects.append(Round(*round))
