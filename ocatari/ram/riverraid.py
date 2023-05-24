from .game_objects import GameObject
import sys
"""
RAM extraction for the game RIVER RAID. Supported modes: raw

Revised mode does not seem feasible for this game. The problem is that for the objects like Helicopter, FuelDepot etc.
only a relative x-Position is found in the RAM. How the exact position is calculated is unknown, it is possible that
the size of the objects (is stored in the RAM) somehow affects the x-Position.
Furthermore there was no y-Position for the Objects found in the RAM. It could be the case that their y-Position is like
the players y-Position not stored in the RAM.
"""

MAX_NB_OBJECTS = {"Player": 1, "PlayerMissile": 1, "Bridge": 1, "Tanker": 6, "FuelDepot": 6,
                  "Helicopter": 6, "Jet": 6}
MAX_NB_OBJECTS_HUD = {'PlayerScore': 6, 'Lives': 1, 'Logo': 1}


class Player(GameObject):
    def __init__(self):
        self._xy = 77, 145
        self.wh = 7, 13
        self.rgb = 232, 232, 74
        self.hud = False


class PlayerMissile(GameObject):
    def __init__(self):
        self._xy = 0, 0
        self.wh = 1, 8
        self.rgb = 232, 232, 74
        self.hud = False


class Helicopter(GameObject):
    def __init__(self):
        self._xy = 0, 0
        self.wh = 8, 7
        self.rgb = 0, 64, 48
        self.hud = False


class Tanker(GameObject):
    def __init__(self):
        self._xy = 0, 0
        self.wh = 12, 2
        self.rgb = 84, 160, 197
        self.hud = False


class Jet(GameObject):
    def __init__(self):
        self._xy = 0, 0
        self.wh = 10, 10
        self.rgb = 117, 181, 239
        self.hud = False


class Bridge(GameObject):
    def __init__(self):
        self._xy = 0, 0
        self.wh = 10, 10
        self.rgb = 134, 134, 29
        self.hud = False


class FuelDepot(GameObject):
    def __init__(self):
        self._xy = 0, 0
        self.wh = 10, 10
        self.rgb = 210, 91, 94
        self.hud = False


class PlayerScore(GameObject):
    def __init__(self):
        self._xy = 97, 165
        self.rgb = 232, 232, 74
        self.wh = 6, 8
        self.hud = True

    def __eq__(self, o):
        return isinstance(o, PlayerScore) and self.xy == o.xy


class Lives(GameObject):
    def __init__(self):
        self._xy = 57, 192
        self.rgb = 232, 232, 74
        self.wh = 6, 8
        self.hud = True


class Logo(GameObject):
    def __init__(self):
        self._xy = 72, 193
        self.rgb = 232, 232, 74
        self.wh = 32, 7
        self.hud = True


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


def _init_objects_riverraid_ram(hud=False):
    """
    (Re)Initialize the objects
    """
    objects = [Player()]

    if hud:
        objects.extend([PlayerScore(), Lives(), Logo()])

    objects.extend([Bridge(), Jet(), Helicopter(), Tanker(), FuelDepot()])
    return objects


def _detect_objects_riverraid_revised(objects, ram_state, hud=False):
    player = objects[0]

    player.xy = ram_state[51] + 1, 145

    if hud:
        del objects[4:]
    else:
        del objects[1:]

    obj = _calculate_objects(ram_state)
    objects.extend(obj)

    if hud:
        score, lives = objects[1:3]
        score_value = riverraid_score(ram_state)
        if score_value >= 10:
            sc = PlayerScore()
            score.xy = 89, 165
            score.wh = 6, 8
            objects.append(sc)

        if score_value >= 100:
            sc = PlayerScore()
            sc.xy = 81, 165
            sc.wh = 6, 8
            objects.append(sc)

        if score_value >= 1000:
            sc = PlayerScore()
            sc.xy = 73, 165
            sc.wh = 6, 8
            objects.append(sc)

        if score_value >= 10000:
            sc = PlayerScore()
            sc.xy = 65, 165
            sc.wh = 6, 8
            objects.append(sc)

        if score_value >= 100000:
            sc = PlayerScore()
            sc.xy = 57, 165
            sc.wh = 6, 8
            objects.append(sc)


def _calculate_objects(ram_state):
    objects = []

    # player missile
    if ram_state[117] != 0 and 162 - ram_state[50] >= 0:  # else not firing
        missile = PlayerMissile()
        missile.xy = ram_state[117] - 1, 162 - ram_state[50]
        objects.append(missile)

    # objects
    for i in range(6):
        obj_type = ram_state[32 + i]
        if obj_type == 4:
            obj_instance = Jet()
        elif obj_type == 5:
            obj_instance = Helicopter()
        elif obj_type == 7:
            obj_instance = Tanker()
        elif obj_type == 8:
            obj_instance = Bridge()
        else:
            continue

        # obj_pos = ram_state[20 + i]
        # Add here x and y-Position for the objects
        obj_instance.xy = 0, 0
    return objects


def _detect_objects_riverraid_raw(info, ram_state):
    # for all the objects: the lowest RAM state so 20 for object position always references the object that is the next
    # object to leave the screen. So when a helicopter is passed and gets off the screen all other objects will move
    # one RAM position down.

    info["objects_pos"] = ram_state[20:26]  # only a relative position from 1 to 8. 1 equals to left side and 8 to the
    # right side. However there is an offset or something to move the objects a little bit
    info["object_size"] = ram_state[26:32]
    info["object_type"] = ram_state[32:38]  # 10 = fuel depot, 6 = helicopter (normal), 7 = boat, 9 = house tree right,
    # 1, 2 and 3 = destroyed, 0 invisible, 8 = bridge, 4 = jet, 5 = helicopter
    info["grass_layout"] = ram_state[14:20]
    info["water_width"] = ram_state[38:44]  # 35 = normal, 12 = canal, 7 = spreads
    info["player_x"] = ram_state[51]  # start at x = 76, player_y is constant
    info["missile_x"] = ram_state[117]
    info["missile_y"] = ram_state[50]
    info["fuel_meter_high"] = ram_state[55]
    info["fuel_meter_low"] = ram_state[56]
    info["lives_"] = (ram_state[64] / 8) + 1
    info["score"] = riverraid_score(ram_state)
    info["fuel_meter"] = (ram_state[55] / 255) * 100


def riverraid_score(ram_state):
    """
    Returns the current score for River Raid. Each digit up to the hundreds of thousands position
    has its own RAM position. However in the RAM is the digit value times 8 represented f.e.
    ram value 24 represents a three on screen.

    Args:
        ram_state: current RAM representation of the game

    Returns:
        score (int): current score
    """
    score = 0
    # hundreds of thousands
    if ram_state[77] != 88:  # if the ram value is 88, the digit is not shown on the screen
        score = score + 100000 * ram_state[77] / 8
    # ten thousands
    if ram_state[79] != 88:
        score = score + 10000 * ram_state[79] / 8
    # thousands
    if ram_state[81] != 88:
        score = score + 1000 * ram_state[81] / 8
    # hundreds
    if ram_state[83] != 88:
        score = score + 100 * ram_state[83] / 8
    # tens
    if ram_state[85] != 88:
        score = score + 10 * ram_state[85] / 8
    # ones
    if ram_state[87] != 88:
        score = score + ram_state[87] / 8

    return score
