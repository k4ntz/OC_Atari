import sys
from .game_objects import GameObject


MAX_NB_OBJECTS = {'Player': 1, 'Ball': 1, 'Enemy': 1}
MAX_NB_OBJECTS_HUD = {'Player': 1, 'Ball': 1, 'Enemy': 1, 'PlayerScore': 1, 'EnemyScore': 2}


class Player(GameObject):
    def __init__(self):
        super().__init__()
        self._xy = 0, 0
        self.wh = 4, 15
        self.rgb = 92, 186, 92
        self.hud = False
        self._above_10 = False


class Enemy(GameObject):
    def __init__(self):
        super().__init__()
        self._xy = 0, 0
        self.wh = 4, 15
        self.rgb = 213, 130, 74
        self.hud = False
        self._above_10 = False


class Ball(GameObject):
    def __init__(self):
        super().__init__()
        self._xy = 0, 0
        self.wh = 2, 3
        self.rgb = 236, 236, 236
        self.hud = False


class PlayerScore(GameObject):
    def __init__(self, ten=False):
        super().__init__()
        if ten:
            self._xy = 100, 1
        else:
            self._xy = 116, 1
        self.ten = ten
        self.rgb = 92, 186, 92
        self.wh = 12, 20
        self.hud = True

    def __eq__(self, o):
        return isinstance(o, PlayerScore) and self.xy == o.xy


class EnemyScore(GameObject):
    def __init__(self, ten=False):
        super().__init__()
        if ten:
            self._xy = 20, 1
        else:
            self._xy = 36, 1
        self.ten = ten
        self.rgb = 213, 130, 74
        self.wh = 12, 20
        self.hud = True

    def __eq__(self, o):
        return isinstance(o, EnemyScore) and self.xy == o.xy

# parses MAX_NB* dicts, returns default init list of objects
def _get_max_objects(hud=False):

    def fromdict(max_obj_dict):
        objects = []
        mod = sys.modules[__name__]
        for k, v in max_obj_dict.items():
            for _ in range(0, v):
                objects.append(getattr(mod, k)())    
        return objects

    if hud:
        return fromdict(MAX_NB_OBJECTS_HUD)
    return fromdict(MAX_NB_OBJECTS)

def _init_objects_pong_ram(hud=False):
    """
    (Re)Initialize the objects
    """
    objects = [Player(), Ball(), Enemy()]
    if hud:
        objects.extend([PlayerScore(), EnemyScore()])
    return objects


def _detect_objects_pong_revised(objects, ram_state, hud=False):
    """
    For all 3 objects:
    (x, y, w, h, r, g, b)
    """
    # set defauld coord if object does not exist
    player, ball, enemy = objects[:3]
    if ram_state[54] != 0:  # otherwise no ball
        ball.xy = ram_state[49]-49, ram_state[54]-14
    # same for enemy
    # if ram_state[50] > 18:  # otherwise no enemy
    #     if ram_state[50] - 15 < 34:
    #         enemy.xy = 16, 34
    #         enemy.wh = 4, ram_state[50]-33
    #     elif ram_state[50] > 194:
    #         enemy.xy = 16, ram_state[50]-15
    #         enemy.wh = 4, 209 - ram_state[50]
    #     else:
    #         enemy.xy = 16, ram_state[50]-15
    #         enemy.wh = 4, 15
    # if ram_state[51] - 13 < 34:
    #     player.xy = 140, 34
    #     player.wh = 4, ram_state[51]-33
    # elif ram_state[51] + 2 > 194:
    #     player.xy = 140, ram_state[51]-13
    #     player.wh = 4, 207 - ram_state[51]
    # else:
    #     player.xy = 140, ram_state[51]-13
    #     player.wh = 4, 15
    # if hud:
    #     # scores
    #     if ram_state[13] > 10:  # enemy score
    #         if not enemy._above_10:
    #             objects.append(EnemyScore(ten=True))
    #             enemy._above_10 = True
    #     else:
    #         if enemy._above_10:
    #             objects.remove(EnemyScore(ten=True))
    #             enemy._above_10 = False
    #     if ram_state[14] > 10:  # player score
    #         if not player._above_10:
    #             objects.append(PlayerScore(ten=True))
    #             player._above_10 = True
    #     else:
    #         if player._above_10:
    #             objects.remove(PlayerScore(ten=True))
    #             player._above_10 = False
    # print(objects)


def _detect_objects_pong_raw(info, ram_state):
    """
    returns unprocessed list with
    ball_x, ball_y, enemy_y, player_y
    """
    info["ball_x"] = ram_state[49]
    info["ball_y"] = ram_state[54]
    info["enemy_y"] = ram_state[50]
    info["player_y"] = ram_state[51]


# def _detect_objects_pong_revised_old(info, ram_state, hud=False):
#     """
#     For all 3 objects:
#     (x, y, w, h, r, g, b)
#     """
#     objects = {}
#     # set defauld coord if object does not exist
#     if ram_state[54] != 0:  # otherwise no ball
#         objects["ball"] = ram_state[49]-49, ram_state[54]-14, 2, 3, 236, 236, 236
#     else:
#         objects["ball"] = (0, 0, 0, 0, 0, 0, 0)
#     # same for enemy
#     if ram_state[50] > 18 or ram_state[50] != 0:  # otherwise no enemy
#         objects["enemy"] = 16, ram_state[50]-15, 4, 15, 213, 130, 74
#     else:
#         objects["enemy"] = (0, 0, 0, 0, 0, 0, 0)
#     objects["player"] = 140, ram_state[51]-13, 4, 15, 92, 186, 92
#     if hud:
#         # scores
#         if ram_state[13] < 10: # enemy score
#             objects["enemy_score"] = 0, 0, 0, 0, 0, 0, 0
#         else:
#             objects["enemy_score"] = 20, 1, 12, 20, 213, 130, 74
#         objects["enemy_score_2"] = 36, 1, 12, 20, 213, 130, 74
#         if ram_state[14] < 10: # player score
#             objects["player_score"] = (0, 0, 0, 0, 0, 0, 0)
#         else:
#             objects["player_score"] = 100, 1, 12, 20, 92, 186, 92
#         objects["player_score_2"] = 116, 1, 12, 20, 92, 186, 92
#     info["objects"] = objects
