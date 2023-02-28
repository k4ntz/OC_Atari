from .utils import find_objects
from .game_objects import GameObject

trees_c = [[158, 208, 101], [82, 126, 45], [110, 156, 66], [72, 160, 72]]
moguls_c = [[192, 192, 192], [214, 214, 214]]
flag_c = [[66, 72, 200], [184, 50, 50]]
player_c = [214, 92, 92]
logo_c = [0, 0, 0]


class Player(GameObject):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.rgb = 214, 92, 92
        self.hud = False


class Flag(GameObject):
    def __init__(self, x, y, w, h, rgb):
        super().__init__(x, y, w, h)
        self.rgb = rgb
        self.hud = False


class Tree(GameObject):
    def __init__(self, x, y, w, h, rgb):
        super().__init__(x, y, w, h)
        self.rgb = rgb
        self.hud = False


class Mogul(GameObject):
    def __init__(self, x, y, w, h, rgb):
        super().__init__(x, y, w, h)
        self.rgb = rgb
        self.hud = False


class Logo(GameObject):
    def __init__(self):
        self._xy = 65, 187
        self.wh = 31, 6
        self.rgb = 0, 0, 0
        self.hud = True


class Clock(GameObject):
    def __init__(self, x, y, w, h):
        self._xy = x, y
        self.wh = w, h
        self.rgb = 0, 0, 0
        self.hud = True


class Score(GameObject):
    def __init__(self, ten=False):
        if ten:
            self._xy = 67, 6
        else:
            self._xy = 75, 6
        self.ten = ten
        self.rgb = 0, 0, 0
        self.wh = 6, 7
        self.hud = True


def _detect_objects_skiing(objects, obs, hud=False):
    objects.clear()
    player = find_objects(obs, player_c)
    for el in player:
        objects.append(Player(*el))
    for col in flag_c:
        flags = find_objects(obs, col)
        for el in flags:
            objects.append(Flag(*el, col))
    for col in trees_c:
        trees = find_objects(obs, col)
        for el in trees:
            objects.append(Tree(*el, col))
    for col in moguls_c:
        moguls = find_objects(obs, col)
        for el in moguls:
            objects.append(Mogul(*el, col))
    if hud:
        objects.append(Logo())
