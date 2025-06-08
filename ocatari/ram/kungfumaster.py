from .game_objects import GameObject, ValueObject, NoObject, Orientation, OrientedObject
from ._helper_methods import _convert_number
import sys

MAX_NB_OBJECTS = {"Player": 1, "Knife_Throwers": 1, "Henchmen": 3, "Snake": 1, "Dragon": 1, "Dragon_Smoke": 1,
                  "Dragon_Balls": 1, "Red_Ball": 1, "Airball": 1, "Small_Enemy": 1, "Killer_Moth": 1,"Enemy_Final_Fighter": 1, "Knifes": 1, "Dragon_Fire": 1}
MAX_NB_OBJECTS_HUD = {"Player": 1, "Knife_Throwers": 1, "Henchmen": 3, "Snake": 1, "Dragon": 1, "Dragon_Smoke": 1, "Dragon_Balls": 1, "Red_Ball": 1, "Airball": 1,
                      "Small_Enemy": 1, "Killer_Moth": 1,"Enemy_Final_Fighter": 1, "Knifes": 1, "Dragon_Fire": 1, "Score": 1, "Time": 1, "Lives": 1, "Player_Health_Bar": 1, "Enemy_Health_Bar": 1}


class Player(OrientedObject):
    """
    Fighter fighting through the level
    """

    def __init__(self):
        super(Player, self).__init__()
        self._xy = 76, 100
        self.wh = (8, 34)
        self.rgb = 214, 214, 214
        self.hud = False
        self.orientation = Orientation.E


class Knife_Throwers(GameObject):
    """
    Enemy throwing knifes. Can throw low and on head hight
    """

    def __init__(self):
        super(Knife_Throwers, self).__init__()
        self._xy = 76, 100
        self.wh = (8, 34)
        self.rgb = 192, 192, 192
        self.hud = False


class Henchmen(GameObject):
    """
    Basic enemy dealing damage when in contact with the player
    """

    def __init__(self):
        super(Henchmen, self).__init__()
        self._xy = 76, 100
        self.wh = (8, 34)
        self.rgb = 104, 25, 154
        self.hud = False


class Snake(GameObject):
    """
    Drops from the top and then crawls on the ground
    """

    def __init__(self):
        super(Snake, self).__init__()
        self._xy = 76, 100
        self.wh = (8, 12)
        self.rgb = 0, 68, 0
        self.hud = False


class Dragon(GameObject):
    """
    Appears out of smoke and shoots fire
    """

    def __init__(self):
        super(Dragon, self).__init__()
        self._xy = 76, 100
        self.wh = (8, 34)
        self.rgb = 0, 68, 0
        self.hud = False


class Dragon_Smoke(GameObject):
    """
    Rises out of the dragon ball
    """

    def __init__(self):
        super(Dragon_Smoke, self).__init__()
        self._xy = 76, 100
        self.wh = (7, 37)
        self.rgb = 214, 214, 214
        self.hud = False


class Dragon_Balls(GameObject):
    """
    Drops from the ceiling to release the dragon
    """

    def __init__(self):
        super(Dragon_Balls, self).__init__()
        self._xy = 76, 100
        self.wh = (8, 12)
        self.rgb = 227, 151, 89
        self.hud = False


class Red_Ball(GameObject):
    """
    Drops from the ceiling to hit the player
    """

    def __init__(self):
        super(Red_Ball, self).__init__()
        self._xy = 76, 100
        self.wh = (8, 12)
        self.rgb = 148, 0, 0
        self.hud = False


class Airball(GameObject):
    """
    Flyies through the air to hit the player
    """

    def __init__(self):
        super(Airball, self).__init__()
        self._xy = 76, 100
        self.wh = (4, 6)
        self.rgb = 214, 214, 214
        self.hud = False


class Small_Enemy(GameObject):
    """
    Runs at player or jumps over them
    """

    def __init__(self):
        super(Small_Enemy, self).__init__()
        self._xy = 76, 100
        self.wh = (7, 21)
        self.rgb = 163, 57, 21
        self.hud = False


class Killer_Moth(GameObject):
    """
    Flies through the air to hit player
    """

    def __init__(self):
        super(Killer_Moth, self).__init__()
        self._xy = 76, 100
        self.wh = (7, 6)
        self.rgb = 148, 0, 0
        self.hud = False


