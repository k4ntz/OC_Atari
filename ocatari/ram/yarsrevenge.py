from .game_objects import GameObject, ValueObject
import sys

"""
RAM extraction for the game Yars' Revenge.
"""

MAX_NB_OBJECTS = {"Player": 1}
MAX_NB_OBJECTS_HUD = {}  # 'Score': 1}


class Player(GameObject):
    """
    The player figure i.e., the Yar.
    """

    def __init__(self):
        super().__init__()
        self._xy = 0, 0
        self.wh = (8, 16)
        self.rgb = 169, 128, 240
        self.hud = False


class Enemy(GameObject):
    """
    The enemy Qotile.
    """

    def __init__(self):
        super().__init__()
        self._xy = 0, 0
        self.wh = (8, 18)
        self.rgb = 240, 240, 240
        self.hud = False


class Swirl(GameObject):
    """
    The Qotile when transformed into a Swirl, charging at the player.
    """

    def __init__(self):
        super().__init__()
        self._xy = 0, 0
        self.wh = (8, 18)
        self.rgb = 169, 128, 240
        self.hud = False


class Enemy_Missile(GameObject):
    """
    The Destroyer Missles fired by the Qotile.
    """

    def __init__(self):
        super().__init__()
        self._xy = 0, 0
        self.wh = (4, 2)
        self.rgb = 169, 128, 240
        self.hud = False


class Barrier(GameObject):
    """
    The colorful and glittering neutral zone.
    """

    def __init__(self):
        super().__init__()
        self._xy = 0, 0
        self.wh = (28, 190)
        self.rgb = 250, 250, 250
        self.hud = False


class Player_Bullet(GameObject):
    """
    The Energy Missles fired by the player.
    """

    def __init__(self):
        super().__init__()
        self._xy = 0, 0
        self.wh = (1, 2)
        self.rgb = 169, 128, 240
        self.hud = False


class Shield_Block(GameObject):
    """
    The cells of the energy shield protecting the Qotile.
    """

    def __init__(self):
        super().__init__()
        self._xy = 0, 0
        self.wh = 4, 8
        self.rgb = 163, 57, 21
        self.hud = False


class Score(ValueObject):
    def __init__(self):
        super(Score, self).__init__()
        self._xy = 0, 0
        self.wh = (7, 7)
        self.rgb = 78, 50, 181
        self.hud = False


class Life(GameObject):
    def __init__(self):
        super(Life, self).__init__()
        self._xy = 0, 0
        self.wh = (7, 7)
        self.rgb = 78, 50, 181
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
    objects = []

    objects.extend([None] * 135)
    if hud:
        objects.extend([None] * 7)
    return objects


def _detect_objects_ram(objects, ram_state, hud=False):
    """
    For all 3 objects:
    (x, y, w, h, r, g, b)
    """
    if ram_state[53] > 159:
        player = Player()
        objects[0] = player
        player.xy = ram_state[32], ram_state[31]+3
        if ram_state[43] >= 145:
            enemy = Enemy()
            enemy.xy = ram_state[43], ram_state[42]+3
            objects[2] = None
            objects[1] = enemy
        else:
            swirl = Swirl()
            swirl.xy = ram_state[43]+4, ram_state[42]+3
            objects[2] = swirl
            objects[1] = None
        # Enemy Missile
        e_m = Enemy_Missile()
        e_m.xy = ram_state[47], ram_state[46]+2
        objects[3] = e_m
        # Player Missile
        if abs(ram_state[38]-3-ram_state[32]) > 5 and abs(ram_state[37]-ram_state[31]) > 5:
            p_m = Player_Bullet()
            p_m.xy = ram_state[38]-1, ram_state[37]+4
            objects[5] = p_m
        else:
            objects[5] = None
        # Adding Barrier
        if ram_state[53] > 159:
            b = Barrier()
            b.xy = 52, 4
            objects[4] = b
        else:
            objects[4] = None

        # blocks ram 0 to 16 binary coding lsb left to msb right

        for j in range(16):
            for i in range(8):
                if ram_state[j+1] & 2**i:
                    block = Shield_Block()
                    objects[5+(i+(j*8))] = block
                    if j == 15:
                        block.xy = 128 + (i*4), ram_state[26] + 122 - (j*8)
                        block.wh = 4, 7
                    else:
                        block.xy = 128 + (i*4), ram_state[26] + 121 - (j*8)
                else:
                    objects[5+(i+(j*8))] = None
    else:
        objects[0:] = [None]*172

        if hud:
            # scores ram: 96-98 lives 99
            if ram_state[96] > 15:
                score = Score()
                objects[0] = score
                score.xy = 55, 47
                score.wh = 47, 7
            elif ram_state[96]:
                score = Score()
                objects[0] = score
                score.xy = 63, 48
                score.wh = 39, 7
            elif ram_state[97] > 15:
                score = Score()
                objects[0] = score
                score.xy = 71, 48
                score.wh = 31, 7
            elif ram_state[97]:
                score = Score()
                objects[0] = score
                score.xy = 79, 48
                score.wh = 23, 7
            elif ram_state[98] > 15:
                score = Score()
                objects[0] = score
                score.xy = 87, 48
                score.wh = 15, 7
            elif ram_state[98]:
                score = Score()
                objects[0] = score
                score.xy = 95, 48
                score.wh = 7, 7

            life = Life()
            objects[1] = life
            life.xy = 95, 74
