from .utils import find_objects, find_mc_objects, find_rectangle_objects
from .game_objects import GameObject

objects_colors = {"gopher": [72,44,0], "blocks":[223,183,85]}
hud_color=[195,144,61]
player_colors=[[72,160,72],[214,92,92],[183,194,95],[181,83,40],[84,92,214],[181,83,40]]
carrot_colors=[[50,132,50],[162,98,33],[180,122,48],[181,83,40]]
birdcolors=[[195,144,61],[236,236,236],[232,204,99],[117,128,240]]

class Player(GameObject):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.rgb = 72,160,72
        self.hud = False

class Gopher(GameObject):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.rgb = 72,44,0
        self.hud = False

class Carrot(GameObject):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.rgb = 162,98,33
        self.hud = False

class Bird(GameObject):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.rgb = 45,50,184 
        self.hud = False

class Empty_block(GameObject):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.rgb = 223,183,85 
        self.hud = False

class Score(GameObject):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.rgb = 195,144,65 
        self.hud = True


def _detect_objects(objects, obs, hud=False):
    # detection and filtering
    objects.clear()
    player = find_mc_objects(obs, player_colors, size=(11,50),tol_s=2, closing_dist=1)
    for p in player:
        objects.append(Player(*p))
    
    carrots = find_mc_objects(obs, carrot_colors, size=(12,27), miny=125, tol_s=4, closing_dist=2)
    for c in carrots:
        objects.append(Carrot(*c))
    
    gopher=find_objects(obs,objects_colors["gopher"],miny=130,size=(14,10),tol_s=2)
    for g in gopher:
        objects.append(Gopher(*g))
    
    blocks = find_rectangle_objects(obs, objects_colors["blocks"], max_size=(8,6),maxy=182,miny=176)
    for b in blocks:
        objects.append(Empty_block(*b))
    
    blocks = find_rectangle_objects(obs, objects_colors["blocks"], max_size=(8,6),maxy=176,miny=168)
    for b in blocks:
        objects.append(Empty_block(*b))
    
    blocks = find_rectangle_objects(obs, objects_colors["blocks"], max_size=(8,6),maxy=168,miny=162)
    for b in blocks:
        objects.append(Empty_block(*b))
    
    blocks = find_rectangle_objects(obs, objects_colors["blocks"], max_size=(8,12),miny=182)
    for b in blocks:
        objects.append(Empty_block(*b))
    

    if hud:
        birds = find_mc_objects(obs, birdcolors, size=(15,18), maxy=90, tol_s=3, closing_dist=2)
        for b in birds:
            objects.append(Bird(*b))
        score=find_objects(obs,hud_color,maxy=60,size=(5,9),tol_s=2, closing_active=False)
        for s in score:
            objects.append(Score(*s))
        
        


        # import ipdb; ipdb.set_trace()
        
