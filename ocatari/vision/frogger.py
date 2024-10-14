from .utils import find_objects
from .game_objects import GameObject

objects_colors = {"frog": [[110, 156, 66],[162,162,42]], "log": [105,105,15], "turtle": [144,72,17] ,"diving turtle" :[66,114,194],
                  "lady frog":[236,236,236], "alligator":[105,105,15], "snake":[82,126,45], "happy frog":[82,126,45], 
                  "alligator's head":[110,156,66], "fly": [110,156,66], 
                  "score": [195,144,61],"lives": [236,236,236], "time": [[0,0,0],[144,72,17]]}

cars_colors = {"car1": [195, 144, 61],"car2": [164,89,208],"car3": [82,126,45],
              "car4": [198,89,179],"car5": [236,236,236]}

class Frog(GameObject):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.rgb = 110, 156, 66
        
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
    objects.clear()
    
    # Detect Frog 
    frogs = []
    for color in objects_colors["frog"]:
        frogs += find_objects(obs, color, miny = 30)
    for frog in frogs:
        objects.append(Frog(*frog))
     
    # Detect Log and Alligator    
    logs = find_objects(obs, objects_colors["log"]) 
    for log in logs:
        if (obs[log[1]][log[0]] == [105,105,15]).all():
            objects.append(Log(*log))
        else:
            objects.append(Alligator(*log))

    # Detect Turtle
    turtles = find_objects(obs, objects_colors["turtle"], size=(7,8), maxy = 100)
    for turtle in turtles:
        objects.append(Turtle(*turtle))
        
    # Detect Diving Turtle
    turtles = find_objects(obs, objects_colors["diving turtle"], size=(7,8), maxy = 100)
    for turtle in turtles:
        objects.append(DivingTurtle(*turtle))
             
    #Detect lady frog
    ladys = find_objects(obs, objects_colors["lady frog"], maxy= 100, size =(8,11))
    for lady in ladys:
        objects.append(LadyFrog(*lady))
         
    #Snakes    
    snakes = find_objects(obs, objects_colors["snake"], maxy= 110, minx=8, maxx=152, size=(16,5), tol_s = 2)
    for snake in snakes:
        objects.append(Snake(*snake))

    #Detect happy frog
    happys = find_objects(obs, objects_colors["happy frog"], maxy= 26, miny =14, minx=8, maxx=152, size=(8,10), tol_s = 2)
    for happy in happys:
        objects.append(HappyFrog(*happy))
    
            
    #Detect Alligator's Head
    alligators = find_objects(obs, objects_colors["alligator's head"], maxy= 30, size =(8,10), tol_s= 0)      
    for alli in alligators:
        objects.append(AlligatorHead(*alli))
   
    # Detect fly
    flys = find_objects(obs, objects_colors["fly"], maxy= 30, size =(8,11), tol_s= 0, )
    for fly in flys:
        objects.append(Fly(*fly))
   
    # Detect cars        
    cars = []
    for color in cars_colors.values():
        cars += find_objects(obs, color, miny = 110, maxy = 170, minx = 8, maxx = 152)
    for car in cars:
        objects.append(Car(*car))    
    
    # HUD elements: Score, Lives and Time
    if hud:
        score = find_objects(obs, objects_colors["score"], miny=0, maxy=20, closing_dist = 10)
        for s in score:
            objects.append(Score(*s))
        
        
        lives = find_objects(obs, objects_colors["lives"], miny= 180, maxy=200)
        for l in lives:
            objects.append(Lives(*l))
        
        time =[]
        for color in objects_colors["time"]:                
            time += find_objects(obs, color, miny=180, maxy=200, minx =120, maxx=190)
        for t in time:
            objects.append(Time(*t))