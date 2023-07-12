from .utils import find_objects, find_mc_objects
from .game_objects import GameObject

objects_colors = {"ball": [0, 0, 0], "enemyscore":[236,200,96], "playerscore":[84,92,214], "timer":[84,92,214]}
hud_color=[132,144,252]
player_colors=[[45,50,184],[200,72,72],[184,50,50]]
enemy_colors=[[200,72,72],[210,182,86],[232,204,99],[82,126,45]]

class Player(GameObject):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.rgb = 45,50,184 
        self.hud = False


def _detect_objects_gopher(objects, obs, hud=False):
    # detection and filtering
    objects.clear()
    player = find_mc_objects(obs, player_colors, size=(16, 20), tol_s=10, closing_dist=3)
    for p in player:
        objects.append(Player(*p))
    
    ball=find_objects(obs,objects_colors["ball"],size=(2,2),minx=32,maxx=127,miny=46,maxy=182,tol_s=1,min_distance=1)
    # import ipdb; ipdb.set_trace()
    for b in ball:
        objects.append(Player(*b))
    

    if hud:
        pass
        


        # import ipdb; ipdb.set_trace()
        