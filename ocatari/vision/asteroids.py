from .utils import find_objects
from .game_objects import GameObject

objects_colors = {"player": [240, 128, 128], "background": [0, 0, 0], "score": [184, 50, 50], "lives": [184, 50, 50]}

asteroids_colors = {"brown": [180, 122, 48], "purple": [104, 72, 198], "yellow": [136, 146, 62],
                    "lightyellow": [187, 187, 53], "grey": [214, 214, 214], "lightblue": [117, 181, 239],
                    "pink": [184, 70, 162], "red": [184, 50, 50]}

player_missile_colors = {"blue": [117, 181, 239], "red": [240, 128, 128]}


class Player(GameObject):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.rgb = 240, 128, 128


class PlayerScore(GameObject):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.rgb = 184, 50, 50


class Lives(GameObject):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.rgb = 184, 50, 50


class Asteroid(GameObject):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.rgb = 180, 122, 48


class PlayerMissile(GameObject):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.rgb = 117, 181, 239


def _detect_objects(objects, obs, hud=False):
    objects.clear()

    player = find_objects(obs, objects_colors["player"], min_distance=1)
    for p in player:
        if p[2] > 2 and p[3] > 4:
            objects.append(Player(*p))

    for asteroidColor in asteroids_colors.values():
        asteroid = find_objects(obs, asteroidColor, min_distance=1)
        for ast in asteroid:
            if ast[1] > 5 and ast[2] > 2 and ast[3] > 4:
                asteroid_inst = Asteroid(*ast)
                asteroid_inst.rgb = asteroidColor
                objects.append(asteroid_inst)

    for missile_color in player_missile_colors.values():
        missiles = find_objects(obs, missile_color, min_distance=1)
        for mis in missiles:
            if mis[2] <= 2 and mis[3] <= 3:
                missile_inst = PlayerMissile(*mis)
                missile_inst.rgb = missile_color
                objects.append(missile_inst)

    if hud:
        score = find_objects(obs, objects_colors["score"], closing_dist=6)
        for s in score:
            if s[0] < 132 and s[1] <= 5:
                objects.append(PlayerScore(*s))

        live = find_objects(obs, objects_colors["lives"], min_distance=1)
        for l1 in live:
            if l1[0] >= 132 and l1[1] <= 5:
                objects.append(Lives(*l1))
