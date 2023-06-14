from ._helper_methods import _convert_number
from .game_objects import GameObject
import sys

"""
RAM extraction for the game SEAQUEST. Supported modes: raw, revised.
"""

# submarine and missile increased manually, during training more observed than via max_object script
MAX_NB_OBJECTS =  {'Player': 1, 'Diver': 4, 'PlayerMissile': 1, 'Enemy': 4, 'EnemySubmarine': 4, 'EnemyMissile': 3}
MAX_NB_OBJECTS_HUD =  {'Player': 1, 'PlayerScore': 1, 'Lives': 1, 'OxygenBar': 1, 'OxygenBarDepleted': 1, 'OxygenBarLogo': 1, 'Diver': 4, 'PlayerMissile': 1, 'Enemy': 4, 'CollectedDiver': 3, 'EnemySubmarine': 3, 'EnemyMissile': 3}


class Player(GameObject):
    def __init__(self):
        super().__init__()
        self._xy = 76, 46
        self.wh = 16, 11
        self.rgb = 187, 187, 53
        self.hud = False


class Diver(GameObject):
    def __init__(self):
        super().__init__()
        self._xy = 0, 0
        self.wh = 8, 11
        self.rgb = 66, 72, 200
        self.hud = False


class Enemy(GameObject):
    def __init__(self):
        super().__init__()
        self._xy = 0, 0
        self.wh = 8, 7
        self.rgb = 1, 1, 1
        self.hud = False


class EnemySubmarine(GameObject):
    def __init__(self):
        self._xy = 0, 0
        self.wh = 8, 11
        self.rgb = 170, 170, 170
        self.hud = False


class EnemyMissile(GameObject):
    def __init__(self):
        self._xy = 0, 0
        self.wh = 6, 4
        self.rgb = 66, 72, 200
        self.hud = False


class PlayerMissile(GameObject):
    def __init__(self):
        super().__init__()
        self._xy = 0, 0
        self.wh = 8, 1
        self.rgb = 187, 187, 53
        self.hud = False


class PlayerScore(GameObject):
    def __init__(self):
        super().__init__()
        self._xy = 99, 9
        self.rgb = 210, 210, 64
        self.wh = 6, 8
        self.hud = True

    def __eq__(self, o):
        return isinstance(o, PlayerScore) and self.xy == o.xy


class Lives(GameObject):
    def __init__(self):
        super().__init__()
        self._xy = 58, 22
        self.rgb = 210, 210, 64
        self.wh = 23, 8
        self.hud = True


class OxygenBar(GameObject):
    def __init__(self):
        super().__init__()
        self._xy = 49, 170
        self.rgb = 214, 214, 214
        self.wh = 63, 5
        self.hud = True


class OxygenBarDepleted(GameObject):
    def __init__(self):
        super().__init__()
        self._xy = 49, 170
        self.rgb = 163, 57, 21
        self.wh = 63, 5
        self.hud = True


class OxygenBarLogo(GameObject):
    def __init__(self):
        super().__init__()
        self._xy = 15, 170
        self.rgb = 0, 0, 0
        self.wh = 23, 5
        self.hud = True


class CollectedDiver(GameObject):
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
        return fromdict(MAX_NB_OBJECTS_HUD)
    return fromdict(MAX_NB_OBJECTS)

def _init_objects_seaquest_ram(hud=False):
    """
    (Re)Initialize the objects
    """
    objects = [Player()]

    if hud:
        objects.extend([PlayerScore(), Lives(), OxygenBar(), OxygenBarDepleted(), OxygenBarLogo()])

    return objects


def _detect_objects_seaquest_revised(objects, ram_state, hud=False):
    player = objects[0]
    player.xy = ram_state[70], ram_state[97] + 32
    if hud:
        score = objects[1]

    if hud:
        del objects[2:]
    else:
        del objects[1:]
    objs = _calculate_objects(ram_state)
    objects.extend(objs)

    if hud:
        # score
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

        # lives
        if ram_state[59] != 0:
            lives = Lives()
            lives.wh = 7 + 8 * (ram_state[59] - 1), 8
            objects.append(lives)

        # oxygen bar
        if ram_state[102] != 0:
            oxygen = OxygenBar()
            if ram_state[102] == 64:
                oxygen.wh = 63, 5
            else:
                oxygen.wh = ram_state[102], 5
            objects.append(oxygen)

        # depleted oxygen bar
        if ram_state[102] != 64:
            oxygen_dpl = OxygenBarDepleted()
            oxygen_dpl.xy = 49 + ram_state[102], 170
            oxygen_dpl.wh = 63 - ram_state[102], 5
            objects.append(oxygen_dpl)

        # collected divers, if you have six collected divers they blink but that is not implemented
        for i in range(ram_state[62]):
            collected = CollectedDiver()
            collected.xy = 58 + i * 8, 178
            objects.append(collected)

        # oxygen bar logo
        logo_bar = OxygenBarLogo()
        objects.append(logo_bar)


