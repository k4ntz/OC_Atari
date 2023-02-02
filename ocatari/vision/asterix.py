from .utils import find_objects, find_mc_objects
from .game_objects import GameObject

objects_colors = {'player': [187, 187, 53],
                  'enemy': [228, 111, 111],
                  'score': [187, 187, 53],
                  'lives': [187, 187, 53],

                  # next color is inner one. [170, 170, 170] is in all rewards
                  'reward1': [[198, 89, 179], [127, 92, 213]],  # value 50  cauldron
                  'reward2': [[135, 183, 84], [213, 130, 74]],  # value 100 helmet. same as reward5 :(
                  'reward3': [[195, 144, 61], [84, 138, 210]],  # value 200 shield
                  'reward4': [[213, 130, 74], [84, 92, 214]],  # value 300 lamp
                  'reward5': [[135, 183, 84], [214, 92, 92]],  # value 400 apple
                  'reward6': [[163, 57, 21], [164, 89, 208]],  # value 500 fish, meat and mug

                  # next objects are which meant with reward
                  'cauldron': [[167, 26, 26], [184, 50, 50]],
                  'helmet': [[240, 128, 128], [236, 236, 236]],  # got after 13600 frames
                  'shield': [214, 214, 214],
                  'lamp': [[187, 53, 53], [214, 214, 214]],
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
# cause they are not important for the agent
class Reward(GameObject):
    def __init__(self, num, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.rgb = (
            [[198, 89, 179], [127, 92, 213]],
            [[135, 183, 84], [213, 130, 74]],
            [[195, 144, 61], [84, 138, 210]],
            [[213, 130, 74], [84, 92, 214]],
            [[135, 183, 84], [214, 92, 92]],
            [[163, 57, 21], [164, 89, 208]]
        )[num - 1]
        # self.value = num  # what is this for, quentin?


class Cauldron(GameObject):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.rgb = [[167, 26, 26], [184, 50, 50]]


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
        self.rgb = [[240, 128, 128], [236, 236, 236]]


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
        self.rgb = [[184, 50, 50], [110, 156, 66]]


class Fish(GameObject):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.rgb = [198, 89, 179]


class Meat(GameObject):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.rgb = [[184, 50, 50], [214, 214, 214]]


class Mug(GameObject):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.rgb = [[184, 50, 50], [214, 214, 214]]


# TODO
def _detect_objects_asterix(objects, obs, hud=False):
    objects.clear()

    player = find_objects(obs, objects_colors["player"], maxy=160)
    for instance in player:
        objects.append(Player(*instance))

    cauldron = find_mc_objects(obs, objects_colors["cauldron"], size=(10, 10), closing_dist=6)
    for instance in cauldron:
        objects.append(Cauldron(*instance))

    enemy = find_objects(obs, objects_colors["enemy"], closing_dist=6)
    for instance in enemy:
        objects.append(Enemy(*instance))

    ctr = 1
    for x in ["reward1", "reward2", "reward3", "reward4", "reward5", "reward6"]:
        reward = find_mc_objects(obs, objects_colors[x], min_distance=1, size=(10, 10), closing_dist=8)
        for instance in reward:
            objects.append(Reward(ctr, *instance))
            ctr += 1

    helmet = find_mc_objects(obs, objects_colors["helmet"], closing_dist=6)
    for instance in helmet:
        objects.append(Helmet(*instance))

    shield = find_objects(obs, objects_colors["shield"], closing_dist=0, size=(5, 11), min_distance=0)  # teste pars
    for instance in shield:
        objects.append(Shield(*instance))

    lamp = find_mc_objects(obs, objects_colors["lamp"], closing_dist=3)
    for instance in lamp:
        objects.append(Lamp(*instance))

    # 'apple':     'fish': 'meat':  'mug':
    
    if hud:
        score = find_objects(obs, objects_colors["score"], closing_dist=3, miny=160, maxy=181)  # cl_di was 1 before
        for instance in score:
            objects.append(Score(*instance))

        lives = find_objects(obs, objects_colors["lives"], min_distance=1, miny=181)
        for instance in lives:
            objects.append(Lives(*instance))

    # print("\nobjects:")
    # print(*objects, sep="\n")
    # print("\n")
