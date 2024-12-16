from .utils import find_objects, find_mc_objects, find_rectangle_objects
from .game_objects import GameObject
import numpy as np

objects_colors = {
    "player": [169, 128, 240], "shield": [163, 57, 21]
}
player_colors = [[132, 144, 252], [252, 144, 144]]
barrier_colors = [[162, 134, 56], [200, 72, 72], [82, 126, 45]]


class Player(GameObject):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.rgb = 169, 128, 240
        self.hud = False


class Enemy(GameObject):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.rgb = 240, 240, 240
        self.hud = False


class Swirl(GameObject):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.rgb = 181, 83, 40
        self.hud = False


class Enemy_Missile(GameObject):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.rgb = 169, 128, 240
        self.hud = False


class Barrier(GameObject):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.rgb = 163, 57, 21
        self.hud = False


class Player_Bullet(GameObject):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.rgb = 169, 128, 240
        self.hud = False


class Shield_Block(GameObject):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.rgb = 163, 57, 21
        self.hud = False


class Canon(GameObject):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.rgb = 163, 57, 21
        self.hud = False


# List of objects to detect: Player, Enemy, Swirl, fired bullets by Player, missile by Enemy, Cannon that appears, Shield chunks, Barrier
def _detect_objects(objects, obs, hud=False):
    # detection and filtering
    objects.clear()
    ################################
    # Detecting the number of unique colors present in the image
    all_colors_image = np.unique(obs.reshape(-1, obs.shape[2]), axis=0)

    player = find_objects(
        obs, objects_colors["player"], closing_active=False, size=(8, 16), tol_s=2)
    for p in player:
        # Handling the case where color of enemy is same as color of object
        if p[0] <= 146:
            objects.append(Player(*p))
        else:
            objects.append(Enemy(*p))

    b = (52, 4, 28, 190)
    count = 0
    for color in barrier_colors:
        b_segment = find_objects(obs, color, closing_active=False, size=(
            10, 10), minx=51, maxx=78, tol_s=8)
        count += len(b_segment)
    if count != 0:
        objects.append(Barrier(*b))

    # Detecting enemy and swirl
    # Detecting what color is enemy right now
    enemy_color = None
    swirl_color = None
    for color in all_colors_image:
        enemy = find_objects(obs, list(color), size=(8, 18), tol_s=2, minx=147)
        if not np.all(color == objects_colors["player"]):
            swirl = find_objects(
                obs, list(color), size=(8, 18), tol_s=2, maxx=125)
        for e in enemy:
            enemy_color = list(color)
            objects.append(Enemy(*e))
        for s in swirl:
            swirl_color = list(color)
            objects.append(Swirl(*s))
        e_m = find_objects(obs, list(color), size=(
            4, 2), tol_s=1, maxx=49, closing_active=False)
        for e in e_m:
            objects.append(Enemy_Missile(*e))
        e_m = find_objects(obs, list(color), size=(
            4, 2), tol_s=1, minx=81, closing_active=False)
        for e in e_m:
            objects.append(Enemy_Missile(*e))
    # detecting player bullet
    p_b = find_objects(obs, objects_colors["player"], size=(
        1, 2), tol_s=1, maxx=49, closing_active=False)
    for p in p_b:
        objects.append(Player_Bullet(*p))
    p_b = find_objects(obs, objects_colors["player"], size=(
        1, 2), tol_s=1, minx=81, closing_active=False)
    for p in p_b:
        objects.append(Player_Bullet(*p))

    # Currently throwing some unknown error
    # Detecting the fired Missile by Enemy

    shield = find_rectangle_objects(
        obs, objects_colors["shield"], max_size=(4, 8), minx=125)
    for s in shield:
        objects.append(Shield_Block(*s))

    if hud:
        pass