def _calculate_objects(ram_state):
    """
    Calculate the current enemies, divers and missiles that are on the screen.
    """
    enemies = []
    divers_or_enemy_missiles = []
    missiles = []
    is_submarine = []

    for i in range(4):
        if 3 < ram_state[89 + i] % 8 < 7:
            is_submarine.append(True)
        else:
            is_submarine.append(False)

    # left enemy appears at variations 4, 5, 6, 7
    for i in range(4):  # for the 4 lanes, check if the left enemy appears
        if ram_state[36 + i] >= 4 and ram_state[30 + i] < 160:
            if is_submarine[i]:
                submarine = EnemySubmarine()
                submarine.xy = ram_state[30 + i], 141 - i * 24
                enemies.append(submarine)
            else:
                enemy = Enemy()
                enemy.xy = ram_state[30 + i], 141 - i * 24
                enemies.append(enemy)

    # right enemy appears at variations 1, 3, 5, 7;
    # offset of 32 in x-position because the ram only saves the x-position of the left enemy
    for i in range(4):
        if ram_state[36 + i] % 2 == 1 and (ram_state[30 + i] + 32) % 256 < 160:
            if is_submarine[i]:
                submarine = EnemySubmarine()
                submarine.xy = (ram_state[30 + i] + 32) % 256, 141 - i * 24
                enemies.append(submarine)
            else:
                enemy = Enemy()
                enemy.xy = (ram_state[30 + i] + 32) % 256, 141 - i * 24
                enemies.append(enemy)

    # middle enemy appears at variations 2, 3, 6, 7
    # offset of 16 in x-position because the ram only saves the x-position of the left enemy
    for i in range(4):
        if (ram_state[36 + i] == 2 or ram_state[36 + i] == 3 or ram_state[36 + i] == 6 or ram_state[36 + i] == 7) \
                and (ram_state[30] + 16) % 256 < 160:
            if is_submarine[i]:
                submarine = EnemySubmarine()
                submarine.xy = (ram_state[30 + i] + 16) % 256, 141 - i * 24
                enemies.append(submarine)
            else:
                enemy = Enemy()
                enemy.xy = (ram_state[30 + i] + 16) % 256, 141 - i * 24
                enemies.append(enemy)

    # fifth lane enemy, only spawns in higher levels
    if ram_state[60] >= 2 and ram_state[118] < 160:
        submarine = EnemySubmarine()
        submarine.xy = ram_state[118], 45
        enemies.append(submarine)

    # divers and enemy_missiles share a ram position
    for i in range(4):
        if 0 < ram_state[71 + i] < 160:
            if is_submarine[i]:     # then its an enemy missile
                missile = EnemyMissile()
                missile.xy = ram_state[71 + i] + 3, 145 - i * 24
                divers_or_enemy_missiles.append(missile)
            else:
                diver = Diver()
                diver.xy = ram_state[71 + i], 141 - i * 24
                divers_or_enemy_missiles.append(diver)

    # player missile
    if 0 < ram_state[103] < 160:
        missile = PlayerMissile()
        missile.xy = ram_state[103], ram_state[97] + 40
        missiles.append(missile)

    return enemies + divers_or_enemy_missiles + missiles


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
    divers_missile_x = ram_state[71:75]  # 71 for first lane, 72 second lane, ...   divers and enemy missiles x position
    enemy_x = ram_state[30:34]
    enemy5_x = [ram_state[118]]  # lane 5 enemy only moves if top_enemy_enabled is 2 or higher
    oxygen = [ram_state[102]]
    player_missiles_x = [ram_state[103]]
    relevant_objects = player + divers_missile_x.tolist() + enemy_x.tolist() + enemy5_x + oxygen + player_missiles_x
    info["relevant_objects"] = relevant_objects

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
