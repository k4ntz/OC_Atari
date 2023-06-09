from .game_objects import GameObject
from ._helper_methods import _convert_number
import math


class Player(GameObject):
    class Player(GameObject):
        def __init__(self):
            super().__init__()
            self.rgb = 187, 187, 53
            self._xy = 0, 0
            self.wh = 8, 11  # at some point 16, 11. advanced other player (oblix) is (6, 11)
            self.hud = False


class Cauldron(GameObject):
    def __init__(self):
        super().__init__()
        self.rgb = 167, 26, 26
        self._xy = 0, 0
        self.wh = 7, 10
        self.hud = False


class Enemy(GameObject):
    def __init__(self):
        super().__init__()
        self.rgb = 228, 111, 111
        self._xy = 0, 0
        self.wh = 7, 11
        self.hud = False


class Score(GameObject):
    def __init__(self):
        super().__init__()
        self.rgb = 187, 187, 53
        self._xy = 0, 0
        self.wh = 8, 11
        self.hud = True


class Lives(GameObject):
    def __init__(self):
        super().__init__()
        self.rgb = 187, 187, 53
        self._xy = 0, 0
        self.wh = 6, 7
        self.hud = True


class Helmet(GameObject):
    def __init__(self):
        super().__init__()
        self.rgb = 240, 128, 128
        self._xy = 0, 0
        self.wh = 7, 11
        self.hud = False


class Shield(GameObject):
    def __init__(self):
        super().__init__()
        self.rgb = 214, 214, 214
        self._xy = 0, 0
        self.wh = 5, 11
        self.hud = False


class Lamp(GameObject):
    def __init__(self):
        super().__init__()
        self.rgb = 187, 53, 53
        self._xy = 0, 0
        self.wh = 8, 11
        self.hud = False


class Apple(GameObject):
    def __init__(self):
        super().__init__()
        self.rgb = 184, 50, 50
        self._xy = 0, 0
        self.wh = 8, 11
        self.hud = False


class Fish(GameObject):
    def __init__(self):
        super().__init__()
        self.rgb = 198, 89, 179
        self._xy = 0, 0
        self.wh = 8, 5
        self.hud = False


class Meat(GameObject):
    def __init__(self):
        super().__init__()
        self.rgb = 184, 50, 50
        self._xy = 0, 0
        self.wh = 5, 11
        self.hud = False


class Mug(GameObject):
    def __init__(self):
        super().__init__()
        self.rgb = 184, 50, 50
        self._xy = 0, 0
        self.wh = 7, 11
        self.hud = False


class Reward50(GameObject):
    def __init__(self):
        super().__init__()
        self.rgb = 198, 89, 179
        self._xy = 0, 0
        self.wh = 6, 11
        self.hud = False


class Reward100(GameObject):
    def __init__(self):
        super().__init__()
        self.rgb = 135, 183, 84
        self._xy = 0, 0
        self.wh = 8, 11
        self.hud = False


class Reward200(GameObject):
    def __init__(self):
        super().__init__()
        self.rgb = 195, 144, 61
        self._xy = 0, 0
        self.wh = 8, 11
        self.hud = False


class Reward300(GameObject):
    def __init__(self):
        super().__init__()
        self.rgb = 213, 130, 74
        self._xy = 0, 0
        self.wh = 8, 11
        self.hud = False


class Reward400(GameObject):
    def __init__(self):
        super().__init__()
        self.rgb = 135, 183, 84
        self._xy = 0, 0
        self.wh = 8, 11
        self.hud = False


class Reward500(GameObject):
    def __init__(self):
        super().__init__()
        self.rgb = 163, 57, 21
        self._xy = 0, 0
        self.wh = 8, 11
        self.hud = False


def _init_objects_asterix_ram(hud=False):
    """
    (Re)Initialize the objects
    """
    objects = [Player()]
    if hud:
        objects.extend([Score(), Lives(), Lives()])

    return objects


