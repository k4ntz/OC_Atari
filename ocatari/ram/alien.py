from .game_objects import GameObject, ValueObject, NoObject
import sys

MAX_NB_OBJECTS = {"Player": 1, "Alien": 12,
                  "Pulsar": 1, "Rocket": 1, "Egg": 156}
MAX_NB_OBJECTS_HUD = {"Player": 1, "Alien": 12, "Pulsar": 1,
                      "Rocket": 1, "Egg": 156, "Score": 1, "Life": 1}

ALIEN_COLORS = [
    (252, 252, 84), # yellow
    (236, 140, 224), # pink
    (132, 144, 252), # blue
    (252, 144, 144), # orange
    (252, 252, 84), # yellow
    (132, 144, 252), # blue
]

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

    objects.extend([NoObject()] * 170)
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
    if ram_state[0] == 0:
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

        if type(objects[4]) is not NoObject:
            for i in range(9):
                objects[4+i] = NoObject()

        pulsar = objects[13]
        if ram_state[103]:
            if not pulsar:
                pulsar = Pulsar()
                objects[13] = pulsar

            if ram_state[103] == 1:
                pulsar.xy = 123, 137
            elif ram_state[103] == 2:
                pulsar.xy = 31, 137
            elif ram_state[103] == 3:
                pulsar.xy = 77, 17
        elif pulsar:
            objects[13] = NoObject()

        rocket = objects[14]
        if ram_state[47]:
            if not rocket:
                rocket = Rocket()
                objects[14] = rocket
            rocket.xy = 17+15*(ram_state[60] & 7), 197-(2*ram_state[47])
        elif rocket:
            objects[14] = NoObject()

    ##############################################
    # ============================================
    ##############################################
        y = 19
        for i in range(13):
            if ram_state[65+i] & 4:
                if type(objects[15+i*6]) is NoObject:
                    objects[15+i*6] = Egg(x=26, y=y)
            else:
                objects[15+i*6] = NoObject()

            if ram_state[65+i] & 8:
                if type(objects[16+i*6]) is NoObject:
                    objects[16+i*6] = Egg(x=56, y=y)
            else:
                objects[16+i*6] = NoObject()

            if ram_state[65+i] & 16:
                if type(objects[17+i*6]) is NoObject:
                    objects[17+i*6] = Egg(x=34, y=y+2)
            else:
                objects[17+i*6] = NoObject()

            if ram_state[65+i] & 32:
                if type(objects[18+i*6]) is NoObject:
                    objects[18+i*6] = Egg(x=64, y=y+2)
            else:
                objects[18+i*6] = NoObject()

            if ram_state[65+i] & 64:
                if type(objects[19+i*6]) is NoObject:
                    objects[19+i*6] = Egg(x=42, y=y+4)
            else:
                objects[19+i*6] = NoObject()

            if ram_state[65+i] & 128:
                if type(objects[20+i*6]) is NoObject:
                    objects[20+i*6] = Egg(x=72, y=y+4)
            else:
                objects[20+i*6] = NoObject()

            y += 12

        y = 19
        for i in range(13):
            if ram_state[78+i] & 4:
                if type(objects[93+i*6]) is NoObject:
                    objects[93+i*6] = Egg(x=89, y=y)
            else:
                objects[93+i*6] = NoObject()

            if ram_state[78+i] & 8:
                if type(objects[94+i*6]) is NoObject:
                    objects[94+i*6] = Egg(x=118, y=y)
            else:
                objects[94+i*6] = NoObject()

            if ram_state[78+i] & 16:
                if type(objects[95+i*6]) is NoObject:
                    objects[95+i*6] = Egg(x=97, y=y+2)
            else:
                objects[95+i*6] = NoObject()

            if ram_state[78+i] & 32:
                if type(objects[96+i*6]) is NoObject:
                    objects[96+i*6] = Egg(x=126, y=y+2)
            else:
                objects[96+i*6] = NoObject()

            if ram_state[78+i] & 64:
                if type(objects[97+i*6]) is NoObject:
                    objects[97+i*6] = Egg(x=105, y=y+4)
            else:
                objects[97+i*6] = NoObject()

            if ram_state[78+i] & 128:
                if type(objects[98+i*6]) is NoObject:
                    objects[98+i*6] = Egg(x=134, y=y+4)
            else:
                objects[98+i*6] = NoObject()

            y += 12
    else: # 32 or 48 for the dark mode
        if type(objects[6]) is NoObject:
            for i in range(170):
                objects[1+i] = NoObject()
        
        for i, color in enumerate(ALIEN_COLORS):
            if type(objects[1+(2*i)]) is NoObject:
                objects[1+(2*i)] = Alien()
                objects[2+(2*i)] = Alien()
            if ram_state[66+i]&128:
                x = 20 + ((ram_state[66+i]&15)<<4) - (ram_state[66+i]>>4)
            else:
                x = 4 + ((ram_state[66+i]&15)<<4) - (ram_state[66+i]>>4)
            x = x + ((88 - x)>>4)
            objects[1+(2*i)].xy = x, 37+20*i
            objects[2+(2*i)].xy = x+32, 37+20*i
            objects[1+(2*i)].rgb = color
            objects[2+(2*i)].rgb = color
        rocket = objects[14]
        if ram_state[73] == 131:
            if not rocket:
                rocket = Rocket()
                objects[14] = rocket
            rocket.xy = 77, 19
            rocket.rgb = 132, 252, 112
        elif rocket:
            objects[14] = NoObject()

    if hud:
        score = objects[171]
        score.xy = 63, 176
        score.wh = 6, 7
        x = 23
        w = 46
        value = 0
        for i in range(5):
            if ram_state[11-2*i] != 128:
                score.xy = x, 176
                score.wh = w, 7
                value += (ram_state[11-2*i] // 8) * 10**(i+1)
            else:
                x += 8
                w -= 8
        value += ram_state[13] // 8
        score.value = value

        lives_v = ram_state[64] - 1
        life = objects[172]
        if lives_v:
            if not life:
                life = Life()
                objects[172] = life
            life.wh = 5 + 8*(lives_v-1), 5
            life.value = lives_v
        else:
            objects[172] = NoObject()


def _detect_objects_alien_raw(info, ram_state):
    """
    returns unprocessed list with
    ball_x, ball_y, enemy_y, player_y
    """
    info["objects_list"] = ram_state[32:36]

