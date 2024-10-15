from .game_objects import GameObject, NoObject

"""
RAM extraction for the game Frogger.

"""

MAX_NB_OBJECTS = {'Frog': 1, 'Car': 12, 'Log': 8, 'Alligator': 2, 'Turtle': 10}
MAX_NB_OBJECTS_HUD = {'Frog': 1, 'Car': 12, 'Log': 8, 'Alligator': 2, 'Turtle': 10}

class Frog(GameObject):
    """
    The player figure i.e., the frog. 
    """
    
    def __init__(self):
        super(Frog, self).__init__()
        self._xy = 0, 0
        self.wh = 7, 7
        self.rgb = 110, 156, 66
        self.hud = False

class Car(GameObject):
    """
    A car.
    """
    def __init__(self):
        super(Car, self).__init__()
        self._xy = 0, 0
        self.wh = 14, 7
        self.rgb = 195, 144, 61
        self.hud = False


class Log(GameObject):
    def __init__(self):
        super().__init__()
        self.rgb = 105, 105, 15        


class Turtle(GameObject):
    def __init__(self):
        super().__init__()
        self.rgb = 144, 72, 17


class Alligator(GameObject):
    def __init__(self):
        super().__init__()
        self.rgb = 105, 105, 15

# class DivingTurtle(GameObject):
#     def __init__(self, *args, **kwargs):
#         super().__init__(*args, **kwargs)
#         self.rgb = 66,114,194

# class LadyFrog(GameObject):
#     def __init__(self, *args, **kwargs):
#         super().__init__(*args, **kwargs)
#         self.rgb = 236,236,236



# class Snake(GameObject):
#     def __init__(self, *args, **kwargs):
#         super().__init__(*args, **kwargs)
#         self.rgb = 82,126,45   
        
# class HappyFrog(GameObject):
#     def __init__(self, *args, **kwargs):
#         super().__init__(*args, **kwargs)
#         self.rgb = 82,126,45

# class AlligatorHead(GameObject):
#     def __init__(self, *args, **kwargs):
#         super().__init__(*args, **kwargs)
#         self.rgb = 110,156,66

# class Fly(GameObject):
#     def __init__(self, *args, **kwargs):
#         super().__init__(*args, **kwargs)
#         self.rgb = 110,156,66

# class Car(GameObject):
#     def __init__(self, *args, **kwargs):
#         super().__init__(*args, **kwargs)
#         self.rgb = 195, 144, 61

# class Score(GameObject):
#     def __init__(self, *args, **kwargs):
#         super().__init__(*args, **kwargs)
#         self.rgb = 195,144,61
#         self.hud = True

# class Lives(GameObject):
#     def __init__(self, *args, **kwargs):
#         super().__init__(*args, **kwargs)
#         self.rgb = 236,236,236
#         self.hud = True
                
# class Time(GameObject):
#     def __init__(self, *args, **kwargs):
#         super().__init__(*args, **kwargs)
#         self.rgb = 0,0,0
#         self.hud = True

def _init_objects_ram(hud=False):
    """
    (Re)Initialize the objects
    """
    cars = [NoObject()] * 12
    logs = [NoObject()] * 8
    aligators = [NoObject()] * 2
    turtles = [NoObject()] * 10
    return [Frog()] + cars + logs + aligators + turtles

def _detect_objects_ram(objects, ram_state, hud=False):
    """
    For all objects:
    (x, y, w, h, r, g, b)
    """
    frog = objects[0]
    frog.x = ram_state[48] - 1
    if ram_state[44] == 255:
        frog.y = 171
    elif ram_state[44] == 5:
        frog.y = 95
    else:
        frog.y = - 13 * ram_state[44] + 161