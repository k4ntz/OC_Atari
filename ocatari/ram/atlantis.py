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


class Aqua_plane(GameObject):
    def __init__(self):
        super(Aqua_plane, self).__init__()
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
        self._xy = 0, 0
        self.wh = 0, 0
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

    objects = [Sentry()]

    return objects


# levels: ram_state[36], total of 3 levels: 0,1 and 2
def _detect_objects_atlantis_revised(objects, ram_state, hud=True):
    objects.clear()

    if ram_state[39] != 0:
        g_s = Gorgon_Ship()
        g_s.xy = ram_state[39] - 7, 19
        objects.append(g_s)

    if ram_state[38] != 0:
        g_s = Gorgon_Ship()
        g_s.xy = ram_state[38] - 7, 40
        objects.append(g_s)

    if ram_state[37] != 0:
        g_s = Gorgon_Ship()
        g_s.xy = ram_state[37] - 7, 61
        objects.append(g_s)

    if ram_state[36] != 0:
        g_s = Gorgon_Ship()
        g_s.xy = ram_state[36] - 7, 82
        objects.append(g_s)

    return objects


def _detect_objects_atlantis_raw(info, ram_state):

    enemy_x = ram_state[36:40]
    info["ram_slice"]
