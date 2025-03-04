from .game_objects import GameObject, ValueObject, NoObject
from ._helper_methods import _convert_number
from .utils import match_objects
import sys

MAX_NB_OBJECTS = {"Player": 1, 'Lyssa': 1, 'Slayers': 15, 'Slayer_Shot': 1, 'Weapon': 1, 'Beast': 1, 'Enemy_Weapon': 1,
                  'Wall': 64, 'Star': 1, 'Spider': 1, 'Window': 1, 'Line': 462, 'Fire_Mare': 1, 'Weapon': 1, 'Life': 1, 'Castle': 1}
MAX_NB_OBJECTS_HUD = {"Player": 1, 'Lyssa': 1, 'Slayers': 15, 'Slayer_Shot': 1, 'Weapon': 1, 'Beast': 1, 'Enemy_Weapon': 1, 'Wall': 64, 'Star': 1, 'Spider': 1,
                      'Window': 1, 'Line': 462, 'Fire_Mare': 1, 'Weapon': 1, 'Life': 1, 'Castle': 1, 'Sun': 1, 'Hour_Glass': 1, 'Score': 1, 'Life_HUD': 3, 'Weapon_HUD': 3}  # 'Score': 1}


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
    def __init__(self, x=0, y=160, w=6, h=16):
        super(Slayers, self).__init__()
        self._xy = x, y
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
        self.wh = (3, 4)
        self.rgb = 236, 236, 236
        self.hud = False


class Castle(GameObject):
    def __init__(self):
        super(Castle, self).__init__()
        self._xy = 0, 0
        self.wh = (64, 4)
        self.rgb = 162, 98, 33
        self.hud = False


class Life(GameObject):
    def __init__(self):
        super(Life, self).__init__()
        self._xy = 0, 0
        self.wh = (6, 7)
        self.rgb = 92, 186, 92
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


class Life_HUD(ValueObject):
    def __init__(self):
        super(Life_HUD, self).__init__()
        self._xy = 56, 188
        self.wh = (6, 7)
        self.rgb = 92, 186, 92
        self.hud = True
        self.value = 0


