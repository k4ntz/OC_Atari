from .game_objects import GameObject, ValueObject
import sys 

MAX_NB_OBJECTS = {"Player": 1, "Window": 72, "Enemy_Red": 1, "Enemy_Bird": 1, "Projectile": 1, "Helicopter": 1}
MAX_NB_OBJECTS_HUD = {}# 'Score': 1}

class Player(GameObject):
    def __init__(self):
        super(Player, self).__init__()
        self._xy = 0, 160
        self.wh = (12, 21)
        self.rgb = 111, 210, 111
        self.hud = False


class Window(GameObject):
    def __init__(self):
        super(Window, self).__init__()
        self._xy = 0, 0
        self.wh = (8, 8)
        self.rgb = 255, 255, 255
        # self.rgb = 0, 0, 0
        self.hud = False


class Enemy_Red(GameObject):
    def __init__(self):
        super(Enemy_Red, self).__init__()
        self._xy = 0, 0
        self.wh = (8, 8)
        self.rgb = 200, 72, 72
        self.hud = False

class Enemy_Bird(GameObject):
    def __init__(self):
        super(Enemy_Bird, self).__init__()
        self._xy = 0, 0
        self.wh = (8, 8)
        self.rgb = 214, 214, 214
        self.hud = False
        self.orientation = 1


class Yellow_Projectile(GameObject):
    def __init__(self):
        super(Yellow_Projectile, self).__init__()
        self._xy = 0, 0
        self.wh = (6, 12)
        self.rgb = 210, 210, 64
        self.hud = False

class Purple_Projectile(GameObject):
    def __init__(self):
        super(Purple_Projectile, self).__init__()
        self._xy = 0, 0
        self.wh = (4, 12)
        self.rgb = 181, 108, 224
        self.hud = False

class Blue_Projectile(GameObject):
    def __init__(self):
        super(Blue_Projectile, self).__init__()
        self._xy = 0, 0
        self.wh = (6, 12)
        self.rgb = 101, 160, 225
        self.hud = False


class Yellow_Ball(GameObject):
    def __init__(self):
        super(Yellow_Ball, self).__init__()
        self._xy = 0, 0
        self.wh = (8, 8)
        self.rgb = 210, 210, 64
        self.hud = False


class Helicopter(GameObject):
    def __init__(self):
        super(Helicopter, self).__init__()
        self._xy = 0, 0
        self.wh = (30, 26)
        self.rgb = 66, 72, 200
        self.hud = False
        self.orientation = 1


class Score(ValueObject):
    def __init__(self):
        super(Score, self).__init__()
        self._xy = 49, 21
        self.wh = (47, 17) #37,95
        self.rgb = 111, 210, 111
        self.hud = False


class Life(GameObject):
    def __init__(self):
        super(Life, self).__init__()
        self._xy = 58, 13
        self.wh = (5, 6)
        self.rgb = 72, 160, 72
        self.hud = False


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

    objects.extend([None] * 150)
    if hud:
        objects.extend([None] * 4)
        objects[76] = Score()
    return objects


