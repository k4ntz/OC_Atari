from .utils import find_objects, find_mc_objects, find_rectangle_objects
from .game_objects import GameObject
import numpy as np

objects_colors = {"player": [213, 130, 74],
                  "enemy_c1_": [66, 158, 130], "enemy_c2_": [72, 160, 72], "enemy_c3_": [110, 156, 66], "enemy_c4_": [136, 146, 62], "enemy_c5_": [162, 134, 56],
                  "enemy_c1_2": [24, 98, 78], "enemy_c2_2": [50, 132, 50], "enemy_c3_2": [110, 156, 66], "enemy_c4_2": [136, 146, 62], "enemy_c5_2": [162, 134, 56],
                  "enemy_c1_3": [162, 162, 42], "enemy_c2_3": [72, 160, 72], "enemy_c3_3": [136, 146, 62], "enemy_c4_3": [162, 134, 56],
                  "enemy_c1_4": [84, 184, 153], "enemy_c2_4": [50, 132, 50], "enemy_c3_4": [110, 156, 66], "enemy_c4_4": [136, 146, 62], "enemy_c5_4": [162, 134, 56],
                  "tower_purple": [146, 70, 192], "tower_pink": [184, 70, 162], "tower_red": [200, 72, 72], "tower_orange": [198, 108, 58],
                  "enemy_orange": [181, 83, 40], "enemy_orange2": [213, 130, 74], "sentry": [162, 162, 42],
                  "fuel_tank1": [110, 156, 66], "fuel_tank2": [135, 183, 84], "enemy_shot": [210, 164, 74], "satellite": [184, 50, 50],
                  "zaxxon": [136, 146, 62], "zaxxon_c2_1": [198, 108, 58], "zaxxon_c2_2": [180, 122, 48], "score": [198, 108, 58]
                  }


class Player(GameObject):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.rgb = 213, 130, 74
        self.hud = False


class Player_Shot(GameObject):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.rgb = 213, 130, 74
        self.hud = False


class Player_Shadow(GameObject):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.rgb = 0, 0, 0
        self.hud = False


class Hostile_Fighter(GameObject):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.rgb = 72, 160, 72
        self.hud = False


class Hostile_Shot(GameObject):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.rgb = 210, 164, 74
        self.hud = False


class Hostile_Orange(GameObject):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.rgb = 213, 130, 74
        self.hud = False


class Tower(GameObject):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.rgb = 146, 70, 192
        self.hud = False


class Fuel_Tank(GameObject):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.rgb = 110, 156, 66
        self.hud = False


class Sentry(GameObject):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.rgb = 162, 162, 42
        self.hud = False


class Satellite(GameObject):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.rgb = 184, 50, 50
        self.hud = False


class Zaxxon(GameObject):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.rgb = 136, 146, 62
        self.hud = False


class Score(GameObject):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.rgb = 198, 108, 58
        self.hud = True


class Life(GameObject):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.rgb = 162, 162, 42
        self.hud = True


class Fuel(GameObject):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.rgb = 162, 162, 42
        self.hud = True


class Altitude(GameObject):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.rgb = 24, 59, 157
        self.hud = True


# List of objects to detect: Player, Enemy, Swirl, fired bullets by Player, missile by Enemy, Cannon that appears, Shield chunks, Barrier
def _detect_objects_zaxxon(objects, obs, hud=False):
    # detection and filtering
    objects.clear()

    player = find_objects(obs, objects_colors["player"])
    for bb in player:
        if bb[2] == 1:
            objects.append(Player_Shot(*bb))
        elif bb[2] > 12:
            objects.append(Player(*bb))

    if obs[190, 85, 0] != 0:
        shadow = find_objects(
            obs, [0, 0, 0], minx=16, miny=160, maxx=143, maxy=190, size=(14, 12), tol_s=4)
        for bb in shadow:
            objects.append(Player_Shadow(*bb))

    fighter = find_mc_objects(obs, [objects_colors["enemy_c1_"], objects_colors["enemy_c2_"], objects_colors["enemy_c3_"],
                                    objects_colors["enemy_c4_"], objects_colors["enemy_c5_"]])
    fighter.extend(find_mc_objects(obs, [objects_colors["enemy_c1_2"], objects_colors["enemy_c2_2"], objects_colors["enemy_c3_2"],
                                         objects_colors["enemy_c4_2"], objects_colors["enemy_c5_2"]]))
    fighter.extend(find_mc_objects(obs, [objects_colors["enemy_c1_3"], objects_colors["enemy_c2_3"], objects_colors["enemy_c3_3"],
                                         objects_colors["enemy_c4_3"]]))
    fighter.extend(find_mc_objects(obs, [objects_colors["enemy_c1_4"], objects_colors["enemy_c2_4"], objects_colors["enemy_c3_4"],
                                         objects_colors["enemy_c4_4"], objects_colors["enemy_c5_4"]]))
    for bb in fighter:
        objects.append(Hostile_Fighter(*bb))

    tower = find_mc_objects(obs, [objects_colors["tower_purple"], objects_colors["tower_pink"], objects_colors["tower_red"],
                                  objects_colors["tower_orange"]])
    tower.extend(find_mc_objects(obs, [objects_colors["tower_purple"],
                 objects_colors["tower_pink"], objects_colors["tower_orange"]]))
    for bb in tower:
        objects.append(Tower(*bb))

    shot = find_objects(obs, objects_colors["enemy_shot"])
    for bb in shot:
        objects.append(Hostile_Shot(*bb))

    tank = find_mc_objects(
        obs, [objects_colors["fuel_tank1"], objects_colors["fuel_tank2"]])
    # tank = find_objects(obs, objects_colors["fuel_tank1"], closing_dist=6)
    for bb in tank:
        if bb[3] > 2:
            objects.append(Fuel_Tank(*bb))

    enemy = find_objects(obs, objects_colors["enemy_orange"])
    enemy.extend(find_objects(obs, objects_colors["enemy_orange2"]))
    for bb in enemy:
        if bb[2] < 13:
            objects.append(Hostile_Orange(*bb))

    sentry = find_objects(obs, objects_colors["sentry"], maxy=190)
    for bb in sentry:
        if bb[2] > 2 and bb[3] > 8:
            objects.append(Sentry(*bb))

    satellite = find_objects(obs, objects_colors["satellite"])
    for bb in satellite:
        objects.append(Satellite(*bb))

    zaxxon = find_mc_objects(
        obs, [objects_colors["sentry"], objects_colors["zaxxon"]])
    for bb in zaxxon:
        z = Zaxxon(*bb)
        z.rgb = 198, 108, 58
        objects.append(z)

    if len(zaxxon) == 0:
        zaxxon = find_mc_objects(
            obs, [objects_colors["zaxxon_c2_1"], objects_colors["zaxxon_c2_2"]])
        for bb in zaxxon:
            objects.append(Zaxxon(*bb))

    if hud:
        score = find_objects(
            obs, objects_colors["score"], maxy=20, closing_dist=6)
        for bb in score:
            objects.append(Score(*bb))

        life = find_objects(obs, objects_colors["sentry"], maxx=58, miny=191)
        for bb in life:
            objects.append(Life(*bb))

        fuel = find_objects(obs, objects_colors["sentry"], minx=58, miny=191)
        for bb in fuel:
            objects.append(Fuel(*bb))

        top = 192
        for y in range(105, 191):
            if obs[y, 9, 0] != 0 and obs[y, 9, 1] != 0 and obs[y, 9, 2] != 0:
                top = y
                break

        if top < 192:
            objects.append(Altitude(x=8, y=top, w=4, h=191-top))
