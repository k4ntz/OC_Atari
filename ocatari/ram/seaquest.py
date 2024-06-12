import sys
from typing import Type, Sequence, Dict

from ._helper_methods import _convert_number
from .game_objects import GameObject, ValueObject, Orientation
from itertools import chain

"""
RAM extraction for the game SEAQUEST. Supported modes: ram.
"""

MAX_ESSENTIAL_OBJECTS = {
    'Player': 1,
    'Diver': 4,
    'Shark': 12,
    'Submarine': 12,
    'SurfaceSubmarine': 1,
    'PlayerMissile': 1,
    'EnemyMissile': 4,
    'Lives': 1,
    'OxygenBar': 1,
    'CollectedDiver': 6,
}

MAX_OPTIONAL_OBJECTS = {
    'PlayerScore': 1,
    'OxygenBarDepleted': 1,
    'OxygenBarLogo': 1,
}

# MAX_ALL_OBJECTS = dict(MAX_ESSENTIAL_OBJECTS.items()|MAX_OPTIONAL_OBJECTS.items())
MAX_ALL_OBJECTS = dict(chain(MAX_ESSENTIAL_OBJECTS.items(),MAX_OPTIONAL_OBJECTS.items()))


class Player(GameObject):
    """
    The player figure, i.e., the submarine.
    """

    def __init__(self):
        super().__init__()
        self._xy = 76, 46
        self.wh = 16, 11
        self.rgb = 187, 187, 53
        self.hud = False
        self.orientation = Orientation.E  # E is right, W is left
        self.crashed = False


class Diver(GameObject):
    """
    The divers to be retrieved and rescued.
    """

    def __init__(self):
        super().__init__()
        self._xy = 0, 0
        self.wh = 8, 11
        self.rgb = 66, 72, 200
        self.hud = False


class Shark(GameObject):
    """
    The killer sharks.
    """

    def __init__(self):
        super().__init__()
        self._xy = 0, 0
        self.wh = 8, 7
        self.rgb = 92, 186, 92
        self.hud = False


class Submarine(GameObject):
    """
    The enemy submarines.
    """

    def __init__(self):
        super().__init__()
        self._xy = 0, 0
        self.wh = 8, 11
        self.rgb = 170, 170, 170
        self.hud = False


class SurfaceSubmarine(Submarine):
    """
    Spawns right at the surface, but only in later games.
    """


class EnemyMissile(GameObject):
    """
    The torpedoes fired from enemy submarines.
    """

    def __init__(self):
        super().__init__()
        self._xy = 0, 0
        self.wh = 6, 4
        self.rgb = 66, 72, 200
        self.hud = False


class PlayerMissile(GameObject):
    """
    The torpedoes launched from the player's submarine.
    """

    def __init__(self):
        super().__init__()
        self._xy = 0, 0
        self.wh = 8, 1
        self.rgb = 187, 187, 53
        self.hud = False


class PlayerScore(ValueObject):
    """
    The player's score display (HUD).
    """

    def __init__(self):
        super().__init__()
        self._xy = 99, 9
        self.rgb = 210, 210, 64
        self.wh = 6, 8
        self.hud = True
        self.value = 0

    def __eq__(self, o):
        return isinstance(o, PlayerScore) and self.xy == o.xy


class Lives(ValueObject):
    """
    The indidcator for remaining reserve subs (lives) (HUD).
    """

    def __init__(self):
        super().__init__()
        self._xy = 58, 22
        self.rgb = 210, 210, 64
        self.wh = 23, 8
        self.hud = True
        self.value = 3


class OxygenBar(ValueObject):
    """
    The oxygen gauge (HUD).
    """

    def __init__(self):
        super().__init__()
        self._xy = 49, 170
        self.rgb = 214, 214, 214
        self.wh = 63, 5
        self.hud = True
        self.value = 0


class OxygenBarDepleted(ValueObject):
    """
    The empty oxygen bar (HUD).
    """

    def __init__(self):
        super().__init__()
        self._xy = 49, 170
        self.rgb = 163, 57, 21
        self.wh = 63, 5
        self.hud = True
        self.value = 64


class OxygenBarLogo(GameObject):
    """
    The 'OXYGEN' lettering next to the oxygen gauge (HUD).
    """

    def __init__(self):
        super().__init__()
        self._xy = 15, 170
        self.rgb = 0, 0, 0
        self.wh = 23, 5
        self.hud = True


class CollectedDiver(GameObject):
    """
    The indicator for collected divers (HUD).
    """

    def __init__(self):
        super().__init__()
        self._xy = 0, 0
        self.rgb = 24, 26, 167
        self.wh = 8, 9
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
        return fromdict(MAX_ALL_OBJECTS)
    return fromdict(MAX_ESSENTIAL_OBJECTS)


def _init_all_objects() -> Dict[Type[GameObject], Sequence[GameObject]]:
    mod = sys.modules[__name__]
    all_objects = {}
    for obj_cls_name, max_obj_count in MAX_ALL_OBJECTS.items():
        obj_cls = getattr(mod, obj_cls_name)
        all_objects[obj_cls] = max_obj_count * [None]
    return all_objects