def _detect_objects_ram(objects, ram_state, hud=False):
    """
    For all 3 objects:
    (x, y, w, h, r, g, b)
    """
    player = objects[0]

    # 19 left pull progress, 21 right pull progression
    if ram_state[19] == 124 or ram_state[21] == 124:
        player.xy = ram_state[24]-8, 158
        player.wh = 12, 23
    else:
        player.xy = ram_state[24]-8, 160

    # 95-102 window closing progress 0 == open 2-7 progress
    # 108-115 closing window constellation: 0 == 101101; 2 == 010010; 8 == 10 01; 10 == 01 10; 4 == 1001; 6 == 0110
    # 46-57 window constellation 0 == full

    for i in range(12):
        for j in range(6):
            if ram_state[46+i] == 4 and 0 < j < 5:
                win = Window()
                objects[1+(6*i)+j] = win

                # Window closing constellation
                if 2 <= i < 10 and ram_state[108+i-2] == 4 and j  in [1, 4]:
                    closing = ram_state[95+i-2]
                elif 2 <= i < 10 and ram_state[108+i-2] == 6 and j not in [1, 4]:
                    closing = ram_state[95+i-2]
                else:
                    closing = 0

                # Window position
                if j < 3:
                    win.xy = 44+(12*j), 47+(13*i)+closing+ram_state[58]
                    win.wh = 8, 8-closing
                else:
                    win.xy = 48+(12*j), 47+(13*i)+closing+ram_state[58]
                    win.wh = 8, 8-closing

            elif ram_state[46+i] == 8 and (j < 2 or j > 3):
                win = Window()
                objects[1+(6*i)+j] = win

                # Window closing constellation
                if 2 <= i < 10 and ram_state[108+i-2] == 8 and j not in [1, 4]:
                    closing = ram_state[95+i-2]
                elif 2 <= i < 10 and ram_state[108+i-2] == 10 and j in [1, 4]:
                    closing = ram_state[95+i-2]
                else:
                    closing = 0
                
                # Window position
                if j < 3:
                    win.xy = 44+(12*j), 47+(13*i)+closing+ram_state[58]
                    win.wh = 8, 8-closing
                else:
                    win.xy = 48+(12*j), 47+(13*i)+closing+ram_state[58]
                    win.wh = 8, 8-closing

            elif (ram_state[46+i] == 12 or ram_state[46+i] == 16) and 1 < j < 4:
                win = Window()
                objects[1+(6*i)+j] = win

                # Window closing constellation
                if 2 <= i < 10 and ram_state[108+i-2] == 12 or ram_state[108+i-2] == 14 or ram_state[108+i-2] == 16 or ram_state[108+i-2] == 18:
                    closing = ram_state[95+i-2]
                else:
                    closing = 0
                
                # Window position
                if j < 3:
                    win.xy = 44+(12*j), 47+(13*i)+closing+ram_state[58]
                    win.wh = 8, 8-closing
                else:
                    win.xy = 48+(12*j), 47+(13*i)+closing+ram_state[58]
                    win.wh = 8, 8-closing

            elif not ram_state[46+i]:
                win = Window()
                objects[1+(6*i)+j] = win

                # Window closing constellation
                if 2 <= i < 10 and ram_state[108+i-2] == 0 and j not in [1, 4]:
                    closing = ram_state[95+i-2]
                elif 2 <= i < 10 and ram_state[108+i-2] == 2 and j in [1, 4]:
                    closing = ram_state[95+i-2]
                else:
                    closing = 0
                
                # Window position
                if j < 3:
                    win.xy = 44+(12*j), 47+(13*i)+closing+ram_state[58]
                    win.wh = 8, 8-closing
                else:
                    win.xy = 48+(12*j), 47+(13*i)+closing+ram_state[58]
                    win.wh = 8, 8-closing
                
            else:
                objects[1+(6*i)+j] = None
    
    # enemy xy == 14,15; closing/offset == 16
    # Enemy type == 84; bird == 252; red == 253
    # bird turn == 74; 1 -> right, 8 -> left

    if ram_state[16] and ram_state[14]:
        if ram_state[84] == 253:
            enemy = Enemy_Red()
            if ram_state[14] < 6:
                enemy.xy = 45+(12*(ram_state[14]-3)), 81+(13*ram_state[15])-ram_state[16]+ram_state[58]
                enemy.wh = 8, ram_state[16]
            elif ram_state[14] == 7:
                enemy.xy = 49+(12*(ram_state[14]-2)), 81+(13*ram_state[15])-ram_state[16]+ram_state[58]
                enemy.wh = 8, ram_state[16]
            else:
                enemy.xy = 49+(12*(ram_state[14]-3)), 81+(13*ram_state[15])-ram_state[16]+ram_state[58]
                enemy.wh = 8, ram_state[16]
        elif ram_state[84] == 252:
            if type(objects[73]) == Enemy_Bird:
                enemy = objects[73]
            else:
                enemy = Enemy_Bird()
            if ram_state[74] > ram_state[75]:
                enemy.orientation = 1
            elif ram_state[74] < ram_state[75]:
                enemy.orientation = 0
            if enemy.orientation:
                enemy.xy = ram_state[34]-9, 49
            else:
                enemy.xy = ram_state[34]-19, 49
            enemy.wh = 16, 8
        else:
            enemy = None
        objects[73] = enemy
    else:
        objects[73] = None
    
    # projectile xy == 14,81; closing/offset == 16
    # projectile color == 83; purple == 219; blue == 229; yellow == 239
    # yellow ball == 145;
    # 85 == x of ball

    if ram_state[81]:
        x = ram_state[85]-10
        if ram_state[83] == 239:
            projectile = Yellow_Projectile()
        elif ram_state[83] == 229:
            projectile = Blue_Projectile()
            x+=1
        elif ram_state[83] == 219:
            projectile = Purple_Projectile()
            x+=2
        elif ram_state[83] == 145:
            projectile = Yellow_Ball()
        else:
            projectile = None
        objects[74] = projectile
        if ram_state[83] == 145:
            projectile.xy = x, 42 + int(ram_state[81]*1.2) # (49 + int(ram_state[81]*1.1))
        elif projectile is not None:
            projectile.xy = x, 35 + int(ram_state[81]*1.2)# int((ram_state[82] - ram_state[81])/5)
    else:
        objects[74] = None

    # heli xy == 34, 9

    if ram_state[9] >  50:
        if objects[75] is None:
            heli = Helicopter()
            objects[75] = heli
        else:
            heli = objects[75]
        if ram_state[34] <= 30:
            heli.orientation = 1
        elif ram_state[34] >= 120:
            heli.orientation = 0
        if heli.orientation:
            heli.xy = ram_state[34]-9, ram_state[9]+11
        else:
            heli.xy = ram_state[34]-23, ram_state[9]+11

    else:
        objects[75] = None

    if hud:
        for i in range(3):
            objects[77+i] = None
            if ram_state[42] > i:
                life = Life()
                objects[77+i] = life
                life.xy = 58 + (i*16), 13 #74