def _detect_objects_asterix_raw(info, ram_state):
    info["x_positions"] = ram_state[41:50]  # 41 for player, 42 for obj in upper lane...
    info["y_player"] = ram_state[39]  # from 0 to 7 (8 lanes)
    info["score"] = ram_state[94:97]  # on ram in decimal/ on screen in hex(like other 2 games)
    info["score_dec"] = ram_state[94:97]
    info["lives"] = ram_state[83]
    info["kind_of_visible_objs"] = ram_state[54] % 8
    info["rewards_visible"] = ram_state[73:81]
    info["enemy_or_eatable_object"] = ram_state[29:37] % 2  # = 1 for enemy

    # info["maybe_useful"] = ram_state[10:18], ram_state[40], ram_state[19:27], ram_state[29:37], ram_state[87],
    # ram_state[7]
    # not known what they are for exactly
    print(ram_state)


class rev:
    """
    to save values temporarily
    """
    prevRam = []
    lanes = {}

    def __init__(self, prevRam, lanes):
        self.prevRam = prevRam  # saving last ram
        self.lanes = lanes  # saving current objs


def _create_obj(i, level, array, rev_inst):
    if array[i] % 2 == 1:  # create Enemy
        rev_inst.lanes[i] = Enemy()
    else:  # create eatable
        if level == 0:
            rev_inst.lanes[i] = Cauldron()
        elif level == 1:
            rev_inst.lanes[i] = Helmet()
        elif level == 2:
            rev_inst.lanes[i] = Shield()
        elif level == 3:
            rev_inst.lanes[i] = Lamp()
        elif level == 4:
            rev_inst.lanes[i] = Apple()
        elif level == 5:
            rev_inst.lanes[i] = Fish()
        elif level == 6:
            rev_inst.lanes[i] = Meat()
        elif level == 7:
            rev_inst.lanes[i] = Mug()
    rev_inst.lanes[i].xy = array[i], 26 + i * 16  # specific poses we give in part updating in calling function
    print("new object created:", rev_inst.lanes[0])
    # return rev_inst


