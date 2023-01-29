from .utils import find_objects
from .game_objects import GameObject

objects_colors = {'player': [187, 187, 53],
                  'cauldron': [167, 26, 26],  # two colors: 167, 26, 26 / 184, 50, 50
                  # and 184, 50, 50 you could see in the enemy!
                  'enemy': [228, 111, 111],  # two colors: 184, 50, 50 (two red lines in middle) / 228, 111, 111
                  'score': [187, 187, 53],
                  'lives': [187, 187, 53],

                  # new not edited objects:
                  'bounty': [198, 89, 179],  # bounty or prize or bonus
                  # make min_distance for bounty bigger cause of more than one color in this and you are
                  # taking the borders, so you have all the object in the rectangle

                  }  # it still not all objects covered


class Player(GameObject):  # player could be shown over all enemies/other objects (see Figure_4.png)
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.rgb = 187, 187, 53


class Cauldron(GameObject):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.rgb = 184, 50, 50


class Enemy(GameObject):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.rgb = 228, 111, 111


class Score(GameObject):
    def __init__(self, x, y, w, h, num, *args, **kwargs):
        super().__init__(x, y, w, h, *args)
        self.rgb = 187, 187, 53  # same color as player


class Lives(GameObject):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.rgb = 187, 187, 53  # same color as player


# initialize new classes for new covered objects


# TODO
def _detect_objects_asterix(objects, obs, hud=False):
    objects.clear()

    player = find_objects(obs, objects_colors["player"], maxy=160)  # enemy has same color
    #  if___:  # we need some if?
    for instance in player:
        objects.append(Player(*instance))
    # objects.append(player)

    cauldron = find_objects(obs, objects_colors["cauldron"], closing_dist=6)
    objects.append(cauldron)

    enemy = find_objects(obs, objects_colors["enemy"], closing_dist=6)
    objects.append(enemy)

    score = find_objects(obs, objects_colors["score"], closing_distance=10,
                         miny=160, maxy=181)
    objects.append(score)

    lives = find_objects(obs, objects_colors["lives"],
                         miny=181)
    objects.append(lives)

    bounty = find_objects(obs, objects_colors["bounty"], closing_dist=10)
    objects.append(bounty)

    print(len(objects), "elements in objects:\n")
    print(*objects, sep="\n")
    print("\n\n")
