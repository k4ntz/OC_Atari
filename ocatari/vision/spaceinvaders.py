from .utils import find_objects
from .game_objects import GameObject

objects_colors = {"player": [50, 132, 50], "score": [50, 132, 50],
                  "player2": [162, 134, 56], "score2": [162, 134, 56],
                  "alien": [134, 134, 29], "shield": [181, 83, 40],
                  "satellite": [151, 25, 122], "bullet": [142, 142, 142],
                  "lives": [162, 134, 56]
                  }


class Player(GameObject):
    def __init__(self, x, y, w, h, num, *args):
        super().__init__(x, y, w, h, *args)
        if num == 1:
            self.rgb = 92, 186, 92
        else:
            self.rgb = 162, 134, 56  # yellow
        self.player_num = num


class Alien(GameObject):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.rgb = 134, 134, 29


class Satellite(GameObject):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.rgb = 151, 25, 122


class Shield(GameObject):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.rgb = 181, 83, 40


class Bullet(GameObject):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.rgb = 142, 142, 142


class Score(GameObject):
    def __init__(self, x, y, w, h, num, *args):
        super().__init__(x, y, w, h, *args)
        if num == 1:
            self.rgb = 92, 186, 92
        else:
            self.rgb = 162, 134, 56


class Lives(GameObject):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.rgb = 162, 134, 56


def _detect_objects(objects, obs, hud):
    objects.clear()

    for i, obj in enumerate(["player", "player2"]):
        players = find_objects(obs, objects_colors[obj], closing_active=False,
                               miny=180, maxy=195)
        for instance in players:
            if instance[2] < 10:  # width
                objects.append(Player(*instance, i + 1))
            elif hud and instance[2] > 10:
                objects.append(Lives(*instance))

    if hud:
        for i, obj in enumerate(["score", "score2"]):
            scores = find_objects(obs, objects_colors[obj], closing_dist=12, maxy=30)
            for instance in scores:
                objects.append(Score(*instance, i + 1))

    aliens = find_objects(obs, objects_colors["alien"])
    for instance in aliens:
        objects.append(Alien(*instance))

    shields = find_objects(obs, objects_colors["shield"], closing_dist=17, min_distance=20)
    for instance in shields:
        objects.append(Shield(*instance))

    satellites = find_objects(obs, objects_colors["satellite"])
    for instance in satellites:
        objects.append(Satellite(*instance))

    bullets = find_objects(obs, objects_colors["bullet"])
    for instance in bullets:
        objects.append(Bullet(*instance))
