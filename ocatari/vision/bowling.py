from .utils import find_objects
from .game_objects import GameObject

objects_colors = {"player_head": [198, 89, 179], "player_shoes": [0, 0, 0], "ball": [45, 50, 184],
                  "background": [180, 122, 48], "player_score": [84, 92, 214], "round_player_1": [45, 50, 184],
                  "round_player_2": [45, 50, 184], "pins": [45, 50, 184]}


class Player(GameObject):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.rgb = 0, 0, 0


class Pins(GameObject):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.rgb = 45, 50, 184


class Ball(GameObject):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.rgb = 45, 50, 184


class PlayerScore(GameObject):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.rgb = 84, 92, 214


class PlayerRound(GameObject):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.rgb = 45, 50, 184


class Player2Round(GameObject):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.rgb = 45, 50, 184


def _detect_objects_bowling(objects, obs, hud=False):
    objects.clear()
    ball = find_objects(obs, objects_colors["ball"], min_distance=1)
    for bb in ball:
        if bb[2] < 160 and 100 < bb[1] < 175 and bb[3] < 20:
            objects.append(Ball(*bb))

    pins = find_objects(obs, objects_colors["pins"], min_distance=1)
    for p in pins:
        if p[2] < 160 and 100 < p[1] < 175 and p[3] > 10:
            objects.append(Pins(*p))

    if hud:
        round_player_1 = find_objects(obs, objects_colors["round_player_1"], min_distance=1)
        for ro in round_player_1:
            if ro[2] < 160 and ro[1] < 100 and ro[0] < 50:
                objects.append(PlayerRound(*ro))
            if ro[2] < 160 and ro[1] < 100 and ro[0] > 110:
                objects.append(Player2Round(*ro))

        player_score = find_objects(obs, objects_colors["player_score"], min_distance=1)
        for score in player_score:
            if score[1] < 20 and hud:
                objects.append(PlayerScore(*score))
    # player_head = [bb for bb in find_objects(obs, objects_colors["player_head"], min_distance=None)]
    # if player_head:
    #    objects["player_head"] = player_head[0]

    player_shoes = find_objects(obs, objects_colors["player_shoes"], min_distance=1)
    for p in player_shoes:
        if p[2] < 100:
            objects.append(Player(*p))
    print(objects)
