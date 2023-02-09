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
        self.wh = 17, 8
        self.rgb = 240, 170, 103
        self.hud = False


class Generator(GameObject):
    def __init__(self):
        super(Domed_Palace, self).__init__()
        self.visible = True
        self._xy = 0, 0
        self.wh = 0, 0
        self.rgb = 117, 231, 194
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

    return objects


def _detect_objects_atlantis_raw(info, ram_state):

    info["ram_slice"]
