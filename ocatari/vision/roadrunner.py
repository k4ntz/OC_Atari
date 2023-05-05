from .utils import find_objects, find_mc_objects
from .game_objects import GameObject


objects_colors = {
    "birdseeds": [84, 92, 214], "cactus": [187, 187, 53],
    "whatvev": [214, 214, 214], "thiswaysign": [0, 0, 0],
    "hud_objs": [20, 60, 0]
    }

playercolors = [[101, 111, 228], [84, 92, 214], [66, 72, 200]]
enemycolors = [[198, 108, 58], [181, 83, 40], [213, 130, 74]]
truckcolors = [[252, 224, 112], [198, 108, 58], [213, 130, 74], [181, 83, 40]]

class Player(GameObject):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.rgb = 101, 111, 228
        self.hud = False


class Enemy(GameObject):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.rgb = 198, 108, 58
        self.hud = False


class Birdseeds(GameObject):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.rgb = 84, 92, 214
        self.hud = False


class Truck(GameObject):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.rgb = 198, 108, 58
        self.hud = False


class Cactus(GameObject):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.rgb = 187, 187, 53
        self.hud = False

class ThisWaySign(GameObject):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.rgb = 0, 0, 0
        self.hud = False

class PlayerScore(GameObject):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.rgb = 214, 214, 214
        self.hud = True


class EnemyScore(GameObject):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.rgb = 0, 0, 0


def _detect_objects_roadrunner(objects, obs, hud=False):
    # detection and filtering
    objects.clear()
    player = find_mc_objects(obs, playercolors, size=(8, 28), tol_s=8, miny=37, min_distance=1)
    if player:
        objects.append(Player(*player[0]))
    enemy = find_mc_objects(obs, enemycolors, size=(8, 28), tol_s=8, miny=37, min_distance=1)
    if enemy:
        objects.append(Enemy(*enemy[0]))
    birdseeds = find_objects(obs, objects_colors["birdseeds"], closing_dist=5, size=(5,3), tol_s=2)
    for seed in birdseeds:
        objects.append(Birdseeds(*seed))
    trucks = find_mc_objects(obs, truckcolors, size=(16, 18), tol_s=2, min_distance=1)
    for truck in trucks:
        objects.append(Truck(*truck))
    cactus = find_objects(obs, objects_colors["cactus"], closing_active=False, size=(8, 8), tol_s=2)
    for cac in cactus:
        objects.append(Cactus(*cac))
    twss = find_objects(obs, objects_colors["thiswaysign"], closing_active=False, size=(16, 15), tol_s=3, miny=25, maxy=107)
    for tws in twss:
        objects.append(ThisWaySign(*tws))
    # if hud:
    #     huds = find_objects(obs, objects_colors["hud_objs"], closing_active=False, maxy=25)
    #     for el in huds:
    #         objects.append(Logo(*el))
    #     huds = find_objects(obs, objects_colors["hud_objs"], miny=187)
    #     for el in huds:
    #         objects.append(Clock(*el))
