from .game_objects import GameObject, ValueObject, NoObject
import sys
"""
RAM extraction for the game RIVER RAID. Supported modes: raw

ram mode does not seem feasible for this game. The problem is that for the objects like Helicopter, FuelDepot etc.
only a relative x-Position is found in the RAM. How the exact position is calculated is unknown, it is possible that
the size of the objects (is stored in the RAM) somehow affects the x-Position.
Furthermore there was no y-Position for the Objects found in the RAM. It could be the case that their y-Position is like
the players y-Position not stored in the RAM.
"""

MAX_NB_OBJECTS = {'Player': 1, 'PlayerMissile': 1, 'FuelDepot': 4, 'Tanker': 4, 'Helicopter': 4, 'House': 4, 'Jet': 4, 'Bridge': 1}
MAX_NB_OBJECTS_HUD = dict(MAX_NB_OBJECTS, **{'PlayerScore': 1, 'Lives': 1}) 


def twos_comp(val):
    """compute the 2's complement of int value val in 4 bits"""
    if (val & (1 << 3)) != 0:  # if sign bit is set e.g., 4bit: -8 -> 7
        val = val - (1 << 4)        # compute negative value
    return val


class _DescendingObject(GameObject):
    """
    A support class for objects descending on the screen.
    """

    _offset = None

    def __init__(self, xfr=0, x_off=0):
        super().__init__()
        self._xy = 15 * xfr - x_off, -5 - self.wh[1]
        self._ram_index = 5

    def _update_xy(self, xfr, x_off, yfr, y_off):  # xfr
        self._xy = 15 * xfr - x_off, yfr * 32 + y_off - self._offset
    


class Player(GameObject):
    """
    The player figure i.e., the jet.
    """

    def __init__(self):
        super().__init__()
        self._xy = 77, 145
        self.wh = 7, 13
        self.rgb = 232, 232, 74
        self.hud = False


class PlayerMissile(GameObject):
    """
    The missles shot from the player's jet.
    """

    def __init__(self):
        super().__init__()
        self._xy = 0, 0
        self.wh = 1, 8
        self.rgb = 232, 232, 74
        self.hud = False


class House(_DescendingObject):
    """
    The houses and Tree.
    """

    _offset = 20
    fh = 20  # final height

    def __init__(self, xfr=0, x_off=0):
        super().__init__(xfr, x_off)
        self.wh = 17, 20
        self.rgb = 232, 232, 232
        self.hud = False
        self.xy = self.xy[0], self.xy[1] - self.wh[1]
        self._lowest = False  # highest in the slot


class Helicopter(_DescendingObject):
    """
    The enemy helicopters.
    """

    _offset = 16
    fh = 10  # final height

    def __init__(self, xfr=0, x_off=0):
        super().__init__(xfr, x_off)
        self.wh = 8, 10
        self.rgb = 0, 64, 48
        self.hud = False
        self.xy = self.xy[0], self.xy[1] - self.wh[1]


class Tanker(_DescendingObject):
    """
    The enemy tankers.
    """

    _offset = 13
    fh = 9

    def __init__(self, xfr=0, x_off=0):
        super().__init__(xfr, x_off)
        self.wh = 17, 9
        self.rgb = 84, 160, 197
        self.hud = False


class Jet(_DescendingObject):
    """
    The enemy jets.
    """

    _offset = 15
    fh = 6

    def __init__(self, xfr=0, x_off=0):
        super().__init__(xfr, x_off)
        self.wh = 9, 6
        self.rgb = 117, 181, 239
        self.hud = False


class Bridge(_DescendingObject):
    """
    The bridge targets.
    """

    _offset = 17
    fh = 18

    def __init__(self, xfr=0, x_off=0):
        super().__init__(xfr, x_off)
        self.wh = 32, 18
        self.rgb = 134, 134, 29
        self.hud = False


class FuelDepot(_DescendingObject):
    """
    Fuel depots targets.
    """

    _offset = 23
    fh = 24

    def __init__(self, xfr=0, x_off=0):
        super().__init__(xfr, x_off)
        self.wh = 7, 24
        self.rgb = 210, 91, 94
        self.hud = False
        self.xy = self.xy[0], self.xy[1] - self.wh[1]


class PlayerScore(ValueObject):
    """
    The player's score display (HUD).
    """

    def __init__(self):
        super().__init__()
        self._xy = 97, 165
        self.rgb = 232, 232, 74
        self.wh = 6, 8
        self.hud = True

    def __eq__(self, o):
        return isinstance(o, PlayerScore) and self.xy == o.xy


class Lives(ValueObject):
    """
    The indicator for remaining jets (lives) (HUD).
    """

    def __init__(self):
        super().__init__()
        self._xy = 57, 192
        self.rgb = 232, 232, 74
        self.wh = 6, 8
        self.hud = True

#0 nothing, 1, 2, 3 is explosion
# 9th would be houseandtree
_ram_to_class = [None, None, None, None, 
                 Jet, Helicopter, Helicopter, Tanker, 
                 Bridge, House, FuelDepot]  
y_offsets = [None, None, None, None, 
             15, 6, 6, 5, 
             17, 1, 0]
obj_list_offs = [None, None, None, None, 
                 18, 10, 10, 6, 
                 22, 14, 2]


# MAX_NB_OBJECTS = {'Player': 1, 'PlayerMissile': 1, 'FuelDepot': 4, 'Tanker': 4, 'Helicopter': 4, 'House': 4, 'Jet': 4}

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


