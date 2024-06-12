from .utils import find_objects, find_mc_objects
from .game_objects import GameObject


objects_colors = {"player": [[162, 162, 42], [214, 214, 214], [66, 72, 200]], "background": [0, 0, 0],
                  "enemy": [[180, 122, 48], [181, 83, 40], [167, 26, 26]],
                  "mother_ship": [[180, 122, 48], [187, 187, 53], [110, 156, 66], [72, 160, 72]],
                  "score": [195, 144, 61], "lives": [170, 170, 170]}

enemy_missile_colors = {"blue": [84, 138, 210], "yellow": [187, 187, 53], "green": [92, 186, 92], "red": [214, 92, 92]}
player_missile_colors = {"horizontal": [214, 214, 214], "vertical": [236, 236, 236]}
mother_ship_colors = {"1": [[180, 122, 48], [187, 187, 53], [110, 156, 66], [72, 160, 72]],
                      "2": [[66, 114, 194], [45, 87, 176], [24, 59, 157], [24, 59, 157], [151, 25, 122],
                            [184, 70, 162], [26, 102, 26], [50, 132, 50], [72, 160, 72]]}
enemy_ship_colors = {"red": [[180, 122, 48], [181, 83, 40], [167, 26, 26]],
                     "green": [[72, 160, 72], [110, 156, 66], [24, 59, 157], [187, 187, 53], [180, 122, 48]],
                     "blue": [[214, 92, 92], [200, 72, 72], [162, 162, 42], [134, 134, 29],
                              [45, 87, 176], [66, 114, 194], [84, 138, 210]],
                     "yellow": [[162, 162, 42], [134, 134, 29], [105, 105, 15], [105, 77, 20], [134, 106, 38],
                                [162, 134, 56]]}
health_colors = {"green": [72, 160, 72], "red": [200, 72, 72]}


class Player(GameObject):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.rgb = 214, 214, 214


class PlayerMissileHorizontal(GameObject):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.rgb = 214, 214, 214


class PlayerMissileVertical(GameObject):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.rgb = 236, 236, 236


class MotherShip(GameObject):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.rgb = 72, 160, 72


class Enemy(GameObject):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.rgb = 167, 26, 26


class EnemyMissile(GameObject):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.rgb = 210, 210, 64


class PlayerScore(GameObject):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.rgb = 195, 144, 61


class Lives(GameObject):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.rgb = 170, 170, 170


class Health(GameObject):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.rgb = 72, 160, 72


def _detect_objects(objects, obs, hud=False):
    objects.clear()
    player = find_mc_objects(obs, objects_colors["player"], min_distance=1)
    for p in player:
        if p[1] > 170 and p[2] > 4:
            objects.append(Player(*p))

    for player_missile_color in player_missile_colors.values():
        player_missile = find_objects(obs, player_missile_color, min_distance=1)
        for mis in player_missile:
            if mis[2] < 8:
                if [214, 214, 214] == player_missile_color:
                    objects.append(PlayerMissileHorizontal(*mis))
                else:
                    objects.append(PlayerMissileVertical(*mis))

    for enemy_ship_color in enemy_ship_colors.values():
        enemy = find_mc_objects(obs, enemy_ship_color, min_distance=1)
        for en in enemy:
            if 30 < en[1] < 180 and en[3] > 3 and en[2] > 1:
                enemy_inst = Enemy(*en)
                if [167, 26, 26] in enemy_ship_color:
                    enemy_inst.rgb = 167, 26, 26
                elif [72, 160, 72] in enemy_ship_color:
                    enemy_inst.rgb = 72, 160, 72
                elif [84, 138, 210] in enemy_ship_color:
                    enemy_inst.rgb = 84, 138, 210
                elif [105, 77, 20] in enemy_ship_color:
                    enemy_inst.rgb = 105, 77, 20
                objects.append(enemy_inst)

    for enemy_missile_color in enemy_missile_colors.values():
        missile = find_objects(obs, enemy_missile_color, min_distance=1)
        for mis in missile:
            if [92, 186, 92] == enemy_missile_color:
                missile_inst = EnemyMissile(*mis)
                missile_inst.rgb = enemy_missile_color
                objects.append(missile_inst)
            if [214, 92, 92] == enemy_missile_color and mis[3] > 2:
                missile_inst = EnemyMissile(*mis)
                missile_inst.rgb = enemy_missile_color
                objects.append(missile_inst)
            if mis[1] > 30 and mis[2] == 1 and mis[3] > 1:
                missile_inst = EnemyMissile(*mis)
                missile_inst.rgb = enemy_missile_color
                objects.append(missile_inst)

    for mother_ship_color in mother_ship_colors.values():
        mother_ship = find_mc_objects(obs, mother_ship_color, min_distance=1)
        for mother in mother_ship:
            if mother[1] < 20 and mother[2] > 30:
                mother_ship_inst = MotherShip(*mother)
                if [110, 156, 66] in mother_ship_color:
                    mother_ship_inst.rgb = 72, 160, 72
                else:
                    mother_ship_inst.rgb = 184, 70, 162

                objects.append(mother_ship_inst)

    if hud:
        score = find_objects(obs, objects_colors["score"], min_distance=1, closing_dist=1)
        for sc in score:
            objects.append(PlayerScore(*sc))

        lives = find_objects(obs, objects_colors["lives"], min_distance=1)
        for liv in lives:
            objects.append(Lives(*liv))

        for health_color in health_colors.values():
            health = find_objects(obs, health_color, min_distance=1)
            for h in health:
                if h[1] > 180:
                    health_inst = Health(*h)
                    health_inst.rgb = health_color
                    objects.append(health_inst)
