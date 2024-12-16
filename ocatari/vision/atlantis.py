from .utils import find_objects, find_mc_objects
from .game_objects import GameObject
from itertools import product

objects_colors = {"sentry": [[252, 224, 112], [111, 210, 111], [84, 138, 210], [184, 70, 162],
                             [187, 187, 53], [227, 151, 89]],
                  "aqua_plane": [[111, 210, 111], [101, 111, 228], [181, 108, 224], [212, 108, 195],
                                 [210, 164, 74], [252, 144, 144]],
                  "domed_palace": [[240, 170, 103], [232, 204, 99], [212, 108, 195], [128, 232, 128]],
                  "generator_1": [117, 231, 194],
                  "generator_2": [[111, 210, 111], [232, 204, 99], [101, 111, 228], [228, 111, 111],
                                  [127, 92, 213]],
                  "generator_3": [188, 144, 252],
                  "bridged_bazaar": [[214, 214, 214], [101, 111, 228], [149, 111, 227], [181, 108, 224],
                                     [212, 108, 195], [228, 111, 111], [227, 151, 89]],
                  "acropolis_command_post": [[227, 151, 89], [210, 210, 64], [210, 164, 74],
                                             [228, 111, 111], [164, 89, 208]],
                  "bandit_bomber": [[125, 48, 173], [45, 109, 152], [127, 92, 213], [158, 208, 101],
                                    [227, 151, 89], [184, 70, 162], [187, 187, 53]],
                  "gorgon_ship": [[125, 48, 173], [45, 109, 152], [127, 92, 213], [158, 208, 101],
                                  [227, 151, 89], [184, 70, 162], [187, 187, 53], [84, 138, 210]],
                  "gorgon_ship_2": [[125, 48, 173], [45, 109, 152], [127, 92, 213], [158, 208, 101],
                                    [227, 151, 89], [184, 70, 162], [187, 187, 53]],
                  "deathray": [[101, 209, 174], [72, 160, 72]], "score": [252, 188, 116],
                  "projectile": [[45, 109, 152], [84, 138, 210], [125, 48, 173], [127, 92, 213],
                                 [158, 208, 101], [164, 89, 208], [
                                     184, 70, 162], [187, 187, 53],
                                 [227, 151, 89], [228, 11, 111], [252, 188, 116]]
                  }


class Sentry(GameObject):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.rgb = 111, 210, 111


# No clue how the projectiles work
class Projectile(GameObject):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.rgb = 125, 48, 173
        # self.rgb = 184, 70, 162


class AquaPlane(GameObject):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.rgb = 252, 144, 144


class DomedPalace(GameObject):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.rgb = 240, 170, 103


class Generator(GameObject):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.rgb = 117, 231, 194


class BridgedBazaar(GameObject):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.rgb = 214, 214, 214


class AcropolisCommandPost(GameObject):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.rgb = 227, 151, 89


class BanditBomber(GameObject):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.rgb = 125, 48, 173


class GorgonShip(GameObject):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.rgb = 187, 187, 53


# Not implemented in vision due to it having the same colors as the environment
class Deathray(GameObject):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.rgb = 101, 209, 174


class Score(GameObject):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.rgb = 252, 188, 116


def _detect_objects(objects, obs, hud=True):
    objects.clear()

    sentry = find_mc_objects(
        obs, objects_colors["sentry"], min_distance=1, maxx=10, miny=110)
    for bb in sentry:
        objects.append(Sentry(*bb))

    sentry = find_mc_objects(
        obs, objects_colors["sentry"], min_distance=1, minx=150, miny=110)
    for bb in sentry:
        objects.append(Sentry(*bb))

    aqua_plane = find_mc_objects(
        obs, objects_colors["aqua_plane"], min_distance=1, minx=14, maxx=32, miny=110)
    for bb in aqua_plane:
        objects.append(AquaPlane(*bb))

    domed_palace = find_mc_objects(
        obs, objects_colors["domed_palace"], min_distance=1, minx=35, maxx=54, miny=110)
    for bb in domed_palace:
        objects.append(DomedPalace(*bb))

    generator_1 = find_objects(
        obs, objects_colors["generator_1"], min_distance=1, minx=59, maxx=70, miny=110)
    for bb in generator_1:
        objects.append(Generator(*bb))

    generator_2 = find_mc_objects(
        obs, objects_colors["generator_2"], min_distance=1, minx=80, maxx=90, miny=110)
    for bb in generator_2:
        g2 = Generator(*bb)
        g2.rgb = objects_colors["generator_2"][0]
        objects.append(g2)

    generator_3 = find_objects(
        obs, objects_colors["generator_3"], min_distance=1, minx=140, maxx=148, miny=110)
    for bb in generator_3:
        g3 = Generator(*bb)
        g3.rgb = objects_colors["generator_3"]
        objects.append(g3)

    bridged_bazaar = find_mc_objects(
        obs, objects_colors["bridged_bazaar"], min_distance=1, minx=94, maxx=112, miny=110)
    for bb in bridged_bazaar:
        objects.append(BridgedBazaar(*bb))

    acropolis_command_post = find_mc_objects(obs, objects_colors["acropolis_command_post"], min_distance=1, minx=70,
                                             maxx=80, miny=110)
    for bb in acropolis_command_post:
        objects.append(AcropolisCommandPost(*bb))

    bandit_bomber = find_mc_objects(obs, objects_colors["bandit_bomber"], min_distance=1, maxy=110,
                                    size=(9, 7), tol_s=1)
    for bb in bandit_bomber:
        objects.append(BanditBomber(*bb))

    gorgon_ship = find_mc_objects(obs, objects_colors["gorgon_ship"], min_distance=1, maxy=110,
                                  size=(15, 8), tol_s=5)

    gorgon_ship2 = find_mc_objects(obs, objects_colors["gorgon_ship_2"], min_distance=1, maxy=110,
                                   size=(15, 7), tol_s=5)
    for bb in gorgon_ship:
        objects.append(GorgonShip(*bb))

    for bb in gorgon_ship2:
        contains = False
        for gor in gorgon_ship:
            if bb[1] - 1 == gor[1] or bb[1] == gor[1]:
                contains = True
                break
        if not contains:
            objects.append(GorgonShip(*bb))

    # deathray = find_mc_objects(obs, objects_colors["deathray"], min_distance=1)
    # for bb in deathray:
    #     objects.append(Deathray(*bb))
    sizes = [(1, 1), (1, 2), (2, 1)]
    projectiles = sum([find_objects(obs, col, size=si, tol_s=0) for col,
                       si in product(objects_colors["projectile"], sizes)], [])

    projobjs = [Projectile(*bb) for bb in projectiles]
    valid_projobjs = [proj for proj in projobjs if not any(
        [proj.is_on_top(obj) for obj in objects])]
    objects.extend(valid_projobjs)

    if hud:
        score = find_objects(
            obs, objects_colors["score"], min_distance=1, miny=120, closing_dist=10)
        for bb in score:
            objects.append(Score(*bb))
