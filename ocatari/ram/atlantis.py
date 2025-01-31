from .game_objects import GameObject, NoObject
import sys

"""
RAM extraction for the game Atlantis. Supported modes: ram.

"""

MAX_NB_OBJECTS = {'Projectile': 2, 'Sentry': 2, 'AcropolisCommandPost': 1, 'Generator': 3, 'DomedPalace': 1,
                  'BridgedBazaar': 1, 'AquaPlane': 1, 'GorgonShip': 4, 'Deathray': 1, 'BanditBomber': 3}
MAX_NB_OBJECTS_HUD = {'Projectile': 2, 'Sentry': 2, 'AcropolisCommandPost': 1, 'Generator': 3, 'DomedPalace': 1,
                      'BridgedBazaar': 1, 'AquaPlane': 1, 'GorgonShip': 4, 'Deathray': 1, 'BanditBomber': 3, 'Score': 1}


class Sentry(GameObject):
    """
    The left and right sentry posts.
    """

    def __init__(self):
        super(Sentry, self).__init__()
        self._xy = 0, 124
        self.wh = 8, 8
        self.rgb = 111, 210, 111
        self.hud = False


# No clue how the projectiles work
class Projectile(GameObject):
    """
    The projectiles shot from the sentry posts or the Acropolis Command Post.
    """

    def __init__(self):
        super().__init__()
        self._xy = 0, 0
        self.wh = 1, 1
        self.rgb = 184, 70, 162
        self.hud = False


class AquaPlane(GameObject):
    """
    The Aqua Plain district of the city.
    """

    def __init__(self):
        super(AquaPlane, self).__init__()
        self._xy = 16, 171
        self.wh = 16, 7
        self.rgb = 252, 144, 144
        self.hud = False


class DomedPalace(GameObject):
    """
    The Doomed Palace district of the city.
    """

    def __init__(self):
        super(DomedPalace, self).__init__()
        self._xy = 38, 148
        self.wh = 16, 8
        self.rgb = 240, 170, 103
        self.hud = False


class Generator(GameObject):
    """
    The three Generator Stations.
    """

    def __init__(self):
        super(Generator, self).__init__()
        self._xy = 62, 137
        self.wh = 4, 8
        self.rgb = 117, 231, 194
        self.hud = False


class BridgedBazaar(GameObject):
    """
    The Bridged Bazaar district of the city.
    """

    def __init__(self):
        super(BridgedBazaar, self).__init__()
        self._xy = 96, 159
        self.wh = 16, 8
        self.rgb = 214, 214, 214
        self.hud = False


class AcropolisCommandPost(GameObject):
    """
    The Acropolis Command Post that defends the centre of Atlantis.
    """

    def __init__(self):
        super(AcropolisCommandPost, self).__init__()
        self._xy = 72, 112
        self.wh = 8, 8
        self.rgb = 227, 151, 89
        self.hud = False


class BanditBomber(GameObject):
    """
    The fast Gorgon Bandit Bombers.
    """

    def __init__(self):
        super(BanditBomber, self).__init__()
        self._xy = 0, 0
        self.wh = 9, 7
        self.rgb = 125, 48, 173
        self.hud = False


class GorgonShip(GameObject):
    """
    The Large Gorgon Vessels.
    """

    def __init__(self):
        super(GorgonShip, self).__init__()
        self._xy = 0, 0
        self.wh = 15, 8
        self.rgb = 187, 187, 53
        self.hud = False


class Deathray(GameObject):
    """
    The deathray fired by close Gorgon units.
    """

    def __init__(self):
        super(Deathray, self).__init__()
        self._xy = 0, 92
        self.wh = 2, 88
        self.rgb = 101, 209, 174
        self.hud = False


class Score(GameObject):
    """
    The player's score display.
    """

    def __init__(self):
        super(Score, self).__init__()
        self._xy = 96, 188
        self.wh = 7, 10
        self.rgb = 252, 188, 116
        self.hud = False


def _init_objects_ram(hud=True):
    """
    (Re)Initialize the objects
    """
    gen_pruple = Generator()
    gen_green = Generator()
    gen_mc = Generator()
    objects = [NoObject() for _ in range(2)] + [Sentry(), Sentry()] + \
        [AcropolisCommandPost()] + [gen_mc, gen_green, gen_pruple] + \
        [DomedPalace()] + [BridgedBazaar()] + [AquaPlane()] + \
        [NoObject() for _ in range(8)]
    gen_mc.xy = 82, 124
    gen_mc.rgb = 111, 210, 111
    gen_pruple.xy = 142, 137
    gen_pruple.rgb = 188, 144, 252
    objects[3].xy = 152, 112 # Sentry right

    if hud:
        objects += [NoObject()] # Score
    return objects