def _init_objects_ram(hud=False):
    """
    (Re)Initialize the objects
    """
    global cntr, prev11, prev70
    descending = [NoObject() for _ in range(21)]
    objects = [NoObject() for _ in range(2)] + descending  # Player, missile and the other objects
    objects[0]._prev11 = 0
    objects[0]._add_next_object = False

    if hud:
        objects.extend([PlayerScore(), NoObject()])
    return objects


def _get_lowest_idx(slot_list):
    if all(not obj for obj in slot_list):
        return -1
    for i, obj in enumerate(slot_list):
        if obj and obj._lowest:
            return i
    raise ValueError("No lowest object in slot")


def _detect_objects_ram(objects, ram_state, hud=False):
    player = objects[0]
    _prev11 = player._prev11
    _add_next_object = player._add_next_object
    if ram_state[58] == 0:
        if player:
            player = NoObject()
            player._prev11 = _prev11
            player._add_next_object = _add_next_object
            objects[0] = player
    elif not player:
        player = Player()
        player._prev11 = _prev11
        player._add_next_object = _add_next_object
        objects[0] = player
        player.xy = ram_state[51] + 1, 145
    else:
        player.xy = ram_state[51] + 1, 145

    missile = objects[1]
    # player missile
    if ram_state[117] != 0 and 162 - ram_state[50] >= 0:  # else not firing
        if not missile:
            missile = PlayerMissile()
            objects[1] = missile
        missile.xy = ram_state[117] - 1, 162 - ram_state[50]
    elif missile:
        objects[1] = NoObject()

    if ram_state[11] < player._prev11 and ram_state[37] > 3 and \
            not player._add_next_object: # new object from the top
        player._add_next_object = True
    if ram_state[58] == 223: # player is dead
        player._add_next_object = False
    y_off = ram_state[11]
    if player._add_next_object:
        obj_type = ram_state[37]
        offset = y_offsets[obj_type]
        if y_off - offset > 2: # add object
            xanchor = ram_state[25]
            x_off = twos_comp(ram_state[31]//16) - 6
            orientation = (ram_state[31] % 16)//8
            obj_type = ram_state[37]
            obj_class = _ram_to_class[obj_type]
            obj = obj_class(xanchor, x_off)
            obj.y = y_off - offset
            # insert object in the right slot
            ooff = obj_list_offs[obj_type]
            next_available_slots = 0
            if obj_type == 8: # bridge
                next_available_slots = 0
            else:
                for i in range(4):
                    if objects[ooff + i]:
                        next_available_slots = i + 1
                    elif next_available_slots:
                        break
            objects[ooff + next_available_slots%4] = obj
            player._add_next_object = False
    for j, obj in enumerate(objects[2:23]):
        if obj:
            # import ipdb; ipdb.set_trace()
            if ram_state[11] < player._prev11:
                obj._ram_index -= 1
            i = obj._ram_index
            if ram_state[32+i] < 4:
                objects[2+j] = NoObject()
                continue
            xanchor = ram_state[20+i]
            x_off = twos_comp(ram_state[26 + i]//16) - 6
            obj.orientation = (ram_state[26 + i] % 16)//8
            obj._update_xy(xanchor, x_off, 5-i, y_off)
            if obj.y + obj.h >= 162:
                obj.h = 163 - obj.y
            if obj.h <= 0:
                objects[2+j] = NoObject()
            if obj.y <= 2:
                obj.h = obj.fh + obj.y - 2
                obj._xy = obj._xy[0], 2
    if hud:
        score, lives = objects[23:25]
        if ram_state[64] > 24:
            objects[24] = NoObject()
        else:
            if not lives:
                lives = Lives()
                objects[24] = lives
            lives.value = ram_state[64] // 8
        score_value = riverraid_score(ram_state)
        score.value = score_value
        if score_value >= 100000:
            score.xy = 57, 165
            score.wh = 46, 8
        elif score_value >= 10000:
            score.xy = 65, 165
            score.wh = 38, 8
        elif score_value >= 1000:
            score.xy = 73, 165
            score.wh = 30, 8
        elif score_value >= 100:
            score.xy = 81, 165
            score.wh = 22, 8
        elif score_value >= 10:
            score.xy = 89, 165
            score.wh = 14, 8
        else:
            score.xy = 97, 165
            score.wh = 6, 8   
    player._prev11 = ram_state[11]
    return objects
    


def _detect_objects_riverraid_raw(info, ram_state):
    # for all the objects: the lowest RAM state so 20 for object position always references the object that is the next
    # object to leave the screen. So when a helicopter is passed and gets off the screen all other objects will move
    # one RAM position down.
    # only a relative position from 1 to 8. 1 equals to left side and 8 to the
    info["objects_pos"] = ram_state[20:26]
    # right side. However there is an offset or something to move the objects a little bit
    info["object_size"] = ram_state[26:32]  # size, orientation and offset
    # 10 = fuel depot, 6 = helicopter (normal), 7 = boat, 9 = house tree right,
    info["object_type"] = ram_state[32:38]
    # 1, 2 and 3 = destroyed, 0 invisible, 8 = bridge, 4 = jet, 5 = helicopter
    info["grass_layout"] = ram_state[14:20]
    # 35 = normal, 12 = canal, 7 = spreads
    info["water_width"] = ram_state[38:44]
    info["player_x"] = ram_state[51]  # start at x = 76, player_y is constant
    info["missile_x"] = ram_state[117]
    info["missile_y"] = ram_state[50]
    info["game_active"] = ram_state[53] # == 254
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
