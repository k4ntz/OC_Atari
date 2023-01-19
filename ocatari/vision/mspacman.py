from .utils import find_objects
from .game_objects import GameObject


objects_colors = {"player": [210, 164, 74], "life": [187, 187, 53], "score": [195, 144, 61],
                  "ghosts":{"orange": [180, 122, 48], "cyan": [84, 184, 153],
                  "pink": [198, 89, 179], "red": [200, 72, 72], "eatable": [66, 114, 194]},
                  "fruit":{"cherry/strawberry/Apple": [184, 50, 50], "pretzel": [162, 162, 42],
                  "orange/banana": [198, 108, 58], "pear": [110, 156, 66]},
                  }


class Player(GameObject):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.rgb = 210, 164, 74


class Ghost(GameObject):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if GameObject == "orange":
            self.rgb = 180, 122, 48
        elif GameObject == "cyan":
            self.rgb = 84, 184, 153
        elif GameObject == "pink":
            self.rgb = 198, 89, 179
        elif GameObject == "red":
            self.rgb = 200, 72, 72


class Fruit(GameObject):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if GameObject == "cherry/strawberry/Apple":
            self.rgb = 184, 50, 50
        elif GameObject == "pretzel":
            self.rgb = 162, 162, 42
        elif GameObject == "orange/banana":
            self.rgb = 198, 108, 58
        elif GameObject == "pear":
            self.rgb = 110, 156, 66


class Score(GameObject):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.rgb = 195, 144, 61


class Life(GameObject):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.rgb = 187, 187, 53


def _detect_objects_mspacman(objects, obs, hud=False):
    objects.clear()

    player = find_objects(obs, objects_colors["player"], min_distance=1)
    if len(player) >= 1:
        for p in player:
            objects.append(Player(*player))

    for i in objects_colors["ghosts"]:
        ghosts = find_objects(obs, objects_colors["ghosts"][i], min_distance=1)
        # index = 0
        objects.append(Ghost(ghosts))

    for i in objects_colors["fruit"]:
        fruit = find_objects(obs, objects_colors["fruit"][i], min_distance=1)
        for f in fruit:
            objects.append(Fruit(f))

    if hud:
        score = find_objects(obs, objects_colors["score"], min_distance=1)
        for s in score:
            objects.append(Score(*s))

        life = find_objects(obs, objects_colors["live"], min_distance=1)
        for l1 in life:
            objects.append(Live(*l1))