# parses MAX_NB* dicts, returns default init list of objects
def _get_max_objects(hud=False):
    def fromdict(max_obj_dict):
        objects = []
        mod = sys.modules[__name__]
        for k, v in max_obj_dict.items():
            for _ in range(0, v):
                objects.append(getattr(mod, k)())
        return objects

    if hud:
        return fromdict(MAX_NB_OBJECTS_HUD)
    return fromdict(MAX_NB_OBJECTS)


# Determines whether the deathray can be used by the ships or not
# global ray_available
# Saves the previous amount of buildings that are still standing
# global buildings_amount

# global prev_x_p1
# global prev_x_p2


def missile_pos(rs):
    if 182 <= rs:
        return 201 - rs
    elif 164 <= rs:
        return 202 - rs
    elif 145 <= rs:
        return 203 - rs
    elif 126 <= rs:
        return 204 - rs
    elif 114 <= rs:
        return 205 - rs
    elif 106 <= rs:
        return 206 - rs
    elif 104 <= rs:
        return 207 - rs
    else:
        return 208 - rs


def _detect_objects_ram(objects, ram_state, hud=True):
    proj1, proj2 = objects[0:2]
    # left canon : ram_state[61] % 3 == 2
    # middle canon : ram_state[61] % 3 == 0
    # right canon : ram_state[61] % 3 == 1
    if ram_state[59] != 0 and ram_state[61] != 0:
        if not proj1:
            proj1 = Projectile()
            objects[0] = proj1
        if ram_state[61] % 3 == 2: # left
            proj1.xy = ram_state[61]-3, missile_pos(ram_state[59])-1
        elif ram_state[61] % 3 == 0: # middle
            proj1.xy = ram_state[61], missile_pos(ram_state[59])
        else: # right
            proj1.xy = ram_state[61]+3, missile_pos(ram_state[59])-1
    elif proj1:
        objects[0] = NoObject()

    if ram_state[58] != 0 and ram_state[60] != 0:
        if not proj2:
            proj2 = Projectile()
            objects[1] = proj2
        if ram_state[60] % 3 == 2: # left
            proj2.xy = ram_state[60]-3, missile_pos(ram_state[58])-1
        elif ram_state[60] % 3 == 0: # middle
            proj2.xy = ram_state[60], missile_pos(ram_state[58])
        else: # right
            proj2.xy = ram_state[60]+3, missile_pos(ram_state[58])-1
    elif proj2:
        objects[1] = NoObject()
    
    object_classes = [AcropolisCommandPost, Generator, Generator, Generator, DomedPalace, BridgedBazaar, AquaPlane] 
    for i, base_cls in enumerate(object_classes):
        if ram_state[84+i]: # object destroyed
            if objects[4+i]:
                objects[4+i] = NoObject()
        elif not objects[4+i]:
            recovered = base_cls()
            if i == 3:
                recovered.xy = 82, 124
                recovered.rgb = 111, 210, 111
            elif i == 5:
                recovered.xy = 142, 137
                recovered.rgb = 188, 144, 252
            objects[4+i] = recovered
