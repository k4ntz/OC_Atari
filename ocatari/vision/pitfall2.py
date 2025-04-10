from .utils import find_objects, find_mc_objects, match_objects
from .game_objects import GameObject, NoObject


objects_colors = {
    "player": [[228, 111, 111], [92, 186, 92], [53, 95, 24]],
    "frog": [[82, 126, 45], [110, 156, 66]], "bat": [111, 111, 111], "scorpion": [236, 236, 236],
    "bird": [[134, 134, 29], [180, 122, 48], [195, 144, 61]], "bird_wing": [[[105, 105, 15], [236, 236, 236]], [[210, 164, 74]]],
    "serpant": [[0, 0, 0], [236, 236, 236]],
    "ballon": [[167, 26, 26], [184, 50, 50], [135, 183, 84], [66, 72, 200], [148, 0, 0], [170, 170, 170]],
    "rhonda": [[163, 57, 21], [228, 111, 111], [53, 95, 24], [135, 183, 84], [110, 156, 66], [20, 60, 0], [134, 134, 29]],
    "gold": [252, 252, 84], "red_cross": [163, 57, 21], "rat": [192, 192, 192], "ring": [[236, 236, 236], [252, 252, 84]],
    "quickclaw": [[162, 162, 42], [210, 210, 64]],
    "wall": [105, 105, 15], "platform": [187, 187, 53], "water": [45, 50, 184],
    "player_score": [214, 214, 214]
}

class Player(GameObject):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.rgb = 53, 95, 24
        self.hud = False

class Frog(GameObject):
    """
    The Frog.
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.rgb = 53, 95, 24
        self.hud = False


class Bat(GameObject):
    """
    The Bat.
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.rgb = 111, 111, 111
        self.hud = False


class Bird(GameObject):
    """
    The Bird.
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.rgb = 180, 122, 48
        self.hud = False


class Scorpion(GameObject):
    """
    The scorpions.
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.rgb = 236, 236, 236
        self.hud = False


class ElectricSerpent(GameObject):
    """
    The electric serpent.
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.rgb = 236, 236, 236
        self.hud = False


class Balloon(GameObject):
    """
    A ballon that transports the player to a higher level.
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.rgb = 167, 26, 26
        self.hud = False


class RedCross(GameObject):
    """
    The red cross. Is a checkpoint.
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.rgb = 163, 57, 21
        self.hud = False


class GoldBar(GameObject):
    """
    The collectable gold bars.
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.rgb = 252, 252, 84
        self.hud = False


class DiamondRing(GameObject):
    """
    The collectable diamond rings.
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.rgb = 252, 252, 84
        self.hud = False


class Rhonda(GameObject):
    """
    The friend to be rescued.
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.rgb = 110, 156, 66
        self.hud = False


class Quickclaw(GameObject):
    """
    The dancing cat to be rescued.
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.rgb = 162, 162, 42
        self.hud = False


class Rat(GameObject):
    """
    The rat. Can be collected.
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.rgb = 192, 192, 192
        self.hud = False


class Platform(GameObject):
    """
    Permanent platforms.
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.rgb = 187, 187, 53
        self.hud = False


class Wall(GameObject):
    """
    The underground brick walls.
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.rgb = 105, 105, 15
        self.hud = False


class Ladder(GameObject):
    """
    The escape shafts from the underground.
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.rgb = 105, 105, 15
        self.hud = False


class Water(GameObject):
    """
    The escape shafts from the underground.
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.rgb = 45, 50, 184
        self.hud = False


