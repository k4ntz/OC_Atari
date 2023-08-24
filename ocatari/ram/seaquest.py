import sys

from ._helper_methods import _convert_number
from .game_objects import GameObject

"""
RAM extraction for the game SEAQUEST. Supported modes: raw, revised.
"""

# submarine and missile increased manually, during training more observed than via max_object script
MAX_NB_OBJECTS = {'Player': 1, 'Diver': 4, 'PlayerMissile': 1, 'Enemy': 4, 'EnemySubmarine': 4, 'EnemyMissile': 4}
MAX_NB_OBJECTS_HUD = {'Player': 1, 'PlayerScore': 1, 'Lives': 1, 'OxygenBar': 1, 'OxygenBarDepleted': 1,
                      'OxygenBarLogo': 1, 'Diver': 4, 'PlayerMissile': 1, 'Enemy': 4, 'CollectedDiver': 6,
                      'EnemySubmarine': 4, 'EnemyMissile': 4}


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
        self.orientation = 0  # O is right, 8 is left
        self.exists = True


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
        self.exists = False


class Enemy(GameObject):
    """
    The killer sharks.
    """

    def __init__(self):
        super().__init__()
        self._xy = 0, 0
        self.wh = 8, 7
        self.rgb = 92, 186, 92
        self.hud = False
        self.exists = False


class EnemySubmarine(GameObject):
    """
    The enemy submarines.
    """

    def __init__(self):
        super().__init__()
        self._xy = 0, 0
        self.wh = 8, 11
        self.rgb = 170, 170, 170
        self.hud = False
        self.exists = False


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
        self.exists = False


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
        self.exists = False


class PlayerScore(GameObject):
    """
    The player's score display (HUD).
    """

    def __init__(self):
        super().__init__()
        self._xy = 99, 9
        self.rgb = 210, 210, 64
        self.wh = 6, 8
        self.hud = True
        self.exists = True

    def __eq__(self, o):
        return isinstance(o, PlayerScore) and self.xy == o.xy


class Lives(GameObject):
    """
    The indidcator for remaining reserve subs (lives) (HUD).
    """

    def __init__(self):
        super().__init__()
        self._xy = 58, 22
        self.rgb = 210, 210, 64
        self.wh = 23, 8
        self.hud = True
        self.exists = True


class OxygenBar(GameObject):
    """
    The oxygen gauge (HUD).
    """

    def __init__(self):
        super().__init__()
        self._xy = 49, 170
        self.rgb = 214, 214, 214
        self.wh = 63, 5
        self.hud = True
        self.exists = True


class OxygenBarDepleted(GameObject):
    """
    The empty oxygen bar (HUD).
    """

    def __init__(self):
        super().__init__()
        self._xy = 49, 170
        self.rgb = 163, 57, 21
        self.wh = 63, 5
        self.hud = True
        self.exists = True


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
        self.exists = True


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
        self.exists = False


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


def _init_all_objects() -> dict[str, list[GameObject]]:
    mod = sys.modules[__name__]
    all_objects = {}
    for obj_cls_name, max_obj_count in MAX_NB_OBJECTS_HUD.items():
        same_type_objects = [getattr(mod, obj_cls_name)() for _ in range(max_obj_count)]
        all_objects[obj_cls_name] = same_type_objects
    return all_objects


objects = _init_all_objects()


def _init_objects_seaquest_ram(hud=False):
    """
    (Re)Initialize the objects
    """
    objects = [Player()]

    if hud:
        objects.extend([PlayerScore(), Lives(), OxygenBar(), OxygenBarDepleted(), OxygenBarLogo()])

    return objects


def _detect_objects_seaquest_revised(objects_old, ram_state, hud=False):
    _update_objects(ram_state, hud)
    existing_objects = []
    object_categories = list(objects.values())
    for same_type_objects in object_categories:
        for game_object in same_type_objects:
            if game_object.exists:
                existing_objects.append(game_object)
    del objects_old[:]
    objects_old.extend(existing_objects)


def _update_objects(ram_state, hud=False):
    _update_player(ram_state)
    _update_enemies(ram_state)
    _update_player_missile(ram_state)
    _update_divers_and_enemy_missiles(ram_state)
    _update_fifth_lane_enemy(ram_state)

    if hud:
        _update_score(ram_state)
        _update_lives(ram_state)
        _update_oxygen_bar(ram_state)
        _update_depleted_oxygen_bar(ram_state)
        _update_collected_divers(ram_state)


def _update_player(ram_state):
    player = objects["Player"][0]
    player.xy = ram_state[70], ram_state[97] + 32
    player.orientation = ram_state[86]


