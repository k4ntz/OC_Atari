from .game_objects import GameObject
from ._helper_methods import bitfield_to_number, number_to_bitfield


class Player(GameObject):
    def __init__(self):
        super(Player, self).__init__()
        self.visible = True
        self._xy = 0, 0
        self.wh = 7, 12
        self.rgb = 184, 70, 162
        self.hud = False


class Enemy(GameObject):
    def __init__(self):
        super(Enemy, self).__init__()
        self.visible = False
        self._xy = 0, 0
        self.wh = 16, 7
        self.rgb = 213, 130, 74
        self.hud = False


class ProjectileFriendly(GameObject):
    def __init__(self):
        super(ProjectileFriendly, self).__init__()
        self.visible = True
        self._xy = 0, 0
        self.wh = 1, 8
        self.rgb = 212, 140, 252
        self.hud = False


class ProjectileHostile(GameObject):
    def __init__(self):
        super(ProjectileHostile, self).__init__()
        self.visible = True
        self._xy = 0, 0
        self.wh = 1, 4
        self.rgb = 252, 144, 144
        self.hud = False


class Score(GameObject):
    def __init__(self):     # TODO
        super(Score, self).__init__()
        self.visible = True
        self._xy = 96, 7
        self.wh = 5, 9
        self.rgb = 223, 183, 85
        self.hud = True


class Live(GameObject):
    def __init__(self):
        super(Live, self).__init__()
        self.visible = True
        self._xy = 0, 0
        self.wh = 3, 5
        self.rgb = 240, 128, 128
        self.hud = True


def calculate_small_projectiles_from_bitmap(bitmap, basex):
    result = []
    offsetcollumn = 8

    currenty = 183
    for number in bitmap:
        bitfield = number_to_bitfield(number)

        index = 0
        for b in bitfield:
            if b == 1:
                proj = ProjectileHostile()
                proj.xy = basex + index, currenty  # projectiles are only one pixel wide
                result.append(proj)
            index += 1

        currenty -= offsetcollumn

    return result


def bitfield_to_number_equality(bitfield):
    res = bitfield[0] * 7 - bitfield[1] * 6 - bitfield[2] * 3 - bitfield[3]  # not 100% exact but close
    return res


def calc_x(number, ignore_upper=True):
    """
    takes the bitfield(4 bits) and extracts the x of the object
    way too complicated for no reason
    """
    bitfield = number_to_bitfield(number)
    xbits = bitfield[4:]
    # res = 26 - bitfield_to_number(bitfield[:4])
    res = 10 + bitfield_to_number_equality(bitfield[:4])

    if ignore_upper:
        res = 10

    res = res + int(bitfield_to_number(xbits) * 15.5)

    return res


def _init_objects_demon_attack_ram(hud=False):
    """
    (Re)Initialize the objects
    """
    objects = [Player(), Enemy(), Enemy(), Enemy(), ProjectileFriendly()]
    if hud:
        objects.append(Score())

        basex = 17
        for i in range(3):
            live = Live()
            live.xy = basex, 188
            objects.append(live)
            basex += 8

    return objects


def _detect_objects_demon_attack_revised(objects, ram_state, hud=False):
    player, e1, e2, e3, proj_frienddly, proj_hostile = objects[:6]

    player.xy = calc_x(ram_state[16], True), 174

    enemies = [e1, e2, e3]
    for i in range(3):
        if ram_state[13 + i] == 0:
            enemies[i].visible = False
        else:
            enemies[i].visible = True
        x = calc_x(ram_state[13 + i], False)
        if i == 2:
            x = x + 3
        enemies[i].xy = x, 175 - ram_state[69 + i]

    if 90 <= ram_state[21]:
        proj_frienddly.xy = 3 + calc_x(ram_state[22]), 176 - ram_state[21]
    else:
        proj_frienddly.xy = 3 + calc_x(ram_state[22]), 178 - ram_state[21]

    objects_temp = [obj for obj in objects if not isinstance(obj, ProjectileHostile)]
    objects_temp.extend(calculate_small_projectiles_from_bitmap(ram_state[37:47], 3 + calc_x(ram_state[20], False)))

    objects.clear()     # giga ugly but i didnt find a better solution
    objects.extend(objects_temp)

    if hud:
        if ram_state[114] < 3 and len(objects) > 8 and isinstance(objects[8], Live):
            del objects[8]
        if ram_state[114] < 2 and len(objects) > 7 and isinstance(objects[7], Live):
            del objects[7]
        if ram_state[114] < 1 and len(objects) > 6 and isinstance(objects[6], Live):
            del objects[6]


def _detect_objects_demon_attack_raw(info, ram_state):
    info["lives"] = ram_state[114]  # 0-3 but renders correctly till 6
    info["player_x"] = ram_state[16]
    info["enemy_y"] = ram_state[69:71]  # 69 is topmost enemy 71 is lowest
    info["enemy_x"] = ram_state[13:15]  # 13 is topmost enemy 15 is lowest
    info["enemy_projectile_y"] = ram_state[37:46]
    # kind of like a bit map. If a value is 0 then there is no projectile
    # at that position the higher the value the thicker / more projectiles
    # at that position 46(ram) is highest possible enemy_position_y(lowest enemy)
    # 37(ram) is player position_y
    info["player_projectile_y"] = ram_state[21]
    info["player_projectile_x"] = ram_state[22]
