from .game_objects import GameObject, ValueObject
import sys 

"""
RAM extraction for the game Yars' Revenge.
"""

MAX_NB_OBJECTS = {"Player": 1}
MAX_NB_OBJECTS_HUD = {}# 'Score': 1}

class Player(GameObject):
    def __init__(self):
        super(Player, self).__init__()
        self._xy = 76, 100
        self.wh = (14, 10)
        self.rgb = 213, 130, 74
        self.hud = False

class Player_Shot(GameObject):
    def __init__(self):
        super(Player_Shot, self).__init__()
        self._xy = 76, 100
        self.wh = (16, 16)
        self.rgb = 213, 130, 74
        self.hud = False

class Player_Shadow(GameObject):
    def __init__(self):
        super(Player_Shadow, self).__init__()
        self._xy = 76, 176
        self.wh = (14, 10)
        self.rgb = 0, 0, 0
        self.hud = False

class Hostile_Fighter(GameObject):
    def __init__(self):
        super(Hostile_Fighter, self).__init__()
        self._xy = 76, 100
        self.wh = (16, 10)
        self.rgb = 72, 160, 72
        self.hud = False

class Hostile_Orange(GameObject):
    def __init__(self):
        super(Hostile_Orange, self).__init__()
        self._xy = 76, 100
        self.wh = (10, 16)
        self.rgb = 213, 130, 74
        self.hud = False

class Hostile_Shot(GameObject):
    def __init__(self):
        super(Hostile_Fighter, self).__init__()
        self._xy = 76, 100
        self.wh = (16, 16)
        self.rgb = 210, 164, 74
        self.hud = False

class Tower(GameObject):
    def __init__(self):
        super(Tower, self).__init__()
        self._xy = 76, 100
        self.wh = (16, 24)
        self.rgb = 146, 70, 192
        self.hud = False

class Fuel_Tank(GameObject):
    def __init__(self):
        super(Fuel_Tank, self).__init__()
        self._xy = 76, 100
        self.wh = (16, 24)
        self.rgb = 110, 156, 66
        self.hud = False

class Sentry(GameObject):
    def __init__(self):
        super(Sentry, self).__init__()
        self._xy = 76, 100
        self.wh = (16, 22)
        self.rgb = 162, 162, 42
        self.hud = False

class Satellite(GameObject):
    def __init__(self):
        super(Satellite, self).__init__()
        self._xy = 76, 100
        self.wh = (16, 16)
        self.rgb = 184, 50, 50
        self.hud = False

class Zaxxon(GameObject):
    def __init__(self):
        super(Zaxxon, self).__init__()
        self._xy = 76, 100
        self.wh = (16, 16)
        self.rgb = 136, 146, 62
        self.hud = False

class Wall(GameObject):
    def __init__(self):
        super(Wall, self).__init__()
        self._xy = 76, 100
        self.wh = (16, 16)
        self.rgb = 162, 98, 33
        self.hud = False


class Score(GameObject):
    def __init__(self):
        super(Score, self).__init__()
        self._xy = 52, 10
        self.wh = (46, 8)
        self.rgb = 198, 108, 58
        self.hud = True

class Life(GameObject):
    def __init__(self):
        super(Life, self).__init__()
        self._xy = 52, 196
        self.wh = (6, 8)
        self.rgb = 162, 162, 42
        self.hud = True

class Fuel(GameObject):
    def __init__(self):
        super(Fuel, self).__init__()
        self._xy = 58, 196
        self.wh = (16, 7)
        self.rgb = 162, 162, 42
        self.hud = True

class Altitude(GameObject):
    def __init__(self):
        super(Altitude, self).__init__()
        self._xy = 8, 123
        self.wh = (4, 6)
        self.rgb = 24, 59, 157
        self.hud = True

# parses MAX_NB* dicts, returns default init list of objects
def _get_max_objects(hud=False):

    def fromdict(max_obj_dict):
        objects = []
        mod = sys.modules[__name__]
        for k, v in max_obj_dict.items():
            for _ in range(0, v):
                objects.append(getattr(mod, k)())    
        return objects

    if hud:
        return fromdict(MAX_NB_OBJECTS_HUD)
    return fromdict(MAX_NB_OBJECTS)


def _init_objects_ram(hud=False):
    """
    (Re)Initialize the objects
    """
    objects = [Player()]

    objects.extend([None] * 135)
    if hud:
        objects.extend([Score(), Life(), Fuel(), Altitude()])
    return objects


