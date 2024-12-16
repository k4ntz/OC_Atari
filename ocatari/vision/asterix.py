from .utils import find_objects, find_mc_objects, match_objects
from .game_objects import GameObject

objects_colors = {'player': [187, 187, 53],
                  'enemy': [[228, 111, 111], [184, 50, 50]],
                  'score': [187, 187, 53],
                  'lives': [187, 187, 53],

                  # next color is inner one
                  # cauldron
                  'reward_50': [[198, 89, 179], [127, 92, 213], [170, 170, 170]],
                  # helmet
                  'reward_100': [[135, 183, 84], [213, 130, 74], [170, 170, 170]],
                  # shield
                  'reward_200': [[195, 144, 61], [84, 138, 210], [170, 170, 170]],
                  # lamp
                  'reward_300': [[213, 130, 74], [84, 92, 214], [170, 170, 170]],
                  # apple
                  'reward_400': [[135, 183, 84], [214, 92, 92], [170, 170, 170]],
                  # fish, meat and mug then cauldron...
                  'reward_500': [[163, 57, 21], [164, 89, 208], [170, 170, 170]],

                  'cauldron': [[167, 26, 26], [184, 50, 50]],
                  'helmet': [[240, 128, 128], [236, 236, 236], [214, 214, 214], [192, 192, 192], [170, 170, 170]],
                  'shield': [214, 214, 214],
                  'lamp': [[187, 53, 53], [184, 50, 50], [214, 214, 214]],
                  # red and green. 110, 156, 66 is for green
                  'apple': [[184, 50, 50], [110, 156, 66]],
                  'fish': [198, 89, 179],
                  # [214, 214, 214] for small white part
                  'meat': [[184, 50, 50], [214, 214, 214]],
                  'mug': [[184, 50, 50], [214, 214, 214]]
                  }


# the given color to the multicolor classes is the most outer one, so it fits with the surrounding rectangle
class Player(GameObject):  # player could be shown over all enemies/other objects (see Figure_4.png)
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.rgb = 187, 187, 53


class Cauldron(GameObject):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.rgb = 167, 26, 26  # , [184, 50, 50]]


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


class Helmet(GameObject):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.rgb = 240, 128, 128  # [[240, 128, 128], [236, 236, 236]]


class Shield(GameObject):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.rgb = 214, 214, 214


class Lamp(GameObject):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.rgb = 187, 53, 53


class Apple(GameObject):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.rgb = 184, 50, 50  # [[184, 50, 50], [110, 156, 66]]


class Fish(GameObject):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.rgb = 198, 89, 179


class Meat(GameObject):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.rgb = 184, 50, 50  # [[184, 50, 50], [214, 214, 214]]


class Mug(GameObject):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.rgb = 184, 50, 50  # [[184, 50, 50], [214, 214, 214]]


class Reward50(GameObject):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.rgb = 198, 89, 179


class Reward100(GameObject):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.rgb = 135, 183, 84


class Reward200(GameObject):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.rgb = 195, 144, 61


class Reward300(GameObject):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.rgb = 213, 130, 74


class Reward400(GameObject):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.rgb = 135, 183, 84


class Reward500(GameObject):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.rgb = 163, 57, 21

# MAX_NB_OBJECTS_HUD = {"Player" :  1, "Enemy": 8, "Reward" : 8, "Consumable" : 8, "Score" : 1, "Lives": 1}