class Weapon_HUD(ValueObject):
    def __init__(self):
        super(Weapon_HUD, self).__init__()
        self._xy = 79, 188
        self.wh = (8, 7)
        self.rgb = 92, 186, 92
        self.hud = True
        self.value = 0


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

    objects.extend([NoObject()] * 553)
    if hud:
        objects.extend([NoObject(), NoObject(), Score(), Life_HUD(), Weapon_HUD()])
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
        enemies_pos = []
        if ram_state[114] or (ram_state[38] in (8, 9, 10, 11) and ram_state[98]):
            player.xy = ram_state[90] + 9, (ram_state[98]*2) + 16
            if ram_state[73] != 80:
                if type(objects[1]) is NoObject:
                    objects[1] = Lyssa()
                objects[1].xy = ram_state[89] + 9, (ram_state[97]*2) + 15
            else:
                objects[1] = NoObject()
            enemies = 0
            for i in range(5):
                if ram_state[99+i] and enemies < ram_state[82] and not (ram_state[73] == 80 and ram_state[91+i] >= 69):
                    enemies += 1
                    enemies_pos.append((ram_state[83+i] + 9, (ram_state[91+i]*2) + 15, 6, 16))

                for j in range(3):
                    if ram_state[99+i] & 2**j and type(objects[2+(5*i)]) is not NoObject:
                        enemies_pos.append((ram_state[83+i] + 9 + (
                            16 * (ram_state[99+i] & 2**j)), (ram_state[91+i]*2) + 15, 6, 16))
        else:
            player.xy = ram_state[89] + 9, (ram_state[97]*2) + 16
            if type(objects[1]) is NoObject:
                objects[1] = Lyssa()
            objects[1].xy = ram_state[83] + 9, (ram_state[91]*2) + 15
            for i in range(5):
                if ram_state[100+i] and ram_state[82] > i:
                    enemies_pos.append((ram_state[84+i] + 9, (ram_state[92+i]*2) + 15, 6, 16))

                    for j in range(3):
                        if ram_state[100+i] & 2**j:
                            enemies_pos.append((ram_state[84+i] + 9 + (
                                16 * (ram_state[100+i] & 2**j)), (ram_state[92+i]*2) + 15, 6, 16))
                            
        match_objects(objects, enemies_pos, 2, 15, Slayers)
        
        if ram_state[77]:
            if type(objects[17]) is NoObject:
                objects[17] = Slayer_Shot()
            if ram_state[79] & 16:
                objects[17].wh = 7, 7
                if ram_state[79] & 128:
                    objects[17].xy = (ram_state[78] + 7 + ram_state[76]
                               * 2) - 32, ram_state[77]*2 + 6
                else:
                    objects[17].xy = (ram_state[78] + 7 - ram_state[76]
                               * 2) + 25, ram_state[77]*2 + 6
            else:
                objects[17].wh = 1, 7
                objects[17].xy = ram_state[78] + 7, ram_state[77]*2 + 6
        else:
            objects[17] = NoObject()

    elif room == 1:
        for i in range(2,18):
            objects[i] = NoObject()
        for i in range(84, 500):
            objects[i] = NoObject()

        player.xy = ram_state[83] + 9, (ram_state[91]*2) + 15
        player.wh = 7, 16

        if type(objects[1]) is Lyssa:
            objects[1] = Lyssa()

        if ram_state[109] == 42:
            objects[1].xy = ram_state[85] + 9, (ram_state[93]*2) + 15
        else:
            objects[1].xy = ram_state[85] + 8, (ram_state[93]*2) + 15

        if ram_state[97] < 80:
            if type(objects[18]) is NoObject:
                objects[18] = Weapon()
                objects[18].rgb = 224, 236, 124
            if ram_state[47] == 24:
                objects[18].xy = ram_state[89] + 11, (ram_state[97]*2) + 16
                objects[18].wh = 2, 2
            elif ram_state[47] == 36:
                objects[18].xy = ram_state[89] + 9, (ram_state[97]*2) + 16
                objects[18].wh = 6, 6
            else:
                objects[18].xy = ram_state[89] + 8, (ram_state[97]*2) + 16
                objects[18].wh = 8, 8
        else:
            objects[18] = NoObject()

        if type(objects[19]) is NoObject:
            objects[19] = Beast()
        if ram_state[100] == 157:
            objects[19].xy = ram_state[84] + 13, (ram_state[92]*2) + 15
        else:
            objects[19].xy = ram_state[84] + 9, (ram_state[92]*2) + 15

        if ram_state[77] < 83:
            if type(objects[20]) is NoObject:
                objects[20] = Enemy_Weapon()
            objects[20].xy = ram_state[79] + 7, (ram_state[77]*2) + 7
        else:
            objects[20] = NoObject()

        for j in range(4):
            for i in range(8):
                if ram_state[115+j*2] & 2**i:
                    if type(objects[21+16*j+i]) is NoObject:
                        objects[21+16*j+i] = Wall()
                    objects[21+16*j+i].xy = 48 + 4*i, 39 + 4*j
                else:
                    objects[21+16*j+i] = NoObject()
                if ram_state[116+j*2] & 2**i:
                    if type(objects[29+16*j+i]) is NoObject:
                        objects[29+16*j+i] = Wall()
                    objects[29+16*j+i].xy = 108 - 4*i, 39 + 4*j
                else:
                    objects[29+16*j+i] = NoObject()

    elif room == 2:
        for i in range(89):
            objects[i] = NoObject()

        player.xy = ram_state[83] + 8, (ram_state[91]*2) + 20
        player.wh = 6, 16
        if ram_state[68] == 41:
            if type(objects[89]) is NoObject:
                objects[89] = Star()
            objects[89].xy = ram_state[89] + 10, (ram_state[97]*2) + 21

            objects[90] = NoObject()
        else:
            if type(objects[90]) is NoObject:
                objects[90] = Spider()
            objects[90].xy = ram_state[89] + 8, (ram_state[97]*2) + 21

            objects[89] = NoObject()


        if type(objects[91]) is NoObject:
            objects[91] = Window()

        # r115 == lines right; 44 == 75-115, 63 == 118-158
        # 24 pixels between lines
        for i in range(40):
            # line1, line2, line3, line4, line5, line6 = Line(
            # ), Line(), Line(), Line(), Line(), Line()
            # objects[92+(i*3)], objects[93+(i*3)], objects[94 + (i*3)] = line1, line2, line3
            # objects[323+(i*3)], objects[324+(i*3)], objects[325 + (i*3)] = line4, line5, line6

            for j in range(3):
                if type(objects[92+(i*3)+j]) is NoObject:
                    objects[92+(i*3)+j] = Line()
                if type(objects[323+(i*3)+j]) is NoObject:
                    objects[323+(i*3)+j] = Line()
            objects[92+(i*3)].xy = 7 + i + ram_state[115], 17 + i*2
            objects[93+(i*3)].xy = 31 + i + ram_state[115], 17 + i*2
            objects[94 + (i*3)].xy = 55 + i + ram_state[115], 17 + i*2
            objects[323+(i*3)].xy = 6 - i + ram_state[116], 19 + i*2
            objects[324+(i*3)].xy = 30 - i + ram_state[116], 19 + i*2
            objects[325 + (i*3)].xy = 54 - i + ram_state[116], 19 + i*2

        for i in range(37):
            # line1, line2, line3, line4, line5, line6 = Line(
            # ), Line(), Line(), Line(), Line(), Line()
            # objects[212+(i*3)], objects[213+(i*3)], objects[214 +
            #                                                 (i*3)] = line1, line2, line3
            # objects[443+(i*3)], objects[444+(i*3)], objects[445 +
            #                                                 (i*3)] = line4, line5, line6
            
            for j in range(3):
                if type(objects[212+(i*3)+j]) is NoObject:
                    objects[212+(i*3)+j] = Line()
                if type(objects[443+(i*3)+j]) is NoObject:
                    objects[443+(i*3)+j] = Line()

            objects[212+(i*3)].xy = 47 - i + ram_state[115], 97 + i*2
            objects[213+(i*3)].xy = 71 - i + ram_state[115], 97 + i*2
            objects[214 + (i*3)].xy = 95 - i + ram_state[115], 97 + i*2
            objects[443+(i*3)].xy = i + ram_state[116] - 33, 97 + i*2
            objects[444+(i*3)].xy = i + ram_state[116] - 9, 97 + i*2
            objects[445 + (i*3)].xy = i + ram_state[116] + 15, 97 + i*2

    elif room == 3:
        for i in range(1, 85):
            objects[i] = NoObject()
        for i in range(89, 500):
            objects[i] = NoObject()

        player.xy = ram_state[90] + 8, 145
        player.wh = 8, 9
        if type(objects[85]) is NoObject:
            objects[85] = Fire_Mare()
        objects[85].xy = ram_state[89] + 8, 145

        offset = 8
        if ram_state[76] & 128:
            for i in range(4):
                if not ram_state[76] & 2**(i+3):
                    offset += 1
        else:
            for i in range(4):
                if ram_state[76] & 2**(i+3):
                    offset -= 1
        # items in the ground
        if ram_state[70] == 226:
            if type(objects[86]) is NoObject:
                objects[86] = Weapon()
            objects[86].xy = ram_state[78] + offset, 157
        else:
            objects[86] = NoObject()

        if ram_state[70] == 233:
            if type(objects[87]) is NoObject:
                objects[87] = Life()
            objects[87].xy = ram_state[78] + offset, 157
        else:
            objects[87] = NoObject()

        if ram_state[80]:
            if type(objects[88]) is NoObject:
                objects[88] = Castle()
            objects[88].xy = 48, 145 - ram_state[80]
            objects[88].wh = 64, ram_state[80] + 3
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
            if type(objects[-5]) is NoObject:
                objects[-5] = Sun()
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
            objects[-5].xy = ram_state[24] + 9 + xoff, ram_state[23] - 30 + top
            objects[-5].wh = 7 - (xoff*2), 7 - top - bottom
        else:
            objects[-5] = NoObject()

        # Hour Glass
        if ram_state[26]:
            if type(objects[-4]) is NoObject:
                objects[-4] = Hour_Glass()
            yoff = 0
            h = 0
            for i in range(8):
                if ram_state[26] & 2**i:
                    if yoff:
                        h += i - yoff + 1
                    else:
                        h = 1
                    yoff = i+1

            objects[-4].xy = 121, 11 - yoff
            objects[-4].wh = 5, h
        else:
            objects[-4] = NoObject()

        # Score
        x, w = 82, 4
        if ram_state[28] > 15:
            x, w = 57, 45
        elif ram_state[28]:
            x, w = 66, 36
        elif ram_state[29] > 15:
            x, w = 66, 28
        elif ram_state[29]:
            x, w = 74, 20
        elif ram_state[30] > 15:
            x, w = 74, 12
        else:
            x, w = 82, 4

        objects[-3].xywh = x, 176, w, 7
        objects[-3].value = _convert_number(ram_state[28])*10000 + _convert_number(ram_state[29])*100 + _convert_number(ram_state[30])

        # Lives
        if ram_state[31]:
            if type(objects[-2]) is NoObject:
                objects[-2] = Life_HUD()
            if ram_state[31] < 4:
                objects[-2].wh = 6 + (8*(ram_state[31]-1)), 7
                objects[-2].value = ram_state[31]
            else:
                objects[-2].wh = 22, 7
                objects[-2].value = 3
        else:
            objects[-2] = NoObject()

        # Weapons
        if ram_state[32]:
            if type(objects[-1]) is NoObject:
                objects[-1] = Weapon_HUD()
            if ram_state[32] < 4:
                objects[-1].wh = 8*ram_state[32], 7
                objects[-1].value = ram_state[32]
            else:
                objects[-1].wh = 24, 7
                objects[-1].value = 3
        else:
            objects[-1] = NoObject()
