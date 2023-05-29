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

# MAX_NB_OBJECTS = {"Player": 1, "PlayerMissile": 1, "Bridge": 1, "Tanker": 6, "FuelDepot": 6,
#                   "Helicopter": 6, "Jet": 6}
MAX_NB_OBJECTS = {'PlayerScore': 6, 'Lives': 1}
MAX_NB_OBJECTS_HUD = {'PlayerScore': 6, 'Lives': 1}


class _DescendingObject(GameObject):
    _offset = None
    
    def __init__(self, xfr):
        super().__init__()
        self._xy = self._offset + 15 * xfr, 0
    
    def _update_xy(self, xfr, offset): # xfr
        self._xy = self._offset + 15 * xfr, self._xy[1] + offset


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


class Helicopter(_DescendingObject):
    _offset = 6
    def __init__(self, xfr):
        super().__init__(xfr)
        self.wh = 8, 10
        self.rgb = 0, 64, 48
        self.hud = False
    
    def _update_xy(self, xfr, offset): # xfr
        self._xy = self._offset + 15 * xfr, self._xy[1] + 2 * offset


class Tanker(_DescendingObject):
    _offset = 12
    def __init__(self, xfr):
        super().__init__(xfr)
        self.wh = 16, 8
        self.rgb = 84, 160, 197
        self.hud = False


class Jet(_DescendingObject):
    _offset = 12
    def __init__(self, xfr):
        super().__init__(xfr)
        self.wh = 10, 10
        self.rgb = 117, 181, 239
        self.hud = False


class Bridge(_DescendingObject):
    _offset = 12
    def __init__(self, xfr):
        super().__init__(xfr)
        self.wh = 10, 10
        self.rgb = 134, 134, 29
        self.hud = False


class FuelDepot(_DescendingObject):
    _offset = 1
    def __init__(self, xfr):
        super().__init__(xfr)
        self.wh = 7, 24
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


_ram_to_class = [None, None, None, None, Jet, Helicopter, None, Tanker, Bridge, None, FuelDepot] # 9th would be houseandtree
global cntr, prev70


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
    objects = [None] * 8 # Player, missile and 6 objects
    global cntr, prev70
    cntr, prev70 = 0, None
    if hud:
        objects.extend([PlayerScore(), Lives()])

    # objects.extend([Bridge(), Jet(), Helicopter(), Tanker(), FuelDepot()])
    return objects


def _detect_objects_riverraid_revised(objects, ram_state, hud=False):
    # player = objects[0]
    # if ram_state[70]:
    #     objects[0] = None
    # elif player is None:
    #     player = Player()
    #     objects[0] = player
    #     player.xy = ram_state[51] + 1, 145
    # else:
    #     player.xy = ram_state[51] + 1, 145

    # missile = objects[1]
    # # player missile
    # if ram_state[117] != 0 and 162 - ram_state[50] >= 0:  # else not firing
    #     if missile is None:
    #         missile = PlayerMissile()
    #         objects[1] = missile
    #     missile.xy = ram_state[117] - 1, 162 - ram_state[50]
    # elif missile is not None:
    #     objects[1] = None
    
    global cntr, prev70
    framskips = (cntr - ram_state[2]) % 256
    if ram_state[70] == 0 or ram_state[70] != prev70:
        speed = 1
    else: # hasn't fired yet
        speed = 0
    # print(framskips)
    # print(ram_state[70])
    if prev70 == 0 and ram_state[70]:
        objects[2:8] = [None] * 6
    for i in range(6):
        eobj = objects[2+i]
        obj_type = ram_state[32 + i]
        obj_class = _ram_to_class[obj_type]
        if obj_class is not None:
            if not isinstance(eobj, obj_class):
                if i < 5 and isinstance(objects[3+i], obj_class): # moving down
                    eobj = objects[3+i]
                    objects[3+i] = None
                    eobj._update_xy(ram_state[20+i], framskips * speed)
                elif eobj is None:
                    eobj = obj_class(ram_state[20+i])
                objects[2+i] = eobj
            else:
                eobj._update_xy(ram_state[20+i], framskips * speed)


    # if hud:
    #     score, lives, _ = objects[9:12]
    #     score_value = riverraid_score(ram_state)
    #     if score_value >= 10:
    #         score.xy = 89, 165
    #         score.wh = 6, 8

    #     if score_value >= 100:
    #         score.xy = 81, 165
    #         score.wh = 6, 8

    #     if score_value >= 1000:
    #         score.xy = 73, 165
    #         score.wh = 6, 8

    #     if score_value >= 10000:
    #         score.xy = 65, 165
    #         score.wh = 6, 8
    cntr = ram_state[2]
    prev70 = ram_state[70]

    #     if score_value >= 100000:
    #         score.xy = 57, 165
    #         score.wh = 6, 8





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
