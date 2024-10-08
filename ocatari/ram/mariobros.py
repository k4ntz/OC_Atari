from typing import Type, Dict, Sequence

from .game_objects import GameObject, ValueObject
from ._helper_methods import _convert_number
import sys



MAX_NB_OBJECTS = {"Player": 1, "Pest": 3, "Fireball": 1, "PowBlock": 1, "BonusBlock": 1, "Platform": 7,
                  "BonusCoin": 8, "Time": 1}

MAX_NB_OBJECTS_HUD = {"Life": 5, "Score": 6}



class Player(GameObject):
    def __init__(self):
        super(Player, self).__init__()
        self._xy = 37, 100
        self.wh = 9, 21
        self.rgb = 181,83,40

        self.hud = False


class Fireball(GameObject):
    def __init__(self):
        super(Fireball, self).__init__()
        self._xy = 154, 84
        self.wh = 9, 14
        self.rgb = 227, 151,89

        self.hud = False


class Platform(GameObject):
    def __init__(self, x=31, y=94, w=97, h=3):
        super(Platform, self).__init__()
        self._xy = x,y
        self.rgb = 228, 111, 111
        self.wh = w, h

        self.hud = False


class PowBlock(GameObject):
    def __init__(self):
        super(PowBlock, self).__init__()
        self._xy = 72,141
        self.wh = 16, 7
        self.rgb = 201, 164,74

        self.hud = False


class Life(GameObject):
    def __init__(self):
        super(Life, self).__init__()
        self._xy = 71, 12
        self.wh = 32, 9
        self.value = 5
        self.rgb = 78, 50, 181

        self.hud = True


class Score(ValueObject):
    def __init__(self):
        super(Score, self).__init__()
        self.xy = 55,12
        self.wh = 48,9
        self.rgb = 78, 50, 181
        self.value = 0
        self.hud = True


class BonusBlock(GameObject):
    def __init__(self):
        super(BonusBlock, self).__init__()
        self._xy = 0,0
        self.rgb = 45, 50, 184
        self.wh = 10,10

        self.hud = False


class Pest(GameObject):
    def __init__(self, x=21, y=23):
        super(Pest, self).__init__()
        self._xy = x, y
        self.wh = 9, 9
        self.rgb = 0,0,0

        self.hud = False


class BonusCoin(GameObject):
    def __init__(self,x=0,y=0):
        super(BonusCoin, self).__init__()
        self._xy = x, y
        self.wh = 9,13
        self.rgb = 104,72,198
        self.hud = False


class Time(ValueObject):
    def __init__(self):
        super(Time, self).__init__()
        self._xy = 72,180
        self.wh = 14, 7
        self.rgb = 204, 216, 110
        self.value = 0
        self.hud = False


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



def _init_objects_ram(hud=True):
    """
    (Re)Initialize the objects
    """

    # Player, PowBlock, Fireball, 3*Pest, 1*BonusBlock, 8*Coins in Bonus Phase
    objects = [Player(), PowBlock(), Fireball()] + [None] * 4 + [None] + [None] * 8 + \
        [Platform(x=0, y=57, w=64),Platform(x=96, y=57, w=68),
         Platform(x=31, y=95, w=97),Platform(x=0, y=95, w=16),Platform(x=144, y=95, w=18),
         Platform(x=0, y=135, w=48),Platform(x=112, y=135, w=48)] + [None]
    if hud:
        objects.extend([Score(), Life()])

    return objects


