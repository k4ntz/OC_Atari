from .utils import find_objects
from .game_objects import GameObject

objects_colors = {"player": [210, 164, 74], "life": [187, 187, 53], "score": [195, 144, 61],
                  "ghosts": {"orange": [180, 122, 48], "cyan": [84, 184, 153],
                             "pink": [198, 89, 179], "red": [200, 72, 72], "eatable": [66, 114, 194]},
                  "fruit": {"cherry/strawberry/Apple": [184, 50, 50], "pretzel": [162, 162, 42],
                            "orange/banana": [198, 108, 58], "pear": [110, 156, 66]},
                  }


class Player(GameObject):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.rgb = 210, 164, 74


class Ghost(GameObject):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.rgb = 180, 122, 48


class Fruit(GameObject):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.rgb = 184, 50, 50


class Score(GameObject):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.rgb = 195, 144, 61


class Life(GameObject):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.rgb = 187, 187, 53


def _detect_objects(objects, obs, hud=True):
    objects.clear()

    player = find_objects(obs, objects_colors["player"], min_distance=1)
    for bb in player:
        objects.append(Player(*bb))

    for i in objects_colors["ghosts"]:
        ghosts = find_objects(obs, objects_colors["ghosts"][i], min_distance=1)

        for bb in ghosts:
            ghs = Ghost(*bb)
            ghs.rgb = objects_colors["ghosts"][i]
            objects.append(ghs)
    if hud:
        for i in objects_colors["fruit"]:
            fruit = find_objects(obs, objects_colors["fruit"][i], min_distance=1)

            for bb in fruit:
                fru = Fruit(*bb)
                fru.rgb = objects_colors["fruit"][i]
                objects.append(fru)

        score = find_objects(obs, objects_colors["score"], closing_dist=5, min_distance=1)
        for s in score:
            objects.append(Score(*s))

        life = find_objects(obs, objects_colors["life"], min_distance=1)
        for l1 in life:
            objects.append(Life(*l1))
    else:
        for i in objects_colors["fruit"]:
            fruit = find_objects(obs, objects_colors["fruit"][i], min_distance=1)

            for bb in fruit:
                if bb[1] < 170:
                    fru = Fruit(*bb)
                    fru.rgb = objects_colors["fruit"][i]
                    objects.append(fru)
