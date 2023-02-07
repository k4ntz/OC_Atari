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
    player_x = ram_state[41]
    enemy_x = ram_state[33:40]
    enemy_y = ram_state[25:32]
    projectile_x = ram_state[40]
    projectile_y = ram_state[32]
    # ram_state[42:49]no clue? killt player
    # ram_state[49] projectile 0 shootable 35 already shot
    # ram_state[0] sector
    # ram_state[5] lives: renders up to 13
    # ram_state[16] gamestatus: 1 = neutral, 2 = fighting, 3 = sentinel, 4 = transition
    # ram_state[83] torpedo amount
    # ram_state[83] enemy amount
    # 93-95 irgend was mit entfernung von Gegnern. 93 am weitesten entfernt 95 am nächsten
    pass
