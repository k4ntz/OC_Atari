from .utils import find_objects, match_objects
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
        super().__init__(x, y, w, h)
        self.rgb = 0, 0, 0
        self.hud = True


class Score(GameObject):
    def __init__(self, x, y, w, h):
        super().__init__(x, y, w, h)
        self.rgb = 0, 0, 0
        self.hud = True


# MAX_NB_OBJECTS =  {'Player': 1, 'Tree': 4, 'Mogul': 3, 'Flag': 4}
# MAX_NB_OBJECTS_HUD =  {'Player': 1, 'Tree': 4, 'Mogul': 3, 'Flag': 4, 'Score': 1, 'Clock': 1}


def _detect_objects(objects, obs, hud=False):
    player = objects[0]
    player_bb = find_objects(obs, player_c)[0]
    player.xywh = player_bb
    trees_bb = []
    for col in trees_c:
        trees_bb.extend([list(bb) + [col] for bb in find_objects(obs,
                        col, closing_active=True, closing_dist=12)])
    match_objects(objects, trees_bb, 1, 4, Tree)
    moguls_bb = []
    for col in moguls_c:
        moguls_bb.extend([list(bb) + [col] for bb in find_objects(obs,
                         col, closing_active=True, closing_dist=12)])
    match_objects(objects, moguls_bb, 5, 3, Mogul)
    flags_bb = []
    for col in flag_c:
        flags_bb.extend([list(bb) + [col] for bb in find_objects(obs,
                        col, closing_active=True, closing_dist=12)])
    match_objects(objects, flags_bb, 8, 4, Flag)
    if hud:
        score, clock = objects[-2:]
        score_bb = find_objects(obs, (0, 0, 0), miny=4, maxy=14,
                                minx=50, maxx=100, closing_active=True, closing_dist=5)[0]
        score.xywh = score_bb
        clock_bb = find_objects(obs, (0, 0, 0), miny=15, maxy=25,
                                minx=50, maxx=100, closing_active=True, closing_dist=5)[0]
        clock.xywh = clock_bb
