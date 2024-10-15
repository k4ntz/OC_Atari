from .utils import find_objects, match_objects
from .game_objects import GameObject

objects_colors = {"frog": [[110, 156, 66],[162,162,42]], "log": [105,105,15], "turtle": [[144,72,17], [66, 114, 194]],
                  "lady frog":[236,236,236], "alligator":[105,105,15], "snake":[82,126,45], "happy frog":[82,126,45], 
                  "alligator's head":[110,156,66], "fly": [110,156,66], 
                  "score": [195,144,61], "lives": [236,236,236], "time": [[0,0,0],[144,72,17]]}

car_colors = [[195, 144, 61], [164, 89, 208], [82, 126, 45], [198, 89, 179], [236, 236, 236]]
lane_limits = [[158, 170], [147,159], [134, 146], [121, 133], [104, 120]]
cars_per_line = [2, 2, 4, 2, 2]

logs_per_line = [3, 2, 3]
logs_lane_limits = [[66, 78], [53, 65], [27, 39]]

turtles_per_line = [6, 4]
turtles_lane_limits = [[79, 91], [40, 52]]

class Frog(GameObject):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.rgb = 110, 156, 66
        

class Log(GameObject):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.rgb = 105, 105, 15       


class Alligator(GameObject):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.rgb = 105, 105, 15


class Turtle(GameObject):
    def __init__(self, x, y, w, h, rgb):
        super().__init__(x, y, w, h)
        self.rgb = rgb
    
    @property
    def diving(self):
        return self.rgb == [66, 114, 194]


# class DivingTurtle(GameObject):
#     def __init__(self, *args, **kwargs):
#         super().__init__(*args, **kwargs)
#         self.rgb = 66,114,194


class LadyFrog(GameObject):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.rgb = 236,236,236


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
    def __init__(self, x, y, w, h, rgb):
        super().__init__(x, y, w, h)
        self.rgb = rgb


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
    
    # Detect Frog 
    frogs = []
    for color in objects_colors["frog"]:
        frog_bb = find_objects(obs, color)
        if frog_bb:
            frog.xywh = frog_bb[0]
            frog.rgb = color
    
    start_idx = 1
    for nbcars, color, (miny, maxy) in zip(cars_per_line, car_colors, lane_limits):
        cars_bb = [list(bb) + [color] for bb in find_objects(obs, color, closing_active=True, minx=8, maxx=152, miny=miny, maxy=maxy)]
        match_objects(objects, cars_bb, start_idx, nbcars, Car)
        start_idx += nbcars
    
    start_idx = 13
    aligators_bb = []
    # Detect Log and Alligator    
    for nblogs, (miny, maxy) in zip(logs_per_line, logs_lane_limits):
        logs_bb = find_objects(obs, objects_colors["log"], closing_active=True, minx=8, maxx=152, miny=miny, maxy=maxy)
        for bb in logs_bb:
            if not (obs[bb[1]][bb[0]] == [105, 105, 15]).all(): # check if it is an alligator
                aligators_bb.append(bb)
                logs_bb.remove(bb)
        match_objects(objects, logs_bb, start_idx, nblogs, Log)
        start_idx += nblogs
    
    start_idx = 21
    if aligators_bb:
        match_objects(objects, aligators_bb, start_idx, 2, Alligator)

    start_idx = 23
    # Detect Turtle
    for nbturtles, (miny, maxy) in zip(turtles_per_line, turtles_lane_limits):
        turtles_bb = []
        for color in objects_colors["turtle"]:
            turtles_bb += [list(bb) + [color] for bb in find_objects(obs, color, miny=miny, maxy=maxy)]
        match_objects(objects, turtles_bb, start_idx, nbturtles, Turtle)
        start_idx += nbturtles

        
    # # Detect Diving Turtle
    # turtles = find_objects(obs, objects_colors["diving turtle"], size=(7,8), maxy = 100)
    # for turtle in turtles:
    #     objects.append(DivingTurtle(*turtle))
             
    # #Detect lady frog
    # ladys = find_objects(obs, objects_colors["lady frog"], maxy= 100, size =(8,11))
    # for lady in ladys:
    #     objects.append(LadyFrog(*lady))
         
    # #Snakes    
    # snakes = find_objects(obs, objects_colors["snake"], maxy= 110, minx=8, maxx=152, size=(16,5), tol_s = 2)
    # for snake in snakes:
    #     objects.append(Snake(*snake))

    # #Detect happy frog
    # happys = find_objects(obs, objects_colors["happy frog"], maxy= 26, miny =14, minx=8, maxx=152, size=(8,10), tol_s = 2)
    # for happy in happys:
    #     objects.append(HappyFrog(*happy))
    
            
    # #Detect Alligator's Head
    # alligators = find_objects(obs, objects_colors["alligator's head"], maxy= 30, size =(8,10), tol_s= 0)      
    # for alli in alligators:
    #     objects.append(AlligatorHead(*alli))
   
    # # Detect fly
    # flys = find_objects(obs, objects_colors["fly"], maxy= 30, size =(8,11), tol_s= 0, )
    # for fly in flys:
    #     objects.append(Fly(*fly))
   
    # # Detect cars        
    # cars = []
    # for color in cars_colors.values():
    #     cars += find_objects(obs, color, miny = 110, maxy = 170, minx = 8, maxx = 152)
    # for car in cars:
    #     objects.append(Car(*car))    
    
    # # HUD elements: Score, Lives and Time
    # if hud:
    #     score = find_objects(obs, objects_colors["score"], miny=0, maxy=20, closing_dist = 10)
    #     for s in score:
    #         objects.append(Score(*s))
        
        
    #     lives = find_objects(obs, objects_colors["lives"], miny= 180, maxy=200)
    #     for l in lives:
    #         objects.append(Lives(*l))
        
    #     time =[]
    #     for color in objects_colors["time"]:                
    #         time += find_objects(obs, color, miny=180, maxy=200, minx =120, maxx=190)
    #     for t in time:
    #         objects.append(Time(*t))