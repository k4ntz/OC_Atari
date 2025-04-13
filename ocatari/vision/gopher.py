from .utils import find_objects, find_mc_objects, find_rectangle_objects, match_objects
from .game_objects import GameObject, NoObject

objects_colors = {"player" : [[72, 160, 72], [214, 92, 92], [183, 194, 95],
                                [181, 83, 40], [84, 92, 214], [181, 83, 40]],
                  "gopher": [72, 44, 0],
                  "carrot": [[50, 132, 50], [162, 98, 33], [180, 122, 48], [181, 83, 40]],
                  "hole": [223, 183, 85],
                  "bird" :[[195, 144, 61], [236, 236, 236], [232, 204, 99], [117, 128, 240]],
                  "hud" : [195, 144, 61]}

class Player(GameObject):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.rgb = 72, 160, 72
        self.hud = False

class Gopher(GameObject):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.rgb = 72, 44, 0
        self.hud = False

class Carrot(GameObject):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.rgb = 162, 98, 33
        self.hud = False

class Bird(GameObject):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.rgb = 45, 50, 184
        self.hud = False

class Hole(GameObject):
      def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)
            self.rgb = 223, 183, 85
            self.hud = False

class Floor(GameObject):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.rgb = 223, 183, 85
        self.hud = False

class Score(GameObject):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.rgb = 195, 144, 65
        self.hud = True


def _detect_objects(objects, obs, hud=False):

    #Player
    player = objects[0]
    player_bb = find_mc_objects(obs, objects_colors["player"], size=(
        11, 50), tol_s=2, closing_dist=1)
    if player_bb:
        player.xywh = player_bb[0]
    start_idx = 1

    #Gopher
    gopher = objects[1]
    gopher_bb = find_objects(
        obs, objects_colors["gopher"], miny=130, size=(14, 10))
    if gopher_bb:
        gopher.xywh = gopher_bb[0]
    start_idx += 1
    
    #Carrot
    carrots_bb = find_mc_objects(obs, objects_colors["carrot"], size=(
        12, 27), miny=125, tol_s=4, closing_dist=2)
    match_objects(objects, carrots_bb, start_idx, 3, Carrot)
    start_idx+=3
    
    #Hole
    hole_bb = find_objects(obs, objects_colors["hole"], size=(8,7), tol_s=(0,21) ,maxy=183)
    match_objects(objects, hole_bb, start_idx, 6, Hole)
    start_idx+=6
    #Floor
    start_idx+=1
    
    #Bird
    bird_bb = find_mc_objects(obs, objects_colors["bird"], size=(15,18))
    match_objects(objects, bird_bb, start_idx, 1, Bird)
    start_idx+=1


    if hud:
        #Score
        score_bb = find_objects(obs, objects_colors["hud"], closing_dist=10)
        match_objects(objects, score_bb, start_idx, 1, Score)
