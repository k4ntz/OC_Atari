from .game_objects import GameObject
from .utils import find_objects, find_mc_objects


objects_colors = {'white': [236, 236, 236], 'yellow': [232, 204, 99], 'orange': [213, 130, 74],
                  'blue': [101, 111, 228], 'green': [92, 186, 92], 'yellow_2':[204, 216, 110],
                  'white_2': [214, 214, 214], 'white_3': [192, 192, 192],
                  'playercolors': [[228, 111, 111], [200, 72, 72], [210, 182, 86]],
                  'playercolors2': [[240, 128, 128], [200, 72, 72], [210, 182, 86]],
                  'lifecolors': [[200, 72, 72], [210, 182, 86]]}


class Player(GameObject):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.rgb = [228, 111, 111]


#  ---- enemies -----
class Skull(GameObject):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.rgb = [236, 236, 236]


class Spider(GameObject):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.rgb = [92, 186, 92]


class Snake(GameObject):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.rgb = [192, 192, 192]


#  ---- collectable objects -----
class Key(GameObject):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.rgb = [232, 204, 99]

class Amulet(GameObject):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.rgb = [210, 182, 86]


class Torch(GameObject):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.rgb = [204, 216, 110]


class Sword(GameObject):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.rgb = [214, 214, 214]


class Ruby(GameObject):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.rgb = [213, 130, 74]


#  ---- others -----
class Barrier(GameObject):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.rgb = [232, 204, 99]


class Beam(GameObject):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.rgb = [101, 111, 228]


class Rope(GameObject):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.rgb = [232, 204, 99]


#  ---- HUD -----
class Life(GameObject):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.rgb = [210, 182, 86]


class Score(GameObject):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.rgb = [236, 236, 236]


class Torch_HUD(GameObject):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.rgb = [232, 204, 99]


class Sword_HUD(GameObject):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.rgb = [232, 204, 99]


class Key_HUD(GameObject):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.rgb = [232, 204, 99]


class Amulet_HUD(GameObject):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.rgb = [232, 204, 99]


def _detect_objects(objects, obs, hud=False):
    objects.clear()

    players = find_mc_objects(obs, objects_colors['playercolors'], miny=25)
    for bb in players:
        objects.append(Player(*bb))

    players2 = find_mc_objects(obs, objects_colors['playercolors2'], miny=25)
    for bb in players2:
        objects.append(Player(*bb))

    skull = find_objects(obs, objects_colors['white'], miny=25, size=(13,7))
    for bb in skull:
        objects.append(Skull(*bb))

    spider = find_objects(obs, objects_colors['green'], miny=25)
    for bb in spider:
        objects.append(Spider(*bb))

    snek = find_objects(obs, objects_colors['white_3'], miny=25, size=(13,7))
    for bb in snek:
        objects.append(Snake(*bb))

    torch = find_objects(obs, objects_colors['yellow_2'], size=(6,13), miny=48)
    for bb in torch:
        objects.append(Torch(*bb))

    sword = find_objects(obs, objects_colors['white_2'], size=(7,15), miny=48)
    for bb in sword:
        objects.append(Sword(*bb))

    rope = find_objects(obs, objects_colors['yellow'], size=(1,39), tol_s=2)
    for bb in rope:
        objects.append(Rope(*bb))

    rope2 = find_objects(obs, objects_colors['yellow'], size=(1,51), tol_s=4)
    for bb in rope2:
        objects.append(Rope(*bb))

    rope_w = find_objects(obs, objects_colors['white'], miny=25, size=(1, 25))
    for bb in rope_w:
        r = Rope(*bb)
        r.rgb = objects_colors['white']
        objects.append(r)

    key = find_objects(obs, objects_colors['yellow'], size=(7,15), miny=48)
    for bb in key:
        objects.append(Key(*bb))

    amulet = find_mc_objects(obs, objects_colors['playercolors'], miny=25, size=(6,15), tol_s=2)
    for bb in amulet:
        objects.append(Amulet(*bb))

    barrier = find_objects(obs, objects_colors['yellow'], size=(4,37), tol_s=2)
    for bb in barrier:
        objects.append(Barrier(*bb))

    beam = find_objects(obs, objects_colors['blue'], minx=10, maxx=150, closing_dist=4)
    for bb in beam:
        objects.append(Beam(*bb))

    ruby = find_objects(obs, objects_colors['orange'], size=(7,12), tol_s=2)
    for bb in ruby:
            objects.append(Ruby(*bb))

    if hud:

        torch_h = find_objects(obs, objects_colors['yellow'], size=(6,13), tol_s=0, maxy=48, closing_dist=1)
        for bb in torch_h:
            objects.append(Torch_HUD(*bb))

        sword_h = find_objects(obs, objects_colors['yellow'], size=(6,15), tol_s=0, maxy=48, closing_dist=1,)
        for bb in sword_h:
            objects.append(Sword_HUD(*bb))

        key_h = find_objects(obs, objects_colors['yellow'], size=(7,15), tol_s=0, maxy=48, closing_dist=1)
        for bb in key_h:
            objects.append(Key_HUD(*bb))

        amulet_h = find_objects(obs, objects_colors['yellow'], size=(5,15), tol_s=0, maxy=48, closing_dist=1)
        for bb in amulet_h:
            objects.append(Amulet_HUD(*bb))
        
        lifes = find_mc_objects(obs, objects_colors['lifecolors'], maxy=25, closing_dist=1)
        for bb in lifes:
            objects.append(Life(*bb))

        scores = find_objects(obs, objects_colors['white'], maxy=25, closing_dist=1)
        for bb in scores:
            objects.append(Score(*bb))
