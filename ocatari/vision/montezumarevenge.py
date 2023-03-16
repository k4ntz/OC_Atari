from .game_objects import GameObject
from .utils import find_objects, find_mc_objects


objects_colors = {'white': [236, 236, 236], 'yellow': [232, 204, 99],
                  'playercolors': [[228, 111, 111], [200, 72, 72], [210, 182, 86]],
                  'lifecolors': [[200, 72, 72], [210, 182, 86]]}


#  ---- enemies -----
class Skull(GameObject):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.rgb = [236, 236, 236]


#  ---- collectable objects -----
class Key(GameObject):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.rgb = [232, 204, 99]


#  ---- others -----
class Player(GameObject):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.rgb = [228, 111, 111]


#  ---- HUD -----
class Life(GameObject):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.rgb = [210, 182, 86]


class Score(GameObject):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.rgb = [236, 236, 236]


def _detect_objects_montezumarevenge(objects, obs, hud=False):
    objects.clear()

    object0 = find_objects(obs, objects_colors['white'], miny=25)
    for bb in object0:
        objects.append(Skull(*bb))

    object1 = find_objects(obs, objects_colors['yellow'])
    for bb in object1:
        if bb[3] <= 16:
            objects.append(Key(*bb))

    players = find_mc_objects(obs, objects_colors['playercolors'], miny=25)
    for bb in players:
        objects.append(Player(*bb))

    if hud:
        lifes = find_mc_objects(obs, objects_colors['lifecolors'], maxy=25, closing_dist=1)
        for bb in lifes:
            objects.append(Life(*bb))

        scores = find_objects(obs, objects_colors['white'], maxy=25, closing_dist=1)
        for bb in scores:
            objects.append(Score(*bb))
