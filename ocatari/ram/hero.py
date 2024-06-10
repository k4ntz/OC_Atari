from enum import Enum

import numpy as np

from .game_objects import GameObject

"""
RAM extraction for the game H.E.R.O.
"""

MAX_NB_OBJECTS = {"Wall": 15, "LavaWall": 15, "Enemy": 10, "Player": 1, "LaserBeam": 3, "Bomb": 5, "EndNPC": 1,
                  "Lamp": 1, "Snake": 5, }
MAX_NB_OBJECTS_HUD = {"Wall": 15, "LavaWall": 15, "Enemy": 10, "Player": 1, "LaserBeam": 3, "Bomb": 5, "EndNPC": 1,
                      "Lamp": 1, "Snake": 5, "PowerBar": 1, "BombStock": 1, "Life": 1, "Score": 1}


# changing ram 54 activate some kind of bot that plays alone
class Wall(GameObject):
    """
    The walls in the mineshafts.
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.xy = 0, 0
        self.wh = 8, 10
        self.destructible: bool = False


class LavaWall(GameObject):
    """
    The lava walls in the mineshafts.
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.xy = 0, 0
        self.wh = 8, 10


class Platform(GameObject):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.xy = 0, 136
        self.wh = 9, 3


class EnemyType(Enum):
    Spider = 1
    Bat = 2
    Moth = 3
    Snake = 4
    Tentacle = 5


class Enemy(GameObject):
    """
    The dangerous creatures inside the mineshafts.
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.xy = 0, 0
        self.wh = 7, 10
        self.type: EnemyType


class Player(GameObject):
    """
    The player figure.
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.xy = 0, 0
        self.wh = 6, 25
        self.rgb = [84, 138, 210]


class LaserBeam(GameObject):
    """
    The laser beams shot from the helmet of the player figure.
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.xy = 0, 0
        self.wh = 7, 2
        self.rgb = [200, 72, 72]


class Bomb(GameObject):
    """
    The dynamite sticks that can be deployed by the player.
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.xy = 0, 0
        self.wh = 3, 11
        self.rgb = [184, 50, 50]


class EndNPC(GameObject):
    """
    The trapped miners to be rescued.
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.xy = 0, 85
        self.wh = 8, 13


class Lamp(GameObject):
    """
    The lanterns that light the mineshafts.
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.xy = 0, 35
        self.wh = 7, 8


class PowerBar(GameObject):
    """
    The power gauge (HUD).
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.xy = 49, 145
        self.wh = 79, 5
        self.value = 1


class BombStock(GameObject):
    """
    The indicator for remaining dynamite sticks (HUD).
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.xy = 58, 165
        self.wh = 43, 12
        self.value = 5


class Life(GameObject):
    """
    The indicator for the player's remaining lives (HUD).
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.xy = 58, 152
        self.wh = 43, 13
        self.value = 4


class Score(GameObject):
    """
    The player's score display (HUD).
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.xy = 58, 178
        self.wh = 43, 8
        self.value = 0


def _get_max_objects(hud=False):
    return


def _init_objects_ram(hud=False):
    objects = [Player()]
    if hud:
        objects.extend([PowerBar(), BombStock(), Life(), Score(), ])
    return objects


number_of_added_enemies = 0
objects_map = {}


def _detect_objects_ram(objects, ram_state, hud=False):
    objects[0].xy = ram_state[27] + 1, 135 - ram_state[31]
    base_length = 1 if not hud else 5
    global objects_map

    # Updating enemy and lamp positions
    # TODO get enemy type
    for i in range(3):
        # height =
        # type =
        # subtype = ram_state[78 + i]
        x, y = ram_state[37 + i], 115 - i * 42 - ram_state[33 + i]

        currobj = objects_map.get(f"Instance {i}")
        if ram_state[33 + i] == 50 or x == 147:
            if currobj is not None:
                objects_map.pop(f"Instance {i}")
        else:
            if i != 0 or ((x < 146) and not ((
                    x in [64, 68, 75, 76, 77] and (ram_state[117], ram_state[28]) not in [(1, 2), (2, 1), (3, 6),
                                                                                          (5, 2),
                                                                                          (6, 7), (6, 10), (7, 1),
                                                                                          (7, 2),
                                                                                          (7, 13), (8, 10), (8, 11),
                                                                                          (8, 13),
                                                                                          (9, 7), (9, 8), (9, 9),
                                                                                          (9, 11),
                                                                                          (9, 12), ]))):
                if currobj is not None:
                    if i == 2 and (ram_state[117], ram_state[28]) in [(2, 1), (2, 3), (3, 1), (3, 2), (3, 3), (3, 4),
                                                                      (3, 5), (3, 6),
                                                                      (4, 1), (4, 3), (4, 4), (4, 5), (4, 6), (5, 1),
                                                                      (5, 2), (5, 3),
                                                                      (5, 4), (5, 5), (5, 6), (5, 7), (5, 8), (6, 1),
                                                                      (6, 2), (6, 3),
                                                                      (6, 4), (6, 5), (6, 6), (6, 7), (6, 8), (6, 9),
                                                                      (6, 10), (7, 1),
                                                                      (7, 2), (7, 3), (7, 4), (7, 5), (7, 6), (7, 7),
                                                                      (7, 8), (7, 9),
                                                                      (7, 10), (8, 1), (8, 2), (8, 3), (8, 4), (8, 5),
                                                                      (8, 6), (8, 7),
                                                                      (8, 8), (8, 9), (8, 10), (9, 1), (9, 2), (9, 3),
                                                                      (9, 4), (9, 5),
                                                                      (9, 6), (9, 7), (9, 8), (9, 9), (9, 10), (10, 1),
                                                                      (10, 2),
                                                                      (10, 3), (10, 4), (10, 5), (10, 6), (10, 7),
                                                                      (10, 8), (10, 9),
                                                                      (10, 10), (11, 1), (11, 2), (11, 4), (11, 5),
                                                                      (11, 6), (11, 7),
                                                                      (11, 9), (11, 10), (12, 1), (12, 2), (12, 3),
                                                                      (12, 4), (12, 5),
                                                                      (12, 6), (12, 8), (12, 9), (13, 1), (13, 3),
                                                                      (13, 5), (13, 6),
                                                                      (13, 7), (13, 10), (14, 1), (14, 2), (14, 3),
                                                                      (14, 4), (14, 5),
                                                                      (14, 6), (14, 7), (14, 8), (14, 9), (14, 10),
                                                                      (15, 1), (15, 3),
                                                                      (15, 4), (15, 5), (15, 6), (15, 7), (15, 8),
                                                                      (15, 9), (15, 10),
                                                                      (16, 1), (16, 2), (16, 3), (16, 4), (16, 5),
                                                                      (16, 6), (16, 7),
                                                                      (16, 9), (16, 10), (17, 1), (17, 2), (17, 3),
                                                                      (17, 4), (17, 5),
                                                                      (17, 7), (17, 8), (17, 9), (17, 10), (18, 1),
                                                                      (18, 2), (18, 3),
                                                                      (18, 4), (18, 5), (18, 6), (18, 7), (18, 8),
                                                                      (18, 9), (18, 10),
                                                                      (19, 1), (19, 2), (19, 3), (19, 4), (19, 5),
                                                                      (19, 6), (19, 7),
                                                                      (19, 8), (19, 10)]:
                        enemy_instance = Lamp()
                        enemy_instance.xy = x, enemy_instance.y
                        objects_map[f"Instance {i}"] = enemy_instance
                    else:
                        currobj.xy = x, y
                else:
                    if i == 2 and (ram_state[117], ram_state[28]) in [(2, 1), (2, 3), (3, 1), (3, 2), (3, 3), (3, 4),
                                                                      (3, 5), (3, 6),
                                                                      (4, 1), (4, 3), (4, 4), (4, 5), (4, 6), (5, 1),
                                                                      (5, 2), (5, 3),
                                                                      (5, 4), (5, 5), (5, 6), (5, 7), (5, 8), (6, 1),
                                                                      (6, 2), (6, 3),
                                                                      (6, 4), (6, 5), (6, 6), (6, 7), (6, 8), (6, 9),
                                                                      (6, 10), (7, 1),
                                                                      (7, 2), (7, 3), (7, 4), (7, 5), (7, 6), (7, 7),
                                                                      (7, 8), (7, 9),
                                                                      (7, 10), (8, 1), (8, 2), (8, 3), (8, 4), (8, 5),
                                                                      (8, 6), (8, 7),
                                                                      (8, 8), (8, 9), (8, 10), (9, 1), (9, 2), (9, 3),
                                                                      (9, 4), (9, 5),
                                                                      (9, 6), (9, 7), (9, 8), (9, 9), (9, 10), (10, 1),
                                                                      (10, 2),
                                                                      (10, 3), (10, 4), (10, 5), (10, 6), (10, 7),
                                                                      (10, 8), (10, 9),
                                                                      (10, 10), (11, 1), (11, 2), (11, 4), (11, 5),
                                                                      (11, 6), (11, 7),
                                                                      (11, 9), (11, 10), (12, 1), (12, 2), (12, 3),
                                                                      (12, 4), (12, 5),
                                                                      (12, 6), (12, 8), (12, 9), (13, 1), (13, 3),
                                                                      (13, 5), (13, 6),
                                                                      (13, 7), (13, 10), (14, 1), (14, 2), (14, 3),
                                                                      (14, 4), (14, 5),
                                                                      (14, 6), (14, 7), (14, 8), (14, 9), (14, 10),
                                                                      (15, 1), (15, 3),
                                                                      (15, 4), (15, 5), (15, 6), (15, 7), (15, 8),
                                                                      (15, 9), (15, 10),
                                                                      (16, 1), (16, 2), (16, 3), (16, 4), (16, 5),
                                                                      (16, 6), (16, 7),
                                                                      (16, 9), (16, 10), (17, 1), (17, 2), (17, 3),
                                                                      (17, 4), (17, 5),
                                                                      (17, 7), (17, 8), (17, 9), (17, 10), (18, 1),
                                                                      (18, 2), (18, 3),
                                                                      (18, 4), (18, 5), (18, 6), (18, 7), (18, 8),
                                                                      (18, 9), (18, 10),
                                                                      (19, 1), (19, 2), (19, 3), (19, 4), (19, 5),
                                                                      (19, 6), (19, 7),
                                                                      (19, 8), (19, 10)]:
                        enemy_instance = Lamp()
                        enemy_instance.xy = x, enemy_instance.y
                    else:
                        enemy_instance = Enemy()
                        enemy_instance.xy = x, y
                    objects_map[f"Instance {i}"] = enemy_instance

    # updating Laser Beam position
    player_xy = objects[0].xy
    laser_beam = objects_map.get(f"LaserBeam")
    if ram_state[115] == 253:
        if laser_beam is not None:
            objects_map.pop(f"LaserBeam")
    else:
        orientation = 1 if ram_state[48] == 0 else -1
        if laser_beam is None:
            laser_beam_instance = LaserBeam()
            objects_map[f"LaserBeam"] = laser_beam_instance
        laser_beam = objects_map[f"LaserBeam"]
        if ram_state[115] != 0:
            if orientation == 1:
                laser_beam.xy = player_xy[0] + 2 + ram_state[115] * orientation, player_xy[1] + 3
            else:
                laser_beam.xy = player_xy[0] + 4 + ram_state[115] * orientation - laser_beam.w, \
                                player_xy[1] + 3
        else:
            if orientation == 1:
                laser_beam.xy = player_xy[0] + 2 + 11 * orientation, player_xy[1] + 3
            else:
                laser_beam.xy = player_xy[0] + 4 + 11 * orientation, player_xy[1] + 3

    # destructible wall
    destructible_wall = objects_map.get(f"destructible wall")
    if ram_state[32] in [0, 9, 153]:
        if destructible_wall is not None:
            objects_map.pop(f"destructible wall")
    else:
        if destructible_wall is not None:
            destructible_wall.xy = ram_state[32], 19
        else:
            destructible_wall_instance = Wall()
            destructible_wall_instance.xy = ram_state[32], 19
            destructible_wall_instance.wh = 8, 79
            destructible_wall_instance.destructible = True
            objects_map[f"destructible wall"] = destructible_wall_instance

    objects_map = add_walls_to_object_list(ram_state, objects_map)
    # Bomb / NPC position
    # NPC --> ram_state[41]
    number_of_configuration_per_level = [2, 4, 6, 8, 8, 10, 12, 14, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16]
    if ram_state[41] != 147:
        if ram_state[28] == number_of_configuration_per_level[ram_state[117]] - 1:
            if objects_map.get("EndNPC") == None:
                objects_map["EndNPC"] = EndNPC()
                objects_map["EndNPC"].xy = ram_state[41], objects_map["EndNPC"].y
                if objects_map.get("bomb") != None:
                    objects_map.pop("bomb")
        else:
            if objects_map.get("bomb") == None:
                objects_map["bomb"] = Bomb()
                objects_map["bomb"].xy = ram_state[41] + 3, objects[0].y + 13
                if objects_map.get("EndNPC") != None:
                    objects_map.pop("EndNPC")
    else:
        if objects_map.get("EndNPC") != None:
            objects_map.pop("EndNPC")
        elif objects_map.get("bomb") != None:
            objects_map.pop("bomb")

    if ram_state[40] != 147:
        if (ram_state[117], ram_state[28]) in [(9, 13), (10, 12), (11, 14), (12, 12), (13, 12), (14, 13), (15, 11),
                                               (15, 13), (16, 14), (17, 12), (18, 12), (19, 11)]:
            if objects_map.get("platform") == None:
                objects_map["platform"] = Platform()
                objects_map["platform"].xy = ram_state[40], 135
            else:
                objects_map["platform"].xy = ram_state[40], 135
            if objects_map.get("tentacle") != None:
                objects_map.pop("tentacle")

        else:
            if objects_map.get("tentacle") == None:
                objects_map["tentacle"] = Enemy()
                objects_map["tentacle"].xy = ram_state[40], 137
                objects_map["tentacle"].wh = 7, 10
            else:
                objects_map["tentacle"].xy = ram_state[40], 137
            if objects_map.get("platform") != None:
                objects_map.pop("platform")
    else:
        if objects_map.get("tentacle") != None:
            objects_map.pop("tentacle")
        elif objects_map.get("platform") != None:
            objects_map.pop("platform")
    # If we're on the final part of the level --> NPC position else bomb position

    if hud:
        objects[1].value = ram_state[43] / 81
        objects[2].value = ram_state[50]
        objects[2].xy = 102 - (objects[2].value) * 7, objects[2].y
        objects[2].wh = (objects[2].value) * 7, objects[2].h
        objects[3].value = ram_state[51]
        objects[3].xy = 102 - (objects[3].value - 1) * 7, objects[3].y
        objects[3].wh = (objects[3].value - 1) * 7, objects[3].h
        #score value is related to ram_state[56], ram_state[55] and ram_state[57] --> TODO: Get relation
        objects[4].value = ram_state[56]
        objects[4].xy = 103 - (int(np.log(max(objects[4].value, 1))) + 1) * 6, objects[4].y
        objects[4].wh = (int(np.log(max(objects[4].value, 1))) + 1) * 6, objects[4].h

    # if we want to not use lava wall detection, because it has some bugs
    # objects[:] = objects[0:base_length]
    # for key in objects_map.keys():
    #     if str(key)[0:4] != "lava" :
    #         objects.append(objects_map[key])

    objects[:] = objects[0:base_length] + list(objects_map.values())


def _detect_objects_hero_raw(info, ram_state):
    return


def add_walls_to_object_list(ram_state, objects_map):
    if ram_state[117] == 0:
        if ram_state[28] == 0:
            number_of_lava_walls = 0
            i = 0
            while (objects_map.get(f"lava wall {number_of_lava_walls + i}") != None):
                objects_map.pop(f"lava wall {number_of_lava_walls + i}")
                i += 1
            wall_instance0 = Wall()
            wall_instance0.xy = (136, 21)
            wall_instance0.wh = (24, 38)
            objects_map['fixed wall 0'] = wall_instance0
            wall_instance1 = Wall()
            wall_instance1.xy = (8, 21)
            wall_instance1.wh = (16, 38)
            objects_map['fixed wall 1'] = wall_instance1
            wall_instance2 = Wall()
            wall_instance2.xy = (144, 61)
            wall_instance2.wh = (16, 37)
            objects_map['fixed wall 2'] = wall_instance2
            wall_instance3 = Wall()
            wall_instance3.xy = (8, 61)
            wall_instance3.wh = (8, 37)
            objects_map['fixed wall 3'] = wall_instance3
            wall_instance4 = Wall()
            wall_instance4.xy = (88, 101)
            wall_instance4.wh = (72, 38)
            objects_map['fixed wall 4'] = wall_instance4
            wall_instance5 = Wall()
            wall_instance5.xy = (8, 101)
            wall_instance5.wh = (64, 38)
            objects_map['fixed wall 5'] = wall_instance5
            number_of_walls = 6
            i = 0
            while (objects_map.get(f"fixed wall {number_of_walls + i}") != None):
                objects_map.pop(f"fixed wall {number_of_walls + i}")
                i += 1
        elif ram_state[28] == 1:
            number_of_lava_walls = 0
            i = 0
            while (objects_map.get(f"lava wall {number_of_lava_walls + i}") != None):
                objects_map.pop(f"lava wall {number_of_lava_walls + i}")
                i += 1
            wall_instance0 = Wall()
            wall_instance0.xy = (88, 21)
            wall_instance0.wh = (72, 38)
            objects_map['fixed wall 0'] = wall_instance0
            wall_instance1 = Wall()
            wall_instance1.xy = (8, 21)
            wall_instance1.wh = (64, 38)
            objects_map['fixed wall 1'] = wall_instance1
            wall_instance2 = Wall()
            wall_instance2.xy = (136, 61)
            wall_instance2.wh = (24, 37)
            objects_map['fixed wall 2'] = wall_instance2
            wall_instance3 = Wall()
            wall_instance3.xy = (8, 61)
            wall_instance3.wh = (16, 37)
            objects_map['fixed wall 3'] = wall_instance3
            wall_instance4 = Wall()
            wall_instance4.xy = (8, 101)
            wall_instance4.wh = (152, 38)
            objects_map['fixed wall 4'] = wall_instance4
            number_of_walls = 5
            i = 0
            while (objects_map.get(f"fixed wall {number_of_walls + i}") != None):
                objects_map.pop(f"fixed wall {number_of_walls + i}")
                i += 1

    elif ram_state[117] == 1:
        if ram_state[28] == 0:
            number_of_lava_walls = 0
            i = 0
            while (objects_map.get(f"lava wall {number_of_lava_walls + i}") != None):
                objects_map.pop(f"lava wall {number_of_lava_walls + i}")
                i += 1
            wall_instance0 = Wall()
            wall_instance0.xy = (136, 21)
            wall_instance0.wh = (24, 38)
            objects_map['fixed wall 0'] = wall_instance0
            wall_instance1 = Wall()
            wall_instance1.xy = (8, 21)
            wall_instance1.wh = (16, 38)
            objects_map['fixed wall 1'] = wall_instance1
            wall_instance2 = Wall()
            wall_instance2.xy = (144, 61)
            wall_instance2.wh = (16, 37)
            objects_map['fixed wall 2'] = wall_instance2
            wall_instance3 = Wall()
            wall_instance3.xy = (8, 61)
            wall_instance3.wh = (8, 37)
            objects_map['fixed wall 3'] = wall_instance3
            wall_instance4 = Wall()
            wall_instance4.xy = (88, 101)
            wall_instance4.wh = (72, 38)
            objects_map['fixed wall 4'] = wall_instance4
            wall_instance5 = Wall()
            wall_instance5.xy = (8, 101)
            wall_instance5.wh = (64, 38)
            objects_map['fixed wall 5'] = wall_instance5
            number_of_walls = 6
            i = 0
            while (objects_map.get(f"fixed wall {number_of_walls + i}") != None):
                objects_map.pop(f"fixed wall {number_of_walls + i}")
                i += 1
        elif ram_state[28] == 1:
            number_of_lava_walls = 0
            i = 0
            while (objects_map.get(f"lava wall {number_of_lava_walls + i}") != None):
                objects_map.pop(f"lava wall {number_of_lava_walls + i}")
                i += 1
            wall_instance0 = Wall()
            wall_instance0.xy = (88, 21)
            wall_instance0.wh = (72, 38)
            objects_map['fixed wall 0'] = wall_instance0
            wall_instance1 = Wall()
            wall_instance1.xy = (8, 21)
            wall_instance1.wh = (64, 38)
            objects_map['fixed wall 1'] = wall_instance1
            wall_instance2 = Wall()
            wall_instance2.xy = (144, 61)
            wall_instance2.wh = (16, 37)
            objects_map['fixed wall 2'] = wall_instance2
            wall_instance3 = Wall()
            wall_instance3.xy = (8, 61)
            wall_instance3.wh = (8, 37)
            objects_map['fixed wall 3'] = wall_instance3
            wall_instance4 = Wall()
            wall_instance4.xy = (120, 101)
            wall_instance4.wh = (40, 38)
            objects_map['fixed wall 4'] = wall_instance4
            wall_instance5 = Wall()
            wall_instance5.xy = (48, 101)
            wall_instance5.wh = (64, 38)
            objects_map['fixed wall 5'] = wall_instance5
            wall_instance6 = Wall()
            wall_instance6.xy = (8, 101)
            wall_instance6.wh = (32, 38)
            objects_map['fixed wall 6'] = wall_instance6
            number_of_walls = 7
            i = 0
            while (objects_map.get(f"fixed wall {number_of_walls + i}") != None):
                objects_map.pop(f"fixed wall {number_of_walls + i}")
                i += 1
        elif ram_state[28] == 2:
            number_of_lava_walls = 0
            i = 0
            while (objects_map.get(f"lava wall {number_of_lava_walls + i}") != None):
                objects_map.pop(f"lava wall {number_of_lava_walls + i}")
                i += 1
            wall_instance0 = Wall()
            wall_instance0.xy = (120, 21)
            wall_instance0.wh = (40, 38)
            objects_map['fixed wall 0'] = wall_instance0
            wall_instance1 = Wall()
            wall_instance1.xy = (48, 21)
            wall_instance1.wh = (64, 38)
            objects_map['fixed wall 1'] = wall_instance1
            wall_instance2 = Wall()
            wall_instance2.xy = (8, 21)
            wall_instance2.wh = (32, 38)
            objects_map['fixed wall 2'] = wall_instance2
            wall_instance3 = Wall()
            wall_instance3.xy = (144, 61)
            wall_instance3.wh = (16, 37)
            objects_map['fixed wall 3'] = wall_instance3
            wall_instance4 = Wall()
            wall_instance4.xy = (64, 61)
            wall_instance4.wh = (44, 37)
            objects_map['fixed wall 4'] = wall_instance4
            wall_instance5 = Wall()
            wall_instance5.xy = (8, 61)
            wall_instance5.wh = (20, 37)
            objects_map['fixed wall 5'] = wall_instance5
            wall_instance6 = Wall()
            wall_instance6.xy = (104, 101)
            wall_instance6.wh = (56, 38)
            objects_map['fixed wall 6'] = wall_instance6
            wall_instance7 = Wall()
            wall_instance7.xy = (8, 101)
            wall_instance7.wh = (48, 38)
            objects_map['fixed wall 7'] = wall_instance7
            number_of_walls = 8
            i = 0
            while (objects_map.get(f"fixed wall {number_of_walls + i}") != None):
                objects_map.pop(f"fixed wall {number_of_walls + i}")
                i += 1
        elif ram_state[28] == 3:
            number_of_lava_walls = 0
            i = 0
            while (objects_map.get(f"lava wall {number_of_lava_walls + i}") != None):
                objects_map.pop(f"lava wall {number_of_lava_walls + i}")
                i += 1
            wall_instance0 = Wall()
            wall_instance0.xy = (8, 21)
            wall_instance0.wh = (152, 38)
            objects_map['fixed wall 0'] = wall_instance0
            wall_instance1 = Wall()
            wall_instance1.xy = (144, 61)
            wall_instance1.wh = (16, 37)
            objects_map['fixed wall 1'] = wall_instance1
            wall_instance2 = Wall()
            wall_instance2.xy = (8, 61)
            wall_instance2.wh = (8, 37)
            objects_map['fixed wall 2'] = wall_instance2
            wall_instance3 = Wall()
            wall_instance3.xy = (88, 101)
            wall_instance3.wh = (72, 38)
            objects_map['fixed wall 3'] = wall_instance3
            wall_instance4 = Wall()
            wall_instance4.xy = (8, 101)
            wall_instance4.wh = (64, 38)
            objects_map['fixed wall 4'] = wall_instance4
            number_of_walls = 5
            i = 0
            while (objects_map.get(f"fixed wall {number_of_walls + i}") != None):
                objects_map.pop(f"fixed wall {number_of_walls + i}")
                i += 1

    elif ram_state[117] == 2:
        if ram_state[28] == 0:
            number_of_lava_walls = 0
            i = 0
            while (objects_map.get(f"lava wall {number_of_lava_walls + i}") != None):
                objects_map.pop(f"lava wall {number_of_lava_walls + i}")
                i += 1
            wall_instance0 = Wall()
            wall_instance0.xy = (136, 21)
            wall_instance0.wh = (24, 38)
            objects_map['fixed wall 0'] = wall_instance0
            wall_instance1 = Wall()
            wall_instance1.xy = (8, 21)
            wall_instance1.wh = (16, 38)
            objects_map['fixed wall 1'] = wall_instance1
            wall_instance2 = Wall()
            wall_instance2.xy = (144, 61)
            wall_instance2.wh = (16, 37)
            objects_map['fixed wall 2'] = wall_instance2
            wall_instance3 = Wall()
            wall_instance3.xy = (8, 61)
            wall_instance3.wh = (8, 37)
            objects_map['fixed wall 3'] = wall_instance3
            wall_instance4 = Wall()
            wall_instance4.xy = (88, 101)
            wall_instance4.wh = (72, 38)
            objects_map['fixed wall 4'] = wall_instance4
            wall_instance5 = Wall()
            wall_instance5.xy = (8, 101)
            wall_instance5.wh = (64, 38)
            objects_map['fixed wall 5'] = wall_instance5
            number_of_walls = 6
            i = 0
            while (objects_map.get(f"fixed wall {number_of_walls + i}") != None):
                objects_map.pop(f"fixed wall {number_of_walls + i}")
                i += 1
        elif ram_state[28] == 1:
            number_of_lava_walls = 0
            i = 0
            while (objects_map.get(f"lava wall {number_of_lava_walls + i}") != None):
                objects_map.pop(f"lava wall {number_of_lava_walls + i}")
                i += 1
            wall_instance0 = Wall()
            wall_instance0.xy = (88, 21)
            wall_instance0.wh = (72, 38)
            objects_map['fixed wall 0'] = wall_instance0
            wall_instance1 = Wall()
            wall_instance1.xy = (8, 21)
            wall_instance1.wh = (64, 38)
            objects_map['fixed wall 1'] = wall_instance1
            wall_instance2 = Wall()
            wall_instance2.xy = (144, 61)
            wall_instance2.wh = (16, 37)
            objects_map['fixed wall 2'] = wall_instance2
            wall_instance3 = Wall()
            wall_instance3.xy = (8, 61)
            wall_instance3.wh = (8, 37)
            objects_map['fixed wall 3'] = wall_instance3
            wall_instance4 = Wall()
            wall_instance4.xy = (136, 101)
            wall_instance4.wh = (24, 38)
            objects_map['fixed wall 4'] = wall_instance4
            wall_instance5 = Wall()
            wall_instance5.xy = (8, 101)
            wall_instance5.wh = (16, 38)
            objects_map['fixed wall 5'] = wall_instance5
            number_of_walls = 6
            i = 0
            while (objects_map.get(f"fixed wall {number_of_walls + i}") != None):
                objects_map.pop(f"fixed wall {number_of_walls + i}")
                i += 1
        elif ram_state[28] == 2:
            number_of_lava_walls = 0
            i = 0
            while (objects_map.get(f"lava wall {number_of_lava_walls + i}") != None):
                objects_map.pop(f"lava wall {number_of_lava_walls + i}")
                i += 1
            wall_instance0 = Wall()
            wall_instance0.xy = (136, 21)
            wall_instance0.wh = (24, 38)
            objects_map['fixed wall 0'] = wall_instance0
            wall_instance1 = Wall()
            wall_instance1.xy = (8, 21)
            wall_instance1.wh = (16, 38)
            objects_map['fixed wall 1'] = wall_instance1
            wall_instance2 = Wall()
            wall_instance2.xy = (144, 61)
            wall_instance2.wh = (16, 37)
            objects_map['fixed wall 2'] = wall_instance2
            wall_instance3 = Wall()
            wall_instance3.xy = (8, 61)
            wall_instance3.wh = (8, 37)
            objects_map['fixed wall 3'] = wall_instance3
            wall_instance4 = Wall()
            wall_instance4.xy = (112, 101)
            wall_instance4.wh = (48, 38)
            objects_map['fixed wall 4'] = wall_instance4
            wall_instance5 = Wall()
            wall_instance5.xy = (56, 101)
            wall_instance5.wh = (48, 38)
            objects_map['fixed wall 5'] = wall_instance5
            wall_instance6 = Wall()
            wall_instance6.xy = (8, 101)
            wall_instance6.wh = (40, 38)
            objects_map['fixed wall 6'] = wall_instance6
            number_of_walls = 7
            i = 0
            while (objects_map.get(f"fixed wall {number_of_walls + i}") != None):
                objects_map.pop(f"fixed wall {number_of_walls + i}")
                i += 1
        elif ram_state[28] == 3:
            number_of_lava_walls = 0
            i = 0
            while (objects_map.get(f"lava wall {number_of_lava_walls + i}") != None):
                objects_map.pop(f"lava wall {number_of_lava_walls + i}")
                i += 1
            wall_instance0 = Wall()
            wall_instance0.xy = (112, 21)
            wall_instance0.wh = (48, 38)
            objects_map['fixed wall 0'] = wall_instance0
            wall_instance1 = Wall()
            wall_instance1.xy = (56, 21)
            wall_instance1.wh = (48, 38)
            objects_map['fixed wall 1'] = wall_instance1
            wall_instance2 = Wall()
            wall_instance2.xy = (8, 21)
            wall_instance2.wh = (40, 38)
            objects_map['fixed wall 2'] = wall_instance2
            wall_instance3 = Wall()
            wall_instance3.xy = (144, 61)
            wall_instance3.wh = (16, 37)
            objects_map['fixed wall 3'] = wall_instance3
            wall_instance4 = Wall()
            wall_instance4.xy = (8, 61)
            wall_instance4.wh = (8, 37)
            objects_map['fixed wall 4'] = wall_instance4
            wall_instance5 = Wall()
            wall_instance5.xy = (120, 101)
            wall_instance5.wh = (40, 38)
            objects_map['fixed wall 5'] = wall_instance5
            wall_instance6 = Wall()
            wall_instance6.xy = (48, 101)
            wall_instance6.wh = (64, 38)
            objects_map['fixed wall 6'] = wall_instance6
            wall_instance7 = Wall()
            wall_instance7.xy = (8, 101)
            wall_instance7.wh = (32, 38)
            objects_map['fixed wall 7'] = wall_instance7
            number_of_walls = 8
            i = 0
            while (objects_map.get(f"fixed wall {number_of_walls + i}") != None):
                objects_map.pop(f"fixed wall {number_of_walls + i}")
                i += 1
        elif ram_state[28] == 4:
            number_of_lava_walls = 0
            i = 0
            while (objects_map.get(f"lava wall {number_of_lava_walls + i}") != None):
                objects_map.pop(f"lava wall {number_of_lava_walls + i}")
                i += 1
            wall_instance0 = Wall()
            wall_instance0.xy = (120, 21)
            wall_instance0.wh = (40, 38)
            objects_map['fixed wall 0'] = wall_instance0
            wall_instance1 = Wall()
            wall_instance1.xy = (48, 21)
            wall_instance1.wh = (64, 38)
            objects_map['fixed wall 1'] = wall_instance1
            wall_instance2 = Wall()
            wall_instance2.xy = (8, 21)
            wall_instance2.wh = (32, 38)
            objects_map['fixed wall 2'] = wall_instance2
            wall_instance3 = Wall()
            wall_instance3.xy = (144, 61)
            wall_instance3.wh = (16, 37)
            objects_map['fixed wall 3'] = wall_instance3
            wall_instance4 = Wall()
            wall_instance4.xy = (8, 61)
            wall_instance4.wh = (8, 37)
            objects_map['fixed wall 4'] = wall_instance4
            wall_instance5 = Wall()
            wall_instance5.xy = (88, 101)
            wall_instance5.wh = (72, 38)
            objects_map['fixed wall 5'] = wall_instance5
            wall_instance6 = Wall()
            wall_instance6.xy = (8, 101)
            wall_instance6.wh = (64, 38)
            objects_map['fixed wall 6'] = wall_instance6
            number_of_walls = 7
            i = 0
            while (objects_map.get(f"fixed wall {number_of_walls + i}") != None):
                objects_map.pop(f"fixed wall {number_of_walls + i}")
                i += 1
        elif ram_state[28] == 5:
            number_of_lava_walls = 0
            i = 0
            while (objects_map.get(f"lava wall {number_of_lava_walls + i}") != None):
                objects_map.pop(f"lava wall {number_of_lava_walls + i}")
                i += 1
            wall_instance0 = Wall()
            wall_instance0.xy = (88, 21)
            wall_instance0.wh = (72, 38)
            objects_map['fixed wall 0'] = wall_instance0
            wall_instance1 = Wall()
            wall_instance1.xy = (8, 21)
            wall_instance1.wh = (64, 38)
            objects_map['fixed wall 1'] = wall_instance1
            wall_instance2 = Wall()
            wall_instance2.xy = (136, 61)
            wall_instance2.wh = (24, 37)
            objects_map['fixed wall 2'] = wall_instance2
            wall_instance3 = Wall()
            wall_instance3.xy = (8, 61)
            wall_instance3.wh = (16, 37)
            objects_map['fixed wall 3'] = wall_instance3
            wall_instance4 = Wall()
            wall_instance4.xy = (8, 101)
            wall_instance4.wh = (152, 38)
            objects_map['fixed wall 4'] = wall_instance4
            number_of_walls = 5
            i = 0
            while (objects_map.get(f"fixed wall {number_of_walls + i}") != None):
                objects_map.pop(f"fixed wall {number_of_walls + i}")
                i += 1

    elif ram_state[117] == 3:
        if ram_state[28] == 0:
            number_of_lava_walls = 0
            i = 0
            while (objects_map.get(f"lava wall {number_of_lava_walls + i}") != None):
                objects_map.pop(f"lava wall {number_of_lava_walls + i}")
                i += 1
            wall_instance0 = Wall()
            wall_instance0.xy = (136, 21)
            wall_instance0.wh = (24, 38)
            objects_map['fixed wall 0'] = wall_instance0
            wall_instance1 = Wall()
            wall_instance1.xy = (8, 21)
            wall_instance1.wh = (16, 38)
            objects_map['fixed wall 1'] = wall_instance1
            wall_instance2 = Wall()
            wall_instance2.xy = (140, 61)
            wall_instance2.wh = (20, 37)
            objects_map['fixed wall 2'] = wall_instance2
            wall_instance3 = Wall()
            wall_instance3.xy = (8, 61)
            wall_instance3.wh = (12, 37)
            objects_map['fixed wall 3'] = wall_instance3
            wall_instance4 = Wall()
            wall_instance4.xy = (88, 101)
            wall_instance4.wh = (72, 38)
            objects_map['fixed wall 4'] = wall_instance4
            wall_instance5 = Wall()
            wall_instance5.xy = (8, 101)
            wall_instance5.wh = (64, 38)
            objects_map['fixed wall 5'] = wall_instance5
            number_of_walls = 6
            i = 0
            while (objects_map.get(f"fixed wall {number_of_walls + i}") != None):
                objects_map.pop(f"fixed wall {number_of_walls + i}")
                i += 1
        elif ram_state[28] == 1:
            number_of_lava_walls = 0
            i = 0
            while (objects_map.get(f"lava wall {number_of_lava_walls + i}") != None):
                objects_map.pop(f"lava wall {number_of_lava_walls + i}")
                i += 1
            wall_instance0 = Wall()
            wall_instance0.xy = (88, 21)
            wall_instance0.wh = (72, 38)
            objects_map['fixed wall 0'] = wall_instance0
            wall_instance1 = Wall()
            wall_instance1.xy = (8, 21)
            wall_instance1.wh = (64, 38)
            objects_map['fixed wall 1'] = wall_instance1
            wall_instance2 = Wall()
            wall_instance2.xy = (144, 61)
            wall_instance2.wh = (16, 37)
            objects_map['fixed wall 2'] = wall_instance2
            wall_instance3 = Wall()
            wall_instance3.xy = (8, 61)
            wall_instance3.wh = (8, 37)
            objects_map['fixed wall 3'] = wall_instance3
            wall_instance4 = Wall()
            wall_instance4.xy = (140, 101)
            wall_instance4.wh = (20, 38)
            objects_map['fixed wall 4'] = wall_instance4
            wall_instance5 = Wall()
            wall_instance5.xy = (28, 101)
            wall_instance5.wh = (104, 38)
            objects_map['fixed wall 5'] = wall_instance5
            wall_instance6 = Wall()
            wall_instance6.xy = (8, 101)
            wall_instance6.wh = (12, 38)
            objects_map['fixed wall 6'] = wall_instance6
            number_of_walls = 7
            i = 0
            while (objects_map.get(f"fixed wall {number_of_walls + i}") != None):
                objects_map.pop(f"fixed wall {number_of_walls + i}")
                i += 1
        elif ram_state[28] == 2:
            number_of_lava_walls = 0
            i = 0
            while (objects_map.get(f"lava wall {number_of_lava_walls + i}") != None):
                objects_map.pop(f"lava wall {number_of_lava_walls + i}")
                i += 1
            wall_instance0 = Wall()
            wall_instance0.xy = (140, 21)
            wall_instance0.wh = (20, 38)
            objects_map['fixed wall 0'] = wall_instance0
            wall_instance1 = Wall()
            wall_instance1.xy = (28, 21)
            wall_instance1.wh = (104, 38)
            objects_map['fixed wall 1'] = wall_instance1
            wall_instance2 = Wall()
            wall_instance2.xy = (8, 21)
            wall_instance2.wh = (12, 38)
            objects_map['fixed wall 2'] = wall_instance2
            wall_instance3 = Wall()
            wall_instance3.xy = (144, 61)
            wall_instance3.wh = (16, 37)
            objects_map['fixed wall 3'] = wall_instance3
            wall_instance4 = Wall()
            wall_instance4.xy = (40, 61)
            wall_instance4.wh = (80, 37)
            objects_map['fixed wall 4'] = wall_instance4
            wall_instance5 = Wall()
            wall_instance5.xy = (8, 61)
            wall_instance5.wh = (8, 37)
            objects_map['fixed wall 5'] = wall_instance5
            wall_instance6 = Wall()
            wall_instance6.xy = (128, 101)
            wall_instance6.wh = (32, 38)
            objects_map['fixed wall 6'] = wall_instance6
            wall_instance7 = Wall()
            wall_instance7.xy = (44, 101)
            wall_instance7.wh = (72, 38)
            objects_map['fixed wall 7'] = wall_instance7
            wall_instance8 = Wall()
            wall_instance8.xy = (8, 101)
            wall_instance8.wh = (24, 38)
            objects_map['fixed wall 8'] = wall_instance8
            number_of_walls = 9
            i = 0
            while (objects_map.get(f"fixed wall {number_of_walls + i}") != None):
                objects_map.pop(f"fixed wall {number_of_walls + i}")
                i += 1
        elif ram_state[28] == 3:
            number_of_lava_walls = 0
            i = 0
            while (objects_map.get(f"lava wall {number_of_lava_walls + i}") != None):
                objects_map.pop(f"lava wall {number_of_lava_walls + i}")
                i += 1
            wall_instance0 = Wall()
            wall_instance0.xy = (128, 21)
            wall_instance0.wh = (32, 38)
            objects_map['fixed wall 0'] = wall_instance0
            wall_instance1 = Wall()
            wall_instance1.xy = (44, 21)
            wall_instance1.wh = (72, 38)
            objects_map['fixed wall 1'] = wall_instance1
            wall_instance2 = Wall()
            wall_instance2.xy = (8, 21)
            wall_instance2.wh = (24, 38)
            objects_map['fixed wall 2'] = wall_instance2
            wall_instance3 = Wall()
            wall_instance3.xy = (140, 61)
            wall_instance3.wh = (20, 37)
            objects_map['fixed wall 3'] = wall_instance3
            wall_instance4 = Wall()
            wall_instance4.xy = (48, 61)
            wall_instance4.wh = (64, 37)
            objects_map['fixed wall 4'] = wall_instance4
            wall_instance5 = Wall()
            wall_instance5.xy = (8, 61)
            wall_instance5.wh = (12, 37)
            objects_map['fixed wall 5'] = wall_instance5
            wall_instance6 = Wall()
            wall_instance6.xy = (144, 101)
            wall_instance6.wh = (16, 38)
            objects_map['fixed wall 6'] = wall_instance6
            wall_instance7 = Wall()
            wall_instance7.xy = (32, 101)
            wall_instance7.wh = (96, 38)
            objects_map['fixed wall 7'] = wall_instance7
            wall_instance8 = Wall()
            wall_instance8.xy = (8, 101)
            wall_instance8.wh = (8, 38)
            objects_map['fixed wall 8'] = wall_instance8
            number_of_walls = 9
            i = 0
            while (objects_map.get(f"fixed wall {number_of_walls + i}") != None):
                objects_map.pop(f"fixed wall {number_of_walls + i}")
                i += 1
        elif ram_state[28] == 4:
            number_of_lava_walls = 0
            i = 0
            while (objects_map.get(f"lava wall {number_of_lava_walls + i}") != None):
                objects_map.pop(f"lava wall {number_of_lava_walls + i}")
                i += 1
            wall_instance0 = Wall()
            wall_instance0.xy = (144, 21)
            wall_instance0.wh = (16, 38)
            objects_map['fixed wall 0'] = wall_instance0
            wall_instance1 = Wall()
            wall_instance1.xy = (32, 21)
            wall_instance1.wh = (96, 38)
            objects_map['fixed wall 1'] = wall_instance1
            wall_instance2 = Wall()
            wall_instance2.xy = (8, 21)
            wall_instance2.wh = (8, 38)
            objects_map['fixed wall 2'] = wall_instance2
            wall_instance3 = Wall()
            wall_instance3.xy = (140, 61)
            wall_instance3.wh = (20, 37)
            objects_map['fixed wall 3'] = wall_instance3
            wall_instance4 = Wall()
            wall_instance4.xy = (8, 61)
            wall_instance4.wh = (12, 37)
            objects_map['fixed wall 4'] = wall_instance4
            wall_instance5 = Wall()
            wall_instance5.xy = (88, 101)
            wall_instance5.wh = (72, 38)
            objects_map['fixed wall 5'] = wall_instance5
            wall_instance6 = Wall()
            wall_instance6.xy = (8, 101)
            wall_instance6.wh = (64, 38)
            objects_map['fixed wall 6'] = wall_instance6
            number_of_walls = 7
            i = 0
            while (objects_map.get(f"fixed wall {number_of_walls + i}") != None):
                objects_map.pop(f"fixed wall {number_of_walls + i}")
                i += 1
        elif ram_state[28] == 5:
            number_of_lava_walls = 0
            i = 0
            while (objects_map.get(f"lava wall {number_of_lava_walls + i}") != None):
                objects_map.pop(f"lava wall {number_of_lava_walls + i}")
                i += 1
            wall_instance0 = Wall()
            wall_instance0.xy = (88, 21)
            wall_instance0.wh = (72, 38)
            objects_map['fixed wall 0'] = wall_instance0
            wall_instance1 = Wall()
            wall_instance1.xy = (8, 21)
            wall_instance1.wh = (64, 38)
            objects_map['fixed wall 1'] = wall_instance1
            wall_instance2 = Wall()
            wall_instance2.xy = (144, 61)
            wall_instance2.wh = (16, 37)
            objects_map['fixed wall 2'] = wall_instance2
            wall_instance3 = Wall()
            wall_instance3.xy = (8, 61)
            wall_instance3.wh = (8, 37)
            objects_map['fixed wall 3'] = wall_instance3
            wall_instance4 = Wall()
            wall_instance4.xy = (140, 101)
            wall_instance4.wh = (20, 38)
            objects_map['fixed wall 4'] = wall_instance4
            wall_instance5 = Wall()
            wall_instance5.xy = (28, 101)
            wall_instance5.wh = (104, 38)
            objects_map['fixed wall 5'] = wall_instance5
            wall_instance6 = Wall()
            wall_instance6.xy = (8, 101)
            wall_instance6.wh = (12, 38)
            objects_map['fixed wall 6'] = wall_instance6
            number_of_walls = 7
            i = 0
            while (objects_map.get(f"fixed wall {number_of_walls + i}") != None):
                objects_map.pop(f"fixed wall {number_of_walls + i}")
                i += 1
        elif ram_state[28] == 6:
            number_of_lava_walls = 0
            i = 0
            while (objects_map.get(f"lava wall {number_of_lava_walls + i}") != None):
                objects_map.pop(f"lava wall {number_of_lava_walls + i}")
                i += 1
            wall_instance0 = Wall()
            wall_instance0.xy = (140, 21)
            wall_instance0.wh = (20, 38)
            objects_map['fixed wall 0'] = wall_instance0
            wall_instance1 = Wall()
            wall_instance1.xy = (28, 21)
            wall_instance1.wh = (104, 38)
            objects_map['fixed wall 1'] = wall_instance1
            wall_instance2 = Wall()
            wall_instance2.xy = (8, 21)
            wall_instance2.wh = (12, 38)
            objects_map['fixed wall 2'] = wall_instance2
            wall_instance3 = Wall()
            wall_instance3.xy = (144, 61)
            wall_instance3.wh = (16, 37)
            objects_map['fixed wall 3'] = wall_instance3
            wall_instance4 = Wall()
            wall_instance4.xy = (8, 61)
            wall_instance4.wh = (8, 37)
            objects_map['fixed wall 4'] = wall_instance4
            wall_instance5 = Wall()
            wall_instance5.xy = (100, 101)
            wall_instance5.wh = (60, 38)
            objects_map['fixed wall 5'] = wall_instance5
            wall_instance6 = Wall()
            wall_instance6.xy = (8, 101)
            wall_instance6.wh = (52, 38)
            objects_map['fixed wall 6'] = wall_instance6
            number_of_walls = 7
            i = 0
            while (objects_map.get(f"fixed wall {number_of_walls + i}") != None):
                objects_map.pop(f"fixed wall {number_of_walls + i}")
                i += 1
        elif ram_state[28] == 7:
            number_of_lava_walls = 0
            i = 0
            while (objects_map.get(f"lava wall {number_of_lava_walls + i}") != None):
                objects_map.pop(f"lava wall {number_of_lava_walls + i}")
                i += 1
            wall_instance0 = Wall()
            wall_instance0.xy = (100, 21)
            wall_instance0.wh = (60, 38)
            objects_map['fixed wall 0'] = wall_instance0
            wall_instance1 = Wall()
            wall_instance1.xy = (8, 21)
            wall_instance1.wh = (52, 38)
            objects_map['fixed wall 1'] = wall_instance1
            wall_instance2 = Wall()
            wall_instance2.xy = (136, 61)
            wall_instance2.wh = (24, 37)
            objects_map['fixed wall 2'] = wall_instance2
            wall_instance3 = Wall()
            wall_instance3.xy = (72, 61)
            wall_instance3.wh = (16, 37)
            objects_map['fixed wall 3'] = wall_instance3
            wall_instance4 = Wall()
            wall_instance4.xy = (8, 61)
            wall_instance4.wh = (16, 37)
            objects_map['fixed wall 4'] = wall_instance4
            wall_instance5 = Wall()
            wall_instance5.xy = (8, 101)
            wall_instance5.wh = (152, 38)
            objects_map['fixed wall 5'] = wall_instance5
            number_of_walls = 6
            i = 0
            while (objects_map.get(f"fixed wall {number_of_walls + i}") != None):
                objects_map.pop(f"fixed wall {number_of_walls + i}")
                i += 1

    elif ram_state[117] == 4:
        if ram_state[28] == 0:
            number_of_lava_walls = 0
            i = 0
            while (objects_map.get(f"lava wall {number_of_lava_walls + i}") != None):
                objects_map.pop(f"lava wall {number_of_lava_walls + i}")
                i += 1
            wall_instance0 = Wall()
            wall_instance0.xy = (136, 21)
            wall_instance0.wh = (24, 38)
            objects_map['fixed wall 0'] = wall_instance0
            wall_instance1 = Wall()
            wall_instance1.xy = (8, 21)
            wall_instance1.wh = (16, 38)
            objects_map['fixed wall 1'] = wall_instance1
            wall_instance2 = Wall()
            wall_instance2.xy = (144, 61)
            wall_instance2.wh = (16, 37)
            objects_map['fixed wall 2'] = wall_instance2
            wall_instance3 = Wall()
            wall_instance3.xy = (8, 61)
            wall_instance3.wh = (8, 37)
            objects_map['fixed wall 3'] = wall_instance3
            wall_instance4 = Wall()
            wall_instance4.xy = (88, 101)
            wall_instance4.wh = (72, 38)
            objects_map['fixed wall 4'] = wall_instance4
            wall_instance5 = Wall()
            wall_instance5.xy = (8, 101)
            wall_instance5.wh = (64, 38)
            objects_map['fixed wall 5'] = wall_instance5
            number_of_walls = 6
            i = 0
            while (objects_map.get(f"fixed wall {number_of_walls + i}") != None):
                objects_map.pop(f"fixed wall {number_of_walls + i}")
                i += 1
        elif ram_state[28] == 1:
            wall_instance0 = LavaWall()
            wall_instance0.xy = (144, 61)
            wall_instance0.wh = (16, 37)
            objects_map['lava wall 0'] = wall_instance0
            wall_instance1 = LavaWall()
            wall_instance1.xy = (8, 61)
            wall_instance1.wh = (8, 37)
            objects_map['lava wall 1'] = wall_instance1
            number_of_lava_walls = 2
            i = 0
            while (objects_map.get(f"lava wall {number_of_lava_walls + i}") != None):
                objects_map.pop(f"lava wall {number_of_lava_walls + i}")
                i += 1
            wall_instance0 = Wall()
            wall_instance0.xy = (88, 21)
            wall_instance0.wh = (72, 38)
            objects_map['fixed wall 0'] = wall_instance0
            wall_instance1 = Wall()
            wall_instance1.xy = (8, 21)
            wall_instance1.wh = (64, 38)
            objects_map['fixed wall 1'] = wall_instance1
            wall_instance2 = Wall()
            wall_instance2.xy = (8, 101)
            wall_instance2.wh = (152, 38)
            objects_map['fixed wall 2'] = wall_instance2
            number_of_walls = 3
            i = 0
            while (objects_map.get(f"fixed wall {number_of_walls + i}") != None):
                objects_map.pop(f"fixed wall {number_of_walls + i}")
                i += 1
        elif ram_state[28] == 2:
            number_of_lava_walls = 0
            i = 0
            while (objects_map.get(f"lava wall {number_of_lava_walls + i}") != None):
                objects_map.pop(f"lava wall {number_of_lava_walls + i}")
                i += 1
            wall_instance0 = Wall()
            wall_instance0.xy = (8, 21)
            wall_instance0.wh = (152, 38)
            objects_map['fixed wall 0'] = wall_instance0
            wall_instance1 = Wall()
            wall_instance1.xy = (144, 61)
            wall_instance1.wh = (16, 37)
            objects_map['fixed wall 1'] = wall_instance1
            wall_instance2 = Wall()
            wall_instance2.xy = (8, 61)
            wall_instance2.wh = (8, 37)
            objects_map['fixed wall 2'] = wall_instance2
            wall_instance3 = Wall()
            wall_instance3.xy = (136, 101)
            wall_instance3.wh = (24, 38)
            objects_map['fixed wall 3'] = wall_instance3
            wall_instance4 = Wall()
            wall_instance4.xy = (8, 101)
            wall_instance4.wh = (16, 38)
            objects_map['fixed wall 4'] = wall_instance4
            number_of_walls = 5
            i = 0
            while (objects_map.get(f"fixed wall {number_of_walls + i}") != None):
                objects_map.pop(f"fixed wall {number_of_walls + i}")
                i += 1
        elif ram_state[28] == 3:
            wall_instance0 = LavaWall()
            wall_instance0.xy = (112, 61)
            wall_instance0.wh = (48, 37)
            objects_map['lava wall 0'] = wall_instance0
            wall_instance1 = LavaWall()
            wall_instance1.xy = (8, 61)
            wall_instance1.wh = (40, 37)
            objects_map['lava wall 1'] = wall_instance1
            number_of_lava_walls = 2
            i = 0
            while (objects_map.get(f"lava wall {number_of_lava_walls + i}") != None):
                objects_map.pop(f"lava wall {number_of_lava_walls + i}")
                i += 1
            wall_instance0 = Wall()
            wall_instance0.xy = (136, 21)
            wall_instance0.wh = (24, 38)
            objects_map['fixed wall 0'] = wall_instance0
            wall_instance1 = Wall()
            wall_instance1.xy = (8, 21)
            wall_instance1.wh = (16, 38)
            objects_map['fixed wall 1'] = wall_instance1
            wall_instance2 = Wall()
            wall_instance2.xy = (84, 101)
            wall_instance2.wh = (76, 38)
            objects_map['fixed wall 2'] = wall_instance2
            wall_instance3 = Wall()
            wall_instance3.xy = (8, 101)
            wall_instance3.wh = (68, 38)
            objects_map['fixed wall 3'] = wall_instance3
            number_of_walls = 4
            i = 0
            while (objects_map.get(f"fixed wall {number_of_walls + i}") != None):
                objects_map.pop(f"fixed wall {number_of_walls + i}")
                i += 1
        elif ram_state[28] == 4:
            number_of_lava_walls = 0
            i = 0
            while (objects_map.get(f"lava wall {number_of_lava_walls + i}") != None):
                objects_map.pop(f"lava wall {number_of_lava_walls + i}")
                i += 1
            wall_instance0 = Wall()
            wall_instance0.xy = (84, 21)
            wall_instance0.wh = (76, 38)
            objects_map['fixed wall 0'] = wall_instance0
            wall_instance1 = Wall()
            wall_instance1.xy = (8, 21)
            wall_instance1.wh = (68, 38)
            objects_map['fixed wall 1'] = wall_instance1
            wall_instance2 = Wall()
            wall_instance2.xy = (144, 61)
            wall_instance2.wh = (16, 37)
            objects_map['fixed wall 2'] = wall_instance2
            wall_instance3 = Wall()
            wall_instance3.xy = (8, 61)
            wall_instance3.wh = (8, 37)
            objects_map['fixed wall 3'] = wall_instance3
            wall_instance4 = Wall()
            wall_instance4.xy = (136, 101)
            wall_instance4.wh = (24, 38)
            objects_map['fixed wall 4'] = wall_instance4
            wall_instance5 = Wall()
            wall_instance5.xy = (32, 101)
            wall_instance5.wh = (96, 38)
            objects_map['fixed wall 5'] = wall_instance5
            wall_instance6 = Wall()
            wall_instance6.xy = (8, 101)
            wall_instance6.wh = (16, 38)
            objects_map['fixed wall 6'] = wall_instance6
            number_of_walls = 7
            i = 0
            while (objects_map.get(f"fixed wall {number_of_walls + i}") != None):
                objects_map.pop(f"fixed wall {number_of_walls + i}")
                i += 1
        elif ram_state[28] == 5:
            wall_instance0 = LavaWall()
            wall_instance0.xy = (144, 61)
            wall_instance0.wh = (16, 37)
            objects_map['lava wall 0'] = wall_instance0
            wall_instance1 = LavaWall()
            wall_instance1.xy = (8, 61)
            wall_instance1.wh = (8, 37)
            objects_map['lava wall 1'] = wall_instance1
            number_of_lava_walls = 2
            i = 0
            while (objects_map.get(f"lava wall {number_of_lava_walls + i}") != None):
                objects_map.pop(f"lava wall {number_of_lava_walls + i}")
                i += 1
            wall_instance0 = Wall()
            wall_instance0.xy = (136, 21)
            wall_instance0.wh = (24, 38)
            objects_map['fixed wall 0'] = wall_instance0
            wall_instance1 = Wall()
            wall_instance1.xy = (32, 21)
            wall_instance1.wh = (96, 38)
            objects_map['fixed wall 1'] = wall_instance1
            wall_instance2 = Wall()
            wall_instance2.xy = (8, 21)
            wall_instance2.wh = (16, 38)
            objects_map['fixed wall 2'] = wall_instance2
            wall_instance3 = Wall()
            wall_instance3.xy = (88, 101)
            wall_instance3.wh = (72, 38)
            objects_map['fixed wall 3'] = wall_instance3
            wall_instance4 = Wall()
            wall_instance4.xy = (8, 101)
            wall_instance4.wh = (64, 38)
            objects_map['fixed wall 4'] = wall_instance4
            number_of_walls = 5
            i = 0
            while (objects_map.get(f"fixed wall {number_of_walls + i}") != None):
                objects_map.pop(f"fixed wall {number_of_walls + i}")
                i += 1
        elif ram_state[28] == 6:
            wall_instance0 = LavaWall()
            wall_instance0.xy = (144, 61)
            wall_instance0.wh = (16, 37)
            objects_map['lava wall 0'] = wall_instance0
            wall_instance1 = LavaWall()
            wall_instance1.xy = (8, 61)
            wall_instance1.wh = (8, 37)
            objects_map['lava wall 1'] = wall_instance1
            number_of_lava_walls = 2
            i = 0
            while (objects_map.get(f"lava wall {number_of_lava_walls + i}") != None):
                objects_map.pop(f"lava wall {number_of_lava_walls + i}")
                i += 1
            wall_instance0 = Wall()
            wall_instance0.xy = (88, 21)
            wall_instance0.wh = (72, 38)
            objects_map['fixed wall 0'] = wall_instance0
            wall_instance1 = Wall()
            wall_instance1.xy = (8, 21)
            wall_instance1.wh = (64, 38)
            objects_map['fixed wall 1'] = wall_instance1
            wall_instance2 = Wall()
            wall_instance2.xy = (120, 101)
            wall_instance2.wh = (40, 38)
            objects_map['fixed wall 2'] = wall_instance2
            wall_instance3 = Wall()
            wall_instance3.xy = (48, 101)
            wall_instance3.wh = (64, 38)
            objects_map['fixed wall 3'] = wall_instance3
            wall_instance4 = Wall()
            wall_instance4.xy = (8, 101)
            wall_instance4.wh = (32, 38)
            objects_map['fixed wall 4'] = wall_instance4
            number_of_walls = 5
            i = 0
            while (objects_map.get(f"fixed wall {number_of_walls + i}") != None):
                objects_map.pop(f"fixed wall {number_of_walls + i}")
                i += 1
        elif ram_state[28] == 7:
            number_of_lava_walls = 0
            i = 0
            while (objects_map.get(f"lava wall {number_of_lava_walls + i}") != None):
                objects_map.pop(f"lava wall {number_of_lava_walls + i}")
                i += 1
            wall_instance0 = Wall()
            wall_instance0.xy = (120, 21)
            wall_instance0.wh = (40, 38)
            objects_map['fixed wall 0'] = wall_instance0
            wall_instance1 = Wall()
            wall_instance1.xy = (48, 21)
            wall_instance1.wh = (64, 38)
            objects_map['fixed wall 1'] = wall_instance1
            wall_instance2 = Wall()
            wall_instance2.xy = (8, 21)
            wall_instance2.wh = (32, 38)
            objects_map['fixed wall 2'] = wall_instance2
            wall_instance3 = Wall()
            wall_instance3.xy = (144, 61)
            wall_instance3.wh = (16, 37)
            objects_map['fixed wall 3'] = wall_instance3
            wall_instance4 = Wall()
            wall_instance4.xy = (8, 61)
            wall_instance4.wh = (8, 37)
            objects_map['fixed wall 4'] = wall_instance4
            wall_instance5 = Wall()
            wall_instance5.xy = (8, 101)
            wall_instance5.wh = (152, 38)
            objects_map['fixed wall 5'] = wall_instance5
            number_of_walls = 6
            i = 0
            while (objects_map.get(f"fixed wall {number_of_walls + i}") != None):
                objects_map.pop(f"fixed wall {number_of_walls + i}")
                i += 1

    elif ram_state[117] == 5:
        if ram_state[28] == 0:
            wall_instance0 = LavaWall()
            wall_instance0.xy = (144, 61)
            wall_instance0.wh = (16, 37)
            objects_map['lava wall 0'] = wall_instance0
            wall_instance1 = LavaWall()
            wall_instance1.xy = (8, 61)
            wall_instance1.wh = (8, 37)
            objects_map['lava wall 1'] = wall_instance1
            number_of_lava_walls = 2
            i = 0
            while (objects_map.get(f"lava wall {number_of_lava_walls + i}") != None):
                objects_map.pop(f"lava wall {number_of_lava_walls + i}")
                i += 1
            wall_instance0 = Wall()
            wall_instance0.xy = (136, 21)
            wall_instance0.wh = (24, 38)
            objects_map['fixed wall 0'] = wall_instance0
            wall_instance1 = Wall()
            wall_instance1.xy = (8, 21)
            wall_instance1.wh = (16, 38)
            objects_map['fixed wall 1'] = wall_instance1
            wall_instance2 = Wall()
            wall_instance2.xy = (88, 101)
            wall_instance2.wh = (72, 38)
            objects_map['fixed wall 2'] = wall_instance2
            wall_instance3 = Wall()
            wall_instance3.xy = (8, 101)
            wall_instance3.wh = (64, 38)
            objects_map['fixed wall 3'] = wall_instance3
            number_of_walls = 4
            i = 0
            while (objects_map.get(f"fixed wall {number_of_walls + i}") != None):
                objects_map.pop(f"fixed wall {number_of_walls + i}")
                i += 1
        elif ram_state[28] == 1:
            number_of_lava_walls = 0
            i = 0
            while (objects_map.get(f"lava wall {number_of_lava_walls + i}") != None):
                objects_map.pop(f"lava wall {number_of_lava_walls + i}")
                i += 1
            wall_instance0 = Wall()
            wall_instance0.xy = (88, 21)
            wall_instance0.wh = (72, 38)
            objects_map['fixed wall 0'] = wall_instance0
            wall_instance1 = Wall()
            wall_instance1.xy = (8, 21)
            wall_instance1.wh = (64, 38)
            objects_map['fixed wall 1'] = wall_instance1
            wall_instance2 = Wall()
            wall_instance2.xy = (144, 61)
            wall_instance2.wh = (16, 37)
            objects_map['fixed wall 2'] = wall_instance2
            wall_instance3 = Wall()
            wall_instance3.xy = (8, 61)
            wall_instance3.wh = (8, 37)
            objects_map['fixed wall 3'] = wall_instance3
            wall_instance4 = Wall()
            wall_instance4.xy = (140, 101)
            wall_instance4.wh = (20, 38)
            objects_map['fixed wall 4'] = wall_instance4
            wall_instance5 = Wall()
            wall_instance5.xy = (56, 101)
            wall_instance5.wh = (48, 38)
            objects_map['fixed wall 5'] = wall_instance5
            wall_instance6 = Wall()
            wall_instance6.xy = (8, 101)
            wall_instance6.wh = (12, 38)
            objects_map['fixed wall 6'] = wall_instance6
            number_of_walls = 7
            i = 0
            while (objects_map.get(f"fixed wall {number_of_walls + i}") != None):
                objects_map.pop(f"fixed wall {number_of_walls + i}")
                i += 1
        elif ram_state[28] == 2:
            wall_instance0 = LavaWall()
            wall_instance0.xy = (144, 61)
            wall_instance0.wh = (16, 37)
            objects_map['lava wall 0'] = wall_instance0
            wall_instance1 = LavaWall()
            wall_instance1.xy = (8, 61)
            wall_instance1.wh = (8, 37)
            objects_map['lava wall 1'] = wall_instance1
            number_of_lava_walls = 2
            i = 0
            while (objects_map.get(f"lava wall {number_of_lava_walls + i}") != None):
                objects_map.pop(f"lava wall {number_of_lava_walls + i}")
                i += 1
            wall_instance0 = Wall()
            wall_instance0.xy = (140, 21)
            wall_instance0.wh = (20, 38)
            objects_map['fixed wall 0'] = wall_instance0
            wall_instance1 = Wall()
            wall_instance1.xy = (56, 21)
            wall_instance1.wh = (48, 38)
            objects_map['fixed wall 1'] = wall_instance1
            wall_instance2 = Wall()
            wall_instance2.xy = (8, 21)
            wall_instance2.wh = (12, 38)
            objects_map['fixed wall 2'] = wall_instance2
            wall_instance3 = Wall()
            wall_instance3.xy = (88, 101)
            wall_instance3.wh = (72, 38)
            objects_map['fixed wall 3'] = wall_instance3
            wall_instance4 = Wall()
            wall_instance4.xy = (8, 101)
            wall_instance4.wh = (64, 38)
            objects_map['fixed wall 4'] = wall_instance4
            number_of_walls = 5
            i = 0
            while (objects_map.get(f"fixed wall {number_of_walls + i}") != None):
                objects_map.pop(f"fixed wall {number_of_walls + i}")
                i += 1
        elif ram_state[28] == 3:
            number_of_lava_walls = 0
            i = 0
            while (objects_map.get(f"lava wall {number_of_lava_walls + i}") != None):
                objects_map.pop(f"lava wall {number_of_lava_walls + i}")
                i += 1
            wall_instance0 = Wall()
            wall_instance0.xy = (88, 21)
            wall_instance0.wh = (72, 38)
            objects_map['fixed wall 0'] = wall_instance0
            wall_instance1 = Wall()
            wall_instance1.xy = (8, 21)
            wall_instance1.wh = (64, 38)
            objects_map['fixed wall 1'] = wall_instance1
            wall_instance2 = Wall()
            wall_instance2.xy = (136, 61)
            wall_instance2.wh = (24, 37)
            objects_map['fixed wall 2'] = wall_instance2
            wall_instance3 = Wall()
            wall_instance3.xy = (8, 61)
            wall_instance3.wh = (16, 37)
            objects_map['fixed wall 3'] = wall_instance3
            wall_instance4 = Wall()
            wall_instance4.xy = (132, 101)
            wall_instance4.wh = (28, 38)
            objects_map['fixed wall 4'] = wall_instance4
            wall_instance5 = Wall()
            wall_instance5.xy = (104, 101)
            wall_instance5.wh = (20, 38)
            objects_map['fixed wall 5'] = wall_instance5
            wall_instance6 = Wall()
            wall_instance6.xy = (64, 101)
            wall_instance6.wh = (32, 38)
            objects_map['fixed wall 6'] = wall_instance6
            wall_instance7 = Wall()
            wall_instance7.xy = (36, 101)
            wall_instance7.wh = (20, 38)
            objects_map['fixed wall 7'] = wall_instance7
            wall_instance8 = Wall()
            wall_instance8.xy = (8, 101)
            wall_instance8.wh = (20, 38)
            objects_map['fixed wall 8'] = wall_instance8
            number_of_walls = 9
            i = 0
            while (objects_map.get(f"fixed wall {number_of_walls + i}") != None):
                objects_map.pop(f"fixed wall {number_of_walls + i}")
                i += 1
        elif ram_state[28] == 4:
            wall_instance0 = LavaWall()
            wall_instance0.xy = (112, 61)
            wall_instance0.wh = (48, 37)
            objects_map['lava wall 0'] = wall_instance0
            wall_instance1 = LavaWall()
            wall_instance1.xy = (8, 61)
            wall_instance1.wh = (40, 37)
            objects_map['lava wall 1'] = wall_instance1
            number_of_lava_walls = 2
            i = 0
            while (objects_map.get(f"lava wall {number_of_lava_walls + i}") != None):
                objects_map.pop(f"lava wall {number_of_lava_walls + i}")
                i += 1
            wall_instance0 = Wall()
            wall_instance0.xy = (132, 21)
            wall_instance0.wh = (28, 38)
            objects_map['fixed wall 0'] = wall_instance0
            wall_instance1 = Wall()
            wall_instance1.xy = (104, 21)
            wall_instance1.wh = (20, 38)
            objects_map['fixed wall 1'] = wall_instance1
            wall_instance2 = Wall()
            wall_instance2.xy = (64, 21)
            wall_instance2.wh = (32, 38)
            objects_map['fixed wall 2'] = wall_instance2
            wall_instance3 = Wall()
            wall_instance3.xy = (36, 21)
            wall_instance3.wh = (20, 38)
            objects_map['fixed wall 3'] = wall_instance3
            wall_instance4 = Wall()
            wall_instance4.xy = (8, 21)
            wall_instance4.wh = (20, 38)
            objects_map['fixed wall 4'] = wall_instance4
            wall_instance5 = Wall()
            wall_instance5.xy = (108, 101)
            wall_instance5.wh = (52, 38)
            objects_map['fixed wall 5'] = wall_instance5
            wall_instance6 = Wall()
            wall_instance6.xy = (60, 101)
            wall_instance6.wh = (40, 38)
            objects_map['fixed wall 6'] = wall_instance6
            wall_instance7 = Wall()
            wall_instance7.xy = (8, 101)
            wall_instance7.wh = (44, 38)
            objects_map['fixed wall 7'] = wall_instance7
            number_of_walls = 8
            i = 0
            while (objects_map.get(f"fixed wall {number_of_walls + i}") != None):
                objects_map.pop(f"fixed wall {number_of_walls + i}")
                i += 1
        elif ram_state[28] == 5:
            number_of_lava_walls = 0
            i = 0
            while (objects_map.get(f"lava wall {number_of_lava_walls + i}") != None):
                objects_map.pop(f"lava wall {number_of_lava_walls + i}")
                i += 1
            wall_instance0 = Wall()
            wall_instance0.xy = (108, 21)
            wall_instance0.wh = (52, 38)
            objects_map['fixed wall 0'] = wall_instance0
            wall_instance1 = Wall()
            wall_instance1.xy = (60, 21)
            wall_instance1.wh = (40, 38)
            objects_map['fixed wall 1'] = wall_instance1
            wall_instance2 = Wall()
            wall_instance2.xy = (8, 21)
            wall_instance2.wh = (44, 38)
            objects_map['fixed wall 2'] = wall_instance2
            wall_instance3 = Wall()
            wall_instance3.xy = (132, 61)
            wall_instance3.wh = (28, 37)
            objects_map['fixed wall 3'] = wall_instance3
            wall_instance4 = Wall()
            wall_instance4.xy = (52, 61)
            wall_instance4.wh = (44, 37)
            objects_map['fixed wall 4'] = wall_instance4
            wall_instance5 = Wall()
            wall_instance5.xy = (8, 61)
            wall_instance5.wh = (8, 37)
            objects_map['fixed wall 5'] = wall_instance5
            wall_instance6 = Wall()
            wall_instance6.xy = (120, 101)
            wall_instance6.wh = (40, 38)
            objects_map['fixed wall 6'] = wall_instance6
            wall_instance7 = Wall()
            wall_instance7.xy = (8, 101)
            wall_instance7.wh = (32, 38)
            objects_map['fixed wall 7'] = wall_instance7
            number_of_walls = 8
            i = 0
            while (objects_map.get(f"fixed wall {number_of_walls + i}") != None):
                objects_map.pop(f"fixed wall {number_of_walls + i}")
                i += 1
        elif ram_state[28] == 6:
            wall_instance0 = LavaWall()
            wall_instance0.xy = (144, 61)
            wall_instance0.wh = (16, 37)
            objects_map['lava wall 0'] = wall_instance0
            wall_instance1 = LavaWall()
            wall_instance1.xy = (8, 61)
            wall_instance1.wh = (8, 37)
            objects_map['lava wall 1'] = wall_instance1
            number_of_lava_walls = 2
            i = 0
            while (objects_map.get(f"lava wall {number_of_lava_walls + i}") != None):
                objects_map.pop(f"lava wall {number_of_lava_walls + i}")
                i += 1
            wall_instance0 = Wall()
            wall_instance0.xy = (120, 21)
            wall_instance0.wh = (40, 38)
            objects_map['fixed wall 0'] = wall_instance0
            wall_instance1 = Wall()
            wall_instance1.xy = (8, 21)
            wall_instance1.wh = (32, 38)
            objects_map['fixed wall 1'] = wall_instance1
            wall_instance2 = Wall()
            wall_instance2.xy = (136, 101)
            wall_instance2.wh = (24, 38)
            objects_map['fixed wall 2'] = wall_instance2
            wall_instance3 = Wall()
            wall_instance3.xy = (32, 101)
            wall_instance3.wh = (96, 38)
            objects_map['fixed wall 3'] = wall_instance3
            wall_instance4 = Wall()
            wall_instance4.xy = (8, 101)
            wall_instance4.wh = (16, 38)
            objects_map['fixed wall 4'] = wall_instance4
            number_of_walls = 5
            i = 0
            while (objects_map.get(f"fixed wall {number_of_walls + i}") != None):
                objects_map.pop(f"fixed wall {number_of_walls + i}")
                i += 1
        elif ram_state[28] == 7:
            number_of_lava_walls = 0
            i = 0
            while (objects_map.get(f"lava wall {number_of_lava_walls + i}") != None):
                objects_map.pop(f"lava wall {number_of_lava_walls + i}")
                i += 1
            wall_instance0 = Wall()
            wall_instance0.xy = (136, 21)
            wall_instance0.wh = (24, 38)
            objects_map['fixed wall 0'] = wall_instance0
            wall_instance1 = Wall()
            wall_instance1.xy = (32, 21)
            wall_instance1.wh = (96, 38)
            objects_map['fixed wall 1'] = wall_instance1
            wall_instance2 = Wall()
            wall_instance2.xy = (8, 21)
            wall_instance2.wh = (16, 38)
            objects_map['fixed wall 2'] = wall_instance2
            wall_instance3 = Wall()
            wall_instance3.xy = (144, 61)
            wall_instance3.wh = (16, 37)
            objects_map['fixed wall 3'] = wall_instance3
            wall_instance4 = Wall()
            wall_instance4.xy = (8, 61)
            wall_instance4.wh = (8, 37)
            objects_map['fixed wall 4'] = wall_instance4
            wall_instance5 = Wall()
            wall_instance5.xy = (112, 101)
            wall_instance5.wh = (48, 38)
            objects_map['fixed wall 5'] = wall_instance5
            wall_instance6 = Wall()
            wall_instance6.xy = (56, 101)
            wall_instance6.wh = (48, 38)
            objects_map['fixed wall 6'] = wall_instance6
            wall_instance7 = Wall()
            wall_instance7.xy = (8, 101)
            wall_instance7.wh = (40, 38)
            objects_map['fixed wall 7'] = wall_instance7
            number_of_walls = 8
            i = 0
            while (objects_map.get(f"fixed wall {number_of_walls + i}") != None):
                objects_map.pop(f"fixed wall {number_of_walls + i}")
                i += 1
        elif ram_state[28] == 8:
            wall_instance0 = LavaWall()
            wall_instance0.xy = (136, 61)
            wall_instance0.wh = (24, 37)
            objects_map['lava wall 0'] = wall_instance0
            wall_instance1 = LavaWall()
            wall_instance1.xy = (8, 61)
            wall_instance1.wh = (16, 37)
            objects_map['lava wall 1'] = wall_instance1
            number_of_lava_walls = 2
            i = 0
            while (objects_map.get(f"lava wall {number_of_lava_walls + i}") != None):
                objects_map.pop(f"lava wall {number_of_lava_walls + i}")
                i += 1
            wall_instance0 = Wall()
            wall_instance0.xy = (112, 21)
            wall_instance0.wh = (48, 38)
            objects_map['fixed wall 0'] = wall_instance0
            wall_instance1 = Wall()
            wall_instance1.xy = (56, 21)
            wall_instance1.wh = (48, 38)
            objects_map['fixed wall 1'] = wall_instance1
            wall_instance2 = Wall()
            wall_instance2.xy = (8, 21)
            wall_instance2.wh = (40, 38)
            objects_map['fixed wall 2'] = wall_instance2
            wall_instance3 = Wall()
            wall_instance3.xy = (88, 101)
            wall_instance3.wh = (72, 38)
            objects_map['fixed wall 3'] = wall_instance3
            wall_instance4 = Wall()
            wall_instance4.xy = (8, 101)
            wall_instance4.wh = (64, 38)
            objects_map['fixed wall 4'] = wall_instance4
            number_of_walls = 5
            i = 0
            while (objects_map.get(f"fixed wall {number_of_walls + i}") != None):
                objects_map.pop(f"fixed wall {number_of_walls + i}")
                i += 1
        elif ram_state[28] == 9:
            number_of_lava_walls = 0
            i = 0
            while (objects_map.get(f"lava wall {number_of_lava_walls + i}") != None):
                objects_map.pop(f"lava wall {number_of_lava_walls + i}")
                i += 1
            wall_instance0 = Wall()
            wall_instance0.xy = (88, 21)
            wall_instance0.wh = (72, 38)
            objects_map['fixed wall 0'] = wall_instance0
            wall_instance1 = Wall()
            wall_instance1.xy = (8, 21)
            wall_instance1.wh = (64, 38)
            objects_map['fixed wall 1'] = wall_instance1
            wall_instance2 = Wall()
            wall_instance2.xy = (136, 61)
            wall_instance2.wh = (24, 37)
            objects_map['fixed wall 2'] = wall_instance2
            wall_instance3 = Wall()
            wall_instance3.xy = (8, 61)
            wall_instance3.wh = (16, 37)
            objects_map['fixed wall 3'] = wall_instance3
            wall_instance4 = Wall()
            wall_instance4.xy = (8, 101)
            wall_instance4.wh = (152, 38)
            objects_map['fixed wall 4'] = wall_instance4
            number_of_walls = 5
            i = 0
            while (objects_map.get(f"fixed wall {number_of_walls + i}") != None):
                objects_map.pop(f"fixed wall {number_of_walls + i}")
                i += 1

    elif ram_state[117] == 6:
        if ram_state[28] == 0:
            wall_instance0 = LavaWall()
            wall_instance0.xy = (140, 61)
            wall_instance0.wh = (20, 37)
            objects_map['lava wall 0'] = wall_instance0
            wall_instance1 = LavaWall()
            wall_instance1.xy = (8, 61)
            wall_instance1.wh = (12, 37)
            objects_map['lava wall 1'] = wall_instance1
            number_of_lava_walls = 2
            i = 0
            while (objects_map.get(f"lava wall {number_of_lava_walls + i}") != None):
                objects_map.pop(f"lava wall {number_of_lava_walls + i}")
                i += 1
            wall_instance0 = Wall()
            wall_instance0.xy = (136, 21)
            wall_instance0.wh = (24, 38)
            objects_map['fixed wall 0'] = wall_instance0
            wall_instance1 = Wall()
            wall_instance1.xy = (8, 21)
            wall_instance1.wh = (16, 38)
            objects_map['fixed wall 1'] = wall_instance1
            wall_instance2 = Wall()
            wall_instance2.xy = (88, 101)
            wall_instance2.wh = (72, 38)
            objects_map['fixed wall 2'] = wall_instance2
            wall_instance3 = Wall()
            wall_instance3.xy = (8, 101)
            wall_instance3.wh = (64, 38)
            objects_map['fixed wall 3'] = wall_instance3
            number_of_walls = 4
            i = 0
            while (objects_map.get(f"fixed wall {number_of_walls + i}") != None):
                objects_map.pop(f"fixed wall {number_of_walls + i}")
                i += 1
        elif ram_state[28] == 1:
            number_of_lava_walls = 0
            i = 0
            while (objects_map.get(f"lava wall {number_of_lava_walls + i}") != None):
                objects_map.pop(f"lava wall {number_of_lava_walls + i}")
                i += 1
            wall_instance0 = Wall()
            wall_instance0.xy = (88, 21)
            wall_instance0.wh = (72, 38)
            objects_map['fixed wall 0'] = wall_instance0
            wall_instance1 = Wall()
            wall_instance1.xy = (8, 21)
            wall_instance1.wh = (64, 38)
            objects_map['fixed wall 1'] = wall_instance1
            wall_instance2 = Wall()
            wall_instance2.xy = (140, 61)
            wall_instance2.wh = (20, 37)
            objects_map['fixed wall 2'] = wall_instance2
            wall_instance3 = Wall()
            wall_instance3.xy = (8, 61)
            wall_instance3.wh = (12, 37)
            objects_map['fixed wall 3'] = wall_instance3
            wall_instance4 = Wall()
            wall_instance4.xy = (136, 101)
            wall_instance4.wh = (24, 38)
            objects_map['fixed wall 4'] = wall_instance4
            wall_instance5 = Wall()
            wall_instance5.xy = (32, 101)
            wall_instance5.wh = (96, 38)
            objects_map['fixed wall 5'] = wall_instance5
            wall_instance6 = Wall()
            wall_instance6.xy = (8, 101)
            wall_instance6.wh = (16, 38)
            objects_map['fixed wall 6'] = wall_instance6
            number_of_walls = 7
            i = 0
            while (objects_map.get(f"fixed wall {number_of_walls + i}") != None):
                objects_map.pop(f"fixed wall {number_of_walls + i}")
                i += 1
        elif ram_state[28] == 2:
            wall_instance0 = LavaWall()
            wall_instance0.xy = (144, 61)
            wall_instance0.wh = (16, 37)
            objects_map['lava wall 0'] = wall_instance0
            wall_instance1 = LavaWall()
            wall_instance1.xy = (8, 61)
            wall_instance1.wh = (8, 37)
            objects_map['lava wall 1'] = wall_instance1
            number_of_lava_walls = 2
            i = 0
            while (objects_map.get(f"lava wall {number_of_lava_walls + i}") != None):
                objects_map.pop(f"lava wall {number_of_lava_walls + i}")
                i += 1
            wall_instance0 = Wall()
            wall_instance0.xy = (136, 21)
            wall_instance0.wh = (24, 38)
            objects_map['fixed wall 0'] = wall_instance0
            wall_instance1 = Wall()
            wall_instance1.xy = (32, 21)
            wall_instance1.wh = (96, 38)
            objects_map['fixed wall 1'] = wall_instance1
            wall_instance2 = Wall()
            wall_instance2.xy = (8, 21)
            wall_instance2.wh = (16, 38)
            objects_map['fixed wall 2'] = wall_instance2
            wall_instance3 = Wall()
            wall_instance3.xy = (84, 101)
            wall_instance3.wh = (76, 38)
            objects_map['fixed wall 3'] = wall_instance3
            wall_instance4 = Wall()
            wall_instance4.xy = (8, 101)
            wall_instance4.wh = (68, 38)
            objects_map['fixed wall 4'] = wall_instance4
            number_of_walls = 5
            i = 0
            while (objects_map.get(f"fixed wall {number_of_walls + i}") != None):
                objects_map.pop(f"fixed wall {number_of_walls + i}")
                i += 1
        elif ram_state[28] == 3:
            number_of_lava_walls = 0
            i = 0
            while (objects_map.get(f"lava wall {number_of_lava_walls + i}") != None):
                objects_map.pop(f"lava wall {number_of_lava_walls + i}")
                i += 1
            wall_instance0 = Wall()
            wall_instance0.xy = (84, 21)
            wall_instance0.wh = (76, 38)
            objects_map['fixed wall 0'] = wall_instance0
            wall_instance1 = Wall()
            wall_instance1.xy = (8, 21)
            wall_instance1.wh = (68, 38)
            objects_map['fixed wall 1'] = wall_instance1
            wall_instance2 = Wall()
            wall_instance2.xy = (112, 61)
            wall_instance2.wh = (48, 37)
            objects_map['fixed wall 2'] = wall_instance2
            wall_instance3 = Wall()
            wall_instance3.xy = (8, 61)
            wall_instance3.wh = (40, 37)
            objects_map['fixed wall 3'] = wall_instance3
            wall_instance4 = Wall()
            wall_instance4.xy = (108, 101)
            wall_instance4.wh = (52, 38)
            objects_map['fixed wall 4'] = wall_instance4
            wall_instance5 = Wall()
            wall_instance5.xy = (60, 101)
            wall_instance5.wh = (40, 38)
            objects_map['fixed wall 5'] = wall_instance5
            wall_instance6 = Wall()
            wall_instance6.xy = (8, 101)
            wall_instance6.wh = (44, 38)
            objects_map['fixed wall 6'] = wall_instance6
            number_of_walls = 7
            i = 0
            while (objects_map.get(f"fixed wall {number_of_walls + i}") != None):
                objects_map.pop(f"fixed wall {number_of_walls + i}")
                i += 1
        elif ram_state[28] == 4:
            wall_instance0 = LavaWall()
            wall_instance0.xy = (144, 61)
            wall_instance0.wh = (16, 37)
            objects_map['lava wall 0'] = wall_instance0
            wall_instance1 = LavaWall()
            wall_instance1.xy = (64, 61)
            wall_instance1.wh = (48, 37)
            objects_map['lava wall 1'] = wall_instance1
            wall_instance2 = LavaWall()
            wall_instance2.xy = (8, 61)
            wall_instance2.wh = (24, 37)
            objects_map['lava wall 2'] = wall_instance2
            number_of_lava_walls = 3
            i = 0
            while (objects_map.get(f"lava wall {number_of_lava_walls + i}") != None):
                objects_map.pop(f"lava wall {number_of_lava_walls + i}")
                i += 1
            wall_instance0 = Wall()
            wall_instance0.xy = (108, 21)
            wall_instance0.wh = (52, 38)
            objects_map['fixed wall 0'] = wall_instance0
            wall_instance1 = Wall()
            wall_instance1.xy = (60, 21)
            wall_instance1.wh = (40, 38)
            objects_map['fixed wall 1'] = wall_instance1
            wall_instance2 = Wall()
            wall_instance2.xy = (8, 21)
            wall_instance2.wh = (44, 38)
            objects_map['fixed wall 2'] = wall_instance2
            wall_instance3 = Wall()
            wall_instance3.xy = (136, 101)
            wall_instance3.wh = (24, 38)
            objects_map['fixed wall 3'] = wall_instance3
            wall_instance4 = Wall()
            wall_instance4.xy = (40, 101)
            wall_instance4.wh = (80, 38)
            objects_map['fixed wall 4'] = wall_instance4
            wall_instance5 = Wall()
            wall_instance5.xy = (8, 101)
            wall_instance5.wh = (16, 38)
            objects_map['fixed wall 5'] = wall_instance5
            number_of_walls = 6
            i = 0
            while (objects_map.get(f"fixed wall {number_of_walls + i}") != None):
                objects_map.pop(f"fixed wall {number_of_walls + i}")
                i += 1
        elif ram_state[28] == 5:
            number_of_lava_walls = 0
            i = 0
            while (objects_map.get(f"lava wall {number_of_lava_walls + i}") != None):
                objects_map.pop(f"lava wall {number_of_lava_walls + i}")
                i += 1
            wall_instance0 = Wall()
            wall_instance0.xy = (136, 21)
            wall_instance0.wh = (24, 38)
            objects_map['fixed wall 0'] = wall_instance0
            wall_instance1 = Wall()
            wall_instance1.xy = (40, 21)
            wall_instance1.wh = (80, 38)
            objects_map['fixed wall 1'] = wall_instance1
            wall_instance2 = Wall()
            wall_instance2.xy = (8, 21)
            wall_instance2.wh = (16, 38)
            objects_map['fixed wall 2'] = wall_instance2
            wall_instance3 = Wall()
            wall_instance3.xy = (128, 61)
            wall_instance3.wh = (32, 37)
            objects_map['fixed wall 3'] = wall_instance3
            wall_instance4 = Wall()
            wall_instance4.xy = (8, 61)
            wall_instance4.wh = (24, 37)
            objects_map['fixed wall 4'] = wall_instance4
            wall_instance5 = Wall()
            wall_instance5.xy = (144, 101)
            wall_instance5.wh = (16, 38)
            objects_map['fixed wall 5'] = wall_instance5
            wall_instance6 = Wall()
            wall_instance6.xy = (48, 101)
            wall_instance6.wh = (64, 38)
            objects_map['fixed wall 6'] = wall_instance6
            wall_instance7 = Wall()
            wall_instance7.xy = (8, 101)
            wall_instance7.wh = (8, 38)
            objects_map['fixed wall 7'] = wall_instance7
            number_of_walls = 8
            i = 0
            while (objects_map.get(f"fixed wall {number_of_walls + i}") != None):
                objects_map.pop(f"fixed wall {number_of_walls + i}")
                i += 1
        elif ram_state[28] == 6:
            wall_instance0 = LavaWall()
            wall_instance0.xy = (136, 61)
            wall_instance0.wh = (24, 37)
            objects_map['lava wall 0'] = wall_instance0
            wall_instance1 = LavaWall()
            wall_instance1.xy = (56, 61)
            wall_instance1.wh = (64, 37)
            objects_map['lava wall 1'] = wall_instance1
            wall_instance2 = LavaWall()
            wall_instance2.xy = (8, 61)
            wall_instance2.wh = (32, 37)
            objects_map['lava wall 2'] = wall_instance2
            number_of_lava_walls = 3
            i = 0
            while (objects_map.get(f"lava wall {number_of_lava_walls + i}") != None):
                objects_map.pop(f"lava wall {number_of_lava_walls + i}")
                i += 1
            wall_instance0 = Wall()
            wall_instance0.xy = (144, 21)
            wall_instance0.wh = (16, 38)
            objects_map['fixed wall 0'] = wall_instance0
            wall_instance1 = Wall()
            wall_instance1.xy = (48, 21)
            wall_instance1.wh = (64, 38)
            objects_map['fixed wall 1'] = wall_instance1
            wall_instance2 = Wall()
            wall_instance2.xy = (8, 21)
            wall_instance2.wh = (8, 38)
            objects_map['fixed wall 2'] = wall_instance2
            wall_instance3 = Wall()
            wall_instance3.xy = (144, 101)
            wall_instance3.wh = (16, 38)
            objects_map['fixed wall 3'] = wall_instance3
            wall_instance4 = Wall()
            wall_instance4.xy = (36, 101)
            wall_instance4.wh = (88, 38)
            objects_map['fixed wall 4'] = wall_instance4
            wall_instance5 = Wall()
            wall_instance5.xy = (8, 101)
            wall_instance5.wh = (8, 38)
            objects_map['fixed wall 5'] = wall_instance5
            number_of_walls = 6
            i = 0
            while (objects_map.get(f"fixed wall {number_of_walls + i}") != None):
                objects_map.pop(f"fixed wall {number_of_walls + i}")
                i += 1
        elif ram_state[28] == 7:
            number_of_lava_walls = 0
            i = 0
            while (objects_map.get(f"lava wall {number_of_lava_walls + i}") != None):
                objects_map.pop(f"lava wall {number_of_lava_walls + i}")
                i += 1
            wall_instance0 = Wall()
            wall_instance0.xy = (144, 21)
            wall_instance0.wh = (16, 38)
            objects_map['fixed wall 0'] = wall_instance0
            wall_instance1 = Wall()
            wall_instance1.xy = (36, 21)
            wall_instance1.wh = (88, 38)
            objects_map['fixed wall 1'] = wall_instance1
            wall_instance2 = Wall()
            wall_instance2.xy = (8, 21)
            wall_instance2.wh = (8, 38)
            objects_map['fixed wall 2'] = wall_instance2
            wall_instance3 = Wall()
            wall_instance3.xy = (132, 61)
            wall_instance3.wh = (28, 37)
            objects_map['fixed wall 3'] = wall_instance3
            wall_instance4 = Wall()
            wall_instance4.xy = (8, 61)
            wall_instance4.wh = (20, 37)
            objects_map['fixed wall 4'] = wall_instance4
            wall_instance5 = Wall()
            wall_instance5.xy = (88, 101)
            wall_instance5.wh = (72, 38)
            objects_map['fixed wall 5'] = wall_instance5
            wall_instance6 = Wall()
            wall_instance6.xy = (8, 101)
            wall_instance6.wh = (64, 38)
            objects_map['fixed wall 6'] = wall_instance6
            number_of_walls = 7
            i = 0
            while (objects_map.get(f"fixed wall {number_of_walls + i}") != None):
                objects_map.pop(f"fixed wall {number_of_walls + i}")
                i += 1
        elif ram_state[28] == 8:
            wall_instance0 = LavaWall()
            wall_instance0.xy = (132, 61)
            wall_instance0.wh = (28, 37)
            objects_map['lava wall 0'] = wall_instance0
            wall_instance1 = LavaWall()
            wall_instance1.xy = (8, 61)
            wall_instance1.wh = (20, 37)
            objects_map['lava wall 1'] = wall_instance1
            number_of_lava_walls = 2
            i = 0
            while (objects_map.get(f"lava wall {number_of_lava_walls + i}") != None):
                objects_map.pop(f"lava wall {number_of_lava_walls + i}")
                i += 1
            wall_instance0 = Wall()
            wall_instance0.xy = (88, 21)
            wall_instance0.wh = (72, 38)
            objects_map['fixed wall 0'] = wall_instance0
            wall_instance1 = Wall()
            wall_instance1.xy = (8, 21)
            wall_instance1.wh = (64, 38)
            objects_map['fixed wall 1'] = wall_instance1
            wall_instance2 = Wall()
            wall_instance2.xy = (128, 101)
            wall_instance2.wh = (32, 38)
            objects_map['fixed wall 2'] = wall_instance2
            wall_instance3 = Wall()
            wall_instance3.xy = (48, 101)
            wall_instance3.wh = (64, 38)
            objects_map['fixed wall 3'] = wall_instance3
            wall_instance4 = Wall()
            wall_instance4.xy = (8, 101)
            wall_instance4.wh = (24, 38)
            objects_map['fixed wall 4'] = wall_instance4
            number_of_walls = 5
            i = 0
            while (objects_map.get(f"fixed wall {number_of_walls + i}") != None):
                objects_map.pop(f"fixed wall {number_of_walls + i}")
                i += 1
        elif ram_state[28] == 9:
            number_of_lava_walls = 0
            i = 0
            while (objects_map.get(f"lava wall {number_of_lava_walls + i}") != None):
                objects_map.pop(f"lava wall {number_of_lava_walls + i}")
                i += 1
            wall_instance0 = Wall()
            wall_instance0.xy = (128, 21)
            wall_instance0.wh = (32, 38)
            objects_map['fixed wall 0'] = wall_instance0
            wall_instance1 = Wall()
            wall_instance1.xy = (48, 21)
            wall_instance1.wh = (64, 38)
            objects_map['fixed wall 1'] = wall_instance1
            wall_instance2 = Wall()
            wall_instance2.xy = (8, 21)
            wall_instance2.wh = (24, 38)
            objects_map['fixed wall 2'] = wall_instance2
            wall_instance3 = Wall()
            wall_instance3.xy = (136, 61)
            wall_instance3.wh = (24, 37)
            objects_map['fixed wall 3'] = wall_instance3
            wall_instance4 = Wall()
            wall_instance4.xy = (8, 61)
            wall_instance4.wh = (16, 37)
            objects_map['fixed wall 4'] = wall_instance4
            wall_instance5 = Wall()
            wall_instance5.xy = (96, 101)
            wall_instance5.wh = (64, 38)
            objects_map['fixed wall 5'] = wall_instance5
            wall_instance6 = Wall()
            wall_instance6.xy = (72, 101)
            wall_instance6.wh = (16, 38)
            objects_map['fixed wall 6'] = wall_instance6
            wall_instance7 = Wall()
            wall_instance7.xy = (8, 101)
            wall_instance7.wh = (56, 38)
            objects_map['fixed wall 7'] = wall_instance7
            number_of_walls = 8
            i = 0
            while (objects_map.get(f"fixed wall {number_of_walls + i}") != None):
                objects_map.pop(f"fixed wall {number_of_walls + i}")
                i += 1
        elif ram_state[28] == 10:
            number_of_lava_walls = 0
            i = 0
            while (objects_map.get(f"lava wall {number_of_lava_walls + i}") != None):
                objects_map.pop(f"lava wall {number_of_lava_walls + i}")
                i += 1
            wall_instance0 = Wall()
            wall_instance0.xy = (96, 21)
            wall_instance0.wh = (64, 38)
            objects_map['fixed wall 0'] = wall_instance0
            wall_instance1 = Wall()
            wall_instance1.xy = (72, 21)
            wall_instance1.wh = (16, 38)
            objects_map['fixed wall 1'] = wall_instance1
            wall_instance2 = Wall()
            wall_instance2.xy = (8, 21)
            wall_instance2.wh = (56, 38)
            objects_map['fixed wall 2'] = wall_instance2
            wall_instance3 = Wall()
            wall_instance3.xy = (128, 101)
            wall_instance3.wh = (32, 38)
            objects_map['fixed wall 3'] = wall_instance3
            wall_instance4 = Wall()
            wall_instance4.xy = (8, 101)
            wall_instance4.wh = (24, 38)
            objects_map['fixed wall 4'] = wall_instance4
            number_of_walls = 5
            i = 0
            while (objects_map.get(f"fixed wall {number_of_walls + i}") != None):
                objects_map.pop(f"fixed wall {number_of_walls + i}")
                i += 1
        elif ram_state[28] == 11:
            number_of_lava_walls = 0
            i = 0
            while (objects_map.get(f"lava wall {number_of_lava_walls + i}") != None):
                objects_map.pop(f"lava wall {number_of_lava_walls + i}")
                i += 1
            wall_instance0 = Wall()
            wall_instance0.xy = (8, 21)
            wall_instance0.wh = (152, 38)
            objects_map['fixed wall 0'] = wall_instance0
            wall_instance1 = Wall()
            wall_instance1.xy = (8, 101)
            wall_instance1.wh = (152, 38)
            objects_map['fixed wall 1'] = wall_instance1
            number_of_walls = 2
            i = 0
            while (objects_map.get(f"fixed wall {number_of_walls + i}") != None):
                objects_map.pop(f"fixed wall {number_of_walls + i}")
                i += 1

    elif ram_state[117] == 7:
        if ram_state[28] == 0:
            wall_instance0 = LavaWall()
            wall_instance0.xy = (140, 61)
            wall_instance0.wh = (20, 37)
            objects_map['lava wall 0'] = wall_instance0
            wall_instance1 = LavaWall()
            wall_instance1.xy = (8, 61)
            wall_instance1.wh = (12, 37)
            objects_map['lava wall 1'] = wall_instance1
            number_of_lava_walls = 2
            i = 0
            while (objects_map.get(f"lava wall {number_of_lava_walls + i}") != None):
                objects_map.pop(f"lava wall {number_of_lava_walls + i}")
                i += 1
            wall_instance0 = Wall()
            wall_instance0.xy = (136, 21)
            wall_instance0.wh = (24, 38)
            objects_map['fixed wall 0'] = wall_instance0
            wall_instance1 = Wall()
            wall_instance1.xy = (8, 21)
            wall_instance1.wh = (16, 38)
            objects_map['fixed wall 1'] = wall_instance1
            wall_instance2 = Wall()
            wall_instance2.xy = (88, 101)
            wall_instance2.wh = (72, 38)
            objects_map['fixed wall 2'] = wall_instance2
            wall_instance3 = Wall()
            wall_instance3.xy = (8, 101)
            wall_instance3.wh = (64, 38)
            objects_map['fixed wall 3'] = wall_instance3
            number_of_walls = 4
            i = 0
            while (objects_map.get(f"fixed wall {number_of_walls + i}") != None):
                objects_map.pop(f"fixed wall {number_of_walls + i}")
                i += 1
        elif ram_state[28] == 1:
            wall_instance0 = LavaWall()
            wall_instance0.xy = (144, 61)
            wall_instance0.wh = (16, 37)
            objects_map['lava wall 0'] = wall_instance0
            wall_instance1 = LavaWall()
            wall_instance1.xy = (8, 61)
            wall_instance1.wh = (8, 37)
            objects_map['lava wall 1'] = wall_instance1
            number_of_lava_walls = 2
            i = 0
            while (objects_map.get(f"lava wall {number_of_lava_walls + i}") != None):
                objects_map.pop(f"lava wall {number_of_lava_walls + i}")
                i += 1
            wall_instance0 = Wall()
            wall_instance0.xy = (88, 21)
            wall_instance0.wh = (72, 38)
            objects_map['fixed wall 0'] = wall_instance0
            wall_instance1 = Wall()
            wall_instance1.xy = (8, 21)
            wall_instance1.wh = (64, 38)
            objects_map['fixed wall 1'] = wall_instance1
            wall_instance2 = Wall()
            wall_instance2.xy = (112, 101)
            wall_instance2.wh = (48, 38)
            objects_map['fixed wall 2'] = wall_instance2
            wall_instance3 = Wall()
            wall_instance3.xy = (8, 101)
            wall_instance3.wh = (40, 38)
            objects_map['fixed wall 3'] = wall_instance3
            number_of_walls = 4
            i = 0
            while (objects_map.get(f"fixed wall {number_of_walls + i}") != None):
                objects_map.pop(f"fixed wall {number_of_walls + i}")
                i += 1
        elif ram_state[28] == 2:
            wall_instance0 = LavaWall()
            wall_instance0.xy = (92, 61)
            wall_instance0.wh = (68, 37)
            objects_map['lava wall 0'] = wall_instance0
            wall_instance1 = LavaWall()
            wall_instance1.xy = (8, 61)
            wall_instance1.wh = (60, 37)
            objects_map['lava wall 1'] = wall_instance1
            number_of_lava_walls = 2
            i = 0
            while (objects_map.get(f"lava wall {number_of_lava_walls + i}") != None):
                objects_map.pop(f"lava wall {number_of_lava_walls + i}")
                i += 1
            wall_instance0 = Wall()
            wall_instance0.xy = (112, 21)
            wall_instance0.wh = (48, 38)
            objects_map['fixed wall 0'] = wall_instance0
            wall_instance1 = Wall()
            wall_instance1.xy = (8, 21)
            wall_instance1.wh = (40, 38)
            objects_map['fixed wall 1'] = wall_instance1
            wall_instance2 = Wall()
            wall_instance2.xy = (88, 101)
            wall_instance2.wh = (72, 38)
            objects_map['fixed wall 2'] = wall_instance2
            wall_instance3 = Wall()
            wall_instance3.xy = (8, 101)
            wall_instance3.wh = (64, 38)
            objects_map['fixed wall 3'] = wall_instance3
            number_of_walls = 4
            i = 0
            while (objects_map.get(f"fixed wall {number_of_walls + i}") != None):
                objects_map.pop(f"fixed wall {number_of_walls + i}")
                i += 1
        elif ram_state[28] == 3:
            wall_instance0 = LavaWall()
            wall_instance0.xy = (144, 61)
            wall_instance0.wh = (16, 37)
            objects_map['lava wall 0'] = wall_instance0
            wall_instance1 = LavaWall()
            wall_instance1.xy = (8, 61)
            wall_instance1.wh = (8, 37)
            objects_map['lava wall 1'] = wall_instance1
            number_of_lava_walls = 2
            i = 0
            while (objects_map.get(f"lava wall {number_of_lava_walls + i}") != None):
                objects_map.pop(f"lava wall {number_of_lava_walls + i}")
                i += 1
            wall_instance0 = Wall()
            wall_instance0.xy = (88, 21)
            wall_instance0.wh = (72, 38)
            objects_map['fixed wall 0'] = wall_instance0
            wall_instance1 = Wall()
            wall_instance1.xy = (8, 21)
            wall_instance1.wh = (64, 38)
            objects_map['fixed wall 1'] = wall_instance1
            wall_instance2 = Wall()
            wall_instance2.xy = (112, 101)
            wall_instance2.wh = (48, 38)
            objects_map['fixed wall 2'] = wall_instance2
            wall_instance3 = Wall()
            wall_instance3.xy = (56, 101)
            wall_instance3.wh = (48, 38)
            objects_map['fixed wall 3'] = wall_instance3
            wall_instance4 = Wall()
            wall_instance4.xy = (8, 101)
            wall_instance4.wh = (40, 38)
            objects_map['fixed wall 4'] = wall_instance4
            number_of_walls = 5
            i = 0
            while (objects_map.get(f"fixed wall {number_of_walls + i}") != None):
                objects_map.pop(f"fixed wall {number_of_walls + i}")
                i += 1
        elif ram_state[28] == 4:
            wall_instance0 = LavaWall()
            wall_instance0.xy = (124, 61)
            wall_instance0.wh = (36, 37)
            objects_map['lava wall 0'] = wall_instance0
            wall_instance1 = LavaWall()
            wall_instance1.xy = (60, 61)
            wall_instance1.wh = (40, 37)
            objects_map['lava wall 1'] = wall_instance1
            wall_instance2 = LavaWall()
            wall_instance2.xy = (8, 61)
            wall_instance2.wh = (28, 37)
            objects_map['lava wall 2'] = wall_instance2
            number_of_lava_walls = 3
            i = 0
            while (objects_map.get(f"lava wall {number_of_lava_walls + i}") != None):
                objects_map.pop(f"lava wall {number_of_lava_walls + i}")
                i += 1
            wall_instance0 = Wall()
            wall_instance0.xy = (112, 21)
            wall_instance0.wh = (48, 38)
            objects_map['fixed wall 0'] = wall_instance0
            wall_instance1 = Wall()
            wall_instance1.xy = (56, 21)
            wall_instance1.wh = (48, 38)
            objects_map['fixed wall 1'] = wall_instance1
            wall_instance2 = Wall()
            wall_instance2.xy = (8, 21)
            wall_instance2.wh = (40, 38)
            objects_map['fixed wall 2'] = wall_instance2
            wall_instance3 = Wall()
            wall_instance3.xy = (128, 101)
            wall_instance3.wh = (32, 38)
            objects_map['fixed wall 3'] = wall_instance3
            wall_instance4 = Wall()
            wall_instance4.xy = (52, 101)
            wall_instance4.wh = (56, 38)
            objects_map['fixed wall 4'] = wall_instance4
            wall_instance5 = Wall()
            wall_instance5.xy = (8, 101)
            wall_instance5.wh = (24, 38)
            objects_map['fixed wall 5'] = wall_instance5
            number_of_walls = 6
            i = 0
            while (objects_map.get(f"fixed wall {number_of_walls + i}") != None):
                objects_map.pop(f"fixed wall {number_of_walls + i}")
                i += 1
        elif ram_state[28] == 5:
            wall_instance0 = LavaWall()
            wall_instance0.xy = (124, 61)
            wall_instance0.wh = (36, 37)
            objects_map['lava wall 0'] = wall_instance0
            wall_instance1 = LavaWall()
            wall_instance1.xy = (8, 61)
            wall_instance1.wh = (28, 37)
            objects_map['lava wall 1'] = wall_instance1
            number_of_lava_walls = 2
            i = 0
            while (objects_map.get(f"lava wall {number_of_lava_walls + i}") != None):
                objects_map.pop(f"lava wall {number_of_lava_walls + i}")
                i += 1
            wall_instance0 = Wall()
            wall_instance0.xy = (128, 21)
            wall_instance0.wh = (32, 38)
            objects_map['fixed wall 0'] = wall_instance0
            wall_instance1 = Wall()
            wall_instance1.xy = (52, 21)
            wall_instance1.wh = (56, 38)
            objects_map['fixed wall 1'] = wall_instance1
            wall_instance2 = Wall()
            wall_instance2.xy = (8, 21)
            wall_instance2.wh = (24, 38)
            objects_map['fixed wall 2'] = wall_instance2
            wall_instance3 = Wall()
            wall_instance3.xy = (88, 101)
            wall_instance3.wh = (72, 38)
            objects_map['fixed wall 3'] = wall_instance3
            wall_instance4 = Wall()
            wall_instance4.xy = (8, 101)
            wall_instance4.wh = (64, 38)
            objects_map['fixed wall 4'] = wall_instance4
            number_of_walls = 5
            i = 0
            while (objects_map.get(f"fixed wall {number_of_walls + i}") != None):
                objects_map.pop(f"fixed wall {number_of_walls + i}")
                i += 1
        elif ram_state[28] == 6:
            wall_instance0 = LavaWall()
            wall_instance0.xy = (144, 61)
            wall_instance0.wh = (16, 37)
            objects_map['lava wall 0'] = wall_instance0
            wall_instance1 = LavaWall()
            wall_instance1.xy = (8, 61)
            wall_instance1.wh = (8, 37)
            objects_map['lava wall 1'] = wall_instance1
            number_of_lava_walls = 2
            i = 0
            while (objects_map.get(f"lava wall {number_of_lava_walls + i}") != None):
                objects_map.pop(f"lava wall {number_of_lava_walls + i}")
                i += 1
            wall_instance0 = Wall()
            wall_instance0.xy = (88, 21)
            wall_instance0.wh = (72, 38)
            objects_map['fixed wall 0'] = wall_instance0
            wall_instance1 = Wall()
            wall_instance1.xy = (8, 21)
            wall_instance1.wh = (64, 38)
            objects_map['fixed wall 1'] = wall_instance1
            wall_instance2 = Wall()
            wall_instance2.xy = (136, 101)
            wall_instance2.wh = (24, 38)
            objects_map['fixed wall 2'] = wall_instance2
            wall_instance3 = Wall()
            wall_instance3.xy = (32, 101)
            wall_instance3.wh = (96, 38)
            objects_map['fixed wall 3'] = wall_instance3
            wall_instance4 = Wall()
            wall_instance4.xy = (8, 101)
            wall_instance4.wh = (16, 38)
            objects_map['fixed wall 4'] = wall_instance4
            number_of_walls = 5
            i = 0
            while (objects_map.get(f"fixed wall {number_of_walls + i}") != None):
                objects_map.pop(f"fixed wall {number_of_walls + i}")
                i += 1
        elif ram_state[28] == 7:
            wall_instance0 = LavaWall()
            wall_instance0.xy = (144, 61)
            wall_instance0.wh = (16, 37)
            objects_map['lava wall 0'] = wall_instance0
            wall_instance1 = LavaWall()
            wall_instance1.xy = (64, 61)
            wall_instance1.wh = (32, 37)
            objects_map['lava wall 1'] = wall_instance1
            wall_instance2 = LavaWall()
            wall_instance2.xy = (8, 61)
            wall_instance2.wh = (8, 37)
            objects_map['lava wall 2'] = wall_instance2
            number_of_lava_walls = 3
            i = 0
            while (objects_map.get(f"lava wall {number_of_lava_walls + i}") != None):
                objects_map.pop(f"lava wall {number_of_lava_walls + i}")
                i += 1
            wall_instance0 = Wall()
            wall_instance0.xy = (136, 21)
            wall_instance0.wh = (24, 38)
            objects_map['fixed wall 0'] = wall_instance0
            wall_instance1 = Wall()
            wall_instance1.xy = (32, 21)
            wall_instance1.wh = (96, 38)
            objects_map['fixed wall 1'] = wall_instance1
            wall_instance2 = Wall()
            wall_instance2.xy = (8, 21)
            wall_instance2.wh = (16, 38)
            objects_map['fixed wall 2'] = wall_instance2
            wall_instance3 = Wall()
            wall_instance3.xy = (112, 101)
            wall_instance3.wh = (48, 38)
            objects_map['fixed wall 3'] = wall_instance3
            wall_instance4 = Wall()
            wall_instance4.xy = (56, 101)
            wall_instance4.wh = (48, 38)
            objects_map['fixed wall 4'] = wall_instance4
            wall_instance5 = Wall()
            wall_instance5.xy = (8, 101)
            wall_instance5.wh = (40, 38)
            objects_map['fixed wall 5'] = wall_instance5
            number_of_walls = 6
            i = 0
            while (objects_map.get(f"fixed wall {number_of_walls + i}") != None):
                objects_map.pop(f"fixed wall {number_of_walls + i}")
                i += 1
        elif ram_state[28] == 8:
            wall_instance0 = LavaWall()
            wall_instance0.xy = (132, 61)
            wall_instance0.wh = (28, 37)
            objects_map['lava wall 0'] = wall_instance0
            wall_instance1 = LavaWall()
            wall_instance1.xy = (72, 61)
            wall_instance1.wh = (16, 37)
            objects_map['lava wall 1'] = wall_instance1
            wall_instance2 = LavaWall()
            wall_instance2.xy = (8, 61)
            wall_instance2.wh = (20, 37)
            objects_map['lava wall 2'] = wall_instance2
            number_of_lava_walls = 3
            i = 0
            while (objects_map.get(f"lava wall {number_of_lava_walls + i}") != None):
                objects_map.pop(f"lava wall {number_of_lava_walls + i}")
                i += 1
            wall_instance0 = Wall()
            wall_instance0.xy = (112, 21)
            wall_instance0.wh = (48, 38)
            objects_map['fixed wall 0'] = wall_instance0
            wall_instance1 = Wall()
            wall_instance1.xy = (56, 21)
            wall_instance1.wh = (48, 38)
            objects_map['fixed wall 1'] = wall_instance1
            wall_instance2 = Wall()
            wall_instance2.xy = (8, 21)
            wall_instance2.wh = (40, 38)
            objects_map['fixed wall 2'] = wall_instance2
            wall_instance3 = Wall()
            wall_instance3.xy = (144, 101)
            wall_instance3.wh = (16, 38)
            objects_map['fixed wall 3'] = wall_instance3
            wall_instance4 = Wall()
            wall_instance4.xy = (56, 101)
            wall_instance4.wh = (48, 38)
            objects_map['fixed wall 4'] = wall_instance4
            wall_instance5 = Wall()
            wall_instance5.xy = (8, 101)
            wall_instance5.wh = (8, 38)
            objects_map['fixed wall 5'] = wall_instance5
            number_of_walls = 6
            i = 0
            while (objects_map.get(f"fixed wall {number_of_walls + i}") != None):
                objects_map.pop(f"fixed wall {number_of_walls + i}")
                i += 1
        elif ram_state[28] == 9:
            wall_instance0 = LavaWall()
            wall_instance0.xy = (128, 61)
            wall_instance0.wh = (32, 37)
            objects_map['lava wall 0'] = wall_instance0
            wall_instance1 = LavaWall()
            wall_instance1.xy = (48, 61)
            wall_instance1.wh = (64, 37)
            objects_map['lava wall 1'] = wall_instance1
            wall_instance2 = LavaWall()
            wall_instance2.xy = (8, 61)
            wall_instance2.wh = (24, 37)
            objects_map['lava wall 2'] = wall_instance2
            number_of_lava_walls = 3
            i = 0
            while (objects_map.get(f"lava wall {number_of_lava_walls + i}") != None):
                objects_map.pop(f"lava wall {number_of_lava_walls + i}")
                i += 1
            wall_instance0 = Wall()
            wall_instance0.xy = (144, 21)
            wall_instance0.wh = (16, 38)
            objects_map['fixed wall 0'] = wall_instance0
            wall_instance1 = Wall()
            wall_instance1.xy = (56, 21)
            wall_instance1.wh = (48, 38)
            objects_map['fixed wall 1'] = wall_instance1
            wall_instance2 = Wall()
            wall_instance2.xy = (8, 21)
            wall_instance2.wh = (8, 38)
            objects_map['fixed wall 2'] = wall_instance2
            wall_instance3 = Wall()
            wall_instance3.xy = (136, 101)
            wall_instance3.wh = (24, 38)
            objects_map['fixed wall 3'] = wall_instance3
            wall_instance4 = Wall()
            wall_instance4.xy = (64, 101)
            wall_instance4.wh = (32, 38)
            objects_map['fixed wall 4'] = wall_instance4
            wall_instance5 = Wall()
            wall_instance5.xy = (8, 101)
            wall_instance5.wh = (16, 38)
            objects_map['fixed wall 5'] = wall_instance5
            number_of_walls = 6
            i = 0
            while (objects_map.get(f"fixed wall {number_of_walls + i}") != None):
                objects_map.pop(f"fixed wall {number_of_walls + i}")
                i += 1
        elif ram_state[28] == 10:
            number_of_lava_walls = 0
            i = 0
            while (objects_map.get(f"lava wall {number_of_lava_walls + i}") != None):
                objects_map.pop(f"lava wall {number_of_lava_walls + i}")
                i += 1
            wall_instance0 = Wall()
            wall_instance0.xy = (136, 21)
            wall_instance0.wh = (24, 38)
            objects_map['fixed wall 0'] = wall_instance0
            wall_instance1 = Wall()
            wall_instance1.xy = (64, 21)
            wall_instance1.wh = (32, 38)
            objects_map['fixed wall 1'] = wall_instance1
            wall_instance2 = Wall()
            wall_instance2.xy = (8, 21)
            wall_instance2.wh = (16, 38)
            objects_map['fixed wall 2'] = wall_instance2
            wall_instance3 = Wall()
            wall_instance3.xy = (120, 101)
            wall_instance3.wh = (40, 38)
            objects_map['fixed wall 3'] = wall_instance3
            wall_instance4 = Wall()
            wall_instance4.xy = (8, 101)
            wall_instance4.wh = (32, 38)
            objects_map['fixed wall 4'] = wall_instance4
            number_of_walls = 5
            i = 0
            while (objects_map.get(f"fixed wall {number_of_walls + i}") != None):
                objects_map.pop(f"fixed wall {number_of_walls + i}")
                i += 1
        elif ram_state[28] == 11:
            number_of_lava_walls = 0
            i = 0
            while (objects_map.get(f"lava wall {number_of_lava_walls + i}") != None):
                objects_map.pop(f"lava wall {number_of_lava_walls + i}")
                i += 1
            wall_instance0 = Wall()
            wall_instance0.xy = (8, 21)
            wall_instance0.wh = (152, 38)
            objects_map['fixed wall 0'] = wall_instance0
            wall_instance1 = Wall()
            wall_instance1.xy = (56, 61)
            wall_instance1.wh = (48, 37)
            objects_map['fixed wall 1'] = wall_instance1
            wall_instance2 = Wall()
            wall_instance2.xy = (116, 101)
            wall_instance2.wh = (44, 38)
            objects_map['fixed wall 2'] = wall_instance2
            wall_instance3 = Wall()
            wall_instance3.xy = (8, 101)
            wall_instance3.wh = (36, 38)
            objects_map['fixed wall 3'] = wall_instance3
            number_of_walls = 4
            i = 0
            while (objects_map.get(f"fixed wall {number_of_walls + i}") != None):
                objects_map.pop(f"fixed wall {number_of_walls + i}")
                i += 1
        elif ram_state[28] == 12:
            number_of_lava_walls = 0
            i = 0
            while (objects_map.get(f"lava wall {number_of_lava_walls + i}") != None):
                objects_map.pop(f"lava wall {number_of_lava_walls + i}")
                i += 1
            wall_instance0 = Wall()
            wall_instance0.xy = (8, 21)
            wall_instance0.wh = (152, 38)
            objects_map['fixed wall 0'] = wall_instance0
            wall_instance1 = Wall()
            wall_instance1.xy = (128, 101)
            wall_instance1.wh = (32, 38)
            objects_map['fixed wall 1'] = wall_instance1
            wall_instance2 = Wall()
            wall_instance2.xy = (72, 101)
            wall_instance2.wh = (16, 38)
            objects_map['fixed wall 2'] = wall_instance2
            wall_instance3 = Wall()
            wall_instance3.xy = (8, 101)
            wall_instance3.wh = (24, 38)
            objects_map['fixed wall 3'] = wall_instance3
            number_of_walls = 4
            i = 0
            while (objects_map.get(f"fixed wall {number_of_walls + i}") != None):
                objects_map.pop(f"fixed wall {number_of_walls + i}")
                i += 1
        elif ram_state[28] == 13:
            number_of_lava_walls = 0
            i = 0
            while (objects_map.get(f"lava wall {number_of_lava_walls + i}") != None):
                objects_map.pop(f"lava wall {number_of_lava_walls + i}")
                i += 1
            wall_instance0 = Wall()
            wall_instance0.xy = (8, 21)
            wall_instance0.wh = (152, 38)
            objects_map['fixed wall 0'] = wall_instance0
            wall_instance1 = Wall()
            wall_instance1.xy = (8, 101)
            wall_instance1.wh = (152, 38)
            objects_map['fixed wall 1'] = wall_instance1
            number_of_walls = 2
            i = 0
            while (objects_map.get(f"fixed wall {number_of_walls + i}") != None):
                objects_map.pop(f"fixed wall {number_of_walls + i}")
                i += 1

    elif ram_state[117] == 8:
        if ram_state[28] == 0:
            wall_instance0 = LavaWall()
            wall_instance0.xy = (144, 61)
            wall_instance0.wh = (16, 37)
            objects_map['lava wall 0'] = wall_instance0
            wall_instance1 = LavaWall()
            wall_instance1.xy = (8, 61)
            wall_instance1.wh = (8, 37)
            objects_map['lava wall 1'] = wall_instance1
            number_of_lava_walls = 2
            i = 0
            while (objects_map.get(f"lava wall {number_of_lava_walls + i}") != None):
                objects_map.pop(f"lava wall {number_of_lava_walls + i}")
                i += 1
            wall_instance0 = Wall()
            wall_instance0.xy = (136, 21)
            wall_instance0.wh = (24, 38)
            objects_map['fixed wall 0'] = wall_instance0
            wall_instance1 = Wall()
            wall_instance1.xy = (8, 21)
            wall_instance1.wh = (16, 38)
            objects_map['fixed wall 1'] = wall_instance1
            wall_instance2 = Wall()
            wall_instance2.xy = (88, 101)
            wall_instance2.wh = (72, 38)
            objects_map['fixed wall 2'] = wall_instance2
            wall_instance3 = Wall()
            wall_instance3.xy = (8, 101)
            wall_instance3.wh = (64, 38)
            objects_map['fixed wall 3'] = wall_instance3
            number_of_walls = 4
            i = 0
            while (objects_map.get(f"fixed wall {number_of_walls + i}") != None):
                objects_map.pop(f"fixed wall {number_of_walls + i}")
                i += 1
        elif ram_state[28] == 1:
            wall_instance0 = LavaWall()
            wall_instance0.xy = (144, 61)
            wall_instance0.wh = (16, 37)
            objects_map['lava wall 0'] = wall_instance0
            wall_instance1 = LavaWall()
            wall_instance1.xy = (8, 61)
            wall_instance1.wh = (8, 37)
            objects_map['lava wall 1'] = wall_instance1
            number_of_lava_walls = 2
            i = 0
            while (objects_map.get(f"lava wall {number_of_lava_walls + i}") != None):
                objects_map.pop(f"lava wall {number_of_lava_walls + i}")
                i += 1
            wall_instance0 = Wall()
            wall_instance0.xy = (88, 21)
            wall_instance0.wh = (72, 38)
            objects_map['fixed wall 0'] = wall_instance0
            wall_instance1 = Wall()
            wall_instance1.xy = (8, 21)
            wall_instance1.wh = (64, 38)
            objects_map['fixed wall 1'] = wall_instance1
            wall_instance2 = Wall()
            wall_instance2.xy = (136, 101)
            wall_instance2.wh = (24, 38)
            objects_map['fixed wall 2'] = wall_instance2
            wall_instance3 = Wall()
            wall_instance3.xy = (40, 101)
            wall_instance3.wh = (80, 38)
            objects_map['fixed wall 3'] = wall_instance3
            wall_instance4 = Wall()
            wall_instance4.xy = (8, 101)
            wall_instance4.wh = (16, 38)
            objects_map['fixed wall 4'] = wall_instance4
            number_of_walls = 5
            i = 0
            while (objects_map.get(f"fixed wall {number_of_walls + i}") != None):
                objects_map.pop(f"fixed wall {number_of_walls + i}")
                i += 1
        elif ram_state[28] == 2:
            wall_instance0 = LavaWall()
            wall_instance0.xy = (140, 61)
            wall_instance0.wh = (20, 37)
            objects_map['lava wall 0'] = wall_instance0
            wall_instance1 = LavaWall()
            wall_instance1.xy = (44, 61)
            wall_instance1.wh = (72, 37)
            objects_map['lava wall 1'] = wall_instance1
            wall_instance2 = LavaWall()
            wall_instance2.xy = (8, 61)
            wall_instance2.wh = (12, 37)
            objects_map['lava wall 2'] = wall_instance2
            number_of_lava_walls = 3
            i = 0
            while (objects_map.get(f"lava wall {number_of_lava_walls + i}") != None):
                objects_map.pop(f"lava wall {number_of_lava_walls + i}")
                i += 1
            wall_instance0 = Wall()
            wall_instance0.xy = (136, 21)
            wall_instance0.wh = (24, 38)
            objects_map['fixed wall 0'] = wall_instance0
            wall_instance1 = Wall()
            wall_instance1.xy = (40, 21)
            wall_instance1.wh = (80, 38)
            objects_map['fixed wall 1'] = wall_instance1
            wall_instance2 = Wall()
            wall_instance2.xy = (8, 21)
            wall_instance2.wh = (16, 38)
            objects_map['fixed wall 2'] = wall_instance2
            wall_instance3 = Wall()
            wall_instance3.xy = (136, 101)
            wall_instance3.wh = (24, 38)
            objects_map['fixed wall 3'] = wall_instance3
            wall_instance4 = Wall()
            wall_instance4.xy = (8, 101)
            wall_instance4.wh = (16, 38)
            objects_map['fixed wall 4'] = wall_instance4
            number_of_walls = 5
            i = 0
            while (objects_map.get(f"fixed wall {number_of_walls + i}") != None):
                objects_map.pop(f"fixed wall {number_of_walls + i}")
                i += 1
        elif ram_state[28] == 3:
            wall_instance0 = LavaWall()
            wall_instance0.xy = (128, 61)
            wall_instance0.wh = (32, 37)
            objects_map['lava wall 0'] = wall_instance0
            wall_instance1 = LavaWall()
            wall_instance1.xy = (44, 61)
            wall_instance1.wh = (72, 37)
            objects_map['lava wall 1'] = wall_instance1
            wall_instance2 = LavaWall()
            wall_instance2.xy = (8, 61)
            wall_instance2.wh = (24, 37)
            objects_map['lava wall 2'] = wall_instance2
            number_of_lava_walls = 3
            i = 0
            while (objects_map.get(f"lava wall {number_of_lava_walls + i}") != None):
                objects_map.pop(f"lava wall {number_of_lava_walls + i}")
                i += 1
            wall_instance0 = Wall()
            wall_instance0.xy = (136, 21)
            wall_instance0.wh = (24, 38)
            objects_map['fixed wall 0'] = wall_instance0
            wall_instance1 = Wall()
            wall_instance1.xy = (8, 21)
            wall_instance1.wh = (16, 38)
            objects_map['fixed wall 1'] = wall_instance1
            wall_instance2 = Wall()
            wall_instance2.xy = (136, 101)
            wall_instance2.wh = (24, 38)
            objects_map['fixed wall 2'] = wall_instance2
            wall_instance3 = Wall()
            wall_instance3.xy = (8, 101)
            wall_instance3.wh = (16, 38)
            objects_map['fixed wall 3'] = wall_instance3
            number_of_walls = 4
            i = 0
            while (objects_map.get(f"fixed wall {number_of_walls + i}") != None):
                objects_map.pop(f"fixed wall {number_of_walls + i}")
                i += 1
        elif ram_state[28] == 4:
            wall_instance0 = LavaWall()
            wall_instance0.xy = (116, 61)
            wall_instance0.wh = (44, 37)
            objects_map['lava wall 0'] = wall_instance0
            wall_instance1 = LavaWall()
            wall_instance1.xy = (56, 61)
            wall_instance1.wh = (48, 37)
            objects_map['lava wall 1'] = wall_instance1
            wall_instance2 = LavaWall()
            wall_instance2.xy = (8, 61)
            wall_instance2.wh = (36, 37)
            objects_map['lava wall 2'] = wall_instance2
            number_of_lava_walls = 3
            i = 0
            while (objects_map.get(f"lava wall {number_of_lava_walls + i}") != None):
                objects_map.pop(f"lava wall {number_of_lava_walls + i}")
                i += 1
            wall_instance0 = Wall()
            wall_instance0.xy = (136, 21)
            wall_instance0.wh = (24, 38)
            objects_map['fixed wall 0'] = wall_instance0
            wall_instance1 = Wall()
            wall_instance1.xy = (8, 21)
            wall_instance1.wh = (16, 38)
            objects_map['fixed wall 1'] = wall_instance1
            wall_instance2 = Wall()
            wall_instance2.xy = (136, 101)
            wall_instance2.wh = (24, 38)
            objects_map['fixed wall 2'] = wall_instance2
            wall_instance3 = Wall()
            wall_instance3.xy = (8, 101)
            wall_instance3.wh = (16, 38)
            objects_map['fixed wall 3'] = wall_instance3
            number_of_walls = 4
            i = 0
            while (objects_map.get(f"fixed wall {number_of_walls + i}") != None):
                objects_map.pop(f"fixed wall {number_of_walls + i}")
                i += 1
        elif ram_state[28] == 5:
            wall_instance0 = LavaWall()
            wall_instance0.xy = (108, 61)
            wall_instance0.wh = (52, 37)
            objects_map['lava wall 0'] = wall_instance0
            wall_instance1 = LavaWall()
            wall_instance1.xy = (64, 61)
            wall_instance1.wh = (32, 37)
            objects_map['lava wall 1'] = wall_instance1
            wall_instance2 = LavaWall()
            wall_instance2.xy = (8, 61)
            wall_instance2.wh = (44, 37)
            objects_map['lava wall 2'] = wall_instance2
            number_of_lava_walls = 3
            i = 0
            while (objects_map.get(f"lava wall {number_of_lava_walls + i}") != None):
                objects_map.pop(f"lava wall {number_of_lava_walls + i}")
                i += 1
            wall_instance0 = Wall()
            wall_instance0.xy = (136, 21)
            wall_instance0.wh = (24, 38)
            objects_map['fixed wall 0'] = wall_instance0
            wall_instance1 = Wall()
            wall_instance1.xy = (8, 21)
            wall_instance1.wh = (16, 38)
            objects_map['fixed wall 1'] = wall_instance1
            wall_instance2 = Wall()
            wall_instance2.xy = (136, 101)
            wall_instance2.wh = (24, 38)
            objects_map['fixed wall 2'] = wall_instance2
            wall_instance3 = Wall()
            wall_instance3.xy = (8, 101)
            wall_instance3.wh = (16, 38)
            objects_map['fixed wall 3'] = wall_instance3
            number_of_walls = 4
            i = 0
            while (objects_map.get(f"fixed wall {number_of_walls + i}") != None):
                objects_map.pop(f"fixed wall {number_of_walls + i}")
                i += 1
        elif ram_state[28] == 6:
            wall_instance0 = LavaWall()
            wall_instance0.xy = (108, 61)
            wall_instance0.wh = (52, 37)
            objects_map['lava wall 0'] = wall_instance0
            wall_instance1 = LavaWall()
            wall_instance1.xy = (8, 61)
            wall_instance1.wh = (44, 37)
            objects_map['lava wall 1'] = wall_instance1
            number_of_lava_walls = 2
            i = 0
            while (objects_map.get(f"lava wall {number_of_lava_walls + i}") != None):
                objects_map.pop(f"lava wall {number_of_lava_walls + i}")
                i += 1
            wall_instance0 = Wall()
            wall_instance0.xy = (136, 21)
            wall_instance0.wh = (24, 38)
            objects_map['fixed wall 0'] = wall_instance0
            wall_instance1 = Wall()
            wall_instance1.xy = (8, 21)
            wall_instance1.wh = (16, 38)
            objects_map['fixed wall 1'] = wall_instance1
            wall_instance2 = Wall()
            wall_instance2.xy = (104, 101)
            wall_instance2.wh = (56, 38)
            objects_map['fixed wall 2'] = wall_instance2
            wall_instance3 = Wall()
            wall_instance3.xy = (72, 101)
            wall_instance3.wh = (16, 38)
            objects_map['fixed wall 3'] = wall_instance3
            wall_instance4 = Wall()
            wall_instance4.xy = (8, 101)
            wall_instance4.wh = (48, 38)
            objects_map['fixed wall 4'] = wall_instance4
            number_of_walls = 5
            i = 0
            while (objects_map.get(f"fixed wall {number_of_walls + i}") != None):
                objects_map.pop(f"fixed wall {number_of_walls + i}")
                i += 1
        elif ram_state[28] == 7:
            wall_instance0 = LavaWall()
            wall_instance0.xy = (144, 61)
            wall_instance0.wh = (16, 37)
            objects_map['lava wall 0'] = wall_instance0
            wall_instance1 = LavaWall()
            wall_instance1.xy = (8, 61)
            wall_instance1.wh = (8, 37)
            objects_map['lava wall 1'] = wall_instance1
            number_of_lava_walls = 2
            i = 0
            while (objects_map.get(f"lava wall {number_of_lava_walls + i}") != None):
                objects_map.pop(f"lava wall {number_of_lava_walls + i}")
                i += 1
            wall_instance0 = Wall()
            wall_instance0.xy = (104, 21)
            wall_instance0.wh = (56, 38)
            objects_map['fixed wall 0'] = wall_instance0
            wall_instance1 = Wall()
            wall_instance1.xy = (72, 21)
            wall_instance1.wh = (16, 38)
            objects_map['fixed wall 1'] = wall_instance1
            wall_instance2 = Wall()
            wall_instance2.xy = (8, 21)
            wall_instance2.wh = (48, 38)
            objects_map['fixed wall 2'] = wall_instance2
            wall_instance3 = Wall()
            wall_instance3.xy = (136, 101)
            wall_instance3.wh = (24, 38)
            objects_map['fixed wall 3'] = wall_instance3
            wall_instance4 = Wall()
            wall_instance4.xy = (32, 101)
            wall_instance4.wh = (96, 38)
            objects_map['fixed wall 4'] = wall_instance4
            wall_instance5 = Wall()
            wall_instance5.xy = (8, 101)
            wall_instance5.wh = (16, 38)
            objects_map['fixed wall 5'] = wall_instance5
            number_of_walls = 6
            i = 0
            while (objects_map.get(f"fixed wall {number_of_walls + i}") != None):
                objects_map.pop(f"fixed wall {number_of_walls + i}")
                i += 1
        elif ram_state[28] == 8:
            wall_instance0 = LavaWall()
            wall_instance0.xy = (144, 61)
            wall_instance0.wh = (16, 37)
            objects_map['lava wall 0'] = wall_instance0
            wall_instance1 = LavaWall()
            wall_instance1.xy = (8, 61)
            wall_instance1.wh = (8, 37)
            objects_map['lava wall 1'] = wall_instance1
            number_of_lava_walls = 2
            i = 0
            while (objects_map.get(f"lava wall {number_of_lava_walls + i}") != None):
                objects_map.pop(f"lava wall {number_of_lava_walls + i}")
                i += 1
            wall_instance0 = Wall()
            wall_instance0.xy = (136, 21)
            wall_instance0.wh = (24, 38)
            objects_map['fixed wall 0'] = wall_instance0
            wall_instance1 = Wall()
            wall_instance1.xy = (32, 21)
            wall_instance1.wh = (96, 38)
            objects_map['fixed wall 1'] = wall_instance1
            wall_instance2 = Wall()
            wall_instance2.xy = (8, 21)
            wall_instance2.wh = (16, 38)
            objects_map['fixed wall 2'] = wall_instance2
            wall_instance3 = Wall()
            wall_instance3.xy = (88, 101)
            wall_instance3.wh = (72, 38)
            objects_map['fixed wall 3'] = wall_instance3
            wall_instance4 = Wall()
            wall_instance4.xy = (8, 101)
            wall_instance4.wh = (64, 38)
            objects_map['fixed wall 4'] = wall_instance4
            number_of_walls = 5
            i = 0
            while (objects_map.get(f"fixed wall {number_of_walls + i}") != None):
                objects_map.pop(f"fixed wall {number_of_walls + i}")
                i += 1
        elif ram_state[28] == 9:
            wall_instance0 = LavaWall()
            wall_instance0.xy = (92, 61)
            wall_instance0.wh = (68, 37)
            objects_map['lava wall 0'] = wall_instance0
            wall_instance1 = LavaWall()
            wall_instance1.xy = (8, 61)
            wall_instance1.wh = (60, 37)
            objects_map['lava wall 1'] = wall_instance1
            number_of_lava_walls = 2
            i = 0
            while (objects_map.get(f"lava wall {number_of_lava_walls + i}") != None):
                objects_map.pop(f"lava wall {number_of_lava_walls + i}")
                i += 1
            wall_instance0 = Wall()
            wall_instance0.xy = (88, 21)
            wall_instance0.wh = (72, 38)
            objects_map['fixed wall 0'] = wall_instance0
            wall_instance1 = Wall()
            wall_instance1.xy = (8, 21)
            wall_instance1.wh = (64, 38)
            objects_map['fixed wall 1'] = wall_instance1
            wall_instance2 = Wall()
            wall_instance2.xy = (136, 101)
            wall_instance2.wh = (24, 38)
            objects_map['fixed wall 2'] = wall_instance2
            wall_instance3 = Wall()
            wall_instance3.xy = (8, 101)
            wall_instance3.wh = (16, 38)
            objects_map['fixed wall 3'] = wall_instance3
            number_of_walls = 4
            i = 0
            while (objects_map.get(f"fixed wall {number_of_walls + i}") != None):
                objects_map.pop(f"fixed wall {number_of_walls + i}")
                i += 1
        elif ram_state[28] == 10:
            number_of_lava_walls = 0
            i = 0
            while (objects_map.get(f"lava wall {number_of_lava_walls + i}") != None):
                objects_map.pop(f"lava wall {number_of_lava_walls + i}")
                i += 1
            wall_instance0 = Wall()
            wall_instance0.xy = (136, 21)
            wall_instance0.wh = (24, 38)
            objects_map['fixed wall 0'] = wall_instance0
            wall_instance1 = Wall()
            wall_instance1.xy = (8, 21)
            wall_instance1.wh = (16, 38)
            objects_map['fixed wall 1'] = wall_instance1
            wall_instance2 = Wall()
            wall_instance2.xy = (112, 101)
            wall_instance2.wh = (48, 38)
            objects_map['fixed wall 2'] = wall_instance2
            wall_instance3 = Wall()
            wall_instance3.xy = (8, 101)
            wall_instance3.wh = (40, 38)
            objects_map['fixed wall 3'] = wall_instance3
            number_of_walls = 4
            i = 0
            while (objects_map.get(f"fixed wall {number_of_walls + i}") != None):
                objects_map.pop(f"fixed wall {number_of_walls + i}")
                i += 1
        elif ram_state[28] == 11:
            number_of_lava_walls = 0
            i = 0
            while (objects_map.get(f"lava wall {number_of_lava_walls + i}") != None):
                objects_map.pop(f"lava wall {number_of_lava_walls + i}")
                i += 1
            wall_instance0 = Wall()
            wall_instance0.xy = (8, 21)
            wall_instance0.wh = (152, 38)
            objects_map['fixed wall 0'] = wall_instance0
            wall_instance1 = Wall()
            wall_instance1.xy = (128, 101)
            wall_instance1.wh = (32, 38)
            objects_map['fixed wall 1'] = wall_instance1
            wall_instance2 = Wall()
            wall_instance2.xy = (8, 101)
            wall_instance2.wh = (24, 38)
            objects_map['fixed wall 2'] = wall_instance2
            number_of_walls = 3
            i = 0
            while (objects_map.get(f"fixed wall {number_of_walls + i}") != None):
                objects_map.pop(f"fixed wall {number_of_walls + i}")
                i += 1
        elif ram_state[28] == 12:
            number_of_lava_walls = 0
            i = 0
            while (objects_map.get(f"lava wall {number_of_lava_walls + i}") != None):
                objects_map.pop(f"lava wall {number_of_lava_walls + i}")
                i += 1
            wall_instance0 = Wall()
            wall_instance0.xy = (8, 21)
            wall_instance0.wh = (152, 38)
            objects_map['fixed wall 0'] = wall_instance0
            wall_instance1 = Wall()
            wall_instance1.xy = (140, 101)
            wall_instance1.wh = (20, 38)
            objects_map['fixed wall 1'] = wall_instance1
            wall_instance2 = Wall()
            wall_instance2.xy = (72, 101)
            wall_instance2.wh = (16, 38)
            objects_map['fixed wall 2'] = wall_instance2
            wall_instance3 = Wall()
            wall_instance3.xy = (8, 101)
            wall_instance3.wh = (12, 38)
            objects_map['fixed wall 3'] = wall_instance3
            number_of_walls = 4
            i = 0
            while (objects_map.get(f"fixed wall {number_of_walls + i}") != None):
                objects_map.pop(f"fixed wall {number_of_walls + i}")
                i += 1
        elif ram_state[28] == 13:
            number_of_lava_walls = 0
            i = 0
            while (objects_map.get(f"lava wall {number_of_lava_walls + i}") != None):
                objects_map.pop(f"lava wall {number_of_lava_walls + i}")
                i += 1
            wall_instance0 = Wall()
            wall_instance0.xy = (8, 21)
            wall_instance0.wh = (152, 38)
            objects_map['fixed wall 0'] = wall_instance0
            wall_instance1 = Wall()
            wall_instance1.xy = (64, 61)
            wall_instance1.wh = (32, 37)
            objects_map['fixed wall 1'] = wall_instance1
            wall_instance2 = Wall()
            wall_instance2.xy = (112, 101)
            wall_instance2.wh = (48, 38)
            objects_map['fixed wall 2'] = wall_instance2
            wall_instance3 = Wall()
            wall_instance3.xy = (8, 101)
            wall_instance3.wh = (40, 38)
            objects_map['fixed wall 3'] = wall_instance3
            number_of_walls = 4
            i = 0
            while (objects_map.get(f"fixed wall {number_of_walls + i}") != None):
                objects_map.pop(f"fixed wall {number_of_walls + i}")
                i += 1
        elif ram_state[28] == 14:
            number_of_lava_walls = 0
            i = 0
            while (objects_map.get(f"lava wall {number_of_lava_walls + i}") != None):
                objects_map.pop(f"lava wall {number_of_lava_walls + i}")
                i += 1
            wall_instance0 = Wall()
            wall_instance0.xy = (8, 21)
            wall_instance0.wh = (152, 38)
            objects_map['fixed wall 0'] = wall_instance0
            wall_instance1 = Wall()
            wall_instance1.xy = (48, 61)
            wall_instance1.wh = (64, 37)
            objects_map['fixed wall 1'] = wall_instance1
            wall_instance2 = Wall()
            wall_instance2.xy = (136, 101)
            wall_instance2.wh = (24, 38)
            objects_map['fixed wall 2'] = wall_instance2
            wall_instance3 = Wall()
            wall_instance3.xy = (8, 101)
            wall_instance3.wh = (16, 38)
            objects_map['fixed wall 3'] = wall_instance3
            number_of_walls = 4
            i = 0
            while (objects_map.get(f"fixed wall {number_of_walls + i}") != None):
                objects_map.pop(f"fixed wall {number_of_walls + i}")
                i += 1
        elif ram_state[28] == 15:
            number_of_lava_walls = 0
            i = 0
            while (objects_map.get(f"lava wall {number_of_lava_walls + i}") != None):
                objects_map.pop(f"lava wall {number_of_lava_walls + i}")
                i += 1
            wall_instance0 = Wall()
            wall_instance0.xy = (8, 21)
            wall_instance0.wh = (152, 38)
            objects_map['fixed wall 0'] = wall_instance0
            wall_instance1 = Wall()
            wall_instance1.xy = (8, 101)
            wall_instance1.wh = (152, 38)
            objects_map['fixed wall 1'] = wall_instance1
            number_of_walls = 2
            i = 0
            while (objects_map.get(f"fixed wall {number_of_walls + i}") != None):
                objects_map.pop(f"fixed wall {number_of_walls + i}")
                i += 1

    elif ram_state[117] == 9:
        if ram_state[28] == 0:
            wall_instance0 = LavaWall()
            wall_instance0.xy = (144, 61)
            wall_instance0.wh = (16, 37)
            objects_map['lava wall 0'] = wall_instance0
            wall_instance1 = LavaWall()
            wall_instance1.xy = (8, 61)
            wall_instance1.wh = (8, 37)
            objects_map['lava wall 1'] = wall_instance1
            number_of_lava_walls = 2
            i = 0
            while (objects_map.get(f"lava wall {number_of_lava_walls + i}") != None):
                objects_map.pop(f"lava wall {number_of_lava_walls + i}")
                i += 1
            wall_instance0 = Wall()
            wall_instance0.xy = (136, 21)
            wall_instance0.wh = (24, 38)
            objects_map['fixed wall 0'] = wall_instance0
            wall_instance1 = Wall()
            wall_instance1.xy = (8, 21)
            wall_instance1.wh = (16, 38)
            objects_map['fixed wall 1'] = wall_instance1
            wall_instance2 = Wall()
            wall_instance2.xy = (88, 101)
            wall_instance2.wh = (72, 38)
            objects_map['fixed wall 2'] = wall_instance2
            wall_instance3 = Wall()
            wall_instance3.xy = (8, 101)
            wall_instance3.wh = (64, 38)
            objects_map['fixed wall 3'] = wall_instance3
            number_of_walls = 4
            i = 0
            while (objects_map.get(f"fixed wall {number_of_walls + i}") != None):
                objects_map.pop(f"fixed wall {number_of_walls + i}")
                i += 1
        elif ram_state[28] == 1:
            wall_instance0 = LavaWall()
            wall_instance0.xy = (144, 61)
            wall_instance0.wh = (16, 37)
            objects_map['lava wall 0'] = wall_instance0
            wall_instance1 = LavaWall()
            wall_instance1.xy = (8, 61)
            wall_instance1.wh = (8, 37)
            objects_map['lava wall 1'] = wall_instance1
            number_of_lava_walls = 2
            i = 0
            while (objects_map.get(f"lava wall {number_of_lava_walls + i}") != None):
                objects_map.pop(f"lava wall {number_of_lava_walls + i}")
                i += 1
            wall_instance0 = Wall()
            wall_instance0.xy = (88, 21)
            wall_instance0.wh = (72, 38)
            objects_map['fixed wall 0'] = wall_instance0
            wall_instance1 = Wall()
            wall_instance1.xy = (8, 21)
            wall_instance1.wh = (64, 38)
            objects_map['fixed wall 1'] = wall_instance1
            wall_instance2 = Wall()
            wall_instance2.xy = (136, 101)
            wall_instance2.wh = (24, 38)
            objects_map['fixed wall 2'] = wall_instance2
            wall_instance3 = Wall()
            wall_instance3.xy = (32, 101)
            wall_instance3.wh = (96, 38)
            objects_map['fixed wall 3'] = wall_instance3
            wall_instance4 = Wall()
            wall_instance4.xy = (8, 101)
            wall_instance4.wh = (16, 38)
            objects_map['fixed wall 4'] = wall_instance4
            number_of_walls = 5
            i = 0
            while (objects_map.get(f"fixed wall {number_of_walls + i}") != None):
                objects_map.pop(f"fixed wall {number_of_walls + i}")
                i += 1
        elif ram_state[28] == 2:
            wall_instance0 = LavaWall()
            wall_instance0.xy = (144, 61)
            wall_instance0.wh = (16, 37)
            objects_map['lava wall 0'] = wall_instance0
            wall_instance1 = LavaWall()
            wall_instance1.xy = (8, 61)
            wall_instance1.wh = (8, 37)
            objects_map['lava wall 1'] = wall_instance1
            number_of_lava_walls = 2
            i = 0
            while (objects_map.get(f"lava wall {number_of_lava_walls + i}") != None):
                objects_map.pop(f"lava wall {number_of_lava_walls + i}")
                i += 1
            wall_instance0 = Wall()
            wall_instance0.xy = (136, 21)
            wall_instance0.wh = (24, 38)
            objects_map['fixed wall 0'] = wall_instance0
            wall_instance1 = Wall()
            wall_instance1.xy = (32, 21)
            wall_instance1.wh = (96, 38)
            objects_map['fixed wall 1'] = wall_instance1
            wall_instance2 = Wall()
            wall_instance2.xy = (8, 21)
            wall_instance2.wh = (16, 38)
            objects_map['fixed wall 2'] = wall_instance2
            wall_instance3 = Wall()
            wall_instance3.xy = (84, 101)
            wall_instance3.wh = (76, 38)
            objects_map['fixed wall 3'] = wall_instance3
            wall_instance4 = Wall()
            wall_instance4.xy = (8, 101)
            wall_instance4.wh = (68, 38)
            objects_map['fixed wall 4'] = wall_instance4
            number_of_walls = 5
            i = 0
            while (objects_map.get(f"fixed wall {number_of_walls + i}") != None):
                objects_map.pop(f"fixed wall {number_of_walls + i}")
                i += 1
        elif ram_state[28] == 3:
            wall_instance0 = LavaWall()
            wall_instance0.xy = (144, 61)
            wall_instance0.wh = (16, 37)
            objects_map['lava wall 0'] = wall_instance0
            wall_instance1 = LavaWall()
            wall_instance1.xy = (8, 61)
            wall_instance1.wh = (8, 37)
            objects_map['lava wall 1'] = wall_instance1
            number_of_lava_walls = 2
            i = 0
            while (objects_map.get(f"lava wall {number_of_lava_walls + i}") != None):
                objects_map.pop(f"lava wall {number_of_lava_walls + i}")
                i += 1
            wall_instance0 = Wall()
            wall_instance0.xy = (84, 21)
            wall_instance0.wh = (76, 38)
            objects_map['fixed wall 0'] = wall_instance0
            wall_instance1 = Wall()
            wall_instance1.xy = (8, 21)
            wall_instance1.wh = (68, 38)
            objects_map['fixed wall 1'] = wall_instance1
            wall_instance2 = Wall()
            wall_instance2.xy = (132, 101)
            wall_instance2.wh = (28, 38)
            objects_map['fixed wall 2'] = wall_instance2
            wall_instance3 = Wall()
            wall_instance3.xy = (84, 101)
            wall_instance3.wh = (40, 38)
            objects_map['fixed wall 3'] = wall_instance3
            wall_instance4 = Wall()
            wall_instance4.xy = (36, 101)
            wall_instance4.wh = (40, 38)
            objects_map['fixed wall 4'] = wall_instance4
            wall_instance5 = Wall()
            wall_instance5.xy = (8, 101)
            wall_instance5.wh = (20, 38)
            objects_map['fixed wall 5'] = wall_instance5
            number_of_walls = 6
            i = 0
            while (objects_map.get(f"fixed wall {number_of_walls + i}") != None):
                objects_map.pop(f"fixed wall {number_of_walls + i}")
                i += 1
        elif ram_state[28] == 4:
            wall_instance0 = LavaWall()
            wall_instance0.xy = (136, 61)
            wall_instance0.wh = (24, 37)
            objects_map['lava wall 0'] = wall_instance0
            wall_instance1 = LavaWall()
            wall_instance1.xy = (56, 61)
            wall_instance1.wh = (64, 37)
            objects_map['lava wall 1'] = wall_instance1
            wall_instance2 = LavaWall()
            wall_instance2.xy = (8, 61)
            wall_instance2.wh = (32, 37)
            objects_map['lava wall 2'] = wall_instance2
            number_of_lava_walls = 3
            i = 0
            while (objects_map.get(f"lava wall {number_of_lava_walls + i}") != None):
                objects_map.pop(f"lava wall {number_of_lava_walls + i}")
                i += 1
            wall_instance0 = Wall()
            wall_instance0.xy = (132, 21)
            wall_instance0.wh = (28, 38)
            objects_map['fixed wall 0'] = wall_instance0
            wall_instance1 = Wall()
            wall_instance1.xy = (84, 21)
            wall_instance1.wh = (40, 38)
            objects_map['fixed wall 1'] = wall_instance1
            wall_instance2 = Wall()
            wall_instance2.xy = (36, 21)
            wall_instance2.wh = (40, 38)
            objects_map['fixed wall 2'] = wall_instance2
            wall_instance3 = Wall()
            wall_instance3.xy = (8, 21)
            wall_instance3.wh = (20, 38)
            objects_map['fixed wall 3'] = wall_instance3
            wall_instance4 = Wall()
            wall_instance4.xy = (132, 101)
            wall_instance4.wh = (28, 38)
            objects_map['fixed wall 4'] = wall_instance4
            wall_instance5 = Wall()
            wall_instance5.xy = (36, 101)
            wall_instance5.wh = (88, 38)
            objects_map['fixed wall 5'] = wall_instance5
            wall_instance6 = Wall()
            wall_instance6.xy = (8, 101)
            wall_instance6.wh = (20, 38)
            objects_map['fixed wall 6'] = wall_instance6
            number_of_walls = 7
            i = 0
            while (objects_map.get(f"fixed wall {number_of_walls + i}") != None):
                objects_map.pop(f"fixed wall {number_of_walls + i}")
                i += 1
        elif ram_state[28] == 5:
            wall_instance0 = LavaWall()
            wall_instance0.xy = (144, 61)
            wall_instance0.wh = (16, 37)
            objects_map['lava wall 0'] = wall_instance0
            wall_instance1 = LavaWall()
            wall_instance1.xy = (44, 61)
            wall_instance1.wh = (72, 37)
            objects_map['lava wall 1'] = wall_instance1
            wall_instance2 = LavaWall()
            wall_instance2.xy = (8, 61)
            wall_instance2.wh = (8, 37)
            objects_map['lava wall 2'] = wall_instance2
            number_of_lava_walls = 3
            i = 0
            while (objects_map.get(f"lava wall {number_of_lava_walls + i}") != None):
                objects_map.pop(f"lava wall {number_of_lava_walls + i}")
                i += 1
            wall_instance0 = Wall()
            wall_instance0.xy = (132, 21)
            wall_instance0.wh = (28, 38)
            objects_map['fixed wall 0'] = wall_instance0
            wall_instance1 = Wall()
            wall_instance1.xy = (36, 21)
            wall_instance1.wh = (88, 38)
            objects_map['fixed wall 1'] = wall_instance1
            wall_instance2 = Wall()
            wall_instance2.xy = (8, 21)
            wall_instance2.wh = (20, 38)
            objects_map['fixed wall 2'] = wall_instance2
            wall_instance3 = Wall()
            wall_instance3.xy = (124, 101)
            wall_instance3.wh = (36, 38)
            objects_map['fixed wall 3'] = wall_instance3
            wall_instance4 = Wall()
            wall_instance4.xy = (48, 101)
            wall_instance4.wh = (64, 38)
            objects_map['fixed wall 4'] = wall_instance4
            wall_instance5 = Wall()
            wall_instance5.xy = (8, 101)
            wall_instance5.wh = (28, 38)
            objects_map['fixed wall 5'] = wall_instance5
            number_of_walls = 6
            i = 0
            while (objects_map.get(f"fixed wall {number_of_walls + i}") != None):
                objects_map.pop(f"fixed wall {number_of_walls + i}")
                i += 1
        elif ram_state[28] == 6:
            wall_instance0 = LavaWall()
            wall_instance0.xy = (144, 61)
            wall_instance0.wh = (16, 37)
            objects_map['lava wall 0'] = wall_instance0
            wall_instance1 = LavaWall()
            wall_instance1.xy = (8, 61)
            wall_instance1.wh = (8, 37)
            objects_map['lava wall 1'] = wall_instance1
            number_of_lava_walls = 2
            i = 0
            while (objects_map.get(f"lava wall {number_of_lava_walls + i}") != None):
                objects_map.pop(f"lava wall {number_of_lava_walls + i}")
                i += 1
            wall_instance0 = Wall()
            wall_instance0.xy = (124, 21)
            wall_instance0.wh = (36, 38)
            objects_map['fixed wall 0'] = wall_instance0
            wall_instance1 = Wall()
            wall_instance1.xy = (48, 21)
            wall_instance1.wh = (64, 38)
            objects_map['fixed wall 1'] = wall_instance1
            wall_instance2 = Wall()
            wall_instance2.xy = (8, 21)
            wall_instance2.wh = (28, 38)
            objects_map['fixed wall 2'] = wall_instance2
            wall_instance3 = Wall()
            wall_instance3.xy = (140, 101)
            wall_instance3.wh = (20, 38)
            objects_map['fixed wall 3'] = wall_instance3
            wall_instance4 = Wall()
            wall_instance4.xy = (88, 101)
            wall_instance4.wh = (36, 38)
            objects_map['fixed wall 4'] = wall_instance4
            wall_instance5 = Wall()
            wall_instance5.xy = (36, 101)
            wall_instance5.wh = (36, 38)
            objects_map['fixed wall 5'] = wall_instance5
            wall_instance6 = Wall()
            wall_instance6.xy = (8, 101)
            wall_instance6.wh = (12, 38)
            objects_map['fixed wall 6'] = wall_instance6
            number_of_walls = 7
            i = 0
            while (objects_map.get(f"fixed wall {number_of_walls + i}") != None):
                objects_map.pop(f"fixed wall {number_of_walls + i}")
                i += 1
        elif ram_state[28] == 7:
            wall_instance0 = LavaWall()
            wall_instance0.xy = (136, 61)
            wall_instance0.wh = (24, 37)
            objects_map['lava wall 0'] = wall_instance0
            wall_instance1 = LavaWall()
            wall_instance1.xy = (84, 61)
            wall_instance1.wh = (44, 37)
            objects_map['lava wall 1'] = wall_instance1
            wall_instance2 = LavaWall()
            wall_instance2.xy = (32, 61)
            wall_instance2.wh = (44, 37)
            objects_map['lava wall 2'] = wall_instance2
            wall_instance3 = LavaWall()
            wall_instance3.xy = (8, 61)
            wall_instance3.wh = (16, 37)
            objects_map['lava wall 3'] = wall_instance3
            number_of_lava_walls = 4
            i = 0
            while (objects_map.get(f"lava wall {number_of_lava_walls + i}") != None):
                objects_map.pop(f"lava wall {number_of_lava_walls + i}")
                i += 1
            wall_instance0 = Wall()
            wall_instance0.xy = (140, 21)
            wall_instance0.wh = (20, 38)
            objects_map['fixed wall 0'] = wall_instance0
            wall_instance1 = Wall()
            wall_instance1.xy = (88, 21)
            wall_instance1.wh = (36, 38)
            objects_map['fixed wall 1'] = wall_instance1
            wall_instance2 = Wall()
            wall_instance2.xy = (36, 21)
            wall_instance2.wh = (36, 38)
            objects_map['fixed wall 2'] = wall_instance2
            wall_instance3 = Wall()
            wall_instance3.xy = (8, 21)
            wall_instance3.wh = (12, 38)
            objects_map['fixed wall 3'] = wall_instance3
            wall_instance4 = Wall()
            wall_instance4.xy = (144, 101)
            wall_instance4.wh = (16, 38)
            objects_map['fixed wall 4'] = wall_instance4
            wall_instance5 = Wall()
            wall_instance5.xy = (8, 101)
            wall_instance5.wh = (8, 38)
            objects_map['fixed wall 5'] = wall_instance5
            number_of_walls = 6
            i = 0
            while (objects_map.get(f"fixed wall {number_of_walls + i}") != None):
                objects_map.pop(f"fixed wall {number_of_walls + i}")
                i += 1
        elif ram_state[28] == 8:
            wall_instance0 = LavaWall()
            wall_instance0.xy = (88, 61)
            wall_instance0.wh = (72, 37)
            objects_map['lava wall 0'] = wall_instance0
            wall_instance1 = LavaWall()
            wall_instance1.xy = (8, 61)
            wall_instance1.wh = (64, 37)
            objects_map['lava wall 1'] = wall_instance1
            number_of_lava_walls = 2
            i = 0
            while (objects_map.get(f"lava wall {number_of_lava_walls + i}") != None):
                objects_map.pop(f"lava wall {number_of_lava_walls + i}")
                i += 1
            wall_instance0 = Wall()
            wall_instance0.xy = (144, 21)
            wall_instance0.wh = (16, 38)
            objects_map['fixed wall 0'] = wall_instance0
            wall_instance1 = Wall()
            wall_instance1.xy = (8, 21)
            wall_instance1.wh = (8, 38)
            objects_map['fixed wall 1'] = wall_instance1
            wall_instance2 = Wall()
            wall_instance2.xy = (144, 101)
            wall_instance2.wh = (16, 38)
            objects_map['fixed wall 2'] = wall_instance2
            wall_instance3 = Wall()
            wall_instance3.xy = (8, 101)
            wall_instance3.wh = (8, 38)
            objects_map['fixed wall 3'] = wall_instance3
            number_of_walls = 4
            i = 0
            while (objects_map.get(f"fixed wall {number_of_walls + i}") != None):
                objects_map.pop(f"fixed wall {number_of_walls + i}")
                i += 1
        elif ram_state[28] == 9:
            wall_instance0 = LavaWall()
            wall_instance0.xy = (96, 61)
            wall_instance0.wh = (64, 37)
            objects_map['lava wall 0'] = wall_instance0
            wall_instance1 = LavaWall()
            wall_instance1.xy = (8, 61)
            wall_instance1.wh = (56, 37)
            objects_map['lava wall 1'] = wall_instance1
            number_of_lava_walls = 2
            i = 0
            while (objects_map.get(f"lava wall {number_of_lava_walls + i}") != None):
                objects_map.pop(f"lava wall {number_of_lava_walls + i}")
                i += 1
            wall_instance0 = Wall()
            wall_instance0.xy = (144, 21)
            wall_instance0.wh = (16, 38)
            objects_map['fixed wall 0'] = wall_instance0
            wall_instance1 = Wall()
            wall_instance1.xy = (8, 21)
            wall_instance1.wh = (8, 38)
            objects_map['fixed wall 1'] = wall_instance1
            wall_instance2 = Wall()
            wall_instance2.xy = (136, 101)
            wall_instance2.wh = (24, 38)
            objects_map['fixed wall 2'] = wall_instance2
            wall_instance3 = Wall()
            wall_instance3.xy = (8, 101)
            wall_instance3.wh = (16, 38)
            objects_map['fixed wall 3'] = wall_instance3
            number_of_walls = 4
            i = 0
            while (objects_map.get(f"fixed wall {number_of_walls + i}") != None):
                objects_map.pop(f"fixed wall {number_of_walls + i}")
                i += 1
        elif ram_state[28] == 10:
            wall_instance0 = LavaWall()
            wall_instance0.xy = (48, 61)
            wall_instance0.wh = (64, 37)
            objects_map['lava wall 0'] = wall_instance0
            number_of_lava_walls = 1
            i = 0
            while (objects_map.get(f"lava wall {number_of_lava_walls + i}") != None):
                objects_map.pop(f"lava wall {number_of_lava_walls + i}")
                i += 1
            wall_instance0 = Wall()
            wall_instance0.xy = (136, 21)
            wall_instance0.wh = (24, 38)
            objects_map['fixed wall 0'] = wall_instance0
            wall_instance1 = Wall()
            wall_instance1.xy = (8, 21)
            wall_instance1.wh = (16, 38)
            objects_map['fixed wall 1'] = wall_instance1
            wall_instance2 = Wall()
            wall_instance2.xy = (128, 101)
            wall_instance2.wh = (32, 38)
            objects_map['fixed wall 2'] = wall_instance2
            wall_instance3 = Wall()
            wall_instance3.xy = (8, 101)
            wall_instance3.wh = (24, 38)
            objects_map['fixed wall 3'] = wall_instance3
            number_of_walls = 4
            i = 0
            while (objects_map.get(f"fixed wall {number_of_walls + i}") != None):
                objects_map.pop(f"fixed wall {number_of_walls + i}")
                i += 1
        elif ram_state[28] == 11:
            number_of_lava_walls = 0
            i = 0
            while (objects_map.get(f"lava wall {number_of_lava_walls + i}") != None):
                objects_map.pop(f"lava wall {number_of_lava_walls + i}")
                i += 1
            wall_instance0 = Wall()
            wall_instance0.xy = (8, 21)
            wall_instance0.wh = (152, 38)
            objects_map['fixed wall 0'] = wall_instance0
            wall_instance1 = Wall()
            wall_instance1.xy = (132, 101)
            wall_instance1.wh = (28, 38)
            objects_map['fixed wall 1'] = wall_instance1
            wall_instance2 = Wall()
            wall_instance2.xy = (8, 101)
            wall_instance2.wh = (20, 38)
            objects_map['fixed wall 2'] = wall_instance2
            number_of_walls = 3
            i = 0
            while (objects_map.get(f"fixed wall {number_of_walls + i}") != None):
                objects_map.pop(f"fixed wall {number_of_walls + i}")
                i += 1
        elif ram_state[28] == 12:
            number_of_lava_walls = 0
            i = 0
            while (objects_map.get(f"lava wall {number_of_lava_walls + i}") != None):
                objects_map.pop(f"lava wall {number_of_lava_walls + i}")
                i += 1
            wall_instance0 = Wall()
            wall_instance0.xy = (8, 21)
            wall_instance0.wh = (152, 38)
            objects_map['fixed wall 0'] = wall_instance0
            wall_instance1 = Wall()
            wall_instance1.xy = (136, 101)
            wall_instance1.wh = (24, 38)
            objects_map['fixed wall 1'] = wall_instance1
            wall_instance2 = Wall()
            wall_instance2.xy = (72, 101)
            wall_instance2.wh = (16, 38)
            objects_map['fixed wall 2'] = wall_instance2
            wall_instance3 = Wall()
            wall_instance3.xy = (8, 101)
            wall_instance3.wh = (16, 38)
            objects_map['fixed wall 3'] = wall_instance3
            number_of_walls = 4
            i = 0
            while (objects_map.get(f"fixed wall {number_of_walls + i}") != None):
                objects_map.pop(f"fixed wall {number_of_walls + i}")
                i += 1
        elif ram_state[28] == 13:
            wall_instance0 = LavaWall()
            wall_instance0.xy = (72, 61)
            wall_instance0.wh = (16, 37)
            objects_map['lava wall 0'] = wall_instance0
            number_of_lava_walls = 1
            i = 0
            while (objects_map.get(f"lava wall {number_of_lava_walls + i}") != None):
                objects_map.pop(f"lava wall {number_of_lava_walls + i}")
                i += 1
            wall_instance0 = Wall()
            wall_instance0.xy = (8, 21)
            wall_instance0.wh = (152, 38)
            objects_map['fixed wall 0'] = wall_instance0
            wall_instance1 = Wall()
            wall_instance1.xy = (136, 101)
            wall_instance1.wh = (24, 38)
            objects_map['fixed wall 1'] = wall_instance1
            wall_instance2 = Wall()
            wall_instance2.xy = (8, 101)
            wall_instance2.wh = (16, 38)
            objects_map['fixed wall 2'] = wall_instance2
            number_of_walls = 3
            i = 0
            while (objects_map.get(f"fixed wall {number_of_walls + i}") != None):
                objects_map.pop(f"fixed wall {number_of_walls + i}")
                i += 1
        elif ram_state[28] == 14:
            number_of_lava_walls = 0
            i = 0
            while (objects_map.get(f"lava wall {number_of_lava_walls + i}") != None):
                objects_map.pop(f"lava wall {number_of_lava_walls + i}")
                i += 1
            wall_instance0 = Wall()
            wall_instance0.xy = (8, 21)
            wall_instance0.wh = (152, 38)
            objects_map['fixed wall 0'] = wall_instance0
            wall_instance1 = Wall()
            wall_instance1.xy = (120, 101)
            wall_instance1.wh = (40, 38)
            objects_map['fixed wall 1'] = wall_instance1
            wall_instance2 = Wall()
            wall_instance2.xy = (72, 101)
            wall_instance2.wh = (16, 38)
            objects_map['fixed wall 2'] = wall_instance2
            wall_instance3 = Wall()
            wall_instance3.xy = (8, 101)
            wall_instance3.wh = (32, 38)
            objects_map['fixed wall 3'] = wall_instance3
            number_of_walls = 4
            i = 0
            while (objects_map.get(f"fixed wall {number_of_walls + i}") != None):
                objects_map.pop(f"fixed wall {number_of_walls + i}")
                i += 1
        elif ram_state[28] == 15:
            number_of_lava_walls = 0
            i = 0
            while (objects_map.get(f"lava wall {number_of_lava_walls + i}") != None):
                objects_map.pop(f"lava wall {number_of_lava_walls + i}")
                i += 1
            wall_instance0 = Wall()
            wall_instance0.xy = (8, 21)
            wall_instance0.wh = (152, 38)
            objects_map['fixed wall 0'] = wall_instance0
            wall_instance1 = Wall()
            wall_instance1.xy = (8, 101)
            wall_instance1.wh = (152, 38)
            objects_map['fixed wall 1'] = wall_instance1
            number_of_walls = 2
            i = 0
            while (objects_map.get(f"fixed wall {number_of_walls + i}") != None):
                objects_map.pop(f"fixed wall {number_of_walls + i}")
                i += 1

    elif ram_state[117] == 10:
        if ram_state[28] == 0:
            wall_instance0 = LavaWall()
            wall_instance0.xy = (140, 61)
            wall_instance0.wh = (20, 37)
            objects_map['lava wall 0'] = wall_instance0
            wall_instance1 = LavaWall()
            wall_instance1.xy = (8, 61)
            wall_instance1.wh = (12, 37)
            objects_map['lava wall 1'] = wall_instance1
            number_of_lava_walls = 2
            i = 0
            while (objects_map.get(f"lava wall {number_of_lava_walls + i}") != None):
                objects_map.pop(f"lava wall {number_of_lava_walls + i}")
                i += 1
            wall_instance0 = Wall()
            wall_instance0.xy = (136, 21)
            wall_instance0.wh = (24, 38)
            objects_map['fixed wall 0'] = wall_instance0
            wall_instance1 = Wall()
            wall_instance1.xy = (8, 21)
            wall_instance1.wh = (16, 38)
            objects_map['fixed wall 1'] = wall_instance1
            wall_instance2 = Wall()
            wall_instance2.xy = (88, 101)
            wall_instance2.wh = (72, 38)
            objects_map['fixed wall 2'] = wall_instance2
            wall_instance3 = Wall()
            wall_instance3.xy = (8, 101)
            wall_instance3.wh = (64, 38)
            objects_map['fixed wall 3'] = wall_instance3
            number_of_walls = 4
            i = 0
            while (objects_map.get(f"fixed wall {number_of_walls + i}") != None):
                objects_map.pop(f"fixed wall {number_of_walls + i}")
                i += 1
        elif ram_state[28] == 1:
            wall_instance0 = LavaWall()
            wall_instance0.xy = (88, 61)
            wall_instance0.wh = (72, 37)
            objects_map['lava wall 0'] = wall_instance0
            wall_instance1 = LavaWall()
            wall_instance1.xy = (8, 61)
            wall_instance1.wh = (64, 37)
            objects_map['lava wall 1'] = wall_instance1
            number_of_lava_walls = 2
            i = 0
            while (objects_map.get(f"lava wall {number_of_lava_walls + i}") != None):
                objects_map.pop(f"lava wall {number_of_lava_walls + i}")
                i += 1
            wall_instance0 = Wall()
            wall_instance0.xy = (88, 21)
            wall_instance0.wh = (72, 38)
            objects_map['fixed wall 0'] = wall_instance0
            wall_instance1 = Wall()
            wall_instance1.xy = (8, 21)
            wall_instance1.wh = (64, 38)
            objects_map['fixed wall 1'] = wall_instance1
            wall_instance2 = Wall()
            wall_instance2.xy = (112, 101)
            wall_instance2.wh = (48, 38)
            objects_map['fixed wall 2'] = wall_instance2
            wall_instance3 = Wall()
            wall_instance3.xy = (8, 101)
            wall_instance3.wh = (40, 38)
            objects_map['fixed wall 3'] = wall_instance3
            number_of_walls = 4
            i = 0
            while (objects_map.get(f"fixed wall {number_of_walls + i}") != None):
                objects_map.pop(f"fixed wall {number_of_walls + i}")
                i += 1
        elif ram_state[28] == 2:
            wall_instance0 = LavaWall()
            wall_instance0.xy = (144, 61)
            wall_instance0.wh = (16, 37)
            objects_map['lava wall 0'] = wall_instance0
            wall_instance1 = LavaWall()
            wall_instance1.xy = (72, 61)
            wall_instance1.wh = (16, 37)
            objects_map['lava wall 1'] = wall_instance1
            wall_instance2 = LavaWall()
            wall_instance2.xy = (8, 61)
            wall_instance2.wh = (8, 37)
            objects_map['lava wall 2'] = wall_instance2
            number_of_lava_walls = 3
            i = 0
            while (objects_map.get(f"lava wall {number_of_lava_walls + i}") != None):
                objects_map.pop(f"lava wall {number_of_lava_walls + i}")
                i += 1
            wall_instance0 = Wall()
            wall_instance0.xy = (112, 21)
            wall_instance0.wh = (48, 38)
            objects_map['fixed wall 0'] = wall_instance0
            wall_instance1 = Wall()
            wall_instance1.xy = (8, 21)
            wall_instance1.wh = (40, 38)
            objects_map['fixed wall 1'] = wall_instance1
            wall_instance2 = Wall()
            wall_instance2.xy = (140, 101)
            wall_instance2.wh = (20, 38)
            objects_map['fixed wall 2'] = wall_instance2
            wall_instance3 = Wall()
            wall_instance3.xy = (28, 101)
            wall_instance3.wh = (104, 38)
            objects_map['fixed wall 3'] = wall_instance3
            wall_instance4 = Wall()
            wall_instance4.xy = (8, 101)
            wall_instance4.wh = (12, 38)
            objects_map['fixed wall 4'] = wall_instance4
            number_of_walls = 5
            i = 0
            while (objects_map.get(f"fixed wall {number_of_walls + i}") != None):
                objects_map.pop(f"fixed wall {number_of_walls + i}")
                i += 1
        elif ram_state[28] == 3:
            wall_instance0 = LavaWall()
            wall_instance0.xy = (144, 61)
            wall_instance0.wh = (16, 37)
            objects_map['lava wall 0'] = wall_instance0
            wall_instance1 = LavaWall()
            wall_instance1.xy = (8, 61)
            wall_instance1.wh = (8, 37)
            objects_map['lava wall 1'] = wall_instance1
            number_of_lava_walls = 2
            i = 0
            while (objects_map.get(f"lava wall {number_of_lava_walls + i}") != None):
                objects_map.pop(f"lava wall {number_of_lava_walls + i}")
                i += 1
            wall_instance0 = Wall()
            wall_instance0.xy = (140, 21)
            wall_instance0.wh = (20, 38)
            objects_map['fixed wall 0'] = wall_instance0
            wall_instance1 = Wall()
            wall_instance1.xy = (28, 21)
            wall_instance1.wh = (104, 38)
            objects_map['fixed wall 1'] = wall_instance1
            wall_instance2 = Wall()
            wall_instance2.xy = (8, 21)
            wall_instance2.wh = (12, 38)
            objects_map['fixed wall 2'] = wall_instance2
            wall_instance3 = Wall()
            wall_instance3.xy = (88, 101)
            wall_instance3.wh = (72, 38)
            objects_map['fixed wall 3'] = wall_instance3
            wall_instance4 = Wall()
            wall_instance4.xy = (8, 101)
            wall_instance4.wh = (64, 38)
            objects_map['fixed wall 4'] = wall_instance4
            number_of_walls = 5
            i = 0
            while (objects_map.get(f"fixed wall {number_of_walls + i}") != None):
                objects_map.pop(f"fixed wall {number_of_walls + i}")
                i += 1
        elif ram_state[28] == 4:
            wall_instance0 = LavaWall()
            wall_instance0.xy = (144, 61)
            wall_instance0.wh = (16, 37)
            objects_map['lava wall 0'] = wall_instance0
            wall_instance1 = LavaWall()
            wall_instance1.xy = (92, 61)
            wall_instance1.wh = (12, 37)
            objects_map['lava wall 1'] = wall_instance1
            wall_instance2 = LavaWall()
            wall_instance2.xy = (56, 61)
            wall_instance2.wh = (12, 37)
            objects_map['lava wall 2'] = wall_instance2
            wall_instance3 = LavaWall()
            wall_instance3.xy = (8, 61)
            wall_instance3.wh = (8, 37)
            objects_map['lava wall 3'] = wall_instance3
            number_of_lava_walls = 4
            i = 0
            while (objects_map.get(f"lava wall {number_of_lava_walls + i}") != None):
                objects_map.pop(f"lava wall {number_of_lava_walls + i}")
                i += 1
            wall_instance0 = Wall()
            wall_instance0.xy = (88, 21)
            wall_instance0.wh = (72, 38)
            objects_map['fixed wall 0'] = wall_instance0
            wall_instance1 = Wall()
            wall_instance1.xy = (8, 21)
            wall_instance1.wh = (64, 38)
            objects_map['fixed wall 1'] = wall_instance1
            wall_instance2 = Wall()
            wall_instance2.xy = (140, 101)
            wall_instance2.wh = (20, 38)
            objects_map['fixed wall 2'] = wall_instance2
            wall_instance3 = Wall()
            wall_instance3.xy = (116, 101)
            wall_instance3.wh = (16, 38)
            objects_map['fixed wall 3'] = wall_instance3
            wall_instance4 = Wall()
            wall_instance4.xy = (84, 101)
            wall_instance4.wh = (24, 38)
            objects_map['fixed wall 4'] = wall_instance4
            wall_instance5 = Wall()
            wall_instance5.xy = (52, 101)
            wall_instance5.wh = (24, 38)
            objects_map['fixed wall 5'] = wall_instance5
            wall_instance6 = Wall()
            wall_instance6.xy = (28, 101)
            wall_instance6.wh = (16, 38)
            objects_map['fixed wall 6'] = wall_instance6
            wall_instance7 = Wall()
            wall_instance7.xy = (8, 101)
            wall_instance7.wh = (12, 38)
            objects_map['fixed wall 7'] = wall_instance7
            number_of_walls = 8
            i = 0
            while (objects_map.get(f"fixed wall {number_of_walls + i}") != None):
                objects_map.pop(f"fixed wall {number_of_walls + i}")
                i += 1
        elif ram_state[28] == 5:
            wall_instance0 = LavaWall()
            wall_instance0.xy = (140, 61)
            wall_instance0.wh = (20, 37)
            objects_map['lava wall 0'] = wall_instance0
            wall_instance1 = LavaWall()
            wall_instance1.xy = (120, 61)
            wall_instance1.wh = (12, 37)
            objects_map['lava wall 1'] = wall_instance1
            wall_instance2 = LavaWall()
            wall_instance2.xy = (28, 61)
            wall_instance2.wh = (12, 37)
            objects_map['lava wall 2'] = wall_instance2
            wall_instance3 = LavaWall()
            wall_instance3.xy = (8, 61)
            wall_instance3.wh = (12, 37)
            objects_map['lava wall 3'] = wall_instance3
            number_of_lava_walls = 4
            i = 0
            while (objects_map.get(f"lava wall {number_of_lava_walls + i}") != None):
                objects_map.pop(f"lava wall {number_of_lava_walls + i}")
                i += 1
            wall_instance0 = Wall()
            wall_instance0.xy = (140, 21)
            wall_instance0.wh = (20, 38)
            objects_map['fixed wall 0'] = wall_instance0
            wall_instance1 = Wall()
            wall_instance1.xy = (116, 21)
            wall_instance1.wh = (16, 38)
            objects_map['fixed wall 1'] = wall_instance1
            wall_instance2 = Wall()
            wall_instance2.xy = (84, 21)
            wall_instance2.wh = (24, 38)
            objects_map['fixed wall 2'] = wall_instance2
            wall_instance3 = Wall()
            wall_instance3.xy = (52, 21)
            wall_instance3.wh = (24, 38)
            objects_map['fixed wall 3'] = wall_instance3
            wall_instance4 = Wall()
            wall_instance4.xy = (28, 21)
            wall_instance4.wh = (16, 38)
            objects_map['fixed wall 4'] = wall_instance4
            wall_instance5 = Wall()
            wall_instance5.xy = (8, 21)
            wall_instance5.wh = (12, 38)
            objects_map['fixed wall 5'] = wall_instance5
            wall_instance6 = Wall()
            wall_instance6.xy = (140, 101)
            wall_instance6.wh = (20, 38)
            objects_map['fixed wall 6'] = wall_instance6
            wall_instance7 = Wall()
            wall_instance7.xy = (28, 101)
            wall_instance7.wh = (104, 38)
            objects_map['fixed wall 7'] = wall_instance7
            wall_instance8 = Wall()
            wall_instance8.xy = (8, 101)
            wall_instance8.wh = (12, 38)
            objects_map['fixed wall 8'] = wall_instance8
            number_of_walls = 9
            i = 0
            while (objects_map.get(f"fixed wall {number_of_walls + i}") != None):
                objects_map.pop(f"fixed wall {number_of_walls + i}")
                i += 1
        elif ram_state[28] == 6:
            wall_instance0 = LavaWall()
            wall_instance0.xy = (144, 61)
            wall_instance0.wh = (16, 37)
            objects_map['lava wall 0'] = wall_instance0
            wall_instance1 = LavaWall()
            wall_instance1.xy = (8, 61)
            wall_instance1.wh = (8, 37)
            objects_map['lava wall 1'] = wall_instance1
            number_of_lava_walls = 2
            i = 0
            while (objects_map.get(f"lava wall {number_of_lava_walls + i}") != None):
                objects_map.pop(f"lava wall {number_of_lava_walls + i}")
                i += 1
            wall_instance0 = Wall()
            wall_instance0.xy = (140, 21)
            wall_instance0.wh = (20, 38)
            objects_map['fixed wall 0'] = wall_instance0
            wall_instance1 = Wall()
            wall_instance1.xy = (28, 21)
            wall_instance1.wh = (104, 38)
            objects_map['fixed wall 1'] = wall_instance1
            wall_instance2 = Wall()
            wall_instance2.xy = (8, 21)
            wall_instance2.wh = (12, 38)
            objects_map['fixed wall 2'] = wall_instance2
            wall_instance3 = Wall()
            wall_instance3.xy = (112, 101)
            wall_instance3.wh = (48, 38)
            objects_map['fixed wall 3'] = wall_instance3
            wall_instance4 = Wall()
            wall_instance4.xy = (8, 101)
            wall_instance4.wh = (40, 38)
            objects_map['fixed wall 4'] = wall_instance4
            number_of_walls = 5
            i = 0
            while (objects_map.get(f"fixed wall {number_of_walls + i}") != None):
                objects_map.pop(f"fixed wall {number_of_walls + i}")
                i += 1
        elif ram_state[28] == 7:
            wall_instance0 = LavaWall()
            wall_instance0.xy = (88, 61)
            wall_instance0.wh = (72, 37)
            objects_map['lava wall 0'] = wall_instance0
            wall_instance1 = LavaWall()
            wall_instance1.xy = (8, 61)
            wall_instance1.wh = (64, 37)
            objects_map['lava wall 1'] = wall_instance1
            number_of_lava_walls = 2
            i = 0
            while (objects_map.get(f"lava wall {number_of_lava_walls + i}") != None):
                objects_map.pop(f"lava wall {number_of_lava_walls + i}")
                i += 1
            wall_instance0 = Wall()
            wall_instance0.xy = (112, 21)
            wall_instance0.wh = (48, 38)
            objects_map['fixed wall 0'] = wall_instance0
            wall_instance1 = Wall()
            wall_instance1.xy = (8, 21)
            wall_instance1.wh = (40, 38)
            objects_map['fixed wall 1'] = wall_instance1
            wall_instance2 = Wall()
            wall_instance2.xy = (144, 101)
            wall_instance2.wh = (16, 38)
            objects_map['fixed wall 2'] = wall_instance2
            wall_instance3 = Wall()
            wall_instance3.xy = (8, 101)
            wall_instance3.wh = (8, 38)
            objects_map['fixed wall 3'] = wall_instance3
            number_of_walls = 4
            i = 0
            while (objects_map.get(f"fixed wall {number_of_walls + i}") != None):
                objects_map.pop(f"fixed wall {number_of_walls + i}")
                i += 1
        elif ram_state[28] == 8:
            wall_instance0 = LavaWall()
            wall_instance0.xy = (104, 61)
            wall_instance0.wh = (56, 37)
            objects_map['lava wall 0'] = wall_instance0
            wall_instance1 = LavaWall()
            wall_instance1.xy = (72, 61)
            wall_instance1.wh = (16, 37)
            objects_map['lava wall 1'] = wall_instance1
            wall_instance2 = LavaWall()
            wall_instance2.xy = (8, 61)
            wall_instance2.wh = (48, 37)
            objects_map['lava wall 2'] = wall_instance2
            number_of_lava_walls = 3
            i = 0
            while (objects_map.get(f"lava wall {number_of_lava_walls + i}") != None):
                objects_map.pop(f"lava wall {number_of_lava_walls + i}")
                i += 1
            wall_instance0 = Wall()
            wall_instance0.xy = (144, 21)
            wall_instance0.wh = (16, 38)
            objects_map['fixed wall 0'] = wall_instance0
            wall_instance1 = Wall()
            wall_instance1.xy = (8, 21)
            wall_instance1.wh = (8, 38)
            objects_map['fixed wall 1'] = wall_instance1
            wall_instance2 = Wall()
            wall_instance2.xy = (144, 101)
            wall_instance2.wh = (16, 38)
            objects_map['fixed wall 2'] = wall_instance2
            wall_instance3 = Wall()
            wall_instance3.xy = (8, 101)
            wall_instance3.wh = (8, 38)
            objects_map['fixed wall 3'] = wall_instance3
            number_of_walls = 4
            i = 0
            while (objects_map.get(f"fixed wall {number_of_walls + i}") != None):
                objects_map.pop(f"fixed wall {number_of_walls + i}")
                i += 1
        elif ram_state[28] == 9:
            wall_instance0 = LavaWall()
            wall_instance0.xy = (88, 61)
            wall_instance0.wh = (72, 37)
            objects_map['lava wall 0'] = wall_instance0
            wall_instance1 = LavaWall()
            wall_instance1.xy = (8, 61)
            wall_instance1.wh = (64, 37)
            objects_map['lava wall 1'] = wall_instance1
            number_of_lava_walls = 2
            i = 0
            while (objects_map.get(f"lava wall {number_of_lava_walls + i}") != None):
                objects_map.pop(f"lava wall {number_of_lava_walls + i}")
                i += 1
            wall_instance0 = Wall()
            wall_instance0.xy = (144, 21)
            wall_instance0.wh = (16, 38)
            objects_map['fixed wall 0'] = wall_instance0
            wall_instance1 = Wall()
            wall_instance1.xy = (8, 21)
            wall_instance1.wh = (8, 38)
            objects_map['fixed wall 1'] = wall_instance1
            wall_instance2 = Wall()
            wall_instance2.xy = (112, 101)
            wall_instance2.wh = (48, 38)
            objects_map['fixed wall 2'] = wall_instance2
            wall_instance3 = Wall()
            wall_instance3.xy = (8, 101)
            wall_instance3.wh = (40, 38)
            objects_map['fixed wall 3'] = wall_instance3
            number_of_walls = 4
            i = 0
            while (objects_map.get(f"fixed wall {number_of_walls + i}") != None):
                objects_map.pop(f"fixed wall {number_of_walls + i}")
                i += 1
        elif ram_state[28] == 10:
            number_of_lava_walls = 0
            i = 0
            while (objects_map.get(f"lava wall {number_of_lava_walls + i}") != None):
                objects_map.pop(f"lava wall {number_of_lava_walls + i}")
                i += 1
            wall_instance0 = Wall()
            wall_instance0.xy = (112, 21)
            wall_instance0.wh = (48, 38)
            objects_map['fixed wall 0'] = wall_instance0
            wall_instance1 = Wall()
            wall_instance1.xy = (8, 21)
            wall_instance1.wh = (40, 38)
            objects_map['fixed wall 1'] = wall_instance1
            wall_instance2 = Wall()
            wall_instance2.xy = (104, 61)
            wall_instance2.wh = (16, 37)
            objects_map['fixed wall 2'] = wall_instance2
            wall_instance3 = Wall()
            wall_instance3.xy = (72, 61)
            wall_instance3.wh = (16, 37)
            objects_map['fixed wall 3'] = wall_instance3
            wall_instance4 = Wall()
            wall_instance4.xy = (40, 61)
            wall_instance4.wh = (16, 37)
            objects_map['fixed wall 4'] = wall_instance4
            wall_instance5 = Wall()
            wall_instance5.xy = (136, 101)
            wall_instance5.wh = (24, 38)
            objects_map['fixed wall 5'] = wall_instance5
            wall_instance6 = Wall()
            wall_instance6.xy = (68, 101)
            wall_instance6.wh = (24, 38)
            objects_map['fixed wall 6'] = wall_instance6
            wall_instance7 = Wall()
            wall_instance7.xy = (8, 101)
            wall_instance7.wh = (16, 38)
            objects_map['fixed wall 7'] = wall_instance7
            number_of_walls = 8
            i = 0
            while (objects_map.get(f"fixed wall {number_of_walls + i}") != None):
                objects_map.pop(f"fixed wall {number_of_walls + i}")
                i += 1
        elif ram_state[28] == 11:
            number_of_lava_walls = 0
            i = 0
            while (objects_map.get(f"lava wall {number_of_lava_walls + i}") != None):
                objects_map.pop(f"lava wall {number_of_lava_walls + i}")
                i += 1
            wall_instance0 = Wall()
            wall_instance0.xy = (8, 21)
            wall_instance0.wh = (152, 38)
            objects_map['fixed wall 0'] = wall_instance0
            wall_instance1 = Wall()
            wall_instance1.xy = (128, 101)
            wall_instance1.wh = (32, 38)
            objects_map['fixed wall 1'] = wall_instance1
            wall_instance2 = Wall()
            wall_instance2.xy = (72, 101)
            wall_instance2.wh = (16, 38)
            objects_map['fixed wall 2'] = wall_instance2
            wall_instance3 = Wall()
            wall_instance3.xy = (8, 101)
            wall_instance3.wh = (24, 38)
            objects_map['fixed wall 3'] = wall_instance3
            number_of_walls = 4
            i = 0
            while (objects_map.get(f"fixed wall {number_of_walls + i}") != None):
                objects_map.pop(f"fixed wall {number_of_walls + i}")
                i += 1
        elif ram_state[28] == 12:
            wall_instance0 = LavaWall()
            wall_instance0.xy = (72, 61)
            wall_instance0.wh = (16, 37)
            objects_map['lava wall 0'] = wall_instance0
            number_of_lava_walls = 1
            i = 0
            while (objects_map.get(f"lava wall {number_of_lava_walls + i}") != None):
                objects_map.pop(f"lava wall {number_of_lava_walls + i}")
                i += 1
            wall_instance0 = Wall()
            wall_instance0.xy = (8, 21)
            wall_instance0.wh = (152, 38)
            objects_map['fixed wall 0'] = wall_instance0
            wall_instance1 = Wall()
            wall_instance1.xy = (136, 101)
            wall_instance1.wh = (24, 38)
            objects_map['fixed wall 1'] = wall_instance1
            wall_instance2 = Wall()
            wall_instance2.xy = (8, 101)
            wall_instance2.wh = (16, 38)
            objects_map['fixed wall 2'] = wall_instance2
            number_of_walls = 3
            i = 0
            while (objects_map.get(f"fixed wall {number_of_walls + i}") != None):
                objects_map.pop(f"fixed wall {number_of_walls + i}")
                i += 1
        elif ram_state[28] == 13:
            number_of_lava_walls = 0
            i = 0
            while (objects_map.get(f"lava wall {number_of_lava_walls + i}") != None):
                objects_map.pop(f"lava wall {number_of_lava_walls + i}")
                i += 1
            wall_instance0 = Wall()
            wall_instance0.xy = (8, 21)
            wall_instance0.wh = (152, 38)
            objects_map['fixed wall 0'] = wall_instance0
            wall_instance1 = Wall()
            wall_instance1.xy = (112, 101)
            wall_instance1.wh = (48, 38)
            objects_map['fixed wall 1'] = wall_instance1
            wall_instance2 = Wall()
            wall_instance2.xy = (64, 101)
            wall_instance2.wh = (32, 38)
            objects_map['fixed wall 2'] = wall_instance2
            wall_instance3 = Wall()
            wall_instance3.xy = (8, 101)
            wall_instance3.wh = (40, 38)
            objects_map['fixed wall 3'] = wall_instance3
            number_of_walls = 4
            i = 0
            while (objects_map.get(f"fixed wall {number_of_walls + i}") != None):
                objects_map.pop(f"fixed wall {number_of_walls + i}")
                i += 1
        elif ram_state[28] == 14:
            number_of_lava_walls = 0
            i = 0
            while (objects_map.get(f"lava wall {number_of_lava_walls + i}") != None):
                objects_map.pop(f"lava wall {number_of_lava_walls + i}")
                i += 1
            wall_instance0 = Wall()
            wall_instance0.xy = (8, 21)
            wall_instance0.wh = (152, 38)
            objects_map['fixed wall 0'] = wall_instance0
            wall_instance1 = Wall()
            wall_instance1.xy = (136, 101)
            wall_instance1.wh = (24, 38)
            objects_map['fixed wall 1'] = wall_instance1
            wall_instance2 = Wall()
            wall_instance2.xy = (48, 101)
            wall_instance2.wh = (64, 38)
            objects_map['fixed wall 2'] = wall_instance2
            wall_instance3 = Wall()
            wall_instance3.xy = (8, 101)
            wall_instance3.wh = (16, 38)
            objects_map['fixed wall 3'] = wall_instance3
            number_of_walls = 4
            i = 0
            while (objects_map.get(f"fixed wall {number_of_walls + i}") != None):
                objects_map.pop(f"fixed wall {number_of_walls + i}")
                i += 1
        elif ram_state[28] == 15:
            number_of_lava_walls = 0
            i = 0
            while (objects_map.get(f"lava wall {number_of_lava_walls + i}") != None):
                objects_map.pop(f"lava wall {number_of_lava_walls + i}")
                i += 1
            wall_instance0 = Wall()
            wall_instance0.xy = (8, 21)
            wall_instance0.wh = (152, 38)
            objects_map['fixed wall 0'] = wall_instance0
            wall_instance1 = Wall()
            wall_instance1.xy = (8, 101)
            wall_instance1.wh = (152, 38)
            objects_map['fixed wall 1'] = wall_instance1
            number_of_walls = 2
            i = 0
            while (objects_map.get(f"fixed wall {number_of_walls + i}") != None):
                objects_map.pop(f"fixed wall {number_of_walls + i}")
                i += 1

    elif ram_state[117] == 11:
        if ram_state[28] == 0:
            wall_instance0 = LavaWall()
            wall_instance0.xy = (132, 61)
            wall_instance0.wh = (28, 37)
            objects_map['lava wall 0'] = wall_instance0
            wall_instance1 = LavaWall()
            wall_instance1.xy = (8, 61)
            wall_instance1.wh = (20, 37)
            objects_map['lava wall 1'] = wall_instance1
            number_of_lava_walls = 2
            i = 0
            while (objects_map.get(f"lava wall {number_of_lava_walls + i}") != None):
                objects_map.pop(f"lava wall {number_of_lava_walls + i}")
                i += 1
            wall_instance0 = Wall()
            wall_instance0.xy = (136, 21)
            wall_instance0.wh = (24, 38)
            objects_map['fixed wall 0'] = wall_instance0
            wall_instance1 = Wall()
            wall_instance1.xy = (8, 21)
            wall_instance1.wh = (16, 38)
            objects_map['fixed wall 1'] = wall_instance1
            wall_instance2 = Wall()
            wall_instance2.xy = (88, 101)
            wall_instance2.wh = (72, 38)
            objects_map['fixed wall 2'] = wall_instance2
            wall_instance3 = Wall()
            wall_instance3.xy = (8, 101)
            wall_instance3.wh = (64, 38)
            objects_map['fixed wall 3'] = wall_instance3
            number_of_walls = 4
            i = 0
            while (objects_map.get(f"fixed wall {number_of_walls + i}") != None):
                objects_map.pop(f"fixed wall {number_of_walls + i}")
                i += 1
        elif ram_state[28] == 1:
            wall_instance0 = LavaWall()
            wall_instance0.xy = (136, 61)
            wall_instance0.wh = (24, 37)
            objects_map['lava wall 0'] = wall_instance0
            wall_instance1 = LavaWall()
            wall_instance1.xy = (8, 61)
            wall_instance1.wh = (16, 37)
            objects_map['lava wall 1'] = wall_instance1
            number_of_lava_walls = 2
            i = 0
            while (objects_map.get(f"lava wall {number_of_lava_walls + i}") != None):
                objects_map.pop(f"lava wall {number_of_lava_walls + i}")
                i += 1
            wall_instance0 = Wall()
            wall_instance0.xy = (88, 21)
            wall_instance0.wh = (72, 38)
            objects_map['fixed wall 0'] = wall_instance0
            wall_instance1 = Wall()
            wall_instance1.xy = (8, 21)
            wall_instance1.wh = (64, 38)
            objects_map['fixed wall 1'] = wall_instance1
            wall_instance2 = Wall()
            wall_instance2.xy = (132, 101)
            wall_instance2.wh = (28, 38)
            objects_map['fixed wall 2'] = wall_instance2
            wall_instance3 = Wall()
            wall_instance3.xy = (36, 101)
            wall_instance3.wh = (88, 38)
            objects_map['fixed wall 3'] = wall_instance3
            wall_instance4 = Wall()
            wall_instance4.xy = (8, 101)
            wall_instance4.wh = (20, 38)
            objects_map['fixed wall 4'] = wall_instance4
            number_of_walls = 5
            i = 0
            while (objects_map.get(f"fixed wall {number_of_walls + i}") != None):
                objects_map.pop(f"fixed wall {number_of_walls + i}")
                i += 1
        elif ram_state[28] == 2:
            wall_instance0 = LavaWall()
            wall_instance0.xy = (144, 61)
            wall_instance0.wh = (16, 37)
            objects_map['lava wall 0'] = wall_instance0
            wall_instance1 = LavaWall()
            wall_instance1.xy = (8, 61)
            wall_instance1.wh = (8, 37)
            objects_map['lava wall 1'] = wall_instance1
            number_of_lava_walls = 2
            i = 0
            while (objects_map.get(f"lava wall {number_of_lava_walls + i}") != None):
                objects_map.pop(f"lava wall {number_of_lava_walls + i}")
                i += 1
            wall_instance0 = Wall()
            wall_instance0.xy = (132, 21)
            wall_instance0.wh = (28, 38)
            objects_map['fixed wall 0'] = wall_instance0
            wall_instance1 = Wall()
            wall_instance1.xy = (36, 21)
            wall_instance1.wh = (88, 38)
            objects_map['fixed wall 1'] = wall_instance1
            wall_instance2 = Wall()
            wall_instance2.xy = (8, 21)
            wall_instance2.wh = (20, 38)
            objects_map['fixed wall 2'] = wall_instance2
            wall_instance3 = Wall()
            wall_instance3.xy = (8, 101)
            wall_instance3.wh = (152, 38)
            objects_map['fixed wall 3'] = wall_instance3
            number_of_walls = 4
            i = 0
            while (objects_map.get(f"fixed wall {number_of_walls + i}") != None):
                objects_map.pop(f"fixed wall {number_of_walls + i}")
                i += 1
        elif ram_state[28] == 3:
            wall_instance0 = LavaWall()
            wall_instance0.xy = (144, 61)
            wall_instance0.wh = (16, 37)
            objects_map['lava wall 0'] = wall_instance0
            wall_instance1 = LavaWall()
            wall_instance1.xy = (8, 61)
            wall_instance1.wh = (8, 37)
            objects_map['lava wall 1'] = wall_instance1
            number_of_lava_walls = 2
            i = 0
            while (objects_map.get(f"lava wall {number_of_lava_walls + i}") != None):
                objects_map.pop(f"lava wall {number_of_lava_walls + i}")
                i += 1
            wall_instance0 = Wall()
            wall_instance0.xy = (8, 21)
            wall_instance0.wh = (152, 38)
            objects_map['fixed wall 0'] = wall_instance0
            wall_instance1 = Wall()
            wall_instance1.xy = (120, 101)
            wall_instance1.wh = (40, 38)
            objects_map['fixed wall 1'] = wall_instance1
            wall_instance2 = Wall()
            wall_instance2.xy = (48, 101)
            wall_instance2.wh = (64, 38)
            objects_map['fixed wall 2'] = wall_instance2
            wall_instance3 = Wall()
            wall_instance3.xy = (8, 101)
            wall_instance3.wh = (32, 38)
            objects_map['fixed wall 3'] = wall_instance3
            number_of_walls = 4
            i = 0
            while (objects_map.get(f"fixed wall {number_of_walls + i}") != None):
                objects_map.pop(f"fixed wall {number_of_walls + i}")
                i += 1
        elif ram_state[28] == 4:
            wall_instance0 = LavaWall()
            wall_instance0.xy = (144, 61)
            wall_instance0.wh = (16, 37)
            objects_map['lava wall 0'] = wall_instance0
            wall_instance1 = LavaWall()
            wall_instance1.xy = (8, 61)
            wall_instance1.wh = (8, 37)
            objects_map['lava wall 1'] = wall_instance1
            number_of_lava_walls = 2
            i = 0
            while (objects_map.get(f"lava wall {number_of_lava_walls + i}") != None):
                objects_map.pop(f"lava wall {number_of_lava_walls + i}")
                i += 1
            wall_instance0 = Wall()
            wall_instance0.xy = (120, 21)
            wall_instance0.wh = (40, 38)
            objects_map['fixed wall 0'] = wall_instance0
            wall_instance1 = Wall()
            wall_instance1.xy = (48, 21)
            wall_instance1.wh = (64, 38)
            objects_map['fixed wall 1'] = wall_instance1
            wall_instance2 = Wall()
            wall_instance2.xy = (8, 21)
            wall_instance2.wh = (32, 38)
            objects_map['fixed wall 2'] = wall_instance2
            wall_instance3 = Wall()
            wall_instance3.xy = (88, 101)
            wall_instance3.wh = (72, 38)
            objects_map['fixed wall 3'] = wall_instance3
            wall_instance4 = Wall()
            wall_instance4.xy = (8, 101)
            wall_instance4.wh = (64, 38)
            objects_map['fixed wall 4'] = wall_instance4
            number_of_walls = 5
            i = 0
            while (objects_map.get(f"fixed wall {number_of_walls + i}") != None):
                objects_map.pop(f"fixed wall {number_of_walls + i}")
                i += 1
        elif ram_state[28] == 5:
            wall_instance0 = LavaWall()
            wall_instance0.xy = (120, 61)
            wall_instance0.wh = (40, 37)
            objects_map['lava wall 0'] = wall_instance0
            wall_instance1 = LavaWall()
            wall_instance1.xy = (8, 61)
            wall_instance1.wh = (32, 37)
            objects_map['lava wall 1'] = wall_instance1
            number_of_lava_walls = 2
            i = 0
            while (objects_map.get(f"lava wall {number_of_lava_walls + i}") != None):
                objects_map.pop(f"lava wall {number_of_lava_walls + i}")
                i += 1
            wall_instance0 = Wall()
            wall_instance0.xy = (88, 21)
            wall_instance0.wh = (72, 38)
            objects_map['fixed wall 0'] = wall_instance0
            wall_instance1 = Wall()
            wall_instance1.xy = (8, 21)
            wall_instance1.wh = (64, 38)
            objects_map['fixed wall 1'] = wall_instance1
            wall_instance2 = Wall()
            wall_instance2.xy = (144, 101)
            wall_instance2.wh = (16, 38)
            objects_map['fixed wall 2'] = wall_instance2
            wall_instance3 = Wall()
            wall_instance3.xy = (48, 101)
            wall_instance3.wh = (64, 38)
            objects_map['fixed wall 3'] = wall_instance3
            wall_instance4 = Wall()
            wall_instance4.xy = (8, 101)
            wall_instance4.wh = (8, 38)
            objects_map['fixed wall 4'] = wall_instance4
            number_of_walls = 5
            i = 0
            while (objects_map.get(f"fixed wall {number_of_walls + i}") != None):
                objects_map.pop(f"fixed wall {number_of_walls + i}")
                i += 1
        elif ram_state[28] == 6:
            wall_instance0 = LavaWall()
            wall_instance0.xy = (128, 61)
            wall_instance0.wh = (32, 37)
            objects_map['lava wall 0'] = wall_instance0
            wall_instance1 = LavaWall()
            wall_instance1.xy = (40, 61)
            wall_instance1.wh = (80, 37)
            objects_map['lava wall 1'] = wall_instance1
            wall_instance2 = LavaWall()
            wall_instance2.xy = (8, 61)
            wall_instance2.wh = (24, 37)
            objects_map['lava wall 2'] = wall_instance2
            number_of_lava_walls = 3
            i = 0
            while (objects_map.get(f"lava wall {number_of_lava_walls + i}") != None):
                objects_map.pop(f"lava wall {number_of_lava_walls + i}")
                i += 1
            wall_instance0 = Wall()
            wall_instance0.xy = (144, 21)
            wall_instance0.wh = (16, 38)
            objects_map['fixed wall 0'] = wall_instance0
            wall_instance1 = Wall()
            wall_instance1.xy = (48, 21)
            wall_instance1.wh = (64, 38)
            objects_map['fixed wall 1'] = wall_instance1
            wall_instance2 = Wall()
            wall_instance2.xy = (8, 21)
            wall_instance2.wh = (8, 38)
            objects_map['fixed wall 2'] = wall_instance2
            wall_instance3 = Wall()
            wall_instance3.xy = (136, 101)
            wall_instance3.wh = (24, 38)
            objects_map['fixed wall 3'] = wall_instance3
            wall_instance4 = Wall()
            wall_instance4.xy = (8, 101)
            wall_instance4.wh = (16, 38)
            objects_map['fixed wall 4'] = wall_instance4
            number_of_walls = 5
            i = 0
            while (objects_map.get(f"fixed wall {number_of_walls + i}") != None):
                objects_map.pop(f"fixed wall {number_of_walls + i}")
                i += 1
        elif ram_state[28] == 7:
            wall_instance0 = LavaWall()
            wall_instance0.xy = (144, 61)
            wall_instance0.wh = (16, 37)
            objects_map['lava wall 0'] = wall_instance0
            wall_instance1 = LavaWall()
            wall_instance1.xy = (8, 61)
            wall_instance1.wh = (8, 37)
            objects_map['lava wall 1'] = wall_instance1
            number_of_lava_walls = 2
            i = 0
            while (objects_map.get(f"lava wall {number_of_lava_walls + i}") != None):
                objects_map.pop(f"lava wall {number_of_lava_walls + i}")
                i += 1
            wall_instance0 = Wall()
            wall_instance0.xy = (136, 21)
            wall_instance0.wh = (24, 38)
            objects_map['fixed wall 0'] = wall_instance0
            wall_instance1 = Wall()
            wall_instance1.xy = (8, 21)
            wall_instance1.wh = (16, 38)
            objects_map['fixed wall 1'] = wall_instance1
            wall_instance2 = Wall()
            wall_instance2.xy = (8, 101)
            wall_instance2.wh = (152, 38)
            objects_map['fixed wall 2'] = wall_instance2
            number_of_walls = 3
            i = 0
            while (objects_map.get(f"fixed wall {number_of_walls + i}") != None):
                objects_map.pop(f"fixed wall {number_of_walls + i}")
                i += 1
        elif ram_state[28] == 8:
            wall_instance0 = LavaWall()
            wall_instance0.xy = (144, 61)
            wall_instance0.wh = (16, 37)
            objects_map['lava wall 0'] = wall_instance0
            wall_instance1 = LavaWall()
            wall_instance1.xy = (60, 61)
            wall_instance1.wh = (40, 37)
            objects_map['lava wall 1'] = wall_instance1
            wall_instance2 = LavaWall()
            wall_instance2.xy = (8, 61)
            wall_instance2.wh = (8, 37)
            objects_map['lava wall 2'] = wall_instance2
            number_of_lava_walls = 3
            i = 0
            while (objects_map.get(f"lava wall {number_of_lava_walls + i}") != None):
                objects_map.pop(f"lava wall {number_of_lava_walls + i}")
                i += 1
            wall_instance0 = Wall()
            wall_instance0.xy = (8, 21)
            wall_instance0.wh = (152, 38)
            objects_map['fixed wall 0'] = wall_instance0
            wall_instance1 = Wall()
            wall_instance1.xy = (112, 101)
            wall_instance1.wh = (48, 38)
            objects_map['fixed wall 1'] = wall_instance1
            wall_instance2 = Wall()
            wall_instance2.xy = (8, 101)
            wall_instance2.wh = (40, 38)
            objects_map['fixed wall 2'] = wall_instance2
            number_of_walls = 3
            i = 0
            while (objects_map.get(f"fixed wall {number_of_walls + i}") != None):
                objects_map.pop(f"fixed wall {number_of_walls + i}")
                i += 1
        elif ram_state[28] == 9:
            wall_instance0 = LavaWall()
            wall_instance0.xy = (144, 61)
            wall_instance0.wh = (16, 37)
            objects_map['lava wall 0'] = wall_instance0
            wall_instance1 = LavaWall()
            wall_instance1.xy = (56, 61)
            wall_instance1.wh = (48, 37)
            objects_map['lava wall 1'] = wall_instance1
            wall_instance2 = LavaWall()
            wall_instance2.xy = (8, 61)
            wall_instance2.wh = (8, 37)
            objects_map['lava wall 2'] = wall_instance2
            number_of_lava_walls = 3
            i = 0
            while (objects_map.get(f"lava wall {number_of_lava_walls + i}") != None):
                objects_map.pop(f"lava wall {number_of_lava_walls + i}")
                i += 1
            wall_instance0 = Wall()
            wall_instance0.xy = (112, 21)
            wall_instance0.wh = (48, 38)
            objects_map['fixed wall 0'] = wall_instance0
            wall_instance1 = Wall()
            wall_instance1.xy = (8, 21)
            wall_instance1.wh = (40, 38)
            objects_map['fixed wall 1'] = wall_instance1
            wall_instance2 = Wall()
            wall_instance2.xy = (112, 101)
            wall_instance2.wh = (48, 38)
            objects_map['fixed wall 2'] = wall_instance2
            wall_instance3 = Wall()
            wall_instance3.xy = (8, 101)
            wall_instance3.wh = (40, 38)
            objects_map['fixed wall 3'] = wall_instance3
            number_of_walls = 4
            i = 0
            while (objects_map.get(f"fixed wall {number_of_walls + i}") != None):
                objects_map.pop(f"fixed wall {number_of_walls + i}")
                i += 1
        elif ram_state[28] == 10:
            wall_instance0 = LavaWall()
            wall_instance0.xy = (72, 61)
            wall_instance0.wh = (16, 37)
            objects_map['lava wall 0'] = wall_instance0
            number_of_lava_walls = 1
            i = 0
            while (objects_map.get(f"lava wall {number_of_lava_walls + i}") != None):
                objects_map.pop(f"lava wall {number_of_lava_walls + i}")
                i += 1
            wall_instance0 = Wall()
            wall_instance0.xy = (112, 21)
            wall_instance0.wh = (48, 38)
            objects_map['fixed wall 0'] = wall_instance0
            wall_instance1 = Wall()
            wall_instance1.xy = (8, 21)
            wall_instance1.wh = (40, 38)
            objects_map['fixed wall 1'] = wall_instance1
            wall_instance2 = Wall()
            wall_instance2.xy = (136, 101)
            wall_instance2.wh = (24, 38)
            objects_map['fixed wall 2'] = wall_instance2
            wall_instance3 = Wall()
            wall_instance3.xy = (68, 101)
            wall_instance3.wh = (24, 38)
            objects_map['fixed wall 3'] = wall_instance3
            wall_instance4 = Wall()
            wall_instance4.xy = (8, 101)
            wall_instance4.wh = (16, 38)
            objects_map['fixed wall 4'] = wall_instance4
            number_of_walls = 5
            i = 0
            while (objects_map.get(f"fixed wall {number_of_walls + i}") != None):
                objects_map.pop(f"fixed wall {number_of_walls + i}")
                i += 1
        elif ram_state[28] == 11:
            number_of_lava_walls = 0
            i = 0
            while (objects_map.get(f"lava wall {number_of_lava_walls + i}") != None):
                objects_map.pop(f"lava wall {number_of_lava_walls + i}")
                i += 1
            wall_instance0 = Wall()
            wall_instance0.xy = (8, 21)
            wall_instance0.wh = (152, 38)
            objects_map['fixed wall 0'] = wall_instance0
            wall_instance1 = Wall()
            wall_instance1.xy = (144, 101)
            wall_instance1.wh = (16, 38)
            objects_map['fixed wall 1'] = wall_instance1
            wall_instance2 = Wall()
            wall_instance2.xy = (68, 101)
            wall_instance2.wh = (24, 38)
            objects_map['fixed wall 2'] = wall_instance2
            wall_instance3 = Wall()
            wall_instance3.xy = (8, 101)
            wall_instance3.wh = (8, 38)
            objects_map['fixed wall 3'] = wall_instance3
            number_of_walls = 4
            i = 0
            while (objects_map.get(f"fixed wall {number_of_walls + i}") != None):
                objects_map.pop(f"fixed wall {number_of_walls + i}")
                i += 1
        elif ram_state[28] == 12:
            number_of_lava_walls = 0
            i = 0
            while (objects_map.get(f"lava wall {number_of_lava_walls + i}") != None):
                objects_map.pop(f"lava wall {number_of_lava_walls + i}")
                i += 1
            wall_instance0 = Wall()
            wall_instance0.xy = (8, 21)
            wall_instance0.wh = (152, 38)
            objects_map['fixed wall 0'] = wall_instance0
            wall_instance1 = Wall()
            wall_instance1.xy = (72, 61)
            wall_instance1.wh = (16, 37)
            objects_map['fixed wall 1'] = wall_instance1
            wall_instance2 = Wall()
            wall_instance2.xy = (112, 101)
            wall_instance2.wh = (48, 38)
            objects_map['fixed wall 2'] = wall_instance2
            wall_instance3 = Wall()
            wall_instance3.xy = (8, 101)
            wall_instance3.wh = (40, 38)
            objects_map['fixed wall 3'] = wall_instance3
            number_of_walls = 4
            i = 0
            while (objects_map.get(f"fixed wall {number_of_walls + i}") != None):
                objects_map.pop(f"fixed wall {number_of_walls + i}")
                i += 1
        elif ram_state[28] == 13:
            number_of_lava_walls = 0
            i = 0
            while (objects_map.get(f"lava wall {number_of_lava_walls + i}") != None):
                objects_map.pop(f"lava wall {number_of_lava_walls + i}")
                i += 1
            wall_instance0 = Wall()
            wall_instance0.xy = (8, 21)
            wall_instance0.wh = (152, 38)
            objects_map['fixed wall 0'] = wall_instance0
            wall_instance1 = Wall()
            wall_instance1.xy = (144, 101)
            wall_instance1.wh = (16, 38)
            objects_map['fixed wall 1'] = wall_instance1
            wall_instance2 = Wall()
            wall_instance2.xy = (72, 101)
            wall_instance2.wh = (16, 38)
            objects_map['fixed wall 2'] = wall_instance2
            wall_instance3 = Wall()
            wall_instance3.xy = (8, 101)
            wall_instance3.wh = (8, 38)
            objects_map['fixed wall 3'] = wall_instance3
            number_of_walls = 4
            i = 0
            while (objects_map.get(f"fixed wall {number_of_walls + i}") != None):
                objects_map.pop(f"fixed wall {number_of_walls + i}")
                i += 1
        elif ram_state[28] == 14:
            wall_instance0 = LavaWall()
            wall_instance0.xy = (72, 61)
            wall_instance0.wh = (16, 37)
            objects_map['lava wall 0'] = wall_instance0
            number_of_lava_walls = 1
            i = 0
            while (objects_map.get(f"lava wall {number_of_lava_walls + i}") != None):
                objects_map.pop(f"lava wall {number_of_lava_walls + i}")
                i += 1
            wall_instance0 = Wall()
            wall_instance0.xy = (8, 21)
            wall_instance0.wh = (152, 38)
            objects_map['fixed wall 0'] = wall_instance0
            wall_instance1 = Wall()
            wall_instance1.xy = (136, 101)
            wall_instance1.wh = (24, 38)
            objects_map['fixed wall 1'] = wall_instance1
            wall_instance2 = Wall()
            wall_instance2.xy = (8, 101)
            wall_instance2.wh = (16, 38)
            objects_map['fixed wall 2'] = wall_instance2
            number_of_walls = 3
            i = 0
            while (objects_map.get(f"fixed wall {number_of_walls + i}") != None):
                objects_map.pop(f"fixed wall {number_of_walls + i}")
                i += 1
        elif ram_state[28] == 15:
            number_of_lava_walls = 0
            i = 0
            while (objects_map.get(f"lava wall {number_of_lava_walls + i}") != None):
                objects_map.pop(f"lava wall {number_of_lava_walls + i}")
                i += 1
            wall_instance0 = Wall()
            wall_instance0.xy = (8, 21)
            wall_instance0.wh = (152, 38)
            objects_map['fixed wall 0'] = wall_instance0
            wall_instance1 = Wall()
            wall_instance1.xy = (112, 101)
            wall_instance1.wh = (48, 38)
            objects_map['fixed wall 1'] = wall_instance1
            wall_instance2 = Wall()
            wall_instance2.xy = (8, 101)
            wall_instance2.wh = (40, 38)
            objects_map['fixed wall 2'] = wall_instance2
            number_of_walls = 3
            i = 0
            while (objects_map.get(f"fixed wall {number_of_walls + i}") != None):
                objects_map.pop(f"fixed wall {number_of_walls + i}")
                i += 1

    elif ram_state[117] == 12:
        if ram_state[28] == 0:
            wall_instance0 = LavaWall()
            wall_instance0.xy = (144, 61)
            wall_instance0.wh = (16, 37)
            objects_map['lava wall 0'] = wall_instance0
            wall_instance1 = LavaWall()
            wall_instance1.xy = (8, 61)
            wall_instance1.wh = (8, 37)
            objects_map['lava wall 1'] = wall_instance1
            number_of_lava_walls = 2
            i = 0
            while (objects_map.get(f"lava wall {number_of_lava_walls + i}") != None):
                objects_map.pop(f"lava wall {number_of_lava_walls + i}")
                i += 1
            wall_instance0 = Wall()
            wall_instance0.xy = (136, 21)
            wall_instance0.wh = (24, 38)
            objects_map['fixed wall 0'] = wall_instance0
            wall_instance1 = Wall()
            wall_instance1.xy = (8, 21)
            wall_instance1.wh = (16, 38)
            objects_map['fixed wall 1'] = wall_instance1
            wall_instance2 = Wall()
            wall_instance2.xy = (88, 101)
            wall_instance2.wh = (72, 38)
            objects_map['fixed wall 2'] = wall_instance2
            wall_instance3 = Wall()
            wall_instance3.xy = (8, 101)
            wall_instance3.wh = (64, 38)
            objects_map['fixed wall 3'] = wall_instance3
            number_of_walls = 4
            i = 0
            while (objects_map.get(f"fixed wall {number_of_walls + i}") != None):
                objects_map.pop(f"fixed wall {number_of_walls + i}")
                i += 1
        elif ram_state[28] == 1:
            wall_instance0 = LavaWall()
            wall_instance0.xy = (144, 61)
            wall_instance0.wh = (16, 37)
            objects_map['lava wall 0'] = wall_instance0
            wall_instance1 = LavaWall()
            wall_instance1.xy = (92, 61)
            wall_instance1.wh = (12, 37)
            objects_map['lava wall 1'] = wall_instance1
            wall_instance2 = LavaWall()
            wall_instance2.xy = (56, 61)
            wall_instance2.wh = (12, 37)
            objects_map['lava wall 2'] = wall_instance2
            wall_instance3 = LavaWall()
            wall_instance3.xy = (8, 61)
            wall_instance3.wh = (8, 37)
            objects_map['lava wall 3'] = wall_instance3
            number_of_lava_walls = 4
            i = 0
            while (objects_map.get(f"lava wall {number_of_lava_walls + i}") != None):
                objects_map.pop(f"lava wall {number_of_lava_walls + i}")
                i += 1
            wall_instance0 = Wall()
            wall_instance0.xy = (88, 21)
            wall_instance0.wh = (72, 38)
            objects_map['fixed wall 0'] = wall_instance0
            wall_instance1 = Wall()
            wall_instance1.xy = (8, 21)
            wall_instance1.wh = (64, 38)
            objects_map['fixed wall 1'] = wall_instance1
            wall_instance2 = Wall()
            wall_instance2.xy = (140, 101)
            wall_instance2.wh = (20, 38)
            objects_map['fixed wall 2'] = wall_instance2
            wall_instance3 = Wall()
            wall_instance3.xy = (116, 101)
            wall_instance3.wh = (16, 38)
            objects_map['fixed wall 3'] = wall_instance3
            wall_instance4 = Wall()
            wall_instance4.xy = (88, 101)
            wall_instance4.wh = (20, 38)
            objects_map['fixed wall 4'] = wall_instance4
            wall_instance5 = Wall()
            wall_instance5.xy = (52, 101)
            wall_instance5.wh = (20, 38)
            objects_map['fixed wall 5'] = wall_instance5
            wall_instance6 = Wall()
            wall_instance6.xy = (28, 101)
            wall_instance6.wh = (16, 38)
            objects_map['fixed wall 6'] = wall_instance6
            wall_instance7 = Wall()
            wall_instance7.xy = (8, 101)
            wall_instance7.wh = (12, 38)
            objects_map['fixed wall 7'] = wall_instance7
            number_of_walls = 8
            i = 0
            while (objects_map.get(f"fixed wall {number_of_walls + i}") != None):
                objects_map.pop(f"fixed wall {number_of_walls + i}")
                i += 1
        elif ram_state[28] == 2:
            wall_instance0 = LavaWall()
            wall_instance0.xy = (140, 61)
            wall_instance0.wh = (20, 37)
            objects_map['lava wall 0'] = wall_instance0
            wall_instance1 = LavaWall()
            wall_instance1.xy = (120, 61)
            wall_instance1.wh = (12, 37)
            objects_map['lava wall 1'] = wall_instance1
            wall_instance2 = LavaWall()
            wall_instance2.xy = (28, 61)
            wall_instance2.wh = (12, 37)
            objects_map['lava wall 2'] = wall_instance2
            wall_instance3 = LavaWall()
            wall_instance3.xy = (8, 61)
            wall_instance3.wh = (12, 37)
            objects_map['lava wall 3'] = wall_instance3
            number_of_lava_walls = 4
            i = 0
            while (objects_map.get(f"lava wall {number_of_lava_walls + i}") != None):
                objects_map.pop(f"lava wall {number_of_lava_walls + i}")
                i += 1
            wall_instance0 = Wall()
            wall_instance0.xy = (140, 21)
            wall_instance0.wh = (20, 38)
            objects_map['fixed wall 0'] = wall_instance0
            wall_instance1 = Wall()
            wall_instance1.xy = (116, 21)
            wall_instance1.wh = (16, 38)
            objects_map['fixed wall 1'] = wall_instance1
            wall_instance2 = Wall()
            wall_instance2.xy = (88, 21)
            wall_instance2.wh = (20, 38)
            objects_map['fixed wall 2'] = wall_instance2
            wall_instance3 = Wall()
            wall_instance3.xy = (52, 21)
            wall_instance3.wh = (20, 38)
            objects_map['fixed wall 3'] = wall_instance3
            wall_instance4 = Wall()
            wall_instance4.xy = (28, 21)
            wall_instance4.wh = (16, 38)
            objects_map['fixed wall 4'] = wall_instance4
            wall_instance5 = Wall()
            wall_instance5.xy = (8, 21)
            wall_instance5.wh = (12, 38)
            objects_map['fixed wall 5'] = wall_instance5
            wall_instance6 = Wall()
            wall_instance6.xy = (144, 101)
            wall_instance6.wh = (16, 38)
            objects_map['fixed wall 6'] = wall_instance6
            wall_instance7 = Wall()
            wall_instance7.xy = (32, 101)
            wall_instance7.wh = (96, 38)
            objects_map['fixed wall 7'] = wall_instance7
            wall_instance8 = Wall()
            wall_instance8.xy = (8, 101)
            wall_instance8.wh = (8, 38)
            objects_map['fixed wall 8'] = wall_instance8
            number_of_walls = 9
            i = 0
            while (objects_map.get(f"fixed wall {number_of_walls + i}") != None):
                objects_map.pop(f"fixed wall {number_of_walls + i}")
                i += 1
        elif ram_state[28] == 3:
            wall_instance0 = LavaWall()
            wall_instance0.xy = (140, 61)
            wall_instance0.wh = (20, 37)
            objects_map['lava wall 0'] = wall_instance0
            wall_instance1 = LavaWall()
            wall_instance1.xy = (8, 61)
            wall_instance1.wh = (12, 37)
            objects_map['lava wall 1'] = wall_instance1
            number_of_lava_walls = 2
            i = 0
            while (objects_map.get(f"lava wall {number_of_lava_walls + i}") != None):
                objects_map.pop(f"lava wall {number_of_lava_walls + i}")
                i += 1
            wall_instance0 = Wall()
            wall_instance0.xy = (144, 21)
            wall_instance0.wh = (16, 38)
            objects_map['fixed wall 0'] = wall_instance0
            wall_instance1 = Wall()
            wall_instance1.xy = (32, 21)
            wall_instance1.wh = (96, 38)
            objects_map['fixed wall 1'] = wall_instance1
            wall_instance2 = Wall()
            wall_instance2.xy = (8, 21)
            wall_instance2.wh = (8, 38)
            objects_map['fixed wall 2'] = wall_instance2
            wall_instance3 = Wall()
            wall_instance3.xy = (120, 101)
            wall_instance3.wh = (40, 38)
            objects_map['fixed wall 3'] = wall_instance3
            wall_instance4 = Wall()
            wall_instance4.xy = (48, 101)
            wall_instance4.wh = (64, 38)
            objects_map['fixed wall 4'] = wall_instance4
            wall_instance5 = Wall()
            wall_instance5.xy = (8, 101)
            wall_instance5.wh = (32, 38)
            objects_map['fixed wall 5'] = wall_instance5
            number_of_walls = 6
            i = 0
            while (objects_map.get(f"fixed wall {number_of_walls + i}") != None):
                objects_map.pop(f"fixed wall {number_of_walls + i}")
                i += 1
        elif ram_state[28] == 4:
            wall_instance0 = LavaWall()
            wall_instance0.xy = (128, 61)
            wall_instance0.wh = (32, 37)
            objects_map['lava wall 0'] = wall_instance0
            wall_instance1 = LavaWall()
            wall_instance1.xy = (8, 61)
            wall_instance1.wh = (24, 37)
            objects_map['lava wall 1'] = wall_instance1
            number_of_lava_walls = 2
            i = 0
            while (objects_map.get(f"lava wall {number_of_lava_walls + i}") != None):
                objects_map.pop(f"lava wall {number_of_lava_walls + i}")
                i += 1
            wall_instance0 = Wall()
            wall_instance0.xy = (120, 21)
            wall_instance0.wh = (40, 38)
            objects_map['fixed wall 0'] = wall_instance0
            wall_instance1 = Wall()
            wall_instance1.xy = (48, 21)
            wall_instance1.wh = (64, 38)
            objects_map['fixed wall 1'] = wall_instance1
            wall_instance2 = Wall()
            wall_instance2.xy = (8, 21)
            wall_instance2.wh = (32, 38)
            objects_map['fixed wall 2'] = wall_instance2
            wall_instance3 = Wall()
            wall_instance3.xy = (144, 101)
            wall_instance3.wh = (16, 38)
            objects_map['fixed wall 3'] = wall_instance3
            wall_instance4 = Wall()
            wall_instance4.xy = (40, 101)
            wall_instance4.wh = (80, 38)
            objects_map['fixed wall 4'] = wall_instance4
            wall_instance5 = Wall()
            wall_instance5.xy = (8, 101)
            wall_instance5.wh = (8, 38)
            objects_map['fixed wall 5'] = wall_instance5
            number_of_walls = 6
            i = 0
            while (objects_map.get(f"fixed wall {number_of_walls + i}") != None):
                objects_map.pop(f"fixed wall {number_of_walls + i}")
                i += 1
        elif ram_state[28] == 5:
            wall_instance0 = LavaWall()
            wall_instance0.xy = (136, 61)
            wall_instance0.wh = (24, 37)
            objects_map['lava wall 0'] = wall_instance0
            wall_instance1 = LavaWall()
            wall_instance1.xy = (40, 61)
            wall_instance1.wh = (80, 37)
            objects_map['lava wall 1'] = wall_instance1
            wall_instance2 = LavaWall()
            wall_instance2.xy = (8, 61)
            wall_instance2.wh = (16, 37)
            objects_map['lava wall 2'] = wall_instance2
            number_of_lava_walls = 3
            i = 0
            while (objects_map.get(f"lava wall {number_of_lava_walls + i}") != None):
                objects_map.pop(f"lava wall {number_of_lava_walls + i}")
                i += 1
            wall_instance0 = Wall()
            wall_instance0.xy = (144, 21)
            wall_instance0.wh = (16, 38)
            objects_map['fixed wall 0'] = wall_instance0
            wall_instance1 = Wall()
            wall_instance1.xy = (40, 21)
            wall_instance1.wh = (80, 38)
            objects_map['fixed wall 1'] = wall_instance1
            wall_instance2 = Wall()
            wall_instance2.xy = (8, 21)
            wall_instance2.wh = (8, 38)
            objects_map['fixed wall 2'] = wall_instance2
            wall_instance3 = Wall()
            wall_instance3.xy = (144, 101)
            wall_instance3.wh = (16, 38)
            objects_map['fixed wall 3'] = wall_instance3
            wall_instance4 = Wall()
            wall_instance4.xy = (32, 101)
            wall_instance4.wh = (96, 38)
            objects_map['fixed wall 4'] = wall_instance4
            wall_instance5 = Wall()
            wall_instance5.xy = (8, 101)
            wall_instance5.wh = (8, 38)
            objects_map['fixed wall 5'] = wall_instance5
            number_of_walls = 6
            i = 0
            while (objects_map.get(f"fixed wall {number_of_walls + i}") != None):
                objects_map.pop(f"fixed wall {number_of_walls + i}")
                i += 1
        elif ram_state[28] == 6:
            wall_instance0 = LavaWall()
            wall_instance0.xy = (144, 61)
            wall_instance0.wh = (16, 37)
            objects_map['lava wall 0'] = wall_instance0
            wall_instance1 = LavaWall()
            wall_instance1.xy = (40, 61)
            wall_instance1.wh = (80, 37)
            objects_map['lava wall 1'] = wall_instance1
            wall_instance2 = LavaWall()
            wall_instance2.xy = (8, 61)
            wall_instance2.wh = (8, 37)
            objects_map['lava wall 2'] = wall_instance2
            number_of_lava_walls = 3
            i = 0
            while (objects_map.get(f"lava wall {number_of_lava_walls + i}") != None):
                objects_map.pop(f"lava wall {number_of_lava_walls + i}")
                i += 1
            wall_instance0 = Wall()
            wall_instance0.xy = (144, 21)
            wall_instance0.wh = (16, 38)
            objects_map['fixed wall 0'] = wall_instance0
            wall_instance1 = Wall()
            wall_instance1.xy = (32, 21)
            wall_instance1.wh = (96, 38)
            objects_map['fixed wall 1'] = wall_instance1
            wall_instance2 = Wall()
            wall_instance2.xy = (8, 21)
            wall_instance2.wh = (8, 38)
            objects_map['fixed wall 2'] = wall_instance2
            wall_instance3 = Wall()
            wall_instance3.xy = (8, 101)
            wall_instance3.wh = (152, 38)
            objects_map['fixed wall 3'] = wall_instance3
            number_of_walls = 4
            i = 0
            while (objects_map.get(f"fixed wall {number_of_walls + i}") != None):
                objects_map.pop(f"fixed wall {number_of_walls + i}")
                i += 1
        elif ram_state[28] == 7:
            wall_instance0 = LavaWall()
            wall_instance0.xy = (144, 61)
            wall_instance0.wh = (16, 37)
            objects_map['lava wall 0'] = wall_instance0
            wall_instance1 = LavaWall()
            wall_instance1.xy = (8, 61)
            wall_instance1.wh = (8, 37)
            objects_map['lava wall 1'] = wall_instance1
            number_of_lava_walls = 2
            i = 0
            while (objects_map.get(f"lava wall {number_of_lava_walls + i}") != None):
                objects_map.pop(f"lava wall {number_of_lava_walls + i}")
                i += 1
            wall_instance0 = Wall()
            wall_instance0.xy = (8, 21)
            wall_instance0.wh = (152, 38)
            objects_map['fixed wall 0'] = wall_instance0
            wall_instance1 = Wall()
            wall_instance1.xy = (88, 101)
            wall_instance1.wh = (72, 38)
            objects_map['fixed wall 1'] = wall_instance1
            wall_instance2 = Wall()
            wall_instance2.xy = (8, 101)
            wall_instance2.wh = (64, 38)
            objects_map['fixed wall 2'] = wall_instance2
            number_of_walls = 3
            i = 0
            while (objects_map.get(f"fixed wall {number_of_walls + i}") != None):
                objects_map.pop(f"fixed wall {number_of_walls + i}")
                i += 1
        elif ram_state[28] == 8:
            number_of_lava_walls = 0
            i = 0
            while (objects_map.get(f"lava wall {number_of_lava_walls + i}") != None):
                objects_map.pop(f"lava wall {number_of_lava_walls + i}")
                i += 1
            wall_instance0 = Wall()
            wall_instance0.xy = (88, 21)
            wall_instance0.wh = (72, 38)
            objects_map['fixed wall 0'] = wall_instance0
            wall_instance1 = Wall()
            wall_instance1.xy = (8, 21)
            wall_instance1.wh = (64, 38)
            objects_map['fixed wall 1'] = wall_instance1
            wall_instance2 = Wall()
            wall_instance2.xy = (144, 61)
            wall_instance2.wh = (16, 37)
            objects_map['fixed wall 2'] = wall_instance2
            wall_instance3 = Wall()
            wall_instance3.xy = (8, 61)
            wall_instance3.wh = (8, 37)
            objects_map['fixed wall 3'] = wall_instance3
            wall_instance4 = Wall()
            wall_instance4.xy = (116, 101)
            wall_instance4.wh = (44, 38)
            objects_map['fixed wall 4'] = wall_instance4
            wall_instance5 = Wall()
            wall_instance5.xy = (52, 101)
            wall_instance5.wh = (56, 38)
            objects_map['fixed wall 5'] = wall_instance5
            wall_instance6 = Wall()
            wall_instance6.xy = (8, 101)
            wall_instance6.wh = (36, 38)
            objects_map['fixed wall 6'] = wall_instance6
            number_of_walls = 7
            i = 0
            while (objects_map.get(f"fixed wall {number_of_walls + i}") != None):
                objects_map.pop(f"fixed wall {number_of_walls + i}")
                i += 1
        elif ram_state[28] == 9:
            wall_instance0 = LavaWall()
            wall_instance0.xy = (144, 61)
            wall_instance0.wh = (16, 37)
            objects_map['lava wall 0'] = wall_instance0
            wall_instance1 = LavaWall()
            wall_instance1.xy = (8, 61)
            wall_instance1.wh = (8, 37)
            objects_map['lava wall 1'] = wall_instance1
            number_of_lava_walls = 2
            i = 0
            while (objects_map.get(f"lava wall {number_of_lava_walls + i}") != None):
                objects_map.pop(f"lava wall {number_of_lava_walls + i}")
                i += 1
            wall_instance0 = Wall()
            wall_instance0.xy = (116, 21)
            wall_instance0.wh = (44, 38)
            objects_map['fixed wall 0'] = wall_instance0
            wall_instance1 = Wall()
            wall_instance1.xy = (52, 21)
            wall_instance1.wh = (56, 38)
            objects_map['fixed wall 1'] = wall_instance1
            wall_instance2 = Wall()
            wall_instance2.xy = (8, 21)
            wall_instance2.wh = (36, 38)
            objects_map['fixed wall 2'] = wall_instance2
            wall_instance3 = Wall()
            wall_instance3.xy = (8, 101)
            wall_instance3.wh = (152, 38)
            objects_map['fixed wall 3'] = wall_instance3
            number_of_walls = 4
            i = 0
            while (objects_map.get(f"fixed wall {number_of_walls + i}") != None):
                objects_map.pop(f"fixed wall {number_of_walls + i}")
                i += 1
        elif ram_state[28] == 10:
            number_of_lava_walls = 0
            i = 0
            while (objects_map.get(f"lava wall {number_of_lava_walls + i}") != None):
                objects_map.pop(f"lava wall {number_of_lava_walls + i}")
                i += 1
            wall_instance0 = Wall()
            wall_instance0.xy = (8, 21)
            wall_instance0.wh = (152, 38)
            objects_map['fixed wall 0'] = wall_instance0
            wall_instance1 = Wall()
            wall_instance1.xy = (8, 101)
            wall_instance1.wh = (152, 38)
            objects_map['fixed wall 1'] = wall_instance1
            number_of_walls = 2
            i = 0
            while (objects_map.get(f"fixed wall {number_of_walls + i}") != None):
                objects_map.pop(f"fixed wall {number_of_walls + i}")
                i += 1
        elif ram_state[28] == 11:
            number_of_lava_walls = 0
            i = 0
            while (objects_map.get(f"lava wall {number_of_lava_walls + i}") != None):
                objects_map.pop(f"lava wall {number_of_lava_walls + i}")
                i += 1
            wall_instance0 = Wall()
            wall_instance0.xy = (8, 21)
            wall_instance0.wh = (152, 38)
            objects_map['fixed wall 0'] = wall_instance0
            wall_instance1 = Wall()
            wall_instance1.xy = (136, 101)
            wall_instance1.wh = (24, 38)
            objects_map['fixed wall 1'] = wall_instance1
            wall_instance2 = Wall()
            wall_instance2.xy = (68, 101)
            wall_instance2.wh = (24, 38)
            objects_map['fixed wall 2'] = wall_instance2
            wall_instance3 = Wall()
            wall_instance3.xy = (8, 101)
            wall_instance3.wh = (16, 38)
            objects_map['fixed wall 3'] = wall_instance3
            number_of_walls = 4
            i = 0
            while (objects_map.get(f"fixed wall {number_of_walls + i}") != None):
                objects_map.pop(f"fixed wall {number_of_walls + i}")
                i += 1
        elif ram_state[28] == 12:
            wall_instance0 = LavaWall()
            wall_instance0.xy = (68, 61)
            wall_instance0.wh = (24, 37)
            objects_map['lava wall 0'] = wall_instance0
            number_of_lava_walls = 1
            i = 0
            while (objects_map.get(f"lava wall {number_of_lava_walls + i}") != None):
                objects_map.pop(f"lava wall {number_of_lava_walls + i}")
                i += 1
            wall_instance0 = Wall()
            wall_instance0.xy = (8, 21)
            wall_instance0.wh = (152, 38)
            objects_map['fixed wall 0'] = wall_instance0
            wall_instance1 = Wall()
            wall_instance1.xy = (136, 101)
            wall_instance1.wh = (24, 38)
            objects_map['fixed wall 1'] = wall_instance1
            wall_instance2 = Wall()
            wall_instance2.xy = (8, 101)
            wall_instance2.wh = (16, 38)
            objects_map['fixed wall 2'] = wall_instance2
            number_of_walls = 3
            i = 0
            while (objects_map.get(f"fixed wall {number_of_walls + i}") != None):
                objects_map.pop(f"fixed wall {number_of_walls + i}")
                i += 1
        elif ram_state[28] == 13:
            number_of_lava_walls = 0
            i = 0
            while (objects_map.get(f"lava wall {number_of_lava_walls + i}") != None):
                objects_map.pop(f"lava wall {number_of_lava_walls + i}")
                i += 1
            wall_instance0 = Wall()
            wall_instance0.xy = (8, 21)
            wall_instance0.wh = (152, 38)
            objects_map['fixed wall 0'] = wall_instance0
            wall_instance1 = Wall()
            wall_instance1.xy = (136, 101)
            wall_instance1.wh = (24, 38)
            objects_map['fixed wall 1'] = wall_instance1
            wall_instance2 = Wall()
            wall_instance2.xy = (72, 101)
            wall_instance2.wh = (16, 38)
            objects_map['fixed wall 2'] = wall_instance2
            wall_instance3 = Wall()
            wall_instance3.xy = (8, 101)
            wall_instance3.wh = (16, 38)
            objects_map['fixed wall 3'] = wall_instance3
            number_of_walls = 4
            i = 0
            while (objects_map.get(f"fixed wall {number_of_walls + i}") != None):
                objects_map.pop(f"fixed wall {number_of_walls + i}")
                i += 1
        elif ram_state[28] == 14:
            number_of_lava_walls = 0
            i = 0
            while (objects_map.get(f"lava wall {number_of_lava_walls + i}") != None):
                objects_map.pop(f"lava wall {number_of_lava_walls + i}")
                i += 1
            wall_instance0 = Wall()
            wall_instance0.xy = (8, 21)
            wall_instance0.wh = (152, 38)
            objects_map['fixed wall 0'] = wall_instance0
            wall_instance1 = Wall()
            wall_instance1.xy = (112, 101)
            wall_instance1.wh = (48, 38)
            objects_map['fixed wall 1'] = wall_instance1
            wall_instance2 = Wall()
            wall_instance2.xy = (64, 101)
            wall_instance2.wh = (32, 38)
            objects_map['fixed wall 2'] = wall_instance2
            wall_instance3 = Wall()
            wall_instance3.xy = (8, 101)
            wall_instance3.wh = (40, 38)
            objects_map['fixed wall 3'] = wall_instance3
            number_of_walls = 4
            i = 0
            while (objects_map.get(f"fixed wall {number_of_walls + i}") != None):
                objects_map.pop(f"fixed wall {number_of_walls + i}")
                i += 1
        elif ram_state[28] == 15:
            number_of_lava_walls = 0
            i = 0
            while (objects_map.get(f"lava wall {number_of_lava_walls + i}") != None):
                objects_map.pop(f"lava wall {number_of_lava_walls + i}")
                i += 1
            wall_instance0 = Wall()
            wall_instance0.xy = (8, 21)
            wall_instance0.wh = (152, 38)
            objects_map['fixed wall 0'] = wall_instance0
            wall_instance1 = Wall()
            wall_instance1.xy = (112, 101)
            wall_instance1.wh = (48, 38)
            objects_map['fixed wall 1'] = wall_instance1
            wall_instance2 = Wall()
            wall_instance2.xy = (8, 101)
            wall_instance2.wh = (40, 38)
            objects_map['fixed wall 2'] = wall_instance2
            number_of_walls = 3
            i = 0
            while (objects_map.get(f"fixed wall {number_of_walls + i}") != None):
                objects_map.pop(f"fixed wall {number_of_walls + i}")
                i += 1

    elif ram_state[117] == 13:
        if ram_state[28] == 0:
            wall_instance0 = LavaWall()
            wall_instance0.xy = (144, 61)
            wall_instance0.wh = (16, 37)
            objects_map['lava wall 0'] = wall_instance0
            wall_instance1 = LavaWall()
            wall_instance1.xy = (8, 61)
            wall_instance1.wh = (8, 37)
            objects_map['lava wall 1'] = wall_instance1
            number_of_lava_walls = 2
            i = 0
            while (objects_map.get(f"lava wall {number_of_lava_walls + i}") != None):
                objects_map.pop(f"lava wall {number_of_lava_walls + i}")
                i += 1
            wall_instance0 = Wall()
            wall_instance0.xy = (136, 21)
            wall_instance0.wh = (24, 38)
            objects_map['fixed wall 0'] = wall_instance0
            wall_instance1 = Wall()
            wall_instance1.xy = (8, 21)
            wall_instance1.wh = (16, 38)
            objects_map['fixed wall 1'] = wall_instance1
            wall_instance2 = Wall()
            wall_instance2.xy = (88, 101)
            wall_instance2.wh = (72, 38)
            objects_map['fixed wall 2'] = wall_instance2
            wall_instance3 = Wall()
            wall_instance3.xy = (8, 101)
            wall_instance3.wh = (64, 38)
            objects_map['fixed wall 3'] = wall_instance3
            number_of_walls = 4
            i = 0
            while (objects_map.get(f"fixed wall {number_of_walls + i}") != None):
                objects_map.pop(f"fixed wall {number_of_walls + i}")
                i += 1
        elif ram_state[28] == 1:
            wall_instance0 = LavaWall()
            wall_instance0.xy = (80, 61)
            wall_instance0.wh = (16, 37)
            objects_map['lava wall 0'] = wall_instance0
            wall_instance1 = LavaWall()
            wall_instance1.xy = (8, 61)
            wall_instance1.wh = (8, 37)
            objects_map['lava wall 1'] = wall_instance1
            number_of_lava_walls = 2
            i = 0
            while (objects_map.get(f"lava wall {number_of_lava_walls + i}") != None):
                objects_map.pop(f"lava wall {number_of_lava_walls + i}")
                i += 1
            wall_instance0 = Wall()
            wall_instance0.xy = (88, 21)
            wall_instance0.wh = (72, 38)
            objects_map['fixed wall 0'] = wall_instance0
            wall_instance1 = Wall()
            wall_instance1.xy = (8, 21)
            wall_instance1.wh = (64, 38)
            objects_map['fixed wall 1'] = wall_instance1
            wall_instance2 = Wall()
            wall_instance2.xy = (8, 101)
            wall_instance2.wh = (152, 38)
            objects_map['fixed wall 2'] = wall_instance2
            number_of_walls = 3
            i = 0
            while (objects_map.get(f"fixed wall {number_of_walls + i}") != None):
                objects_map.pop(f"fixed wall {number_of_walls + i}")
                i += 1
        elif ram_state[28] == 2:
            wall_instance0 = LavaWall()
            wall_instance0.xy = (144, 61)
            wall_instance0.wh = (16, 37)
            objects_map['lava wall 0'] = wall_instance0
            wall_instance1 = LavaWall()
            wall_instance1.xy = (8, 61)
            wall_instance1.wh = (8, 37)
            objects_map['lava wall 1'] = wall_instance1
            number_of_lava_walls = 2
            i = 0
            while (objects_map.get(f"lava wall {number_of_lava_walls + i}") != None):
                objects_map.pop(f"lava wall {number_of_lava_walls + i}")
                i += 1
            wall_instance0 = Wall()
            wall_instance0.xy = (8, 21)
            wall_instance0.wh = (152, 38)
            objects_map['fixed wall 0'] = wall_instance0
            wall_instance1 = Wall()
            wall_instance1.xy = (88, 101)
            wall_instance1.wh = (72, 38)
            objects_map['fixed wall 1'] = wall_instance1
            wall_instance2 = Wall()
            wall_instance2.xy = (8, 101)
            wall_instance2.wh = (64, 38)
            objects_map['fixed wall 2'] = wall_instance2
            number_of_walls = 3
            i = 0
            while (objects_map.get(f"fixed wall {number_of_walls + i}") != None):
                objects_map.pop(f"fixed wall {number_of_walls + i}")
                i += 1
        elif ram_state[28] == 3:
            wall_instance0 = LavaWall()
            wall_instance0.xy = (144, 61)
            wall_instance0.wh = (16, 37)
            objects_map['lava wall 0'] = wall_instance0
            wall_instance1 = LavaWall()
            wall_instance1.xy = (8, 61)
            wall_instance1.wh = (8, 37)
            objects_map['lava wall 1'] = wall_instance1
            number_of_lava_walls = 2
            i = 0
            while (objects_map.get(f"lava wall {number_of_lava_walls + i}") != None):
                objects_map.pop(f"lava wall {number_of_lava_walls + i}")
                i += 1
            wall_instance0 = Wall()
            wall_instance0.xy = (88, 21)
            wall_instance0.wh = (72, 38)
            objects_map['fixed wall 0'] = wall_instance0
            wall_instance1 = Wall()
            wall_instance1.xy = (8, 21)
            wall_instance1.wh = (64, 38)
            objects_map['fixed wall 1'] = wall_instance1
            wall_instance2 = Wall()
            wall_instance2.xy = (8, 101)
            wall_instance2.wh = (152, 38)
            objects_map['fixed wall 2'] = wall_instance2
            number_of_walls = 3
            i = 0
            while (objects_map.get(f"fixed wall {number_of_walls + i}") != None):
                objects_map.pop(f"fixed wall {number_of_walls + i}")
                i += 1
        elif ram_state[28] == 4:
            wall_instance0 = LavaWall()
            wall_instance0.xy = (144, 61)
            wall_instance0.wh = (16, 37)
            objects_map['lava wall 0'] = wall_instance0
            wall_instance1 = LavaWall()
            wall_instance1.xy = (8, 61)
            wall_instance1.wh = (8, 37)
            objects_map['lava wall 1'] = wall_instance1
            number_of_lava_walls = 2
            i = 0
            while (objects_map.get(f"lava wall {number_of_lava_walls + i}") != None):
                objects_map.pop(f"lava wall {number_of_lava_walls + i}")
                i += 1
            wall_instance0 = Wall()
            wall_instance0.xy = (8, 21)
            wall_instance0.wh = (152, 38)
            objects_map['fixed wall 0'] = wall_instance0
            wall_instance1 = Wall()
            wall_instance1.xy = (136, 101)
            wall_instance1.wh = (24, 38)
            objects_map['fixed wall 1'] = wall_instance1
            wall_instance2 = Wall()
            wall_instance2.xy = (88, 101)
            wall_instance2.wh = (32, 38)
            objects_map['fixed wall 2'] = wall_instance2
            wall_instance3 = Wall()
            wall_instance3.xy = (40, 101)
            wall_instance3.wh = (32, 38)
            objects_map['fixed wall 3'] = wall_instance3
            wall_instance4 = Wall()
            wall_instance4.xy = (8, 101)
            wall_instance4.wh = (16, 38)
            objects_map['fixed wall 4'] = wall_instance4
            number_of_walls = 5
            i = 0
            while (objects_map.get(f"fixed wall {number_of_walls + i}") != None):
                objects_map.pop(f"fixed wall {number_of_walls + i}")
                i += 1
        elif ram_state[28] == 5:
            wall_instance0 = LavaWall()
            wall_instance0.xy = (84, 61)
            wall_instance0.wh = (76, 37)
            objects_map['lava wall 0'] = wall_instance0
            wall_instance1 = LavaWall()
            wall_instance1.xy = (8, 61)
            wall_instance1.wh = (68, 37)
            objects_map['lava wall 1'] = wall_instance1
            number_of_lava_walls = 2
            i = 0
            while (objects_map.get(f"lava wall {number_of_lava_walls + i}") != None):
                objects_map.pop(f"lava wall {number_of_lava_walls + i}")
                i += 1
            wall_instance0 = Wall()
            wall_instance0.xy = (136, 21)
            wall_instance0.wh = (24, 38)
            objects_map['fixed wall 0'] = wall_instance0
            wall_instance1 = Wall()
            wall_instance1.xy = (88, 21)
            wall_instance1.wh = (32, 38)
            objects_map['fixed wall 1'] = wall_instance1
            wall_instance2 = Wall()
            wall_instance2.xy = (40, 21)
            wall_instance2.wh = (32, 38)
            objects_map['fixed wall 2'] = wall_instance2
            wall_instance3 = Wall()
            wall_instance3.xy = (8, 21)
            wall_instance3.wh = (16, 38)
            objects_map['fixed wall 3'] = wall_instance3
            wall_instance4 = Wall()
            wall_instance4.xy = (112, 101)
            wall_instance4.wh = (48, 38)
            objects_map['fixed wall 4'] = wall_instance4
            wall_instance5 = Wall()
            wall_instance5.xy = (8, 101)
            wall_instance5.wh = (40, 38)
            objects_map['fixed wall 5'] = wall_instance5
            number_of_walls = 6
            i = 0
            while (objects_map.get(f"fixed wall {number_of_walls + i}") != None):
                objects_map.pop(f"fixed wall {number_of_walls + i}")
                i += 1
        elif ram_state[28] == 6:
            wall_instance0 = LavaWall()
            wall_instance0.xy = (128, 61)
            wall_instance0.wh = (32, 37)
            objects_map['lava wall 0'] = wall_instance0
            wall_instance1 = LavaWall()
            wall_instance1.xy = (48, 61)
            wall_instance1.wh = (48, 37)
            objects_map['lava wall 1'] = wall_instance1
            wall_instance2 = LavaWall()
            wall_instance2.xy = (8, 61)
            wall_instance2.wh = (8, 37)
            objects_map['lava wall 2'] = wall_instance2
            number_of_lava_walls = 3
            i = 0
            while (objects_map.get(f"lava wall {number_of_lava_walls + i}") != None):
                objects_map.pop(f"lava wall {number_of_lava_walls + i}")
                i += 1
            wall_instance0 = Wall()
            wall_instance0.xy = (112, 21)
            wall_instance0.wh = (48, 38)
            objects_map['fixed wall 0'] = wall_instance0
            wall_instance1 = Wall()
            wall_instance1.xy = (8, 21)
            wall_instance1.wh = (40, 38)
            objects_map['fixed wall 1'] = wall_instance1
            wall_instance2 = Wall()
            wall_instance2.xy = (140, 101)
            wall_instance2.wh = (20, 38)
            objects_map['fixed wall 2'] = wall_instance2
            wall_instance3 = Wall()
            wall_instance3.xy = (44, 101)
            wall_instance3.wh = (72, 38)
            objects_map['fixed wall 3'] = wall_instance3
            wall_instance4 = Wall()
            wall_instance4.xy = (8, 101)
            wall_instance4.wh = (12, 38)
            objects_map['fixed wall 4'] = wall_instance4
            number_of_walls = 5
            i = 0
            while (objects_map.get(f"fixed wall {number_of_walls + i}") != None):
                objects_map.pop(f"fixed wall {number_of_walls + i}")
                i += 1
        elif ram_state[28] == 7:
            wall_instance0 = LavaWall()
            wall_instance0.xy = (144, 61)
            wall_instance0.wh = (16, 37)
            objects_map['lava wall 0'] = wall_instance0
            wall_instance1 = LavaWall()
            wall_instance1.xy = (8, 61)
            wall_instance1.wh = (8, 37)
            objects_map['lava wall 1'] = wall_instance1
            number_of_lava_walls = 2
            i = 0
            while (objects_map.get(f"lava wall {number_of_lava_walls + i}") != None):
                objects_map.pop(f"lava wall {number_of_lava_walls + i}")
                i += 1
            wall_instance0 = Wall()
            wall_instance0.xy = (140, 21)
            wall_instance0.wh = (20, 38)
            objects_map['fixed wall 0'] = wall_instance0
            wall_instance1 = Wall()
            wall_instance1.xy = (44, 21)
            wall_instance1.wh = (72, 38)
            objects_map['fixed wall 1'] = wall_instance1
            wall_instance2 = Wall()
            wall_instance2.xy = (8, 21)
            wall_instance2.wh = (12, 38)
            objects_map['fixed wall 2'] = wall_instance2
            wall_instance3 = Wall()
            wall_instance3.xy = (8, 101)
            wall_instance3.wh = (152, 38)
            objects_map['fixed wall 3'] = wall_instance3
            number_of_walls = 4
            i = 0
            while (objects_map.get(f"fixed wall {number_of_walls + i}") != None):
                objects_map.pop(f"fixed wall {number_of_walls + i}")
                i += 1
        elif ram_state[28] == 8:
            wall_instance0 = LavaWall()
            wall_instance0.xy = (144, 61)
            wall_instance0.wh = (16, 37)
            objects_map['lava wall 0'] = wall_instance0
            wall_instance1 = LavaWall()
            wall_instance1.xy = (8, 61)
            wall_instance1.wh = (8, 37)
            objects_map['lava wall 1'] = wall_instance1
            number_of_lava_walls = 2
            i = 0
            while (objects_map.get(f"lava wall {number_of_lava_walls + i}") != None):
                objects_map.pop(f"lava wall {number_of_lava_walls + i}")
                i += 1
            wall_instance0 = Wall()
            wall_instance0.xy = (8, 21)
            wall_instance0.wh = (152, 38)
            objects_map['fixed wall 0'] = wall_instance0
            wall_instance1 = Wall()
            wall_instance1.xy = (136, 101)
            wall_instance1.wh = (24, 38)
            objects_map['fixed wall 1'] = wall_instance1
            wall_instance2 = Wall()
            wall_instance2.xy = (52, 101)
            wall_instance2.wh = (56, 38)
            objects_map['fixed wall 2'] = wall_instance2
            wall_instance3 = Wall()
            wall_instance3.xy = (8, 101)
            wall_instance3.wh = (16, 38)
            objects_map['fixed wall 3'] = wall_instance3
            number_of_walls = 4
            i = 0
            while (objects_map.get(f"fixed wall {number_of_walls + i}") != None):
                objects_map.pop(f"fixed wall {number_of_walls + i}")
                i += 1
        elif ram_state[28] == 9:
            wall_instance0 = LavaWall()
            wall_instance0.xy = (120, 61)
            wall_instance0.wh = (40, 37)
            objects_map['lava wall 0'] = wall_instance0
            wall_instance1 = LavaWall()
            wall_instance1.xy = (8, 61)
            wall_instance1.wh = (32, 37)
            objects_map['lava wall 1'] = wall_instance1
            number_of_lava_walls = 2
            i = 0
            while (objects_map.get(f"lava wall {number_of_lava_walls + i}") != None):
                objects_map.pop(f"lava wall {number_of_lava_walls + i}")
                i += 1
            wall_instance0 = Wall()
            wall_instance0.xy = (136, 21)
            wall_instance0.wh = (24, 38)
            objects_map['fixed wall 0'] = wall_instance0
            wall_instance1 = Wall()
            wall_instance1.xy = (52, 21)
            wall_instance1.wh = (56, 38)
            objects_map['fixed wall 1'] = wall_instance1
            wall_instance2 = Wall()
            wall_instance2.xy = (8, 21)
            wall_instance2.wh = (16, 38)
            objects_map['fixed wall 2'] = wall_instance2
            wall_instance3 = Wall()
            wall_instance3.xy = (84, 101)
            wall_instance3.wh = (76, 38)
            objects_map['fixed wall 3'] = wall_instance3
            wall_instance4 = Wall()
            wall_instance4.xy = (8, 101)
            wall_instance4.wh = (68, 38)
            objects_map['fixed wall 4'] = wall_instance4
            number_of_walls = 5
            i = 0
            while (objects_map.get(f"fixed wall {number_of_walls + i}") != None):
                objects_map.pop(f"fixed wall {number_of_walls + i}")
                i += 1
        elif ram_state[28] == 10:
            number_of_lava_walls = 0
            i = 0
            while (objects_map.get(f"lava wall {number_of_lava_walls + i}") != None):
                objects_map.pop(f"lava wall {number_of_lava_walls + i}")
                i += 1
            wall_instance0 = Wall()
            wall_instance0.xy = (84, 21)
            wall_instance0.wh = (76, 38)
            objects_map['fixed wall 0'] = wall_instance0
            wall_instance1 = Wall()
            wall_instance1.xy = (8, 21)
            wall_instance1.wh = (68, 38)
            objects_map['fixed wall 1'] = wall_instance1
            wall_instance2 = Wall()
            wall_instance2.xy = (104, 61)
            wall_instance2.wh = (16, 37)
            objects_map['fixed wall 2'] = wall_instance2
            wall_instance3 = Wall()
            wall_instance3.xy = (40, 61)
            wall_instance3.wh = (16, 37)
            objects_map['fixed wall 3'] = wall_instance3
            wall_instance4 = Wall()
            wall_instance4.xy = (140, 101)
            wall_instance4.wh = (20, 38)
            objects_map['fixed wall 4'] = wall_instance4
            wall_instance5 = Wall()
            wall_instance5.xy = (8, 101)
            wall_instance5.wh = (12, 38)
            objects_map['fixed wall 5'] = wall_instance5
            number_of_walls = 6
            i = 0
            while (objects_map.get(f"fixed wall {number_of_walls + i}") != None):
                objects_map.pop(f"fixed wall {number_of_walls + i}")
                i += 1
        elif ram_state[28] == 11:
            number_of_lava_walls = 0
            i = 0
            while (objects_map.get(f"lava wall {number_of_lava_walls + i}") != None):
                objects_map.pop(f"lava wall {number_of_lava_walls + i}")
                i += 1
            wall_instance0 = Wall()
            wall_instance0.xy = (8, 21)
            wall_instance0.wh = (152, 38)
            objects_map['fixed wall 0'] = wall_instance0
            wall_instance1 = Wall()
            wall_instance1.xy = (136, 101)
            wall_instance1.wh = (24, 38)
            objects_map['fixed wall 1'] = wall_instance1
            wall_instance2 = Wall()
            wall_instance2.xy = (68, 101)
            wall_instance2.wh = (24, 38)
            objects_map['fixed wall 2'] = wall_instance2
            wall_instance3 = Wall()
            wall_instance3.xy = (8, 101)
            wall_instance3.wh = (16, 38)
            objects_map['fixed wall 3'] = wall_instance3
            number_of_walls = 4
            i = 0
            while (objects_map.get(f"fixed wall {number_of_walls + i}") != None):
                objects_map.pop(f"fixed wall {number_of_walls + i}")
                i += 1
        elif ram_state[28] == 12:
            wall_instance0 = LavaWall()
            wall_instance0.xy = (68, 61)
            wall_instance0.wh = (24, 37)
            objects_map['lava wall 0'] = wall_instance0
            number_of_lava_walls = 1
            i = 0
            while (objects_map.get(f"lava wall {number_of_lava_walls + i}") != None):
                objects_map.pop(f"lava wall {number_of_lava_walls + i}")
                i += 1
            wall_instance0 = Wall()
            wall_instance0.xy = (8, 21)
            wall_instance0.wh = (152, 38)
            objects_map['fixed wall 0'] = wall_instance0
            wall_instance1 = Wall()
            wall_instance1.xy = (136, 101)
            wall_instance1.wh = (24, 38)
            objects_map['fixed wall 1'] = wall_instance1
            wall_instance2 = Wall()
            wall_instance2.xy = (8, 101)
            wall_instance2.wh = (16, 38)
            objects_map['fixed wall 2'] = wall_instance2
            number_of_walls = 3
            i = 0
            while (objects_map.get(f"fixed wall {number_of_walls + i}") != None):
                objects_map.pop(f"fixed wall {number_of_walls + i}")
                i += 1
        elif ram_state[28] == 13:
            number_of_lava_walls = 0
            i = 0
            while (objects_map.get(f"lava wall {number_of_lava_walls + i}") != None):
                objects_map.pop(f"lava wall {number_of_lava_walls + i}")
                i += 1
            wall_instance0 = Wall()
            wall_instance0.xy = (8, 21)
            wall_instance0.wh = (152, 38)
            objects_map['fixed wall 0'] = wall_instance0
            wall_instance1 = Wall()
            wall_instance1.xy = (136, 101)
            wall_instance1.wh = (24, 38)
            objects_map['fixed wall 1'] = wall_instance1
            wall_instance2 = Wall()
            wall_instance2.xy = (72, 101)
            wall_instance2.wh = (16, 38)
            objects_map['fixed wall 2'] = wall_instance2
            wall_instance3 = Wall()
            wall_instance3.xy = (8, 101)
            wall_instance3.wh = (16, 38)
            objects_map['fixed wall 3'] = wall_instance3
            number_of_walls = 4
            i = 0
            while (objects_map.get(f"fixed wall {number_of_walls + i}") != None):
                objects_map.pop(f"fixed wall {number_of_walls + i}")
                i += 1
        elif ram_state[28] == 14:
            number_of_lava_walls = 0
            i = 0
            while (objects_map.get(f"lava wall {number_of_lava_walls + i}") != None):
                objects_map.pop(f"lava wall {number_of_lava_walls + i}")
                i += 1
            wall_instance0 = Wall()
            wall_instance0.xy = (8, 21)
            wall_instance0.wh = (152, 38)
            objects_map['fixed wall 0'] = wall_instance0
            wall_instance1 = Wall()
            wall_instance1.xy = (136, 101)
            wall_instance1.wh = (24, 38)
            objects_map['fixed wall 1'] = wall_instance1
            wall_instance2 = Wall()
            wall_instance2.xy = (96, 101)
            wall_instance2.wh = (16, 38)
            objects_map['fixed wall 2'] = wall_instance2
            wall_instance3 = Wall()
            wall_instance3.xy = (48, 101)
            wall_instance3.wh = (16, 38)
            objects_map['fixed wall 3'] = wall_instance3
            wall_instance4 = Wall()
            wall_instance4.xy = (8, 101)
            wall_instance4.wh = (16, 38)
            objects_map['fixed wall 4'] = wall_instance4
            number_of_walls = 5
            i = 0
            while (objects_map.get(f"fixed wall {number_of_walls + i}") != None):
                objects_map.pop(f"fixed wall {number_of_walls + i}")
                i += 1
        elif ram_state[28] == 15:
            number_of_lava_walls = 0
            i = 0
            while (objects_map.get(f"lava wall {number_of_lava_walls + i}") != None):
                objects_map.pop(f"lava wall {number_of_lava_walls + i}")
                i += 1
            wall_instance0 = Wall()
            wall_instance0.xy = (8, 21)
            wall_instance0.wh = (152, 38)
            objects_map['fixed wall 0'] = wall_instance0
            wall_instance1 = Wall()
            wall_instance1.xy = (112, 101)
            wall_instance1.wh = (48, 38)
            objects_map['fixed wall 1'] = wall_instance1
            wall_instance2 = Wall()
            wall_instance2.xy = (72, 101)
            wall_instance2.wh = (16, 38)
            objects_map['fixed wall 2'] = wall_instance2
            wall_instance3 = Wall()
            wall_instance3.xy = (8, 101)
            wall_instance3.wh = (40, 38)
            objects_map['fixed wall 3'] = wall_instance3
            number_of_walls = 4
            i = 0
            while (objects_map.get(f"fixed wall {number_of_walls + i}") != None):
                objects_map.pop(f"fixed wall {number_of_walls + i}")
                i += 1

    elif ram_state[117] == 14:
        if ram_state[28] == 0:
            wall_instance0 = LavaWall()
            wall_instance0.xy = (144, 61)
            wall_instance0.wh = (16, 37)
            objects_map['lava wall 0'] = wall_instance0
            wall_instance1 = LavaWall()
            wall_instance1.xy = (8, 61)
            wall_instance1.wh = (8, 37)
            objects_map['lava wall 1'] = wall_instance1
            number_of_lava_walls = 2
            i = 0
            while (objects_map.get(f"lava wall {number_of_lava_walls + i}") != None):
                objects_map.pop(f"lava wall {number_of_lava_walls + i}")
                i += 1
            wall_instance0 = Wall()
            wall_instance0.xy = (136, 21)
            wall_instance0.wh = (24, 38)
            objects_map['fixed wall 0'] = wall_instance0
            wall_instance1 = Wall()
            wall_instance1.xy = (8, 21)
            wall_instance1.wh = (16, 38)
            objects_map['fixed wall 1'] = wall_instance1
            wall_instance2 = Wall()
            wall_instance2.xy = (88, 101)
            wall_instance2.wh = (72, 38)
            objects_map['fixed wall 2'] = wall_instance2
            wall_instance3 = Wall()
            wall_instance3.xy = (8, 101)
            wall_instance3.wh = (64, 38)
            objects_map['fixed wall 3'] = wall_instance3
            number_of_walls = 4
            i = 0
            while (objects_map.get(f"fixed wall {number_of_walls + i}") != None):
                objects_map.pop(f"fixed wall {number_of_walls + i}")
                i += 1
        elif ram_state[28] == 1:
            wall_instance0 = LavaWall()
            wall_instance0.xy = (124, 61)
            wall_instance0.wh = (36, 37)
            objects_map['lava wall 0'] = wall_instance0
            wall_instance1 = LavaWall()
            wall_instance1.xy = (8, 61)
            wall_instance1.wh = (28, 37)
            objects_map['lava wall 1'] = wall_instance1
            number_of_lava_walls = 2
            i = 0
            while (objects_map.get(f"lava wall {number_of_lava_walls + i}") != None):
                objects_map.pop(f"lava wall {number_of_lava_walls + i}")
                i += 1
            wall_instance0 = Wall()
            wall_instance0.xy = (88, 21)
            wall_instance0.wh = (72, 38)
            objects_map['fixed wall 0'] = wall_instance0
            wall_instance1 = Wall()
            wall_instance1.xy = (8, 21)
            wall_instance1.wh = (64, 38)
            objects_map['fixed wall 1'] = wall_instance1
            wall_instance2 = Wall()
            wall_instance2.xy = (112, 101)
            wall_instance2.wh = (48, 38)
            objects_map['fixed wall 2'] = wall_instance2
            wall_instance3 = Wall()
            wall_instance3.xy = (56, 101)
            wall_instance3.wh = (48, 38)
            objects_map['fixed wall 3'] = wall_instance3
            wall_instance4 = Wall()
            wall_instance4.xy = (8, 101)
            wall_instance4.wh = (40, 38)
            objects_map['fixed wall 4'] = wall_instance4
            number_of_walls = 5
            i = 0
            while (objects_map.get(f"fixed wall {number_of_walls + i}") != None):
                objects_map.pop(f"fixed wall {number_of_walls + i}")
                i += 1
        elif ram_state[28] == 2:
            wall_instance0 = LavaWall()
            wall_instance0.xy = (144, 61)
            wall_instance0.wh = (16, 37)
            objects_map['lava wall 0'] = wall_instance0
            wall_instance1 = LavaWall()
            wall_instance1.xy = (64, 61)
            wall_instance1.wh = (56, 37)
            objects_map['lava wall 1'] = wall_instance1
            wall_instance2 = LavaWall()
            wall_instance2.xy = (8, 61)
            wall_instance2.wh = (32, 37)
            objects_map['lava wall 2'] = wall_instance2
            number_of_lava_walls = 3
            i = 0
            while (objects_map.get(f"lava wall {number_of_lava_walls + i}") != None):
                objects_map.pop(f"lava wall {number_of_lava_walls + i}")
                i += 1
            wall_instance0 = Wall()
            wall_instance0.xy = (112, 21)
            wall_instance0.wh = (48, 38)
            objects_map['fixed wall 0'] = wall_instance0
            wall_instance1 = Wall()
            wall_instance1.xy = (56, 21)
            wall_instance1.wh = (48, 38)
            objects_map['fixed wall 1'] = wall_instance1
            wall_instance2 = Wall()
            wall_instance2.xy = (8, 21)
            wall_instance2.wh = (40, 38)
            objects_map['fixed wall 2'] = wall_instance2
            wall_instance3 = Wall()
            wall_instance3.xy = (104, 101)
            wall_instance3.wh = (56, 38)
            objects_map['fixed wall 3'] = wall_instance3
            wall_instance4 = Wall()
            wall_instance4.xy = (8, 101)
            wall_instance4.wh = (48, 38)
            objects_map['fixed wall 4'] = wall_instance4
            number_of_walls = 5
            i = 0
            while (objects_map.get(f"fixed wall {number_of_walls + i}") != None):
                objects_map.pop(f"fixed wall {number_of_walls + i}")
                i += 1
        elif ram_state[28] == 3:
            wall_instance0 = LavaWall()
            wall_instance0.xy = (144, 61)
            wall_instance0.wh = (16, 37)
            objects_map['lava wall 0'] = wall_instance0
            wall_instance1 = LavaWall()
            wall_instance1.xy = (8, 61)
            wall_instance1.wh = (8, 37)
            objects_map['lava wall 1'] = wall_instance1
            number_of_lava_walls = 2
            i = 0
            while (objects_map.get(f"lava wall {number_of_lava_walls + i}") != None):
                objects_map.pop(f"lava wall {number_of_lava_walls + i}")
                i += 1
            wall_instance0 = Wall()
            wall_instance0.xy = (104, 21)
            wall_instance0.wh = (56, 38)
            objects_map['fixed wall 0'] = wall_instance0
            wall_instance1 = Wall()
            wall_instance1.xy = (8, 21)
            wall_instance1.wh = (48, 38)
            objects_map['fixed wall 1'] = wall_instance1
            wall_instance2 = Wall()
            wall_instance2.xy = (128, 101)
            wall_instance2.wh = (32, 38)
            objects_map['fixed wall 2'] = wall_instance2
            wall_instance3 = Wall()
            wall_instance3.xy = (40, 101)
            wall_instance3.wh = (80, 38)
            objects_map['fixed wall 3'] = wall_instance3
            wall_instance4 = Wall()
            wall_instance4.xy = (8, 101)
            wall_instance4.wh = (24, 38)
            objects_map['fixed wall 4'] = wall_instance4
            number_of_walls = 5
            i = 0
            while (objects_map.get(f"fixed wall {number_of_walls + i}") != None):
                objects_map.pop(f"fixed wall {number_of_walls + i}")
                i += 1
        elif ram_state[28] == 4:
            wall_instance0 = LavaWall()
            wall_instance0.xy = (144, 61)
            wall_instance0.wh = (16, 37)
            objects_map['lava wall 0'] = wall_instance0
            wall_instance1 = LavaWall()
            wall_instance1.xy = (8, 61)
            wall_instance1.wh = (8, 37)
            objects_map['lava wall 1'] = wall_instance1
            number_of_lava_walls = 2
            i = 0
            while (objects_map.get(f"lava wall {number_of_lava_walls + i}") != None):
                objects_map.pop(f"lava wall {number_of_lava_walls + i}")
                i += 1
            wall_instance0 = Wall()
            wall_instance0.xy = (128, 21)
            wall_instance0.wh = (32, 38)
            objects_map['fixed wall 0'] = wall_instance0
            wall_instance1 = Wall()
            wall_instance1.xy = (40, 21)
            wall_instance1.wh = (80, 38)
            objects_map['fixed wall 1'] = wall_instance1
            wall_instance2 = Wall()
            wall_instance2.xy = (8, 21)
            wall_instance2.wh = (24, 38)
            objects_map['fixed wall 2'] = wall_instance2
            wall_instance3 = Wall()
            wall_instance3.xy = (96, 101)
            wall_instance3.wh = (64, 38)
            objects_map['fixed wall 3'] = wall_instance3
            wall_instance4 = Wall()
            wall_instance4.xy = (8, 101)
            wall_instance4.wh = (56, 38)
            objects_map['fixed wall 4'] = wall_instance4
            number_of_walls = 5
            i = 0
            while (objects_map.get(f"fixed wall {number_of_walls + i}") != None):
                objects_map.pop(f"fixed wall {number_of_walls + i}")
                i += 1
        elif ram_state[28] == 5:
            wall_instance0 = LavaWall()
            wall_instance0.xy = (144, 61)
            wall_instance0.wh = (16, 37)
            objects_map['lava wall 0'] = wall_instance0
            wall_instance1 = LavaWall()
            wall_instance1.xy = (8, 61)
            wall_instance1.wh = (8, 37)
            objects_map['lava wall 1'] = wall_instance1
            number_of_lava_walls = 2
            i = 0
            while (objects_map.get(f"lava wall {number_of_lava_walls + i}") != None):
                objects_map.pop(f"lava wall {number_of_lava_walls + i}")
                i += 1
            wall_instance0 = Wall()
            wall_instance0.xy = (96, 21)
            wall_instance0.wh = (64, 38)
            objects_map['fixed wall 0'] = wall_instance0
            wall_instance1 = Wall()
            wall_instance1.xy = (8, 21)
            wall_instance1.wh = (56, 38)
            objects_map['fixed wall 1'] = wall_instance1
            wall_instance2 = Wall()
            wall_instance2.xy = (136, 101)
            wall_instance2.wh = (24, 38)
            objects_map['fixed wall 2'] = wall_instance2
            wall_instance3 = Wall()
            wall_instance3.xy = (84, 101)
            wall_instance3.wh = (44, 38)
            objects_map['fixed wall 3'] = wall_instance3
            wall_instance4 = Wall()
            wall_instance4.xy = (32, 101)
            wall_instance4.wh = (44, 38)
            objects_map['fixed wall 4'] = wall_instance4
            wall_instance5 = Wall()
            wall_instance5.xy = (8, 101)
            wall_instance5.wh = (16, 38)
            objects_map['fixed wall 5'] = wall_instance5
            number_of_walls = 6
            i = 0
            while (objects_map.get(f"fixed wall {number_of_walls + i}") != None):
                objects_map.pop(f"fixed wall {number_of_walls + i}")
                i += 1
        elif ram_state[28] == 6:
            wall_instance0 = LavaWall()
            wall_instance0.xy = (144, 61)
            wall_instance0.wh = (16, 37)
            objects_map['lava wall 0'] = wall_instance0
            wall_instance1 = LavaWall()
            wall_instance1.xy = (64, 61)
            wall_instance1.wh = (32, 37)
            objects_map['lava wall 1'] = wall_instance1
            wall_instance2 = LavaWall()
            wall_instance2.xy = (8, 61)
            wall_instance2.wh = (8, 37)
            objects_map['lava wall 2'] = wall_instance2
            number_of_lava_walls = 3
            i = 0
            while (objects_map.get(f"lava wall {number_of_lava_walls + i}") != None):
                objects_map.pop(f"lava wall {number_of_lava_walls + i}")
                i += 1
            wall_instance0 = Wall()
            wall_instance0.xy = (136, 21)
            wall_instance0.wh = (24, 38)
            objects_map['fixed wall 0'] = wall_instance0
            wall_instance1 = Wall()
            wall_instance1.xy = (84, 21)
            wall_instance1.wh = (44, 38)
            objects_map['fixed wall 1'] = wall_instance1
            wall_instance2 = Wall()
            wall_instance2.xy = (32, 21)
            wall_instance2.wh = (44, 38)
            objects_map['fixed wall 2'] = wall_instance2
            wall_instance3 = Wall()
            wall_instance3.xy = (8, 21)
            wall_instance3.wh = (16, 38)
            objects_map['fixed wall 3'] = wall_instance3
            wall_instance4 = Wall()
            wall_instance4.xy = (136, 101)
            wall_instance4.wh = (24, 38)
            objects_map['fixed wall 4'] = wall_instance4
            wall_instance5 = Wall()
            wall_instance5.xy = (48, 101)
            wall_instance5.wh = (64, 38)
            objects_map['fixed wall 5'] = wall_instance5
            wall_instance6 = Wall()
            wall_instance6.xy = (8, 101)
            wall_instance6.wh = (16, 38)
            objects_map['fixed wall 6'] = wall_instance6
            number_of_walls = 7
            i = 0
            while (objects_map.get(f"fixed wall {number_of_walls + i}") != None):
                objects_map.pop(f"fixed wall {number_of_walls + i}")
                i += 1
        elif ram_state[28] == 7:
            wall_instance0 = LavaWall()
            wall_instance0.xy = (144, 61)
            wall_instance0.wh = (16, 37)
            objects_map['lava wall 0'] = wall_instance0
            wall_instance1 = LavaWall()
            wall_instance1.xy = (8, 61)
            wall_instance1.wh = (8, 37)
            objects_map['lava wall 1'] = wall_instance1
            number_of_lava_walls = 2
            i = 0
            while (objects_map.get(f"lava wall {number_of_lava_walls + i}") != None):
                objects_map.pop(f"lava wall {number_of_lava_walls + i}")
                i += 1
            wall_instance0 = Wall()
            wall_instance0.xy = (136, 21)
            wall_instance0.wh = (24, 38)
            objects_map['fixed wall 0'] = wall_instance0
            wall_instance1 = Wall()
            wall_instance1.xy = (48, 21)
            wall_instance1.wh = (64, 38)
            objects_map['fixed wall 1'] = wall_instance1
            wall_instance2 = Wall()
            wall_instance2.xy = (8, 21)
            wall_instance2.wh = (16, 38)
            objects_map['fixed wall 2'] = wall_instance2
            wall_instance3 = Wall()
            wall_instance3.xy = (136, 101)
            wall_instance3.wh = (24, 38)
            objects_map['fixed wall 3'] = wall_instance3
            wall_instance4 = Wall()
            wall_instance4.xy = (32, 101)
            wall_instance4.wh = (96, 38)
            objects_map['fixed wall 4'] = wall_instance4
            wall_instance5 = Wall()
            wall_instance5.xy = (8, 101)
            wall_instance5.wh = (16, 38)
            objects_map['fixed wall 5'] = wall_instance5
            number_of_walls = 6
            i = 0
            while (objects_map.get(f"fixed wall {number_of_walls + i}") != None):
                objects_map.pop(f"fixed wall {number_of_walls + i}")
                i += 1
        elif ram_state[28] == 8:
            wall_instance0 = LavaWall()
            wall_instance0.xy = (144, 61)
            wall_instance0.wh = (16, 37)
            objects_map['lava wall 0'] = wall_instance0
            wall_instance1 = LavaWall()
            wall_instance1.xy = (8, 61)
            wall_instance1.wh = (8, 37)
            objects_map['lava wall 1'] = wall_instance1
            number_of_lava_walls = 2
            i = 0
            while (objects_map.get(f"lava wall {number_of_lava_walls + i}") != None):
                objects_map.pop(f"lava wall {number_of_lava_walls + i}")
                i += 1
            wall_instance0 = Wall()
            wall_instance0.xy = (136, 21)
            wall_instance0.wh = (24, 38)
            objects_map['fixed wall 0'] = wall_instance0
            wall_instance1 = Wall()
            wall_instance1.xy = (32, 21)
            wall_instance1.wh = (96, 38)
            objects_map['fixed wall 1'] = wall_instance1
            wall_instance2 = Wall()
            wall_instance2.xy = (8, 21)
            wall_instance2.wh = (16, 38)
            objects_map['fixed wall 2'] = wall_instance2
            wall_instance3 = Wall()
            wall_instance3.xy = (136, 101)
            wall_instance3.wh = (24, 38)
            objects_map['fixed wall 3'] = wall_instance3
            wall_instance4 = Wall()
            wall_instance4.xy = (84, 101)
            wall_instance4.wh = (44, 38)
            objects_map['fixed wall 4'] = wall_instance4
            wall_instance5 = Wall()
            wall_instance5.xy = (32, 101)
            wall_instance5.wh = (44, 38)
            objects_map['fixed wall 5'] = wall_instance5
            wall_instance6 = Wall()
            wall_instance6.xy = (8, 101)
            wall_instance6.wh = (16, 38)
            objects_map['fixed wall 6'] = wall_instance6
            number_of_walls = 7
            i = 0
            while (objects_map.get(f"fixed wall {number_of_walls + i}") != None):
                objects_map.pop(f"fixed wall {number_of_walls + i}")
                i += 1
        elif ram_state[28] == 9:
            wall_instance0 = LavaWall()
            wall_instance0.xy = (84, 61)
            wall_instance0.wh = (76, 37)
            objects_map['lava wall 0'] = wall_instance0
            wall_instance1 = LavaWall()
            wall_instance1.xy = (8, 61)
            wall_instance1.wh = (68, 37)
            objects_map['lava wall 1'] = wall_instance1
            number_of_lava_walls = 2
            i = 0
            while (objects_map.get(f"lava wall {number_of_lava_walls + i}") != None):
                objects_map.pop(f"lava wall {number_of_lava_walls + i}")
                i += 1
            wall_instance0 = Wall()
            wall_instance0.xy = (136, 21)
            wall_instance0.wh = (24, 38)
            objects_map['fixed wall 0'] = wall_instance0
            wall_instance1 = Wall()
            wall_instance1.xy = (84, 21)
            wall_instance1.wh = (44, 38)
            objects_map['fixed wall 1'] = wall_instance1
            wall_instance2 = Wall()
            wall_instance2.xy = (32, 21)
            wall_instance2.wh = (44, 38)
            objects_map['fixed wall 2'] = wall_instance2
            wall_instance3 = Wall()
            wall_instance3.xy = (8, 21)
            wall_instance3.wh = (16, 38)
            objects_map['fixed wall 3'] = wall_instance3
            wall_instance4 = Wall()
            wall_instance4.xy = (88, 101)
            wall_instance4.wh = (72, 38)
            objects_map['fixed wall 4'] = wall_instance4
            wall_instance5 = Wall()
            wall_instance5.xy = (8, 101)
            wall_instance5.wh = (64, 38)
            objects_map['fixed wall 5'] = wall_instance5
            number_of_walls = 6
            i = 0
            while (objects_map.get(f"fixed wall {number_of_walls + i}") != None):
                objects_map.pop(f"fixed wall {number_of_walls + i}")
                i += 1
        elif ram_state[28] == 10:
            number_of_lava_walls = 0
            i = 0
            while (objects_map.get(f"lava wall {number_of_lava_walls + i}") != None):
                objects_map.pop(f"lava wall {number_of_lava_walls + i}")
                i += 1
            wall_instance0 = Wall()
            wall_instance0.xy = (88, 21)
            wall_instance0.wh = (72, 38)
            objects_map['fixed wall 0'] = wall_instance0
            wall_instance1 = Wall()
            wall_instance1.xy = (8, 21)
            wall_instance1.wh = (64, 38)
            objects_map['fixed wall 1'] = wall_instance1
            wall_instance2 = Wall()
            wall_instance2.xy = (128, 61)
            wall_instance2.wh = (32, 37)
            objects_map['fixed wall 2'] = wall_instance2
            wall_instance3 = Wall()
            wall_instance3.xy = (48, 61)
            wall_instance3.wh = (32, 37)
            objects_map['fixed wall 3'] = wall_instance3
            wall_instance4 = Wall()
            wall_instance4.xy = (120, 101)
            wall_instance4.wh = (40, 38)
            objects_map['fixed wall 4'] = wall_instance4
            wall_instance5 = Wall()
            wall_instance5.xy = (8, 101)
            wall_instance5.wh = (32, 38)
            objects_map['fixed wall 5'] = wall_instance5
            number_of_walls = 6
            i = 0
            while (objects_map.get(f"fixed wall {number_of_walls + i}") != None):
                objects_map.pop(f"fixed wall {number_of_walls + i}")
                i += 1
        elif ram_state[28] == 11:
            number_of_lava_walls = 0
            i = 0
            while (objects_map.get(f"lava wall {number_of_lava_walls + i}") != None):
                objects_map.pop(f"lava wall {number_of_lava_walls + i}")
                i += 1
            wall_instance0 = Wall()
            wall_instance0.xy = (8, 21)
            wall_instance0.wh = (152, 38)
            objects_map['fixed wall 0'] = wall_instance0
            wall_instance1 = Wall()
            wall_instance1.xy = (144, 101)
            wall_instance1.wh = (16, 38)
            objects_map['fixed wall 1'] = wall_instance1
            wall_instance2 = Wall()
            wall_instance2.xy = (72, 101)
            wall_instance2.wh = (16, 38)
            objects_map['fixed wall 2'] = wall_instance2
            wall_instance3 = Wall()
            wall_instance3.xy = (8, 101)
            wall_instance3.wh = (8, 38)
            objects_map['fixed wall 3'] = wall_instance3
            number_of_walls = 4
            i = 0
            while (objects_map.get(f"fixed wall {number_of_walls + i}") != None):
                objects_map.pop(f"fixed wall {number_of_walls + i}")
                i += 1
        elif ram_state[28] == 12:
            number_of_lava_walls = 0
            i = 0
            while (objects_map.get(f"lava wall {number_of_lava_walls + i}") != None):
                objects_map.pop(f"lava wall {number_of_lava_walls + i}")
                i += 1
            wall_instance0 = Wall()
            wall_instance0.xy = (8, 21)
            wall_instance0.wh = (152, 38)
            objects_map['fixed wall 0'] = wall_instance0
            wall_instance1 = Wall()
            wall_instance1.xy = (120, 61)
            wall_instance1.wh = (16, 37)
            objects_map['fixed wall 1'] = wall_instance1
            wall_instance2 = Wall()
            wall_instance2.xy = (40, 61)
            wall_instance2.wh = (16, 37)
            objects_map['fixed wall 2'] = wall_instance2
            wall_instance3 = Wall()
            wall_instance3.xy = (144, 101)
            wall_instance3.wh = (16, 38)
            objects_map['fixed wall 3'] = wall_instance3
            wall_instance4 = Wall()
            wall_instance4.xy = (64, 101)
            wall_instance4.wh = (32, 38)
            objects_map['fixed wall 4'] = wall_instance4
            wall_instance5 = Wall()
            wall_instance5.xy = (8, 101)
            wall_instance5.wh = (8, 38)
            objects_map['fixed wall 5'] = wall_instance5
            number_of_walls = 6
            i = 0
            while (objects_map.get(f"fixed wall {number_of_walls + i}") != None):
                objects_map.pop(f"fixed wall {number_of_walls + i}")
                i += 1
        elif ram_state[28] == 13:
            wall_instance0 = LavaWall()
            wall_instance0.xy = (48, 61)
            wall_instance0.wh = (64, 37)
            objects_map['lava wall 0'] = wall_instance0
            number_of_lava_walls = 1
            i = 0
            while (objects_map.get(f"lava wall {number_of_lava_walls + i}") != None):
                objects_map.pop(f"lava wall {number_of_lava_walls + i}")
                i += 1
            wall_instance0 = Wall()
            wall_instance0.xy = (8, 21)
            wall_instance0.wh = (152, 38)
            objects_map['fixed wall 0'] = wall_instance0
            wall_instance1 = Wall()
            wall_instance1.xy = (136, 101)
            wall_instance1.wh = (24, 38)
            objects_map['fixed wall 1'] = wall_instance1
            wall_instance2 = Wall()
            wall_instance2.xy = (8, 101)
            wall_instance2.wh = (16, 38)
            objects_map['fixed wall 2'] = wall_instance2
            number_of_walls = 3
            i = 0
            while (objects_map.get(f"fixed wall {number_of_walls + i}") != None):
                objects_map.pop(f"fixed wall {number_of_walls + i}")
                i += 1
        elif ram_state[28] == 14:
            number_of_lava_walls = 0
            i = 0
            while (objects_map.get(f"lava wall {number_of_lava_walls + i}") != None):
                objects_map.pop(f"lava wall {number_of_lava_walls + i}")
                i += 1
            wall_instance0 = Wall()
            wall_instance0.xy = (8, 21)
            wall_instance0.wh = (152, 38)
            objects_map['fixed wall 0'] = wall_instance0
            wall_instance1 = Wall()
            wall_instance1.xy = (8, 101)
            wall_instance1.wh = (152, 38)
            objects_map['fixed wall 1'] = wall_instance1
            number_of_walls = 2
            i = 0
            while (objects_map.get(f"fixed wall {number_of_walls + i}") != None):
                objects_map.pop(f"fixed wall {number_of_walls + i}")
                i += 1
        elif ram_state[28] == 15:
            number_of_lava_walls = 0
            i = 0
            while (objects_map.get(f"lava wall {number_of_lava_walls + i}") != None):
                objects_map.pop(f"lava wall {number_of_lava_walls + i}")
                i += 1
            wall_instance0 = Wall()
            wall_instance0.xy = (8, 21)
            wall_instance0.wh = (152, 38)
            objects_map['fixed wall 0'] = wall_instance0
            wall_instance1 = Wall()
            wall_instance1.xy = (112, 101)
            wall_instance1.wh = (48, 38)
            objects_map['fixed wall 1'] = wall_instance1
            wall_instance2 = Wall()
            wall_instance2.xy = (60, 101)
            wall_instance2.wh = (40, 38)
            objects_map['fixed wall 2'] = wall_instance2
            wall_instance3 = Wall()
            wall_instance3.xy = (8, 101)
            wall_instance3.wh = (40, 38)
            objects_map['fixed wall 3'] = wall_instance3
            number_of_walls = 4
            i = 0
            while (objects_map.get(f"fixed wall {number_of_walls + i}") != None):
                objects_map.pop(f"fixed wall {number_of_walls + i}")
                i += 1

    elif ram_state[117] == 15:
        if ram_state[28] == 0:
            wall_instance0 = LavaWall()
            wall_instance0.xy = (144, 61)
            wall_instance0.wh = (16, 37)
            objects_map['lava wall 0'] = wall_instance0
            wall_instance1 = LavaWall()
            wall_instance1.xy = (8, 61)
            wall_instance1.wh = (8, 37)
            objects_map['lava wall 1'] = wall_instance1
            number_of_lava_walls = 2
            i = 0
            while (objects_map.get(f"lava wall {number_of_lava_walls + i}") != None):
                objects_map.pop(f"lava wall {number_of_lava_walls + i}")
                i += 1
            wall_instance0 = Wall()
            wall_instance0.xy = (136, 21)
            wall_instance0.wh = (24, 38)
            objects_map['fixed wall 0'] = wall_instance0
            wall_instance1 = Wall()
            wall_instance1.xy = (8, 21)
            wall_instance1.wh = (16, 38)
            objects_map['fixed wall 1'] = wall_instance1
            wall_instance2 = Wall()
            wall_instance2.xy = (136, 101)
            wall_instance2.wh = (24, 38)
            objects_map['fixed wall 2'] = wall_instance2
            wall_instance3 = Wall()
            wall_instance3.xy = (88, 101)
            wall_instance3.wh = (40, 38)
            objects_map['fixed wall 3'] = wall_instance3
            wall_instance4 = Wall()
            wall_instance4.xy = (32, 101)
            wall_instance4.wh = (40, 38)
            objects_map['fixed wall 4'] = wall_instance4
            wall_instance5 = Wall()
            wall_instance5.xy = (8, 101)
            wall_instance5.wh = (16, 38)
            objects_map['fixed wall 5'] = wall_instance5
            number_of_walls = 6
            i = 0
            while (objects_map.get(f"fixed wall {number_of_walls + i}") != None):
                objects_map.pop(f"fixed wall {number_of_walls + i}")
                i += 1
        elif ram_state[28] == 1:
            wall_instance0 = LavaWall()
            wall_instance0.xy = (144, 61)
            wall_instance0.wh = (16, 37)
            objects_map['lava wall 0'] = wall_instance0
            wall_instance1 = LavaWall()
            wall_instance1.xy = (64, 61)
            wall_instance1.wh = (32, 37)
            objects_map['lava wall 1'] = wall_instance1
            wall_instance2 = LavaWall()
            wall_instance2.xy = (8, 61)
            wall_instance2.wh = (8, 37)
            objects_map['lava wall 2'] = wall_instance2
            number_of_lava_walls = 3
            i = 0
            while (objects_map.get(f"lava wall {number_of_lava_walls + i}") != None):
                objects_map.pop(f"lava wall {number_of_lava_walls + i}")
                i += 1
            wall_instance0 = Wall()
            wall_instance0.xy = (136, 21)
            wall_instance0.wh = (24, 38)
            objects_map['fixed wall 0'] = wall_instance0
            wall_instance1 = Wall()
            wall_instance1.xy = (88, 21)
            wall_instance1.wh = (40, 38)
            objects_map['fixed wall 1'] = wall_instance1
            wall_instance2 = Wall()
            wall_instance2.xy = (32, 21)
            wall_instance2.wh = (40, 38)
            objects_map['fixed wall 2'] = wall_instance2
            wall_instance3 = Wall()
            wall_instance3.xy = (8, 21)
            wall_instance3.wh = (16, 38)
            objects_map['fixed wall 3'] = wall_instance3
            wall_instance4 = Wall()
            wall_instance4.xy = (8, 101)
            wall_instance4.wh = (152, 38)
            objects_map['fixed wall 4'] = wall_instance4
            number_of_walls = 5
            i = 0
            while (objects_map.get(f"fixed wall {number_of_walls + i}") != None):
                objects_map.pop(f"fixed wall {number_of_walls + i}")
                i += 1
        elif ram_state[28] == 2:
            wall_instance0 = LavaWall()
            wall_instance0.xy = (144, 61)
            wall_instance0.wh = (16, 37)
            objects_map['lava wall 0'] = wall_instance0
            wall_instance1 = LavaWall()
            wall_instance1.xy = (68, 61)
            wall_instance1.wh = (24, 37)
            objects_map['lava wall 1'] = wall_instance1
            wall_instance2 = LavaWall()
            wall_instance2.xy = (8, 61)
            wall_instance2.wh = (8, 37)
            objects_map['lava wall 2'] = wall_instance2
            number_of_lava_walls = 3
            i = 0
            while (objects_map.get(f"lava wall {number_of_lava_walls + i}") != None):
                objects_map.pop(f"lava wall {number_of_lava_walls + i}")
                i += 1
            wall_instance0 = Wall()
            wall_instance0.xy = (8, 21)
            wall_instance0.wh = (152, 38)
            objects_map['fixed wall 0'] = wall_instance0
            wall_instance1 = Wall()
            wall_instance1.xy = (128, 101)
            wall_instance1.wh = (32, 38)
            objects_map['fixed wall 1'] = wall_instance1
            wall_instance2 = Wall()
            wall_instance2.xy = (8, 101)
            wall_instance2.wh = (24, 38)
            objects_map['fixed wall 2'] = wall_instance2
            number_of_walls = 3
            i = 0
            while (objects_map.get(f"fixed wall {number_of_walls + i}") != None):
                objects_map.pop(f"fixed wall {number_of_walls + i}")
                i += 1
        elif ram_state[28] == 3:
            wall_instance0 = LavaWall()
            wall_instance0.xy = (104, 61)
            wall_instance0.wh = (56, 37)
            objects_map['lava wall 0'] = wall_instance0
            wall_instance1 = LavaWall()
            wall_instance1.xy = (8, 61)
            wall_instance1.wh = (48, 37)
            objects_map['lava wall 1'] = wall_instance1
            number_of_lava_walls = 2
            i = 0
            while (objects_map.get(f"lava wall {number_of_lava_walls + i}") != None):
                objects_map.pop(f"lava wall {number_of_lava_walls + i}")
                i += 1
            wall_instance0 = Wall()
            wall_instance0.xy = (128, 21)
            wall_instance0.wh = (32, 38)
            objects_map['fixed wall 0'] = wall_instance0
            wall_instance1 = Wall()
            wall_instance1.xy = (8, 21)
            wall_instance1.wh = (24, 38)
            objects_map['fixed wall 1'] = wall_instance1
            wall_instance2 = Wall()
            wall_instance2.xy = (112, 101)
            wall_instance2.wh = (48, 38)
            objects_map['fixed wall 2'] = wall_instance2
            wall_instance3 = Wall()
            wall_instance3.xy = (8, 101)
            wall_instance3.wh = (40, 38)
            objects_map['fixed wall 3'] = wall_instance3
            number_of_walls = 4
            i = 0
            while (objects_map.get(f"fixed wall {number_of_walls + i}") != None):
                objects_map.pop(f"fixed wall {number_of_walls + i}")
                i += 1
        elif ram_state[28] == 4:
            wall_instance0 = LavaWall()
            wall_instance0.xy = (144, 61)
            wall_instance0.wh = (16, 37)
            objects_map['lava wall 0'] = wall_instance0
            wall_instance1 = LavaWall()
            wall_instance1.xy = (72, 61)
            wall_instance1.wh = (16, 37)
            objects_map['lava wall 1'] = wall_instance1
            wall_instance2 = LavaWall()
            wall_instance2.xy = (8, 61)
            wall_instance2.wh = (8, 37)
            objects_map['lava wall 2'] = wall_instance2
            number_of_lava_walls = 3
            i = 0
            while (objects_map.get(f"lava wall {number_of_lava_walls + i}") != None):
                objects_map.pop(f"lava wall {number_of_lava_walls + i}")
                i += 1
            wall_instance0 = Wall()
            wall_instance0.xy = (112, 21)
            wall_instance0.wh = (48, 38)
            objects_map['fixed wall 0'] = wall_instance0
            wall_instance1 = Wall()
            wall_instance1.xy = (8, 21)
            wall_instance1.wh = (40, 38)
            objects_map['fixed wall 1'] = wall_instance1
            wall_instance2 = Wall()
            wall_instance2.xy = (140, 101)
            wall_instance2.wh = (20, 38)
            objects_map['fixed wall 2'] = wall_instance2
            wall_instance3 = Wall()
            wall_instance3.xy = (28, 101)
            wall_instance3.wh = (104, 38)
            objects_map['fixed wall 3'] = wall_instance3
            wall_instance4 = Wall()
            wall_instance4.xy = (8, 101)
            wall_instance4.wh = (12, 38)
            objects_map['fixed wall 4'] = wall_instance4
            number_of_walls = 5
            i = 0
            while (objects_map.get(f"fixed wall {number_of_walls + i}") != None):
                objects_map.pop(f"fixed wall {number_of_walls + i}")
                i += 1
        elif ram_state[28] == 5:
            wall_instance0 = LavaWall()
            wall_instance0.xy = (144, 61)
            wall_instance0.wh = (16, 37)
            objects_map['lava wall 0'] = wall_instance0
            wall_instance1 = LavaWall()
            wall_instance1.xy = (68, 61)
            wall_instance1.wh = (24, 37)
            objects_map['lava wall 1'] = wall_instance1
            wall_instance2 = LavaWall()
            wall_instance2.xy = (8, 61)
            wall_instance2.wh = (8, 37)
            objects_map['lava wall 2'] = wall_instance2
            number_of_lava_walls = 3
            i = 0
            while (objects_map.get(f"lava wall {number_of_lava_walls + i}") != None):
                objects_map.pop(f"lava wall {number_of_lava_walls + i}")
                i += 1
            wall_instance0 = Wall()
            wall_instance0.xy = (140, 21)
            wall_instance0.wh = (20, 38)
            objects_map['fixed wall 0'] = wall_instance0
            wall_instance1 = Wall()
            wall_instance1.xy = (28, 21)
            wall_instance1.wh = (104, 38)
            objects_map['fixed wall 1'] = wall_instance1
            wall_instance2 = Wall()
            wall_instance2.xy = (8, 21)
            wall_instance2.wh = (12, 38)
            objects_map['fixed wall 2'] = wall_instance2
            wall_instance3 = Wall()
            wall_instance3.xy = (108, 101)
            wall_instance3.wh = (52, 38)
            objects_map['fixed wall 3'] = wall_instance3
            wall_instance4 = Wall()
            wall_instance4.xy = (8, 101)
            wall_instance4.wh = (44, 38)
            objects_map['fixed wall 4'] = wall_instance4
            number_of_walls = 5
            i = 0
            while (objects_map.get(f"fixed wall {number_of_walls + i}") != None):
                objects_map.pop(f"fixed wall {number_of_walls + i}")
                i += 1
        elif ram_state[28] == 6:
            wall_instance0 = LavaWall()
            wall_instance0.xy = (104, 61)
            wall_instance0.wh = (56, 37)
            objects_map['lava wall 0'] = wall_instance0
            wall_instance1 = LavaWall()
            wall_instance1.xy = (64, 61)
            wall_instance1.wh = (32, 37)
            objects_map['lava wall 1'] = wall_instance1
            wall_instance2 = LavaWall()
            wall_instance2.xy = (8, 61)
            wall_instance2.wh = (48, 37)
            objects_map['lava wall 2'] = wall_instance2
            number_of_lava_walls = 3
            i = 0
            while (objects_map.get(f"lava wall {number_of_lava_walls + i}") != None):
                objects_map.pop(f"lava wall {number_of_lava_walls + i}")
                i += 1
            wall_instance0 = Wall()
            wall_instance0.xy = (108, 21)
            wall_instance0.wh = (52, 38)
            objects_map['fixed wall 0'] = wall_instance0
            wall_instance1 = Wall()
            wall_instance1.xy = (8, 21)
            wall_instance1.wh = (44, 38)
            objects_map['fixed wall 1'] = wall_instance1
            wall_instance2 = Wall()
            wall_instance2.xy = (144, 101)
            wall_instance2.wh = (16, 38)
            objects_map['fixed wall 2'] = wall_instance2
            wall_instance3 = Wall()
            wall_instance3.xy = (8, 101)
            wall_instance3.wh = (8, 38)
            objects_map['fixed wall 3'] = wall_instance3
            number_of_walls = 4
            i = 0
            while (objects_map.get(f"fixed wall {number_of_walls + i}") != None):
                objects_map.pop(f"fixed wall {number_of_walls + i}")
                i += 1
        elif ram_state[28] == 7:
            wall_instance0 = LavaWall()
            wall_instance0.xy = (84, 61)
            wall_instance0.wh = (76, 37)
            objects_map['lava wall 0'] = wall_instance0
            wall_instance1 = LavaWall()
            wall_instance1.xy = (8, 61)
            wall_instance1.wh = (68, 37)
            objects_map['lava wall 1'] = wall_instance1
            number_of_lava_walls = 2
            i = 0
            while (objects_map.get(f"lava wall {number_of_lava_walls + i}") != None):
                objects_map.pop(f"lava wall {number_of_lava_walls + i}")
                i += 1
            wall_instance0 = Wall()
            wall_instance0.xy = (144, 21)
            wall_instance0.wh = (16, 38)
            objects_map['fixed wall 0'] = wall_instance0
            wall_instance1 = Wall()
            wall_instance1.xy = (8, 21)
            wall_instance1.wh = (8, 38)
            objects_map['fixed wall 1'] = wall_instance1
            wall_instance2 = Wall()
            wall_instance2.xy = (144, 101)
            wall_instance2.wh = (16, 38)
            objects_map['fixed wall 2'] = wall_instance2
            wall_instance3 = Wall()
            wall_instance3.xy = (8, 101)
            wall_instance3.wh = (8, 38)
            objects_map['fixed wall 3'] = wall_instance3
            number_of_walls = 4
            i = 0
            while (objects_map.get(f"fixed wall {number_of_walls + i}") != None):
                objects_map.pop(f"fixed wall {number_of_walls + i}")
                i += 1
        elif ram_state[28] == 8:
            wall_instance0 = LavaWall()
            wall_instance0.xy = (112, 61)
            wall_instance0.wh = (48, 37)
            objects_map['lava wall 0'] = wall_instance0
            wall_instance1 = LavaWall()
            wall_instance1.xy = (84, 61)
            wall_instance1.wh = (20, 37)
            objects_map['lava wall 1'] = wall_instance1
            wall_instance2 = LavaWall()
            wall_instance2.xy = (56, 61)
            wall_instance2.wh = (20, 37)
            objects_map['lava wall 2'] = wall_instance2
            wall_instance3 = LavaWall()
            wall_instance3.xy = (8, 61)
            wall_instance3.wh = (40, 37)
            objects_map['lava wall 3'] = wall_instance3
            number_of_lava_walls = 4
            i = 0
            while (objects_map.get(f"lava wall {number_of_lava_walls + i}") != None):
                objects_map.pop(f"lava wall {number_of_lava_walls + i}")
                i += 1
            wall_instance0 = Wall()
            wall_instance0.xy = (144, 21)
            wall_instance0.wh = (16, 38)
            objects_map['fixed wall 0'] = wall_instance0
            wall_instance1 = Wall()
            wall_instance1.xy = (8, 21)
            wall_instance1.wh = (8, 38)
            objects_map['fixed wall 1'] = wall_instance1
            wall_instance2 = Wall()
            wall_instance2.xy = (144, 101)
            wall_instance2.wh = (16, 38)
            objects_map['fixed wall 2'] = wall_instance2
            wall_instance3 = Wall()
            wall_instance3.xy = (8, 101)
            wall_instance3.wh = (8, 38)
            objects_map['fixed wall 3'] = wall_instance3
            number_of_walls = 4
            i = 0
            while (objects_map.get(f"fixed wall {number_of_walls + i}") != None):
                objects_map.pop(f"fixed wall {number_of_walls + i}")
                i += 1
        elif ram_state[28] == 9:
            wall_instance0 = LavaWall()
            wall_instance0.xy = (92, 61)
            wall_instance0.wh = (68, 37)
            objects_map['lava wall 0'] = wall_instance0
            wall_instance1 = LavaWall()
            wall_instance1.xy = (8, 61)
            wall_instance1.wh = (60, 37)
            objects_map['lava wall 1'] = wall_instance1
            number_of_lava_walls = 2
            i = 0
            while (objects_map.get(f"lava wall {number_of_lava_walls + i}") != None):
                objects_map.pop(f"lava wall {number_of_lava_walls + i}")
                i += 1
            wall_instance0 = Wall()
            wall_instance0.xy = (144, 21)
            wall_instance0.wh = (16, 38)
            objects_map['fixed wall 0'] = wall_instance0
            wall_instance1 = Wall()
            wall_instance1.xy = (8, 21)
            wall_instance1.wh = (8, 38)
            objects_map['fixed wall 1'] = wall_instance1
            wall_instance2 = Wall()
            wall_instance2.xy = (128, 101)
            wall_instance2.wh = (32, 38)
            objects_map['fixed wall 2'] = wall_instance2
            wall_instance3 = Wall()
            wall_instance3.xy = (8, 101)
            wall_instance3.wh = (24, 38)
            objects_map['fixed wall 3'] = wall_instance3
            number_of_walls = 4
            i = 0
            while (objects_map.get(f"fixed wall {number_of_walls + i}") != None):
                objects_map.pop(f"fixed wall {number_of_walls + i}")
                i += 1
        elif ram_state[28] == 10:
            wall_instance0 = LavaWall()
            wall_instance0.xy = (72, 61)
            wall_instance0.wh = (16, 37)
            objects_map['lava wall 0'] = wall_instance0
            number_of_lava_walls = 1
            i = 0
            while (objects_map.get(f"lava wall {number_of_lava_walls + i}") != None):
                objects_map.pop(f"lava wall {number_of_lava_walls + i}")
                i += 1
            wall_instance0 = Wall()
            wall_instance0.xy = (128, 21)
            wall_instance0.wh = (32, 38)
            objects_map['fixed wall 0'] = wall_instance0
            wall_instance1 = Wall()
            wall_instance1.xy = (8, 21)
            wall_instance1.wh = (24, 38)
            objects_map['fixed wall 1'] = wall_instance1
            wall_instance2 = Wall()
            wall_instance2.xy = (136, 101)
            wall_instance2.wh = (24, 38)
            objects_map['fixed wall 2'] = wall_instance2
            wall_instance3 = Wall()
            wall_instance3.xy = (8, 101)
            wall_instance3.wh = (16, 38)
            objects_map['fixed wall 3'] = wall_instance3
            number_of_walls = 4
            i = 0
            while (objects_map.get(f"fixed wall {number_of_walls + i}") != None):
                objects_map.pop(f"fixed wall {number_of_walls + i}")
                i += 1
        elif ram_state[28] == 11:
            wall_instance0 = LavaWall()
            wall_instance0.xy = (48, 61)
            wall_instance0.wh = (64, 37)
            objects_map['lava wall 0'] = wall_instance0
            number_of_lava_walls = 1
            i = 0
            while (objects_map.get(f"lava wall {number_of_lava_walls + i}") != None):
                objects_map.pop(f"lava wall {number_of_lava_walls + i}")
                i += 1
            wall_instance0 = Wall()
            wall_instance0.xy = (8, 21)
            wall_instance0.wh = (152, 38)
            objects_map['fixed wall 0'] = wall_instance0
            wall_instance1 = Wall()
            wall_instance1.xy = (136, 101)
            wall_instance1.wh = (24, 38)
            objects_map['fixed wall 1'] = wall_instance1
            wall_instance2 = Wall()
            wall_instance2.xy = (8, 101)
            wall_instance2.wh = (16, 38)
            objects_map['fixed wall 2'] = wall_instance2
            number_of_walls = 3
            i = 0
            while (objects_map.get(f"fixed wall {number_of_walls + i}") != None):
                objects_map.pop(f"fixed wall {number_of_walls + i}")
                i += 1
        elif ram_state[28] == 12:
            number_of_lava_walls = 0
            i = 0
            while (objects_map.get(f"lava wall {number_of_lava_walls + i}") != None):
                objects_map.pop(f"lava wall {number_of_lava_walls + i}")
                i += 1
            wall_instance0 = Wall()
            wall_instance0.xy = (8, 21)
            wall_instance0.wh = (152, 38)
            objects_map['fixed wall 0'] = wall_instance0
            wall_instance1 = Wall()
            wall_instance1.xy = (132, 101)
            wall_instance1.wh = (28, 38)
            objects_map['fixed wall 1'] = wall_instance1
            wall_instance2 = Wall()
            wall_instance2.xy = (72, 101)
            wall_instance2.wh = (16, 38)
            objects_map['fixed wall 2'] = wall_instance2
            wall_instance3 = Wall()
            wall_instance3.xy = (8, 101)
            wall_instance3.wh = (20, 38)
            objects_map['fixed wall 3'] = wall_instance3
            number_of_walls = 4
            i = 0
            while (objects_map.get(f"fixed wall {number_of_walls + i}") != None):
                objects_map.pop(f"fixed wall {number_of_walls + i}")
                i += 1
        elif ram_state[28] == 13:
            wall_instance0 = LavaWall()
            wall_instance0.xy = (40, 61)
            wall_instance0.wh = (80, 37)
            objects_map['lava wall 0'] = wall_instance0
            number_of_lava_walls = 1
            i = 0
            while (objects_map.get(f"lava wall {number_of_lava_walls + i}") != None):
                objects_map.pop(f"lava wall {number_of_lava_walls + i}")
                i += 1
            wall_instance0 = Wall()
            wall_instance0.xy = (8, 21)
            wall_instance0.wh = (152, 38)
            objects_map['fixed wall 0'] = wall_instance0
            wall_instance1 = Wall()
            wall_instance1.xy = (136, 101)
            wall_instance1.wh = (24, 38)
            objects_map['fixed wall 1'] = wall_instance1
            wall_instance2 = Wall()
            wall_instance2.xy = (8, 101)
            wall_instance2.wh = (16, 38)
            objects_map['fixed wall 2'] = wall_instance2
            number_of_walls = 3
            i = 0
            while (objects_map.get(f"fixed wall {number_of_walls + i}") != None):
                objects_map.pop(f"fixed wall {number_of_walls + i}")
                i += 1
        elif ram_state[28] == 14:
            number_of_lava_walls = 0
            i = 0
            while (objects_map.get(f"lava wall {number_of_lava_walls + i}") != None):
                objects_map.pop(f"lava wall {number_of_lava_walls + i}")
                i += 1
            wall_instance0 = Wall()
            wall_instance0.xy = (8, 21)
            wall_instance0.wh = (152, 38)
            objects_map['fixed wall 0'] = wall_instance0
            wall_instance1 = Wall()
            wall_instance1.xy = (128, 101)
            wall_instance1.wh = (32, 38)
            objects_map['fixed wall 1'] = wall_instance1
            wall_instance2 = Wall()
            wall_instance2.xy = (68, 101)
            wall_instance2.wh = (24, 38)
            objects_map['fixed wall 2'] = wall_instance2
            wall_instance3 = Wall()
            wall_instance3.xy = (8, 101)
            wall_instance3.wh = (24, 38)
            objects_map['fixed wall 3'] = wall_instance3
            number_of_walls = 4
            i = 0
            while (objects_map.get(f"fixed wall {number_of_walls + i}") != None):
                objects_map.pop(f"fixed wall {number_of_walls + i}")
                i += 1
        elif ram_state[28] == 15:
            wall_instance0 = LavaWall()
            wall_instance0.xy = (72, 61)
            wall_instance0.wh = (16, 37)
            objects_map['lava wall 0'] = wall_instance0
            number_of_lava_walls = 1
            i = 0
            while (objects_map.get(f"lava wall {number_of_lava_walls + i}") != None):
                objects_map.pop(f"lava wall {number_of_lava_walls + i}")
                i += 1
            wall_instance0 = Wall()
            wall_instance0.xy = (8, 21)
            wall_instance0.wh = (152, 38)
            objects_map['fixed wall 0'] = wall_instance0
            wall_instance1 = Wall()
            wall_instance1.xy = (112, 101)
            wall_instance1.wh = (48, 38)
            objects_map['fixed wall 1'] = wall_instance1
            wall_instance2 = Wall()
            wall_instance2.xy = (8, 101)
            wall_instance2.wh = (40, 38)
            objects_map['fixed wall 2'] = wall_instance2
            number_of_walls = 3
            i = 0
            while (objects_map.get(f"fixed wall {number_of_walls + i}") != None):
                objects_map.pop(f"fixed wall {number_of_walls + i}")
                i += 1

    elif ram_state[117] == 16:
        if ram_state[28] == 0:
            wall_instance0 = LavaWall()
            wall_instance0.xy = (144, 61)
            wall_instance0.wh = (16, 37)
            objects_map['lava wall 0'] = wall_instance0
            wall_instance1 = LavaWall()
            wall_instance1.xy = (8, 61)
            wall_instance1.wh = (8, 37)
            objects_map['lava wall 1'] = wall_instance1
            number_of_lava_walls = 2
            i = 0
            while (objects_map.get(f"lava wall {number_of_lava_walls + i}") != None):
                objects_map.pop(f"lava wall {number_of_lava_walls + i}")
                i += 1
            wall_instance0 = Wall()
            wall_instance0.xy = (136, 21)
            wall_instance0.wh = (24, 38)
            objects_map['fixed wall 0'] = wall_instance0
            wall_instance1 = Wall()
            wall_instance1.xy = (8, 21)
            wall_instance1.wh = (16, 38)
            objects_map['fixed wall 1'] = wall_instance1
            wall_instance2 = Wall()
            wall_instance2.xy = (88, 101)
            wall_instance2.wh = (72, 38)
            objects_map['fixed wall 2'] = wall_instance2
            wall_instance3 = Wall()
            wall_instance3.xy = (8, 101)
            wall_instance3.wh = (64, 38)
            objects_map['fixed wall 3'] = wall_instance3
            number_of_walls = 4
            i = 0
            while (objects_map.get(f"fixed wall {number_of_walls + i}") != None):
                objects_map.pop(f"fixed wall {number_of_walls + i}")
                i += 1
        elif ram_state[28] == 1:
            wall_instance0 = LavaWall()
            wall_instance0.xy = (128, 61)
            wall_instance0.wh = (32, 37)
            objects_map['lava wall 0'] = wall_instance0
            wall_instance1 = LavaWall()
            wall_instance1.xy = (8, 61)
            wall_instance1.wh = (24, 37)
            objects_map['lava wall 1'] = wall_instance1
            number_of_lava_walls = 2
            i = 0
            while (objects_map.get(f"lava wall {number_of_lava_walls + i}") != None):
                objects_map.pop(f"lava wall {number_of_lava_walls + i}")
                i += 1
            wall_instance0 = Wall()
            wall_instance0.xy = (88, 21)
            wall_instance0.wh = (72, 38)
            objects_map['fixed wall 0'] = wall_instance0
            wall_instance1 = Wall()
            wall_instance1.xy = (8, 21)
            wall_instance1.wh = (64, 38)
            objects_map['fixed wall 1'] = wall_instance1
            wall_instance2 = Wall()
            wall_instance2.xy = (144, 101)
            wall_instance2.wh = (16, 38)
            objects_map['fixed wall 2'] = wall_instance2
            wall_instance3 = Wall()
            wall_instance3.xy = (48, 101)
            wall_instance3.wh = (64, 38)
            objects_map['fixed wall 3'] = wall_instance3
            wall_instance4 = Wall()
            wall_instance4.xy = (8, 101)
            wall_instance4.wh = (8, 38)
            objects_map['fixed wall 4'] = wall_instance4
            number_of_walls = 5
            i = 0
            while (objects_map.get(f"fixed wall {number_of_walls + i}") != None):
                objects_map.pop(f"fixed wall {number_of_walls + i}")
                i += 1
        elif ram_state[28] == 2:
            wall_instance0 = LavaWall()
            wall_instance0.xy = (136, 61)
            wall_instance0.wh = (24, 37)
            objects_map['lava wall 0'] = wall_instance0
            wall_instance1 = LavaWall()
            wall_instance1.xy = (40, 61)
            wall_instance1.wh = (80, 37)
            objects_map['lava wall 1'] = wall_instance1
            wall_instance2 = LavaWall()
            wall_instance2.xy = (8, 61)
            wall_instance2.wh = (16, 37)
            objects_map['lava wall 2'] = wall_instance2
            number_of_lava_walls = 3
            i = 0
            while (objects_map.get(f"lava wall {number_of_lava_walls + i}") != None):
                objects_map.pop(f"lava wall {number_of_lava_walls + i}")
                i += 1
            wall_instance0 = Wall()
            wall_instance0.xy = (144, 21)
            wall_instance0.wh = (16, 38)
            objects_map['fixed wall 0'] = wall_instance0
            wall_instance1 = Wall()
            wall_instance1.xy = (48, 21)
            wall_instance1.wh = (64, 38)
            objects_map['fixed wall 1'] = wall_instance1
            wall_instance2 = Wall()
            wall_instance2.xy = (8, 21)
            wall_instance2.wh = (8, 38)
            objects_map['fixed wall 2'] = wall_instance2
            wall_instance3 = Wall()
            wall_instance3.xy = (128, 101)
            wall_instance3.wh = (32, 38)
            objects_map['fixed wall 3'] = wall_instance3
            wall_instance4 = Wall()
            wall_instance4.xy = (8, 101)
            wall_instance4.wh = (24, 38)
            objects_map['fixed wall 4'] = wall_instance4
            number_of_walls = 5
            i = 0
            while (objects_map.get(f"fixed wall {number_of_walls + i}") != None):
                objects_map.pop(f"fixed wall {number_of_walls + i}")
                i += 1
        elif ram_state[28] == 3:
            number_of_lava_walls = 0
            i = 0
            while (objects_map.get(f"lava wall {number_of_lava_walls + i}") != None):
                objects_map.pop(f"lava wall {number_of_lava_walls + i}")
                i += 1
            wall_instance0 = Wall()
            wall_instance0.xy = (128, 21)
            wall_instance0.wh = (32, 38)
            objects_map['fixed wall 0'] = wall_instance0
            wall_instance1 = Wall()
            wall_instance1.xy = (8, 21)
            wall_instance1.wh = (24, 38)
            objects_map['fixed wall 1'] = wall_instance1
            wall_instance2 = Wall()
            wall_instance2.xy = (112, 61)
            wall_instance2.wh = (48, 37)
            objects_map['fixed wall 2'] = wall_instance2
            wall_instance3 = Wall()
            wall_instance3.xy = (8, 61)
            wall_instance3.wh = (40, 37)
            objects_map['fixed wall 3'] = wall_instance3
            wall_instance4 = Wall()
            wall_instance4.xy = (144, 101)
            wall_instance4.wh = (16, 38)
            objects_map['fixed wall 4'] = wall_instance4
            wall_instance5 = Wall()
            wall_instance5.xy = (8, 101)
            wall_instance5.wh = (8, 38)
            objects_map['fixed wall 5'] = wall_instance5
            number_of_walls = 6
            i = 0
            while (objects_map.get(f"fixed wall {number_of_walls + i}") != None):
                objects_map.pop(f"fixed wall {number_of_walls + i}")
                i += 1
        elif ram_state[28] == 4:
            wall_instance0 = LavaWall()
            wall_instance0.xy = (104, 61)
            wall_instance0.wh = (56, 37)
            objects_map['lava wall 0'] = wall_instance0
            wall_instance1 = LavaWall()
            wall_instance1.xy = (8, 61)
            wall_instance1.wh = (48, 37)
            objects_map['lava wall 1'] = wall_instance1
            number_of_lava_walls = 2
            i = 0
            while (objects_map.get(f"lava wall {number_of_lava_walls + i}") != None):
                objects_map.pop(f"lava wall {number_of_lava_walls + i}")
                i += 1
            wall_instance0 = Wall()
            wall_instance0.xy = (144, 21)
            wall_instance0.wh = (16, 38)
            objects_map['fixed wall 0'] = wall_instance0
            wall_instance1 = Wall()
            wall_instance1.xy = (8, 21)
            wall_instance1.wh = (8, 38)
            objects_map['fixed wall 1'] = wall_instance1
            wall_instance2 = Wall()
            wall_instance2.xy = (112, 101)
            wall_instance2.wh = (48, 38)
            objects_map['fixed wall 2'] = wall_instance2
            wall_instance3 = Wall()
            wall_instance3.xy = (8, 101)
            wall_instance3.wh = (40, 38)
            objects_map['fixed wall 3'] = wall_instance3
            number_of_walls = 4
            i = 0
            while (objects_map.get(f"fixed wall {number_of_walls + i}") != None):
                objects_map.pop(f"fixed wall {number_of_walls + i}")
                i += 1
        elif ram_state[28] == 5:
            wall_instance0 = LavaWall()
            wall_instance0.xy = (104, 61)
            wall_instance0.wh = (56, 37)
            objects_map['lava wall 0'] = wall_instance0
            wall_instance1 = LavaWall()
            wall_instance1.xy = (8, 61)
            wall_instance1.wh = (48, 37)
            objects_map['lava wall 1'] = wall_instance1
            number_of_lava_walls = 2
            i = 0
            while (objects_map.get(f"lava wall {number_of_lava_walls + i}") != None):
                objects_map.pop(f"lava wall {number_of_lava_walls + i}")
                i += 1
            wall_instance0 = Wall()
            wall_instance0.xy = (112, 21)
            wall_instance0.wh = (48, 38)
            objects_map['fixed wall 0'] = wall_instance0
            wall_instance1 = Wall()
            wall_instance1.xy = (8, 21)
            wall_instance1.wh = (40, 38)
            objects_map['fixed wall 1'] = wall_instance1
            wall_instance2 = Wall()
            wall_instance2.xy = (84, 101)
            wall_instance2.wh = (76, 38)
            objects_map['fixed wall 2'] = wall_instance2
            wall_instance3 = Wall()
            wall_instance3.xy = (8, 101)
            wall_instance3.wh = (68, 38)
            objects_map['fixed wall 3'] = wall_instance3
            number_of_walls = 4
            i = 0
            while (objects_map.get(f"fixed wall {number_of_walls + i}") != None):
                objects_map.pop(f"fixed wall {number_of_walls + i}")
                i += 1
        elif ram_state[28] == 6:
            wall_instance0 = LavaWall()
            wall_instance0.xy = (144, 61)
            wall_instance0.wh = (16, 37)
            objects_map['lava wall 0'] = wall_instance0
            wall_instance1 = LavaWall()
            wall_instance1.xy = (8, 61)
            wall_instance1.wh = (8, 37)
            objects_map['lava wall 1'] = wall_instance1
            number_of_lava_walls = 2
            i = 0
            while (objects_map.get(f"lava wall {number_of_lava_walls + i}") != None):
                objects_map.pop(f"lava wall {number_of_lava_walls + i}")
                i += 1
            wall_instance0 = Wall()
            wall_instance0.xy = (84, 21)
            wall_instance0.wh = (76, 38)
            objects_map['fixed wall 0'] = wall_instance0
            wall_instance1 = Wall()
            wall_instance1.xy = (8, 21)
            wall_instance1.wh = (68, 38)
            objects_map['fixed wall 1'] = wall_instance1
            wall_instance2 = Wall()
            wall_instance2.xy = (136, 101)
            wall_instance2.wh = (24, 38)
            objects_map['fixed wall 2'] = wall_instance2
            wall_instance3 = Wall()
            wall_instance3.xy = (32, 101)
            wall_instance3.wh = (96, 38)
            objects_map['fixed wall 3'] = wall_instance3
            wall_instance4 = Wall()
            wall_instance4.xy = (8, 101)
            wall_instance4.wh = (16, 38)
            objects_map['fixed wall 4'] = wall_instance4
            number_of_walls = 5
            i = 0
            while (objects_map.get(f"fixed wall {number_of_walls + i}") != None):
                objects_map.pop(f"fixed wall {number_of_walls + i}")
                i += 1
        elif ram_state[28] == 7:
            wall_instance0 = LavaWall()
            wall_instance0.xy = (144, 61)
            wall_instance0.wh = (16, 37)
            objects_map['lava wall 0'] = wall_instance0
            wall_instance1 = LavaWall()
            wall_instance1.xy = (8, 61)
            wall_instance1.wh = (8, 37)
            objects_map['lava wall 1'] = wall_instance1
            number_of_lava_walls = 2
            i = 0
            while (objects_map.get(f"lava wall {number_of_lava_walls + i}") != None):
                objects_map.pop(f"lava wall {number_of_lava_walls + i}")
                i += 1
            wall_instance0 = Wall()
            wall_instance0.xy = (136, 21)
            wall_instance0.wh = (24, 38)
            objects_map['fixed wall 0'] = wall_instance0
            wall_instance1 = Wall()
            wall_instance1.xy = (32, 21)
            wall_instance1.wh = (96, 38)
            objects_map['fixed wall 1'] = wall_instance1
            wall_instance2 = Wall()
            wall_instance2.xy = (8, 21)
            wall_instance2.wh = (16, 38)
            objects_map['fixed wall 2'] = wall_instance2
            wall_instance3 = Wall()
            wall_instance3.xy = (8, 101)
            wall_instance3.wh = (152, 38)
            objects_map['fixed wall 3'] = wall_instance3
            number_of_walls = 4
            i = 0
            while (objects_map.get(f"fixed wall {number_of_walls + i}") != None):
                objects_map.pop(f"fixed wall {number_of_walls + i}")
                i += 1
        elif ram_state[28] == 8:
            wall_instance0 = LavaWall()
            wall_instance0.xy = (80, 61)
            wall_instance0.wh = (32, 37)
            objects_map['lava wall 0'] = wall_instance0
            wall_instance1 = LavaWall()
            wall_instance1.xy = (8, 61)
            wall_instance1.wh = (24, 37)
            objects_map['lava wall 1'] = wall_instance1
            number_of_lava_walls = 2
            i = 0
            while (objects_map.get(f"lava wall {number_of_lava_walls + i}") != None):
                objects_map.pop(f"lava wall {number_of_lava_walls + i}")
                i += 1
            wall_instance0 = Wall()
            wall_instance0.xy = (8, 21)
            wall_instance0.wh = (152, 38)
            objects_map['fixed wall 0'] = wall_instance0
            wall_instance1 = Wall()
            wall_instance1.xy = (136, 101)
            wall_instance1.wh = (24, 38)
            objects_map['fixed wall 1'] = wall_instance1
            wall_instance2 = Wall()
            wall_instance2.xy = (8, 101)
            wall_instance2.wh = (16, 38)
            objects_map['fixed wall 2'] = wall_instance2
            number_of_walls = 3
            i = 0
            while (objects_map.get(f"fixed wall {number_of_walls + i}") != None):
                objects_map.pop(f"fixed wall {number_of_walls + i}")
                i += 1
        elif ram_state[28] == 9:
            wall_instance0 = LavaWall()
            wall_instance0.xy = (84, 61)
            wall_instance0.wh = (76, 37)
            objects_map['lava wall 0'] = wall_instance0
            wall_instance1 = LavaWall()
            wall_instance1.xy = (8, 61)
            wall_instance1.wh = (68, 37)
            objects_map['lava wall 1'] = wall_instance1
            number_of_lava_walls = 2
            i = 0
            while (objects_map.get(f"lava wall {number_of_lava_walls + i}") != None):
                objects_map.pop(f"lava wall {number_of_lava_walls + i}")
                i += 1
            wall_instance0 = Wall()
            wall_instance0.xy = (136, 21)
            wall_instance0.wh = (24, 38)
            objects_map['fixed wall 0'] = wall_instance0
            wall_instance1 = Wall()
            wall_instance1.xy = (8, 21)
            wall_instance1.wh = (16, 38)
            objects_map['fixed wall 1'] = wall_instance1
            wall_instance2 = Wall()
            wall_instance2.xy = (108, 101)
            wall_instance2.wh = (52, 38)
            objects_map['fixed wall 2'] = wall_instance2
            wall_instance3 = Wall()
            wall_instance3.xy = (8, 101)
            wall_instance3.wh = (44, 38)
            objects_map['fixed wall 3'] = wall_instance3
            number_of_walls = 4
            i = 0
            while (objects_map.get(f"fixed wall {number_of_walls + i}") != None):
                objects_map.pop(f"fixed wall {number_of_walls + i}")
                i += 1
        elif ram_state[28] == 10:
            number_of_lava_walls = 0
            i = 0
            while (objects_map.get(f"lava wall {number_of_lava_walls + i}") != None):
                objects_map.pop(f"lava wall {number_of_lava_walls + i}")
                i += 1
            wall_instance0 = Wall()
            wall_instance0.xy = (108, 21)
            wall_instance0.wh = (52, 38)
            objects_map['fixed wall 0'] = wall_instance0
            wall_instance1 = Wall()
            wall_instance1.xy = (8, 21)
            wall_instance1.wh = (44, 38)
            objects_map['fixed wall 1'] = wall_instance1
            wall_instance2 = Wall()
            wall_instance2.xy = (136, 101)
            wall_instance2.wh = (24, 38)
            objects_map['fixed wall 2'] = wall_instance2
            wall_instance3 = Wall()
            wall_instance3.xy = (36, 101)
            wall_instance3.wh = (88, 38)
            objects_map['fixed wall 3'] = wall_instance3
            wall_instance4 = Wall()
            wall_instance4.xy = (8, 101)
            wall_instance4.wh = (16, 38)
            objects_map['fixed wall 4'] = wall_instance4
            number_of_walls = 5
            i = 0
            while (objects_map.get(f"fixed wall {number_of_walls + i}") != None):
                objects_map.pop(f"fixed wall {number_of_walls + i}")
                i += 1
        elif ram_state[28] == 11:
            number_of_lava_walls = 0
            i = 0
            while (objects_map.get(f"lava wall {number_of_lava_walls + i}") != None):
                objects_map.pop(f"lava wall {number_of_lava_walls + i}")
                i += 1
            wall_instance0 = Wall()
            wall_instance0.xy = (8, 21)
            wall_instance0.wh = (152, 38)
            objects_map['fixed wall 0'] = wall_instance0
            wall_instance1 = Wall()
            wall_instance1.xy = (48, 61)
            wall_instance1.wh = (64, 37)
            objects_map['fixed wall 1'] = wall_instance1
            wall_instance2 = Wall()
            wall_instance2.xy = (132, 101)
            wall_instance2.wh = (28, 38)
            objects_map['fixed wall 2'] = wall_instance2
            wall_instance3 = Wall()
            wall_instance3.xy = (8, 101)
            wall_instance3.wh = (20, 38)
            objects_map['fixed wall 3'] = wall_instance3
            number_of_walls = 4
            i = 0
            while (objects_map.get(f"fixed wall {number_of_walls + i}") != None):
                objects_map.pop(f"fixed wall {number_of_walls + i}")
                i += 1
        elif ram_state[28] == 12:
            number_of_lava_walls = 0
            i = 0
            while (objects_map.get(f"lava wall {number_of_lava_walls + i}") != None):
                objects_map.pop(f"lava wall {number_of_lava_walls + i}")
                i += 1
            wall_instance0 = Wall()
            wall_instance0.xy = (8, 21)
            wall_instance0.wh = (152, 38)
            objects_map['fixed wall 0'] = wall_instance0
            wall_instance1 = Wall()
            wall_instance1.xy = (132, 101)
            wall_instance1.wh = (28, 38)
            objects_map['fixed wall 1'] = wall_instance1
            wall_instance2 = Wall()
            wall_instance2.xy = (72, 101)
            wall_instance2.wh = (16, 38)
            objects_map['fixed wall 2'] = wall_instance2
            wall_instance3 = Wall()
            wall_instance3.xy = (8, 101)
            wall_instance3.wh = (20, 38)
            objects_map['fixed wall 3'] = wall_instance3
            number_of_walls = 4
            i = 0
            while (objects_map.get(f"fixed wall {number_of_walls + i}") != None):
                objects_map.pop(f"fixed wall {number_of_walls + i}")
                i += 1
        elif ram_state[28] == 13:
            number_of_lava_walls = 0
            i = 0
            while (objects_map.get(f"lava wall {number_of_lava_walls + i}") != None):
                objects_map.pop(f"lava wall {number_of_lava_walls + i}")
                i += 1
            wall_instance0 = Wall()
            wall_instance0.xy = (8, 21)
            wall_instance0.wh = (152, 38)
            objects_map['fixed wall 0'] = wall_instance0
            wall_instance1 = Wall()
            wall_instance1.xy = (132, 101)
            wall_instance1.wh = (28, 38)
            objects_map['fixed wall 1'] = wall_instance1
            wall_instance2 = Wall()
            wall_instance2.xy = (72, 101)
            wall_instance2.wh = (16, 38)
            objects_map['fixed wall 2'] = wall_instance2
            wall_instance3 = Wall()
            wall_instance3.xy = (8, 101)
            wall_instance3.wh = (20, 38)
            objects_map['fixed wall 3'] = wall_instance3
            number_of_walls = 4
            i = 0
            while (objects_map.get(f"fixed wall {number_of_walls + i}") != None):
                objects_map.pop(f"fixed wall {number_of_walls + i}")
                i += 1
        elif ram_state[28] == 14:
            wall_instance0 = LavaWall()
            wall_instance0.xy = (48, 61)
            wall_instance0.wh = (64, 37)
            objects_map['lava wall 0'] = wall_instance0
            number_of_lava_walls = 1
            i = 0
            while (objects_map.get(f"lava wall {number_of_lava_walls + i}") != None):
                objects_map.pop(f"lava wall {number_of_lava_walls + i}")
                i += 1
            wall_instance0 = Wall()
            wall_instance0.xy = (8, 21)
            wall_instance0.wh = (152, 38)
            objects_map['fixed wall 0'] = wall_instance0
            wall_instance1 = Wall()
            wall_instance1.xy = (136, 101)
            wall_instance1.wh = (24, 38)
            objects_map['fixed wall 1'] = wall_instance1
            wall_instance2 = Wall()
            wall_instance2.xy = (8, 101)
            wall_instance2.wh = (16, 38)
            objects_map['fixed wall 2'] = wall_instance2
            number_of_walls = 3
            i = 0
            while (objects_map.get(f"fixed wall {number_of_walls + i}") != None):
                objects_map.pop(f"fixed wall {number_of_walls + i}")
                i += 1
        elif ram_state[28] == 15:
            number_of_lava_walls = 0
            i = 0
            while (objects_map.get(f"lava wall {number_of_lava_walls + i}") != None):
                objects_map.pop(f"lava wall {number_of_lava_walls + i}")
                i += 1
            wall_instance0 = Wall()
            wall_instance0.xy = (8, 21)
            wall_instance0.wh = (152, 38)
            objects_map['fixed wall 0'] = wall_instance0
            wall_instance1 = Wall()
            wall_instance1.xy = (124, 101)
            wall_instance1.wh = (36, 38)
            objects_map['fixed wall 1'] = wall_instance1
            wall_instance2 = Wall()
            wall_instance2.xy = (8, 101)
            wall_instance2.wh = (28, 38)
            objects_map['fixed wall 2'] = wall_instance2
            number_of_walls = 3
            i = 0
            while (objects_map.get(f"fixed wall {number_of_walls + i}") != None):
                objects_map.pop(f"fixed wall {number_of_walls + i}")
                i += 1

    elif ram_state[117] == 17:
        if ram_state[28] == 0:
            wall_instance0 = LavaWall()
            wall_instance0.xy = (144, 61)
            wall_instance0.wh = (16, 37)
            objects_map['lava wall 0'] = wall_instance0
            wall_instance1 = LavaWall()
            wall_instance1.xy = (8, 61)
            wall_instance1.wh = (8, 37)
            objects_map['lava wall 1'] = wall_instance1
            number_of_lava_walls = 2
            i = 0
            while (objects_map.get(f"lava wall {number_of_lava_walls + i}") != None):
                objects_map.pop(f"lava wall {number_of_lava_walls + i}")
                i += 1
            wall_instance0 = Wall()
            wall_instance0.xy = (136, 21)
            wall_instance0.wh = (24, 38)
            objects_map['fixed wall 0'] = wall_instance0
            wall_instance1 = Wall()
            wall_instance1.xy = (8, 21)
            wall_instance1.wh = (16, 38)
            objects_map['fixed wall 1'] = wall_instance1
            wall_instance2 = Wall()
            wall_instance2.xy = (88, 101)
            wall_instance2.wh = (72, 38)
            objects_map['fixed wall 2'] = wall_instance2
            wall_instance3 = Wall()
            wall_instance3.xy = (8, 101)
            wall_instance3.wh = (64, 38)
            objects_map['fixed wall 3'] = wall_instance3
            number_of_walls = 4
            i = 0
            while (objects_map.get(f"fixed wall {number_of_walls + i}") != None):
                objects_map.pop(f"fixed wall {number_of_walls + i}")
                i += 1
        elif ram_state[28] == 1:
            wall_instance0 = LavaWall()
            wall_instance0.xy = (144, 61)
            wall_instance0.wh = (16, 37)
            objects_map['lava wall 0'] = wall_instance0
            wall_instance1 = LavaWall()
            wall_instance1.xy = (8, 61)
            wall_instance1.wh = (8, 37)
            objects_map['lava wall 1'] = wall_instance1
            number_of_lava_walls = 2
            i = 0
            while (objects_map.get(f"lava wall {number_of_lava_walls + i}") != None):
                objects_map.pop(f"lava wall {number_of_lava_walls + i}")
                i += 1
            wall_instance0 = Wall()
            wall_instance0.xy = (88, 21)
            wall_instance0.wh = (72, 38)
            objects_map['fixed wall 0'] = wall_instance0
            wall_instance1 = Wall()
            wall_instance1.xy = (8, 21)
            wall_instance1.wh = (64, 38)
            objects_map['fixed wall 1'] = wall_instance1
            wall_instance2 = Wall()
            wall_instance2.xy = (136, 101)
            wall_instance2.wh = (24, 38)
            objects_map['fixed wall 2'] = wall_instance2
            wall_instance3 = Wall()
            wall_instance3.xy = (48, 101)
            wall_instance3.wh = (64, 38)
            objects_map['fixed wall 3'] = wall_instance3
            wall_instance4 = Wall()
            wall_instance4.xy = (8, 101)
            wall_instance4.wh = (16, 38)
            objects_map['fixed wall 4'] = wall_instance4
            number_of_walls = 5
            i = 0
            while (objects_map.get(f"fixed wall {number_of_walls + i}") != None):
                objects_map.pop(f"fixed wall {number_of_walls + i}")
                i += 1
        elif ram_state[28] == 2:
            wall_instance0 = LavaWall()
            wall_instance0.xy = (144, 61)
            wall_instance0.wh = (16, 37)
            objects_map['lava wall 0'] = wall_instance0
            wall_instance1 = LavaWall()
            wall_instance1.xy = (36, 61)
            wall_instance1.wh = (88, 37)
            objects_map['lava wall 1'] = wall_instance1
            wall_instance2 = LavaWall()
            wall_instance2.xy = (8, 61)
            wall_instance2.wh = (8, 37)
            objects_map['lava wall 2'] = wall_instance2
            number_of_lava_walls = 3
            i = 0
            while (objects_map.get(f"lava wall {number_of_lava_walls + i}") != None):
                objects_map.pop(f"lava wall {number_of_lava_walls + i}")
                i += 1
            wall_instance0 = Wall()
            wall_instance0.xy = (136, 21)
            wall_instance0.wh = (24, 38)
            objects_map['fixed wall 0'] = wall_instance0
            wall_instance1 = Wall()
            wall_instance1.xy = (48, 21)
            wall_instance1.wh = (64, 38)
            objects_map['fixed wall 1'] = wall_instance1
            wall_instance2 = Wall()
            wall_instance2.xy = (8, 21)
            wall_instance2.wh = (16, 38)
            objects_map['fixed wall 2'] = wall_instance2
            wall_instance3 = Wall()
            wall_instance3.xy = (132, 101)
            wall_instance3.wh = (28, 38)
            objects_map['fixed wall 3'] = wall_instance3
            wall_instance4 = Wall()
            wall_instance4.xy = (48, 101)
            wall_instance4.wh = (64, 38)
            objects_map['fixed wall 4'] = wall_instance4
            wall_instance5 = Wall()
            wall_instance5.xy = (8, 101)
            wall_instance5.wh = (20, 38)
            objects_map['fixed wall 5'] = wall_instance5
            number_of_walls = 6
            i = 0
            while (objects_map.get(f"fixed wall {number_of_walls + i}") != None):
                objects_map.pop(f"fixed wall {number_of_walls + i}")
                i += 1
        elif ram_state[28] == 3:
            wall_instance0 = LavaWall()
            wall_instance0.xy = (144, 61)
            wall_instance0.wh = (16, 37)
            objects_map['lava wall 0'] = wall_instance0
            wall_instance1 = LavaWall()
            wall_instance1.xy = (8, 61)
            wall_instance1.wh = (8, 37)
            objects_map['lava wall 1'] = wall_instance1
            number_of_lava_walls = 2
            i = 0
            while (objects_map.get(f"lava wall {number_of_lava_walls + i}") != None):
                objects_map.pop(f"lava wall {number_of_lava_walls + i}")
                i += 1
            wall_instance0 = Wall()
            wall_instance0.xy = (132, 21)
            wall_instance0.wh = (28, 38)
            objects_map['fixed wall 0'] = wall_instance0
            wall_instance1 = Wall()
            wall_instance1.xy = (48, 21)
            wall_instance1.wh = (64, 38)
            objects_map['fixed wall 1'] = wall_instance1
            wall_instance2 = Wall()
            wall_instance2.xy = (8, 21)
            wall_instance2.wh = (20, 38)
            objects_map['fixed wall 2'] = wall_instance2
            wall_instance3 = Wall()
            wall_instance3.xy = (88, 101)
            wall_instance3.wh = (72, 38)
            objects_map['fixed wall 3'] = wall_instance3
            wall_instance4 = Wall()
            wall_instance4.xy = (8, 101)
            wall_instance4.wh = (64, 38)
            objects_map['fixed wall 4'] = wall_instance4
            number_of_walls = 5
            i = 0
            while (objects_map.get(f"fixed wall {number_of_walls + i}") != None):
                objects_map.pop(f"fixed wall {number_of_walls + i}")
                i += 1
        elif ram_state[28] == 4:
            wall_instance0 = LavaWall()
            wall_instance0.xy = (144, 61)
            wall_instance0.wh = (16, 37)
            objects_map['lava wall 0'] = wall_instance0
            wall_instance1 = LavaWall()
            wall_instance1.xy = (8, 61)
            wall_instance1.wh = (8, 37)
            objects_map['lava wall 1'] = wall_instance1
            number_of_lava_walls = 2
            i = 0
            while (objects_map.get(f"lava wall {number_of_lava_walls + i}") != None):
                objects_map.pop(f"lava wall {number_of_lava_walls + i}")
                i += 1
            wall_instance0 = Wall()
            wall_instance0.xy = (88, 21)
            wall_instance0.wh = (72, 38)
            objects_map['fixed wall 0'] = wall_instance0
            wall_instance1 = Wall()
            wall_instance1.xy = (8, 21)
            wall_instance1.wh = (64, 38)
            objects_map['fixed wall 1'] = wall_instance1
            wall_instance2 = Wall()
            wall_instance2.xy = (136, 101)
            wall_instance2.wh = (24, 38)
            objects_map['fixed wall 2'] = wall_instance2
            wall_instance3 = Wall()
            wall_instance3.xy = (32, 101)
            wall_instance3.wh = (96, 38)
            objects_map['fixed wall 3'] = wall_instance3
            wall_instance4 = Wall()
            wall_instance4.xy = (8, 101)
            wall_instance4.wh = (16, 38)
            objects_map['fixed wall 4'] = wall_instance4
            number_of_walls = 5
            i = 0
            while (objects_map.get(f"fixed wall {number_of_walls + i}") != None):
                objects_map.pop(f"fixed wall {number_of_walls + i}")
                i += 1
        elif ram_state[28] == 5:
            wall_instance0 = LavaWall()
            wall_instance0.xy = (144, 61)
            wall_instance0.wh = (16, 37)
            objects_map['lava wall 0'] = wall_instance0
            wall_instance1 = LavaWall()
            wall_instance1.xy = (8, 61)
            wall_instance1.wh = (8, 37)
            objects_map['lava wall 1'] = wall_instance1
            number_of_lava_walls = 2
            i = 0
            while (objects_map.get(f"lava wall {number_of_lava_walls + i}") != None):
                objects_map.pop(f"lava wall {number_of_lava_walls + i}")
                i += 1
            wall_instance0 = Wall()
            wall_instance0.xy = (136, 21)
            wall_instance0.wh = (24, 38)
            objects_map['fixed wall 0'] = wall_instance0
            wall_instance1 = Wall()
            wall_instance1.xy = (32, 21)
            wall_instance1.wh = (96, 38)
            objects_map['fixed wall 1'] = wall_instance1
            wall_instance2 = Wall()
            wall_instance2.xy = (8, 21)
            wall_instance2.wh = (16, 38)
            objects_map['fixed wall 2'] = wall_instance2
            wall_instance3 = Wall()
            wall_instance3.xy = (8, 101)
            wall_instance3.wh = (152, 38)
            objects_map['fixed wall 3'] = wall_instance3
            number_of_walls = 4
            i = 0
            while (objects_map.get(f"fixed wall {number_of_walls + i}") != None):
                objects_map.pop(f"fixed wall {number_of_walls + i}")
                i += 1
        elif ram_state[28] == 6:
            wall_instance0 = LavaWall()
            wall_instance0.xy = (144, 61)
            wall_instance0.wh = (16, 37)
            objects_map['lava wall 0'] = wall_instance0
            wall_instance1 = LavaWall()
            wall_instance1.xy = (8, 61)
            wall_instance1.wh = (8, 37)
            objects_map['lava wall 1'] = wall_instance1
            number_of_lava_walls = 2
            i = 0
            while (objects_map.get(f"lava wall {number_of_lava_walls + i}") != None):
                objects_map.pop(f"lava wall {number_of_lava_walls + i}")
                i += 1
            wall_instance0 = Wall()
            wall_instance0.xy = (8, 21)
            wall_instance0.wh = (152, 38)
            objects_map['fixed wall 0'] = wall_instance0
            wall_instance1 = Wall()
            wall_instance1.xy = (128, 101)
            wall_instance1.wh = (32, 38)
            objects_map['fixed wall 1'] = wall_instance1
            wall_instance2 = Wall()
            wall_instance2.xy = (68, 101)
            wall_instance2.wh = (24, 38)
            objects_map['fixed wall 2'] = wall_instance2
            wall_instance3 = Wall()
            wall_instance3.xy = (8, 101)
            wall_instance3.wh = (24, 38)
            objects_map['fixed wall 3'] = wall_instance3
            number_of_walls = 4
            i = 0
            while (objects_map.get(f"fixed wall {number_of_walls + i}") != None):
                objects_map.pop(f"fixed wall {number_of_walls + i}")
                i += 1
        elif ram_state[28] == 7:
            wall_instance0 = LavaWall()
            wall_instance0.xy = (112, 61)
            wall_instance0.wh = (48, 37)
            objects_map['lava wall 0'] = wall_instance0
            wall_instance1 = LavaWall()
            wall_instance1.xy = (8, 61)
            wall_instance1.wh = (40, 37)
            objects_map['lava wall 1'] = wall_instance1
            number_of_lava_walls = 2
            i = 0
            while (objects_map.get(f"lava wall {number_of_lava_walls + i}") != None):
                objects_map.pop(f"lava wall {number_of_lava_walls + i}")
                i += 1
            wall_instance0 = Wall()
            wall_instance0.xy = (128, 21)
            wall_instance0.wh = (32, 38)
            objects_map['fixed wall 0'] = wall_instance0
            wall_instance1 = Wall()
            wall_instance1.xy = (68, 21)
            wall_instance1.wh = (24, 38)
            objects_map['fixed wall 1'] = wall_instance1
            wall_instance2 = Wall()
            wall_instance2.xy = (8, 21)
            wall_instance2.wh = (24, 38)
            objects_map['fixed wall 2'] = wall_instance2
            wall_instance3 = Wall()
            wall_instance3.xy = (84, 101)
            wall_instance3.wh = (76, 38)
            objects_map['fixed wall 3'] = wall_instance3
            wall_instance4 = Wall()
            wall_instance4.xy = (8, 101)
            wall_instance4.wh = (68, 38)
            objects_map['fixed wall 4'] = wall_instance4
            number_of_walls = 5
            i = 0
            while (objects_map.get(f"fixed wall {number_of_walls + i}") != None):
                objects_map.pop(f"fixed wall {number_of_walls + i}")
                i += 1
        elif ram_state[28] == 8:
            wall_instance0 = LavaWall()
            wall_instance0.xy = (84, 61)
            wall_instance0.wh = (76, 37)
            objects_map['lava wall 0'] = wall_instance0
            wall_instance1 = LavaWall()
            wall_instance1.xy = (8, 61)
            wall_instance1.wh = (68, 37)
            objects_map['lava wall 1'] = wall_instance1
            number_of_lava_walls = 2
            i = 0
            while (objects_map.get(f"lava wall {number_of_lava_walls + i}") != None):
                objects_map.pop(f"lava wall {number_of_lava_walls + i}")
                i += 1
            wall_instance0 = Wall()
            wall_instance0.xy = (84, 21)
            wall_instance0.wh = (76, 38)
            objects_map['fixed wall 0'] = wall_instance0
            wall_instance1 = Wall()
            wall_instance1.xy = (8, 21)
            wall_instance1.wh = (68, 38)
            objects_map['fixed wall 1'] = wall_instance1
            wall_instance2 = Wall()
            wall_instance2.xy = (84, 101)
            wall_instance2.wh = (76, 38)
            objects_map['fixed wall 2'] = wall_instance2
            wall_instance3 = Wall()
            wall_instance3.xy = (8, 101)
            wall_instance3.wh = (68, 38)
            objects_map['fixed wall 3'] = wall_instance3
            number_of_walls = 4
            i = 0
            while (objects_map.get(f"fixed wall {number_of_walls + i}") != None):
                objects_map.pop(f"fixed wall {number_of_walls + i}")
                i += 1
        elif ram_state[28] == 9:
            wall_instance0 = LavaWall()
            wall_instance0.xy = (144, 61)
            wall_instance0.wh = (16, 37)
            objects_map['lava wall 0'] = wall_instance0
            wall_instance1 = LavaWall()
            wall_instance1.xy = (92, 61)
            wall_instance1.wh = (12, 37)
            objects_map['lava wall 1'] = wall_instance1
            wall_instance2 = LavaWall()
            wall_instance2.xy = (56, 61)
            wall_instance2.wh = (12, 37)
            objects_map['lava wall 2'] = wall_instance2
            wall_instance3 = LavaWall()
            wall_instance3.xy = (8, 61)
            wall_instance3.wh = (8, 37)
            objects_map['lava wall 3'] = wall_instance3
            number_of_lava_walls = 4
            i = 0
            while (objects_map.get(f"lava wall {number_of_lava_walls + i}") != None):
                objects_map.pop(f"lava wall {number_of_lava_walls + i}")
                i += 1
            wall_instance0 = Wall()
            wall_instance0.xy = (84, 21)
            wall_instance0.wh = (76, 38)
            objects_map['fixed wall 0'] = wall_instance0
            wall_instance1 = Wall()
            wall_instance1.xy = (8, 21)
            wall_instance1.wh = (68, 38)
            objects_map['fixed wall 1'] = wall_instance1
            wall_instance2 = Wall()
            wall_instance2.xy = (140, 101)
            wall_instance2.wh = (20, 38)
            objects_map['fixed wall 2'] = wall_instance2
            wall_instance3 = Wall()
            wall_instance3.xy = (112, 101)
            wall_instance3.wh = (20, 38)
            objects_map['fixed wall 3'] = wall_instance3
            wall_instance4 = Wall()
            wall_instance4.xy = (84, 101)
            wall_instance4.wh = (20, 38)
            objects_map['fixed wall 4'] = wall_instance4
            wall_instance5 = Wall()
            wall_instance5.xy = (56, 101)
            wall_instance5.wh = (20, 38)
            objects_map['fixed wall 5'] = wall_instance5
            wall_instance6 = Wall()
            wall_instance6.xy = (28, 101)
            wall_instance6.wh = (20, 38)
            objects_map['fixed wall 6'] = wall_instance6
            wall_instance7 = Wall()
            wall_instance7.xy = (8, 101)
            wall_instance7.wh = (12, 38)
            objects_map['fixed wall 7'] = wall_instance7
            number_of_walls = 8
            i = 0
            while (objects_map.get(f"fixed wall {number_of_walls + i}") != None):
                objects_map.pop(f"fixed wall {number_of_walls + i}")
                i += 1
        elif ram_state[28] == 10:
            wall_instance0 = LavaWall()
            wall_instance0.xy = (116, 61)
            wall_instance0.wh = (12, 37)
            objects_map['lava wall 0'] = wall_instance0
            wall_instance1 = LavaWall()
            wall_instance1.xy = (32, 61)
            wall_instance1.wh = (12, 37)
            objects_map['lava wall 1'] = wall_instance1
            number_of_lava_walls = 2
            i = 0
            while (objects_map.get(f"lava wall {number_of_lava_walls + i}") != None):
                objects_map.pop(f"lava wall {number_of_lava_walls + i}")
                i += 1
            wall_instance0 = Wall()
            wall_instance0.xy = (140, 21)
            wall_instance0.wh = (20, 38)
            objects_map['fixed wall 0'] = wall_instance0
            wall_instance1 = Wall()
            wall_instance1.xy = (112, 21)
            wall_instance1.wh = (20, 38)
            objects_map['fixed wall 1'] = wall_instance1
            wall_instance2 = Wall()
            wall_instance2.xy = (84, 21)
            wall_instance2.wh = (20, 38)
            objects_map['fixed wall 2'] = wall_instance2
            wall_instance3 = Wall()
            wall_instance3.xy = (56, 21)
            wall_instance3.wh = (20, 38)
            objects_map['fixed wall 3'] = wall_instance3
            wall_instance4 = Wall()
            wall_instance4.xy = (28, 21)
            wall_instance4.wh = (20, 38)
            objects_map['fixed wall 4'] = wall_instance4
            wall_instance5 = Wall()
            wall_instance5.xy = (8, 21)
            wall_instance5.wh = (12, 38)
            objects_map['fixed wall 5'] = wall_instance5
            wall_instance6 = Wall()
            wall_instance6.xy = (8, 101)
            wall_instance6.wh = (152, 38)
            objects_map['fixed wall 6'] = wall_instance6
            number_of_walls = 7
            i = 0
            while (objects_map.get(f"fixed wall {number_of_walls + i}") != None):
                objects_map.pop(f"fixed wall {number_of_walls + i}")
                i += 1
        elif ram_state[28] == 11:
            number_of_lava_walls = 0
            i = 0
            while (objects_map.get(f"lava wall {number_of_lava_walls + i}") != None):
                objects_map.pop(f"lava wall {number_of_lava_walls + i}")
                i += 1
            wall_instance0 = Wall()
            wall_instance0.xy = (8, 21)
            wall_instance0.wh = (152, 38)
            objects_map['fixed wall 0'] = wall_instance0
            wall_instance1 = Wall()
            wall_instance1.xy = (48, 61)
            wall_instance1.wh = (64, 37)
            objects_map['fixed wall 1'] = wall_instance1
            wall_instance2 = Wall()
            wall_instance2.xy = (132, 101)
            wall_instance2.wh = (28, 38)
            objects_map['fixed wall 2'] = wall_instance2
            wall_instance3 = Wall()
            wall_instance3.xy = (8, 101)
            wall_instance3.wh = (20, 38)
            objects_map['fixed wall 3'] = wall_instance3
            number_of_walls = 4
            i = 0
            while (objects_map.get(f"fixed wall {number_of_walls + i}") != None):
                objects_map.pop(f"fixed wall {number_of_walls + i}")
                i += 1
        elif ram_state[28] == 12:
            wall_instance0 = LavaWall()
            wall_instance0.xy = (48, 61)
            wall_instance0.wh = (64, 37)
            objects_map['lava wall 0'] = wall_instance0
            number_of_lava_walls = 1
            i = 0
            while (objects_map.get(f"lava wall {number_of_lava_walls + i}") != None):
                objects_map.pop(f"lava wall {number_of_lava_walls + i}")
                i += 1
            wall_instance0 = Wall()
            wall_instance0.xy = (8, 21)
            wall_instance0.wh = (152, 38)
            objects_map['fixed wall 0'] = wall_instance0
            wall_instance1 = Wall()
            wall_instance1.xy = (136, 101)
            wall_instance1.wh = (24, 38)
            objects_map['fixed wall 1'] = wall_instance1
            wall_instance2 = Wall()
            wall_instance2.xy = (8, 101)
            wall_instance2.wh = (16, 38)
            objects_map['fixed wall 2'] = wall_instance2
            number_of_walls = 3
            i = 0
            while (objects_map.get(f"fixed wall {number_of_walls + i}") != None):
                objects_map.pop(f"fixed wall {number_of_walls + i}")
                i += 1
        elif ram_state[28] == 13:
            number_of_lava_walls = 0
            i = 0
            while (objects_map.get(f"lava wall {number_of_lava_walls + i}") != None):
                objects_map.pop(f"lava wall {number_of_lava_walls + i}")
                i += 1
            wall_instance0 = Wall()
            wall_instance0.xy = (8, 21)
            wall_instance0.wh = (152, 38)
            objects_map['fixed wall 0'] = wall_instance0
            wall_instance1 = Wall()
            wall_instance1.xy = (132, 101)
            wall_instance1.wh = (28, 38)
            objects_map['fixed wall 1'] = wall_instance1
            wall_instance2 = Wall()
            wall_instance2.xy = (72, 101)
            wall_instance2.wh = (16, 38)
            objects_map['fixed wall 2'] = wall_instance2
            wall_instance3 = Wall()
            wall_instance3.xy = (8, 101)
            wall_instance3.wh = (20, 38)
            objects_map['fixed wall 3'] = wall_instance3
            number_of_walls = 4
            i = 0
            while (objects_map.get(f"fixed wall {number_of_walls + i}") != None):
                objects_map.pop(f"fixed wall {number_of_walls + i}")
                i += 1
        elif ram_state[28] == 14:
            number_of_lava_walls = 0
            i = 0
            while (objects_map.get(f"lava wall {number_of_lava_walls + i}") != None):
                objects_map.pop(f"lava wall {number_of_lava_walls + i}")
                i += 1
            wall_instance0 = Wall()
            wall_instance0.xy = (8, 21)
            wall_instance0.wh = (152, 38)
            objects_map['fixed wall 0'] = wall_instance0
            wall_instance1 = Wall()
            wall_instance1.xy = (112, 101)
            wall_instance1.wh = (48, 38)
            objects_map['fixed wall 1'] = wall_instance1
            wall_instance2 = Wall()
            wall_instance2.xy = (8, 101)
            wall_instance2.wh = (40, 38)
            objects_map['fixed wall 2'] = wall_instance2
            number_of_walls = 3
            i = 0
            while (objects_map.get(f"fixed wall {number_of_walls + i}") != None):
                objects_map.pop(f"fixed wall {number_of_walls + i}")
                i += 1
        elif ram_state[28] == 15:
            wall_instance0 = LavaWall()
            wall_instance0.xy = (72, 61)
            wall_instance0.wh = (16, 37)
            objects_map['lava wall 0'] = wall_instance0
            number_of_lava_walls = 1
            i = 0
            while (objects_map.get(f"lava wall {number_of_lava_walls + i}") != None):
                objects_map.pop(f"lava wall {number_of_lava_walls + i}")
                i += 1
            wall_instance0 = Wall()
            wall_instance0.xy = (8, 21)
            wall_instance0.wh = (152, 38)
            objects_map['fixed wall 0'] = wall_instance0
            wall_instance1 = Wall()
            wall_instance1.xy = (120, 101)
            wall_instance1.wh = (40, 38)
            objects_map['fixed wall 1'] = wall_instance1
            wall_instance2 = Wall()
            wall_instance2.xy = (8, 101)
            wall_instance2.wh = (32, 38)
            objects_map['fixed wall 2'] = wall_instance2
            number_of_walls = 3
            i = 0
            while (objects_map.get(f"fixed wall {number_of_walls + i}") != None):
                objects_map.pop(f"fixed wall {number_of_walls + i}")
                i += 1

    elif ram_state[117] == 18:
        if ram_state[28] == 0:
            wall_instance0 = LavaWall()
            wall_instance0.xy = (144, 61)
            wall_instance0.wh = (16, 37)
            objects_map['lava wall 0'] = wall_instance0
            wall_instance1 = LavaWall()
            wall_instance1.xy = (8, 61)
            wall_instance1.wh = (8, 37)
            objects_map['lava wall 1'] = wall_instance1
            number_of_lava_walls = 2
            i = 0
            while (objects_map.get(f"lava wall {number_of_lava_walls + i}") != None):
                objects_map.pop(f"lava wall {number_of_lava_walls + i}")
                i += 1
            wall_instance0 = Wall()
            wall_instance0.xy = (136, 21)
            wall_instance0.wh = (24, 38)
            objects_map['fixed wall 0'] = wall_instance0
            wall_instance1 = Wall()
            wall_instance1.xy = (8, 21)
            wall_instance1.wh = (16, 38)
            objects_map['fixed wall 1'] = wall_instance1
            wall_instance2 = Wall()
            wall_instance2.xy = (84, 101)
            wall_instance2.wh = (76, 38)
            objects_map['fixed wall 2'] = wall_instance2
            wall_instance3 = Wall()
            wall_instance3.xy = (8, 101)
            wall_instance3.wh = (68, 38)
            objects_map['fixed wall 3'] = wall_instance3
            number_of_walls = 4
            i = 0
            while (objects_map.get(f"fixed wall {number_of_walls + i}") != None):
                objects_map.pop(f"fixed wall {number_of_walls + i}")
                i += 1
        elif ram_state[28] == 1:
            wall_instance0 = LavaWall()
            wall_instance0.xy = (144, 61)
            wall_instance0.wh = (16, 37)
            objects_map['lava wall 0'] = wall_instance0
            wall_instance1 = LavaWall()
            wall_instance1.xy = (8, 61)
            wall_instance1.wh = (8, 37)
            objects_map['lava wall 1'] = wall_instance1
            number_of_lava_walls = 2
            i = 0
            while (objects_map.get(f"lava wall {number_of_lava_walls + i}") != None):
                objects_map.pop(f"lava wall {number_of_lava_walls + i}")
                i += 1
            wall_instance0 = Wall()
            wall_instance0.xy = (84, 21)
            wall_instance0.wh = (76, 38)
            objects_map['fixed wall 0'] = wall_instance0
            wall_instance1 = Wall()
            wall_instance1.xy = (8, 21)
            wall_instance1.wh = (68, 38)
            objects_map['fixed wall 1'] = wall_instance1
            wall_instance2 = Wall()
            wall_instance2.xy = (120, 101)
            wall_instance2.wh = (40, 38)
            objects_map['fixed wall 2'] = wall_instance2
            wall_instance3 = Wall()
            wall_instance3.xy = (48, 101)
            wall_instance3.wh = (64, 38)
            objects_map['fixed wall 3'] = wall_instance3
            wall_instance4 = Wall()
            wall_instance4.xy = (8, 101)
            wall_instance4.wh = (32, 38)
            objects_map['fixed wall 4'] = wall_instance4
            number_of_walls = 5
            i = 0
            while (objects_map.get(f"fixed wall {number_of_walls + i}") != None):
                objects_map.pop(f"fixed wall {number_of_walls + i}")
                i += 1
        elif ram_state[28] == 2:
            wall_instance0 = LavaWall()
            wall_instance0.xy = (148, 61)
            wall_instance0.wh = (12, 37)
            objects_map['lava wall 0'] = wall_instance0
            wall_instance1 = LavaWall()
            wall_instance1.xy = (68, 61)
            wall_instance1.wh = (40, 37)
            objects_map['lava wall 1'] = wall_instance1
            wall_instance2 = LavaWall()
            wall_instance2.xy = (8, 61)
            wall_instance2.wh = (20, 37)
            objects_map['lava wall 2'] = wall_instance2
            number_of_lava_walls = 3
            i = 0
            while (objects_map.get(f"lava wall {number_of_lava_walls + i}") != None):
                objects_map.pop(f"lava wall {number_of_lava_walls + i}")
                i += 1
            wall_instance0 = Wall()
            wall_instance0.xy = (120, 21)
            wall_instance0.wh = (40, 38)
            objects_map['fixed wall 0'] = wall_instance0
            wall_instance1 = Wall()
            wall_instance1.xy = (48, 21)
            wall_instance1.wh = (64, 38)
            objects_map['fixed wall 1'] = wall_instance1
            wall_instance2 = Wall()
            wall_instance2.xy = (8, 21)
            wall_instance2.wh = (32, 38)
            objects_map['fixed wall 2'] = wall_instance2
            wall_instance3 = Wall()
            wall_instance3.xy = (100, 101)
            wall_instance3.wh = (60, 38)
            objects_map['fixed wall 3'] = wall_instance3
            wall_instance4 = Wall()
            wall_instance4.xy = (8, 101)
            wall_instance4.wh = (52, 38)
            objects_map['fixed wall 4'] = wall_instance4
            number_of_walls = 5
            i = 0
            while (objects_map.get(f"fixed wall {number_of_walls + i}") != None):
                objects_map.pop(f"fixed wall {number_of_walls + i}")
                i += 1
        elif ram_state[28] == 3:
            wall_instance0 = LavaWall()
            wall_instance0.xy = (128, 61)
            wall_instance0.wh = (32, 37)
            objects_map['lava wall 0'] = wall_instance0
            wall_instance1 = LavaWall()
            wall_instance1.xy = (8, 61)
            wall_instance1.wh = (24, 37)
            objects_map['lava wall 1'] = wall_instance1
            number_of_lava_walls = 2
            i = 0
            while (objects_map.get(f"lava wall {number_of_lava_walls + i}") != None):
                objects_map.pop(f"lava wall {number_of_lava_walls + i}")
                i += 1
            wall_instance0 = Wall()
            wall_instance0.xy = (100, 21)
            wall_instance0.wh = (60, 38)
            objects_map['fixed wall 0'] = wall_instance0
            wall_instance1 = Wall()
            wall_instance1.xy = (8, 21)
            wall_instance1.wh = (52, 38)
            objects_map['fixed wall 1'] = wall_instance1
            wall_instance2 = Wall()
            wall_instance2.xy = (144, 101)
            wall_instance2.wh = (16, 38)
            objects_map['fixed wall 2'] = wall_instance2
            wall_instance3 = Wall()
            wall_instance3.xy = (44, 101)
            wall_instance3.wh = (72, 38)
            objects_map['fixed wall 3'] = wall_instance3
            wall_instance4 = Wall()
            wall_instance4.xy = (8, 101)
            wall_instance4.wh = (8, 38)
            objects_map['fixed wall 4'] = wall_instance4
            number_of_walls = 5
            i = 0
            while (objects_map.get(f"fixed wall {number_of_walls + i}") != None):
                objects_map.pop(f"fixed wall {number_of_walls + i}")
                i += 1
        elif ram_state[28] == 4:
            wall_instance0 = LavaWall()
            wall_instance0.xy = (136, 61)
            wall_instance0.wh = (24, 37)
            objects_map['lava wall 0'] = wall_instance0
            wall_instance1 = LavaWall()
            wall_instance1.xy = (56, 61)
            wall_instance1.wh = (64, 37)
            objects_map['lava wall 1'] = wall_instance1
            wall_instance2 = LavaWall()
            wall_instance2.xy = (8, 61)
            wall_instance2.wh = (32, 37)
            objects_map['lava wall 2'] = wall_instance2
            number_of_lava_walls = 3
            i = 0
            while (objects_map.get(f"lava wall {number_of_lava_walls + i}") != None):
                objects_map.pop(f"lava wall {number_of_lava_walls + i}")
                i += 1
            wall_instance0 = Wall()
            wall_instance0.xy = (144, 21)
            wall_instance0.wh = (16, 38)
            objects_map['fixed wall 0'] = wall_instance0
            wall_instance1 = Wall()
            wall_instance1.xy = (44, 21)
            wall_instance1.wh = (72, 38)
            objects_map['fixed wall 1'] = wall_instance1
            wall_instance2 = Wall()
            wall_instance2.xy = (8, 21)
            wall_instance2.wh = (8, 38)
            objects_map['fixed wall 2'] = wall_instance2
            wall_instance3 = Wall()
            wall_instance3.xy = (144, 101)
            wall_instance3.wh = (16, 38)
            objects_map['fixed wall 3'] = wall_instance3
            wall_instance4 = Wall()
            wall_instance4.xy = (36, 101)
            wall_instance4.wh = (88, 38)
            objects_map['fixed wall 4'] = wall_instance4
            wall_instance5 = Wall()
            wall_instance5.xy = (8, 101)
            wall_instance5.wh = (8, 38)
            objects_map['fixed wall 5'] = wall_instance5
            number_of_walls = 6
            i = 0
            while (objects_map.get(f"fixed wall {number_of_walls + i}") != None):
                objects_map.pop(f"fixed wall {number_of_walls + i}")
                i += 1
        elif ram_state[28] == 5:
            wall_instance0 = LavaWall()
            wall_instance0.xy = (136, 61)
            wall_instance0.wh = (24, 37)
            objects_map['lava wall 0'] = wall_instance0
            wall_instance1 = LavaWall()
            wall_instance1.xy = (8, 61)
            wall_instance1.wh = (16, 37)
            objects_map['lava wall 1'] = wall_instance1
            number_of_lava_walls = 2
            i = 0
            while (objects_map.get(f"lava wall {number_of_lava_walls + i}") != None):
                objects_map.pop(f"lava wall {number_of_lava_walls + i}")
                i += 1
            wall_instance0 = Wall()
            wall_instance0.xy = (144, 21)
            wall_instance0.wh = (16, 38)
            objects_map['fixed wall 0'] = wall_instance0
            wall_instance1 = Wall()
            wall_instance1.xy = (36, 21)
            wall_instance1.wh = (88, 38)
            objects_map['fixed wall 1'] = wall_instance1
            wall_instance2 = Wall()
            wall_instance2.xy = (8, 21)
            wall_instance2.wh = (8, 38)
            objects_map['fixed wall 2'] = wall_instance2
            wall_instance3 = Wall()
            wall_instance3.xy = (84, 101)
            wall_instance3.wh = (76, 38)
            objects_map['fixed wall 3'] = wall_instance3
            wall_instance4 = Wall()
            wall_instance4.xy = (8, 101)
            wall_instance4.wh = (68, 38)
            objects_map['fixed wall 4'] = wall_instance4
            number_of_walls = 5
            i = 0
            while (objects_map.get(f"fixed wall {number_of_walls + i}") != None):
                objects_map.pop(f"fixed wall {number_of_walls + i}")
                i += 1
        elif ram_state[28] == 6:
            wall_instance0 = LavaWall()
            wall_instance0.xy = (92, 61)
            wall_instance0.wh = (68, 37)
            objects_map['lava wall 0'] = wall_instance0
            wall_instance1 = LavaWall()
            wall_instance1.xy = (8, 61)
            wall_instance1.wh = (60, 37)
            objects_map['lava wall 1'] = wall_instance1
            number_of_lava_walls = 2
            i = 0
            while (objects_map.get(f"lava wall {number_of_lava_walls + i}") != None):
                objects_map.pop(f"lava wall {number_of_lava_walls + i}")
                i += 1
            wall_instance0 = Wall()
            wall_instance0.xy = (84, 21)
            wall_instance0.wh = (76, 38)
            objects_map['fixed wall 0'] = wall_instance0
            wall_instance1 = Wall()
            wall_instance1.xy = (8, 21)
            wall_instance1.wh = (68, 38)
            objects_map['fixed wall 1'] = wall_instance1
            wall_instance2 = Wall()
            wall_instance2.xy = (112, 101)
            wall_instance2.wh = (48, 38)
            objects_map['fixed wall 2'] = wall_instance2
            wall_instance3 = Wall()
            wall_instance3.xy = (8, 101)
            wall_instance3.wh = (40, 38)
            objects_map['fixed wall 3'] = wall_instance3
            number_of_walls = 4
            i = 0
            while (objects_map.get(f"fixed wall {number_of_walls + i}") != None):
                objects_map.pop(f"fixed wall {number_of_walls + i}")
                i += 1
        elif ram_state[28] == 7:
            number_of_lava_walls = 0
            i = 0
            while (objects_map.get(f"lava wall {number_of_lava_walls + i}") != None):
                objects_map.pop(f"lava wall {number_of_lava_walls + i}")
                i += 1
            wall_instance0 = Wall()
            wall_instance0.xy = (112, 21)
            wall_instance0.wh = (48, 38)
            objects_map['fixed wall 0'] = wall_instance0
            wall_instance1 = Wall()
            wall_instance1.xy = (8, 21)
            wall_instance1.wh = (40, 38)
            objects_map['fixed wall 1'] = wall_instance1
            wall_instance2 = Wall()
            wall_instance2.xy = (152, 61)
            wall_instance2.wh = (8, 37)
            objects_map['fixed wall 2'] = wall_instance2
            wall_instance3 = Wall()
            wall_instance3.xy = (72, 61)
            wall_instance3.wh = (48, 37)
            objects_map['fixed wall 3'] = wall_instance3
            wall_instance4 = Wall()
            wall_instance4.xy = (8, 61)
            wall_instance4.wh = (32, 37)
            objects_map['fixed wall 4'] = wall_instance4
            wall_instance5 = Wall()
            wall_instance5.xy = (116, 101)
            wall_instance5.wh = (44, 38)
            objects_map['fixed wall 5'] = wall_instance5
            wall_instance6 = Wall()
            wall_instance6.xy = (8, 101)
            wall_instance6.wh = (36, 38)
            objects_map['fixed wall 6'] = wall_instance6
            number_of_walls = 7
            i = 0
            while (objects_map.get(f"fixed wall {number_of_walls + i}") != None):
                objects_map.pop(f"fixed wall {number_of_walls + i}")
                i += 1
        elif ram_state[28] == 8:
            wall_instance0 = LavaWall()
            wall_instance0.xy = (88, 61)
            wall_instance0.wh = (72, 37)
            objects_map['lava wall 0'] = wall_instance0
            wall_instance1 = LavaWall()
            wall_instance1.xy = (8, 61)
            wall_instance1.wh = (64, 37)
            objects_map['lava wall 1'] = wall_instance1
            number_of_lava_walls = 2
            i = 0
            while (objects_map.get(f"lava wall {number_of_lava_walls + i}") != None):
                objects_map.pop(f"lava wall {number_of_lava_walls + i}")
                i += 1
            wall_instance0 = Wall()
            wall_instance0.xy = (116, 21)
            wall_instance0.wh = (44, 38)
            objects_map['fixed wall 0'] = wall_instance0
            wall_instance1 = Wall()
            wall_instance1.xy = (8, 21)
            wall_instance1.wh = (36, 38)
            objects_map['fixed wall 1'] = wall_instance1
            wall_instance2 = Wall()
            wall_instance2.xy = (144, 101)
            wall_instance2.wh = (16, 38)
            objects_map['fixed wall 2'] = wall_instance2
            wall_instance3 = Wall()
            wall_instance3.xy = (8, 101)
            wall_instance3.wh = (8, 38)
            objects_map['fixed wall 3'] = wall_instance3
            number_of_walls = 4
            i = 0
            while (objects_map.get(f"fixed wall {number_of_walls + i}") != None):
                objects_map.pop(f"fixed wall {number_of_walls + i}")
                i += 1
        elif ram_state[28] == 9:
            wall_instance0 = LavaWall()
            wall_instance0.xy = (96, 61)
            wall_instance0.wh = (64, 37)
            objects_map['lava wall 0'] = wall_instance0
            wall_instance1 = LavaWall()
            wall_instance1.xy = (72, 61)
            wall_instance1.wh = (16, 37)
            objects_map['lava wall 1'] = wall_instance1
            wall_instance2 = LavaWall()
            wall_instance2.xy = (8, 61)
            wall_instance2.wh = (56, 37)
            objects_map['lava wall 2'] = wall_instance2
            number_of_lava_walls = 3
            i = 0
            while (objects_map.get(f"lava wall {number_of_lava_walls + i}") != None):
                objects_map.pop(f"lava wall {number_of_lava_walls + i}")
                i += 1
            wall_instance0 = Wall()
            wall_instance0.xy = (144, 21)
            wall_instance0.wh = (16, 38)
            objects_map['fixed wall 0'] = wall_instance0
            wall_instance1 = Wall()
            wall_instance1.xy = (8, 21)
            wall_instance1.wh = (8, 38)
            objects_map['fixed wall 1'] = wall_instance1
            wall_instance2 = Wall()
            wall_instance2.xy = (128, 101)
            wall_instance2.wh = (32, 38)
            objects_map['fixed wall 2'] = wall_instance2
            wall_instance3 = Wall()
            wall_instance3.xy = (8, 101)
            wall_instance3.wh = (24, 38)
            objects_map['fixed wall 3'] = wall_instance3
            number_of_walls = 4
            i = 0
            while (objects_map.get(f"fixed wall {number_of_walls + i}") != None):
                objects_map.pop(f"fixed wall {number_of_walls + i}")
                i += 1
        elif ram_state[28] == 10:
            number_of_lava_walls = 0
            i = 0
            while (objects_map.get(f"lava wall {number_of_lava_walls + i}") != None):
                objects_map.pop(f"lava wall {number_of_lava_walls + i}")
                i += 1
            wall_instance0 = Wall()
            wall_instance0.xy = (128, 21)
            wall_instance0.wh = (32, 38)
            objects_map['fixed wall 0'] = wall_instance0
            wall_instance1 = Wall()
            wall_instance1.xy = (8, 21)
            wall_instance1.wh = (24, 38)
            objects_map['fixed wall 1'] = wall_instance1
            wall_instance2 = Wall()
            wall_instance2.xy = (92, 61)
            wall_instance2.wh = (40, 37)
            objects_map['fixed wall 2'] = wall_instance2
            wall_instance3 = Wall()
            wall_instance3.xy = (28, 61)
            wall_instance3.wh = (40, 37)
            objects_map['fixed wall 3'] = wall_instance3
            wall_instance4 = Wall()
            wall_instance4.xy = (140, 101)
            wall_instance4.wh = (20, 38)
            objects_map['fixed wall 4'] = wall_instance4
            wall_instance5 = Wall()
            wall_instance5.xy = (8, 101)
            wall_instance5.wh = (12, 38)
            objects_map['fixed wall 5'] = wall_instance5
            number_of_walls = 6
            i = 0
            while (objects_map.get(f"fixed wall {number_of_walls + i}") != None):
                objects_map.pop(f"fixed wall {number_of_walls + i}")
                i += 1
        elif ram_state[28] == 11:
            number_of_lava_walls = 0
            i = 0
            while (objects_map.get(f"lava wall {number_of_lava_walls + i}") != None):
                objects_map.pop(f"lava wall {number_of_lava_walls + i}")
                i += 1
            wall_instance0 = Wall()
            wall_instance0.xy = (8, 21)
            wall_instance0.wh = (152, 38)
            objects_map['fixed wall 0'] = wall_instance0
            wall_instance1 = Wall()
            wall_instance1.xy = (56, 61)
            wall_instance1.wh = (48, 37)
            objects_map['fixed wall 1'] = wall_instance1
            wall_instance2 = Wall()
            wall_instance2.xy = (132, 101)
            wall_instance2.wh = (28, 38)
            objects_map['fixed wall 2'] = wall_instance2
            wall_instance3 = Wall()
            wall_instance3.xy = (8, 101)
            wall_instance3.wh = (20, 38)
            objects_map['fixed wall 3'] = wall_instance3
            number_of_walls = 4
            i = 0
            while (objects_map.get(f"fixed wall {number_of_walls + i}") != None):
                objects_map.pop(f"fixed wall {number_of_walls + i}")
                i += 1
        elif ram_state[28] == 12:
            wall_instance0 = LavaWall()
            wall_instance0.xy = (48, 61)
            wall_instance0.wh = (64, 37)
            objects_map['lava wall 0'] = wall_instance0
            number_of_lava_walls = 1
            i = 0
            while (objects_map.get(f"lava wall {number_of_lava_walls + i}") != None):
                objects_map.pop(f"lava wall {number_of_lava_walls + i}")
                i += 1
            wall_instance0 = Wall()
            wall_instance0.xy = (8, 21)
            wall_instance0.wh = (152, 38)
            objects_map['fixed wall 0'] = wall_instance0
            wall_instance1 = Wall()
            wall_instance1.xy = (136, 101)
            wall_instance1.wh = (24, 38)
            objects_map['fixed wall 1'] = wall_instance1
            wall_instance2 = Wall()
            wall_instance2.xy = (8, 101)
            wall_instance2.wh = (16, 38)
            objects_map['fixed wall 2'] = wall_instance2
            number_of_walls = 3
            i = 0
            while (objects_map.get(f"fixed wall {number_of_walls + i}") != None):
                objects_map.pop(f"fixed wall {number_of_walls + i}")
                i += 1
        elif ram_state[28] == 13:
            number_of_lava_walls = 0
            i = 0
            while (objects_map.get(f"lava wall {number_of_lava_walls + i}") != None):
                objects_map.pop(f"lava wall {number_of_lava_walls + i}")
                i += 1
            wall_instance0 = Wall()
            wall_instance0.xy = (8, 21)
            wall_instance0.wh = (152, 38)
            objects_map['fixed wall 0'] = wall_instance0
            wall_instance1 = Wall()
            wall_instance1.xy = (128, 101)
            wall_instance1.wh = (32, 38)
            objects_map['fixed wall 1'] = wall_instance1
            wall_instance2 = Wall()
            wall_instance2.xy = (72, 101)
            wall_instance2.wh = (16, 38)
            objects_map['fixed wall 2'] = wall_instance2
            wall_instance3 = Wall()
            wall_instance3.xy = (8, 101)
            wall_instance3.wh = (24, 38)
            objects_map['fixed wall 3'] = wall_instance3
            number_of_walls = 4
            i = 0
            while (objects_map.get(f"fixed wall {number_of_walls + i}") != None):
                objects_map.pop(f"fixed wall {number_of_walls + i}")
                i += 1
        elif ram_state[28] == 14:
            wall_instance0 = LavaWall()
            wall_instance0.xy = (72, 61)
            wall_instance0.wh = (16, 37)
            objects_map['lava wall 0'] = wall_instance0
            number_of_lava_walls = 1
            i = 0
            while (objects_map.get(f"lava wall {number_of_lava_walls + i}") != None):
                objects_map.pop(f"lava wall {number_of_lava_walls + i}")
                i += 1
            wall_instance0 = Wall()
            wall_instance0.xy = (8, 21)
            wall_instance0.wh = (152, 38)
            objects_map['fixed wall 0'] = wall_instance0
            wall_instance1 = Wall()
            wall_instance1.xy = (132, 101)
            wall_instance1.wh = (28, 38)
            objects_map['fixed wall 1'] = wall_instance1
            wall_instance2 = Wall()
            wall_instance2.xy = (8, 101)
            wall_instance2.wh = (20, 38)
            objects_map['fixed wall 2'] = wall_instance2
            number_of_walls = 3
            i = 0
            while (objects_map.get(f"fixed wall {number_of_walls + i}") != None):
                objects_map.pop(f"fixed wall {number_of_walls + i}")
                i += 1
        elif ram_state[28] == 15:
            wall_instance0 = LavaWall()
            wall_instance0.xy = (72, 61)
            wall_instance0.wh = (16, 37)
            objects_map['lava wall 0'] = wall_instance0
            number_of_lava_walls = 1
            i = 0
            while (objects_map.get(f"lava wall {number_of_lava_walls + i}") != None):
                objects_map.pop(f"lava wall {number_of_lava_walls + i}")
                i += 1
            wall_instance0 = Wall()
            wall_instance0.xy = (8, 21)
            wall_instance0.wh = (152, 38)
            objects_map['fixed wall 0'] = wall_instance0
            wall_instance1 = Wall()
            wall_instance1.xy = (112, 101)
            wall_instance1.wh = (48, 38)
            objects_map['fixed wall 1'] = wall_instance1
            wall_instance2 = Wall()
            wall_instance2.xy = (8, 101)
            wall_instance2.wh = (40, 38)
            objects_map['fixed wall 2'] = wall_instance2
            number_of_walls = 3
            i = 0
            while (objects_map.get(f"fixed wall {number_of_walls + i}") != None):
                objects_map.pop(f"fixed wall {number_of_walls + i}")
                i += 1

    elif ram_state[117] == 19:
        if ram_state[28] == 0:
            wall_instance0 = LavaWall()
            wall_instance0.xy = (144, 61)
            wall_instance0.wh = (16, 37)
            objects_map['lava wall 0'] = wall_instance0
            wall_instance1 = LavaWall()
            wall_instance1.xy = (8, 61)
            wall_instance1.wh = (8, 37)
            objects_map['lava wall 1'] = wall_instance1
            number_of_lava_walls = 2
            i = 0
            while (objects_map.get(f"lava wall {number_of_lava_walls + i}") != None):
                objects_map.pop(f"lava wall {number_of_lava_walls + i}")
                i += 1
            wall_instance0 = Wall()
            wall_instance0.xy = (136, 21)
            wall_instance0.wh = (24, 38)
            objects_map['fixed wall 0'] = wall_instance0
            wall_instance1 = Wall()
            wall_instance1.xy = (8, 21)
            wall_instance1.wh = (16, 38)
            objects_map['fixed wall 1'] = wall_instance1
            wall_instance2 = Wall()
            wall_instance2.xy = (84, 101)
            wall_instance2.wh = (76, 38)
            objects_map['fixed wall 2'] = wall_instance2
            wall_instance3 = Wall()
            wall_instance3.xy = (8, 101)
            wall_instance3.wh = (68, 38)
            objects_map['fixed wall 3'] = wall_instance3
            number_of_walls = 4
            i = 0
            while (objects_map.get(f"fixed wall {number_of_walls + i}") != None):
                objects_map.pop(f"fixed wall {number_of_walls + i}")
                i += 1
        elif ram_state[28] == 1:
            wall_instance0 = LavaWall()
            wall_instance0.xy = (144, 61)
            wall_instance0.wh = (16, 37)
            objects_map['lava wall 0'] = wall_instance0
            wall_instance1 = LavaWall()
            wall_instance1.xy = (8, 61)
            wall_instance1.wh = (8, 37)
            objects_map['lava wall 1'] = wall_instance1
            number_of_lava_walls = 2
            i = 0
            while (objects_map.get(f"lava wall {number_of_lava_walls + i}") != None):
                objects_map.pop(f"lava wall {number_of_lava_walls + i}")
                i += 1
            wall_instance0 = Wall()
            wall_instance0.xy = (84, 21)
            wall_instance0.wh = (76, 38)
            objects_map['fixed wall 0'] = wall_instance0
            wall_instance1 = Wall()
            wall_instance1.xy = (8, 21)
            wall_instance1.wh = (68, 38)
            objects_map['fixed wall 1'] = wall_instance1
            wall_instance2 = Wall()
            wall_instance2.xy = (136, 101)
            wall_instance2.wh = (24, 38)
            objects_map['fixed wall 2'] = wall_instance2
            wall_instance3 = Wall()
            wall_instance3.xy = (48, 101)
            wall_instance3.wh = (64, 38)
            objects_map['fixed wall 3'] = wall_instance3
            wall_instance4 = Wall()
            wall_instance4.xy = (8, 101)
            wall_instance4.wh = (16, 38)
            objects_map['fixed wall 4'] = wall_instance4
            number_of_walls = 5
            i = 0
            while (objects_map.get(f"fixed wall {number_of_walls + i}") != None):
                objects_map.pop(f"fixed wall {number_of_walls + i}")
                i += 1
        elif ram_state[28] == 2:
            number_of_lava_walls = 0
            i = 0
            while (objects_map.get(f"lava wall {number_of_lava_walls + i}") != None):
                objects_map.pop(f"lava wall {number_of_lava_walls + i}")
                i += 1
            wall_instance0 = Wall()
            wall_instance0.xy = (136, 21)
            wall_instance0.wh = (24, 38)
            objects_map['fixed wall 0'] = wall_instance0
            wall_instance1 = Wall()
            wall_instance1.xy = (48, 21)
            wall_instance1.wh = (64, 38)
            objects_map['fixed wall 1'] = wall_instance1
            wall_instance2 = Wall()
            wall_instance2.xy = (8, 21)
            wall_instance2.wh = (16, 38)
            objects_map['fixed wall 2'] = wall_instance2
            wall_instance3 = Wall()
            wall_instance3.xy = (128, 61)
            wall_instance3.wh = (32, 37)
            objects_map['fixed wall 3'] = wall_instance3
            wall_instance4 = Wall()
            wall_instance4.xy = (40, 61)
            wall_instance4.wh = (80, 37)
            objects_map['fixed wall 4'] = wall_instance4
            wall_instance5 = Wall()
            wall_instance5.xy = (8, 61)
            wall_instance5.wh = (24, 37)
            objects_map['fixed wall 5'] = wall_instance5
            wall_instance6 = Wall()
            wall_instance6.xy = (144, 101)
            wall_instance6.wh = (16, 38)
            objects_map['fixed wall 6'] = wall_instance6
            wall_instance7 = Wall()
            wall_instance7.xy = (8, 101)
            wall_instance7.wh = (8, 38)
            objects_map['fixed wall 7'] = wall_instance7
            number_of_walls = 8
            i = 0
            while (objects_map.get(f"fixed wall {number_of_walls + i}") != None):
                objects_map.pop(f"fixed wall {number_of_walls + i}")
                i += 1
        elif ram_state[28] == 3:
            wall_instance0 = LavaWall()
            wall_instance0.xy = (128, 61)
            wall_instance0.wh = (32, 37)
            objects_map['lava wall 0'] = wall_instance0
            wall_instance1 = LavaWall()
            wall_instance1.xy = (40, 61)
            wall_instance1.wh = (80, 37)
            objects_map['lava wall 1'] = wall_instance1
            wall_instance2 = LavaWall()
            wall_instance2.xy = (8, 61)
            wall_instance2.wh = (24, 37)
            objects_map['lava wall 2'] = wall_instance2
            number_of_lava_walls = 3
            i = 0
            while (objects_map.get(f"lava wall {number_of_lava_walls + i}") != None):
                objects_map.pop(f"lava wall {number_of_lava_walls + i}")
                i += 1
            wall_instance0 = Wall()
            wall_instance0.xy = (144, 21)
            wall_instance0.wh = (16, 38)
            objects_map['fixed wall 0'] = wall_instance0
            wall_instance1 = Wall()
            wall_instance1.xy = (8, 21)
            wall_instance1.wh = (8, 38)
            objects_map['fixed wall 1'] = wall_instance1
            wall_instance2 = Wall()
            wall_instance2.xy = (144, 101)
            wall_instance2.wh = (16, 38)
            objects_map['fixed wall 2'] = wall_instance2
            wall_instance3 = Wall()
            wall_instance3.xy = (8, 101)
            wall_instance3.wh = (8, 38)
            objects_map['fixed wall 3'] = wall_instance3
            number_of_walls = 4
            i = 0
            while (objects_map.get(f"fixed wall {number_of_walls + i}") != None):
                objects_map.pop(f"fixed wall {number_of_walls + i}")
                i += 1
        elif ram_state[28] == 4:
            wall_instance0 = LavaWall()
            wall_instance0.xy = (104, 61)
            wall_instance0.wh = (56, 37)
            objects_map['lava wall 0'] = wall_instance0
            wall_instance1 = LavaWall()
            wall_instance1.xy = (8, 61)
            wall_instance1.wh = (48, 37)
            objects_map['lava wall 1'] = wall_instance1
            number_of_lava_walls = 2
            i = 0
            while (objects_map.get(f"lava wall {number_of_lava_walls + i}") != None):
                objects_map.pop(f"lava wall {number_of_lava_walls + i}")
                i += 1
            wall_instance0 = Wall()
            wall_instance0.xy = (144, 21)
            wall_instance0.wh = (16, 38)
            objects_map['fixed wall 0'] = wall_instance0
            wall_instance1 = Wall()
            wall_instance1.xy = (8, 21)
            wall_instance1.wh = (8, 38)
            objects_map['fixed wall 1'] = wall_instance1
            wall_instance2 = Wall()
            wall_instance2.xy = (144, 101)
            wall_instance2.wh = (16, 38)
            objects_map['fixed wall 2'] = wall_instance2
            wall_instance3 = Wall()
            wall_instance3.xy = (8, 101)
            wall_instance3.wh = (8, 38)
            objects_map['fixed wall 3'] = wall_instance3
            number_of_walls = 4
            i = 0
            while (objects_map.get(f"fixed wall {number_of_walls + i}") != None):
                objects_map.pop(f"fixed wall {number_of_walls + i}")
                i += 1
        elif ram_state[28] == 5:
            wall_instance0 = LavaWall()
            wall_instance0.xy = (92, 61)
            wall_instance0.wh = (68, 37)
            objects_map['lava wall 0'] = wall_instance0
            wall_instance1 = LavaWall()
            wall_instance1.xy = (8, 61)
            wall_instance1.wh = (60, 37)
            objects_map['lava wall 1'] = wall_instance1
            number_of_lava_walls = 2
            i = 0
            while (objects_map.get(f"lava wall {number_of_lava_walls + i}") != None):
                objects_map.pop(f"lava wall {number_of_lava_walls + i}")
                i += 1
            wall_instance0 = Wall()
            wall_instance0.xy = (144, 21)
            wall_instance0.wh = (16, 38)
            objects_map['fixed wall 0'] = wall_instance0
            wall_instance1 = Wall()
            wall_instance1.xy = (8, 21)
            wall_instance1.wh = (8, 38)
            objects_map['fixed wall 1'] = wall_instance1
            wall_instance2 = Wall()
            wall_instance2.xy = (136, 101)
            wall_instance2.wh = (24, 38)
            objects_map['fixed wall 2'] = wall_instance2
            wall_instance3 = Wall()
            wall_instance3.xy = (8, 101)
            wall_instance3.wh = (16, 38)
            objects_map['fixed wall 3'] = wall_instance3
            number_of_walls = 4
            i = 0
            while (objects_map.get(f"fixed wall {number_of_walls + i}") != None):
                objects_map.pop(f"fixed wall {number_of_walls + i}")
                i += 1
        elif ram_state[28] == 6:
            wall_instance0 = LavaWall()
            wall_instance0.xy = (144, 61)
            wall_instance0.wh = (16, 37)
            objects_map['lava wall 0'] = wall_instance0
            wall_instance1 = LavaWall()
            wall_instance1.xy = (48, 61)
            wall_instance1.wh = (64, 37)
            objects_map['lava wall 1'] = wall_instance1
            wall_instance2 = LavaWall()
            wall_instance2.xy = (8, 61)
            wall_instance2.wh = (8, 37)
            objects_map['lava wall 2'] = wall_instance2
            number_of_lava_walls = 3
            i = 0
            while (objects_map.get(f"lava wall {number_of_lava_walls + i}") != None):
                objects_map.pop(f"lava wall {number_of_lava_walls + i}")
                i += 1
            wall_instance0 = Wall()
            wall_instance0.xy = (136, 21)
            wall_instance0.wh = (24, 38)
            objects_map['fixed wall 0'] = wall_instance0
            wall_instance1 = Wall()
            wall_instance1.xy = (8, 21)
            wall_instance1.wh = (16, 38)
            objects_map['fixed wall 1'] = wall_instance1
            wall_instance2 = Wall()
            wall_instance2.xy = (120, 101)
            wall_instance2.wh = (40, 38)
            objects_map['fixed wall 2'] = wall_instance2
            wall_instance3 = Wall()
            wall_instance3.xy = (8, 101)
            wall_instance3.wh = (32, 38)
            objects_map['fixed wall 3'] = wall_instance3
            number_of_walls = 4
            i = 0
            while (objects_map.get(f"fixed wall {number_of_walls + i}") != None):
                objects_map.pop(f"fixed wall {number_of_walls + i}")
                i += 1
        elif ram_state[28] == 7:
            wall_instance0 = LavaWall()
            wall_instance0.xy = (112, 61)
            wall_instance0.wh = (48, 37)
            objects_map['lava wall 0'] = wall_instance0
            wall_instance1 = LavaWall()
            wall_instance1.xy = (56, 61)
            wall_instance1.wh = (48, 37)
            objects_map['lava wall 1'] = wall_instance1
            wall_instance2 = LavaWall()
            wall_instance2.xy = (8, 61)
            wall_instance2.wh = (40, 37)
            objects_map['lava wall 2'] = wall_instance2
            number_of_lava_walls = 3
            i = 0
            while (objects_map.get(f"lava wall {number_of_lava_walls + i}") != None):
                objects_map.pop(f"lava wall {number_of_lava_walls + i}")
                i += 1
            wall_instance0 = Wall()
            wall_instance0.xy = (120, 21)
            wall_instance0.wh = (40, 38)
            objects_map['fixed wall 0'] = wall_instance0
            wall_instance1 = Wall()
            wall_instance1.xy = (8, 21)
            wall_instance1.wh = (32, 38)
            objects_map['fixed wall 1'] = wall_instance1
            wall_instance2 = Wall()
            wall_instance2.xy = (136, 101)
            wall_instance2.wh = (24, 38)
            objects_map['fixed wall 2'] = wall_instance2
            wall_instance3 = Wall()
            wall_instance3.xy = (64, 101)
            wall_instance3.wh = (32, 38)
            objects_map['fixed wall 3'] = wall_instance3
            wall_instance4 = Wall()
            wall_instance4.xy = (8, 101)
            wall_instance4.wh = (16, 38)
            objects_map['fixed wall 4'] = wall_instance4
            number_of_walls = 5
            i = 0
            while (objects_map.get(f"fixed wall {number_of_walls + i}") != None):
                objects_map.pop(f"fixed wall {number_of_walls + i}")
                i += 1
        elif ram_state[28] == 8:
            wall_instance0 = LavaWall()
            wall_instance0.xy = (144, 61)
            wall_instance0.wh = (16, 37)
            objects_map['lava wall 0'] = wall_instance0
            wall_instance1 = LavaWall()
            wall_instance1.xy = (56, 61)
            wall_instance1.wh = (48, 37)
            objects_map['lava wall 1'] = wall_instance1
            wall_instance2 = LavaWall()
            wall_instance2.xy = (8, 61)
            wall_instance2.wh = (8, 37)
            objects_map['lava wall 2'] = wall_instance2
            number_of_lava_walls = 3
            i = 0
            while (objects_map.get(f"lava wall {number_of_lava_walls + i}") != None):
                objects_map.pop(f"lava wall {number_of_lava_walls + i}")
                i += 1
            wall_instance0 = Wall()
            wall_instance0.xy = (136, 21)
            wall_instance0.wh = (24, 38)
            objects_map['fixed wall 0'] = wall_instance0
            wall_instance1 = Wall()
            wall_instance1.xy = (64, 21)
            wall_instance1.wh = (32, 38)
            objects_map['fixed wall 1'] = wall_instance1
            wall_instance2 = Wall()
            wall_instance2.xy = (8, 21)
            wall_instance2.wh = (16, 38)
            objects_map['fixed wall 2'] = wall_instance2
            wall_instance3 = Wall()
            wall_instance3.xy = (128, 101)
            wall_instance3.wh = (32, 38)
            objects_map['fixed wall 3'] = wall_instance3
            wall_instance4 = Wall()
            wall_instance4.xy = (64, 101)
            wall_instance4.wh = (32, 38)
            objects_map['fixed wall 4'] = wall_instance4
            wall_instance5 = Wall()
            wall_instance5.xy = (8, 101)
            wall_instance5.wh = (24, 38)
            objects_map['fixed wall 5'] = wall_instance5
            number_of_walls = 6
            i = 0
            while (objects_map.get(f"fixed wall {number_of_walls + i}") != None):
                objects_map.pop(f"fixed wall {number_of_walls + i}")
                i += 1
        elif ram_state[28] == 9:
            wall_instance0 = LavaWall()
            wall_instance0.xy = (112, 61)
            wall_instance0.wh = (48, 37)
            objects_map['lava wall 0'] = wall_instance0
            wall_instance1 = LavaWall()
            wall_instance1.xy = (56, 61)
            wall_instance1.wh = (48, 37)
            objects_map['lava wall 1'] = wall_instance1
            wall_instance2 = LavaWall()
            wall_instance2.xy = (8, 61)
            wall_instance2.wh = (40, 37)
            objects_map['lava wall 2'] = wall_instance2
            number_of_lava_walls = 3
            i = 0
            while (objects_map.get(f"lava wall {number_of_lava_walls + i}") != None):
                objects_map.pop(f"lava wall {number_of_lava_walls + i}")
                i += 1
            wall_instance0 = Wall()
            wall_instance0.xy = (128, 21)
            wall_instance0.wh = (32, 38)
            objects_map['fixed wall 0'] = wall_instance0
            wall_instance1 = Wall()
            wall_instance1.xy = (64, 21)
            wall_instance1.wh = (32, 38)
            objects_map['fixed wall 1'] = wall_instance1
            wall_instance2 = Wall()
            wall_instance2.xy = (8, 21)
            wall_instance2.wh = (24, 38)
            objects_map['fixed wall 2'] = wall_instance2
            wall_instance3 = Wall()
            wall_instance3.xy = (140, 101)
            wall_instance3.wh = (20, 38)
            objects_map['fixed wall 3'] = wall_instance3
            wall_instance4 = Wall()
            wall_instance4.xy = (64, 101)
            wall_instance4.wh = (32, 38)
            objects_map['fixed wall 4'] = wall_instance4
            wall_instance5 = Wall()
            wall_instance5.xy = (8, 101)
            wall_instance5.wh = (12, 38)
            objects_map['fixed wall 5'] = wall_instance5
            number_of_walls = 6
            i = 0
            while (objects_map.get(f"fixed wall {number_of_walls + i}") != None):
                objects_map.pop(f"fixed wall {number_of_walls + i}")
                i += 1
        elif ram_state[28] == 10:
            number_of_lava_walls = 0
            i = 0
            while (objects_map.get(f"lava wall {number_of_lava_walls + i}") != None):
                objects_map.pop(f"lava wall {number_of_lava_walls + i}")
                i += 1
            wall_instance0 = Wall()
            wall_instance0.xy = (140, 21)
            wall_instance0.wh = (20, 38)
            objects_map['fixed wall 0'] = wall_instance0
            wall_instance1 = Wall()
            wall_instance1.xy = (64, 21)
            wall_instance1.wh = (32, 38)
            objects_map['fixed wall 1'] = wall_instance1
            wall_instance2 = Wall()
            wall_instance2.xy = (8, 21)
            wall_instance2.wh = (12, 38)
            objects_map['fixed wall 2'] = wall_instance2
            wall_instance3 = Wall()
            wall_instance3.xy = (32, 61)
            wall_instance3.wh = (96, 37)
            objects_map['fixed wall 3'] = wall_instance3
            wall_instance4 = Wall()
            wall_instance4.xy = (140, 101)
            wall_instance4.wh = (20, 38)
            objects_map['fixed wall 4'] = wall_instance4
            wall_instance5 = Wall()
            wall_instance5.xy = (8, 101)
            wall_instance5.wh = (12, 38)
            objects_map['fixed wall 5'] = wall_instance5
            number_of_walls = 6
            i = 0
            while (objects_map.get(f"fixed wall {number_of_walls + i}") != None):
                objects_map.pop(f"fixed wall {number_of_walls + i}")
                i += 1
        elif ram_state[28] == 11:
            wall_instance0 = LavaWall()
            wall_instance0.xy = (40, 61)
            wall_instance0.wh = (80, 37)
            objects_map['lava wall 0'] = wall_instance0
            number_of_lava_walls = 1
            i = 0
            while (objects_map.get(f"lava wall {number_of_lava_walls + i}") != None):
                objects_map.pop(f"lava wall {number_of_lava_walls + i}")
                i += 1
            wall_instance0 = Wall()
            wall_instance0.xy = (8, 21)
            wall_instance0.wh = (152, 38)
            objects_map['fixed wall 0'] = wall_instance0
            wall_instance1 = Wall()
            wall_instance1.xy = (136, 101)
            wall_instance1.wh = (24, 38)
            objects_map['fixed wall 1'] = wall_instance1
            wall_instance2 = Wall()
            wall_instance2.xy = (8, 101)
            wall_instance2.wh = (16, 38)
            objects_map['fixed wall 2'] = wall_instance2
            number_of_walls = 3
            i = 0
            while (objects_map.get(f"fixed wall {number_of_walls + i}") != None):
                objects_map.pop(f"fixed wall {number_of_walls + i}")
                i += 1
        elif ram_state[28] == 12:
            wall_instance0 = LavaWall()
            wall_instance0.xy = (72, 61)
            wall_instance0.wh = (16, 37)
            objects_map['lava wall 0'] = wall_instance0
            number_of_lava_walls = 1
            i = 0
            while (objects_map.get(f"lava wall {number_of_lava_walls + i}") != None):
                objects_map.pop(f"lava wall {number_of_lava_walls + i}")
                i += 1
            wall_instance0 = Wall()
            wall_instance0.xy = (8, 21)
            wall_instance0.wh = (152, 38)
            objects_map['fixed wall 0'] = wall_instance0
            wall_instance1 = Wall()
            wall_instance1.xy = (132, 101)
            wall_instance1.wh = (28, 38)
            objects_map['fixed wall 1'] = wall_instance1
            wall_instance2 = Wall()
            wall_instance2.xy = (8, 101)
            wall_instance2.wh = (20, 38)
            objects_map['fixed wall 2'] = wall_instance2
            number_of_walls = 3
            i = 0
            while (objects_map.get(f"fixed wall {number_of_walls + i}") != None):
                objects_map.pop(f"fixed wall {number_of_walls + i}")
                i += 1
        elif ram_state[28] == 13:
            wall_instance0 = LavaWall()
            wall_instance0.xy = (64, 61)
            wall_instance0.wh = (32, 37)
            objects_map['lava wall 0'] = wall_instance0
            number_of_lava_walls = 1
            i = 0
            while (objects_map.get(f"lava wall {number_of_lava_walls + i}") != None):
                objects_map.pop(f"lava wall {number_of_lava_walls + i}")
                i += 1
            wall_instance0 = Wall()
            wall_instance0.xy = (8, 21)
            wall_instance0.wh = (152, 38)
            objects_map['fixed wall 0'] = wall_instance0
            wall_instance1 = Wall()
            wall_instance1.xy = (128, 101)
            wall_instance1.wh = (32, 38)
            objects_map['fixed wall 1'] = wall_instance1
            wall_instance2 = Wall()
            wall_instance2.xy = (8, 101)
            wall_instance2.wh = (24, 38)
            objects_map['fixed wall 2'] = wall_instance2
            number_of_walls = 3
            i = 0
            while (objects_map.get(f"fixed wall {number_of_walls + i}") != None):
                objects_map.pop(f"fixed wall {number_of_walls + i}")
                i += 1
        elif ram_state[28] == 14:
            wall_instance0 = LavaWall()
            wall_instance0.xy = (72, 61)
            wall_instance0.wh = (16, 37)
            objects_map['lava wall 0'] = wall_instance0
            number_of_lava_walls = 1
            i = 0
            while (objects_map.get(f"lava wall {number_of_lava_walls + i}") != None):
                objects_map.pop(f"lava wall {number_of_lava_walls + i}")
                i += 1
            wall_instance0 = Wall()
            wall_instance0.xy = (8, 21)
            wall_instance0.wh = (152, 38)
            objects_map['fixed wall 0'] = wall_instance0
            wall_instance1 = Wall()
            wall_instance1.xy = (132, 101)
            wall_instance1.wh = (28, 38)
            objects_map['fixed wall 1'] = wall_instance1
            wall_instance2 = Wall()
            wall_instance2.xy = (8, 101)
            wall_instance2.wh = (20, 38)
            objects_map['fixed wall 2'] = wall_instance2
            number_of_walls = 3
            i = 0
            while (objects_map.get(f"fixed wall {number_of_walls + i}") != None):
                objects_map.pop(f"fixed wall {number_of_walls + i}")
                i += 1
        elif ram_state[28] == 15:
            wall_instance0 = LavaWall()
            wall_instance0.xy = (72, 61)
            wall_instance0.wh = (16, 37)
            objects_map['lava wall 0'] = wall_instance0
            number_of_lava_walls = 1
            i = 0
            while (objects_map.get(f"lava wall {number_of_lava_walls + i}") != None):
                objects_map.pop(f"lava wall {number_of_lava_walls + i}")
                i += 1
            wall_instance0 = Wall()
            wall_instance0.xy = (8, 21)
            wall_instance0.wh = (152, 38)
            objects_map['fixed wall 0'] = wall_instance0
            wall_instance1 = Wall()
            wall_instance1.xy = (112, 101)
            wall_instance1.wh = (48, 38)
            objects_map['fixed wall 1'] = wall_instance1
            wall_instance2 = Wall()
            wall_instance2.xy = (8, 101)
            wall_instance2.wh = (40, 38)
            objects_map['fixed wall 2'] = wall_instance2
            number_of_walls = 3
            i = 0
            while (objects_map.get(f"fixed wall {number_of_walls + i}") != None):
                objects_map.pop(f"fixed wall {number_of_walls + i}")
                i += 1

    return objects_map
