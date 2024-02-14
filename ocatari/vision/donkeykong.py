from .utils import find_objects
from .game_objects import GameObject

objects_colors = {"player": [252, 224, 144], "life": [72, 176, 110], "score": [195, 144, 61],
                  "ghosts": {"pink": [252, 144, 200], "eatable": [66, 114, 194]},
                  "cherry": [252, 144, 200]
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
        self.rgb = 252, 144, 200


class Score(GameObject):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.rgb = 195, 144, 61


class Life(GameObject):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.rgb = 187, 187, 53


def _detect_objects_donkeykong(objects, obs, hud=True):
    objects.clear()
    # player = find_objects(obs, objects_colors["player"], min_distance=1)
    # for bb in player:
    #     objects.append(Player(*bb))

    # for i in objects_colors["ghosts"]:
    #     ghosts = find_objects(obs, objects_colors["ghosts"][i], min_distance=1)
    #     for bb in ghosts:
    #         if i == 0 and bb[2] < 5: # cherry
    #             fru = Fruit(*bb)
    #             fru.rgb = objects_colors["cherry"]
    #             objects.append(fru)
    #         else:
    #             ghs = Ghost(*bb)
    #             ghs.rgb = objects_colors["ghosts"][i]
    #             objects.append(ghs)
    # if hud:
    #     score = find_objects(obs, objects_colors["score"], closing_dist=5, min_distance=1)
    #     for s in score:
    #         objects.append(Score(*s))

        # life = find_objects(obs, objects_colors["life"], min_distance=1, miny=216, maxy=224)
        # for l1 in life:
        #     objects.append(Life(*l1))
    # else:
    #     for i in objects_colors["fruit"]:
    #         fruit = find_objects(obs, objects_colors["fruit"][i], min_distance=1)

            # for bb in fruit:
            #     if bb[1] < 170:
            #         fru = Fruit(*bb)
            #         fru.rgb = objects_colors["fruit"][i]
            #         objects.append(fru)