def _detect_objects_asterix_revised(objects, ram_state, hud=False):
    """
    we work on objects in lanes from class rev. And hand these to objects at the end
    """
    if not isinstance(objects[-1], rev):
        rev_inst = rev(ram_state, {})
    else:
        rev_inst = objects[-1]

    ram = ram_state

    # old = rev_inst.old_objs
    lives_nr = ram[83]
    level = ram[54]
    prev = rev_inst.prevRam
    # lanes = rev_inst.lanes  # STRUCTURE: should look like [objs, player, score, lives]
    reward_class = (Reward50, Reward100, Reward200, Reward300, Reward400, Reward500)  # , Reward500, Reward500)
    eatable_class = (Cauldron, Helmet, Shield, Lamp, Apple, Fish, Meat, Mug)
    if not prev == [] and not ram[12] == prev[12]:  # ram[12] decreases by 1 when all objects disappear (player died)
        for i in range(8):
            rev_inst.lanes[i] = None

    if rev_inst.lanes == {}:  # initializing lanes (works correctly)
        for i in range(8):  # objs
            _create_obj(i, level, ram[29:37], rev_inst)  # (here it was creating Cauldrons, which is correct)
            # print(rev_inst.lanes[i])
        for i in range(2):  # player, score
            rev_inst.lanes[i + 8] = objects[i]
        for i in range(2):  # lives (max 2 symbols)
            rev_inst.lanes[i + 10] = Lives()
            rev_inst.lanes[i + 10].xy = 60 + i * 16, 169
            rev_inst.lanes[i + 10].wh = 8, 11
        rev_inst.lanes[8].rgb = 187, 187, 53  # giving player his color (so we see the rectangle!)

    # ####  from now we edit the objects in the lanes which are in dictionary "lanes" #### #

    # 1- here we only delete rewards and disappearing enemies (nothing appears after then)
    if not prev == []:  # (for the first iteration)
        for i in range(8):  # all possible objs are 8 (so going through rev_inst.lanes)
            # for rew in reward_class:
            #     print("checking rew classes")
            #     if isinstance(rev_inst.lanes[i], rew):
            if isinstance(rev_inst.lanes[i], reward_class):
                # because there could be more than one kind reward in one frame
                if not prev[42 + i] == ram[42 + i]:  # so reward moved => disappeared
                    # del rev_inst.lanes[i]
                    # rev_inst.lanes[i] = None  # delete reward
                    rev_inst.lanes[i] = int(ram[42 + i]) - int(prev[42 + i])  # here we're deleting anyway
                    print("deleting rew")
                    # this int value does not get edited later only compared and then just replaced with moving obj
            if isinstance(rev_inst.lanes[i], Enemy):  # if enemy
                if prev[42 + i] == ram[42 + i]:  # if stopped
                    rev_inst.lanes[i] = None  # delete Enemy
    # til here we have deleted the disappearing rews/enemies

    # creating new rewards
    for i in range(8):
        if ram[73 + i]:  # ->there is rew in this lane. (actual values 1-8)
            if not isinstance(rev_inst.lanes[i], int) and rev_inst.lanes[i] is not None:  # -> object has been moving
                # ~if there is None in lanes so don't create reward
                # current moving obj (enemy/eatable) get replaced with a reward
                if level == 0:
                    rev_inst.lanes[i] = Reward50()
                elif level == 1:
                    rev_inst.lanes[i] = Reward100()
                elif level == 2:
                    rev_inst.lanes[i] = Reward200()
                elif level == 3:
                    rev_inst.lanes[i] = Reward300()
                elif level == 4:
                    rev_inst.lanes[i] = Reward400()
                else:
                    rev_inst.lanes[i] = Reward500()
                rev_inst.lanes[i].xy = ram[42 + i], 26 + i * 16
                # we see if we need to specify this value. I guess it is enough to test for 100_rew

    # now we initiate moving objs WHILE PLAYING NOT FROM BEGINNING
    for i in range(8):
        if isinstance(rev_inst.lanes[i], int):
            if (ram[42 + i] - prev[42 + i]) * rev_inst.lanes[i] < 0 or rev_inst.lanes[i] < 0 and ram[42 + i] > 137:
                # ~ IF diff directions OR negative diff AND new obj is on the right side
                # create objs
                _create_obj(i, level, ram[29:37], rev_inst)  # standard

    # print(rev_inst.lanes)
    # UPDATING pos of objs  # works correctly
    for i in range(8):
        if rev_inst.lanes[i] and not isinstance(rev_inst.lanes[i], int):
            if isinstance(rev_inst.lanes[i], Cauldron):
                rev_inst.lanes[i].xy = ram[42 + i] + 1, 26 + i * 16 + 1
            else:
                rev_inst.lanes[i].xy = ram[42 + i], 26 + i * 16

    # if while playing we have new level but objects exist and are moving(they simply turn into new ones)
    if level > prev[54]:
        for i in range(8):
            if isinstance(rev_inst.lanes[i], eatable_class):
                _create_obj(i, level, ram[42:50], rev_inst)

    player = rev_inst.lanes[8]  # works correctly
    player.xy = ram[41], 26 + ram[39] * 16
    if ram[71] < 82:
        if level < 5:  # asterix playing
            player.wh = 8, 11
        else:  # obelix playing
            player.wh = 6, 11
    else:  # player is wide(is dying)
        player.wh = 16, 11

    if hud:
        score = rev_inst.lanes[9]
        dec_value = _convert_number(ram_state[94]) * 10000 + _convert_number(ram_state[95]) * 100 + _convert_number(
            ram_state[96])
        if dec_value == 0:
            score.xy = 96, 184
            score.wh = 6, 7
        else:
            digits = int(math.log10(dec_value))
            score.xy = 96 - digits * 8, 184
            score.wh = 6 + digits * 8, 7

        # here we are deleting lives if they disappeared
        for i in range(2):  # works correctly
            if isinstance(rev_inst.lanes[10 + i], Lives):
                if lives_nr <= i + 1:
                    rev_inst.lanes[10 + i] = None

    del objects[:]  # works correctly (deleting refs no objs)
    # print(rev_inst.lanes)
    # print(ram)
    for i in range(len(rev_inst.lanes)):
        if rev_inst.lanes[i] is not None and not isinstance(rev_inst.lanes[i], int):
            objects.append(rev_inst.lanes[i])
    print(len(objects))
    objects.append(rev_inst)  # so we guarantee that rev_inst does not get deleted
    prev = ram

    # we don't need at beginning to check which objs we had in "objects". because we have already their references in
    # rev_inst.lanes we do all the editing in this function
