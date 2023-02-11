from .game_objects import GameObject

"""
RAM extraction for the game Atlantis. Supported modes: raw, revised.

"""


class Sentry(GameObject):
    def __init__(self):
        super(Sentry, self).__init__()
        self.visible = True
        self._xy = 0, 124
        self.wh = 8, 8
        self.rgb = 111, 210, 111
        self.hud = False


class Aqua_Plane(GameObject):
    def __init__(self):
        super(Aqua_Plane, self).__init__()
        self.visible = True
        self._xy = 16, 171
        self.wh = 16, 7
        self.rgb = 252, 144, 144
        self.hud = False


class Domed_Palace(GameObject):
    def __init__(self):
        super(Domed_Palace, self).__init__()
        self.visible = True
        self._xy = 38, 148
        self.wh = 16, 8
        self.rgb = 240, 170, 103
        self.hud = False


class Generator(GameObject):
    def __init__(self):
        super(Generator, self).__init__()
        self.visible = True
        self._xy = 62, 137
        self.wh = 4, 8
        self.rgb = 117, 231, 194
        self.hud = False


class Bridged_Bazaar(GameObject):
    def __init__(self):
        super(Bridged_Bazaar, self).__init__()
        self.visible = True
        self._xy = 96, 159
        self.wh = 16, 8
        self.rgb = 214, 214, 214
        self.hud = False


class Acropolis_Command_Post(GameObject):
    def __init__(self):
        super(Acropolis_Command_Post, self).__init__()
        self.visible = True
        self._xy = 72, 112
        self.wh = 8, 8
        self.rgb = 227, 151, 89
        self.hud = False


class Bandit_Bomber(GameObject):
    def __init__(self):
        super(Bandit_Bomber, self).__init__()
        self.visible = True
        self._xy = 0, 0
        self.wh = 9, 7
        self.rgb = 125, 48, 173
        self.hud = False


class Gorgon_Ship(GameObject):
    def __init__(self):
        super(Gorgon_Ship, self).__init__()
        self.visible = True
        self._xy = 0, 0
        self.wh = 15, 8
        self.rgb = 187, 187, 53
        self.hud = False


class Deathray(GameObject):
    def __init__(self):
        super(Deathray, self).__init__()
        self.visible = True
        self._xy = 0, 92
        self.wh = 2, 88
        self.rgb = 101, 209, 174
        self.hud = False


class Score(GameObject):
    def __init__(self):
        super(Score, self).__init__()
        self.visible = True
        self._xy = 0, 0
        self.wh = 0, 0
        self.rgb = 252, 188, 116
        self.hud = False


def _init_objects_atlantis_ram(hud=True):
    """
    (Re)Initialize the objects
    """

    objects = [Sentry(), Sentry()]

    objects[1].xy = 152, 112
    global prev_x1
    global prev_x2
    global prev_x3
    global prev_x4
    prev_x1 = 0
    prev_x2 = 0
    prev_x3 = 0
    prev_x4 = 0

    return objects

global ray_available
global prev_x1
global prev_x2
global prev_x3
global prev_x4

