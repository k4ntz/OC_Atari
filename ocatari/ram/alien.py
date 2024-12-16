from .game_objects import GameObject, ValueObject, NoObject
import sys

MAX_NB_OBJECTS = {"Player": 1, "Alien": 3,
                  "Pulsar": 1, "Rocket": 1, "Egg": 156}
MAX_NB_OBJECTS_HUD = {"Player": 1, "Alien": 3, "Pulsar": 1,
                      "Rocket": 1, "Egg": 156, "Score": 1, "Life": 1}


class Player(GameObject):
    def __init__(self):
        super(Player, self).__init__()
        self._xy = 0, 0
        self.wh = (6, 13)
        self.rgb = 132, 144, 252
        self.hud = False


class Alien(GameObject):
    def __init__(self):
        super(Alien, self).__init__()
        self._xy = 0, 0
        self.wh = (8, 13)
        self.rgb = 236, 140, 224
        self.vulnerable = False
        self.hud = False


class Egg(GameObject):
    def __init__(self, x=0, y=0):
        super(Egg, self).__init__()
        self._xy = x, y
        self.wh = (1, 2)
        self.rgb = 198, 108, 58
        self.hud = False


class Pulsar(GameObject):
    def __init__(self):
        super(Pulsar, self).__init__()
        self._xy = 0, 0
        self.wh = (7, 5)
        self.rgb = 252, 144, 144
        self.hud = False


class Rocket(GameObject):
    def __init__(self):
        super(Rocket, self).__init__()
        self._xy = 77, 65
        self.wh = (8, 5)
        self.rgb = 252, 252, 84
        self.hud = False


class Score(ValueObject):
    def __init__(self):
        super(Score, self).__init__()
        self._xy = 0, 0
        self.wh = (6, 7)
        self.rgb = 132, 144, 252
        self.hud = False


class Life(ValueObject):
    def __init__(self):
        super(Life, self).__init__()
        self._xy = 21, 187
        self.wh = (5, 5)
        self.rgb = 132, 144, 252
        self.hud = False
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

    objects.extend([NoObject()] * 173)
    if hud:
        objects.extend([Score(), NoObject()])
    return objects


def _detect_objects_ram(objects, ram_state, hud=False):
    """
    For all 3 objects:
    (x, y, w, h, r, g, b)
    """
    player = objects[0]
    player.xy = ram_state[52] + 18, 196 - ram_state[45]*2 + 1

    # y 110 = 43 152 = 22
    for i in range(3):
        if ram_state[42+i] and ram_state[49+i]:
            if type(objects[1+i]) is NoObject:
                objects[1+i] = Alien()
            alien = objects[1+i]
            alien.xy = ram_state[49+i] + 17, 196 - ram_state[42+i]*2
            if ram_state[117] == 139:
                alien.rgb = 101, 111, 228
                alien.vulnerable = True
            elif i == 0:
                alien.rgb = 132, 252, 212
                alien.vulnerable = False
            elif i == 1:
                alien.rgb = 252, 252, 84
                alien.vulnerable = False
            elif i == 2:
                alien.rgb = 236, 140, 224
                alien.vulnerable = False
        else:
            objects[1+i] = NoObject()

    if ram_state[103]:
        if type(objects[4]) is NoObject:
            objects[4] = Pulsar()

        if ram_state[103] == 1:
            objects[4].xy = 123, 137
        elif ram_state[103] == 2:
            objects[4].xy = 31, 137
        elif ram_state[103] == 3:
            objects[4].xy = 77, 17
    else:
        objects[4] = NoObject()

    if ram_state[47]:
        if type(objects[5]) is NoObject:
            objects[5] = Rocket()
        objects[5].xy = 17+15*(ram_state[60] & 7), 197-(2*ram_state[47])
    else:
        objects[5] = NoObject()

