from .game_objects import GameObject, NoObject

"""
RAM extraction for the game Keystone Kapers.

"""

MAX_NB_OBJECTS = {'Kop': 1, 'Krook': 1, 'Ball': 1, 'Moneybag': 2, 'Suitcase':2, 'Elevator':3, 'Escalator':2, 'SecuritySystem':1,'Radio': 4, 'Cart': 3, 'Biplane': 2}
MAX_NB_OBJECTS_HUD = {'Kop': 1, 'Krook': 1, 'Ball':1, 'Moneybag': 2, 'Suitcase':2,'Elevator':3, 'Escalator':2, 'SecuritySystem':1 ,'Radio':4, 'Cart': 3, 'Biplane': 2}

class Kop(GameObject):
    """
    The player figure i.e., the Kop. 
    """
    
    def __init__(self):
        super().__init__()
        self.rgb = 220,175,111
        self.hud = False
        # self.wh = 6,20
        # self.y-=5
        # self.h+=5

class Krook(GameObject):
    """
    A thief.
    """
    def __init__(self):
        super().__init__()
        self.rgb = 220,175,11
        self.hud = False
        # self._xy = 0, 0
        # self.wh = 7,20
        # self.y-=1
        # self.h+=1


class Ball(GameObject):
    def __init__(self):
        super().__init__()
        self._xy = 0, 0
        self.wh = 6,6
        self.rgb = 137,26,53     
        
class Moneybag(GameObject):
    def __init__(self):
        super().__init__()
        self.rgb = 128,88,0
        
class Suitcase(GameObject):
    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)
        self.rgb = 128,88,0
        #self.xywh += (0,-9,0,9)

class Elevator(GameObject):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.rgb = 72,164,164
        self.is_open = False
        
class Escalator(GameObject):
     def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.rgb = 52,0,128

class SecuritySystem(GameObject):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.rgb = 0,0,0
        
class Radio(GameObject):
     def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.rgb = 236,236,236
        
class Cart(GameObject):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.rgb = 210,210,210

class Biplane(GameObject):
     def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.rgb = 238,209,128
        self.h+=4
        self.y-=1
        
def _init_objects_ram(hud=False):
    """
    (Re)Initialize the objects
    """
    bags = [NoObject()]*2
    suitcases = [NoObject()]*2
    elevators = [NoObject()]*3
    escalators = [NoObject()]*2
    radios = [NoObject()]*4
    carts = [NoObject()]*3
    biplanes = [NoObject()]*2
    return [Kop()]+ [Krook()]+ [Ball()] + bags + suitcases + elevators + escalators + [SecuritySystem()]+ radios + carts + biplanes

def _detect_objects_ram(objects, ram_state, hud=False):
    pass