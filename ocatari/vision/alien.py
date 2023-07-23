from .utils import find_objects
from .game_objects import GameObject


hud_color=[132,144,252]
player_colors=[[132,144,252],[252,144,144]]
egg_colors=[[252,252,84],[132,252,212],[252,144,144],[236,140,224],[132,144,252]]
alien_colors=[[236,140,224],[252,252,84],[132,252,212]]
pulsar_colors=[[252,144,144]]

class Player(GameObject):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.rgb = 132,144,252 
        self.hud = False


class Egg(GameObject):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.rgb = 0, 0, 0
        self.hud = False


class Alien(GameObject):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.rgb = 0,0,0
        self.hud = False


class Pulsar(GameObject):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.rgb = 0,0,0
        self.hud = False


class PlayerScore(GameObject):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.rgb = 132,144,252
        self.hud = True


class PulsarCount(GameObject):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # self.rgb = 0, 0, 0
        self.count=0
        self.hud=True


def _detect_objects_alien(objects, obs, hud=False):
    # detection and filtering
    objects.clear()
    for color in player_colors:
        player = find_objects(obs, color,size=(4,13), tol_s=4, min_distance=1)
        for e in player:
            eg=Player(*e)
            eg.rgb=color
            objects.append(eg)
    for color in egg_colors:
        eggs = find_objects(obs, color,size=(1,2), tol_s=2, min_distance=1)
        for e in eggs:
            eg=Egg(*e)
            eg.rgb=color
            objects.append(eg)
    for color in alien_colors:
        aliens = find_objects(obs, color,size=(8,13), tol_s=4, min_distance=1)
        for e in aliens:
            eg=Alien(*e)
            eg.rgb=color
            objects.append(eg)
    for color in pulsar_colors:
        pulsars = find_objects(obs, color,size=(6,5), tol_s=2, min_distance=1)
        for e in pulsars:
            eg=Pulsar(*e)
            eg.rgb=color
            objects.append(eg)

    if hud:
        score = find_objects(obs, hud_color, closing_active=False, miny=174,maxy=183)
        for s in score:
            objects.append(PlayerScore(*s))
        count_pulsars=find_objects(obs, hud_color, closing_active=False, miny=183,maxy=192)
        for c in count_pulsars:
            objects.append(PulsarCount(*c))


