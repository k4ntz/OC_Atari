from .game_objects import GameObject, ValueObject, NoObject
from ._helper_methods import _convert_number
import sys

MAX_NB_OBJECTS = {"Player": 1, "Player_Projectile": 1, "Enemy_Projectile": 4, "Phoenix": 8, "Bat": 7,
                  "Boss": 1, "Boss_Block_Green": 2, "Boss_Block_Blue": 48, "Boss_Block_Red": 104}
MAX_NB_OBJECTS_HUD = {"Player": 1, "Player_Projectile": 1, "Enemy_Projectile": 4, "Phoenix": 8, "Bat": 7, "Boss": 1,
                      "Boss_Block_Green": 2, "Boss_Block_Blue": 48, "Boss_Block_Red": 104, "Score": 1, "Life": 5}


class Player(GameObject):
    """
    Player shooting at the enemies above while doging bullets
    """

    def __init__(self):
        super(Player, self).__init__()
        self._xy = 76, 100
        self.wh = (7, 10)
        self.rgb = 213, 130, 74
        self.hud = False


class Player_Projectile(GameObject):
    """
    Player projectile. Only one can be on screen at a time
    """

    def __init__(self):
        super(Player_Projectile, self).__init__()
        self._xy = 76, 100
        self.wh = (1, 6)
        self.rgb = 158, 208, 101
        self.hud = False


class Phoenix(GameObject):
    """
    Phoenixes of the first 2 rounds
    """

    def __init__(self):
        super(Phoenix, self).__init__()
        self._xy = 76, 100
        self.wh = (8, 8)
        self.rgb = 227, 151, 89
        self.hud = False


class Enemy_Projectile(GameObject):
    """
    Projectiles shot by the enemy.
    """

    def __init__(self):
        super(Enemy_Projectile, self).__init__()
        self._xy = 76, 100
        self.wh = (1, 6)
        self.rgb = 227, 151, 89
        self.hud = False


class Bat(GameObject):
    """
    Bat like enemies, they have wings that can be shot off.
    The wing Attribute is a bit representation of still to the bat attached wings
    3 (11) -> both wings, 2 (10) -> only left wing, 1 (01) -> only right wing
    Orientation 0 -> bat going left, orientation 1 -> bat going right
    """

    def __init__(self):
        super(Bat, self).__init__()
        self._xy = 76, 100
        self.wh = (8, 10)
        self.rgb = 24, 26, 167
        self.hud = False
        self.wing = 3
        self.orientation = 0


class Boss(GameObject):
    """
    Boss, appears every 5 levels
    """

    def __init__(self):
        super(Boss, self).__init__()
        self._xy = 76, 100
        self.wh = (8, 11)
        self.rgb = 24, 59, 157
        self.hud = False


class Boss_Block_Green(GameObject):
    """
    Indestructable, next to the boss
    """

    def __init__(self):
        super(Boss_Block_Green, self).__init__()
        self._xy = 76, 100
        self.wh = (20, 15)
        self.rgb = 135, 183, 84
        self.hud = False


class Boss_Block_Blue(GameObject):
    """
    2 rows of blocks moving from left to right. Can be destroyed
    """

    def __init__(self, x=0, y=0, *args, **kwargs):
        super(Boss_Block_Blue, self).__init__()
        self._xy = x, y
        self.wh = (4, 3)
        self.rgb = 45, 87, 176
        self.hud = False


class Boss_Block_Red(GameObject):
    """
    Static block, first defense of the boss. Can be destroyed
    """

    def __init__(self, x=0, y=0, *args, **kwargs):
        super(Boss_Block_Red, self).__init__()
        self._xy = x, y
        self.wh = (4, 3)
        self.rgb = 167, 26, 26
        self.hud = False


class Score(ValueObject):
    """
    Players points in the game
    """

    def __init__(self):
        super(Score, self).__init__()
        self._xy = 95, 5
        self.wh = (7, 7)
        self.rgb = 180, 231, 117
        self.hud = True
        self.value = 0