# MAX_NB_OBJECTS = {'Projectile': 2, 'Sentry': 2, 'AcropolisCommandPost': 1, 'Generator': 3, 'DomedPalace': 1,
#                   'BridgedBazaar': 1, 'AquaPlane': 1, 'GorgonShip': 4, 'Deathray': 1, 'BanditBomber': 3}
    # # Enemy ships and the DeathRay
    # global ray_available
    # global buildings_amount

    # for i in range(4):
    #     if ram_state[36+i]:
    #         ship = _get_ship_type(ram_state, 0+i, 128+i)
    #         g_s = NoObject()
    #         if not ship:
    #             continue
    
    #         # calc speed and orientation offset
    #         if not ram_state[75+ship] & 128:
    #             offset = ram_state[75+ship]
    #             if ram_state[79+ship] == 64:
    #                 g_s = GorgonShip()
    #                 g_s.xy = ram_state[36+i] - 7 - offset, 82 - 21*i
    #             elif ram_state[79+ship] == 32 or ram_state[79+ship] == 48:
    #                 g_s = GorgonShip()
    #                 g_s.wh = 15, 7
    #                 g_s.xy = ram_state[36+i] - 7 - offset, 83 - 21*i
    #             elif ram_state[79+ship] == 80:
    #                 g_s = BanditBomber()
    #                 g_s.xy = ram_state[36+i] - 5 - offset, 83 - 21*i
    #         else:
    #             offset = 255 - ram_state[75+ship]
    #             if ram_state[79+ship] == 64:
    #                 g_s = GorgonShip()
    #                 g_s.xy = ram_state[36+i] - 7 + offset, 82 - 21*i
    #             elif ram_state[79+ship] == 32 or ram_state[79+ship] == 48:
    #                 g_s = GorgonShip()
    #                 g_s.wh = 15, 7
    #                 g_s.xy = ram_state[36+i] - 7 + offset, 83 - 21*i
    #             elif ram_state[79+ship] == 80:
    #                 g_s = BanditBomber()
    #                 g_s.xy = ram_state[36+i] - 3 + offset, 83 - 21*i
    #         if g_s:
    #             objects[2+i] = g_s
    
    #         # Deathray can only be shot by ships on lane 4
    #         if not i and ram_state[30] < 152 and ray_available:
    #             ray = Deathray()
    #             if not ram_state[75+ship] & 128:
    #                 ray.xy = ram_state[36] - 1, 92
    #             else:
    #                 ray.xy = ram_state[36] + 1, 92
    #             objects[13] = ray

    # # Command-Post center building with gun
    # if ram_state[84] == 0:
    #     objects[6] = AcropolisCommandPost()
    #     buildings_count += 1

    # # Generator left
    # if ram_state[22] < 152:
    #     gen = Generator()
    #     gen.xy = 82, 124
    #     gen.rgb = 111, 210, 111
    #     objects[7] = gen
    #     buildings_count += 1

    # # Generator Command-Post
    # if ram_state[23] < 152:
    #     objects[8] = Generator()
    #     buildings_count += 1

    # # Generator right
    # if ram_state[24] < 152:
    #     gen = Generator()
    #     gen.xy = 142, 137
    #     gen.rgb = 188, 144, 252
    #     objects[9] = gen
    #     buildings_count += 1

    # # Domed-Palace building with dome
    # if ram_state[25] < 152:
    #     objects[10] = DomedPalace()
    #     buildings_count += 1

    # # Bridged-Bazaar rightmost building
    # if ram_state[26] < 152:
    #     objects[11] = BridgedBazaar()
    #     buildings_count += 1

    # # Aqua-Plane leftmost building
    # if ram_state[27] < 152:
    #     objects[12] = AquaPlane()
    #     buildings_count += 1

    # # Determines if the deathray is usable
    # if ram_state[30] == 152:
    #     ray_available = True
    # elif buildings_count < buildings_amount:
    #     ray_available = False

    # buildings_amount = buildings_count

    # if hud:
    #     # Score
    #     if ram_state[33] or ram_state[34] or ram_state[35]:
    #         score = Score()
    #         if ram_state[33] >= 16:
    #             score.wh = 15, 10
    #             score.xy = 88, 188
    #         if ram_state[34] > 0:
    #             score.wh = 23, 10
    #             score.xy = 80, 188
    #         if ram_state[34] >= 16:
    #             score.wh = 31, 10
    #             score.xy = 72, 188
    #         if ram_state[35] > 0:
    #             score.wh = 39, 10
    #             score.xy = 64, 188
    #         if ram_state[35] >= 16:
    #             score.wh = 47, 10
    #             score.xy = 56, 188
    #         objects[16] = score

    # return objects


def _get_ship_type(ram_state, height1, height2):
    """
    Determines the type of ship by its sprite index
    """
    for i in range(4):
        if ram_state[71+i] == height1 or ram_state[71+i] == height2:
            return i
    return None


def _detect_objects_atlantis_raw(info, ram_state):
    """
    Raw ram-slice for playing the game with minimum requirements
    """

    enemy_x = ram_state[36:40]
    player_projectile = ram_state[58:62]
    # score ram_state[33:36]
    info["ram_slice"] = enemy_x + player_projectile
