from .game_objects import GameObject


class Player(GameObject):
    class Player(GameObject):
        def __init__(self, x, y, w, h, num, *args, **kwargs):
            super().__init__(x, y, w, h, *args, **kwargs)
            self.rgb = 187, 187, 53
            self.player_num = num
            self.visible = False
            self._xy = 0, 0
            self.wh = 8, 11  # at some point 16, 11
            self.hud = False


class Cauldron(GameObject):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.rgb = 184, 50, 50
        self.visible = False
        self._xy = 0, 0
        self.wh = 6, 8
        self.hud = False


class Enemy(GameObject):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.rgb = 228, 111, 111
        self.visible = False
        self._xy = 0, 0
        self.wh = 7, 11
        self.hud = False


class Score(GameObject):
    def __init__(self, x, y, w, h, num, *args, **kwargs):
        super().__init__(x, y, w, h, *args, **kwargs)
        self.rgb = 187, 187, 53  # same color as player
        self.visible = True
        self._xy = 0, 0
        self.wh = 8, 11
        self.hud = True


class Lives(GameObject):
    def __init__(self, y, *args, **kwargs):
        super().__init__(y, *args, **kwargs)
        self.rgb = 187, 187, 53  # same color as player
        self.visible = True
        self._xy = 0, 0
        self.wh = 6, 7
        self.hud = True


class Bounty(GameObject):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.rgb = 198, 89, 179
        self.visible = True
        self._xy = 0, 0
        self.wh = 6, 11
        self.hud = False

# initialize new classes for new covered objects


def _init_objects_asterix_ram(hud=False):
    """
    (Re)Initialize the objects
    """
    objects = [Player, Cauldron, Enemy, Score, Lives, Bounty]
    if hud:
        objects.append(Score)
        # TODO Code for Lives
        # zwei Stueck
        # x: von 59 bis 68 und von 75 bis 84
        # y: von 168 bis 180 (like constant)

    return objects


def _detect_objects_asterix_raw(info, ram_state):
    info["x_positions"] = ram_state[42:50] + ram_state[78]  # 0-3 but renders correctly till 6

    print(ram_state)


def _detect_objects_asterix_revised(objects, ram_state, hud=False):
    print(ram_state)
