from .utils import find_objects, find_mc_objects, find_objects_in_color_range
from .game_objects import GameObject

objects_colors = {
                "Kop": [[220,175,111],[25,63,137]], "Ball": [[137,26,53],[160,50,82],[182,72,110]],"Krook": [[220,175,111],[43,43,43]],
                "Security System": [[0,0,0],[50,152,82],[207,175,92],[171,135,50],[236,236,236]], "Elevator":[[72,164,164],[52,0,128]] ,"Moneybag":[[128,88,0],[171,135,50]],
                "Suitcase":[[128,88,0]], "Escalator":[52,0,128],"Shopping carts":[[210,210,210],[0,0,0]],"Biplane":[238,209,128],"Radio":[[[52,0,128],[236,236,236]],[[210,210,210],[52,0,128]]],
                "Timer":[[0,0,0],[236,236,236]], "Score":[236,236,236], "Bonus Kops":[0,0,0]
                    }

class Kop(GameObject):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.rgb = 220,175,111
        self.y-=5
        self.h+=5

class Cart(GameObject):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.rgb = 210,210,210

class Ball(GameObject):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.rgb = 172,84,108

class Krook(GameObject):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.rgb = 210,210,210
        self.y-=1
        self.h+=1

class Suitcase(GameObject):
    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)
        self.rgb = 128,88,0
        self.h+=9
        self.y-=9
        
class Moneybag(GameObject):
    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)
        self.rgb = 128,88,0
        self.h+=3
        self.y-=3
        self.w+=2
        self.x-=1
        
class SecuritySystem(GameObject):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.rgb = 0,0,0
class Elevator(GameObject):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.rgb = 72,164,164
        self.is_open = False

class Escalator(GameObject):
     def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.rgb = 52,0,128

class Biplane(GameObject):
     def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.rgb = 238,209,128
        self.h+=4
        self.y-=1

class Radio(GameObject):
     def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.rgb = 236,236,236
        
#HUD:
class BonusKops(GameObject):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.rgb = 0, 0, 0
        self.hud = True
        
class Score(GameObject):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.rgb = 236,236,236
        self.hud = True

class Timer(GameObject):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.rgb = 0, 0, 0
        self.hud = True

def _detect_objects(objects, obs, hud=False):
    # detection and filtering
    objects.clear()
    kops = find_mc_objects(obs, objects_colors["Kop"], size=(6, 20), tol_s =9)
    for el in kops:
        objects.append(Kop(*el))
    balls = find_mc_objects(obs, objects_colors["Ball"], size= (6,6), tol_s = 1)
    for el in balls:
        objects.append(Ball(*el))
    thieves = find_mc_objects(obs, objects_colors["Krook"], size =(7, 20), closing_dist= 3)
    for el in thieves:
        objects.append(Krook(*el))
    
    bags = find_mc_objects(obs,objects_colors["Moneybag"], closing_dist=8, size=(7,12), tol_s=3)
    for el in bags:
        objects.append(Moneybag(*el))
    
    suitcases = find_mc_objects(obs,objects_colors["Suitcase"], size=(8,1),tol_s=0)
    for el in suitcases:
        objects.append(Suitcase(*el))
    
    securitysystem = find_mc_objects(obs,objects_colors["Security System"], size = (80, 13), tol_s = 2)
    for el in securitysystem:
            objects.append(SecuritySystem(*el))
            
    elvs=[]
    for color in objects_colors["Elevator"]:
        elvs += find_objects(obs,color, size=(8,23), tol_s = 2)
    for el in elvs:
        new_Elevator = Elevator(*el)
        if new_Elevator.rgb== [72,164,164]:
            new_Elevator.is_open = True
        objects.append(new_Elevator)
            
    escalators = find_objects(obs,objects_colors["Escalator"], closing_dist=8, size =(47,40) , tol_s = 0)
    for el in escalators:
            objects.append(Escalator(*el))
            
    shoppingcarts = find_mc_objects(obs,objects_colors["Shopping carts"], size = (8,10), tol_s = 0)
    for el in shoppingcarts:
            objects.append(Cart(*el))
            
    biplanes = find_objects(obs,objects_colors["Biplane"], size =(8,5), tol_s=1)
    for el in biplanes:
        objects.append(Biplane(*el))
            
    for color in objects_colors["Radio"]:    
        rads = find_mc_objects(obs,color,size =(8,12), tol_s=2, closing_dist=4)
        for el in rads:
                objects.append(Radio(*el))
    if hud:
        score = find_objects(obs,objects_colors["Score"], maxy = 40, maxx=70, closing_dist=5)
        for el in score:
            objects.append(Score(*el))
        bonus = find_objects(obs,objects_colors["Bonus Kops"],minx=10, maxx = 50, miny = 40, maxy = 50)
        for el in bonus:
            objects.append(BonusKops(*el))
        for color in objects_colors["Timer"]:
            timer = find_objects(obs,color,minx=50, maxx = 80, miny = 40, maxy = 50, closing_dist=5)
            for el in timer:
                objects.append(Timer(*el))
        
    
    #print(objects)