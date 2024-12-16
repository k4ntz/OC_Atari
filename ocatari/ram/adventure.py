import sys

from ocatari.ram import GameObject

"""
The map can be found here, if needed :
https://atariage.com/2600/archives/strategy_adventuremap.html?SystemID=2600

"""


class Player(GameObject):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.rgb = [252, 252, 84]
        self.wh = 3, 8


# Each dragon has a different purpose that's why I thought it might be more relevant to have a class for each dragon
class YellowDragon(GameObject):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.rgb = [223, 192, 111]
        self.wh = 1, 1
        self.alive = True


class GreenDragon(GameObject):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.rgb = [223, 192, 111]
        self.wh = 1, 1
        self.alive = True


class RedDragon(GameObject):
    def __init__(self, *args, **kwargs):
        self.rgb = [223, 192, 111]
        self.wh = 1, 1
        self.alive = True


class BlackBat(GameObject):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.rgb = [0, 0, 0]
        self.wh = 1, 1


class DragonSword(GameObject):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.rgb = [223, 192, 111]
        self.wh = 1, 1


class YellowKey(GameObject):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.rgb = [223, 192, 111]
        self.wh = 8, 9


class BlackKey(GameObject):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.rgb = [0, 0, 0]
        self.wh = 8, 9


class WhiteKey(GameObject):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.rgb = [255, 255, 255]
        self.wh = 8, 9


class Magnet(GameObject):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.rgb = [0, 0, 0]
        self.wh = 1, 1


class BridgeEdge(GameObject):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.rgb = [168, 72, 158]
        self.wh = 1, 1


class Gate(GameObject):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.rgb = [0, 0, 0]
        self.wh = 1, 1


class Chalice(GameObject):
    def __init__(self, *args: object, **kwargs: object) -> object:
        super().__init__(*args, **kwargs)
        self.rgb = [168, 72, 158]


def _get_max_objects(hud=False):
    def fromdict(max_obj_dict):
        objects = []
        mod = sys.modules[__name__]
        for k, v in max_obj_dict.items():
            for _ in range(0, v):
                objects.append(getattr(mod, k)())
        return objects

    if hud:
        return
    return


def _init_objects_ram(hud=False):
    """
    (Re)Initialize the objects
    """
    objects = [Player(),]
    return objects


global object1
global object2
object1 = 1
object2 = 2


def _detect_objects_ram(objects, ram_state, hud=False):
    objects[0].xy = ram_state[11] - 0.5, 238 - 2 * ram_state[12]
    while len(objects) > 1:
        objects.pop()
    object1_pos = ram_state[6] + 0.5, 238 - 2 * ram_state[7]
    object2_pos = ram_state[8] + 0.5, 238 - 2 * ram_state[9]

    object1_type = ram_state[21]
    object2_type = ram_state[22]
    object1_height, object2_height = ram_state[16], ram_state[17]
    if object1_type in [9, 18, 27]:
        objects.append(Gate())
        objects[-1].xy = object1_pos
        objects[-1].wh = objects[-1].w, object1_height
    elif object1_type == 54:
        objects.append(RedDragon())
        objects[-1].xy = object1_pos
        objects[-1].wh = objects[-1].w, object1_height
    elif object1_type == 63:
        objects.append(YellowDragon())
        objects[-1].xy = object1_pos
        objects[-1].wh = objects[-1].w, object1_height
    elif object1_type == 72:
        objects.append(GreenDragon())
        objects[-1].xy = object1_pos
        objects[-1].wh = objects[-1].w, object1_height
    elif object1_type == 90:
        objects.append(DragonSword())
        objects[-1].xy = object1_pos
        objects[-1].wh = objects[-1].w, object1_height
    elif object1_type == 9:
        objects.append(BridgeEdge())
        objects[-1].xy = object1_pos
        objects[-1].wh = objects[-1].w, object1_height
        objects.append(BridgeEdge())
        objects[-1].xy = object1_pos[0] + 7, object1_pos[1]
        objects[-1].wh = objects[-1].w, object1_height
    elif object1_type == 99:
        objects.append(YellowKey())
        objects[-1].xy = object1_pos
        objects[-1].wh = objects[-1].w, object1_height
    elif object1_type == 108:
        objects.append(WhiteKey())
        objects[-1].xy = object1_pos
        objects[-1].wh = objects[-1].w, object1_height
    elif object1_type == 117:
        objects.append(BlackKey())
        objects[-1].xy = object1_pos
        objects[-1].wh = objects[-1].w, object1_height
    elif object1_type == 126:
        objects.append(BlackBat())
        objects[-1].xy = object1_pos
        objects[-1].wh = objects[-1].w, object1_height
    elif object1_type == 144:
        objects.append(Chalice())
        objects[-1].xy = object1_pos
        objects[-1].wh = objects[-1].w, object1_height
    elif object1_type == 153:
        objects.append(Magnet())
        objects[-1].xy = object1_pos
        objects[-1].wh = objects[-1].w, object1_height

    if object2_type in [9, 18, 27]:
        objects.append(Gate())
        objects[-1].xy = object2_pos
        objects[-1].wh = objects[-1].w, object2_height
    elif object2_type == 54:
        objects.append(RedDragon())
        objects[-1].xy = object2_pos
        objects[-1].wh = objects[-1].w, object2_height
    elif object2_type == 63:
        objects.append(YellowDragon())
        objects[-1].xy = object2_pos
        objects[-1].wh = objects[-1].w, object2_height
    elif object2_type == 72:
        objects.append(GreenDragon())
        objects[-1].xy = object2_pos
        objects[-1].wh = objects[-1].w, object2_height
    elif object2_type == 81:
        objects.append(DragonSword())
        objects[-1].xy = object2_pos
        objects[-1].wh = objects[-1].w, object2_height
    elif object2_type == 90:
        objects.append(BridgeEdge())
        objects[-1].xy = object2_pos
        objects[-1].wh = objects[-1].w, object2_height
        objects.append(BridgeEdge())
        objects[-1].xy = object2_pos[0] + 7, object2_pos[1]
        objects[-1].wh = objects[-1].w, object2_height
    elif object2_type == 99:
        objects.append(YellowKey())
        objects[-1].xy = object2_pos
        objects[-1].wh = objects[-1].w, object2_height
    elif object2_type == 108:
        objects.append(WhiteKey())
        objects[-1].xy = object2_pos
        objects[-1].wh = objects[-1].w, object2_height
    elif object2_type == 117:
        objects.append(BlackKey())
        objects[-1].xy = object2_pos
        objects[-1].wh = objects[-1].w, object2_height
    elif object2_type == 126:
        objects.append(BlackBat())
        objects[-1].xy = object2_pos
        objects[-1].wh = objects[-1].w, object2_height
    elif object2_type == 144:
        objects.append(Chalice())
        objects[-1].xy = object2_pos
        objects[-1].wh = objects[-1].w, object2_height
    elif object2_type == 153:
        objects.append(Magnet())
        objects[-1].xy = object2_pos
        objects[-1].wh = objects[-1].w, object2_height

    if hud:
        return

    return objects