##############################################
# ============================================
##############################################
    y = 19
    for i in range(13):
        if ram_state[65+i] & 4:
            if type(objects[6+i*6]) is NoObject:
                objects[6+i*6] = Egg(x=26, y=y)
        else:
            objects[6+i*6] = NoObject()

        if ram_state[65+i] & 8:
            if type(objects[7+i*6]) is NoObject:
                objects[7+i*6] = Egg(x=56, y=y)
        else:
            objects[7+i*6] = NoObject()

        if ram_state[65+i] & 16:
            if type(objects[8+i*6]) is NoObject:
                objects[8+i*6] = Egg(x=34, y=y+2)
        else:
            objects[8+i*6] = NoObject()

        if ram_state[65+i] & 32:
            if type(objects[9+i*6]) is NoObject:
                objects[9+i*6] = Egg(x=64, y=y+2)
        else:
            objects[9+i*6] = NoObject()

        if ram_state[65+i] & 64:
            if type(objects[10+i*6]) is NoObject:
                objects[10+i*6] = Egg(x=42, y=y+4)
        else:
            objects[10+i*6] = NoObject()

        if ram_state[65+i] & 128:
            if type(objects[11+i*6]) is NoObject:
                objects[11+i*6] = Egg(x=72, y=y+4)
        else:
            objects[11+i*6] = NoObject()

        y += 12

    y = 19
    for i in range(13):
        if ram_state[78+i] & 4:
            if type(objects[84+i*6]) is NoObject:
                objects[84+i*6] = Egg(x=89, y=y)
        else:
            objects[84+i*6] = NoObject()

        if ram_state[78+i] & 8:
            if type(objects[85+i*6]) is NoObject:
                objects[85+i*6] = Egg(x=118, y=y)
        else:
            objects[85+i*6] = NoObject()

        if ram_state[78+i] & 16:
            if type(objects[86+i*6]) is NoObject:
                objects[86+i*6] = Egg(x=97, y=y+2)
        else:
            objects[86+i*6] = NoObject()

        if ram_state[78+i] & 32:
            if type(objects[87+i*6]) is NoObject:
                objects[87+i*6] = Egg(x=126, y=y+2)
        else:
            objects[87+i*6] = NoObject()

        if ram_state[78+i] & 64:
            if type(objects[88+i*6]) is NoObject:
                objects[88+i*6] = Egg(x=105, y=y+4)
        else:
            objects[88+i*6] = NoObject()

        if ram_state[78+i] & 128:
            if type(objects[89+i*6]) is NoObject:
                objects[89+i*6] = Egg(x=134, y=y+4)
        else:
            objects[89+i*6] = NoObject()

        y += 12

    if hud:
        score = objects[173]
        score.xy = 63, 176
        score.wh = 6, 7
        x = 23
        w = 46
        for i in [3, 5, 7, 9, 11]:
            if ram_state[i] != 128:
                score.xy = x, 176
                score.wh = w, 7
            else:
                x += 8
                w -= 8

        lives = ram_state[64] - 1

        if lives:
            if type(objects[174]) is NoObject:
                objects[174] = Life()
            objects[174].wh = 5 + 8*(lives-1), 5
            objects[174].value = lives
        else:
            objects[174] = NoObject()


def _detect_objects_alien_raw(info, ram_state):
    """
    returns unprocessed list with
    ball_x, ball_y, enemy_y, player_y
    """
    info["objects_list"] = ram_state[32:36]


# def _detect_objects_alien_revised_old(info, ram_state, hud=False):
#     """
#     For all 3 objects:
#     (x, y, w, h, r, g, b)
#     """
#     objects = {}
#     objects["player"] = ram_state[32]+5, ram_state[34]+38, 14, 46, 214, 214, 214
#     objects["enemy"] = ram_state[33]+4, ram_state[35]+38, 14, 46, 0, 0, 0
#     if hud:
#         objects["enemy_score"] = 111, 5, 6, 7, 0, 0, 0
#         if ram_state[19] < 10:
#             objects["enemy_score2"] = 0, 0, 0, 0, 0, 0, 0
#         else:
#             objects["enemy_score2"] = 103, 5, 6, 7, 0, 0, 0
#         objects["player_score"] = 47, 5, 6, 7, 214, 214, 214
#         if ram_state[18] < 10:
#             objects["player_score2"] = 0, 0, 0, 0, 0, 0, 0
#         else:
#             objects["player_score2"] = 39, 5, 6, 7, 214, 214, 214
#         objects["logo"] = 62, 189, 32, 7, 20, 60, 0
#         objects["time1"] = 63, 17, 6, 7, 20, 60, 0
#         objects["time2"] = 73, 18, 2, 5, 20, 60, 0
#         objects["time3"] = 79, 17, 6, 7, 20, 60, 0
#         objects["time4"] = 87, 17, 6, 7, 20, 60, 0
#     info["objects"] = objects
