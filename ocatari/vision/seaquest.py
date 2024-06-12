from .utils import find_objects
from .game_objects import GameObject

objects_colors = {"player": [[187, 187, 53], [236, 236, 236]], "diver": [66, 72, 200], "background_water": [0, 28, 136],
                  "player_score": [210, 210, 64], "oxygen_bar": [214, 214, 214], "lives": [210, 210, 64],
                  "logo": [66, 72, 200], "player_missile": [187, 187, 53], "oxygen_bar_depleted": [163, 57, 21],
                  "oxygen_logo": [0, 0, 0], "collected_diver": [24, 26, 167], "enemy_missile": [66, 72, 200],
                  "submarine": [170, 170, 170]}

enemy_colors = {"green": [92, 186, 92], "orange": [198, 108, 58], "yellow": [160, 171, 79], "lightgreen": [72, 160, 72],
                "pink": [198, 89, 179]}


class Player(GameObject):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.rgb = 187, 187, 53


class Diver(GameObject):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.rgb = 66, 72, 200


class Enemy(GameObject):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.rgb = 92, 186, 92


class EnemySubmarine(GameObject):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.rgb = 170, 170, 170


class PlayerMissile(GameObject):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.rgb = 187, 187, 53


class OxygenBar(GameObject):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.rgb = 214, 214, 214


class OxygenBarDepleted(GameObject):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.rgb = 163, 57, 21


class OxygenBarLogo(GameObject):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.rgb = 0, 0, 0


class PlayerScore(GameObject):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.rgb = 210, 210, 64


class Lives(GameObject):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.rgb = 210, 210, 64


class CollectedDiver(GameObject):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.rgb = 24, 26, 167


class EnemyMissile(GameObject):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.rgb = 66, 72, 200


def _detect_objects(objects, obs, hud=False):
    objects.clear()

    for color in objects_colors["player"]:
        player = find_objects(obs, color, closing_dist=8)
        for p in player:
            if p[1] > 30 and p[3] > 6:
                objects.append(Player(*p))

            if p[1] > 30 and p[3] == 1 and p[2] == 8:
                objects.append(PlayerMissile(*p))

    divers = find_objects(obs, objects_colors["diver"], closing_dist=4)
    for d in divers:
        if d[1] < 190 and d[2] > 2 and d[3] < 5:
            objects.append(EnemyMissile(*d))
        elif d[1] < 190 and d[2] > 2:
            objects.append(Diver(*d))

    for enemyColor in enemy_colors.values():
        enemy = find_objects(obs, enemyColor, min_distance=1)
        for en in enemy:
            enemy_inst = Enemy(*en)
            enemy_inst.rgb = enemyColor
            objects.append(enemy_inst)

    submarine = find_objects(obs, objects_colors["submarine"], min_distance=1)
    for sub in submarine:
        objects.append(EnemySubmarine(*sub))

    if hud:
        score = find_objects(obs, objects_colors["player_score"], maxy=17, min_distance=1, closing_dist=5)
        for s in score:
            objects.append(PlayerScore(*s))

        lives = find_objects(obs, objects_colors["player_score"], miny=22, maxy=30, min_distance=1, closing_dist=5)
        for s in lives:
                objects.append(Lives(*s))

        oxygen_bar = find_objects(obs, objects_colors["oxygen_bar"], min_distance=1)
        for ox in oxygen_bar:
            objects.append(OxygenBar(*ox))

        oxygen_bar_depl = find_objects(obs, objects_colors["oxygen_bar_depleted"], min_distance=1)
        for ox_depl in oxygen_bar_depl:
            objects.append(OxygenBarDepleted(*ox_depl))

        oxygen_logo = find_objects(obs, objects_colors["oxygen_logo"], min_distance=1)
        for ox_logo in oxygen_logo:
            if ox_logo[0] > 0:
                objects.append(OxygenBarLogo(*ox_logo))

        coll_diver = find_objects(obs, objects_colors["collected_diver"], min_distance=10)
        for div in coll_diver:
            objects.append(CollectedDiver(*div))
