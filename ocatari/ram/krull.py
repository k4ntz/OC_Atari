from .game_objects import GameObject, ValueObject
from ._helper_methods import number_to_bitfield
import sys 

MAX_NB_OBJECTS = {"Player": 1}
MAX_NB_OBJECTS_HUD = {}# 'Score': 1}

class Player(GameObject):
    def __init__(self):
        super(Player, self).__init__()
        self._xy = 0, 160
        self.wh = (6, 16)
        self.rgb = 227, 151, 89
        self.hud = False

class Lyssa(GameObject):
    def __init__(self):
        super(Lyssa, self).__init__()
        self._xy = 0, 160
        self.wh = (7, 16)
        self.rgb = 198, 89, 179
        self.hud = False

class Slayers(GameObject):
    def __init__(self):
        super(Slayers, self).__init__()
        self._xy = 0, 160
        self.wh = (6, 16)
        self.rgb = 45, 109, 152
        self.hud = False

class Slayer_Shot(GameObject):
    def __init__(self):
        super(Slayer_Shot, self).__init__()
        self._xy = 0, 160
        self.wh = (1, 6)
        self.rgb = 45, 109, 152
        self.hud = False

class Fire_Mare(GameObject):
    def __init__(self):
        super(Fire_Mare, self).__init__()
        self._xy = 0, 160
        self.wh = (8, 9)
        self.rgb = 213, 130, 74
        self.hud = False

class Spider(GameObject):
    def __init__(self):
        super(Spider, self).__init__()
        self._xy = 0, 160
        self.wh = (8, 12)
        self.rgb = 236, 236, 236
        self.hud = False

class Weapon(GameObject):
    def __init__(self):
        super(Weapon, self).__init__()
        self._xy = 0, 0
        self.wh = (8, 7)
        self.rgb = 92, 186, 92
        self.hud = False


class Enemy_Weapon(GameObject):
    def __init__(self):
        super(Enemy_Weapon, self).__init__()
        self._xy = 0, 0
        self.wh = (4, 8)
        self.rgb = 184, 70, 162
        self.hud = False


class Beast(GameObject):
    def __init__(self):
        super(Beast, self).__init__()
        self._xy = 0, 0
        self.wh = (12, 22)
        self.rgb = 144, 72, 17
        self.hud = False


class Wall(GameObject):
    def __init__(self):
        super(Wall, self).__init__()
        self._xy = 0, 0
        self.wh = (4, 4)
        self.rgb = 162, 98, 33
        self.hud = False


class Window(GameObject):
    def __init__(self):
        super(Window, self).__init__()
        self._xy = 76, 23
        self.wh = (8, 26)
        self.rgb = 142, 142, 142
        self.hud = False


class Line(GameObject):
    def __init__(self):
        super(Line, self).__init__()
        self._xy = 0, 0
        self.wh = (1, 2)
        self.rgb = 142, 142, 142
        self.hud = False


class Star(GameObject):
    def __init__(self):
        super(Star, self).__init__()
        self._xy = 0, 0
        self.wh = (3,4)
        self.rgb = 236, 236, 236
        self.hud = False


class Castle(GameObject):
    def __init__(self):
        super(Castle, self).__init__()
        self._xy = 0, 0
        self.wh = (64, 4)
        self.rgb = 162, 98, 33
        self.hud = False


class Sun(ValueObject):
    def __init__(self):
        super(Sun, self).__init__()
        self._xy = 0, 0
        self.wh = (7, 7)
        self.rgb = 236, 236, 236
        self.hud = True


class Hour_Glass(ValueObject):
    def __init__(self):
        super(Hour_Glass, self).__init__()
        self._xy = 0, 0
        self.wh = (5, 8)
        self.rgb = 214, 92, 92
        self.hud = True


class Score(ValueObject):
    def __init__(self):
        super(Score, self).__init__()
        self._xy = 0, 0
        self.wh = (7, 7)
        self.rgb = 252, 252, 84
        self.hud = True


class Life(GameObject):
    def __init__(self):
        super(Life, self).__init__()
        self._xy = 0, 0
        self.wh = (6, 7)
        self.rgb = 92, 186, 92
        self.hud = True


class Weapon_HUD(GameObject):
    def __init__(self):
        super(Weapon_HUD, self).__init__()
        self._xy = 0, 0
        self.wh = (8, 7)
        self.rgb = 92, 186, 92
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

    objects.extend([None] * 500)
    if hud:
        objects.extend([None] * 4)
    return objects


