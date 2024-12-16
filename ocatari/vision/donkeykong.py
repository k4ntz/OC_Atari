from .utils import find_objects, find_mc_objects
from .game_objects import GameObject

objects_colors = {"player": [[200, 72, 72], [236, 236, 236], [66, 136, 176]],
                  "barrel": [236, 200, 96],
                  "score": [158, 208, 101],
                  "girlfriend": [[252, 252, 84], [84, 160, 197], [200, 72, 72]],
                  "donkeykong": [181, 83, 40],
                  "hammer": [[236, 200, 96], [181, 108, 224]],
                  "ladder": [181, 108, 224],
                  "life": [181, 108, 224],
                  }


class Player(GameObject):
    """
    The player figure: Mother Kangaroo.
    """

    def __init__(self, x, y, w, h):
        super(Player, self).__init__(x, y, w, h)
        self._xy = x, y
        self.wh = w, h
        self.rgb = 200, 72, 72
        self.hud = False


class Girlfriend(GameObject):
    """
    Mario's Girlfriend.
    """

    def __init__(self, x, y, w, h):
        super(Girlfriend, self).__init__(x, y, w, h)
        self._xy = x, y
        self.wh = w, h
        self.rgb = 84, 160, 197
        self.hud = False


class Barrel(GameObject):
    """
    The Monkey monkeys.
    """

    def __init__(self, x, y, w, h):
        super(Barrel, self).__init__(x, y, w, h)
        self._xy = x, y
        self.wh = w, h
        self.rgb = 236, 200, 96
        self.hud = False


class Hammer(GameObject):
    """
    The collectable fruits.
    """

    def __init__(self, x, y, w, h):
        super(Hammer, self).__init__(x, y, w, h)
        self._xy = x, y
        self.wh = w, h
        self.rgb = 236, 200, 96
        self.hud = False


class Ladder(GameObject):
    """
    The ladders.
    """

    def __init__(self, x=0, y=0, w=0, h=0):
        super(Ladder, self).__init__(x, y, w, h)
        self._xy = x, y
        self._prev_xy = x, y
        self.wh = 4, 17
        self.rgb = 181, 108, 224
        self.hud = False


class Platform(GameObject):
    """
    The platforms.
    """

    def __init__(self, x=0, y=0, w=8, h=4):
        super(Platform, self).__init__(x, y, w, h)
        self._xy = x, y
        self._prev_xy = x, y
        self.wh = w, h
        self.rgb = 162, 98, 33
        self.hud = False


class DonkeyKong(GameObject):
    """
    The donkey kong enemy.
    """

    def __init__(self, x, y, w, h):
        super(DonkeyKong, self).__init__(x, y, w, h)
        self._xy = x, y
        self.wh = w, h
        self.rgb = 181, 83, 40
        self.hud = False


class Score(GameObject):
    """
    The player's score display (HUD).
    """

    def __init__(self, x, y, w, h):
        super(Score, self).__init__(x, y, w, h)
        self._xy = x, y
        self.wh = w, h
        self.rgb = 158, 208, 201
        self.hud = True
        self.value = 0


class Life(GameObject):
    """
    The player's remaining lives (HUD).
    """

    def __init__(self, x, y, w, h):
        super(Life, self).__init__(x, y, w, h)
        self._xy = x, y
        self.wh = w, h
        self.rgb = 181, 108, 224
        self.hud = True


ladders = [(108, 176), (48, 148), (80, 148), (88, 120), (108, 120),
           (48, 92), (68, 92), (108, 64), (76, 40), (32, 40)]


def _detect_objects(objects, obs, hud=True):
    objects.clear()
    player = find_mc_objects(
        obs, objects_colors["player"], size=(8, 15), tol_s=4)
    for bb in player:
        objects.append(Player(*bb))
    girlfriend = find_mc_objects(
        obs, objects_colors["girlfriend"], size=(8, 16), tol_s=4)
    for bb in girlfriend:
        objects.append(Girlfriend(*bb))
    donkey = find_objects(
        obs, objects_colors["donkeykong"], size=(18, 21), tol_s=4)
    for bb in donkey:
        objects.append(DonkeyKong(*bb))
    barrels = find_objects(obs, objects_colors["barrel"], size=(8, 8), tol_s=3)
    for bb in barrels:
        objects.append(Barrel(*bb))
    hammers = find_mc_objects(obs, objects_colors["hammer"], size=(
        4, 7), tol_s=3, closing_active=False)
    for bb in hammers:
        objects.append(Hammer(*bb))

    objects.extend([Ladder(*xy) for xy in ladders])

    if hud:
        score = find_objects(obs, objects_colors["score"], maxy=25)
        for bb in score:
            objects.append(Score(*bb))
        life = find_objects(
            obs, objects_colors["life"], miny=20, maxy=32, minx=90, closing_dist=5)
        for bb in life:
            objects.append(Life(*bb))
