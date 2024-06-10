from .utils import find_objects
from .utils import find_mc_objects
from .game_objects import GameObject

objects_colors = {"player": [232, 232, 74], "logo": [232, 232, 74], "background_water": [45, 50, 184],
                  "background_grass": [110, 156, 66], "fuel_bar": [0, 0, 0], "lives": [232, 232, 74],
                  "score": [232, 232, 74], "player_missile": [232, 232, 74],
                  "helicopter": [[0, 64, 48], [0, 0, 148], [210, 164, 74]],
                  "house": [[214, 214, 214], [0, 0, 0]],
                  "tanker": [[84, 160, 197], [163, 57, 21], [0, 0, 0]],
                  "fuel_depot": [[214, 92, 92], [214, 214, 214]],
                  "jet": [[117, 204, 235], [117, 181, 239], [117, 128, 240]],
                  "bridge": [[187, 187, 53], [105, 105, 15], [134, 134, 29], [124, 44, 0]]}


class Player(GameObject):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.rgb = 232, 232, 74


class PlayerMissile(GameObject):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.rgb = 232, 232, 74


class Helicopter(GameObject):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.rgb = 0, 64, 48


class Tanker(GameObject):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.rgb = 84, 160, 197


class FuelDepot(GameObject):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.rgb = 210, 91, 94


class Bridge(GameObject):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.rgb = 134, 134, 29


class Jet(GameObject):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.rgb = 117, 181, 239


class PlayerScore(GameObject):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.rgb = 232, 232, 74


class Lives(GameObject):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.rgb = 232, 232, 74


def _detect_objects(objects, obs, hud=False):
    objects.clear()

    player = find_objects(obs, objects_colors["player"], min_distance=1)
    for p in player:
        if p[1] < 160 and p[2] > 2 and p[3] > 10:
            objects.append(Player(*p))

    player_missile = find_objects(obs, objects_colors["player_missile"], min_distance=1)
    for missile in player_missile:
        if missile[2] < 2 and 1 < missile[3] < 10 and missile[1] < 160:
            objects.append(PlayerMissile(*missile))

    helicopter = find_mc_objects(obs, objects_colors["helicopter"], min_distance=1)
    for heli in helicopter:
        objects.append(Helicopter(*heli))

    tanker = find_mc_objects(obs, objects_colors["tanker"], min_distance=1, minx=10, miny=3, maxy=162)
    for tank in tanker:
        if tank[3] > 3:
            objects.append(Tanker(*tank))

    jet = find_mc_objects(obs, objects_colors["jet"], min_distance=1)
    for j in jet:
        objects.append(Jet(*j))

    fuel_depot = find_mc_objects(obs, objects_colors["fuel_depot"], min_distance=1)
    for fuel in fuel_depot:
        # if True:
        if fuel[2] < 8:
            objects.append(FuelDepot(*fuel))

    bridge = find_mc_objects(obs, objects_colors["bridge"], min_distance=1)
    for br in bridge:
        objects.append(Bridge(*br))

    if hud:
        lives = find_objects(obs, objects_colors["lives"], min_distance=1)
        for liv in lives:
            if liv[1] > 190 and liv[0] < 62:
                objects.append(Lives(*liv))

        score = find_objects(obs, objects_colors["score"], miny=163, maxy=175, min_distance=1, closing_dist=6)
        for sc in score:
            if 160 < sc[1] < 190:
                objects.append(PlayerScore(*sc))
