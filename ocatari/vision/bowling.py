from .utils import find_objects
from .utils import find_mc_objects, match_objects
from .game_objects import GameObject

objects_colors = {"player": [[0, 0, 0], [198, 89, 179]],
                  "ball": [45, 50, 184],
                  "pins": [45, 50, 184],
                  "score": [84, 92, 214],
                  "round": [45, 50, 184],
                  "board": [84, 92, 214],
                  }


class Player(GameObject):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.rgb = 84, 92, 214


class Pin(GameObject):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.rgb = 45, 50, 184


class Ball(GameObject):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.rgb = 45, 50, 184


class Score(GameObject):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.rgb = 84, 92, 214
        self.hud = True

class Board(GameObject):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.rgb = 84, 92, 214
        self.hud = True


class Round(GameObject):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.rgb = 45, 50, 184
        self.hud = True
        
def _detect_objects(objects, obs, hud=False):
    
    player = objects[0]
    player_bb = find_mc_objects(obs, objects_colors["player"], size=(8, 32), tol_s=5, min_distance=1, closing_dist= 30, miny=85)
    if player_bb:
            player.xywh = player_bb[0]
    
    ball = objects[1]
    ball_bb = find_objects(
        obs, objects_colors["ball"], size = (4,10), tol_s = 1,min_distance=0.1, closing_active=False, miny=70)
    if ball_bb:
            ball.xywh = ball_bb[0]
            
    start_idx=2  
          
    pins_bb = find_objects(obs, objects_colors["pins"], size =(2,4) ,tol_s=0, closing_active=False, min_distance=1)
    match_objects(objects, pins_bb, 2,10,Pin)
    start_idx+=10

    if hud:
        player_score = find_objects(
            obs, objects_colors["score"], closing_dist=10, maxy=34, miny=19)
        match_objects(objects, player_score, start_idx,1,Score)
        
        start_idx+=1
        round_player = find_objects(
            obs, objects_colors["round"],maxx=110, maxy=17, closing_dist=10)
        match_objects(objects,round_player,start_idx,1,Round)
        
        start_idx+=1
        board_bb = find_objects(obs, objects_colors["board"],minx=16, miny=35, maxy=80, closing_dist=30)
        match_objects(objects,board_bb,start_idx,1,Board)
        
        