from .game_objects import GameObject
from ._helper_methods import bitfield_to_number, number_to_bitfield


class Player(GameObject):
    def __init__(self):
        super(Player, self).__init__()
        self.visible = True
        self._xy = 0, 0
        self.wh = 9, 10
        self.rgb = 210, 164, 74
        self.hud = False


class Ghost(GameObject):
    def __init__(self, *args, **kwargs):
        super(Ghost, self).__init__()
        self.visible = True
        self._xy = 0, 0
        self.wh = 9, 10
        super().__init__(*args, **kwargs)
        if GameObject == "orange":
            self.rgb = 180, 122, 48
        elif GameObject == "cyan":
            self.rgb = 84, 184, 153
        elif GameObject == "pink":
            self.rgb = 198, 89, 179
        elif GameObject == "red":
            self.rgb = 200, 72, 72
        self.hud = False


class Fruit(GameObject):
    def __init__(self, *args, **kwargs):
        super(Fruit, self).__init__()
        self._xy = 0, 0
        self.wh = 10, 10
        if GameObject == "cherry/strawberry/Apple":
            self.rgb = 184, 50, 50
        elif GameObject == "pretzel":
            self.rgb = 162, 162, 42
        elif GameObject == "orange/banana":
            self.rgb = 198, 108, 58
        elif GameObject == "pear":
            self.rgb = 110, 156, 66
        self.hud = False

class Score(GameObject):
    def __init__(self, *args, **kwargs):
        super(Score, self).__init__()
        self._xy = 0, 0
        self.wh = 10, 10
        self.rgb = 195, 144, 61
        self.hud = True


class Life(GameObject):
    def __init__(self, *args, **kwargs):
        super(Life, self).__init__()
        self._xy = 0, 0
        self.wh = 10, 10
        self.rgb = 187, 187, 53
        self.hud = True


def _init_objects_mspacman_ram(hud=False):
    """
    (Re)Initialize the objects
    """
    objects = [Player(), Ghost(), Ghost(), Ghost(), Ghost(), Fruit()]
    if hud:
        objects.append(Score())

        basex = 17
        for i in range(3):
            life = Life()
            life.xy = basex, 188
            objects.append(life)
            basex += 8

    return objects


def _detect_objects_mspacman_revised(objects, ram_state, hud=False):
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


def _detect_objects_mspacman_raw(info, ram_state):
    pass