class PlayerScore(GameObject):
    """
    The player's score display (HUD).
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.rgb = 214, 214, 214
        self.hud = True

def _detect_objects(objects, obs, hud=False):
    
    player = find_mc_objects(obs, objects_colors["player"])
    if player:
        objects[0].xywh = player[0][0], player[0][1]-1, player[0][2], player[0][3]+1
    
    frog = find_mc_objects(obs, objects_colors["frog"])
    match_objects(objects, frog, 1, 4, Frog)
    
    bat = find_objects(obs, objects_colors["bat"], miny=30)
    match_objects(objects, bat, 5, 4, Bat)

    scorpion = find_objects(obs, objects_colors["scorpion"], size=(7, 10), tol_s=2)
    match_objects(objects, scorpion, 9, 4, Scorpion)

    bird = []
    for i in range(2):
        bird.extend(find_mc_objects(obs, objects_colors["bird"]+objects_colors["bird_wing"][i]))
    match_objects(objects, bird, 13, 4, Bird)

    es = []
    for i in range(2):
        es.extend(find_objects(obs, objects_colors["serpant"][i], size=(8, 2), tol_s=2, minx=9, miny=8, maxx=159, maxy=182))
    match_objects(objects, es, 17, 4, ElectricSerpent)

    gold = find_objects(obs, objects_colors["gold"], size=(7,14), tol_s=4)
    match_objects(objects, gold, 22, 4, GoldBar)

    red_cross = find_objects(obs, objects_colors["red_cross"], size=(7,7), tol_s=3)
    if red_cross:
        if type(objects[26]) is NoObject:
            objects[26] = RedCross(*red_cross[0])
        objects[26].xywh = red_cross[0]
    else:
        objects[26] = NoObject()

    rat = find_objects(obs, objects_colors["rat"])
    if rat:
        if type(objects[27]) is NoObject:
            objects[27] = Rat(*rat[0])
        objects[27].xywh = rat[0]
    else:
        objects[27] = NoObject()

    diamond = find_mc_objects(obs, objects_colors["ring"])
    if diamond:
        if type(objects[28]) is NoObject:
            objects[28] = DiamondRing(*diamond[0])
        objects[28].xywh = diamond[0]
    else:
        objects[28] = NoObject()

    rhonda = find_mc_objects(obs, objects_colors["rhonda"])
    if rhonda:
        if type(objects[29]) is NoObject:
            objects[29] = Rhonda(*rhonda[0])
        objects[29].xywh = rhonda[0]
    else:
        objects[29] = NoObject()

    quickclaw = find_mc_objects(obs, objects_colors["quickclaw"])
    if quickclaw:
        if type(objects[30]) is NoObject:
            objects[30] = Quickclaw(*quickclaw[0])
        objects[30].xywh = quickclaw[0][0], quickclaw[0][1]-2, quickclaw[0][2], quickclaw[0][3]+3
    else:
        objects[30] = NoObject()
    
    walls = find_objects(obs, objects_colors["wall"], size=(8, 20), tol_s=2)
    walls.extend(find_objects(obs, objects_colors["wall"], size=(16, 24), tol_s=2))
    match_objects(objects, walls, 31, 8, Wall)

    # ladders = find_objects(obs, objects_colors["wall"], size=(4,2), closing_dist=0, tol_s=0)
    ladders = find_objects(obs, objects_colors["wall"], minx=75, maxx=84, closing_dist=3)
    l = []
    for bb in ladders:
        if bb[0] == 78:
            l.append(bb)

    match_objects(objects, l, 39, 4, Ladder)

    platforms = find_objects(obs, objects_colors["platform"], size=(152, 9), tol_s=2)
    platforms.extend(find_objects(obs, objects_colors["platform"], size=(48, 9), tol_s=4))
    platforms.extend(find_objects(obs, objects_colors["platform"], size=(29, 9), tol_s=4))
    p = []
    for i, bb in enumerate(platforms):
        if bb[2] > 150:
            if obs[bb[1]+6][80][0] != 187:
                p.append((8, bb[1]+6, 68, 1))
                p.append((84, bb[1]+6, 76, 1))
            else:
                p.append((bb[0], bb[1]+6, bb[2], 1))
        elif bb[2] > 40:
            p.append((bb[0], bb[1]+6, bb[2], 1))
        else:
            if bb[0] == 64:
                p.append((bb[0], bb[1]+6, 12, 1))
                p.append((bb[0]+20, bb[1]+6, 12, 1))
            else:
                p.append((bb[0], bb[1]+6, bb[2], 1))

    match_objects(objects, p, 43, 16, Platform)

    if hud:

        score = find_objects(obs, objects_colors["player_score"], maxy=25, closing_dist=5)
        if score:
            objects[60].xywh = score[0]