objects = _init_all_objects()


def _update_object(obj_cls: Type[GameObject], attr: str, value, idx: int = 0):
    game_object = objects[obj_cls][idx]
    if game_object is None:
        new_game_object = obj_cls()
        new_game_object.__setattr__(attr, value)
        objects[obj_cls][idx] = new_game_object
    else:
        game_object.__setattr__(attr, value)


def _remove_object(obj_cls: Type[GameObject], idx: int = 0):
    objects[obj_cls][idx] = None


def _init_objects_ram(hud=False):
    """(Re)Initialize the objects."""
    objects = [Player(), Lives(), OxygenBar()]

    if hud:
        objects.extend([PlayerScore(), OxygenBarDepleted(), OxygenBarLogo()])

    return objects


def _detect_objects_ram(objects_old, ram_state, hud=False):
    _update_objects(ram_state, hud)
    existing_objects = []
    object_categories = list(objects.values())
    for same_type_objects in object_categories:
        for game_object in same_type_objects:
            if game_object is not None:
                existing_objects.append(game_object)
    del objects_old[:]
    objects_old.extend(existing_objects)


def _update_objects(ram_state, hud=False):
    _update_player(ram_state)
    _update_enemies(ram_state)
    _update_player_missile(ram_state)
    _update_divers_and_enemy_missiles(ram_state)
    _update_surface_submarine(ram_state)
    _update_lives(ram_state)
    _update_oxygen_bar(ram_state)
    _update_collected_divers(ram_state)

    if hud:
        _update_score(ram_state)
        _update_depleted_oxygen_bar(ram_state)


def _update_player(ram_state):
    xy = ram_state[70], ram_state[97] + 32
    orientation = Orientation.E if ram_state[86] == 0 else Orientation.W
    crashed = ram_state[105] > 0

    _update_object(Player, "xy", xy)
    _update_object(Player, "orientation", orientation)
    _update_object(Player, "crashed", crashed)


def _update_score(ram_state):
    score_value = _convert_number(ram_state[56]) * 10000 + \
                  _convert_number(ram_state[57]) * 100 + \
                  _convert_number(ram_state[58])

    if score_value == 0:
        x = 99
        w = 6

    elif 100 > score_value > 0:
        x = 91
        w = 14

    elif 1000 > score_value >= 100:
        x = 83
        w = 22

    elif 10000 > score_value >= 1000:
        x = 75
        w = 30

    elif 100000 > score_value >= 10000:
        x = 67
        w = 38

    else:  # highest possible score is 999_999
        x = 59
        w = 46

    _update_object(PlayerScore, "value", score_value)
    _update_object(PlayerScore, "xy", (x, 9))
    _update_object(PlayerScore, "wh", (w, 8))


def _update_lives(ram_state):
    num_lives = ram_state[59]
    if num_lives > 0:  # Up to 6 lives possible
        new_wh = 7 + 8 * (num_lives - 1), 8
        _update_object(Lives, "wh", new_wh)
        _update_object(Lives, "value", num_lives)
    else:
        _remove_object(Lives)


def _update_oxygen_bar(ram_state):
    if ram_state[102] != 0:
        if ram_state[102] == 64:
            new_wh = 63, 5
        else:
            new_wh = ram_state[102], 5
        _update_object(OxygenBar, "wh", new_wh)
        _update_object(OxygenBar, "value", new_wh[0])
    else:
        _remove_object(OxygenBar)


def _update_depleted_oxygen_bar(ram_state):
    if ram_state[102] != 64:
        new_xy = 49 + ram_state[102], 170
        new_wh = 63 - ram_state[102], 5
        _update_object(OxygenBarDepleted, "xy", new_xy)
        _update_object(OxygenBarDepleted, "wh", new_wh)
        _update_object(OxygenBarDepleted, "value", new_wh[0])
    else:
        _remove_object(OxygenBarDepleted)


def _update_collected_divers(ram_state):
    # If you have six collected divers they blink. Blinking is ignored here
    for i in range(6):
        if i < ram_state[62]:
            _update_object(CollectedDiver, "xy", (58 + i * 8, 178), idx=i)
        else:
            _remove_object(CollectedDiver, idx=i)


