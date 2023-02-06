from .game_objects import GameObject

"""
RAM extraction for the game KANGUROO. Supported modes: raw, revised.

"""


class Player(GameObject):
    def __init__(self):
        super(Player, self).__init__()
        self.visible = True
        self._xy = 78, 103
        self.wh = 8, 24
        self.rgb = 223, 183, 85
        self.hud = False


class Enemy(GameObject):
    def __init__(self, *args, **kwargs):
        super(Enemy, self).__init__()
        super().__init__(*args, **kwargs)
        self.visible = True
        self._xy = 79, 57
        self.wh = 7, 15
        self.rgb = 227, 159, 89
        self.hud = False


def _init_objects_beamrider_ram(hud=True):
    """
    (Re)Initialize the objects
    """

    objects = []

    return objects


# levels: ram_state[36], total of 3 levels: 0,1 and 2
def _detect_objects_beamrider_revised(objects, ram_state, hud=True):

    return objects


def _detect_objects_beamrider_raw(info, ram_state):
    pass
