from .utils import find_objects, find_mc_objects, find_objects_in_color_range, match_objects
from .game_objects import GameObject,  NoObject

objects_colors = {
                "Kop": [[220,175,111],[25,63,137]], "Krook": [[220,175,111],[43,43,43]], "Ball": [[137,26,53],[160,50,82],[182,72,110]],
                "Security System": [[50,152,82],[207,175,92],[171,135,50]], "Elevator":[[72,164,164],[52,0,128]] ,
                "Moneybag":[[128,88,0],[171,135,50]], "Suitcase":[[128,88,0]], "Escalator":[52,0,128],"Shopping carts":[[210,210,210],[0,0,0]],
                "Biplane":[238,209,128],"Radio":[[[52,0,128],[236,236,236]],[[210,210,210],[52,0,128]]],
                "Timer":[[0,0,0],[236,236,236]], "Score":[236,236,236], "Bonus Kops":[0,0,0]
                    }
# objects_colors = {
#                 "Kop": [[220,175,111],[25,63,137]], "Ball": [[137,26,53],[160,50,82],[182,72,110]],"Krook": [[220,175,111],[43,43,43]],
#                 "Security System": [[0,0,0],[50,152,82],[207,175,92],[171,135,50],[236,236,236]], "Elevator":[[72,164,164],[52,0,128]] ,"Moneybag":[[128,88,0],[171,135,50]],
#                 "Suitcase":[[128,88,0]], "Escalator":[52,0,128],"Shopping carts":[[210,210,210],[0,0,0]],"Biplane":[238,209,128],"Radio":[[[52,0,128],[236,236,236]],[[210,210,210],[52,0,128]]],
#                 "Timer":[[0,0,0],[236,236,236]], "Score":[236,236,236], "Bonus Kops":[0,0,0]
#                     }
floors =[[91,116], [123,148],[155,180]]
elevators_per_line = [1,1,1]
class Kop(GameObject):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.rgb = 220,175,111
        #self.xywh+=(0,-5,0,5)

class Krook(GameObject):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.rgb = 210,210,210
        #self.xywh+=(0,-1,0,1)

class Ball(GameObject):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.rgb = 172,84,108

class Suitcase(GameObject):
    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)
        self.rgb = 128,88,0
        #self.xywh += (0,-9,0,9)
        
class Moneybag(GameObject):
    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)
        self.rgb = 128,88,0
        #self.xywh += (-1,-3,2,3)

class Elevator(GameObject):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.rgb = 72,164,164
        self.is_open = False
        
class Escalator(GameObject):
     def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.rgb = 52,0,128

class Cart(GameObject):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.rgb = 210,210,210
        
class SecuritySystem(GameObject):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.rgb = 50,152,82

class Radio(GameObject):
     def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.rgb = 236,236,236

class Biplane(GameObject):
     def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.rgb = 238,209,128
        # self.h+=4
        # self.y-=1

        
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
    #objects.clear()
    
    player = objects[0]
    player_bb = find_mc_objects(obs, objects_colors["Kop"], size=(6, 20), tol_s =9)
    if player_bb:
        player.xywh = tuple(a + b for a, b in zip(player_bb[0], (0,-5,0,5)))
    
    start_idx = 1
    
    thief_bb = find_mc_objects(obs, objects_colors["Krook"], size =(7, 20), closing_dist= 2)
    if thief_bb:  
        thief_bb[0] = tuple(a + b for a, b in zip(thief_bb[0], (0,-1,0,1)))
        objects[start_idx] = Krook(*thief_bb[0])
    else:
        objects[start_idx] = NoObject()
    #match_objects(objects, thief_bb, start_idx, 1, Krook)
    
    start_idx+=1

    balls_bb = [bb for bb in find_mc_objects(obs, objects_colors["Ball"], size= (6,6), tol_s = 1)]
    match_objects(objects, balls_bb, start_idx, 1, Ball) 
    start_idx+=1
    
    bags_bb = [bb for bb in find_mc_objects(obs,objects_colors["Moneybag"], closing_dist=8, size=(7,12), tol_s=3)]
    if bags_bb:
        for i in range(len(bags_bb)):
            bags_bb[i] = tuple(a + b for a, b in zip(bags_bb[i], (-1,-3,2,3)))
    match_objects(objects, bags_bb, start_idx, 2, Moneybag) 
    start_idx+=2
    
    suitcases_bb = [bb for bb in find_mc_objects(obs,objects_colors["Suitcase"], size=(8,1),tol_s=0)]
    if suitcases_bb:
        for i in range(len(suitcases_bb)):
            suitcases_bb[i] = tuple(a + b for a, b in zip(suitcases_bb[i], (0,-9,0,9)))
    match_objects(objects, suitcases_bb, start_idx, 2, Suitcase) 
    start_idx+=1
    
    # #Issue: Open property?
    # for (miny, maxy) in floors:
    #     elv_bb = []
    #     for color in objects_colors["Elevator"]:
    #         elv_bb += [list(bb) + [color] for bb in find_objects(obs,color, size=(8,23), tol_s = 2, miny= miny, maxy= maxy)]
    #     match_objects(objects, elv_bb, start_idx, 1, Elevator)        
    #     start_idx += 1
    #     print(elv_bb)
    
    #with open property
    for (min_y,max_y) in floors:
        elvs_bb=[]
        for color in objects_colors["Elevator"]:
            elvs_bb += [bb for bb in find_objects(obs,color, size=(8,23), tol_s = 2, miny = min_y, maxy= max_y)]
        if elvs_bb:
            for el in elvs_bb:
                new_Elevator = Elevator(*el)
                if new_Elevator.rgb== [72,164,164]:
                    new_Elevator.is_open = True
                objects[start_idx] = new_Elevator
        else:
            objects[start_idx]=NoObject()
        start_idx+=1
    
    escalators_bb = [bb for bb in find_objects(obs,objects_colors["Escalator"], closing_dist=8, size =(47,40) , tol_s = 0)]
    match_objects(objects, escalators_bb,start_idx, 2, Escalator)
    start_idx+=2

    security_bb = find_mc_objects(obs,objects_colors["Security System"], size = (80, 13), tol_s = 2)
    if security_bb:
        objects[start_idx] = SecuritySystem(*security_bb[0])
    else:
        objects[start_idx] = NoObject()
    start_idx+=1
    
    radios_bb = []
    for color in objects_colors["Radio"]:    
        radios_bb += find_mc_objects(obs,color,size =(8,12), tol_s=2, closing_dist=4)
    match_objects(objects, radios_bb,start_idx, 4, Radio)
    start_idx +=4
    
    #Why cart does not fix
    shoppingcarts = find_mc_objects(obs,objects_colors["Shopping carts"], size = (8,10), tol_s = 0)
    for el in shoppingcarts:
            objects.append(Cart(*el))
    start_idx+=3
    
    biplanes_bb = find_objects(obs,objects_colors["Biplane"], size =(8,5), tol_s=1)
    if biplanes_bb:
        for i in range(len(biplanes_bb)):
            biplanes_bb[i] = tuple(a + b for a, b in zip(biplanes_bb[i], (0,-1,0,4)))
    match_objects(objects, biplanes_bb, start_idx, 2, Biplane) 
    start_idx+=2
            
    
'''      
    shoppingcarts = find_mc_objects(obs,objects_colors["Shopping carts"], size = (8,10), tol_s = 0)
    for el in shoppingcarts:
            objects.append(Cart(*el))
            
            
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
        
    
    '''
