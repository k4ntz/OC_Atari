import sys
from .game_objects import GameObject, NoObject


MAX_NB_OBJECTS = {"Player": 1, "Enemy": 1,
                  "Girlfriend": 1, "Bomb": 8, "Ladder": 12}

MAX_NB_OBJECTS_HUD = {"Player": 1, "Enemy": 1, "Girlfriend": 1, "Bomb": 8, "Ladder": 12,
                      "Score": 1, "BonusPoints": 1}


class Player(GameObject):
    def __init__(self):
        super(Player, self).__init__()
        self._xy = 38, 94
        self.wh = 5, 17
        self.rgb = 92, 197, 135
        self.hud = False


class Girlfriend(GameObject):
    def __init__(self):
        super(Girlfriend, self).__init__()
        self._xy = 95, 28
        self.wh = 6, 17
        self.rgb = 50, 50, 176
        self.hud = False


class Enemy(GameObject):
    def __init__(self):
        super(Enemy, self).__init__()
        self._xy = 51, 94
        self.wh = 14, 35
        self.rgb = 150, 113, 26
        self.hud = False


class Bomb(GameObject):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


class Ladder(GameObject):
    def __init__(self, x=140, y=207):
        super(Ladder, self).__init__()
        self._xy = x, y
        self.wh = 8, 18
        self.rgb = 201, 92, 135
        self.hud = False


class Score(GameObject):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


class BonusPoints(GameObject):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


def _get_max_objects(hud=False):
    def fromdict(max_obj_dict):
        objects = []
        mod = sys.modules[__name__]
        for k, v in max_obj_dict.items():
            for _ in range(0, v):
                objects.append(getattr(mod, k)())
        return objects

    if hud:
        return fromdict(MAX_NB_OBJECTS_HUD)
    return fromdict(MAX_NB_OBJECTS)


def _init_objects_ram(hud=False):
    ladder_positions = [(140, 207), (12, 207), (76, 183), (140, 159), (12, 159), (76, 135),
                        (140, 111), (12, 111), (76, 87), (132, 63), (20, 63), (76, 43)]
    objects = [Player(), Enemy(), Girlfriend()] + [NoObject()] * 8 + \
        [Ladder(x=pos[0], y=pos[1]) for pos in ladder_positions]

    if hud:
        objects.extend([Score(), BonusPoints()])
    return objects


def _detect_objects_ram(objects, ram_state, hud=True):
    pass
