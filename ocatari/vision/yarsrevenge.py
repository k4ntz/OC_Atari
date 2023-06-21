from .utils import find_objects,find_mc_objects
from .game_objects import GameObject
import numpy as np

objects_colors = {
    "player": [169,128,240]
    }
player_colors=[[132,144,252],[252,144,144]]
enemy_colors=[[]]
barrier_colors=[[162,134,56],[200,72,72],[82,126,45]]

class Player(GameObject):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.rgb = 169,128,240 
        self.hud = False

class Enemy(GameObject):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.rgb = 240,240,240 
        self.hud = False

class Swirl(GameObject):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.rgb = 169,128,240 
        self.hud = False

class Barrier(GameObject):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.rgb = 250,250,250
        self.hud = False

# List of objects to detect: Player, Enemy, Swirl, fired bullets/shots by both Enemy and Player, Cannon that appears, Shield chunks, Barrier
def _detect_objects_yarsrevenge(objects, obs, hud=False):
    # detection and filtering
    objects.clear()
    player=find_objects(obs, objects_colors["player"], closing_active=False,size=(8,16), tol_s=2)
    for p in player:
        # Handling the case where color of enemy is same as color of object
        if p[0]<=146:
            objects.append(Player(*p))
        else:
            objects.append(Enemy(*p))
    
    b=(52,4,28,190)
    count=0
    for color in barrier_colors:
        b_segment=find_objects(obs,color,closing_active=False,size=(10,10),minx=51, maxx=78, tol_s=8)
        count+=len(b_segment)
    if count!=0:
        objects.append(Barrier(*b))
    
    # Detecting enemy
    # Detecting what color is enemy right now
    enemy_color=[]
    obs_line=np.copy(obs[135:156])

    for i in range(obs_line.shape[0]):
        flag=True
        for j in range(obs_line.shape[1]):
            if not np.array_equal(obs_line[i,j],np.array(objects_colors["player"])):
                if not np.array_equal(obs_line[i,j],np.array([0,0,0])):
                    enemy_color.append(obs_line[i,j])
    import ipdb; ipdb.set_trace()

    # enemy=find_objects(obs,enemy_color,size=)




    if hud:
        pass