# levels: ram_state[36], total of 3 levels: 0,1 and 2
def _detect_objects_atlantis_revised(objects, ram_state, hud=True):
    del objects[2:]

    global prev_x1
    global prev_x2
    global prev_x3
    global prev_x4

    if ram_state[39] != 0:
        ship = _get_ship_type(ram_state, 3, 131)
        g_s = None
        if ship == 64:
            g_s = Gorgon_Ship()
            if prev_x1 < ram_state[39]:
                g_s.xy = ram_state[39] - 8, 19
            else:
                g_s.xy = ram_state[39] - 7, 19
        elif ship == 32 or ship == 48:
            g_s = Gorgon_Ship()
            g_s.wh = 15, 7
            if prev_x1 < ram_state[39]:
                g_s.xy = ram_state[39] - 8, 20
            else:
                g_s.xy = ram_state[39] - 7, 20
        elif ship == 80:
            g_s = Bandit_Bomber()
            if prev_x1 < ram_state[39]:
                g_s.xy = ram_state[39] - 8, 20
            else:
                g_s.xy = ram_state[39] - 3, 20
        if g_s:
            objects.append(g_s)

    prev_x1 = ram_state[39]

    if ram_state[38] != 0:
        ship = _get_ship_type(ram_state, 2, 130)
        g_s = None
        if ship == 64:
            g_s = Gorgon_Ship()
            if prev_x2 < ram_state[38]:
                g_s.xy = ram_state[38] - 8, 40
            else:
                g_s.xy = ram_state[38] - 7, 40
        elif ship == 32 or ship == 48:
            g_s = Gorgon_Ship()
            g_s.wh = 15, 7
            if prev_x2 < ram_state[38]:
                g_s.xy = ram_state[38] - 8, 41
            else:
                g_s.xy = ram_state[38] - 7, 41
        elif ship == 80:
            g_s = Bandit_Bomber()
            if prev_x2 < ram_state[38]:
                g_s.xy = ram_state[38] - 8, 41
            else:
                g_s.xy = ram_state[38] - 3, 41
        if g_s:
            objects.append(g_s)

    prev_x2 = ram_state[38]

    if ram_state[37] != 0:
        ship = _get_ship_type(ram_state, 1, 129)
        g_s = None
        if ship == 64:
            g_s = Gorgon_Ship()
            if prev_x3 < ram_state[37]:
                g_s.xy = ram_state[37] - 8, 61
            else:
                g_s.xy = ram_state[37] - 7, 61
        elif ship == 32 or ship == 48:
            g_s = Gorgon_Ship()
            g_s.wh = 15, 7
            if prev_x3 < ram_state[37]:
                g_s.xy = ram_state[37] - 8, 62
            else:
                g_s.xy = ram_state[37] - 7, 62
        elif ship == 80:
            g_s = Bandit_Bomber()
            if prev_x3 < ram_state[37]:
                g_s.xy = ram_state[37] - 8, 62
            else:
                g_s.xy = ram_state[37] - 3, 62
        if g_s:
            objects.append(g_s)

    prev_x3 = ram_state[37]

    if ram_state[36] != 0:
        ship = _get_ship_type(ram_state, 0, 128)
        g_s = None
        if ship == 64:
            g_s = Gorgon_Ship()
            if prev_x4 < ram_state[36]:
                g_s.xy = ram_state[36] - 8, 82
            else:
                g_s.xy = ram_state[36] - 7, 82
        elif ship == 32 or ship == 48:
            g_s = Gorgon_Ship()
            g_s.wh = 15, 7
            if prev_x4 < ram_state[36]:
                g_s.xy = ram_state[36] - 8, 83
            else:
                g_s.xy = ram_state[36] - 7, 83
        elif ship == 80:
            g_s = Bandit_Bomber()
            if prev_x4 < ram_state[36]:
                g_s.xy = ram_state[36] - 8, 83
            else:
                g_s.xy = ram_state[36] - 3, 83
        if g_s:
            objects.append(g_s)

    prev_x4 = ram_state[36]

    if ram_state[22] < 152:
        gen = Generator()
        gen.xy = 82, 124
        gen.rgb = 111, 210, 111
        objects.append(gen)

    if ram_state[23] < 152:
        objects.append(Generator())

    if ram_state[24] < 152:
        gen = Generator()
        gen.xy = 142, 137
        gen.rgb = 188, 144,252
        objects.append(gen)

    if ram_state[25] < 152:
        objects.append(Domed_Palace())

    if ram_state[26] < 152:
        objects.append(Bridged_Bazaar())

    if ram_state[27] < 152:
        objects.append(Aqua_Plane())

    if ram_state[30] < 75 and ram_state[30] > 60:
        ray = Deathray()
        if prev_x4 < ram_state[36]:
            ray.xy = ram_state[36] - 1, 92
        else:
            ray.xy = ram_state[36] + 1, 92
        objects.append(ray)

    return objects


def _get_ship_type(ram_state, hight1, height2):
    """
    Determins the type of ship by its sprite index
    """
    for i in range(4):
        if ram_state[71+i] == hight1 or ram_state[71+i] == height2:
            return ram_state[79+i]
    return 0


def _detect_objects_atlantis_raw(info, ram_state):

    enemy_x = ram_state[36:40]
    player_projectile = ram_state[58:62]
    # score ram_state[33:36]
    info["ram_slice"] = enemy_x + player_projectile