class Life(ValueObject):
    """
    Players points in the game
    """

    def __init__(self):
        super(Life, self).__init__()
        self._xy = 99, 13
        self.wh = (3, 5)
        self.rgb = 213, 130, 74
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
    objects.extend([NoObject()] * 184)

    if hud:
        objects.extend([Score(), NoObject()])
    return objects


def _detect_objects_ram(objects, ram_state, hud=False):
    """
    For all 3 objects:
    (x, y, w, h, r, g, b)
    """

    # ram[37-40] == x, ram[33-36] == y, odd player, even enemy
    # x == 69 -> 80, x == 80 -> 91
    # y == 100 -> 59, y == 99 -> 60

    # ram[94] == player_x
    objects[0].xy = ram_state[94] - 70, 173

    if not ram_state[84]:
        if type(objects[1]) is NoObject:
            objects[1] = Player_Projectile()
        objects[1].xy = ram_state[93] - 71, 201 - ram_state[89]
    else:
        objects[1] = NoObject()

    for i in range(4):
        if ram_state[58+i] < 250:
            left = ram_state[80+i] >> 4
            right = ram_state[80+i] & 15
            if left & 8:
                x = 5 + (right-3) * 15 + (left ^ 15) + 1
            else:
                x = 5 + (right-3) * 15 - left
            if type(objects[2+i]) is NoObject:
                objects[2+i] = Enemy_Projectile()
            objects[2+i].xy = x, 189 - ram_state[58+i]
        else:
            objects[2+i] = NoObject()

    if ram_state[74] < 4: #ram_state[11]:
        # ram[99-106] == enemy_x
        # ram[41-44] == enemy_y, ram[41] corresponds to ram[99] and ram[103] and so on
        # ram[27-30] == left side types, ram[34-37] == right side types

        if ram_state[27] & 64:
            if ram_state[27] & 32:
                rgb = 158, 208, 101
            else:
                # orange
                rgb = 227, 151, 89
            for i in range(4):
                enemy = objects[6+i]
                enemy2 = objects[10+i]

                # left side enemies
                if ram_state[27+i] & 6 == 6:
                    objects[6+i] = NoObject()
                else:
                    if type(enemy) is NoObject:
                        enemy = Phoenix()
                        objects[6+i] = enemy
                    enemy.rgb = rgb
                    # enemy.xy = ram_state[99+i] - 70, 204 - ram_state[41+i]
                    enemy.xy = ram_state[99+i] - 70, 204 - ram_state[41+i]

                # right side enemies
                if ram_state[34+i] & 6 == 6:
                    objects[10+i] = NoObject()
                else:
                    if type(enemy2) is NoObject:
                        enemy2 = Phoenix()
                        objects[10+i] = enemy2
                    enemy2.rgb = rgb
                    enemy2.xy = ram_state[103+i] - 70, 204 - ram_state[41+i]
            
            # remove all bats
            for i in range(14, 20):
                objects[i] = NoObject()

        else:
            # ram[27-33] == left wing, ram[34-40] == right wing
            if ram_state[27] & 32:
                # red
                rgb = 167, 26, 26
            else:
                # blue
                rgb = 24, 26, 167
            for i in range(7):
                wing_left = ram_state[27+i] & 15
                if wing_left < 8:
                    if type(objects[14+i]) is NoObject:
                        bat = Bat()
                    else:
                        bat = objects[14+i]
                    x = ram_state[99+i] - 65
                    w, h = 8, 10
                    # left wing
                    if wing_left < 7:
                        if wing_left == 3:
                            x -= 3
                            w += 2
                            h += 1
                        elif wing_left == 6:
                            x -= 4
                            w += 4
                            h -= 1
                        else:
                            x -= 4
                            w += 4
                    else:
                        bat.wing = 1

                    # right wing

                    wing_right = ram_state[34+i] & 15
                    if wing_right < 7:
                        if wing_right == 3:
                            w += 4
                        else:
                            w += 4
                    else:
                        bat.wing = bat.wing & 2

                    # bat orientation
                    if ram_state[63] & 2**i:
                        x -= 2
                        bat.orientation = 1

                    bat.xy = x, 201 - ram_state[41+i]
                    bat.wh = w, h
                    bat.rgb = rgb
                    objects[14+i] = bat

                else:
                    objects[14+i] = NoObject()
            # remove all phoenixes
            for i in range(5, 14):
                objects[i] = NoObject()
        # remove all boss phase objects
        if type(objects[21]) is not NoObject:
            for i in range(21, 184):
                objects[i] = NoObject()
    else:
        for i in range(6, 21):
            objects[i] = NoObject()
        # boss -> ram[33-46] == red blocks, ram[27-32] == blue blocks (moving one block every time)
        # ram[95] == boss_y
        if type(objects[21]) is NoObject:
            objects[21] = Boss()
        objects[21].xy = 76, 198 - ram_state[95]

        # indestructable blocks, simple implementation
        if type(objects[22]) is NoObject:
            objects[22] = Boss_Block_Green()
        objects[22].xy = 56, 199 - ram_state[95]
        if type(objects[23]) is NoObject:
            objects[23] = Boss_Block_Green()
        objects[23].xy = 84, 199 - ram_state[95]

        # Outer blocks of first 2 blue rows
        left1 = ram_state[27] >> 4
        right1 = ram_state[27] & 15
        left2 = ram_state[30] >> 4
        right2 = ram_state[30] & 15
        for i in range(4):
            if 2**(3-i) & left1:
                if type(objects[24+i]) is NoObject:
                    objects[24+i] = Boss_Block_Blue()
                objects[24+i].xy = 32+i*4, 214 - ram_state[95]
            else:
                objects[24+i] = NoObject()

            if 2**i & right1:
                if type(objects[28+i]) is NoObject:
                    objects[28+i] = Boss_Block_Blue()
                objects[28+i].xy = 112+i*4, 214 - ram_state[95]
            else:
                objects[28+i] = NoObject()

            if 2**(3-i) & left2:
                if type(objects[32+i]) is NoObject:
                    objects[32+i] = Boss_Block_Blue()
                objects[32+i].xy = 32+i*4, 216 - ram_state[95]
            else:
                objects[32+i] = NoObject()

            if 2**i & right2:
                if type(objects[36+i]) is NoObject:
                    objects[36+i] = Boss_Block_Blue()
                objects[36+i].xy = 112+i*4, 216 - ram_state[95]
            else:
                objects[36+i] = NoObject()

        # left side of blue blocks
        states = [28, 31]
        for i in range(2):
            for j in range(8):
                if ram_state[states[i]] & (2**j):
                    if type(objects[40+j+(8*i)]) is NoObject:
                        objects[40+j+(8*i)] = Boss_Block_Blue()
                    objects[40+j+(8*i)].xy = 48 + j*4, 214+(3*i) - ram_state[95]
                else:
                    objects[40+j+(8*i)] = NoObject()

        # righte side of blue block
        states = [29, 32]
        for i in range(2):
            for j in range(8):
                if ram_state[states[i]] & (2**(7-j)):
                    if type(objects[56+j+(8*i)]) is NoObject:
                        objects[56+j+(8*i)] = Boss_Block_Blue()
                    objects[56+j+(8*i)].xy =80 + j*4, 214+(3*i) - ram_state[95]
                else:
                    objects[56+j+(8*i)] = NoObject()

        # Outer blocks of first 2 red rows
        left1 = ram_state[33] >> 4
        right1 = ram_state[33] & 15
        left2 = ram_state[36] >> 4
        right2 = ram_state[36] & 15
        for i in range(4):
            if 2**(3-i) & left1:
                if type(objects[72+i]) is NoObject:
                    objects[72+i] = Boss_Block_Red()
                objects[72+i].xy = 32+i*4, 218 - ram_state[95]
            else:
                objects[72+i] = NoObject()

            if 2**i & right1:
                if type(objects[76+i]) is NoObject:
                    objects[76+i] = Boss_Block_Red()
                objects[76+i].xy = 112+i*4, 218 - ram_state[95]
            else:
                objects[76+i] = NoObject()

            if 2**(3-i) & left2:
                if type(objects[80+i]) is NoObject:
                    objects[80+i] = Boss_Block_Red()
                objects[80+i].xy = 32+i*4, 221 - ram_state[95]
            else:
                objects[80+i] = NoObject()

            if 2**i & right2:
                if type(objects[84+i]) is NoObject:
                    objects[84+i] = Boss_Block_Red()
                objects[84+i].xy = 112+i*4, 221 - ram_state[95]
            else:
                objects[84+i] = NoObject()

        # left side of red blocks
        states = [34, 37, 39, 41, 43]
        for i in range(5):
            for j in range(8):
                if ram_state[states[i]] & (2**j):
                    if type(objects[88+j+(8*i)]) is NoObject:
                        objects[88+j+(8*i)] = Boss_Block_Red()
                    objects[88+j+(8*i)].xy = 48+j * 4, 218+(3*i) - ram_state[95]
                else:
                    objects[88+j+(8*i)] = NoObject()

        # righte side of red block
        states = [35, 38, 40, 42, 44]
        for i in range(5):
            for j in range(8):
                if ram_state[states[i]] & (2**(7-j)):
                    if type(objects[128+j+(8*i)]) is NoObject:
                        objects[128+j+(8*i)] = Boss_Block_Red()
                    objects[128+j+(8*i)].xy = 80 + j*4, 218+(3*i) - ram_state[95]
                else:
                    objects[128+j+(8*i)] = NoObject()

        # last 2 rows
        for i in range(2):
            left = ram_state[45+i] >> 4
            right = ram_state[45+i] & 15
            for j in range(4):
                if (2**j) & left:
                    if type(objects[168+j+(8*i)]) is NoObject:
                        objects[168+j+(8*i)] = Boss_Block_Red()
                    objects[168+j+(8*i)].xy = 64 + j*4, 233+(3*i) - ram_state[95]
                else:
                    objects[168+j+(8*i)] = NoObject()

                if (2**(3-j)) & right:
                    if type(objects[172+j+(8*i)]) is NoObject:
                        objects[172+j+(8*i)] = Boss_Block_Red()
                    objects[172+j+(8*i)].xy = 80 + j*4, 233+(3*i) - ram_state[95]
                else:
                    objects[172+j+(8*i)] = NoObject()

    if hud:
        # ram[71-73] == score
        x, y, w, h = 95, 5, 7, 7

        if ram_state[73] > 15:
            x -= 40
            w += 40
        elif ram_state[73]:
            x -= 32
            w += 32
        elif ram_state[72] > 15:
            x -= 24
            w += 24
        elif ram_state[72]:
            x -= 16
            w += 16
        elif ram_state[71] > 15:
            x -= 8
            w += 8

        objects[-2].xy = x, y
        objects[-2].wh = w, h
        objects[-2].value = _convert_number(ram_state[73])*10000 + _convert_number(
            ram_state[72])*100 + _convert_number(ram_state[71])

        lives = ram_state[75] & 7
        if ram_state[75] & 7 > 1:
            if type(objects[-1]) is NoObject:
                objects[-1] = Life()
            objects[-1].xy = 99 - 4*(lives - 2), 13
            objects[-1].wh = 3 + 4*(lives - 2), 5
            objects[-1].value = lives - 1
        else:
            objects[-1] = NoObject()
