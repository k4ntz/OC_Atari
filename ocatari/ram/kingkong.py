import sys
from .game_objects import GameObject, NoObject


MAX_NB_OBJECTS = {"Player": 1, "Enemy": 1,
                  "Girlfriend": 1, "Bomb": 8, "Ladder": 12}

MAX_NB_OBJECTS_HUD = {"Player": 1, "Enemy": 1, "Girlfriend": 1, "Bomb": 8, "Ladder": 12,
                      "Score": 1, "BonusPoints": 1}


class Player(GameObject):
    def __init__(self):
        super(Player, self).__init__()
        self._xy = 38, 94
        self.wh = 5, 17
        self.rgb = 92, 197, 135
        self.hud = False


class Girlfriend(GameObject):
    def __init__(self):
        super(Girlfriend, self).__init__()
        self._xy = 95, 28
        self.wh = 6, 17
        self.rgb = 50, 50, 176
        self.hud = False


class Enemy(GameObject):
    def __init__(self):
        super(Enemy, self).__init__()
        self._xy = 51, 94
        self.wh = 14, 35
        self.rgb = 150, 113, 26
        self.hud = False


class Bomb(GameObject):
    def __init__(self, x=0, y=0):
        super(Bomb, self).__init__()
        self._xy = x, y
        self.wh = 6, 17
        self.rgb = 50, 50, 176
        self.hud = False


class Ladder(GameObject):
    def __init__(self, x=140, y=207):
        super(Ladder, self).__init__()
        self._xy = x, y
        self.wh = 8, 18
        self.rgb = 201, 92, 135
        self.hud = False


class Score(GameObject):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


class BonusPoints(GameObject):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


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
    ladder_positions = [(140, 207), (12, 207), (76, 183), (140, 159), (12, 159), (76, 135),
                        (140, 111), (12, 111), (76, 87), (132, 63), (20, 63), (76, 43)]
    objects = [Player(), Enemy(), Girlfriend()] + [NoObject()] * 8 + \
        [Ladder(x=pos[0], y=pos[1]) for pos in ladder_positions]

    if hud:
        objects.extend([Score(), BonusPoints()])
    return objects


def _detect_objects_ram(objects, ram_state, hud=True):
    # bombs 51 - 60 and 41 - 48 (but no so important I guess)
    # player (x=36, y=33) but 39 does also something to it (flips to 10 and 19)
    # 60+i is type of bomb

    enemy = objects[1]
    if ram_state[39] != 94:
        player_x_cell = ram_state[36]
        player_y_cell = ram_state[33]
        enemy._xy = 31, 49
    else:
        player_x_cell = ram_state[35]
        player_y_cell = ram_state[32]
        enemy._xy = 31, 193

    player = objects[0]
    player_x_cell = ram_state[36] if ram_state[39] != 94 else ram_state[35]
    if player_x_cell&128:
        player_x = 20 + ((player_x_cell&15)<<4) - (player_x_cell>>4)
    else:
        player_x = 4 + ((player_x_cell&15)<<4) - (player_x_cell>>4)
    player_x = player_x + ((88 - player_x)>>4) - 20

    player_y = 2*player_y_cell + 24
    

    player._xy = player_x, player_y # ((ram_state[33]&15)<<4) - (ram_state[33]>>4)

    # girlfriend x=76
    platform_y = [43, 63, 87, 111, 135, 159, 183, 207]

    for i in range(8):

        if ram_state[42+i] != 255:
            if type(objects[3+i]) is NoObject:
                objects[3+i] = Bomb()
            if ram_state[51+i]&128:
                x = 20 + ((ram_state[51+i]&15)<<4) - (ram_state[51+i]>>4)
            else:
                x = 4 + ((ram_state[51+i]&15)<<4) - (ram_state[51+i]>>4)

            x = x + ((88 - x)>>4) - 20

            

            objects[3+i]._xy = x, 43
        else:
            objects[3+i] = NoObject()
        
    if hud:
        pass
