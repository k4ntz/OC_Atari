from .utils import find_objects
from .game_objects import GameObject

objects_colors = {
    'player': [[236, 236, 236], [184, 70, 162]], # The second color is also used for bait.
    'arrow': [236, 236, 236],
    'balloon': [[236, 236, 236],
                [127, 92, 213],
                [160, 171, 79],
                [187, 187, 53],
                [92, 186, 92],
                [214, 92, 92]],
    'enemy': [195, 144, 61],
    'stone': [[236, 236, 236],
              [127, 92, 213],
              [160, 171, 79],
              [187, 187, 53],
              [214, 92, 92],
              [92, 186, 92],
              [195, 144, 61]],
    'rock': [162, 98, 33],
    'lives': [0, 0, 0]
    }


class Player(GameObject):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.rgb = 236, 236, 236

class Arrow(GameObject):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.rgb = 236, 236, 236

class Bait(GameObject):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.rgb = 184, 70, 162

class Balloon(GameObject):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.rgb = 92, 186, 92

class Enemy(GameObject):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.rgb = 195, 164, 61

class Stone(GameObject):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.rgb = 92, 186, 92

class Rock(GameObject):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.rgb = 162, 98, 33

class PlayerScore(GameObject):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.rgb = 236, 236, 236
        self.hud = True

class Lives(GameObject):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.rgb = 0, 0, 0
        self.hud = True


def _detect_objects(objects, obs, hud=False):
    # detection and filtering
    objects.clear()
    
    # Player
    for color in objects_colors['player']:
        player = find_objects(obs, color, size=(10, 15), tol_s=2, minx=129, miny=61, maxx=139, maxy=182)
        for el in player:
            objects.append(Player(*el))
    
    # Arrow
    arrow = find_objects(obs, objects_colors['arrow'], size=(8,1), tol_s=1, miny=61, maxx=129)
    for el in arrow:
        objects.append(Arrow(*el))
    
    # Bait
    unpicked_bait = find_objects(obs, objects_colors['player'][0], size=(8, 4),
                                 tol_s=2, minx=129, miny=61, maxx=139, maxy=182)
    flying_bait = find_objects(obs, objects_colors['player'][1], size=(8, 4),
                               tol_s=2, miny=61, maxx=129)
    for el in unpicked_bait + flying_bait:
        objects.append(Bait(*el))
    
    # Balloon
    minx = [43, 75, 107] 
    maxx = [53, 85, 117]
    for i in range(6):
        balloon = find_objects(obs, objects_colors['balloon'][i],
                               minx=minx[i//2], miny=61, maxx=maxx[i//2], maxy=175)
        for el in balloon:
            objects.append(Balloon(*el))
    
    # Enemy
    enemy = find_objects(obs, objects_colors['enemy'], miny=69, maxy=184)
    for el in enemy:
        if el[2] > 4 and el[3] > 4:
            objects.append(Enemy(*el))
    
    # Stone
    for i in range(7):
        stone = find_objects(obs, objects_colors['stone'][i], size=(4, 4), tol_s=0)
        for el in stone:
            objects.append(Stone(*el))

    # Rock
    rock = find_objects(obs, objects_colors['rock'])
    for el in rock:
        objects.append(Rock(*el))
    
    # PlayerScore
    if hud:
        player_score = find_objects(obs, objects_colors["player"][0], maxy=13, closing_dist=8)
        for el in player_score:
            objects.append(PlayerScore(*el))
        
        lives = find_objects(obs, objects_colors["lives"], miny=205, maxy=213, closing_dist=8)
        for el in lives:
            objects.append(Lives(*el))