class Enemy_Final_Fighter(GameObject):
    """
    Final fighter at the end of the level. Second final fighter throws boomerangs
    """

    def __init__(self):
        super(Enemy_Final_Fighter, self).__init__()
        self._xy = 76, 100
        self.wh = (8, 34)
        self.rgb = 74, 74, 74
        self.hud = False


class Knifes(GameObject):
    """
    Knifes throw by Knife_Throwers or Final_Fighters
    """

    def __init__(self):
        super(Knifes, self).__init__()
        self._xy = 76, 100
        self.wh = (5, 2)
        self.rgb = 74, 74, 74
        self.hud = False


class Dragon_Fire(GameObject):
    """
    Fire spit by the dragon
    """

    def __init__(self):
        super(Dragon_Fire, self).__init__()
        self._xy = 76, 100
        self.wh = (18, 4)
        self.rgb = 184, 50, 50
        self.hud = False


class Score(ValueObject):
    """
    Score of the game
    """

    def __init__(self):
        super(Score, self).__init__()
        self._xy = 63, 20
        self.wh = (6, 7)
        self.rgb = 128, 232, 128
        self.hud = True
        self.value = 0


class Time(ValueObject):
    """
    Time left to beat the level
    """

    def __init__(self):
        super(Time, self).__init__()
        self._xy = 63, 20
        self.wh = (6, 7)
        self.rgb = 214, 214, 214
        self.hud = True
        self.value = 0


class Lives(ValueObject):
    """
    Life value. Counts how many restarts are left before the game resets
    """

    def __init__(self):
        super(Lives, self).__init__()
        self._xy = 99, 31
        self.wh = (6, 7)
        self.rgb = 214, 214, 214
        self.hud = True
        self.value = 0


class Player_Health_Bar(ValueObject):
    """
    Indicates how many hits the player can still take.
    """

    def __init__(self):
        super(Player_Health_Bar, self).__init__()
        self._xy = 49, 41
        self.wh = (38, 5)
        self.rgb = 232, 232, 74
        self.hud = True


class Enemy_Health_Bar(ValueObject):
    """
    Indicates how many hits the enemy can still take.
    """

    def __init__(self):
        super(Enemy_Health_Bar, self).__init__()
        self._xy = 49, 49
        self.wh = (38, 5)
        self.rgb = 184, 50, 50
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

    objects.extend([NoObject()] * 15)
    # objects.extend()
    if hud:
        # objects.extend()
        objects.extend([Score(), Time(), Lives(),
                       Player_Health_Bar(), Enemy_Health_Bar()])
    return objects


