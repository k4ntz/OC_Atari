from .game_objects import GameObject


class Player(GameObject):
    class Player(GameObject):
        def __init__(self, x, y, w, h, num, *args, **kwargs):
            super().__init__(x, y, w, h, *args, **kwargs)
            self.rgb = 187, 187, 53
            self.player_num = num
            # self.visible =
            self._xy = 0, 0
            # self.wh =
            self.hud = False


class Cauldron(GameObject):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.rgb = 184, 50, 50
        # self.visible =
        self._xy = 0, 0
        # self.wh =
        self.hud = False


class Enemy(GameObject):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.rgb = 227, 110, 110
        # self.visible =
        self._xy = 0, 0
        # self.wh =
        self.hud = False


class Score(GameObject):
    def __init__(self, x, y, w, h, num, *args, **kwargs):
        super().__init__(x, y, w, h, *args, **kwargs)
        self.rgb = 187, 187, 53  # same color as player
        # self.visible =
        self._xy = 0, 0
        # self.wh =
        self.hud = True


class Lives(GameObject):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.rgb = 187, 187, 53  # same color as player
        # self.visible =
        self._xy = 0, 0
        # self.wh =
        self.hud = True


# initialize new classes for new covered objects


def _init_objects_asterix_ram(hud=False):
    """
    (Re)Initialize the objects
    """
    objects = [Player()]
    if hud:
        objects.append(Score)
        # TODO Code for Lives

    return objects


def _detect_objects_asterix_raw(info, ram_state):

    print(ram_state)


def _detect_objects_asterix_revised(objects, ram_state, hud=False):

    print(ram_state)