def _detect_objects_ram(objects, ram_state, hud=True):
    player = objects[0]
    if 128 <= ram_state[27] <= 255:
        player.xy = ram_state[44]-6, ram_state[42]+13
        player.wh = 9, 21
    else:
        player.xy = ram_state[44]-6, ram_state[42]+13
        player.wh = 9, 24

    # Handle Power Block
    if ram_state[121] == 0 and objects[1] is not None:
        objects[1] = None
    elif ram_state[121] > 0 and objects[1] is None:
        objects[1] = PowBlock()

    platforms = objects[16:23]
    if ram_state[120] == 74:
        platforms[5].rgb = 228, 111, 111
        platforms[6].rgb = 228, 111, 111
    elif ram_state[120] == 116:
        platforms[5].rgb = 78, 50, 181
        platforms[6].rgb = 78, 50, 181
    if ram_state[119] == 74:
        platforms[2].rgb = 228, 111, 111
        platforms[3].rgb = 228, 111, 111
        platforms[4].rgb = 228, 111, 111
    elif ram_state[119] == 116:
        platforms[2].rgb = 78, 50, 181
        platforms[3].rgb = 78, 50, 181
        platforms[4].rgb = 78, 50, 181
    if ram_state[118] == 74:
        platforms[0].rgb = 228, 111, 111
        platforms[1].rgb = 228, 111, 111
    elif ram_state[118] == 116:
        platforms[0].rgb = 78, 50, 181
        platforms[1].rgb = 78, 50, 181


    if ram_state[3] == 3:
        coins = objects[8:16]
        
        for i in range(2, len(objects)-18):
            objects[i] = None
        
        time = objects[23]
        if time is None:
            time = Time()
            objects[23] = time
        time.value = _convert_number(ram_state[5])

        coin_positions = [(136,26),(151,68),(98,104),(148,148),
                          (16,26),(1,68),(54,104),(4,148)]
        # left side coins
        for i in range(len(coins)-4):
            if ram_state[101+i] > 0 and objects[8+i] is None:
                coins[i] = BonusCoin(*coin_positions[i])
                objects[8+i] = coins[i]
            elif ram_state[101+i] == 0:
                coins[i] = None
                objects[8+i] = None

        for i in range(len(coins)-4):
            if ram_state[107+i] > 0 and objects[12+i] is None:
                coins[4+i] = BonusCoin(*coin_positions[4+i])
                objects[12+i] = coins[4+i]
            elif ram_state[107+i] == 0:
                coins[4+i] = None
                objects[12+i] = None


    else:
        # turn coins from bonus phase off
        for i in range(8):
            if objects[8+i] is not None:
                objects[8+i] = None
        # set timer for bonus phase to None
        objects[23] = None

        # Handle Enemy
        fireball = objects[2]
        if fireball is None:
            fireball = Fireball()
            objects[2] = fireball
        if ram_state[117] == 0:
            fireball.xy = ram_state[115]-6, 6+24
        if ram_state[117] == 1:
            fireball.xy = ram_state[115]-6, 44+24
        if ram_state[117] == 2:
            fireball.xy = ram_state[115]-6, 84+24
        if ram_state[117] == 3:
            fireball.xy = ram_state[115]-6, 124+24

        bonus_block = objects[7]
        if ram_state[111] != 0:
            if bonus_block is None:
                bonus_block = BonusBlock()
                objects[7] = bonus_block
            bonus_block.xy = ram_state[99]-4, ram_state[93]+26
            bonus_block.wh = 9, 12
        else:
            if bonus_block is not None:
                bonus_block = None
                objects[7] = bonus_block

        # Handle Pests
        pests = objects[3:7]
        for i, pest in enumerate(pests):
            if ram_state[107+i] != 0:
                if pest is None:
                    pest = Pest(x=ram_state[95+i])
                    objects[3+i] = pest
                # handle turtle
                pest.rgb = 136, 146, 62
                if 128 <= ram_state[107+i] <= 131 or ram_state[107+i] == 74:
                    pest.xy = ram_state[95+i]-7, ram_state[89+i]+27
                    pest.wh = 9, 10
                # turtle knocked out (standing)
                elif ram_state[107+i] == 70 or ram_state[107+i] == 72:
                    pest.xy = ram_state[95+i]-7, ram_state[89+i]+24
                    pest.wh = 9, 13

                # handle crab
                elif 146 <= ram_state[107+i] <= 154:
                    pest.xy = ram_state[95+i]-7, ram_state[89+i]+21
                    pest.wh = 10, 17
                    pest.rgb = 198,108,58
                
                # crab knocked out
                elif ram_state[107+i] == 92:
                    pest.xy = ram_state[95+i]-7, ram_state[89+i]+22
                    pest.wh = 10, 15
                    pest.rgb = 198,108,58

                # crab knocked out (large)
                elif ram_state[107+i] == 94:
                    pest.xy = ram_state[95+i]-7, ram_state[89+i]+20
                    pest.wh = 10, 17
                    pest.rgb = 198,108,58


                # handle bunny
                elif 160 <= ram_state[107+i] <= 161:
                    pest.xy = ram_state[95+i]-7, ram_state[89+i]+24
                    pest.wh = 9, 14
                    pest.rgb = 146,70,192
                elif 162 <= ram_state[107+i] <= 163:
                    pest.xy = ram_state[95+i]-7, ram_state[89+i]+25
                    pest.wh = 9, 11
                    pest.rgb = 146,70,192
                elif 164 <= ram_state[107+i] <= 165:
                    pest.xy = ram_state[95+i]-7, ram_state[89+i]+18
                    pest.wh = 9, 14
                    pest.rgb = 146,70,192
                elif 166 <= ram_state[107+i] <= 167:
                    pest.xy = ram_state[95+i]-7, ram_state[89+i]+20
                    pest.wh = 9, 11
                    pest.rgb = 146,70,192
                elif 168 <= ram_state[107+i] <= 169:
                    pest.xy = ram_state[95+i]-7, ram_state[89+i]+19
                    pest.wh = 9, 12
                    pest.rgb = 146,70,192
                elif 170 <= ram_state[107+i] <= 171:
                    pest.xy = ram_state[95+i]-7, ram_state[89+i]+25
                    pest.wh = 9, 11
                    pest.rgb = 146,70,192
                elif ram_state[107+i] == 111:
                    pest.xy = ram_state[95+i]-7, ram_state[89+i]+27
                    pest.wh = 9, 11
                    pest.rgb = 146,70,192

                # handle ice dude    
                elif 176 <= ram_state[107+i] <= 177:
                    pest.xy = ram_state[95+i]-7, ram_state[89+i]+20
                    # Ice dude
                    pest.wh = 10, 17
                    pest.rgb = 101,183,217
                # (114-118)
                elif 114 <= ram_state[107+i] <= 118:
                    pest.xy = ram_state[95+i]-7, ram_state[89+i]+24
                    # Ice dude
                    pest.wh = 10, 13
                    pest.rgb = 101,183,217
                # (120, 122)
                elif 120 <= ram_state[107+i] <= 122:
                    pest.xy = ram_state[95+i]-7, ram_state[89+i]+31
                    # Ice dude
                    pest.wh = 10, 6
                    pest.rgb = 101,183,217
                # (124)
                elif ram_state[107+i] == 124:
                    pest.xy = ram_state[95+i]-7, ram_state[89+i]+34
                    # Ice dude
                    pest.wh = 10, 3
                    pest.rgb = 101,183,217
            else:
                if pest is not None:
                    objects[3+i] = None

    # Handle HUD
    if hud:
        score = objects[-2]
        score.value = _convert_number(ram_state[9]) * 10000 + \
                      _convert_number(ram_state[10]) * 100
        lives = objects[-1]
        nb_lives = ram_state[7]
        if lives is not None and nb_lives != lives.value:
            if nb_lives == 0:
                objects[-1] = None
                return
            else:
                if lives is None:
                    lives = Life()
                    objects[-1] = lives
                lives.value = nb_lives
                lives.xy = 71 + 8 * (5 - nb_lives), 12
                lives.wh = 8 * (nb_lives - 1), 9
