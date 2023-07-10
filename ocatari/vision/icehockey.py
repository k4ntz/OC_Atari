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


def _detect_objects_icehockey(objects, obs, hud=False):
    # detection and filtering
    objects.clear()
    for color in player_colors:
        player = find_objects(obs, color,size=(4,13), tol_s=4, min_distance=1)
        for e in player:
            eg=Player(*e)
            eg.rgb=color
            objects.append(eg)

    if hud:
        pass

