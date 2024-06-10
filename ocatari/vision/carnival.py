from .utils import find_objects
from .game_objects import GameObject

objects_colors = {"background": [0, 0, 0], "player": [66, 158, 130], "score": [160, 171, 79],
                  "player_missile": [183, 194, 95], "bonus": [214, 92, 92]}

targets_colors = {"owl": [214, 92, 92], "rabbit": [192, 192, 192], "duck": [187, 187, 53],
                  "extra_bullets": [192, 192, 192]}

ammo_bar_colors = {"blue": [24, 59, 157], "green": [0, 68, 0], "purple": [125, 48, 173], "brown": [144, 72, 17],
                   "gray": [111, 111, 111], "dark_gray": [74, 74, 74], "yellow": [252, 224, 112],
                   "cyan": [117, 204, 235], "violett": [84, 92, 214], "bright_yellow": [232, 232, 74],
                   "peach": [252, 188, 116], "dark_purple": [104, 25, 154], "light_purple": [149, 111, 227],
                   "orange": [240, 170, 103], "dark_yellow": [187, 187, 53], "turquoise": [132, 252, 212],
                   "purple_2": [188, 144, 252], "orange_2": [198, 108, 58], "pink_2": [236, 140, 224],
                   "purple_3": [117, 128, 240], "white": [236, 236, 236], "light_blue": [132, 200, 252]}

wheel_colors = {"blue": [45, 87, 176], "green": [26, 102, 26], "purple": [125, 48, 173], "orange": [162, 98, 33]}


class Player(GameObject):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.rgb = 66, 158, 130


class PlayerMissile(GameObject):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.rgb = 183, 194, 95


class Owl(GameObject):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.rgb = 214, 92, 92


class Duck(GameObject):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.rgb = 187, 187, 53


class FlyingDuck(GameObject):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.rgb = 187, 187, 53


class Rabbit(GameObject):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.rgb = 192, 192, 192


class ExtraBullets(GameObject):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.rgb = 192, 192, 192


class PlayerScore(GameObject):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.rgb = 160, 171, 79


class AmmoBar(GameObject):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.rgb = 24, 59, 157


class BonusSign(GameObject):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.rgb = 214, 92, 92

class BonusValue(GameObject):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.rgb = 214, 92, 92


class Wheel(GameObject):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.rgb = 45, 87, 176


def _detect_objects(objects, obs, hud=False):
    objects.clear()

    player = find_objects(obs, objects_colors["player"], min_distance=1)
    for p in player:
        objects.append(Player(*p))

    player_missile = find_objects(obs, objects_colors["player_missile"], min_distance=1)
    for missile in player_missile:
        if missile[2] < 10 and missile[3] < 10:
            objects.append(PlayerMissile(*missile))

    duck = find_objects(obs, targets_colors["duck"], min_distance=1)
    for d in duck:
        if d[1] < 90:
            objects.append(Duck(*d))

    flying_duck = find_objects(obs, targets_colors["duck"], min_distance=1)
    for d in flying_duck:
        if d[1] >= 90:
            objects.append(FlyingDuck(*d))

    rabbit = find_objects(obs, targets_colors["rabbit"], min_distance=1)
    for rab in rabbit:
        if rab[3] > 10:
            objects.append(Rabbit(*rab))
        else:
            objects.append(ExtraBullets(*rab))

    owl = find_objects(obs, targets_colors["owl"], min_distance=1)
    for o in owl:
        if o[1] > 32:
            objects.append(Owl(*o))

    for wheel_color in wheel_colors.values():
        wheel = find_objects(obs, wheel_color, min_distance=1)
        for w in wheel:
            if w[2] > 5 and w[3] > 2:
                wheel_inst = Wheel(*w)
                wheel_inst.rgb = wheel_color
                objects.append(wheel_inst)

    if hud:
        for ammo_bar_color in ammo_bar_colors.values():
            ammo = find_objects(obs, ammo_bar_color, min_distance=1)
            for am in ammo:
                if am[1] >= 203:
                    ammo_inst = AmmoBar(*am)
                    ammo_inst.rgb = ammo_bar_color
                    objects.append(ammo_inst)

        score = find_objects(obs, objects_colors["score"], min_distance=1, closing_dist=5)
        for sc in score:
            objects.append(PlayerScore(*sc))

        bonus = find_objects(obs, objects_colors["bonus"], min_distance=1)
        for bon in bonus:
            if bon[1] <= 32:
                if bon[2] < 10:
                    objects.append(BonusSign(*bon))
                else:
                    objects.append(BonusValue(*bon))
