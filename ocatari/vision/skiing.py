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


class Clock(GameObject):
    def __init__(self, x, y, w, h):
        self._xy = x, y
        self.wh = w, h
        self.rgb = 0, 0, 0
        self.hud = True


class Score(GameObject):
    def __init__(self, x, y, w, h):
        self._xy = x, y
        self.wh = w, h
        self.rgb = 0, 0, 0
        self.hud = True


def _detect_objects(objects, obs, hud=False):
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
        scores = find_objects(obs, (0, 0, 0), miny=4, maxy=14, minx=50, maxx=100, closing_active=False) 
        for sc in scores:
            objects.append(Score(*sc))
        clocks = find_objects(obs, (0, 0, 0), miny=15, maxy=25, minx=50, maxx=100, closing_active=False) 
        for cl in clocks:
            objects.append(Clock(*cl))
