from .game_objects import GameObject

"""
RAM extraction for the game KANGUROO. Supported modes: raw, revised.

"""


class Player(GameObject):
    def __init__(self):
        super(Player, self).__init__()
        self._xy = 78, 103
        self.wh = 8, 24
        self.rgb = 181, 83, 40
        self.hud = False


class PurpleBall(GameObject):
    def __init__(self):
        super(PurpleBall, self).__init__()
        self._xy = 78, 103
        self.wh = 8, 24
        self.rgb = 146, 70, 192
        self.hud = False


class RedBall(GameObject):
    def __init__(self):
        super(RedBall, self).__init__()
        self._xy = 78, 103
        self.wh = 8, 24
        self.rgb = 223, 183, 85
        self.hud = False


class GreenBall(GameObject):
    def __init__(self):
        super(GreenBall, self).__init__()
        self._xy = 78, 103
        self.wh = 8, 24
        self.rgb = 50, 132, 50
        self.hud = False


class Coily(GameObject):
    def __init__(self):
        super(Coily, self).__init__()
        self._xy = 78, 103
        self.wh = 8, 24
        self.rgb = 146, 70, 192
        self.hud = False


class Sam(GameObject):
    def __init__(self):
        super(Sam, self).__init__()
        self._xy = 78, 103
        self.wh = 8, 24
        self.rgb = 50, 132, 50
        self.hud = False


class FlyingDiscs(GameObject):
    def __init__(self):
        super(FlyingDiscs, self).__init__()
        self._xy = 78, 103
        self.wh = 8, 24
        self.rgb = 223, 183, 85
        self.hud = False


class Score(GameObject):
    def __init__(self):
        super(Score, self).__init__()
        self._xy = 78, 103
        self.wh = 8, 24
        self.rgb = 210, 210, 64
        self.hud = False


class Lives(GameObject):
    def __init__(self):
        super(Lives, self).__init__()
        self._xy = 78, 103
        self.wh = 8, 24
        self.rgb = 210, 210, 64
        self.hud = False



def _init_objects_qbert_ram(hud=True):
    """
    (Re)Initialize the objects
    """

    objects = [Player()]

    return objects


def _detect_objects_qbert_revised(objects, ram_state, hud=True):
    objects.clear()

    return objects


def _detect_objects_qbert_raw(info, ram_state):
    pass