"""
    ;#1 Portcullis #1       Black            09
    ;#2 Portcullis #2       Black            12
    ;#3 Portcullis #3       Black            1B
    ;#4 Name                Flash            24
    ;#5 Number              Green            2D
    ;#6 Dragon #1           Red              36
    ;#7 Dragon #2           Yellow           3F
    ;#8 Dragon #3           Green            48
    ;#9 Sword               Yellow           51
    ;#0A Bridge             Purple           5A
    Key #01            Yellow           63
    Key #02            White            6C
    Key #03            Black            75
    ;#0E Bat                Black            7E
    #0F Black Dot          Light Gray       87
    ;#10 Challise           Flash            90
    ;#11 Magnet             Black            99
    ;#12 Null               Black



Gives us the initial location of each object. Each number corresponds (written in hexadecimal) to the room number where
the objects are initially located. For a particular object the first number corresponds to its location in the first level
and so on. Also Portcullis state is a door (thank you wikipedia).
Game1Objects:
       $15,$51,$12            ;Black dot (Room, X, Y)
       $0E,$50,$20,$00,$00    ;Red Dragon (Room, X, Y, Movement, State)
       $01,$50,$20,$00,$00    ;Yellow Dragon (Room, X, Y, Movement, State)
       $1D,$50,$20,$00,$00    ;Green Dragon (Room, X, Y, Movement, State)
       $1B,$80,$20            ;Magnet (Room,X,Y)
       $12,$20,$20            ;Sword (Room,X,Y)
       $1C,$30,$20            ;Challise (Room,X,Y)
       $04,$29,$37            ;Bridge (Room,X,Y)
       $11,$20,$40            ;Yellow Key (Room,X,Y)
       $0E,$20,$40            ;White Key (Room,X,Y)
       $1D,$20,$40            ;Black Key (Room,X,Y)
       $1C                    ;Portcullis State
       $1C                    ;Portcullis State
       $1C                    ;Portcullis State
       $1A,$20,$20,$00,$00    ;Bat (Room, X, Y, Movement, State)
       $78,$00                ;Bat (Carrying, Fed-Up)

;Object locations (room and coordinate) for Games 02 and 03.
Game2Objects:
       $15,$51,$12            ;Black Dot (Room,X,Y)
       $14,$50,$20,$A0,$00    ;Red Dragon (Room,X,Y,Movement,State)
       $19,$50,$20,$A0,$00    ;Yellow Dragon (Room,X,Y,Movement,State)
       $04,$50,$20,$A0,$00    ;Green Dragon (Room,X,Y,Movement,State)
       $0E,$80,$20            ;Magnet (Room,X,Y)
       $11,$20,$20            ;Sword (Room,X,Y)
       $14,$30,$20            ;Chalise (Room,X,Y)
       $0B,$40,$40            ;Bridge (Room,X,Y)
       $09,$20,$40            ;Yellow Key (Room,X,Y)
       $06,$20,$40            ;White Key (Room,X,Y)
       $19,$20,$40            ;Black Key (Room,X,Y)
       $1C                    ;Portcullis State
       $1C                    ;Portcullis State
       $1C                    ;Portcullis State
       $02,$20,$20,$90,$00    ;Bat (Room,X,Y,Movement,State)
       $78,$00                ;Bat (Carrying, Fed-Up)








"""