def _detect_objects_ram(objects, ram_state, hud=False):
    """
    For all 3 objects:
    (x, y, w, h, r, g, b)
    """

    # ram[74] == player x, ram[46] == player y
    # x 131 = 82, 178 = 129
    # y 179 = 126, 157 = 104
    x, y = ram_state[74]-49, ram_state[46]-53
    w, h = 8, 34

    if ram_state[93] == 0:
        if not ram_state[90] & 8:
            x -= 7
        w, h = 15, 29
    elif ram_state[93] == 1:
        if ram_state[90] & 8:
            x -= 3
        w, h = 11, 29
    elif ram_state[93] == 2:
        if ram_state[90] & 8:
            x -= 2
        else:
            x -= 6
        w, h = 16, 34
    elif ram_state[93] == 3:
        if ram_state[90] & 8:
            x -= 1
        else:
            x -= 5
        w, h = 14, 34
    elif ram_state[93] == 4:
        if ram_state[90] & 8:
            x -= 3
        else:
            x -= 5
        w, h = 16, 29

    objects[0].xy = x, y
    objects[0].wh = w, h
    objects[0].orientation = Orientation.E if ram_state[90] else Orientation.W
    
    # ram[72] == enemy x
    if ram_state[72] > 49:
        x, y = ram_state[72]-49, 126
        idx = 0
        if ram_state[50] == 85:
            idx = 9
            if type(objects[9]) is NoObject:
                objects[9] = Red_Ball()
            y = 164 - ram_state[35]
        elif ram_state[50] == 92:
            idx = 1
            if type(objects[1]) is NoObject:
                objects[1] = Knife_Throwers()
        elif ram_state[50] == 97:
            idx = 10
            if type(objects[10]) is NoObject:
                objects[10] = Airball()
            x += 2
            y = 169 - ram_state[35]
        elif ram_state[50] == 134:
            idx = 5
            if type(objects[5]) is NoObject:
                objects[5] = Snake()
            y = 163 - ram_state[35]
        elif ram_state[50] == 160 or 70 <= ram_state[50] <= 83:
            idx = 11
            if type(objects[11]) is NoObject:
                objects[11] = Small_Enemy()
            y = 155 - ram_state[35]
            if 70 <= ram_state[50] <= 83:
                x += 1
                y += 6
                objects[1].wh = 4, 14
            if ram_state[92] & 8:
                x += 1
        elif ram_state[50] == 177:
            idx = 2
            if type(objects[2]) is NoObject:
                objects[2] = Henchmen()
        elif ram_state[50] == 154:
            idx = 6
            if type(objects[6]) is NoObject:
                objects[6] = Dragon()
            y += 1
        elif ram_state[50] == 188:
            idx = 7
            if type(objects[7]) is NoObject:
                objects[7] = Dragon_Smoke()
            y -= 1
        elif ram_state[50] == 204:
            idx = 13
            if type(objects[13]) is NoObject:
                objects[13] = Enemy_Final_Fighter()
        elif ram_state[50] == 227:
            idx = 8
            if type(objects[8]) is NoObject:
                objects[8] = Dragon_Balls()
            y = 163 - ram_state[35]
        elif ram_state[50] == 247:
            idx = 12
            if type(objects[12]) is NoObject:
                objects[12] = Killer_Moth()
            y = 163 - ram_state[35]
        else:
            idx = 1
            if type(objects[1]) is NoObject:
                objects[1] = Knife_Throwers()
        objects[idx].xy = x, y

        # ram [63] if > 1 enemy bit representation of appendix, 16 pixels apart per enemy
        if ram_state[63] & 1 and ram_state[72]-49 > 0:
            objects[3] = Henchmen()
            objects[3].xy = ram_state[72]-33, 126
        else:
            objects[3] = NoObject()
        if ram_state[63] & 2 and ram_state[72]-49 > 0:
            objects[4] = Henchmen()
            objects[4].xy = ram_state[72]-17, 126
        else:
            objects[4] = NoObject()
    else:
        for i in range(1,14):
            objects[i] = NoObject()

    # ram[73] == projectile x, ram[96] == projectile "y" (not really the hight)

    # projectile
    if ram_state[96] != 188:
        if ram_state[50] == 154:
            objects[14] = NoObject()
            if type(objects[15]) is NoObject:
                objects[15] = Dragon_Fire()
            if ram_state[92] & 8:
                objects[15].xy = ram_state[73]-52, 121+ram_state[96]
            else:
                objects[15].xy = ram_state[73]-60, 121+ram_state[96]
        elif ram_state[50] == 204:
            objects[15] = NoObject()
            if type(objects[14]) is NoObject:
                objects[14] = Knifes()
            objects[14].xy = ram_state[73]-50, 121+ram_state[96]
            objects[14].wh = 3, 4
        else:
            objects[15] = NoObject()
            if type(objects[14]) is NoObject:
                objects[14] = Knifes()
            objects[14].xy = ram_state[73]-52, 123+ram_state[96]
    else:
        objects[14], objects[15] = NoObject(), NoObject()

    if hud:
        # ram[29] lives, ram[24-26] score
        x, w = 63, 6
        if ram_state[24] > 16:
            x, w = 23, 46
        elif ram_state[24]:
            x, w = 31, 38
        elif ram_state[25] > 16:
            x, w = 39, 30
        elif ram_state[25]:
            x, w = 47, 22
        elif ram_state[26] > 16:
            x, w = 55, 14

        objects[16].xy = x, 20
        objects[16].wh = w, 7

        x2, w2 = 55, 6
        if ram_state[27] > 16:
            x2, w2 = 31, 30
        elif ram_state[27]:
            x2, w2 = 39, 22
        elif ram_state[28] > 16:
            x2, w2 = 47, 14

        objects[17].xy = x2, 10
        objects[17].wh = w2, 7

        objects[18].value = ram_state[29]

        # ram[75,76] life
        objects[19].wh = ram_state[75], 5
        objects[20].wh = ram_state[76], 5