def _detect_objects(objects, obs, hud=False):
    player = objects[0]
    player_bb = find_objects(
        obs, objects_colors["player"], maxy=160, tol_p=20, tol_s=(9, 1), size=(8, 11))
    if player_bb:
        player.xywh = player_bb[0]
    # for instance in player:  # parameters work for all 3 possible symbols ((wide) asterix and oblix (advanced))
    #     objects.append(Player(*instance))
    enemies_bb = find_mc_objects(
        obs, objects_colors["enemy"], closing_dist=2, miny=24, maxy=151, size=(7, 11), tol_s=1)
    match_objects(objects, enemies_bb, 1, 8, Enemy)

    reward50 = find_mc_objects(obs, objects_colors["reward_50"], min_distance=3, closing_dist=4, miny=24, maxy=151,
                               tol_s=3, size=(6, 11))
    match_objects(objects, reward50, 9, 8, Reward50)

    reward100 = find_mc_objects(obs, objects_colors["reward_100"], min_distance=3, closing_dist=3, miny=24, maxy=151,
                                size=(8, 11), tol_s=2)
    match_objects(objects, reward100, 9, 8, Reward100)
    reward200 = find_mc_objects(obs, objects_colors["reward_200"], min_distance=3, closing_dist=3, miny=24, maxy=151,
                                size=(8, 11), tol_s=3)
    match_objects(objects, reward200, 9, 8, Reward200)
    reward300 = find_mc_objects(obs, objects_colors["reward_300"], min_distance=3, closing_dist=3, miny=24, maxy=151,
                                size=(8, 11), tol_s=3)
    match_objects(objects, reward300, 9, 8, Reward300)
    reward400 = find_mc_objects(obs, objects_colors["reward_400"], min_distance=3, closing_dist=3, miny=24, maxy=151,
                                size=(8, 11), tol_s=3)
    match_objects(objects, reward400, 9, 8, Reward400)
    reward500 = find_mc_objects(obs, objects_colors["reward_500"], min_distance=3, closing_dist=3, miny=24, maxy=151,
                                size=(8, 11), tol_s=3)
    match_objects(objects, reward500, 9, 8, Reward500)

    cauldron = find_mc_objects(
        obs, objects_colors["cauldron"], closing_dist=2, size=(7, 10), tol_s=2)
    match_objects(objects, cauldron, 17, 8, Cauldron)
    helmet = find_mc_objects(obs, objects_colors["helmet"], closing_dist=1, min_distance=1, size=(7, 11),
                             tol_s=2, miny=24, maxy=151)
    match_objects(objects, helmet, 17, 8, Helmet)
    shield = find_objects(obs, objects_colors["shield"], closing_dist=1, size=(5, 11), tol_s=1, min_distance=2,
                          miny=24, maxy=151)
    match_objects(objects, shield, 17, 8, Shield)
    no_shield = len(shield) == 0

    lamp = find_mc_objects(obs, objects_colors["lamp"], closing_dist=4, size=(
        8, 11), tol_s=1, miny=24, maxy=151)
    match_objects(objects, lamp, 17, 8, Lamp)

    apple = find_mc_objects(obs, objects_colors["apple"], closing_dist=2, min_distance=2, size=(8, 11),
                            tol_s=1, miny=24, maxy=151, )
    match_objects(objects, apple, 17, 8, Apple)

    fish = find_objects(obs, objects_colors["fish"], closing_dist=1, min_distance=1,
                        size=(8, 5), tol_s=2, miny=24, maxy=151)
    match_objects(objects, fish, 17, 8, Fish)

    meat = find_mc_objects(obs, objects_colors["meat"], closing_dist=1, min_distance=1, size=(5, 11),
                           tol_s=2, miny=24, maxy=151)
    if no_shield:
        match_objects(objects, meat, 17, 8, Meat)

    mug = find_mc_objects(obs, objects_colors["mug"], closing_dist=2, min_distance=2, size=(7, 11),
                          tol_s=1, miny=24, maxy=151)
    match_objects(objects, mug, 17, 8, Mug)

    # if hud:
    #     lives = find_objects(obs, objects_colors["lives"], min_distance=1, miny=160, maxy=181)
    #     for instance in lives:
    #         objects.append(Lives(*instance))

    #     score = find_objects(obs, objects_colors["score"], closing_dist=4, miny=181)  # don't change closing_dist=4
    #     for instance in score:
    #         objects.append(Score(*instance))

    # remaining problems:
    # lamp and reward_300 are not being detected at all (try with masks?)
