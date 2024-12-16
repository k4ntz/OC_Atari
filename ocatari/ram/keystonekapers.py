from .game_objects import GameObject, NoObject

"""
RAM extraction for the game Keystone Kapers.

"""

MAX_NB_OBJECTS = {'Kop': 1, 'Krook': 1, 'Ball': 1, 'Moneybag': 2, 'Suitcase': 2,
                  'Elevator': 3, 'Escalator': 2, 'SecuritySystem': 1, 'Radio': 4, 'Cart': 4, 'Biplane': 2}
MAX_NB_OBJECTS_HUD = {'Kop': 1, 'Krook': 1, 'Ball': 1, 'Moneybag': 2, 'Suitcase': 2, 'Elevator': 3,
                      'Escalator': 2, 'SecuritySystem': 1, 'Radio': 4, 'Cart': 4, 'Biplane': 2, 'BonusKops': 1, 'Score': 1, 'Timer': 1}


class Kop(GameObject):
    """
    The player figure i.e., the Kop.
    """

    def __init__(self):
        super().__init__()
        self.rgb = 220, 175, 111
        self.hud = False


class Krook(GameObject):
    """
    A thief.
    """

    def __init__(self):
        super().__init__()
        self.rgb = 220, 175, 11
        self.hud = False


class Ball(GameObject):
    def __init__(self):
        super().__init__()
        self._xy = 0, 0
        self.wh = 6, 6
        self.rgb = 137, 26, 53


class Moneybag(GameObject):
    def __init__(self):
        super().__init__()
        self.rgb = 128, 88, 0


class Suitcase(GameObject):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.rgb = 128, 88, 0
        # self.xywh += (0,-9,0,9)


class Elevator(GameObject):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.rgb = 72, 164, 164
        self.is_open = False


class Escalator(GameObject):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.rgb = 52, 0, 128


class SecuritySystem(GameObject):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.rgb = 0, 0, 0


class Radio(GameObject):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.rgb = 236, 236, 236


class Cart(GameObject):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.rgb = 210, 210, 210


class Biplane(GameObject):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.rgb = 238, 209, 128

# HUD:


class BonusKops(GameObject):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.rgb = 0, 0, 0
        self.hud = True


class Score(GameObject):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.rgb = 236, 236, 236
        self.hud = True


class Timer(GameObject):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.rgb = 0, 0, 0
        # self.xywh = (55, 43, 14, 7)
        self.hud = True


def _init_objects_ram(hud=False):
    """
    (Re)Initialize the objects
    """
    bags = [NoObject()]*2
    suitcases = [NoObject()]*2
    elevators = [NoObject()]*3
    escalators = [NoObject()]*2
    radios = [NoObject()]*4
    carts = [NoObject()]*4
    biplanes = [NoObject()]*2
    return [Kop()] + [Krook()] + [Ball()] + bags + suitcases + elevators + escalators + [SecuritySystem()] + radios + carts + biplanes + [BonusKops()] + [Score()] + [Timer()]


def _detect_objects_ram(objects, ram_state, hud=False):
    pass
