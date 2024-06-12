from .utils import find_objects, find_mc_objects
from .game_objects import GameObject

objects_colors = {"player": {"alive": [210, 210, 64], "dead": [200, 72, 72]}, "saucer": {"1": [170, 170, 170], "2": [236, 236, 236]},
                  "rejuvenator": [187, 187, 53], "blocker": [135, 183, 84], "jumper": [],
                  "charger": [], "bouncecraft": [], "chirper": [],
                  "sentinel": [[227, 151, 89], [184, 50, 50], [167, 26, 26], [158, 208, 101], [117, 128, 240]],
                  "rock": [134, 134, 29],
                  "player_projectile": [198, 108, 58], "torpedos": [164 , 89, 208], "torpedos_hud": [104, 25, 154],
                  "enemy_projectile": {"1": [164 ,89, 208], "2": [184, 70, 162]},
                  "hud": [210, 164, 74], "enemy_amount":[82, 126, 45], "life": [210, 210, 64]}


class Player(GameObject):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.rgb = 210, 210, 64


class Player_Projectile(GameObject):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.rgb = 198, 108, 58


class Torpedos(GameObject):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.rgb = 164 , 89, 208


class Saucer(GameObject):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.rgb = 236, 236, 236


class Rejuvenator(GameObject):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.rgb = 187, 187, 53


class Sentinel(GameObject):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.rgb = 184, 50, 50

class Blocker(GameObject):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.rgb = 135, 183, 84

class Jumper(GameObject):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.rgb = None


class Charger(GameObject):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.rgb = None

class Bouncecraft(GameObject):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.rgb = None

class Chriper(GameObject):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.rgb = None

class Rock(GameObject):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.rgb = 134, 134, 29


class Torpedos_Available(GameObject):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.rgb = 104, 25, 154


class Enemy_Projectile(GameObject):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.rgb = 164 ,89, 208


class HUD(GameObject):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.rgb = 210, 164, 74


class Enemy_Amount(GameObject):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.rgb = 82, 126, 45


class Life(GameObject):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.rgb = 210, 210, 64


def _detect_objects(objects, obs, hud=True):
    objects.clear()

    for i in objects_colors["player"]:
        player = find_objects(obs, objects_colors["player"][i], min_distance=1, maxy=181, miny=165)
        for bb in player:
            p = Player(*bb)
            p.rgb = objects_colors["player"][i]
            objects.append(p)

    player_projectile = find_objects(obs, objects_colors["player_projectile"], min_distance=1)
    for bb in player_projectile:
        objects.append(Player_Projectile(*bb))

    for i in range(3):
        torpedos = find_objects(obs, objects_colors["torpedos"], min_distance=1, size=(i*2+1,i*2+1), tol_s= 1)
        for bb in torpedos:
                objects.append(Torpedos(*bb))

    for i in objects_colors["saucer"]:
        saucer = find_objects(obs, objects_colors["saucer"][i], min_distance=1)
        for bb in saucer:
            s = Saucer(*bb)
            s.rgb = objects_colors["saucer"][i]
            objects.append(s)

    rejuvenator = find_objects(obs, objects_colors["rejuvenator"], min_distance=1, size=(3,4), tol_s=3)
    for bb in rejuvenator:
        objects.append(Rejuvenator(*bb))

    blocker = find_objects(obs, objects_colors["blocker"], min_distance=1)
    for bb in blocker:
        objects.append(Blocker(*bb))

    rock = find_objects(obs, objects_colors["rock"], min_distance=1)
    for bb in rock:
        objects.append(Rock(*bb))

    sentinel = find_mc_objects(obs, objects_colors["sentinel"], min_distance=1)
    for bb in sentinel:
        objects.append(Sentinel(*bb))

    enemy_projectile = find_objects(obs, objects_colors["enemy_projectile"]["1"], min_distance=1, size=(4,2), tol_s=1)
    for bb in enemy_projectile:
        p = Enemy_Projectile(*bb)
        p.rgb = objects_colors["enemy_projectile"][i]
        objects.append(p)

    enemy_projectile = find_objects(obs, objects_colors["enemy_projectile"]["2"], min_distance=1, size=(2,6), tol_s=1)
    for bb in enemy_projectile:
        p = Enemy_Projectile(*bb)
        p.rgb = objects_colors["enemy_projectile"][i]
        objects.append(p)

    if hud:
        hud_o = find_objects(obs, objects_colors["hud"], min_distance=1, closing_dist=5)
        for bb in hud_o:
            objects.append(HUD(*bb))

        enemy_amount = find_objects(obs, objects_colors["enemy_amount"], min_distance=1)
        for bb in enemy_amount:
            objects.append(Enemy_Amount(*bb))

        life = find_objects(obs, objects_colors["life"], min_distance=1, miny=181)
        for bb in life:
            objects.append(Life(*bb))

        torpedos_hub = find_objects(obs, objects_colors["torpedos_hud"], min_distance=1, maxy=100)
        for bb in torpedos_hub:
            objects.append(Torpedos_Available(*bb))
