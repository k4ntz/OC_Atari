from .utils import find_objects, find_mc_objects
from .game_objects import GameObject

objects_colors = {"sentry": [[252, 224, 112], [111, 210, 111], [84, 138, 210], [184, 70, 162], [187, 187, 53], [227, 151, 89]],
                  "aqua_plane": [[111, 210, 111], [101, 111, 228], [181, 108, 224], [212, 108, 195], [210, 164, 74], [252, 144, 144]],
                  "domed_palace": [[240, 170, 103], [232, 204, 99], [212, 108, 195], [128, 232, 128]],
                  "generator_1": [117, 231, 194], "generator_2": [[92, 168, 92], [111, 210, 111], [232, 204, 99], [101, 111, 228], [228, 111, 111], [127, 92, 213]], "generator_3": [188, 144,252],
                  "bridged_bazaar": [[214, 214, 214], [101, 111, 228], [149, 111, 227], [181, 108, 224], [212, 108, 195], [228, 111, 111], [227, 151, 89]],
                  "acropolis_command_post": [[227, 151, 89], [210, 210, 64], [210, 164, 74], [228, 111, 111], [164, 89, 208]],
                  "bandit_bomber": [[125, 48, 173], [45, 109, 152], [127, 92, 213], [158, 208, 101], [227, 151, 89], [184, 70, 162], [187, 187, 53]],
                  "gorgon_ship": [[125, 48, 173], [45, 109, 152], [127, 92, 213], [158, 208, 101], [227, 151, 89], [184, 70, 162], [187, 187, 53], [84, 138, 210]],
                  "deathray": [[101, 209, 174], [72, 160, 72]], "score": [252, 188, 116]
                  }


class Sentry(GameObject):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.rgb = 111, 210, 111


class Aqua_plane(GameObject):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.rgb = 252, 144, 144


class Domed_Palace(GameObject):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.rgb = 240, 170, 103


class Generator(GameObject):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.rgb = 117, 231, 194


class Bridged_Bazaar(GameObject):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.rgb = 214, 214, 214


class Acropolis_Command_Post(GameObject):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.rgb = 227, 151, 89


class Bandit_Bomber(GameObject):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.rgb = 125, 48, 173


class Gorgon_Ship(GameObject):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.rgb = 187, 187, 53


class Deathray(GameObject):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.rgb = 101, 209, 174


class Score(GameObject):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.rgb = 252, 188, 116


def _detect_objects_atlantis(objects, obs, hud=True):
    objects.clear()

    sentry = find_mc_objects(obs, objects_colors["sentry"], min_distance=1, maxx=10, miny=110)
    for bb in sentry:
        objects.append(Sentry(*bb))

    sentry = find_mc_objects(obs, objects_colors["sentry"], min_distance=1, minx=150, miny=110)
    for bb in sentry:
        objects.append(Sentry(*bb))

    aqua_plane = find_mc_objects(obs, objects_colors["aqua_plane"], min_distance=1, minx=14, maxx=32, miny=110)
    for bb in aqua_plane:
        objects.append(Aqua_plane(*bb))

    domed_palace = find_mc_objects(obs, objects_colors["domed_palace"], min_distance=1, minx=35, maxx=55, miny=110)
    for bb in domed_palace:
        objects.append(Domed_Palace(*bb))

    generator_1 = find_objects(obs, objects_colors["generator_1"], min_distance=1, minx=61, maxx=66, miny=110)
    for bb in generator_1:
        objects.append(Generator(*bb))

    generator_2 = find_mc_objects(obs, objects_colors["generator_2"], min_distance=0)  # , minx=80, maxx=87, miny=110
    for bb in generator_2:
        g2 = Generator(*bb)
        g2.rgb = objects_colors["generator_2"][0]
        objects.append(Generator(*bb))

    generator_3 = find_objects(obs, objects_colors["generator_3"], min_distance=1, minx=142, maxx=145, miny=110)
    for bb in generator_3:
        g3 = Generator(*bb)
        g3.rgb = objects_colors["generator_3"]
        objects.append(g3)