def _update_score(ram_state):
    score = objects["PlayerScore"][0]
    score_value = (_convert_number(ram_state[57]) * 100) + _convert_number(ram_state[58])

    if 100 > score_value > 0:
        score.xy = 91, 9
        score.wh = 14, 8

    elif 1000 > score_value >= 100:
        score.xy = 83, 9
        score.wh = 22, 8

    elif score_value >= 1000:
        score.xy = 75, 9
        score.wh = 30, 8


def _update_lives(ram_state):
    lives = objects["Lives"][0]
    if ram_state[59] != 0:
        lives.exist = True
        lives.wh = 7 + 8 * (ram_state[59] - 1), 8
    else:
        lives.exist = False


def _update_oxygen_bar(ram_state):
    if ram_state[102] != 0:
        oxygen = objects["OxygenBar"][0]
        if ram_state[102] == 64:
            oxygen.wh = 63, 5
        else:
            oxygen.wh = ram_state[102], 5


def _update_depleted_oxygen_bar(ram_state):
    if ram_state[102] != 64:
        oxygen_dpl = objects["OxygenBarDepleted"][0]
        oxygen_dpl.xy = 49 + ram_state[102], 170
        oxygen_dpl.wh = 63 - ram_state[102], 5


def _update_collected_divers(ram_state):
    # if you have six collected divers they blink but that is not implemented
    for i in range(6):
        collected = objects["CollectedDiver"][i]
        if i < ram_state[62]:
            collected.xy = 58 + i * 8, 178
            collected.exists = True
        else:
            collected.exists = False


def _update_enemies(ram_state):
    offset = ram_state[93] - 4

    for i in range(4):  # for each of the 4 lanes
        submarine = objects["EnemySubmarine"][i]
        submarine.exists = False
        enemy = objects["Enemy"][i]
        enemy.exists = False

        # left enemy appears at variations 4, 5, 6, 7
        if ram_state[36 + i] >= 4 and ram_state[30 + i] < 160:
            if _is_submarine(i, ram_state):
                submarine.exists = True
                submarine.xy = ram_state[30 + i], 141 - i * 24
            else:
                enemy.exists = True
                enemy.xy = ram_state[30 + i], 141 - i * 24 + offset

        # right enemy appears at variations 1, 3, 5, 7;
        # offset of 32 in x-position because the ram only saves the x-position of the left enemy
        if ram_state[36 + i] % 2 == 1 and (ram_state[30 + i] + 32) % 256 < 160:
            if _is_submarine(i, ram_state):
                submarine.exists = True
                submarine.xy = (ram_state[30 + i] + 32) % 256, 141 - i * 24
            else:
                enemy.exists = True
                enemy.xy = (ram_state[30 + i] + 32) % 256, 141 - i * 24 + offset

        # middle enemy appears at variations 2, 3, 6, 7
        # offset of 16 in x-position because the ram only saves the x-position of the left enemy
        if (ram_state[36 + i] == 2 or ram_state[36 + i] == 3 or ram_state[36 + i] == 6 or
                ram_state[36 + i] == 7) and (ram_state[30 + i] + 16) % 256 < 160:
            if _is_submarine(i, ram_state):
                submarine.exists = True
                submarine.xy = (ram_state[30 + i] + 16) % 256, 141 - i * 24
            else:
                enemy.exists = True
                enemy.xy = (ram_state[30 + i] + 16) % 256, 141 - i * 24 + offset


def _update_divers_and_enemy_missiles(ram_state):
    # divers and enemy_missiles share a ram position
    missiles = objects["EnemyMissile"]
    divers = objects["Diver"]
    for i in range(4):
        if 0 < ram_state[71 + i] < 160:
            if _is_submarine(i, ram_state):  # then, it's an enemy missile
                missiles[i].exists = True
                missiles[i].xy = ram_state[71 + i] + 3, 145 - i * 24
            else:
                divers[i].exists = True
                divers[i].xy = ram_state[71 + i], 141 - i * 24
        else:
            missiles[i].exists = False
            divers[i].exists = False


def _update_fifth_lane_enemy(ram_state):
    # only spawns in higher levels
    enemy_sub = objects["EnemySubmarine"][-1]
    if ram_state[60] >= 2 and ram_state[118] < 160:
        enemy_sub.exists = True
        enemy_sub.xy = ram_state[118], 45
    else:
        enemy_sub.exists = False


def _is_submarine(i: int, ram_state) -> bool:
    """True if object with index i is an enemy submarine, else False (i.e., an enemy shark)."""
    return 3 < ram_state[89 + i] % 8 < 7


def _update_player_missile(ram_state):
    missile = objects["PlayerMissile"][0]
    if 0 < ram_state[103] < 160:
        missile.exists = True
        missile.xy = ram_state[103], ram_state[97] + 40
    else:
        missile.exists = False
        player = objects["Player"][0]
        missile.xy = player.xy  # assume the missile to be at the player's position


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