def _update_enemies(ram_state):
    """The diving area is divided into 4 lanes (plus the surface lane).
    Enemies come in batches. Each batch has three slots that can be
    arbitrarily filled up by enemies. Consequently, there are 8 possible
    combinations (formations) of enemy/empty slots for each batch. For each lane,
    one single RAM value determines the current formation. Moreover, each
    batch consists purely of sharks or of submarines, determined by another value."""

    for i in range(4):  # for each of the 4 lanes (from bottom to top lane)
        present_enemy_type = Submarine if _is_submarine(i, ram_state) else Shark
        hidden_enemy_type = Shark if _is_submarine(i, ram_state) else Submarine
        batch_formation = ram_state[36 + i]

        for j in range(3):  # for each of the three slots (left to right)
            enemy_in_slot = (batch_formation // 2 ** (2 - j)) % 2
            idx = i * 3 + j
            if enemy_in_slot:
                x = (ram_state[30 + i] + 16 * j) % 256
                y = 141 - i * 24
                if present_enemy_type == Shark:
                    # Sharks float up and down, determined by an offset
                    y += ram_state[93] - 4
                if -5 <= x <= 165:  # Only track objects that are on the screen
                    _update_object(present_enemy_type, "xy", (x, y), idx=idx)
                else:
                    _remove_object(present_enemy_type, idx)
            else:
                _remove_object(present_enemy_type, idx)
            _remove_object(hidden_enemy_type, idx)  # always remove the invisible enemy


def _update_divers_and_enemy_missiles(ram_state):
    # divers and enemy_missiles share a ram position
    for i in range(4):
        if 0 < ram_state[71 + i] < 160:
            if _is_submarine(i, ram_state):  # then, it's an enemy missile
                _update_object(EnemyMissile, "xy", (ram_state[71 + i] + 3, 145 - i * 24), idx=i)
                _remove_object(Diver, i)
            else:
                _update_object(Diver, "xy", (ram_state[71 + i], 141 - i * 24), idx=i)
                _remove_object(EnemyMissile, i)
        else:
            _remove_object(EnemyMissile, i)
            _remove_object(Diver, i)


def _update_surface_submarine(ram_state):
    # only spawns in late game
    if ram_state[60] >= 2 and ram_state[118] < 160:
        _update_object(SurfaceSubmarine, "xy", (ram_state[118], 45))
    else:
        _remove_object(SurfaceSubmarine)


def _update_player_missile(ram_state):
    if 0 < ram_state[103] < 160:
        new_xy = ram_state[103], ram_state[97] + 40
        _update_object(PlayerMissile, "xy", new_xy)
    else:
        _remove_object(PlayerMissile)


def _is_submarine(i: int, ram_state) -> bool:
    """True if object with index i is an enemy submarine, else False (i.e., an enemy shark)."""
    return 3 < ram_state[89 + i] % 8 < 7


def _detect_objects_seaquest_raw(info, ram_state):
    """
    The game SEAQUEST displays the enemies and divers at specific lanes, where they move from the right side to the left
    or from the left side to the right. Thus there y-Position is fixed.
    Illustration:

    x=0                             x=158
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ (Surface, Lane 5)

    -------------------------------- (Lane 4)

    -------------------------------- (Lane 3)

    -------------------------------- (Lane 2)

    -------------------------------- (Lane 1)

    _________________________________ (Underground)

    """
    player = [ram_state[70], ram_state[97]]
    offset = ram_state[1]
    divers_missile_x = ram_state[71:75]  # 71 for first lane, 72 second lane, ...   divers and enemy missiles x position
    enemy_x = ram_state[30:34]
    enemy5_x = [ram_state[118]]  # lane 5 enemy only moves if top_enemy_enabled is 2 or higher
    oxygen = [ram_state[102]]
    player_missiles_x = [ram_state[103]]
    relevant_objects = player + divers_missile_x.tolist() + enemy_x.tolist() + enemy5_x + oxygen + player_missiles_x
    info["relevant_objects"] = relevant_objects
    enemy_colors = ram_state[44:48]
    # additional info
    info["lives"] = ram_state[59]  # correct until 6 lives
    info["level"] = ram_state[61]  # changes enemies, speed, ... the higher the value the harder the game currently is
    info["score"] = (_convert_number(ram_state[57]) * 100) + _convert_number(ram_state[58])  # the game saves these
    # numbers in 4 bit intervals (hexadecimal) but only displays the decimal numbers
    info["divers_collected"] = ram_state[62]
    info["lane_y_position"] = {"first lane (lowest)": 100,
                               "second lane": 75,
                               "third lane": 50,
                               "fourth lane": 25,
                               "water surface": 13
                               }  # the lanes actual y-positions are not saved within the RAM, therefore these
    # are educated guesses
    info["player_direction"] = ram_state[86]  # 0: player faces to the right and 8: player faces to the left
    info["top_enemy_enabled"] = ram_state[60]  # enables the top ship if higher/equal than 2
    info["enemy_variations"] = {"first lane (lowest)": ram_state[36] % 8,
                                "second lane": ram_state[37] % 8,
                                "third lane": ram_state[38] % 8,
                                "fourth lane": ram_state[39] % 8}
    # 0: no enemy; 1: only right enemy displayed; 2: only middle enemy ; 3: right and middle enemy;
    # 4: only left enemy; 5: right and left enemy ; 6: middle and left enemy; 7: left, middle, right enemy;
    # 8: same as 0; 9: same as 1 -> modulo 8
    info["is_enemy_submarine_and_diver_enemyMissile"] = ram_state[89:93]
    info["enemy_directions"] = ram_state[89:93]
