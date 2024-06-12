from .game_objects import GameObject
from .utils import find_objects

objects_colors = {"player": [], "bridge edge": [168, 72, 158], "black bat": [0, 0, 0], "magnet": [0, 0, 0],
                  "yellow dragon": [223, 192, 111], "green dragon": [], "red dragon": [],
                  "dragon sword": [223, 192, 111], "yellow key": [], "black key": [0, 0, 0], "gate": [0, 0, 0],
                  "chalice": [],
                  "black": [0, 0, 0], "yellow": [223, 192, 111], "red": [182, 72, 110], "green": [92, 197, 135]}


class Player(GameObject):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.rgb = [252, 252, 84]
        self.wh = 5, 8


# Each dragon has a different purpose that's why I thought it might be more relevant to have a class for each dragon
class YellowDragon(GameObject):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.rgb = [223, 192, 111]
        self.alive = True


class GreenDragon(GameObject):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.rgb = [223, 192, 111]
        self.alive = True


class RedDragon(GameObject):
    def __init__(self, *args, **kwargs):
        self.rgb = [223, 192, 111]
        self.alive = True


class BlackBat(GameObject):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.rgb = [0, 0, 0]


class DragonSword(GameObject):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.rgb = [223, 192, 111]


class Key(GameObject):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.rgb = [0, 0, 0]


class Magnet(GameObject):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.rgb = [0, 0, 0]


class BridgeEdge(GameObject):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.rgb = [168, 72, 158]


class Gate(GameObject):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.rgb = [0, 0, 0]


class Chalice(GameObject):
    def __init__(self, *args: object, **kwargs: object) -> object:
        super().__init__(*args, **kwargs)
        self.rgb = [168, 72, 158]


def _detect_objects(objects, obs, hud=False):
    GAMEZONE_Y_MIN = 27
    GAMEZONE_Y_MAX = 225
    player_previous_position = 0, 0
    if len(objects) > 0:
        player_previous_position = objects[0].xy
    objects.clear()
    for possible_player in find_objects(obs, obs[31, 3], miny=27, maxy=225, closing_dist=1):
        if 3 < possible_player[2] < 6 and 7 < possible_player[3] < 9:
            objects.append(Player(*possible_player))
    # if len(objects) == 0: objects.append(Player(player_previous_position[0], player_previous_position[1], 5 ,8))

    for yellow_object in find_objects(obs, objects_colors["yellow"], miny=GAMEZONE_Y_MIN, maxy=GAMEZONE_Y_MAX):
        if 6 < yellow_object[2] < 9 and 33 < yellow_object[3] < 41:
            dragon_instance = GreenDragon(*yellow_object)
            if dragon_instance.h > 35:
                dragon_instance.alive = True
            else:
                dragon_instance.alive = False
            objects.append(dragon_instance)
        elif 7 < yellow_object[2] < 9 and 5 < yellow_object[3] < 7:
            key_instance = Key(*yellow_object)
            key_instance.rgb = objects_colors["yellow"]
            objects.append(key_instance)
        elif 6 < yellow_object[2] < 9 and 9 < yellow_object[3] < 11:
            objects.append(DragonSword(*yellow_object))
        elif 7 < yellow_object[2] < 9 and 15 < yellow_object[3] < 20:
            objects.append(Chalice(*yellow_object))

    for green_object in find_objects(obs, objects_colors["green"], miny=GAMEZONE_Y_MIN, maxy=GAMEZONE_Y_MAX):
        if 6 < green_object[2] < 9 and 33 < green_object[3] < 41:
            dragon_instance = GreenDragon(*green_object)
            if dragon_instance.h > 35:
                dragon_instance.alive = True
            else:
                dragon_instance.alive = False
            objects.append(dragon_instance)
        elif 7 < green_object[2] < 9 and 15 < green_object[3] < 20:
            objects.append(Chalice(*green_object))

    for red_object in find_objects(obs, objects_colors["red"], miny=GAMEZONE_Y_MIN, maxy=GAMEZONE_Y_MAX):
        if 6 < red_object[2] < 9 and 33 < red_object[3] < 41:
            dragon_instance = GreenDragon(*red_object)
            if dragon_instance.h > 35:
                dragon_instance.alive = True
            else:
                dragon_instance.alive = False
            objects.append(dragon_instance)
        elif 7 < red_object[2] < 9 and 15 < red_object[3] < 20:
            objects.append(Chalice(*red_object))

    for black_object in find_objects(obs, objects_colors["black"], miny=GAMEZONE_Y_MIN, maxy=GAMEZONE_Y_MAX):
        if 7 < black_object[2] < 9 and 5 < black_object[3] < 7:
            key_instance = Key(*black_object)
            key_instance.rgb = objects_colors["black"]
            objects.append(key_instance)
        elif 7 < black_object[2] < 9 and 15 < black_object[3] < 16:
            objects.append(Magnet(*black_object))
        elif 6 < black_object[2] < 9 and 31 < black_object[3] < 33:
            objects.append(Gate(*black_object))
        elif 7 < black_object[2] < 9 and 15 < black_object[3] < 20:
            objects.append(Chalice(*black_object))

    for pink_object in find_objects(obs, objects_colors["bridge edge"], miny=GAMEZONE_Y_MIN, maxy=GAMEZONE_Y_MAX):
        if 7 < pink_object[2] < 9 and 15 < pink_object[3] < 20:
            objects.append(Chalice(*pink_object))
        elif 7 < pink_object[2] < 11 and 47 < pink_object[3] < 50:
            objects.append(BridgeEdge(*pink_object))
