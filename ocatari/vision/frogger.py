from .utils import find_objects, match_objects
from .game_objects import GameObject

objects_colors = {"frog": [[110, 156, 66], [162, 162, 42]], "log": [105,105,15], "turtle": [144,72,17] ,"diving turtle" :[66,114,194],
                  "lady frog":[236,236,236], "alligator":[105,105,15], "snake":[82,126,45], "happy frog":[82,126,45], 
                  "alligator's head":[110,156,66], "fly": [110,156,66], 
                  "score": [195,144,61],"lives": [236,236,236], "time": [[0,0,0],[144,72,17]]}

car_colors = [[195, 144, 61], [164, 89, 208], [82, 126, 45], [198, 89, 179], [236, 236, 236]]
cars_per_line = [2, 2, 4, 2, 2]


class Frog(GameObject):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.rgb = 110, 156, 66


class Car(GameObject):
    def __init__(self, x, y, w, h, rgb):
        super().__init__(x, y, w, h)
        self.rgb = rgb


class Log(GameObject):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.rgb = 139, 69, 19        

class Turtle(GameObject):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.rgb = 144,72,17

class DivingTurtle(GameObject):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.rgb = 66,114,194

class LadyFrog(GameObject):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.rgb = 236,236,236

class Alligator(GameObject):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.rgb = 105,105,15

class Snake(GameObject):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.rgb = 82,126,45   
        
class HappyFrog(GameObject):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.rgb = 82,126,45

class AlligatorHead(GameObject):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.rgb = 110,156,66

class Fly(GameObject):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.rgb = 110,156,66

class Car(GameObject):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.rgb = 195, 144, 61

class Score(GameObject):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.rgb = 195,144,61
        self.hud = True

class Lives(GameObject):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.rgb = 236,236,236
        self.hud = True
                
class Time(GameObject):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.rgb = 0,0,0
        self.hud = True

def _detect_objects(objects, obs, hud=False):
    frog = objects[0]
    for frog_color in objects_colors["frog"]:
        frog_bb = find_objects(obs, frog_color, size=(7, 7), tol_s=2)
        if frog_bb:
            frog.xywh = frog_bb[0]

    start_idx = 1
    for nbcars, color in zip(cars_per_line, car_colors):
        cars_bb = [list(bb) + [color] for bb in find_objects(obs, color, closing_active=True, minx=8, maxx=152, miny=104, maxy=170)]
        match_objects(objects, cars_bb, start_idx, nbcars, Car)
        start_idx += nbcars

    # Detect Log and Alligator
    minys, maxys = [[], [], []]
    logs_per_line = [3, 1, 2]
    logs = find_objects(obs, objects_colors["log"], miny=0, maxy=200) 
    # for log in logs:
    #     if (obs[log[1]][log[0]] == [105,105,15]).all():
    #         objects.append(Log(*log))
    #     else:
    #         objects.append(Alligator(*log))