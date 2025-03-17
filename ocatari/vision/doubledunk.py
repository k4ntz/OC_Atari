from .utils import find_objects, find_mc_objects
from .game_objects import GameObject

objects_colors = {"Player": [[45, 129, 105], [160, 171, 79]],#, [236, 236, 236]],
                  "Opponent1": [[236, 236, 236], [160, 171, 79], [232, 204, 99]],
                  "Opponent2": [[236, 236, 236], [80, 89, 22], [232, 204, 99]],
                  "Ball": [144, 72, 17]
                  }


class Player_Small(GameObject):
    """
    Smaller player of the players team
    """

    def __init__(self, x, y, w, h):
        super(Player_Small, self).__init__(x, y, w, h)
        self._xy = x, y
        self.wh = w, h
        self.rgb = 45, 129, 105
        self.hud = False


class Player_Big(GameObject):
    """
    Taller player of the players team
    """

    def __init__(self, x, y, w, h):
        super(Player_Big, self).__init__(x, y, w, h)
        self._xy = x, y
        self.wh = w, h
        self.rgb = 45, 129, 105
        self.hud = False


class Opponent_Small(GameObject):
    """
    Smaller player of the enemy team
    """

    def __init__(self, x, y, w, h):
        super(Opponent_Small, self).__init__(x, y, w, h)
        self._xy = x, y
        self.wh = w, h
        self.rgb = 236, 236, 236
        self.hud = False


class Opponent_Big(GameObject):
    """
    Taller player of the enemy team
    """

    def __init__(self, x, y, w, h):
        super(Opponent_Big, self).__init__(x, y, w, h)
        self._xy = x, y
        self.wh = w, h
        self.rgb = 236, 236, 236
        self.hud = False


class Ball(GameObject):
    """
    It is a ball
    """

    def __init__(self, x=0, y=0, w=0, h=0):
        super(Ball, self).__init__(x, y, w, h)
        self._xy = x, y
        self._prev_xy = x, y
        self.wh = 4, 17
        self.rgb = 144, 72, 17
        self.hud = False


class Basket(GameObject):
    """
    The basket
    """

    def __init__(self, x=0, y=0, w=8, h=4):
        super(Basket, self).__init__(x, y, w, h)
        self._xy = 76, 42
        self.wh = (8, 9)
        self.rgb = 162, 162, 42
        self.hud = False


class Backboard(GameObject):
    """
    Backboard of the basket
    """

    def __init__(self, x, y, w, h):
        super(Backboard, self).__init__(x, y, w, h)
        self._xy = 68, 28
        self.wh = (24, 16)
        self.rgb = 214, 214, 214
        self.hud = False


class Player_Score(GameObject):
    """
    Players points in the game
    """

    def __init__(self, x, y, w, h):
        super(Player_Score, self).__init__(x, y, w, h)
        self._xy = x, y
        self.wh = w, h
        self.rgb = 45, 129, 105
        self.hud = True


class Opponent_Score(GameObject):
    """
    Enemy points in the game
    """

    def __init__(self, x, y, w, h):
        super(Opponent_Score, self).__init__(x, y, w, h)
        self._xy = x, y
        self.wh = w, h
        self.rgb = 236, 236, 236
        self.hud = True


def _detect_objects(objects, obs, hud=True):
    player = find_mc_objects(obs, objects_colors["Player"])
    if player:
        objects[0].xywh = player[0]
    if len(player) > 1:
        objects[1].xywh = player[1]

    opponent1 = find_mc_objects(obs, objects_colors["Opponent1"])
    if opponent1:
        objects[2].xywh = opponent1[0]

    opponent2 = find_mc_objects(obs, objects_colors["Opponent2"])
    if opponent2:
        objects[3].xywh = opponent2[0]

    ball = find_objects(obs, objects_colors["Ball"])
    if ball:
        objects[4].xywh = ball[0]

    if hud:
        pass
