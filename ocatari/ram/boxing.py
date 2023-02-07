from .game_objects import GameObject


class Player(GameObject):
    def __init__(self):
        self._xy = 0, 0
        self.wh = 14, 46
        self.rgb = 214, 214, 214
        self.hud = False


class Enemy(GameObject):
    def __init__(self):
        self._xy = 0, 0
        self.wh = 14, 46
        self.rgb = 0, 0, 0
        self.hud = False


class Logo(GameObject):
    def __init__(self):
        self._xy = 62, 189
        self.wh = 32, 7
        self.rgb = 20, 60, 0
        self.hud = True


class Clock(GameObject):
    def __init__(self, x, y, w, h):
        self._xy = x, y
        self.wh = w, h
        self.rgb = 20, 60, 0
        self.hud = True


class PlayerScore(GameObject):
    def __init__(self, ten=False):
        if ten:
            self._xy = 39, 5
        else:
            self._xy = 47, 5
        self.ten = ten
        self.rgb = 214, 214, 214
        self.wh = 6, 7
        self.hud = True

    def __eq__(self, o):
        return isinstance(o, PlayerScore) and self.xy == o.xy


class EnemyScore(GameObject):
    def __init__(self, ten=False):
        if ten:
            self._xy = 103, 5
        else:
            self._xy = 111, 5
        self.ten = ten
        self.rgb = 0, 0, 0
        self.wh = 6, 7
        self.hud = True


def _init_objects_boxing_ram(hud=False):
    """
    (Re)Initialize the objects
    """
    objects = [Player(), Enemy()]
    if hud:
        objects.extend([PlayerScore(), EnemyScore(), Logo(),
                        Clock(63, 17, 6, 7), Clock(73, 18, 2, 5),
                        Clock(79, 17, 6, 7), Clock(87, 17, 6, 7)])
    return objects


def _detect_objects_boxing_revised(objects, ram_state, hud=False):
    """
    For all 3 objects:
    (x, y, w, h, r, g, b)
    """
    player, enemy = objects[:2]
    player.xy = ram_state[32]+5, ram_state[34]+38
    enemy.xy = ram_state[33]+4, ram_state[35]+38, 14, 46,
    if hud:
        # scores
        if ram_state[19] > 10:  # enemy score
            objects.append(EnemyScore(ten=True))
        else:
            tens = EnemyScore(ten=True)
            if tens in objects:
                objects.remove(tens)
        if ram_state[18] > 10:  # player score
            objects.append(PlayerScore(ten=True))
        else:
            tens = PlayerScore(ten=True)
            if tens in objects:
                objects.remove(tens)


def _detect_objects_boxing_raw(info, ram_state):
    """
    returns unprocessed list with
    ball_x, ball_y, enemy_y, player_y
    """
    info["objects_list"] = ram_state[32:36]


# def _detect_objects_boxing_revised_old(info, ram_state, hud=False):
#     """
#     For all 3 objects:
#     (x, y, w, h, r, g, b)
#     """
#     objects = {}
#     objects["player"] = ram_state[32]+5, ram_state[34]+38, 14, 46, 214, 214, 214
#     objects["enemy"] = ram_state[33]+4, ram_state[35]+38, 14, 46, 0, 0, 0
#     if hud:
#         objects["enemy_score"] = 111, 5, 6, 7, 0, 0, 0
#         if ram_state[19] < 10:
#             objects["enemy_score2"] = 0, 0, 0, 0, 0, 0, 0
#         else:
#             objects["enemy_score2"] = 103, 5, 6, 7, 0, 0, 0
#         objects["player_score"] = 47, 5, 6, 7, 214, 214, 214
#         if ram_state[18] < 10:
#             objects["player_score2"] = 0, 0, 0, 0, 0, 0, 0
#         else:
#             objects["player_score2"] = 39, 5, 6, 7, 214, 214, 214
#         objects["logo"] = 62, 189, 32, 7, 20, 60, 0
#         objects["time1"] = 63, 17, 6, 7, 20, 60, 0
#         objects["time2"] = 73, 18, 2, 5, 20, 60, 0
#         objects["time3"] = 79, 17, 6, 7, 20, 60, 0
#         objects["time4"] = 87, 17, 6, 7, 20, 60, 0
#     info["objects"] = objects