def _detect_objects_ram(objects, ram_state, hud=False):
    """
    For all 3 objects:
    (x, y, w, h, r, g, b)
    """

    # x, y = r32, r33
    # player sprite == r102
    player = objects[0]
    if ram_state[102] == 176:
        player.xy = (ram_state[32]>>1) + 11, 193 - ram_state[33]*2
        player.wh = 14, 10
    elif ram_state[102] == 200 or ram_state[102] == 208 or ram_state[102] == 192:
        player.xy = (ram_state[32]>>1) + 11, 193 - ram_state[33]*2 - 2
        player.wh = 14, 12
    elif ram_state[102] == 184:
        player.xy = (ram_state[32]>>1) + 11, 193 - ram_state[33]*2 - 4
        player.wh = 14, 16

    # Enemy x, y == 25-31, 
    # Enemy types == r70-76
        # 17 == fuel
        # 49 == tower
        # 65 == orange
        # 81 == sentry
        # 113 == figher
        # 145, 161 == zaxxon
    # the smaller the ram position, the closer the enemy
        # from r73-r69 bigger sprites
    for i in range(7):
        ob = None
        if ram_state[31-i] >= 229:
            x1 = 46 + (ram_state[31-i]>>2) + (ram_state[11]>>1)
        else:
            x1 = 46 + (ram_state[31-i]>>2)
        # if ram_state[31-i] >= 229:
        #     x2 = 19 + (ram_state[31-i]>>1) + (ram_state[11]>>1))
        # else:
        # if ram_state[31-i] < 50:
        #     x2 = 46 + (ram_state[31-i]>>2) - (ram_state[11]) - (i-3)*6 - (ram_state[31-i]>>5)
        # elif ram_state[31-i] < 85:
        #     x2 = 46 + (ram_state[31-i]>>2) - (ram_state[11]>>2) - (i-3)*3 - (ram_state[31-i]>>5)
        #     # x2 = 36 + (ram_state[31-i]>>1) -  (ram_state[31-i]>>5) - (i-3)*6 - (ram_state[11]>>1)) - 1
        # elif ram_state[31-i] < 105:
        #     x2 = 46 + (ram_state[31-i]>>2) - (ram_state[11]>>2) - (i-3)*2 + 1
        # elif ram_state[31-i] < 135:
        x2 = 46 + (ram_state[31-i]>>2)
        # if x2-70 < 0:
        #     x2 = int(70 + (x2 - 70) - ((i-1)**2 - ram_state[11])*((x2 - 70)/50))
        # else:
        #     x2 = int(70 + (x2 - 70) + ((i-1)**2 + ram_state[11])*((x2 - 70)/50))
        x2 += int(((i-1)**2 + ram_state[11])*((x2 - 75)/27))
        # elif ram_state[31-i] < 175:
        #     x2 = 46 + (ram_state[31-i]>>2) + (ram_state[11]>>2) + (i-3)*2 + 2
        # elif ram_state[31-i] < 200:
        #     x2 = 46 + (ram_state[31-i]>>2) + (ram_state[11]>>2) + (i-3)*3 + (ram_state[31-i]>>5)
        # else:
        #     x2 = 46 + (ram_state[31-i]>>2) + (ram_state[11]) + (i-3)*6 + (ram_state[31-i]>>5)
            # x2 = 19 + (ram_state[31-i]>>1) -  (ram_state[31-i]>>5)
        
        # x2 = ram_state[31-i]-123 + ram_state[11] + (i-3)*7
        # if ram_state[31-i] > 250:
        #     x2 = (ram_state[31-i]>>1)  + ram_state[11] + (i-3)*7
        # elif ram_state[31-i] < 50:
        #     x2 = (ram_state[31-i]>>1)  - ram_state[11] - (i-3)*7 + 35
        # else:
        #     x2 = (ram_state[31-i]>>1) + 10
        y1 = 30 + ram_state[11]*2 + 16*(i-1) - 2
        y2 = ram_state[11]*4 + 32*(i-1) - 2
        
        # adjust width and hight of objects

        if ram_state[92-i] > 16:
            if ram_state[76-i] == 1:
                objects[i+1] = None
                continue
            elif ram_state[76-i] == 17:
                ob =  Fuel_Tank()
                if i < 3:
                    ob.wh = 8, 12
                y2-=2
            elif ram_state[76-i] == 33:
                ob =  Satellite()
                if i < 3:
                    ob.wh = 8, 12
            elif ram_state[76-i] == 49:
                ob =  Tower()
                if i < 3:
                    ob.wh = 8, 12
            elif ram_state[76-i] == 65 or ram_state[76-i] == 177:
                ob =  Hostile_Orange()
                if i < 3:
                    x1+= 4
                    ob.wh = 5, 8
                else:
                    x2+= 3
            elif ram_state[76-i] == 81:
                ob =  Sentry()
                if i < 3:
                    ob.wh = 8, 12
            elif ram_state[76-i] == 113:
                ob =  Hostile_Fighter()
                if i < 3:
                    ob.wh = 8, 5
                else:
                    y2-=2
            elif ram_state[76-i] == 145 or ram_state[76-i] == 161:
                ob =  Hostile_Orange()
                if i < 3:
                    x1+= 4
                    ob.wh = 5, 8
                else:
                    x2+= 3
        else:
            if ram_state[76-i] == 1:
                objects[i+1] = None
                continue
            else:
                ob =  Hostile_Fighter()
                if i < 3:
                    ob.wh = 8, 6
                    y1+=4 
                else:
                    y2+=6
                
        # print(76-i, 31-i, 40-i)
        objects[i+1] = ob
        if ob is not None:
            if i < 3:
                ob.xy = x1, y1
            else:
                ob.xy = x2, y2
        
    # background == 92-78
    # color == 68-54
    # range == 14
    # size 17 == 48, 18 == 56, 19 == 64
    # center == 80
    for i in range(14):
        # get all orange background panels
        if ram_state[68-i] == 37:
            wall = Wall()
            objects[9+i] = wall
            k = i
            state = ram_state[92-i]
            # Panel with hole on top
            if 40 < state < 55:
                state = ram_state[92-i-1]
            elif 77 < state < 95:
                state = state - 60
            # full wall panel
            if 28 <= state < 41:
                x = 16
                w = 128
            # middle wall panel
            elif 61 <= state < 77:
                x = 68 - ((state-62)*2) - 2
                w = ((state-56)*4) + 4 # 24 + ((state-62)*4)
            # elif 68 <= state < 80:
            #     x = 48
            #     w = 64
            else:
                # full wall panel
                x = 80 - ((state-11)*4)
                w = ((state-11)*8)
            #the previous tiles hight
            ph = 0
            # looping to through all currently displayed wall tiles
            while(ram_state[68-k] == 37):
                y=0
                h=0
                if ram_state[11] < 4:
                    j = i+1
                else:
                    j = i
                # middle wall hights and y positions
                if state >= 72 and state < 80:
                    y = 16*j + ram_state[11]*4 - 53
                    h = 16
                elif state >= 68:
                    y = 16*j + ram_state[11]*4 - 53
                    h = 16
                elif state >= 67:
                    y = 16*j + ram_state[11]*2 - 39
                    h = 8 + ram_state[11]
                elif state >= 66:
                    y = 16*j + ram_state[11]*2 - 23
                    h = 8
                elif state == 65:
                    y = (10+ram_state[11])*j - ram_state[11]*2 # - ram_state[11]*4
                    h = 8
                elif state == 64:
                    y = (10+ram_state[11])*j + ram_state[11] # *2 - ram_state[11]
                    h = 8
                elif state == 63:
                    y = (10+ram_state[11])*j + ram_state[11]*2 # - 3 - ram_state[11]*8
                    h = 8
                elif state == 62:
                    y = 9 + 8*j + ram_state[11]*2
                    h = 8
                elif state == 61:
                    y = 9 + 8*j + ram_state[11]*2
                    h = 8
                # full wall hights and y positions
                elif state >= 32 and state < 40:
                    wall.xy = 80 - ((state-11)*4), 9 + 20*j + ram_state[11]*8
                    wall.wh = ((state-11)*8), 14
                elif state >= 28:
                    y = 16*j + ram_state[11]*4 - 53
                    h = 16
                elif state >= 26:
                    y = 16*j + ram_state[11]*4 - 53
                    h = 16
                elif state >= 24:
                    y = (10+ram_state[11])*j + ram_state[11]*4 - 3 - ram_state[11]*8
                    h = 10+ram_state[11]
                elif state == 23:
                    y = 10*j + ram_state[11]*4 - 12
                    h = 10
                else:
                    y = 9 + 8*j + ram_state[11]*2
                    h = 8
                if y < 24:
                    wall.xy = x, 24
                else:
                    wall.xy = x, y
                if y < 24 and k == 0:
                    wall.wh = w, ph + (h-(24-y))
                    ph += (h-(24-y))
                    k += 1
                elif y + ph + h > 193:
                    wall.wh = w, 194 - y
                    break
                else:
                    wall.wh = w, ph + h
                    ph += h
                    k += 1
            break
        else:
            objects[9+i] = None

    if hud:
        # fuel == r8, 38 == 39 
        fuel = objects[-2]
        fuel.wh = ram_state[8] + 1, 7
        # altitude == r33
        al = objects[-1]
        al.xy = 8, 193 - ram_state[33]*2 + 12
        al.wh = 4, ram_state[33]*2 - 12