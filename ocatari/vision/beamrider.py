from .utils import find_objects
from .game_objects import GameObject

objects_colors = {"player": [210, 210, 64], "saucer": {"1": [170, 170, 170], "2": [236, 236, 236]},
                  "rejuvenator": [187, 187, 53], "sentinel": [], "blocker": [],
                  "charger": [], "bouncecraft": [], "chirper": [],
                  "player_projectile": [198, 108, 58], "torpedos": [104, 25, 154],
                  "enemy_projectile": {"1": [164 ,89, 208], "2": [184, 70, 162]},
                  "hud": [210, 164, 74], "enemy_amount":[82, 126, 45], "life": [210, 210, 64]}


class Player(GameObject):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.rgb = 210, 210, 64


class Saucer(GameObject):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.rgb = 236, 236, 236


class Rejuvenator(GameObject):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.rgb = 227, 151, 89


class Sentinel(GameObject):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.rgb = None

class Blocker(GameObject):
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


class Player_Projectile(GameObject):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.rgb = 198, 108, 58


class Torpedos(GameObject):
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


def _detect_objects_beamrider(objects, obs, hud=True):
    objects.clear()

    player = find_objects(obs, objects_colors["player"], min_distance=1, maxy=181)
    for bb in player:
        objects.append(Player(*bb))

    player_projectile = find_objects(obs, objects_colors["player_projectile"], min_distance=1)
    for bb in player_projectile:
        objects.append(Player_Projectile(*bb))

    for i in objects_colors["saucer"]:
        saucer = find_objects(obs, objects_colors["saucer"][i], min_distance=1)
        for bb in saucer:
            if bb[1] < 170:
                s = Saucer(*bb)
                s.rgb = objects_colors["saucer"][i]
                objects.append(s)

    rejuvenator = find_objects(obs, objects_colors["rejuvenator"], min_distance=1)
    for bb in rejuvenator:
        objects.append(Rejuvenator(*bb))

    torpedos = find_objects(obs, objects_colors["torpedos"], min_distance=1)
    for bb in torpedos:
        objects.append(Torpedos(*bb))

    for i in objects_colors["enemy_projectile"]:
        enemy_projectile = find_objects(obs, objects_colors["enemy_projectile"][i], min_distance=1)
        for bb in enemy_projectile:
            if bb[1] < 170:
                p = Enemy_Projectile(*bb)
                p.rgb = objects_colors["enemy_projectile"][i]
                objects.append(p)

    hud = find_objects(obs, objects_colors["hud"], min_distance=1)
    for bb in hud:
        objects.append(HUD(*bb))

    enemy_amount = find_objects(obs, objects_colors["enemy_amount"], min_distance=1)
    for bb in enemy_amount:
        objects.append(Enemy_Amount(*bb))

    life = find_objects(obs, objects_colors["life"], min_distance=1, miny=181)
    for bb in life:
        objects.append(Life(*bb))