def _detect_objects_ram(objects, ram_state, hud=False):
    """
    For all 3 objects:
    (x, y, w, h, r, g, b)
    """

    # room == r34; 0 == beginning, 1 == Boss, 2 == spider, 3 == ride

    # player xy == r89, r97
    # after beginning == r90, r98
    player = objects[0]
    room = ram_state[34]
    if room == 0:
        player.wh = 6, 16
        if ram_state[114]:
            player.xy = ram_state[90] + 9, (ram_state[98]*2) + 16
            if ram_state[73] != 80:
                lyssa = Lyssa()
                objects[1] = lyssa
                lyssa.xy = ram_state[89] + 9, (ram_state[97]*2) + 15
            else:
                objects[1] = None
            enemies = 0
            for i in range(5):
                objects[2+i] = None
                if ram_state[99+i] and enemies < ram_state[82] and not (ram_state[73] == 80 and ram_state[91+i] >= 69):
                    enemies += 1
                    slayer = Slayers()
                    objects[2+i] = slayer
                    slayer.xy = ram_state[83+i] + 9, (ram_state[91+i]*2) + 15
                for j in range(3):
                    objects[7+i+j*5] = None
                    if ram_state[99+i]&2**j and objects[2+i] is not None:
                        slayer2 = Slayers()
                        objects[7+i+j*5] = slayer2
                        slayer2.xy = ram_state[83+i] + 9 + (16 * (ram_state[99+i]&2**j)), (ram_state[91+i]*2) + 15
        else:
            player.xy = ram_state[89] + 9, (ram_state[97]*2) + 16
            lyssa = Lyssa()
            objects[1] = lyssa
            lyssa.xy = ram_state[83] + 9, (ram_state[91]*2) + 15
            for i in range(5):
                objects[2+i] = None
                if ram_state[100+i] and ram_state[82] > i:
                    slayer = Slayers()
                    objects[2+i] = slayer
                    slayer.xy = ram_state[84+i] + 9, (ram_state[92+i]*2) + 15
                    for j in range(3):
                        objects[7+i+j*5] = None
                        if ram_state[100+i]&2**j:
                            slayer2 = Slayers()
                            objects[7+i+j*5] = slayer2
                            slayer2.xy = ram_state[84+i] + 9 + (16 * (ram_state[100+i]&2**j)), (ram_state[92+i]*2) + 15
        if ram_state[77]:
            shot = Slayer_Shot()
            objects[22] = shot
            if ram_state[79]&16:
                shot.wh = 7, 7
                if ram_state[79]&128:
                    shot.xy = (ram_state[78] + 7 + ram_state[76]*2) - 32, ram_state[77]*2 + 6
                else:
                    shot.xy = (ram_state[78] + 7 - ram_state[76]*2) + 25, ram_state[77]*2 + 6
            else:
                shot.wh = 1, 7
                shot.xy = ram_state[78] + 7, ram_state[77]*2 + 6
    
    elif room == 1:
        for i in range(len(objects)-1):
            objects[i+1] = None

        player.xy = ram_state[83] + 9, (ram_state[91]*2) + 15
        player.wh = 7, 16

        if ram_state[97] < 80:
            weapon = Weapon()
            objects[1] = weapon
            weapon.rgb = 224, 236, 124
            if ram_state[47] == 24:
                weapon.xy =  ram_state[89] + 11, (ram_state[97]*2) + 16
                weapon.wh = 2, 2
            elif ram_state[47] == 36:
                weapon.xy =  ram_state[89] + 9, (ram_state[97]*2) + 16
                weapon.wh = 6, 6
            else:
                weapon.xy =  ram_state[89] + 8, (ram_state[97]*2) + 16
                weapon.wh = 8, 8
        else:
            objects[1] = None

        boss = Beast()
        objects[2] = boss
        if ram_state[100] == 157:
            boss.xy = ram_state[84] + 13, (ram_state[92]*2) + 15
        else:
            boss.xy = ram_state[84] + 9, (ram_state[92]*2) + 15
        
        if ram_state[77] < 83:
            bossw = Enemy_Weapon()
            objects[3] = bossw
            bossw.xy = ram_state[79] + 7, (ram_state[77]*2) + 7
        else:
            objects[3] = None

        lyssa = Lyssa()
        objects[4] = lyssa
        if ram_state[109] == 42:
            lyssa.xy = ram_state[85] + 9, (ram_state[93]*2) + 15
        else:
            lyssa.xy = ram_state[85] + 8, (ram_state[93]*2) + 15

        for j in range(4):
            for i in range(8):
                if ram_state[115+j*2]&2**i:
                    wall = Wall()
                    objects[5+16*j+i] = wall
                    wall.xy = 48 + 4*i, 39 + 4*j
                else:
                    objects[5+16*j+i] = None
                if ram_state[116+j*2]&2**i:
                    wall = Wall()
                    objects[13+16*j+i] = wall
                    wall.xy = 108 - 4*i, 39 + 4*j
                else:
                    objects[13+16*j+i] = None

    elif room == 2:
        for i in range(len(objects)-1):
            objects[i+1] = None
        
        player.xy = ram_state[83] + 8, (ram_state[91]*2) + 20
        player.wh = 6, 16
        if ram_state[68] == 41:
            star = Star()
            objects[1] = star
            star.xy = ram_state[89] + 10, (ram_state[97]*2) + 21
        else:
            spider = Spider()
            objects[1] = spider
            spider.xy = ram_state[89] + 8, (ram_state[97]*2) + 21

        window = Window()
        objects[2] = window

        # r115 == lines right; 44 == 75-115, 63 == 118-158
        # 24 pixels between lines
        for i in range(40):
            line1, line2, line3, line4, line5, line6 = Line(), Line(), Line(), Line(), Line(), Line()
            objects[3+(i*3)], objects[4+(i*3)], objects[5+(i*3)] = line1, line2, line3
            objects[234+(i*3)], objects[235+(i*3)], objects[236+(i*3)] = line4, line5, line6
            line1.xy =  7 + i + ram_state[115], 17 + i*2
            line2.xy =  31 + i + ram_state[115], 17 + i*2
            line3.xy =  55 + i + ram_state[115], 17 + i*2
            line4.xy =  6 - i + ram_state[116], 19 + i*2
            line5.xy =  30 - i + ram_state[116], 19 + i*2
            line6.xy =  54 - i + ram_state[116], 19 + i*2
        for i in range(37):
            line1, line2, line3, line4, line5, line6 = Line(), Line(), Line(), Line(), Line(), Line()
            objects[123+(i*3)], objects[124+(i*3)], objects[125+(i*3)] = line1, line2, line3
            objects[354+(i*3)], objects[355+(i*3)], objects[356+(i*3)] = line4, line5, line6
            line1.xy =  47 - i + ram_state[115], 97 + i*2
            line2.xy =  71 - i + ram_state[115], 97 + i*2
            line3.xy =  95 - i + ram_state[115], 97 + i*2
            line4.xy =  i + ram_state[116] - 33, 97 + i*2
            line5.xy =  i + ram_state[116] - 9, 97 + i*2
            line6.xy =  i + ram_state[116] + 15, 97 + i*2

    elif room == 3:
        for i in range(len(objects)-1):
            objects[i+1] = None
        
        player.xy = ram_state[90] + 8, 145
        player.wh = 8, 9
        mare = Fire_Mare()
        objects[1] = mare
        mare.xy = ram_state[89] + 8, 145
        offset = 8
        if ram_state[76]&128:
            for i in range(4):
                if not ram_state[76]&2**(i+3):
                    offset += 1
        else:
            for i in range(4):
                if ram_state[76]&2**(i+3):
                    offset -= 1
        if ram_state[70] == 226:
            weapon = Weapon()
            objects[2] = weapon
            weapon.xy = ram_state[78] + offset, 157
        elif ram_state[70] == 233:
            life = Life()
            objects[2] = life
            life.xy = ram_state[78] + offset, 157
        else:
            objects[2] = None
        if ram_state[80]:
            castle = Castle()
            objects[3] = castle
            castle.xy = 48, 145 - ram_state[80]
            castle.wh = 64, ram_state[80] + 3
    # r33 type?
    # r67 shot
    # r82 enemypos?
    # r100 enemy formation?
    # r113 sword?

    

    if hud:
        # sun xy == r23, r24,
        # hour-glass == r26
        # lives == r31
        # weapon == r32

        # Sun
        if 25 < ram_state[23] < 42:
            sun = Sun()
            objects[-9] = sun
            top = 0
            bottom = 0
            xoff = 0
            if ram_state[23] < 32:
                top = 32 - ram_state[23]
                if top == 5:
                    xoff = 1
                elif top == 6:
                    xoff = 2
            elif ram_state[23] > 35:
                bottom = ram_state[23] - 35
                if bottom == 5:
                    xoff = 1
                elif bottom == 6:
                    xoff = 2
            sun.xy =  ram_state[24] + 9 + xoff, ram_state[23] - 30 + top
            sun.wh = 7 - (xoff*2), 7 - top - bottom
        else:
            objects[-9] = None

        # Hour Glass
        if ram_state[26]:
            time =  Hour_Glass()
            objects[-8] = time
            yoff = 0
            h = 0
            for i in range(8):
                if ram_state[26]&2**i:
                    if yoff:
                        h += i - yoff + 1
                    else:
                        h = 1
                    yoff = i+1

            time.xy = 121, 11 - yoff
            time.wh = 5, h
        else:
            objects[-8] = None
            
        # Score
        score = Score()
        objects[-7] = score
        if ram_state[28] > 15:
            score.xy = 57, 176
            score.wh = 45, 7
        elif ram_state[28]:
            score.xy = 66, 176
            score.wh = 36, 7
        elif ram_state[29] > 15:
            score.xy = 66, 176
            score.wh = 28, 7
        elif ram_state[29]:
            score.xy = 74, 176
            score.wh = 20, 7
        elif ram_state[30] > 15:
            score.xy = 74, 176
            score.wh = 12, 7
        else:
            score.xy = 82, 176
            score.wh = 4, 7
        
        # Lives
        for i in range(3):
            if i < ram_state[31]:
                life = Life()
                objects[-6+i] = life
                life.xy = 56+(i*8), 188
            else:
                objects[-6+i] = None
        
        # Weapons
        for i in range(3):
            if i < ram_state[32]:
                life = Weapon_HUD()
                objects[-3+i] = life
                life.xy = 79+(i*8), 188
            else:
                objects[-3+i] = None
