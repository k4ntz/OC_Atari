from .utils import find_objects, find_mc_objects
from .game_objects import GameObject

objects_colors = {'player': [187, 187, 53],
                  'enemy': [228, 111, 111],
                  'score': [187, 187, 53],
                  'lives': [187, 187, 53],

                  # (bounty/prize/bonus). and all bounties have same size
                  # next color is inner one. [170, 170, 170] is in all bounties
                  # rename bounty to x_reward?
                  'bounty1': [[198, 89, 179], [127, 92, 213]],  # value 50  cauldron
                  'bounty2': [[135, 183, 84], [213, 130, 74]],  # value 100 helmet. same as bounty5 :(
                  'bounty3': [[195, 144, 61], [84, 138, 210]],  # value 200 shield
                  'bounty4': [[213, 130, 74], [84, 92, 214]],  # value 300 lamp
                  'bounty5': [[135, 183, 84], [214, 92, 92]],  # value 400 apple
                  'bounty6': [[163, 57, 21], [164, 89, 208]],  # value 500 fish, meat and mug

                  # next objects are which meant with reward
                  'cauldron': [[167, 26, 26], [184, 50, 50]],
                  'helmet': [240, 128, 128],  # first line color 236, 236, 236 after 13600 frames
                  'shield': [214, 214, 214],
                  'lamp': [187, 53, 53],
                  'apple': [[184, 50, 50], [110, 156, 66]],  # red and green. 110, 156, 66 is for green
                  'fish': [198, 89, 179],
                  'meat': [[184, 50, 50], [214, 214, 214]],  # 214, 214, 214 for small white part
                  'mug': [[184, 50, 50], [214, 214, 214]]  # like meat. how to differ?

                  # multicolor objects. should we give all contained colores or just what makes obj unique
                  # '50_reward': [[170, 170, 170], [127, 92, 213], [198, 89, 179]]
                  }


class Player(GameObject):  # player could be shown over all enemies/other objects (see Figure_4.png)
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.rgb = 187, 187, 53


# is it better to implement this class for all possible rewards than to have a class for every reward?
# one of the advantages is that the one object turns into another at once
class Reward(GameObject):
    def __init__(self, num, *args, **kwargs):
        super(self).__init__(*args, **kwargs)
        self.rgb = ([167, 26, 26],
                    [240, 128, 128],
                    [214, 214, 214],
                    [187, 53, 53],
                    [184, 50, 50],
                    [198, 89, 179],
                    [184, 50, 50],
                    [184, 50, 50])[num - 1]


class Cauldron(GameObject):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.rgb = 184, 50, 50


class Enemy(GameObject):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.rgb = 228, 111, 111


class Score(GameObject):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.rgb = 187, 187, 53


class Lives(GameObject):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.rgb = 187, 187, 53


class Bounty(GameObject):
    def __init__(self, num, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.rgb = 198, 89, 179
        # self.rgb = ((187, 187, 53),
        #             (135, 183, 84),
        #             (195, 144, 61),
        #             )[num - 1]


class Reward(GameObject):
    def __init__(self, num, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.rgb = 170, 170, 170
        self.value = num


class Helmet(GameObject):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.rgb = 240, 128, 128


class Shield(GameObject):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.rgb = 214, 214, 214


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
    for instance in cauldron:
        objects.append(Cauldron(*instance))

    enemy = find_objects(obs, objects_colors["enemy"], closing_dist=6)
    for instance in enemy:
        objects.append(Enemy(*instance))

    rewards = find_mc_objects(obs, objects_colors["50_reward"], size=(10, 10),
                              closing_dist=6)
    for instance in rewards:
        objects.append(Reward(50, *instance))

    if hud:
        score = find_objects(obs, objects_colors["score"], closing_dist=1, miny=160, maxy=181)  # min_distance=10) !!
        for instance in score:
            objects.append(Score(*instance))

        lives = find_objects(obs, objects_colors["lives"], min_distance=1, miny=181)
        for instance in lives:
            objects.append(Lives(*instance))

    # bounty = find_objects(obs, objects_colors["bounty"], closing_dist=10)
    # for instance in bounty:
    #     objects.append(Bounty(*instance))

    # print("\nobjects:")
    # print(*objects, sep="\n")
    # print("\n")
