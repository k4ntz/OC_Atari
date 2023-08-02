from enum import Enum

from scripts.specialized.hero.detect_walls import Wall, LavaWall
from .game_objects import GameObject

"""
RAM extraction for the game H.E.R.O.
"""

MAX_NB_OBJECTS = {"Wall": 15, "LavaWall": 15, "Enemy": 10, "Player": 1, "LaserBeam": 3, "Bomb": 5, "EndNPC": 1,
                  "Lamp": 1, "Snake": 5, }
MAX_NB_OBJECTS_HUD = {"Wall": 15, "LavaWall": 15, "Enemy": 10, "Player": 1, "LaserBeam": 3, "Bomb": 5, "EndNPC": 1,
                      "Lamp": 1, "Snake": 5, "PowerBar": 1, "BombStock": 1, "Life": 1, "Score": 1}


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
        self.wh = 6, 10
        self.type: EnemyType


class Snake(GameObject):
    """
    The snakes.
    """
    
    def __init__(self, *args, **kwargs):
        self.xy = 0, 0
        self.wh = 8, 10
        super().__init__(*args, **kwargs)


class Player(GameObject):
    """
    The player figure.
    """
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.xy = 0, 0
        self.wh = 5, 25


class LaserBeam(GameObject):
    """
    The laser beams shot from the helmet of the player figure.
    """
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.xy = 0, 0
        self.wh = 7, 2


class Bomb(GameObject):
    """
    The dynamite sticks that can be deployed by the player.
    """
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.xy = 0, 0
        self.wh = 8, 10


class EndNPC(GameObject):
    """
    The trapped miners to be rescued.
    """
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.xy = 0, 0
        self.wh = 8, 10


class Lamp(GameObject):
    """
    The lanterns that light the mineshafts.
    """
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.xy = 0, 0
        self.wh = 8, 10


class PowerBar(GameObject):
    """
    The power gauge (HUD).
    """
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.xy = 0, 0
        self.wh = 8, 10
        self.value = 1


class BombStock(GameObject):
    """
    The indicator for remaining dynamite sticks (HUD).
    """
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.xy = 0, 0
        self.wh = 8, 10
        self.value = 5


class Life(GameObject):
    """
    The indicator for the player's remaining lives (HUD).
    """
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.xy = 0, 0
        self.wh = 8, 10


class Score(GameObject):
    """
    The player's score display (HUD).
    """
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.xy = 0, 0
        self.wh = 8, 10
        self.value = 0


def _get_max_objects(hud=False):
    return


def _init_objects_hero_ram(hud=False):
    objects = [Player()]
    if hud:
        objects.extend([PowerBar(), BombStock(), Life(), Score(), ])
    return objects


number_of_added_enemies = 0
objects_map = {}


def _detect_objects_hero_revised(objects, ram_state, hud=False):
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
            if currobj is not None:
                currobj.xy = x, y
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

    # wall disposition
    # TODO switch case = function of ram_state[28] and which level = ram_state[117] + 1

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
            destructible_wall_instance.wh = 7, 79
            destructible_wall_instance.destructible = True
            objects_map[f"destructible wall"] = destructible_wall_instance

    objects_map = add_walls_to_object_list(ram_state,objects_map)
    # Bomb / NPC position
    # NPC --> ram_state[41]
    # If we're on the final part of the level --> NPC position else bomb position

    if hud:
        objects[1].value = ram_state[43] / 81
        objects[2].value = ram_state[50]
        objects[3].value = ram_state[51]
        objects[4].value = ram_state[56]
    print(ram_state)
    objects[:] = objects[0:base_length] + list(objects_map.values())


def _detect_objects_hero_raw(info, ram_state):
    return


def add_walls_to_object_list(ram_state, objects_map):
    if ram_state[117] == 0:
        if ram_state[28] == 0:
            number_of_lava_walls = 0
            i = 0
            while(objects_map.get(f"fixed wall {number_of_lava_walls + i}")!= None):
                objects_map.pop(f"fixed wall {number_of_lava_walls + i}")
                i += 1
            wall_instance = Wall()
            wall_instance.xy = (136, 21)
            wall_instance.wh = (24, 38)
            objects_map['fixed wall 0'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (8, 21)
            wall_instance.wh = (16, 38)
            objects_map['fixed wall 1'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (144, 61)
            wall_instance.wh = (16, 37)
            objects_map['fixed wall 2'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (8, 61)
            wall_instance.wh = (8, 37)
            objects_map['fixed wall 3'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (88, 101)
            wall_instance.wh = (72, 38)
            objects_map['fixed wall 4'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (8, 101)
            wall_instance.wh = (64, 38)
            objects_map['fixed wall 5'] = wall_instance
            number_of_walls = 6
            i = 0
            while(objects_map.get(f"fixed wall {number_of_walls + i}")!= None):
                objects_map.pop(f"fixed wall {number_of_walls + i}")
                i += 1
        elif ram_state[28] == 1:
            number_of_lava_walls = 0
            i = 0
            while(objects_map.get(f"fixed wall {number_of_lava_walls + i}")!= None):
                objects_map.pop(f"fixed wall {number_of_lava_walls + i}")
                i += 1
            wall_instance = Wall()
            wall_instance.xy = (88, 21)
            wall_instance.wh = (72, 38)
            objects_map['fixed wall 0'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (8, 21)
            wall_instance.wh = (64, 38)
            objects_map['fixed wall 1'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (136, 61)
            wall_instance.wh = (24, 37)
            objects_map['fixed wall 2'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (8, 61)
            wall_instance.wh = (16, 37)
            objects_map['fixed wall 3'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (8, 101)
            wall_instance.wh = (152, 38)
            objects_map['fixed wall 4'] = wall_instance
            number_of_walls = 5
            i = 0
            while(objects_map.get(f"fixed wall {number_of_walls + i}")!= None):
                objects_map.pop(f"fixed wall {number_of_walls + i}")
                i += 1

    elif ram_state[117] == 1:
        if ram_state[28] == 0:
            number_of_lava_walls = 0
            i = 0
            while(objects_map.get(f"fixed wall {number_of_lava_walls + i}")!= None):
                objects_map.pop(f"fixed wall {number_of_lava_walls + i}")
                i += 1
            wall_instance = Wall()
            wall_instance.xy = (136, 21)
            wall_instance.wh = (24, 38)
            objects_map['fixed wall 0'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (8, 21)
            wall_instance.wh = (16, 38)
            objects_map['fixed wall 1'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (144, 61)
            wall_instance.wh = (16, 37)
            objects_map['fixed wall 2'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (8, 61)
            wall_instance.wh = (8, 37)
            objects_map['fixed wall 3'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (88, 101)
            wall_instance.wh = (72, 38)
            objects_map['fixed wall 4'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (8, 101)
            wall_instance.wh = (64, 38)
            objects_map['fixed wall 5'] = wall_instance
            number_of_walls = 6
            i = 0
            while(objects_map.get(f"fixed wall {number_of_walls + i}")!= None):
                objects_map.pop(f"fixed wall {number_of_walls + i}")
                i += 1
        elif ram_state[28] == 1:
            number_of_lava_walls = 0
            i = 0
            while(objects_map.get(f"fixed wall {number_of_lava_walls + i}")!= None):
                objects_map.pop(f"fixed wall {number_of_lava_walls + i}")
                i += 1
            wall_instance = Wall()
            wall_instance.xy = (88, 21)
            wall_instance.wh = (72, 38)
            objects_map['fixed wall 0'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (8, 21)
            wall_instance.wh = (64, 38)
            objects_map['fixed wall 1'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (144, 61)
            wall_instance.wh = (16, 37)
            objects_map['fixed wall 2'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (8, 61)
            wall_instance.wh = (8, 37)
            objects_map['fixed wall 3'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (120, 101)
            wall_instance.wh = (40, 38)
            objects_map['fixed wall 4'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (48, 101)
            wall_instance.wh = (64, 38)
            objects_map['fixed wall 5'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (8, 101)
            wall_instance.wh = (32, 38)
            objects_map['fixed wall 6'] = wall_instance
            number_of_walls = 7
            i = 0
            while(objects_map.get(f"fixed wall {number_of_walls + i}")!= None):
                objects_map.pop(f"fixed wall {number_of_walls + i}")
                i += 1
        elif ram_state[28] == 2:
            number_of_lava_walls = 0
            i = 0
            while(objects_map.get(f"fixed wall {number_of_lava_walls + i}")!= None):
                objects_map.pop(f"fixed wall {number_of_lava_walls + i}")
                i += 1
            wall_instance = Wall()
            wall_instance.xy = (120, 21)
            wall_instance.wh = (40, 38)
            objects_map['fixed wall 0'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (48, 21)
            wall_instance.wh = (64, 38)
            objects_map['fixed wall 1'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (8, 21)
            wall_instance.wh = (32, 38)
            objects_map['fixed wall 2'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (144, 61)
            wall_instance.wh = (16, 37)
            objects_map['fixed wall 3'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (64, 61)
            wall_instance.wh = (44, 37)
            objects_map['fixed wall 4'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (8, 61)
            wall_instance.wh = (20, 37)
            objects_map['fixed wall 5'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (104, 101)
            wall_instance.wh = (56, 38)
            objects_map['fixed wall 6'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (8, 101)
            wall_instance.wh = (48, 38)
            objects_map['fixed wall 7'] = wall_instance
            number_of_walls = 8
            i = 0
            while(objects_map.get(f"fixed wall {number_of_walls + i}")!= None):
                objects_map.pop(f"fixed wall {number_of_walls + i}")
                i += 1
        elif ram_state[28] == 3:
            number_of_lava_walls = 0
            i = 0
            while(objects_map.get(f"fixed wall {number_of_lava_walls + i}")!= None):
                objects_map.pop(f"fixed wall {number_of_lava_walls + i}")
                i += 1
            wall_instance = Wall()
            wall_instance.xy = (8, 21)
            wall_instance.wh = (152, 38)
            objects_map['fixed wall 0'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (88, 101)
            wall_instance.wh = (72, 38)
            objects_map['fixed wall 1'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (8, 101)
            wall_instance.wh = (64, 38)
            objects_map['fixed wall 2'] = wall_instance
            number_of_walls = 3
            i = 0
            while(objects_map.get(f"fixed wall {number_of_walls + i}")!= None):
                objects_map.pop(f"fixed wall {number_of_walls + i}")
                i += 1

    elif ram_state[117] == 2:
        if ram_state[28] == 0:
            number_of_lava_walls = 0
            i = 0
            while(objects_map.get(f"fixed wall {number_of_lava_walls + i}")!= None):
                objects_map.pop(f"fixed wall {number_of_lava_walls + i}")
                i += 1
            wall_instance = Wall()
            wall_instance.xy = (136, 21)
            wall_instance.wh = (24, 38)
            objects_map['fixed wall 0'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (8, 21)
            wall_instance.wh = (16, 38)
            objects_map['fixed wall 1'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (88, 101)
            wall_instance.wh = (72, 38)
            objects_map['fixed wall 2'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (8, 101)
            wall_instance.wh = (64, 38)
            objects_map['fixed wall 3'] = wall_instance
            number_of_walls = 4
            i = 0
            while(objects_map.get(f"fixed wall {number_of_walls + i}")!= None):
                objects_map.pop(f"fixed wall {number_of_walls + i}")
                i += 1
        elif ram_state[28] == 1:
            number_of_lava_walls = 0
            i = 0
            while(objects_map.get(f"fixed wall {number_of_lava_walls + i}")!= None):
                objects_map.pop(f"fixed wall {number_of_lava_walls + i}")
                i += 1
            wall_instance = Wall()
            wall_instance.xy = (88, 21)
            wall_instance.wh = (72, 38)
            objects_map['fixed wall 0'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (8, 21)
            wall_instance.wh = (64, 38)
            objects_map['fixed wall 1'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (136, 101)
            wall_instance.wh = (24, 38)
            objects_map['fixed wall 2'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (8, 101)
            wall_instance.wh = (16, 38)
            objects_map['fixed wall 3'] = wall_instance
            number_of_walls = 4
            i = 0
            while(objects_map.get(f"fixed wall {number_of_walls + i}")!= None):
                objects_map.pop(f"fixed wall {number_of_walls + i}")
                i += 1
        elif ram_state[28] == 2:
            number_of_lava_walls = 0
            i = 0
            while(objects_map.get(f"fixed wall {number_of_lava_walls + i}")!= None):
                objects_map.pop(f"fixed wall {number_of_lava_walls + i}")
                i += 1
            wall_instance = Wall()
            wall_instance.xy = (136, 21)
            wall_instance.wh = (24, 38)
            objects_map['fixed wall 0'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (8, 21)
            wall_instance.wh = (16, 38)
            objects_map['fixed wall 1'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (112, 101)
            wall_instance.wh = (48, 38)
            objects_map['fixed wall 2'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (56, 101)
            wall_instance.wh = (48, 38)
            objects_map['fixed wall 3'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (8, 101)
            wall_instance.wh = (40, 38)
            objects_map['fixed wall 4'] = wall_instance
            number_of_walls = 5
            i = 0
            while(objects_map.get(f"fixed wall {number_of_walls + i}")!= None):
                objects_map.pop(f"fixed wall {number_of_walls + i}")
                i += 1
        elif ram_state[28] == 3:
            number_of_lava_walls = 0
            i = 0
            while(objects_map.get(f"fixed wall {number_of_lava_walls + i}")!= None):
                objects_map.pop(f"fixed wall {number_of_lava_walls + i}")
                i += 1
            wall_instance = Wall()
            wall_instance.xy = (112, 21)
            wall_instance.wh = (48, 38)
            objects_map['fixed wall 0'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (56, 21)
            wall_instance.wh = (48, 38)
            objects_map['fixed wall 1'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (8, 21)
            wall_instance.wh = (40, 38)
            objects_map['fixed wall 2'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (120, 101)
            wall_instance.wh = (40, 38)
            objects_map['fixed wall 3'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (48, 101)
            wall_instance.wh = (64, 38)
            objects_map['fixed wall 4'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (8, 101)
            wall_instance.wh = (32, 38)
            objects_map['fixed wall 5'] = wall_instance
            number_of_walls = 6
            i = 0
            while(objects_map.get(f"fixed wall {number_of_walls + i}")!= None):
                objects_map.pop(f"fixed wall {number_of_walls + i}")
                i += 1
        elif ram_state[28] == 4:
            number_of_lava_walls = 0
            i = 0
            while(objects_map.get(f"fixed wall {number_of_lava_walls + i}")!= None):
                objects_map.pop(f"fixed wall {number_of_lava_walls + i}")
                i += 1
            wall_instance = Wall()
            wall_instance.xy = (120, 21)
            wall_instance.wh = (40, 38)
            objects_map['fixed wall 0'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (48, 21)
            wall_instance.wh = (64, 38)
            objects_map['fixed wall 1'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (8, 21)
            wall_instance.wh = (32, 38)
            objects_map['fixed wall 2'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (88, 101)
            wall_instance.wh = (72, 38)
            objects_map['fixed wall 3'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (8, 101)
            wall_instance.wh = (64, 38)
            objects_map['fixed wall 4'] = wall_instance
            number_of_walls = 5
            i = 0
            while(objects_map.get(f"fixed wall {number_of_walls + i}")!= None):
                objects_map.pop(f"fixed wall {number_of_walls + i}")
                i += 1
        elif ram_state[28] == 5:
            number_of_lava_walls = 0
            i = 0
            while(objects_map.get(f"fixed wall {number_of_lava_walls + i}")!= None):
                objects_map.pop(f"fixed wall {number_of_lava_walls + i}")
                i += 1
            wall_instance = Wall()
            wall_instance.xy = (88, 21)
            wall_instance.wh = (72, 38)
            objects_map['fixed wall 0'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (8, 21)
            wall_instance.wh = (64, 38)
            objects_map['fixed wall 1'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (8, 101)
            wall_instance.wh = (152, 38)
            objects_map['fixed wall 2'] = wall_instance
            number_of_walls = 3
            i = 0
            while(objects_map.get(f"fixed wall {number_of_walls + i}")!= None):
                objects_map.pop(f"fixed wall {number_of_walls + i}")
                i += 1

    elif ram_state[117] == 3:
        if ram_state[28] == 0:
            number_of_lava_walls = 0
            i = 0
            while(objects_map.get(f"fixed wall {number_of_lava_walls + i}")!= None):
                objects_map.pop(f"fixed wall {number_of_lava_walls + i}")
                i += 1
            wall_instance = Wall()
            wall_instance.xy = (136, 21)
            wall_instance.wh = (24, 38)
            objects_map['fixed wall 0'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (8, 21)
            wall_instance.wh = (16, 38)
            objects_map['fixed wall 1'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (88, 101)
            wall_instance.wh = (72, 38)
            objects_map['fixed wall 2'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (8, 101)
            wall_instance.wh = (64, 38)
            objects_map['fixed wall 3'] = wall_instance
            number_of_walls = 4
            i = 0
            while(objects_map.get(f"fixed wall {number_of_walls + i}")!= None):
                objects_map.pop(f"fixed wall {number_of_walls + i}")
                i += 1
        elif ram_state[28] == 1:
            number_of_lava_walls = 0
            i = 0
            while(objects_map.get(f"fixed wall {number_of_lava_walls + i}")!= None):
                objects_map.pop(f"fixed wall {number_of_lava_walls + i}")
                i += 1
            wall_instance = Wall()
            wall_instance.xy = (88, 21)
            wall_instance.wh = (72, 38)
            objects_map['fixed wall 0'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (8, 21)
            wall_instance.wh = (64, 38)
            objects_map['fixed wall 1'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (140, 101)
            wall_instance.wh = (20, 38)
            objects_map['fixed wall 2'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (28, 101)
            wall_instance.wh = (104, 38)
            objects_map['fixed wall 3'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (8, 101)
            wall_instance.wh = (12, 38)
            objects_map['fixed wall 4'] = wall_instance
            number_of_walls = 5
            i = 0
            while(objects_map.get(f"fixed wall {number_of_walls + i}")!= None):
                objects_map.pop(f"fixed wall {number_of_walls + i}")
                i += 1
        elif ram_state[28] == 2:
            number_of_lava_walls = 0
            i = 0
            while(objects_map.get(f"fixed wall {number_of_lava_walls + i}")!= None):
                objects_map.pop(f"fixed wall {number_of_lava_walls + i}")
                i += 1
            wall_instance = Wall()
            wall_instance.xy = (140, 21)
            wall_instance.wh = (20, 38)
            objects_map['fixed wall 0'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (28, 21)
            wall_instance.wh = (104, 38)
            objects_map['fixed wall 1'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (8, 21)
            wall_instance.wh = (12, 38)
            objects_map['fixed wall 2'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (128, 101)
            wall_instance.wh = (32, 38)
            objects_map['fixed wall 3'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (44, 101)
            wall_instance.wh = (72, 38)
            objects_map['fixed wall 4'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (8, 101)
            wall_instance.wh = (24, 38)
            objects_map['fixed wall 5'] = wall_instance
            number_of_walls = 6
            i = 0
            while(objects_map.get(f"fixed wall {number_of_walls + i}")!= None):
                objects_map.pop(f"fixed wall {number_of_walls + i}")
                i += 1
        elif ram_state[28] == 3:
            number_of_lava_walls = 0
            i = 0
            while(objects_map.get(f"fixed wall {number_of_lava_walls + i}")!= None):
                objects_map.pop(f"fixed wall {number_of_lava_walls + i}")
                i += 1
            wall_instance = Wall()
            wall_instance.xy = (128, 21)
            wall_instance.wh = (32, 38)
            objects_map['fixed wall 0'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (44, 21)
            wall_instance.wh = (72, 38)
            objects_map['fixed wall 1'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (8, 21)
            wall_instance.wh = (24, 38)
            objects_map['fixed wall 2'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (144, 101)
            wall_instance.wh = (16, 38)
            objects_map['fixed wall 3'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (32, 101)
            wall_instance.wh = (96, 38)
            objects_map['fixed wall 4'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (8, 101)
            wall_instance.wh = (8, 38)
            objects_map['fixed wall 5'] = wall_instance
            number_of_walls = 6
            i = 0
            while(objects_map.get(f"fixed wall {number_of_walls + i}")!= None):
                objects_map.pop(f"fixed wall {number_of_walls + i}")
                i += 1
        elif ram_state[28] == 4:
            number_of_lava_walls = 0
            i = 0
            while(objects_map.get(f"fixed wall {number_of_lava_walls + i}")!= None):
                objects_map.pop(f"fixed wall {number_of_lava_walls + i}")
                i += 1
            wall_instance = Wall()
            wall_instance.xy = (144, 21)
            wall_instance.wh = (16, 38)
            objects_map['fixed wall 0'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (32, 21)
            wall_instance.wh = (96, 38)
            objects_map['fixed wall 1'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (8, 21)
            wall_instance.wh = (8, 38)
            objects_map['fixed wall 2'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (88, 101)
            wall_instance.wh = (72, 38)
            objects_map['fixed wall 3'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (8, 101)
            wall_instance.wh = (64, 38)
            objects_map['fixed wall 4'] = wall_instance
            number_of_walls = 5
            i = 0
            while(objects_map.get(f"fixed wall {number_of_walls + i}")!= None):
                objects_map.pop(f"fixed wall {number_of_walls + i}")
                i += 1
        elif ram_state[28] == 5:
            number_of_lava_walls = 0
            i = 0
            while(objects_map.get(f"fixed wall {number_of_lava_walls + i}")!= None):
                objects_map.pop(f"fixed wall {number_of_lava_walls + i}")
                i += 1
            wall_instance = Wall()
            wall_instance.xy = (88, 21)
            wall_instance.wh = (72, 38)
            objects_map['fixed wall 0'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (8, 21)
            wall_instance.wh = (64, 38)
            objects_map['fixed wall 1'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (140, 101)
            wall_instance.wh = (20, 38)
            objects_map['fixed wall 2'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (28, 101)
            wall_instance.wh = (104, 38)
            objects_map['fixed wall 3'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (8, 101)
            wall_instance.wh = (12, 38)
            objects_map['fixed wall 4'] = wall_instance
            number_of_walls = 5
            i = 0
            while(objects_map.get(f"fixed wall {number_of_walls + i}")!= None):
                objects_map.pop(f"fixed wall {number_of_walls + i}")
                i += 1
        elif ram_state[28] == 6:
            number_of_lava_walls = 0
            i = 0
            while(objects_map.get(f"fixed wall {number_of_lava_walls + i}")!= None):
                objects_map.pop(f"fixed wall {number_of_lava_walls + i}")
                i += 1
            wall_instance = Wall()
            wall_instance.xy = (140, 21)
            wall_instance.wh = (20, 38)
            objects_map['fixed wall 0'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (28, 21)
            wall_instance.wh = (104, 38)
            objects_map['fixed wall 1'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (8, 21)
            wall_instance.wh = (12, 38)
            objects_map['fixed wall 2'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (100, 101)
            wall_instance.wh = (60, 38)
            objects_map['fixed wall 3'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (8, 101)
            wall_instance.wh = (52, 38)
            objects_map['fixed wall 4'] = wall_instance
            number_of_walls = 5
            i = 0
            while(objects_map.get(f"fixed wall {number_of_walls + i}")!= None):
                objects_map.pop(f"fixed wall {number_of_walls + i}")
                i += 1
        elif ram_state[28] == 7:
            number_of_lava_walls = 0
            i = 0
            while(objects_map.get(f"fixed wall {number_of_lava_walls + i}")!= None):
                objects_map.pop(f"fixed wall {number_of_lava_walls + i}")
                i += 1
            wall_instance = Wall()
            wall_instance.xy = (100, 21)
            wall_instance.wh = (60, 38)
            objects_map['fixed wall 0'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (8, 21)
            wall_instance.wh = (52, 38)
            objects_map['fixed wall 1'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (8, 101)
            wall_instance.wh = (152, 38)
            objects_map['fixed wall 2'] = wall_instance
            number_of_walls = 3
            i = 0
            while(objects_map.get(f"fixed wall {number_of_walls + i}")!= None):
                objects_map.pop(f"fixed wall {number_of_walls + i}")
                i += 1

    elif ram_state[117] == 4:
        if ram_state[28] == 0:
            number_of_lava_walls = 0
            i = 0
            while(objects_map.get(f"fixed wall {number_of_lava_walls + i}")!= None):
                objects_map.pop(f"fixed wall {number_of_lava_walls + i}")
                i += 1
            wall_instance = Wall()
            wall_instance.xy = (136, 21)
            wall_instance.wh = (24, 38)
            objects_map['fixed wall 0'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (8, 21)
            wall_instance.wh = (16, 38)
            objects_map['fixed wall 1'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (88, 101)
            wall_instance.wh = (72, 38)
            objects_map['fixed wall 2'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (8, 101)
            wall_instance.wh = (64, 38)
            objects_map['fixed wall 3'] = wall_instance
            number_of_walls = 4
            i = 0
            while(objects_map.get(f"fixed wall {number_of_walls + i}")!= None):
                objects_map.pop(f"fixed wall {number_of_walls + i}")
                i += 1
        elif ram_state[28] == 1:
            wall_instance = LavaWall()
            wall_instance.xy = (144, 61)
            wall_instance.wh = (16, 37)
            objects_map['lava wall 0'] = wall_instance
            wall_instance = LavaWall()
            wall_instance.xy = (8, 61)
            wall_instance.wh = (8, 37)
            objects_map['lava wall 1'] = wall_instance
            number_of_lava_walls = 2
            i = 0
            while(objects_map.get(f"fixed wall {number_of_lava_walls + i}")!= None):
                objects_map.pop(f"fixed wall {number_of_lava_walls + i}")
                i += 1
            wall_instance = Wall()
            wall_instance.xy = (88, 21)
            wall_instance.wh = (72, 38)
            objects_map['fixed wall 0'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (8, 21)
            wall_instance.wh = (64, 38)
            objects_map['fixed wall 1'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (8, 101)
            wall_instance.wh = (152, 38)
            objects_map['fixed wall 2'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (144, 61)
            wall_instance.wh = (16, 37)
            objects_map['fixed wall 3'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (8, 61)
            wall_instance.wh = (8, 37)
            objects_map['fixed wall 4'] = wall_instance
            number_of_walls = 5
            i = 0
            while(objects_map.get(f"fixed wall {number_of_walls + i}")!= None):
                objects_map.pop(f"fixed wall {number_of_walls + i}")
                i += 1
        elif ram_state[28] == 2:
            number_of_lava_walls = 0
            i = 0
            while(objects_map.get(f"fixed wall {number_of_lava_walls + i}")!= None):
                objects_map.pop(f"fixed wall {number_of_lava_walls + i}")
                i += 1
            wall_instance = Wall()
            wall_instance.xy = (8, 21)
            wall_instance.wh = (152, 38)
            objects_map['fixed wall 0'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (136, 101)
            wall_instance.wh = (24, 38)
            objects_map['fixed wall 1'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (8, 101)
            wall_instance.wh = (16, 38)
            objects_map['fixed wall 2'] = wall_instance
            number_of_walls = 3
            i = 0
            while(objects_map.get(f"fixed wall {number_of_walls + i}")!= None):
                objects_map.pop(f"fixed wall {number_of_walls + i}")
                i += 1
        elif ram_state[28] == 3:
            wall_instance = LavaWall()
            wall_instance.xy = (112, 61)
            wall_instance.wh = (48, 37)
            objects_map['lava wall 0'] = wall_instance
            wall_instance = LavaWall()
            wall_instance.xy = (8, 61)
            wall_instance.wh = (40, 37)
            objects_map['lava wall 1'] = wall_instance
            number_of_lava_walls = 2
            i = 0
            while(objects_map.get(f"fixed wall {number_of_lava_walls + i}")!= None):
                objects_map.pop(f"fixed wall {number_of_lava_walls + i}")
                i += 1
            wall_instance = Wall()
            wall_instance.xy = (136, 21)
            wall_instance.wh = (24, 38)
            objects_map['fixed wall 0'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (8, 21)
            wall_instance.wh = (16, 38)
            objects_map['fixed wall 1'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (84, 101)
            wall_instance.wh = (76, 38)
            objects_map['fixed wall 2'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (8, 101)
            wall_instance.wh = (68, 38)
            objects_map['fixed wall 3'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (112, 61)
            wall_instance.wh = (48, 37)
            objects_map['fixed wall 4'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (8, 61)
            wall_instance.wh = (40, 37)
            objects_map['fixed wall 5'] = wall_instance
            number_of_walls = 6
            i = 0
            while(objects_map.get(f"fixed wall {number_of_walls + i}")!= None):
                objects_map.pop(f"fixed wall {number_of_walls + i}")
                i += 1
        elif ram_state[28] == 4:
            number_of_lava_walls = 0
            i = 0
            while(objects_map.get(f"fixed wall {number_of_lava_walls + i}")!= None):
                objects_map.pop(f"fixed wall {number_of_lava_walls + i}")
                i += 1
            wall_instance = Wall()
            wall_instance.xy = (84, 21)
            wall_instance.wh = (76, 38)
            objects_map['fixed wall 0'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (8, 21)
            wall_instance.wh = (68, 38)
            objects_map['fixed wall 1'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (136, 101)
            wall_instance.wh = (24, 38)
            objects_map['fixed wall 2'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (32, 101)
            wall_instance.wh = (96, 38)
            objects_map['fixed wall 3'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (8, 101)
            wall_instance.wh = (16, 38)
            objects_map['fixed wall 4'] = wall_instance
            number_of_walls = 5
            i = 0
            while(objects_map.get(f"fixed wall {number_of_walls + i}")!= None):
                objects_map.pop(f"fixed wall {number_of_walls + i}")
                i += 1
        elif ram_state[28] == 5:
            wall_instance = LavaWall()
            wall_instance.xy = (144, 61)
            wall_instance.wh = (16, 37)
            objects_map['lava wall 0'] = wall_instance
            wall_instance = LavaWall()
            wall_instance.xy = (8, 61)
            wall_instance.wh = (8, 37)
            objects_map['lava wall 1'] = wall_instance
            number_of_lava_walls = 2
            i = 0
            while(objects_map.get(f"fixed wall {number_of_lava_walls + i}")!= None):
                objects_map.pop(f"fixed wall {number_of_lava_walls + i}")
                i += 1
            wall_instance = Wall()
            wall_instance.xy = (136, 21)
            wall_instance.wh = (24, 38)
            objects_map['fixed wall 0'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (32, 21)
            wall_instance.wh = (96, 38)
            objects_map['fixed wall 1'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (8, 21)
            wall_instance.wh = (16, 38)
            objects_map['fixed wall 2'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (88, 101)
            wall_instance.wh = (72, 38)
            objects_map['fixed wall 3'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (8, 101)
            wall_instance.wh = (64, 38)
            objects_map['fixed wall 4'] = wall_instance
            number_of_walls = 5
            i = 0
            while(objects_map.get(f"fixed wall {number_of_walls + i}")!= None):
                objects_map.pop(f"fixed wall {number_of_walls + i}")
                i += 1
        elif ram_state[28] == 6:
            wall_instance = LavaWall()
            wall_instance.xy = (144, 61)
            wall_instance.wh = (16, 37)
            objects_map['lava wall 0'] = wall_instance
            wall_instance = LavaWall()
            wall_instance.xy = (8, 61)
            wall_instance.wh = (8, 37)
            objects_map['lava wall 1'] = wall_instance
            number_of_lava_walls = 2
            i = 0
            while(objects_map.get(f"fixed wall {number_of_lava_walls + i}")!= None):
                objects_map.pop(f"fixed wall {number_of_lava_walls + i}")
                i += 1
            wall_instance = Wall()
            wall_instance.xy = (88, 21)
            wall_instance.wh = (72, 38)
            objects_map['fixed wall 0'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (8, 21)
            wall_instance.wh = (64, 38)
            objects_map['fixed wall 1'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (120, 101)
            wall_instance.wh = (40, 38)
            objects_map['fixed wall 2'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (48, 101)
            wall_instance.wh = (64, 38)
            objects_map['fixed wall 3'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (8, 101)
            wall_instance.wh = (32, 38)
            objects_map['fixed wall 4'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (144, 61)
            wall_instance.wh = (16, 37)
            objects_map['fixed wall 5'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (8, 61)
            wall_instance.wh = (8, 37)
            objects_map['fixed wall 6'] = wall_instance
            number_of_walls = 7
            i = 0
            while(objects_map.get(f"fixed wall {number_of_walls + i}")!= None):
                objects_map.pop(f"fixed wall {number_of_walls + i}")
                i += 1
        elif ram_state[28] == 7:
            number_of_lava_walls = 0
            i = 0
            while(objects_map.get(f"fixed wall {number_of_lava_walls + i}")!= None):
                objects_map.pop(f"fixed wall {number_of_lava_walls + i}")
                i += 1
            wall_instance = Wall()
            wall_instance.xy = (120, 21)
            wall_instance.wh = (40, 38)
            objects_map['fixed wall 0'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (48, 21)
            wall_instance.wh = (64, 38)
            objects_map['fixed wall 1'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (8, 21)
            wall_instance.wh = (32, 38)
            objects_map['fixed wall 2'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (8, 101)
            wall_instance.wh = (152, 38)
            objects_map['fixed wall 3'] = wall_instance
            number_of_walls = 4
            i = 0
            while(objects_map.get(f"fixed wall {number_of_walls + i}")!= None):
                objects_map.pop(f"fixed wall {number_of_walls + i}")
                i += 1

    elif ram_state[117] == 5:
        if ram_state[28] == 0:
            wall_instance = LavaWall()
            wall_instance.xy = (144, 61)
            wall_instance.wh = (16, 37)
            objects_map['lava wall 0'] = wall_instance
            wall_instance = LavaWall()
            wall_instance.xy = (8, 61)
            wall_instance.wh = (8, 37)
            objects_map['lava wall 1'] = wall_instance
            number_of_lava_walls = 2
            i = 0
            while(objects_map.get(f"fixed wall {number_of_lava_walls + i}")!= None):
                objects_map.pop(f"fixed wall {number_of_lava_walls + i}")
                i += 1
            wall_instance = Wall()
            wall_instance.xy = (136, 21)
            wall_instance.wh = (24, 38)
            objects_map['fixed wall 0'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (8, 21)
            wall_instance.wh = (16, 38)
            objects_map['fixed wall 1'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (88, 101)
            wall_instance.wh = (72, 38)
            objects_map['fixed wall 2'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (8, 101)
            wall_instance.wh = (64, 38)
            objects_map['fixed wall 3'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (144, 61)
            wall_instance.wh = (16, 37)
            objects_map['fixed wall 4'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (8, 61)
            wall_instance.wh = (8, 37)
            objects_map['fixed wall 5'] = wall_instance
            number_of_walls = 6
            i = 0
            while(objects_map.get(f"fixed wall {number_of_walls + i}")!= None):
                objects_map.pop(f"fixed wall {number_of_walls + i}")
                i += 1
        elif ram_state[28] == 1:
            number_of_lava_walls = 0
            i = 0
            while(objects_map.get(f"fixed wall {number_of_lava_walls + i}")!= None):
                objects_map.pop(f"fixed wall {number_of_lava_walls + i}")
                i += 1
            wall_instance = Wall()
            wall_instance.xy = (88, 21)
            wall_instance.wh = (72, 38)
            objects_map['fixed wall 0'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (8, 21)
            wall_instance.wh = (64, 38)
            objects_map['fixed wall 1'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (140, 101)
            wall_instance.wh = (20, 38)
            objects_map['fixed wall 2'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (56, 101)
            wall_instance.wh = (48, 38)
            objects_map['fixed wall 3'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (8, 101)
            wall_instance.wh = (12, 38)
            objects_map['fixed wall 4'] = wall_instance
            number_of_walls = 5
            i = 0
            while(objects_map.get(f"fixed wall {number_of_walls + i}")!= None):
                objects_map.pop(f"fixed wall {number_of_walls + i}")
                i += 1
        elif ram_state[28] == 2:
            wall_instance = LavaWall()
            wall_instance.xy = (144, 61)
            wall_instance.wh = (16, 37)
            objects_map['lava wall 0'] = wall_instance
            wall_instance = LavaWall()
            wall_instance.xy = (8, 61)
            wall_instance.wh = (8, 37)
            objects_map['lava wall 1'] = wall_instance
            number_of_lava_walls = 2
            i = 0
            while(objects_map.get(f"fixed wall {number_of_lava_walls + i}")!= None):
                objects_map.pop(f"fixed wall {number_of_lava_walls + i}")
                i += 1
            wall_instance = Wall()
            wall_instance.xy = (140, 21)
            wall_instance.wh = (20, 38)
            objects_map['fixed wall 0'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (56, 21)
            wall_instance.wh = (48, 38)
            objects_map['fixed wall 1'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (8, 21)
            wall_instance.wh = (12, 38)
            objects_map['fixed wall 2'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (88, 101)
            wall_instance.wh = (72, 38)
            objects_map['fixed wall 3'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (8, 101)
            wall_instance.wh = (64, 38)
            objects_map['fixed wall 4'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (144, 61)
            wall_instance.wh = (16, 37)
            objects_map['fixed wall 5'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (8, 61)
            wall_instance.wh = (8, 37)
            objects_map['fixed wall 6'] = wall_instance
            number_of_walls = 7
            i = 0
            while(objects_map.get(f"fixed wall {number_of_walls + i}")!= None):
                objects_map.pop(f"fixed wall {number_of_walls + i}")
                i += 1
        elif ram_state[28] == 3:
            number_of_lava_walls = 0
            i = 0
            while(objects_map.get(f"fixed wall {number_of_lava_walls + i}")!= None):
                objects_map.pop(f"fixed wall {number_of_lava_walls + i}")
                i += 1
            wall_instance = Wall()
            wall_instance.xy = (88, 21)
            wall_instance.wh = (72, 38)
            objects_map['fixed wall 0'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (8, 21)
            wall_instance.wh = (64, 38)
            objects_map['fixed wall 1'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (132, 101)
            wall_instance.wh = (28, 38)
            objects_map['fixed wall 2'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (104, 101)
            wall_instance.wh = (20, 38)
            objects_map['fixed wall 3'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (64, 101)
            wall_instance.wh = (32, 38)
            objects_map['fixed wall 4'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (36, 101)
            wall_instance.wh = (20, 38)
            objects_map['fixed wall 5'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (8, 101)
            wall_instance.wh = (20, 38)
            objects_map['fixed wall 6'] = wall_instance
            number_of_walls = 7
            i = 0
            while(objects_map.get(f"fixed wall {number_of_walls + i}")!= None):
                objects_map.pop(f"fixed wall {number_of_walls + i}")
                i += 1
        elif ram_state[28] == 4:
            wall_instance = LavaWall()
            wall_instance.xy = (112, 61)
            wall_instance.wh = (48, 37)
            objects_map['lava wall 0'] = wall_instance
            wall_instance = LavaWall()
            wall_instance.xy = (8, 61)
            wall_instance.wh = (40, 37)
            objects_map['lava wall 1'] = wall_instance
            number_of_lava_walls = 2
            i = 0
            while(objects_map.get(f"fixed wall {number_of_lava_walls + i}")!= None):
                objects_map.pop(f"fixed wall {number_of_lava_walls + i}")
                i += 1
            wall_instance = Wall()
            wall_instance.xy = (132, 21)
            wall_instance.wh = (28, 38)
            objects_map['fixed wall 0'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (104, 21)
            wall_instance.wh = (20, 38)
            objects_map['fixed wall 1'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (64, 21)
            wall_instance.wh = (32, 38)
            objects_map['fixed wall 2'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (36, 21)
            wall_instance.wh = (20, 38)
            objects_map['fixed wall 3'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (8, 21)
            wall_instance.wh = (20, 38)
            objects_map['fixed wall 4'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (108, 101)
            wall_instance.wh = (52, 38)
            objects_map['fixed wall 5'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (60, 101)
            wall_instance.wh = (40, 38)
            objects_map['fixed wall 6'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (8, 101)
            wall_instance.wh = (44, 38)
            objects_map['fixed wall 7'] = wall_instance
            number_of_walls = 8
            i = 0
            while(objects_map.get(f"fixed wall {number_of_walls + i}")!= None):
                objects_map.pop(f"fixed wall {number_of_walls + i}")
                i += 1
        elif ram_state[28] == 5:
            number_of_lava_walls = 0
            i = 0
            while(objects_map.get(f"fixed wall {number_of_lava_walls + i}")!= None):
                objects_map.pop(f"fixed wall {number_of_lava_walls + i}")
                i += 1
            wall_instance = Wall()
            wall_instance.xy = (108, 21)
            wall_instance.wh = (52, 38)
            objects_map['fixed wall 0'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (60, 21)
            wall_instance.wh = (40, 38)
            objects_map['fixed wall 1'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (8, 21)
            wall_instance.wh = (44, 38)
            objects_map['fixed wall 2'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (120, 101)
            wall_instance.wh = (40, 38)
            objects_map['fixed wall 3'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (8, 101)
            wall_instance.wh = (32, 38)
            objects_map['fixed wall 4'] = wall_instance
            number_of_walls = 5
            i = 0
            while(objects_map.get(f"fixed wall {number_of_walls + i}")!= None):
                objects_map.pop(f"fixed wall {number_of_walls + i}")
                i += 1
        elif ram_state[28] == 6:
            wall_instance = LavaWall()
            wall_instance.xy = (144, 61)
            wall_instance.wh = (16, 37)
            objects_map['lava wall 0'] = wall_instance
            wall_instance = LavaWall()
            wall_instance.xy = (8, 61)
            wall_instance.wh = (8, 37)
            objects_map['lava wall 1'] = wall_instance
            number_of_lava_walls = 2
            i = 0
            while(objects_map.get(f"fixed wall {number_of_lava_walls + i}")!= None):
                objects_map.pop(f"fixed wall {number_of_lava_walls + i}")
                i += 1
            wall_instance = Wall()
            wall_instance.xy = (120, 21)
            wall_instance.wh = (40, 38)
            objects_map['fixed wall 0'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (8, 21)
            wall_instance.wh = (32, 38)
            objects_map['fixed wall 1'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (136, 101)
            wall_instance.wh = (24, 38)
            objects_map['fixed wall 2'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (32, 101)
            wall_instance.wh = (96, 38)
            objects_map['fixed wall 3'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (8, 101)
            wall_instance.wh = (16, 38)
            objects_map['fixed wall 4'] = wall_instance
            number_of_walls = 5
            i = 0
            while(objects_map.get(f"fixed wall {number_of_walls + i}")!= None):
                objects_map.pop(f"fixed wall {number_of_walls + i}")
                i += 1
        elif ram_state[28] == 7:
            number_of_lava_walls = 0
            i = 0
            while(objects_map.get(f"fixed wall {number_of_lava_walls + i}")!= None):
                objects_map.pop(f"fixed wall {number_of_lava_walls + i}")
                i += 1
            wall_instance = Wall()
            wall_instance.xy = (136, 21)
            wall_instance.wh = (24, 38)
            objects_map['fixed wall 0'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (32, 21)
            wall_instance.wh = (96, 38)
            objects_map['fixed wall 1'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (8, 21)
            wall_instance.wh = (16, 38)
            objects_map['fixed wall 2'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (112, 101)
            wall_instance.wh = (48, 38)
            objects_map['fixed wall 3'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (56, 101)
            wall_instance.wh = (48, 38)
            objects_map['fixed wall 4'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (8, 101)
            wall_instance.wh = (40, 38)
            objects_map['fixed wall 5'] = wall_instance
            number_of_walls = 6
            i = 0
            while(objects_map.get(f"fixed wall {number_of_walls + i}")!= None):
                objects_map.pop(f"fixed wall {number_of_walls + i}")
                i += 1
        elif ram_state[28] == 8:
            wall_instance = LavaWall()
            wall_instance.xy = (136, 61)
            wall_instance.wh = (24, 37)
            objects_map['lava wall 0'] = wall_instance
            wall_instance = LavaWall()
            wall_instance.xy = (8, 61)
            wall_instance.wh = (16, 37)
            objects_map['lava wall 1'] = wall_instance
            number_of_lava_walls = 2
            i = 0
            while(objects_map.get(f"fixed wall {number_of_lava_walls + i}")!= None):
                objects_map.pop(f"fixed wall {number_of_lava_walls + i}")
                i += 1
            wall_instance = Wall()
            wall_instance.xy = (112, 21)
            wall_instance.wh = (48, 38)
            objects_map['fixed wall 0'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (56, 21)
            wall_instance.wh = (48, 38)
            objects_map['fixed wall 1'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (8, 21)
            wall_instance.wh = (40, 38)
            objects_map['fixed wall 2'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (88, 101)
            wall_instance.wh = (72, 38)
            objects_map['fixed wall 3'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (8, 101)
            wall_instance.wh = (64, 38)
            objects_map['fixed wall 4'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (136, 61)
            wall_instance.wh = (24, 37)
            objects_map['fixed wall 5'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (8, 61)
            wall_instance.wh = (16, 37)
            objects_map['fixed wall 6'] = wall_instance
            number_of_walls = 7
            i = 0
            while(objects_map.get(f"fixed wall {number_of_walls + i}")!= None):
                objects_map.pop(f"fixed wall {number_of_walls + i}")
                i += 1
        elif ram_state[28] == 9:
            number_of_lava_walls = 0
            i = 0
            while(objects_map.get(f"fixed wall {number_of_lava_walls + i}")!= None):
                objects_map.pop(f"fixed wall {number_of_lava_walls + i}")
                i += 1
            wall_instance = Wall()
            wall_instance.xy = (88, 21)
            wall_instance.wh = (72, 38)
            objects_map['fixed wall 0'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (8, 21)
            wall_instance.wh = (64, 38)
            objects_map['fixed wall 1'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (8, 101)
            wall_instance.wh = (152, 38)
            objects_map['fixed wall 2'] = wall_instance
            number_of_walls = 3
            i = 0
            while(objects_map.get(f"fixed wall {number_of_walls + i}")!= None):
                objects_map.pop(f"fixed wall {number_of_walls + i}")
                i += 1

    elif ram_state[117] == 6:
        if ram_state[28] == 0:
            wall_instance = LavaWall()
            wall_instance.xy = (140, 61)
            wall_instance.wh = (20, 37)
            objects_map['lava wall 0'] = wall_instance
            wall_instance = LavaWall()
            wall_instance.xy = (8, 61)
            wall_instance.wh = (12, 37)
            objects_map['lava wall 1'] = wall_instance
            number_of_lava_walls = 2
            i = 0
            while(objects_map.get(f"fixed wall {number_of_lava_walls + i}")!= None):
                objects_map.pop(f"fixed wall {number_of_lava_walls + i}")
                i += 1
            wall_instance = Wall()
            wall_instance.xy = (136, 21)
            wall_instance.wh = (24, 38)
            objects_map['fixed wall 0'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (8, 21)
            wall_instance.wh = (16, 38)
            objects_map['fixed wall 1'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (88, 101)
            wall_instance.wh = (72, 38)
            objects_map['fixed wall 2'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (8, 101)
            wall_instance.wh = (64, 38)
            objects_map['fixed wall 3'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (140, 61)
            wall_instance.wh = (20, 37)
            objects_map['fixed wall 4'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (8, 61)
            wall_instance.wh = (12, 37)
            objects_map['fixed wall 5'] = wall_instance
            number_of_walls = 6
            i = 0
            while(objects_map.get(f"fixed wall {number_of_walls + i}")!= None):
                objects_map.pop(f"fixed wall {number_of_walls + i}")
                i += 1
        elif ram_state[28] == 1:
            number_of_lava_walls = 0
            i = 0
            while(objects_map.get(f"fixed wall {number_of_lava_walls + i}")!= None):
                objects_map.pop(f"fixed wall {number_of_lava_walls + i}")
                i += 1
            wall_instance = Wall()
            wall_instance.xy = (88, 21)
            wall_instance.wh = (72, 38)
            objects_map['fixed wall 0'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (8, 21)
            wall_instance.wh = (64, 38)
            objects_map['fixed wall 1'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (136, 101)
            wall_instance.wh = (24, 38)
            objects_map['fixed wall 2'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (32, 101)
            wall_instance.wh = (96, 38)
            objects_map['fixed wall 3'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (8, 101)
            wall_instance.wh = (16, 38)
            objects_map['fixed wall 4'] = wall_instance
            number_of_walls = 5
            i = 0
            while(objects_map.get(f"fixed wall {number_of_walls + i}")!= None):
                objects_map.pop(f"fixed wall {number_of_walls + i}")
                i += 1
        elif ram_state[28] == 2:
            wall_instance = LavaWall()
            wall_instance.xy = (144, 61)
            wall_instance.wh = (16, 37)
            objects_map['lava wall 0'] = wall_instance
            wall_instance = LavaWall()
            wall_instance.xy = (8, 61)
            wall_instance.wh = (8, 37)
            objects_map['lava wall 1'] = wall_instance
            number_of_lava_walls = 2
            i = 0
            while(objects_map.get(f"fixed wall {number_of_lava_walls + i}")!= None):
                objects_map.pop(f"fixed wall {number_of_lava_walls + i}")
                i += 1
            wall_instance = Wall()
            wall_instance.xy = (136, 21)
            wall_instance.wh = (24, 38)
            objects_map['fixed wall 0'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (32, 21)
            wall_instance.wh = (96, 38)
            objects_map['fixed wall 1'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (8, 21)
            wall_instance.wh = (16, 38)
            objects_map['fixed wall 2'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (84, 101)
            wall_instance.wh = (76, 38)
            objects_map['fixed wall 3'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (8, 101)
            wall_instance.wh = (68, 38)
            objects_map['fixed wall 4'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (144, 61)
            wall_instance.wh = (16, 37)
            objects_map['fixed wall 5'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (8, 61)
            wall_instance.wh = (8, 37)
            objects_map['fixed wall 6'] = wall_instance
            number_of_walls = 7
            i = 0
            while(objects_map.get(f"fixed wall {number_of_walls + i}")!= None):
                objects_map.pop(f"fixed wall {number_of_walls + i}")
                i += 1
        elif ram_state[28] == 3:
            number_of_lava_walls = 0
            i = 0
            while(objects_map.get(f"fixed wall {number_of_lava_walls + i}")!= None):
                objects_map.pop(f"fixed wall {number_of_lava_walls + i}")
                i += 1
            wall_instance = Wall()
            wall_instance.xy = (84, 21)
            wall_instance.wh = (76, 38)
            objects_map['fixed wall 0'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (8, 21)
            wall_instance.wh = (68, 38)
            objects_map['fixed wall 1'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (108, 101)
            wall_instance.wh = (52, 38)
            objects_map['fixed wall 2'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (60, 101)
            wall_instance.wh = (40, 38)
            objects_map['fixed wall 3'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (8, 101)
            wall_instance.wh = (44, 38)
            objects_map['fixed wall 4'] = wall_instance
            number_of_walls = 5
            i = 0
            while(objects_map.get(f"fixed wall {number_of_walls + i}")!= None):
                objects_map.pop(f"fixed wall {number_of_walls + i}")
                i += 1
        elif ram_state[28] == 4:
            wall_instance = LavaWall()
            wall_instance.xy = (144, 61)
            wall_instance.wh = (16, 37)
            objects_map['lava wall 0'] = wall_instance
            wall_instance = LavaWall()
            wall_instance.xy = (64, 61)
            wall_instance.wh = (48, 37)
            objects_map['lava wall 1'] = wall_instance
            wall_instance = LavaWall()
            wall_instance.xy = (8, 61)
            wall_instance.wh = (24, 37)
            objects_map['lava wall 2'] = wall_instance
            number_of_lava_walls = 3
            i = 0
            while(objects_map.get(f"fixed wall {number_of_lava_walls + i}")!= None):
                objects_map.pop(f"fixed wall {number_of_lava_walls + i}")
                i += 1
            wall_instance = Wall()
            wall_instance.xy = (108, 21)
            wall_instance.wh = (52, 38)
            objects_map['fixed wall 0'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (60, 21)
            wall_instance.wh = (40, 38)
            objects_map['fixed wall 1'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (8, 21)
            wall_instance.wh = (44, 38)
            objects_map['fixed wall 2'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (136, 101)
            wall_instance.wh = (24, 38)
            objects_map['fixed wall 3'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (40, 101)
            wall_instance.wh = (80, 38)
            objects_map['fixed wall 4'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (8, 101)
            wall_instance.wh = (16, 38)
            objects_map['fixed wall 5'] = wall_instance
            number_of_walls = 6
            i = 0
            while(objects_map.get(f"fixed wall {number_of_walls + i}")!= None):
                objects_map.pop(f"fixed wall {number_of_walls + i}")
                i += 1
        elif ram_state[28] == 5:
            number_of_lava_walls = 0
            i = 0
            while(objects_map.get(f"fixed wall {number_of_lava_walls + i}")!= None):
                objects_map.pop(f"fixed wall {number_of_lava_walls + i}")
                i += 1
            wall_instance = Wall()
            wall_instance.xy = (136, 21)
            wall_instance.wh = (24, 38)
            objects_map['fixed wall 0'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (40, 21)
            wall_instance.wh = (80, 38)
            objects_map['fixed wall 1'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (8, 21)
            wall_instance.wh = (16, 38)
            objects_map['fixed wall 2'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (144, 101)
            wall_instance.wh = (16, 38)
            objects_map['fixed wall 3'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (48, 101)
            wall_instance.wh = (64, 38)
            objects_map['fixed wall 4'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (8, 101)
            wall_instance.wh = (8, 38)
            objects_map['fixed wall 5'] = wall_instance
            number_of_walls = 6
            i = 0
            while(objects_map.get(f"fixed wall {number_of_walls + i}")!= None):
                objects_map.pop(f"fixed wall {number_of_walls + i}")
                i += 1
        elif ram_state[28] == 6:
            wall_instance = LavaWall()
            wall_instance.xy = (136, 61)
            wall_instance.wh = (24, 37)
            objects_map['lava wall 0'] = wall_instance
            wall_instance = LavaWall()
            wall_instance.xy = (56, 61)
            wall_instance.wh = (64, 37)
            objects_map['lava wall 1'] = wall_instance
            wall_instance = LavaWall()
            wall_instance.xy = (8, 61)
            wall_instance.wh = (32, 37)
            objects_map['lava wall 2'] = wall_instance
            number_of_lava_walls = 3
            i = 0
            while(objects_map.get(f"fixed wall {number_of_lava_walls + i}")!= None):
                objects_map.pop(f"fixed wall {number_of_lava_walls + i}")
                i += 1
            wall_instance = Wall()
            wall_instance.xy = (144, 21)
            wall_instance.wh = (16, 38)
            objects_map['fixed wall 0'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (48, 21)
            wall_instance.wh = (64, 38)
            objects_map['fixed wall 1'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (8, 21)
            wall_instance.wh = (8, 38)
            objects_map['fixed wall 2'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (144, 101)
            wall_instance.wh = (16, 38)
            objects_map['fixed wall 3'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (36, 101)
            wall_instance.wh = (88, 38)
            objects_map['fixed wall 4'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (8, 101)
            wall_instance.wh = (8, 38)
            objects_map['fixed wall 5'] = wall_instance
            number_of_walls = 6
            i = 0
            while(objects_map.get(f"fixed wall {number_of_walls + i}")!= None):
                objects_map.pop(f"fixed wall {number_of_walls + i}")
                i += 1
        elif ram_state[28] == 7:
            number_of_lava_walls = 0
            i = 0
            while(objects_map.get(f"fixed wall {number_of_lava_walls + i}")!= None):
                objects_map.pop(f"fixed wall {number_of_lava_walls + i}")
                i += 1
            wall_instance = Wall()
            wall_instance.xy = (144, 21)
            wall_instance.wh = (16, 38)
            objects_map['fixed wall 0'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (36, 21)
            wall_instance.wh = (88, 38)
            objects_map['fixed wall 1'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (8, 21)
            wall_instance.wh = (8, 38)
            objects_map['fixed wall 2'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (88, 101)
            wall_instance.wh = (72, 38)
            objects_map['fixed wall 3'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (8, 101)
            wall_instance.wh = (64, 38)
            objects_map['fixed wall 4'] = wall_instance
            number_of_walls = 5
            i = 0
            while(objects_map.get(f"fixed wall {number_of_walls + i}")!= None):
                objects_map.pop(f"fixed wall {number_of_walls + i}")
                i += 1
        elif ram_state[28] == 8:
            wall_instance = LavaWall()
            wall_instance.xy = (132, 61)
            wall_instance.wh = (28, 37)
            objects_map['lava wall 0'] = wall_instance
            wall_instance = LavaWall()
            wall_instance.xy = (8, 61)
            wall_instance.wh = (20, 37)
            objects_map['lava wall 1'] = wall_instance
            number_of_lava_walls = 2
            i = 0
            while(objects_map.get(f"fixed wall {number_of_lava_walls + i}")!= None):
                objects_map.pop(f"fixed wall {number_of_lava_walls + i}")
                i += 1
            wall_instance = Wall()
            wall_instance.xy = (88, 21)
            wall_instance.wh = (72, 38)
            objects_map['fixed wall 0'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (8, 21)
            wall_instance.wh = (64, 38)
            objects_map['fixed wall 1'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (128, 101)
            wall_instance.wh = (32, 38)
            objects_map['fixed wall 2'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (48, 101)
            wall_instance.wh = (64, 38)
            objects_map['fixed wall 3'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (8, 101)
            wall_instance.wh = (24, 38)
            objects_map['fixed wall 4'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (132, 61)
            wall_instance.wh = (28, 37)
            objects_map['fixed wall 5'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (8, 61)
            wall_instance.wh = (20, 37)
            objects_map['fixed wall 6'] = wall_instance
            number_of_walls = 7
            i = 0
            while(objects_map.get(f"fixed wall {number_of_walls + i}")!= None):
                objects_map.pop(f"fixed wall {number_of_walls + i}")
                i += 1
        elif ram_state[28] == 9:
            number_of_lava_walls = 0
            i = 0
            while(objects_map.get(f"fixed wall {number_of_lava_walls + i}")!= None):
                objects_map.pop(f"fixed wall {number_of_lava_walls + i}")
                i += 1
            wall_instance = Wall()
            wall_instance.xy = (128, 21)
            wall_instance.wh = (32, 38)
            objects_map['fixed wall 0'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (48, 21)
            wall_instance.wh = (64, 38)
            objects_map['fixed wall 1'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (8, 21)
            wall_instance.wh = (24, 38)
            objects_map['fixed wall 2'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (96, 101)
            wall_instance.wh = (64, 38)
            objects_map['fixed wall 3'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (72, 101)
            wall_instance.wh = (16, 38)
            objects_map['fixed wall 4'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (8, 101)
            wall_instance.wh = (56, 38)
            objects_map['fixed wall 5'] = wall_instance
            number_of_walls = 6
            i = 0
            while(objects_map.get(f"fixed wall {number_of_walls + i}")!= None):
                objects_map.pop(f"fixed wall {number_of_walls + i}")
                i += 1
        elif ram_state[28] == 10:
            number_of_lava_walls = 0
            i = 0
            while(objects_map.get(f"fixed wall {number_of_lava_walls + i}")!= None):
                objects_map.pop(f"fixed wall {number_of_lava_walls + i}")
                i += 1
            wall_instance = Wall()
            wall_instance.xy = (96, 21)
            wall_instance.wh = (64, 38)
            objects_map['fixed wall 0'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (72, 21)
            wall_instance.wh = (16, 38)
            objects_map['fixed wall 1'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (8, 21)
            wall_instance.wh = (56, 38)
            objects_map['fixed wall 2'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (128, 101)
            wall_instance.wh = (32, 38)
            objects_map['fixed wall 3'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (8, 101)
            wall_instance.wh = (24, 38)
            objects_map['fixed wall 4'] = wall_instance
            number_of_walls = 5
            i = 0
            while(objects_map.get(f"fixed wall {number_of_walls + i}")!= None):
                objects_map.pop(f"fixed wall {number_of_walls + i}")
                i += 1
        elif ram_state[28] == 11:
            number_of_lava_walls = 0
            i = 0
            while(objects_map.get(f"fixed wall {number_of_lava_walls + i}")!= None):
                objects_map.pop(f"fixed wall {number_of_lava_walls + i}")
                i += 1
            wall_instance = Wall()
            wall_instance.xy = (8, 21)
            wall_instance.wh = (152, 38)
            objects_map['fixed wall 0'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (8, 101)
            wall_instance.wh = (152, 38)
            objects_map['fixed wall 1'] = wall_instance
            number_of_walls = 2
            i = 0
            while(objects_map.get(f"fixed wall {number_of_walls + i}")!= None):
                objects_map.pop(f"fixed wall {number_of_walls + i}")
                i += 1

    elif ram_state[117] == 7:
        if ram_state[28] == 0:
            wall_instance = LavaWall()
            wall_instance.xy = (140, 61)
            wall_instance.wh = (20, 37)
            objects_map['lava wall 0'] = wall_instance
            wall_instance = LavaWall()
            wall_instance.xy = (8, 61)
            wall_instance.wh = (12, 37)
            objects_map['lava wall 1'] = wall_instance
            number_of_lava_walls = 2
            i = 0
            while(objects_map.get(f"fixed wall {number_of_lava_walls + i}")!= None):
                objects_map.pop(f"fixed wall {number_of_lava_walls + i}")
                i += 1
            wall_instance = Wall()
            wall_instance.xy = (136, 21)
            wall_instance.wh = (24, 38)
            objects_map['fixed wall 0'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (8, 21)
            wall_instance.wh = (16, 38)
            objects_map['fixed wall 1'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (88, 101)
            wall_instance.wh = (72, 38)
            objects_map['fixed wall 2'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (8, 101)
            wall_instance.wh = (64, 38)
            objects_map['fixed wall 3'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (140, 61)
            wall_instance.wh = (20, 37)
            objects_map['fixed wall 4'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (8, 61)
            wall_instance.wh = (12, 37)
            objects_map['fixed wall 5'] = wall_instance
            number_of_walls = 6
            i = 0
            while(objects_map.get(f"fixed wall {number_of_walls + i}")!= None):
                objects_map.pop(f"fixed wall {number_of_walls + i}")
                i += 1
        elif ram_state[28] == 1:
            wall_instance = LavaWall()
            wall_instance.xy = (144, 61)
            wall_instance.wh = (16, 37)
            objects_map['lava wall 0'] = wall_instance
            wall_instance = LavaWall()
            wall_instance.xy = (8, 61)
            wall_instance.wh = (8, 37)
            objects_map['lava wall 1'] = wall_instance
            number_of_lava_walls = 2
            i = 0
            while(objects_map.get(f"fixed wall {number_of_lava_walls + i}")!= None):
                objects_map.pop(f"fixed wall {number_of_lava_walls + i}")
                i += 1
            wall_instance = Wall()
            wall_instance.xy = (88, 21)
            wall_instance.wh = (72, 38)
            objects_map['fixed wall 0'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (8, 21)
            wall_instance.wh = (64, 38)
            objects_map['fixed wall 1'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (112, 101)
            wall_instance.wh = (48, 38)
            objects_map['fixed wall 2'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (8, 101)
            wall_instance.wh = (40, 38)
            objects_map['fixed wall 3'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (144, 61)
            wall_instance.wh = (16, 37)
            objects_map['fixed wall 4'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (8, 61)
            wall_instance.wh = (8, 37)
            objects_map['fixed wall 5'] = wall_instance
            number_of_walls = 6
            i = 0
            while(objects_map.get(f"fixed wall {number_of_walls + i}")!= None):
                objects_map.pop(f"fixed wall {number_of_walls + i}")
                i += 1
        elif ram_state[28] == 2:
            wall_instance = LavaWall()
            wall_instance.xy = (92, 61)
            wall_instance.wh = (68, 37)
            objects_map['lava wall 0'] = wall_instance
            wall_instance = LavaWall()
            wall_instance.xy = (8, 61)
            wall_instance.wh = (60, 37)
            objects_map['lava wall 1'] = wall_instance
            number_of_lava_walls = 2
            i = 0
            while(objects_map.get(f"fixed wall {number_of_lava_walls + i}")!= None):
                objects_map.pop(f"fixed wall {number_of_lava_walls + i}")
                i += 1
            wall_instance = Wall()
            wall_instance.xy = (112, 21)
            wall_instance.wh = (48, 38)
            objects_map['fixed wall 0'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (8, 21)
            wall_instance.wh = (40, 38)
            objects_map['fixed wall 1'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (88, 101)
            wall_instance.wh = (72, 38)
            objects_map['fixed wall 2'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (8, 101)
            wall_instance.wh = (64, 38)
            objects_map['fixed wall 3'] = wall_instance
            number_of_walls = 4
            i = 0
            while(objects_map.get(f"fixed wall {number_of_walls + i}")!= None):
                objects_map.pop(f"fixed wall {number_of_walls + i}")
                i += 1
        elif ram_state[28] == 3:
            wall_instance = LavaWall()
            wall_instance.xy = (144, 61)
            wall_instance.wh = (16, 37)
            objects_map['lava wall 0'] = wall_instance
            wall_instance = LavaWall()
            wall_instance.xy = (8, 61)
            wall_instance.wh = (8, 37)
            objects_map['lava wall 1'] = wall_instance
            number_of_lava_walls = 2
            i = 0
            while(objects_map.get(f"fixed wall {number_of_lava_walls + i}")!= None):
                objects_map.pop(f"fixed wall {number_of_lava_walls + i}")
                i += 1
            wall_instance = Wall()
            wall_instance.xy = (88, 21)
            wall_instance.wh = (72, 38)
            objects_map['fixed wall 0'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (8, 21)
            wall_instance.wh = (64, 38)
            objects_map['fixed wall 1'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (112, 101)
            wall_instance.wh = (48, 38)
            objects_map['fixed wall 2'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (56, 101)
            wall_instance.wh = (48, 38)
            objects_map['fixed wall 3'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (8, 101)
            wall_instance.wh = (40, 38)
            objects_map['fixed wall 4'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (144, 61)
            wall_instance.wh = (16, 37)
            objects_map['fixed wall 5'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (8, 61)
            wall_instance.wh = (8, 37)
            objects_map['fixed wall 6'] = wall_instance
            number_of_walls = 7
            i = 0
            while(objects_map.get(f"fixed wall {number_of_walls + i}")!= None):
                objects_map.pop(f"fixed wall {number_of_walls + i}")
                i += 1
        elif ram_state[28] == 4:
            wall_instance = LavaWall()
            wall_instance.xy = (124, 61)
            wall_instance.wh = (36, 37)
            objects_map['lava wall 0'] = wall_instance
            wall_instance = LavaWall()
            wall_instance.xy = (60, 61)
            wall_instance.wh = (40, 37)
            objects_map['lava wall 1'] = wall_instance
            wall_instance = LavaWall()
            wall_instance.xy = (8, 61)
            wall_instance.wh = (28, 37)
            objects_map['lava wall 2'] = wall_instance
            number_of_lava_walls = 3
            i = 0
            while(objects_map.get(f"fixed wall {number_of_lava_walls + i}")!= None):
                objects_map.pop(f"fixed wall {number_of_lava_walls + i}")
                i += 1
            wall_instance = Wall()
            wall_instance.xy = (112, 21)
            wall_instance.wh = (48, 38)
            objects_map['fixed wall 0'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (56, 21)
            wall_instance.wh = (48, 38)
            objects_map['fixed wall 1'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (8, 21)
            wall_instance.wh = (40, 38)
            objects_map['fixed wall 2'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (128, 101)
            wall_instance.wh = (32, 38)
            objects_map['fixed wall 3'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (52, 101)
            wall_instance.wh = (56, 38)
            objects_map['fixed wall 4'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (8, 101)
            wall_instance.wh = (24, 38)
            objects_map['fixed wall 5'] = wall_instance
            number_of_walls = 6
            i = 0
            while(objects_map.get(f"fixed wall {number_of_walls + i}")!= None):
                objects_map.pop(f"fixed wall {number_of_walls + i}")
                i += 1
        elif ram_state[28] == 5:
            wall_instance = LavaWall()
            wall_instance.xy = (124, 61)
            wall_instance.wh = (36, 37)
            objects_map['lava wall 0'] = wall_instance
            wall_instance = LavaWall()
            wall_instance.xy = (8, 61)
            wall_instance.wh = (28, 37)
            objects_map['lava wall 1'] = wall_instance
            number_of_lava_walls = 2
            i = 0
            while(objects_map.get(f"fixed wall {number_of_lava_walls + i}")!= None):
                objects_map.pop(f"fixed wall {number_of_lava_walls + i}")
                i += 1
            wall_instance = Wall()
            wall_instance.xy = (128, 21)
            wall_instance.wh = (32, 38)
            objects_map['fixed wall 0'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (52, 21)
            wall_instance.wh = (56, 38)
            objects_map['fixed wall 1'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (8, 21)
            wall_instance.wh = (24, 38)
            objects_map['fixed wall 2'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (88, 101)
            wall_instance.wh = (72, 38)
            objects_map['fixed wall 3'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (8, 101)
            wall_instance.wh = (64, 38)
            objects_map['fixed wall 4'] = wall_instance
            number_of_walls = 5
            i = 0
            while(objects_map.get(f"fixed wall {number_of_walls + i}")!= None):
                objects_map.pop(f"fixed wall {number_of_walls + i}")
                i += 1
        elif ram_state[28] == 6:
            wall_instance = LavaWall()
            wall_instance.xy = (144, 61)
            wall_instance.wh = (16, 37)
            objects_map['lava wall 0'] = wall_instance
            wall_instance = LavaWall()
            wall_instance.xy = (8, 61)
            wall_instance.wh = (8, 37)
            objects_map['lava wall 1'] = wall_instance
            number_of_lava_walls = 2
            i = 0
            while(objects_map.get(f"fixed wall {number_of_lava_walls + i}")!= None):
                objects_map.pop(f"fixed wall {number_of_lava_walls + i}")
                i += 1
            wall_instance = Wall()
            wall_instance.xy = (88, 21)
            wall_instance.wh = (72, 38)
            objects_map['fixed wall 0'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (8, 21)
            wall_instance.wh = (64, 38)
            objects_map['fixed wall 1'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (136, 101)
            wall_instance.wh = (24, 38)
            objects_map['fixed wall 2'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (32, 101)
            wall_instance.wh = (96, 38)
            objects_map['fixed wall 3'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (8, 101)
            wall_instance.wh = (16, 38)
            objects_map['fixed wall 4'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (144, 61)
            wall_instance.wh = (16, 37)
            objects_map['fixed wall 5'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (8, 61)
            wall_instance.wh = (8, 37)
            objects_map['fixed wall 6'] = wall_instance
            number_of_walls = 7
            i = 0
            while(objects_map.get(f"fixed wall {number_of_walls + i}")!= None):
                objects_map.pop(f"fixed wall {number_of_walls + i}")
                i += 1
        elif ram_state[28] == 7:
            wall_instance = LavaWall()
            wall_instance.xy = (144, 61)
            wall_instance.wh = (16, 37)
            objects_map['lava wall 0'] = wall_instance
            wall_instance = LavaWall()
            wall_instance.xy = (64, 61)
            wall_instance.wh = (32, 37)
            objects_map['lava wall 1'] = wall_instance
            wall_instance = LavaWall()
            wall_instance.xy = (8, 61)
            wall_instance.wh = (8, 37)
            objects_map['lava wall 2'] = wall_instance
            number_of_lava_walls = 3
            i = 0
            while(objects_map.get(f"fixed wall {number_of_lava_walls + i}")!= None):
                objects_map.pop(f"fixed wall {number_of_lava_walls + i}")
                i += 1
            wall_instance = Wall()
            wall_instance.xy = (136, 21)
            wall_instance.wh = (24, 38)
            objects_map['fixed wall 0'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (32, 21)
            wall_instance.wh = (96, 38)
            objects_map['fixed wall 1'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (8, 21)
            wall_instance.wh = (16, 38)
            objects_map['fixed wall 2'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (112, 101)
            wall_instance.wh = (48, 38)
            objects_map['fixed wall 3'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (56, 101)
            wall_instance.wh = (48, 38)
            objects_map['fixed wall 4'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (8, 101)
            wall_instance.wh = (40, 38)
            objects_map['fixed wall 5'] = wall_instance
            number_of_walls = 6
            i = 0
            while(objects_map.get(f"fixed wall {number_of_walls + i}")!= None):
                objects_map.pop(f"fixed wall {number_of_walls + i}")
                i += 1
        elif ram_state[28] == 8:
            wall_instance = LavaWall()
            wall_instance.xy = (132, 61)
            wall_instance.wh = (28, 37)
            objects_map['lava wall 0'] = wall_instance
            wall_instance = LavaWall()
            wall_instance.xy = (72, 61)
            wall_instance.wh = (16, 37)
            objects_map['lava wall 1'] = wall_instance
            wall_instance = LavaWall()
            wall_instance.xy = (8, 61)
            wall_instance.wh = (20, 37)
            objects_map['lava wall 2'] = wall_instance
            number_of_lava_walls = 3
            i = 0
            while(objects_map.get(f"fixed wall {number_of_lava_walls + i}")!= None):
                objects_map.pop(f"fixed wall {number_of_lava_walls + i}")
                i += 1
            wall_instance = Wall()
            wall_instance.xy = (112, 21)
            wall_instance.wh = (48, 38)
            objects_map['fixed wall 0'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (56, 21)
            wall_instance.wh = (48, 38)
            objects_map['fixed wall 1'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (8, 21)
            wall_instance.wh = (40, 38)
            objects_map['fixed wall 2'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (144, 101)
            wall_instance.wh = (16, 38)
            objects_map['fixed wall 3'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (56, 101)
            wall_instance.wh = (48, 38)
            objects_map['fixed wall 4'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (8, 101)
            wall_instance.wh = (8, 38)
            objects_map['fixed wall 5'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (132, 61)
            wall_instance.wh = (28, 37)
            objects_map['fixed wall 6'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (72, 61)
            wall_instance.wh = (16, 37)
            objects_map['fixed wall 7'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (8, 61)
            wall_instance.wh = (20, 37)
            objects_map['fixed wall 8'] = wall_instance
            number_of_walls = 9
            i = 0
            while(objects_map.get(f"fixed wall {number_of_walls + i}")!= None):
                objects_map.pop(f"fixed wall {number_of_walls + i}")
                i += 1
        elif ram_state[28] == 9:
            wall_instance = LavaWall()
            wall_instance.xy = (128, 61)
            wall_instance.wh = (32, 37)
            objects_map['lava wall 0'] = wall_instance
            wall_instance = LavaWall()
            wall_instance.xy = (48, 61)
            wall_instance.wh = (64, 37)
            objects_map['lava wall 1'] = wall_instance
            wall_instance = LavaWall()
            wall_instance.xy = (8, 61)
            wall_instance.wh = (24, 37)
            objects_map['lava wall 2'] = wall_instance
            number_of_lava_walls = 3
            i = 0
            while(objects_map.get(f"fixed wall {number_of_lava_walls + i}")!= None):
                objects_map.pop(f"fixed wall {number_of_lava_walls + i}")
                i += 1
            wall_instance = Wall()
            wall_instance.xy = (144, 21)
            wall_instance.wh = (16, 38)
            objects_map['fixed wall 0'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (56, 21)
            wall_instance.wh = (48, 38)
            objects_map['fixed wall 1'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (8, 21)
            wall_instance.wh = (8, 38)
            objects_map['fixed wall 2'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (136, 101)
            wall_instance.wh = (24, 38)
            objects_map['fixed wall 3'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (64, 101)
            wall_instance.wh = (32, 38)
            objects_map['fixed wall 4'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (8, 101)
            wall_instance.wh = (16, 38)
            objects_map['fixed wall 5'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (128, 61)
            wall_instance.wh = (32, 37)
            objects_map['fixed wall 6'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (48, 61)
            wall_instance.wh = (64, 37)
            objects_map['fixed wall 7'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (8, 61)
            wall_instance.wh = (24, 37)
            objects_map['fixed wall 8'] = wall_instance
            number_of_walls = 9
            i = 0
            while(objects_map.get(f"fixed wall {number_of_walls + i}")!= None):
                objects_map.pop(f"fixed wall {number_of_walls + i}")
                i += 1
        elif ram_state[28] == 10:
            number_of_lava_walls = 0
            i = 0
            while(objects_map.get(f"fixed wall {number_of_lava_walls + i}")!= None):
                objects_map.pop(f"fixed wall {number_of_lava_walls + i}")
                i += 1
            wall_instance = Wall()
            wall_instance.xy = (136, 21)
            wall_instance.wh = (24, 38)
            objects_map['fixed wall 0'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (64, 21)
            wall_instance.wh = (32, 38)
            objects_map['fixed wall 1'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (8, 21)
            wall_instance.wh = (16, 38)
            objects_map['fixed wall 2'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (120, 101)
            wall_instance.wh = (40, 38)
            objects_map['fixed wall 3'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (8, 101)
            wall_instance.wh = (32, 38)
            objects_map['fixed wall 4'] = wall_instance
            number_of_walls = 5
            i = 0
            while(objects_map.get(f"fixed wall {number_of_walls + i}")!= None):
                objects_map.pop(f"fixed wall {number_of_walls + i}")
                i += 1
        elif ram_state[28] == 11:
            number_of_lava_walls = 0
            i = 0
            while(objects_map.get(f"fixed wall {number_of_lava_walls + i}")!= None):
                objects_map.pop(f"fixed wall {number_of_lava_walls + i}")
                i += 1
            wall_instance = Wall()
            wall_instance.xy = (8, 21)
            wall_instance.wh = (152, 38)
            objects_map['fixed wall 0'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (116, 101)
            wall_instance.wh = (44, 38)
            objects_map['fixed wall 1'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (8, 101)
            wall_instance.wh = (36, 38)
            objects_map['fixed wall 2'] = wall_instance
            number_of_walls = 3
            i = 0
            while(objects_map.get(f"fixed wall {number_of_walls + i}")!= None):
                objects_map.pop(f"fixed wall {number_of_walls + i}")
                i += 1
        elif ram_state[28] == 12:
            number_of_lava_walls = 0
            i = 0
            while(objects_map.get(f"fixed wall {number_of_lava_walls + i}")!= None):
                objects_map.pop(f"fixed wall {number_of_lava_walls + i}")
                i += 1
            wall_instance = Wall()
            wall_instance.xy = (8, 21)
            wall_instance.wh = (152, 38)
            objects_map['fixed wall 0'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (128, 101)
            wall_instance.wh = (32, 38)
            objects_map['fixed wall 1'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (72, 101)
            wall_instance.wh = (16, 38)
            objects_map['fixed wall 2'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (8, 101)
            wall_instance.wh = (24, 38)
            objects_map['fixed wall 3'] = wall_instance
            number_of_walls = 4
            i = 0
            while(objects_map.get(f"fixed wall {number_of_walls + i}")!= None):
                objects_map.pop(f"fixed wall {number_of_walls + i}")
                i += 1
        elif ram_state[28] == 13:
            number_of_lava_walls = 0
            i = 0
            while(objects_map.get(f"fixed wall {number_of_lava_walls + i}")!= None):
                objects_map.pop(f"fixed wall {number_of_lava_walls + i}")
                i += 1
            wall_instance = Wall()
            wall_instance.xy = (8, 21)
            wall_instance.wh = (152, 38)
            objects_map['fixed wall 0'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (8, 101)
            wall_instance.wh = (152, 38)
            objects_map['fixed wall 1'] = wall_instance
            number_of_walls = 2
            i = 0
            while(objects_map.get(f"fixed wall {number_of_walls + i}")!= None):
                objects_map.pop(f"fixed wall {number_of_walls + i}")
                i += 1

    elif ram_state[117] == 8:
        if ram_state[28] == 0:
            wall_instance = LavaWall()
            wall_instance.xy = (144, 61)
            wall_instance.wh = (16, 37)
            objects_map['lava wall 0'] = wall_instance
            wall_instance = LavaWall()
            wall_instance.xy = (8, 61)
            wall_instance.wh = (8, 37)
            objects_map['lava wall 1'] = wall_instance
            number_of_lava_walls = 2
            i = 0
            while(objects_map.get(f"fixed wall {number_of_lava_walls + i}")!= None):
                objects_map.pop(f"fixed wall {number_of_lava_walls + i}")
                i += 1
            wall_instance = Wall()
            wall_instance.xy = (136, 21)
            wall_instance.wh = (24, 38)
            objects_map['fixed wall 0'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (8, 21)
            wall_instance.wh = (16, 38)
            objects_map['fixed wall 1'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (88, 101)
            wall_instance.wh = (72, 38)
            objects_map['fixed wall 2'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (8, 101)
            wall_instance.wh = (64, 38)
            objects_map['fixed wall 3'] = wall_instance
            number_of_walls = 4
            i = 0
            while(objects_map.get(f"fixed wall {number_of_walls + i}")!= None):
                objects_map.pop(f"fixed wall {number_of_walls + i}")
                i += 1
        elif ram_state[28] == 1:
            wall_instance = LavaWall()
            wall_instance.xy = (144, 61)
            wall_instance.wh = (16, 37)
            objects_map['lava wall 0'] = wall_instance
            wall_instance = LavaWall()
            wall_instance.xy = (8, 61)
            wall_instance.wh = (8, 37)
            objects_map['lava wall 1'] = wall_instance
            number_of_lava_walls = 2
            i = 0
            while(objects_map.get(f"fixed wall {number_of_lava_walls + i}")!= None):
                objects_map.pop(f"fixed wall {number_of_lava_walls + i}")
                i += 1
            wall_instance = Wall()
            wall_instance.xy = (88, 21)
            wall_instance.wh = (72, 38)
            objects_map['fixed wall 0'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (8, 21)
            wall_instance.wh = (64, 38)
            objects_map['fixed wall 1'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (136, 101)
            wall_instance.wh = (24, 38)
            objects_map['fixed wall 2'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (40, 101)
            wall_instance.wh = (80, 38)
            objects_map['fixed wall 3'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (8, 101)
            wall_instance.wh = (16, 38)
            objects_map['fixed wall 4'] = wall_instance
            number_of_walls = 5
            i = 0
            while(objects_map.get(f"fixed wall {number_of_walls + i}")!= None):
                objects_map.pop(f"fixed wall {number_of_walls + i}")
                i += 1
        elif ram_state[28] == 2:
            wall_instance = LavaWall()
            wall_instance.xy = (140, 61)
            wall_instance.wh = (20, 37)
            objects_map['lava wall 0'] = wall_instance
            wall_instance = LavaWall()
            wall_instance.xy = (44, 61)
            wall_instance.wh = (72, 37)
            objects_map['lava wall 1'] = wall_instance
            wall_instance = LavaWall()
            wall_instance.xy = (8, 61)
            wall_instance.wh = (12, 37)
            objects_map['lava wall 2'] = wall_instance
            number_of_lava_walls = 3
            i = 0
            while(objects_map.get(f"fixed wall {number_of_lava_walls + i}")!= None):
                objects_map.pop(f"fixed wall {number_of_lava_walls + i}")
                i += 1
            wall_instance = Wall()
            wall_instance.xy = (136, 21)
            wall_instance.wh = (24, 38)
            objects_map['fixed wall 0'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (40, 21)
            wall_instance.wh = (80, 38)
            objects_map['fixed wall 1'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (8, 21)
            wall_instance.wh = (16, 38)
            objects_map['fixed wall 2'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (136, 101)
            wall_instance.wh = (24, 38)
            objects_map['fixed wall 3'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (8, 101)
            wall_instance.wh = (16, 38)
            objects_map['fixed wall 4'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (140, 61)
            wall_instance.wh = (20, 37)
            objects_map['fixed wall 5'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (44, 61)
            wall_instance.wh = (72, 37)
            objects_map['fixed wall 6'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (8, 61)
            wall_instance.wh = (12, 37)
            objects_map['fixed wall 7'] = wall_instance
            number_of_walls = 8
            i = 0
            while(objects_map.get(f"fixed wall {number_of_walls + i}")!= None):
                objects_map.pop(f"fixed wall {number_of_walls + i}")
                i += 1
        elif ram_state[28] == 3:
            wall_instance = LavaWall()
            wall_instance.xy = (128, 61)
            wall_instance.wh = (32, 37)
            objects_map['lava wall 0'] = wall_instance
            wall_instance = LavaWall()
            wall_instance.xy = (44, 61)
            wall_instance.wh = (72, 37)
            objects_map['lava wall 1'] = wall_instance
            wall_instance = LavaWall()
            wall_instance.xy = (8, 61)
            wall_instance.wh = (24, 37)
            objects_map['lava wall 2'] = wall_instance
            number_of_lava_walls = 3
            i = 0
            while(objects_map.get(f"fixed wall {number_of_lava_walls + i}")!= None):
                objects_map.pop(f"fixed wall {number_of_lava_walls + i}")
                i += 1
            wall_instance = Wall()
            wall_instance.xy = (136, 21)
            wall_instance.wh = (24, 38)
            objects_map['fixed wall 0'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (8, 21)
            wall_instance.wh = (16, 38)
            objects_map['fixed wall 1'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (136, 101)
            wall_instance.wh = (24, 38)
            objects_map['fixed wall 2'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (8, 101)
            wall_instance.wh = (16, 38)
            objects_map['fixed wall 3'] = wall_instance
            number_of_walls = 4
            i = 0
            while(objects_map.get(f"fixed wall {number_of_walls + i}")!= None):
                objects_map.pop(f"fixed wall {number_of_walls + i}")
                i += 1
        elif ram_state[28] == 4:
            wall_instance = LavaWall()
            wall_instance.xy = (116, 61)
            wall_instance.wh = (44, 37)
            objects_map['lava wall 0'] = wall_instance
            wall_instance = LavaWall()
            wall_instance.xy = (56, 61)
            wall_instance.wh = (48, 37)
            objects_map['lava wall 1'] = wall_instance
            wall_instance = LavaWall()
            wall_instance.xy = (8, 61)
            wall_instance.wh = (36, 37)
            objects_map['lava wall 2'] = wall_instance
            number_of_lava_walls = 3
            i = 0
            while(objects_map.get(f"fixed wall {number_of_lava_walls + i}")!= None):
                objects_map.pop(f"fixed wall {number_of_lava_walls + i}")
                i += 1
            wall_instance = Wall()
            wall_instance.xy = (136, 21)
            wall_instance.wh = (24, 38)
            objects_map['fixed wall 0'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (8, 21)
            wall_instance.wh = (16, 38)
            objects_map['fixed wall 1'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (136, 101)
            wall_instance.wh = (24, 38)
            objects_map['fixed wall 2'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (8, 101)
            wall_instance.wh = (16, 38)
            objects_map['fixed wall 3'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (116, 61)
            wall_instance.wh = (44, 37)
            objects_map['fixed wall 4'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (56, 61)
            wall_instance.wh = (48, 37)
            objects_map['fixed wall 5'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (8, 61)
            wall_instance.wh = (36, 37)
            objects_map['fixed wall 6'] = wall_instance
            number_of_walls = 7
            i = 0
            while(objects_map.get(f"fixed wall {number_of_walls + i}")!= None):
                objects_map.pop(f"fixed wall {number_of_walls + i}")
                i += 1
        elif ram_state[28] == 5:
            wall_instance = LavaWall()
            wall_instance.xy = (108, 61)
            wall_instance.wh = (52, 37)
            objects_map['lava wall 0'] = wall_instance
            wall_instance = LavaWall()
            wall_instance.xy = (64, 61)
            wall_instance.wh = (32, 37)
            objects_map['lava wall 1'] = wall_instance
            wall_instance = LavaWall()
            wall_instance.xy = (8, 61)
            wall_instance.wh = (44, 37)
            objects_map['lava wall 2'] = wall_instance
            number_of_lava_walls = 3
            i = 0
            while(objects_map.get(f"fixed wall {number_of_lava_walls + i}")!= None):
                objects_map.pop(f"fixed wall {number_of_lava_walls + i}")
                i += 1
            wall_instance = Wall()
            wall_instance.xy = (136, 21)
            wall_instance.wh = (24, 38)
            objects_map['fixed wall 0'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (8, 21)
            wall_instance.wh = (16, 38)
            objects_map['fixed wall 1'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (136, 101)
            wall_instance.wh = (24, 38)
            objects_map['fixed wall 2'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (8, 101)
            wall_instance.wh = (16, 38)
            objects_map['fixed wall 3'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (108, 61)
            wall_instance.wh = (52, 37)
            objects_map['fixed wall 4'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (64, 61)
            wall_instance.wh = (32, 37)
            objects_map['fixed wall 5'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (8, 61)
            wall_instance.wh = (44, 37)
            objects_map['fixed wall 6'] = wall_instance
            number_of_walls = 7
            i = 0
            while(objects_map.get(f"fixed wall {number_of_walls + i}")!= None):
                objects_map.pop(f"fixed wall {number_of_walls + i}")
                i += 1
        elif ram_state[28] == 6:
            wall_instance = LavaWall()
            wall_instance.xy = (108, 61)
            wall_instance.wh = (52, 37)
            objects_map['lava wall 0'] = wall_instance
            wall_instance = LavaWall()
            wall_instance.xy = (8, 61)
            wall_instance.wh = (44, 37)
            objects_map['lava wall 1'] = wall_instance
            number_of_lava_walls = 2
            i = 0
            while(objects_map.get(f"fixed wall {number_of_lava_walls + i}")!= None):
                objects_map.pop(f"fixed wall {number_of_lava_walls + i}")
                i += 1
            wall_instance = Wall()
            wall_instance.xy = (136, 21)
            wall_instance.wh = (24, 38)
            objects_map['fixed wall 0'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (8, 21)
            wall_instance.wh = (16, 38)
            objects_map['fixed wall 1'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (104, 101)
            wall_instance.wh = (56, 38)
            objects_map['fixed wall 2'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (72, 101)
            wall_instance.wh = (16, 38)
            objects_map['fixed wall 3'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (8, 101)
            wall_instance.wh = (48, 38)
            objects_map['fixed wall 4'] = wall_instance
            number_of_walls = 5
            i = 0
            while(objects_map.get(f"fixed wall {number_of_walls + i}")!= None):
                objects_map.pop(f"fixed wall {number_of_walls + i}")
                i += 1
        elif ram_state[28] == 7:
            wall_instance = LavaWall()
            wall_instance.xy = (144, 61)
            wall_instance.wh = (16, 37)
            objects_map['lava wall 0'] = wall_instance
            wall_instance = LavaWall()
            wall_instance.xy = (8, 61)
            wall_instance.wh = (8, 37)
            objects_map['lava wall 1'] = wall_instance
            number_of_lava_walls = 2
            i = 0
            while(objects_map.get(f"fixed wall {number_of_lava_walls + i}")!= None):
                objects_map.pop(f"fixed wall {number_of_lava_walls + i}")
                i += 1
            wall_instance = Wall()
            wall_instance.xy = (104, 21)
            wall_instance.wh = (56, 38)
            objects_map['fixed wall 0'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (72, 21)
            wall_instance.wh = (16, 38)
            objects_map['fixed wall 1'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (8, 21)
            wall_instance.wh = (48, 38)
            objects_map['fixed wall 2'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (136, 101)
            wall_instance.wh = (24, 38)
            objects_map['fixed wall 3'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (32, 101)
            wall_instance.wh = (96, 38)
            objects_map['fixed wall 4'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (8, 101)
            wall_instance.wh = (16, 38)
            objects_map['fixed wall 5'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (144, 61)
            wall_instance.wh = (16, 37)
            objects_map['fixed wall 6'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (8, 61)
            wall_instance.wh = (8, 37)
            objects_map['fixed wall 7'] = wall_instance
            number_of_walls = 8
            i = 0
            while(objects_map.get(f"fixed wall {number_of_walls + i}")!= None):
                objects_map.pop(f"fixed wall {number_of_walls + i}")
                i += 1
        elif ram_state[28] == 8:
            wall_instance = LavaWall()
            wall_instance.xy = (144, 61)
            wall_instance.wh = (16, 37)
            objects_map['lava wall 0'] = wall_instance
            wall_instance = LavaWall()
            wall_instance.xy = (8, 61)
            wall_instance.wh = (8, 37)
            objects_map['lava wall 1'] = wall_instance
            number_of_lava_walls = 2
            i = 0
            while(objects_map.get(f"fixed wall {number_of_lava_walls + i}")!= None):
                objects_map.pop(f"fixed wall {number_of_lava_walls + i}")
                i += 1
            wall_instance = Wall()
            wall_instance.xy = (136, 21)
            wall_instance.wh = (24, 38)
            objects_map['fixed wall 0'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (32, 21)
            wall_instance.wh = (96, 38)
            objects_map['fixed wall 1'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (8, 21)
            wall_instance.wh = (16, 38)
            objects_map['fixed wall 2'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (88, 101)
            wall_instance.wh = (72, 38)
            objects_map['fixed wall 3'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (8, 101)
            wall_instance.wh = (64, 38)
            objects_map['fixed wall 4'] = wall_instance
            number_of_walls = 5
            i = 0
            while(objects_map.get(f"fixed wall {number_of_walls + i}")!= None):
                objects_map.pop(f"fixed wall {number_of_walls + i}")
                i += 1
        elif ram_state[28] == 9:
            wall_instance = LavaWall()
            wall_instance.xy = (92, 61)
            wall_instance.wh = (68, 37)
            objects_map['lava wall 0'] = wall_instance
            wall_instance = LavaWall()
            wall_instance.xy = (8, 61)
            wall_instance.wh = (60, 37)
            objects_map['lava wall 1'] = wall_instance
            number_of_lava_walls = 2
            i = 0
            while(objects_map.get(f"fixed wall {number_of_lava_walls + i}")!= None):
                objects_map.pop(f"fixed wall {number_of_lava_walls + i}")
                i += 1
            wall_instance = Wall()
            wall_instance.xy = (88, 21)
            wall_instance.wh = (72, 38)
            objects_map['fixed wall 0'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (8, 21)
            wall_instance.wh = (64, 38)
            objects_map['fixed wall 1'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (136, 101)
            wall_instance.wh = (24, 38)
            objects_map['fixed wall 2'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (8, 101)
            wall_instance.wh = (16, 38)
            objects_map['fixed wall 3'] = wall_instance
            number_of_walls = 4
            i = 0
            while(objects_map.get(f"fixed wall {number_of_walls + i}")!= None):
                objects_map.pop(f"fixed wall {number_of_walls + i}")
                i += 1
        elif ram_state[28] == 10:
            number_of_lava_walls = 0
            i = 0
            while(objects_map.get(f"fixed wall {number_of_lava_walls + i}")!= None):
                objects_map.pop(f"fixed wall {number_of_lava_walls + i}")
                i += 1
            wall_instance = Wall()
            wall_instance.xy = (136, 21)
            wall_instance.wh = (24, 38)
            objects_map['fixed wall 0'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (8, 21)
            wall_instance.wh = (16, 38)
            objects_map['fixed wall 1'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (112, 101)
            wall_instance.wh = (48, 38)
            objects_map['fixed wall 2'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (8, 101)
            wall_instance.wh = (40, 38)
            objects_map['fixed wall 3'] = wall_instance
            number_of_walls = 4
            i = 0
            while(objects_map.get(f"fixed wall {number_of_walls + i}")!= None):
                objects_map.pop(f"fixed wall {number_of_walls + i}")
                i += 1
        elif ram_state[28] == 11:
            number_of_lava_walls = 0
            i = 0
            while(objects_map.get(f"fixed wall {number_of_lava_walls + i}")!= None):
                objects_map.pop(f"fixed wall {number_of_lava_walls + i}")
                i += 1
            wall_instance = Wall()
            wall_instance.xy = (8, 21)
            wall_instance.wh = (152, 38)
            objects_map['fixed wall 0'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (128, 101)
            wall_instance.wh = (32, 38)
            objects_map['fixed wall 1'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (8, 101)
            wall_instance.wh = (24, 38)
            objects_map['fixed wall 2'] = wall_instance
            number_of_walls = 3
            i = 0
            while(objects_map.get(f"fixed wall {number_of_walls + i}")!= None):
                objects_map.pop(f"fixed wall {number_of_walls + i}")
                i += 1
        elif ram_state[28] == 12:
            number_of_lava_walls = 0
            i = 0
            while(objects_map.get(f"fixed wall {number_of_lava_walls + i}")!= None):
                objects_map.pop(f"fixed wall {number_of_lava_walls + i}")
                i += 1
            wall_instance = Wall()
            wall_instance.xy = (8, 21)
            wall_instance.wh = (152, 38)
            objects_map['fixed wall 0'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (140, 101)
            wall_instance.wh = (20, 38)
            objects_map['fixed wall 1'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (72, 101)
            wall_instance.wh = (16, 38)
            objects_map['fixed wall 2'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (8, 101)
            wall_instance.wh = (12, 38)
            objects_map['fixed wall 3'] = wall_instance
            number_of_walls = 4
            i = 0
            while(objects_map.get(f"fixed wall {number_of_walls + i}")!= None):
                objects_map.pop(f"fixed wall {number_of_walls + i}")
                i += 1
        elif ram_state[28] == 13:
            number_of_lava_walls = 0
            i = 0
            while(objects_map.get(f"fixed wall {number_of_lava_walls + i}")!= None):
                objects_map.pop(f"fixed wall {number_of_lava_walls + i}")
                i += 1
            wall_instance = Wall()
            wall_instance.xy = (8, 21)
            wall_instance.wh = (152, 38)
            objects_map['fixed wall 0'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (112, 101)
            wall_instance.wh = (48, 38)
            objects_map['fixed wall 1'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (8, 101)
            wall_instance.wh = (40, 38)
            objects_map['fixed wall 2'] = wall_instance
            number_of_walls = 3
            i = 0
            while(objects_map.get(f"fixed wall {number_of_walls + i}")!= None):
                objects_map.pop(f"fixed wall {number_of_walls + i}")
                i += 1
        elif ram_state[28] == 14:
            number_of_lava_walls = 0
            i = 0
            while(objects_map.get(f"fixed wall {number_of_lava_walls + i}")!= None):
                objects_map.pop(f"fixed wall {number_of_lava_walls + i}")
                i += 1
            wall_instance = Wall()
            wall_instance.xy = (8, 21)
            wall_instance.wh = (152, 38)
            objects_map['fixed wall 0'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (136, 101)
            wall_instance.wh = (24, 38)
            objects_map['fixed wall 1'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (8, 101)
            wall_instance.wh = (16, 38)
            objects_map['fixed wall 2'] = wall_instance
            number_of_walls = 3
            i = 0
            while(objects_map.get(f"fixed wall {number_of_walls + i}")!= None):
                objects_map.pop(f"fixed wall {number_of_walls + i}")
                i += 1
        elif ram_state[28] == 15:
            number_of_lava_walls = 0
            i = 0
            while(objects_map.get(f"fixed wall {number_of_lava_walls + i}")!= None):
                objects_map.pop(f"fixed wall {number_of_lava_walls + i}")
                i += 1
            wall_instance = Wall()
            wall_instance.xy = (8, 21)
            wall_instance.wh = (152, 38)
            objects_map['fixed wall 0'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (8, 101)
            wall_instance.wh = (152, 38)
            objects_map['fixed wall 1'] = wall_instance
            number_of_walls = 2
            i = 0
            while(objects_map.get(f"fixed wall {number_of_walls + i}")!= None):
                objects_map.pop(f"fixed wall {number_of_walls + i}")
                i += 1

    elif ram_state[117] == 9:
        if ram_state[28] == 0:
            wall_instance = LavaWall()
            wall_instance.xy = (144, 61)
            wall_instance.wh = (16, 37)
            objects_map['lava wall 0'] = wall_instance
            wall_instance = LavaWall()
            wall_instance.xy = (8, 61)
            wall_instance.wh = (8, 37)
            objects_map['lava wall 1'] = wall_instance
            number_of_lava_walls = 2
            i = 0
            while(objects_map.get(f"fixed wall {number_of_lava_walls + i}")!= None):
                objects_map.pop(f"fixed wall {number_of_lava_walls + i}")
                i += 1
            wall_instance = Wall()
            wall_instance.xy = (136, 21)
            wall_instance.wh = (24, 38)
            objects_map['fixed wall 0'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (8, 21)
            wall_instance.wh = (16, 38)
            objects_map['fixed wall 1'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (88, 101)
            wall_instance.wh = (72, 38)
            objects_map['fixed wall 2'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (8, 101)
            wall_instance.wh = (64, 38)
            objects_map['fixed wall 3'] = wall_instance
            number_of_walls = 4
            i = 0
            while(objects_map.get(f"fixed wall {number_of_walls + i}")!= None):
                objects_map.pop(f"fixed wall {number_of_walls + i}")
                i += 1
        elif ram_state[28] == 1:
            wall_instance = LavaWall()
            wall_instance.xy = (144, 61)
            wall_instance.wh = (16, 37)
            objects_map['lava wall 0'] = wall_instance
            wall_instance = LavaWall()
            wall_instance.xy = (8, 61)
            wall_instance.wh = (8, 37)
            objects_map['lava wall 1'] = wall_instance
            number_of_lava_walls = 2
            i = 0
            while(objects_map.get(f"fixed wall {number_of_lava_walls + i}")!= None):
                objects_map.pop(f"fixed wall {number_of_lava_walls + i}")
                i += 1
            wall_instance = Wall()
            wall_instance.xy = (88, 21)
            wall_instance.wh = (72, 38)
            objects_map['fixed wall 0'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (8, 21)
            wall_instance.wh = (64, 38)
            objects_map['fixed wall 1'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (136, 101)
            wall_instance.wh = (24, 38)
            objects_map['fixed wall 2'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (32, 101)
            wall_instance.wh = (96, 38)
            objects_map['fixed wall 3'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (8, 101)
            wall_instance.wh = (16, 38)
            objects_map['fixed wall 4'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (144, 61)
            wall_instance.wh = (16, 37)
            objects_map['fixed wall 5'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (8, 61)
            wall_instance.wh = (8, 37)
            objects_map['fixed wall 6'] = wall_instance
            number_of_walls = 7
            i = 0
            while(objects_map.get(f"fixed wall {number_of_walls + i}")!= None):
                objects_map.pop(f"fixed wall {number_of_walls + i}")
                i += 1
        elif ram_state[28] == 2:
            wall_instance = LavaWall()
            wall_instance.xy = (144, 61)
            wall_instance.wh = (16, 37)
            objects_map['lava wall 0'] = wall_instance
            wall_instance = LavaWall()
            wall_instance.xy = (8, 61)
            wall_instance.wh = (8, 37)
            objects_map['lava wall 1'] = wall_instance
            number_of_lava_walls = 2
            i = 0
            while(objects_map.get(f"fixed wall {number_of_lava_walls + i}")!= None):
                objects_map.pop(f"fixed wall {number_of_lava_walls + i}")
                i += 1
            wall_instance = Wall()
            wall_instance.xy = (136, 21)
            wall_instance.wh = (24, 38)
            objects_map['fixed wall 0'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (32, 21)
            wall_instance.wh = (96, 38)
            objects_map['fixed wall 1'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (8, 21)
            wall_instance.wh = (16, 38)
            objects_map['fixed wall 2'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (84, 101)
            wall_instance.wh = (76, 38)
            objects_map['fixed wall 3'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (8, 101)
            wall_instance.wh = (68, 38)
            objects_map['fixed wall 4'] = wall_instance
            number_of_walls = 5
            i = 0
            while(objects_map.get(f"fixed wall {number_of_walls + i}")!= None):
                objects_map.pop(f"fixed wall {number_of_walls + i}")
                i += 1
        elif ram_state[28] == 3:
            wall_instance = LavaWall()
            wall_instance.xy = (144, 61)
            wall_instance.wh = (16, 37)
            objects_map['lava wall 0'] = wall_instance
            wall_instance = LavaWall()
            wall_instance.xy = (8, 61)
            wall_instance.wh = (8, 37)
            objects_map['lava wall 1'] = wall_instance
            number_of_lava_walls = 2
            i = 0
            while(objects_map.get(f"fixed wall {number_of_lava_walls + i}")!= None):
                objects_map.pop(f"fixed wall {number_of_lava_walls + i}")
                i += 1
            wall_instance = Wall()
            wall_instance.xy = (84, 21)
            wall_instance.wh = (76, 38)
            objects_map['fixed wall 0'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (8, 21)
            wall_instance.wh = (68, 38)
            objects_map['fixed wall 1'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (132, 101)
            wall_instance.wh = (28, 38)
            objects_map['fixed wall 2'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (84, 101)
            wall_instance.wh = (40, 38)
            objects_map['fixed wall 3'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (36, 101)
            wall_instance.wh = (40, 38)
            objects_map['fixed wall 4'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (8, 101)
            wall_instance.wh = (20, 38)
            objects_map['fixed wall 5'] = wall_instance
            number_of_walls = 6
            i = 0
            while(objects_map.get(f"fixed wall {number_of_walls + i}")!= None):
                objects_map.pop(f"fixed wall {number_of_walls + i}")
                i += 1
        elif ram_state[28] == 4:
            wall_instance = LavaWall()
            wall_instance.xy = (136, 61)
            wall_instance.wh = (24, 37)
            objects_map['lava wall 0'] = wall_instance
            wall_instance = LavaWall()
            wall_instance.xy = (56, 61)
            wall_instance.wh = (64, 37)
            objects_map['lava wall 1'] = wall_instance
            wall_instance = LavaWall()
            wall_instance.xy = (8, 61)
            wall_instance.wh = (32, 37)
            objects_map['lava wall 2'] = wall_instance
            number_of_lava_walls = 3
            i = 0
            while(objects_map.get(f"fixed wall {number_of_lava_walls + i}")!= None):
                objects_map.pop(f"fixed wall {number_of_lava_walls + i}")
                i += 1
            wall_instance = Wall()
            wall_instance.xy = (132, 21)
            wall_instance.wh = (28, 38)
            objects_map['fixed wall 0'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (84, 21)
            wall_instance.wh = (40, 38)
            objects_map['fixed wall 1'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (36, 21)
            wall_instance.wh = (40, 38)
            objects_map['fixed wall 2'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (8, 21)
            wall_instance.wh = (20, 38)
            objects_map['fixed wall 3'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (132, 101)
            wall_instance.wh = (28, 38)
            objects_map['fixed wall 4'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (36, 101)
            wall_instance.wh = (88, 38)
            objects_map['fixed wall 5'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (8, 101)
            wall_instance.wh = (20, 38)
            objects_map['fixed wall 6'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (136, 61)
            wall_instance.wh = (24, 37)
            objects_map['fixed wall 7'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (56, 61)
            wall_instance.wh = (64, 37)
            objects_map['fixed wall 8'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (8, 61)
            wall_instance.wh = (32, 37)
            objects_map['fixed wall 9'] = wall_instance
            number_of_walls = 10
            i = 0
            while(objects_map.get(f"fixed wall {number_of_walls + i}")!= None):
                objects_map.pop(f"fixed wall {number_of_walls + i}")
                i += 1
        elif ram_state[28] == 5:
            wall_instance = LavaWall()
            wall_instance.xy = (144, 61)
            wall_instance.wh = (16, 37)
            objects_map['lava wall 0'] = wall_instance
            wall_instance = LavaWall()
            wall_instance.xy = (44, 61)
            wall_instance.wh = (72, 37)
            objects_map['lava wall 1'] = wall_instance
            wall_instance = LavaWall()
            wall_instance.xy = (8, 61)
            wall_instance.wh = (8, 37)
            objects_map['lava wall 2'] = wall_instance
            number_of_lava_walls = 3
            i = 0
            while(objects_map.get(f"fixed wall {number_of_lava_walls + i}")!= None):
                objects_map.pop(f"fixed wall {number_of_lava_walls + i}")
                i += 1
            wall_instance = Wall()
            wall_instance.xy = (132, 21)
            wall_instance.wh = (28, 38)
            objects_map['fixed wall 0'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (36, 21)
            wall_instance.wh = (88, 38)
            objects_map['fixed wall 1'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (8, 21)
            wall_instance.wh = (20, 38)
            objects_map['fixed wall 2'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (124, 101)
            wall_instance.wh = (36, 38)
            objects_map['fixed wall 3'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (48, 101)
            wall_instance.wh = (64, 38)
            objects_map['fixed wall 4'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (8, 101)
            wall_instance.wh = (28, 38)
            objects_map['fixed wall 5'] = wall_instance
            number_of_walls = 6
            i = 0
            while(objects_map.get(f"fixed wall {number_of_walls + i}")!= None):
                objects_map.pop(f"fixed wall {number_of_walls + i}")
                i += 1
        elif ram_state[28] == 6:
            wall_instance = LavaWall()
            wall_instance.xy = (144, 61)
            wall_instance.wh = (16, 37)
            objects_map['lava wall 0'] = wall_instance
            wall_instance = LavaWall()
            wall_instance.xy = (8, 61)
            wall_instance.wh = (8, 37)
            objects_map['lava wall 1'] = wall_instance
            number_of_lava_walls = 2
            i = 0
            while(objects_map.get(f"fixed wall {number_of_lava_walls + i}")!= None):
                objects_map.pop(f"fixed wall {number_of_lava_walls + i}")
                i += 1
            wall_instance = Wall()
            wall_instance.xy = (124, 21)
            wall_instance.wh = (36, 38)
            objects_map['fixed wall 0'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (48, 21)
            wall_instance.wh = (64, 38)
            objects_map['fixed wall 1'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (8, 21)
            wall_instance.wh = (28, 38)
            objects_map['fixed wall 2'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (140, 101)
            wall_instance.wh = (20, 38)
            objects_map['fixed wall 3'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (88, 101)
            wall_instance.wh = (36, 38)
            objects_map['fixed wall 4'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (36, 101)
            wall_instance.wh = (36, 38)
            objects_map['fixed wall 5'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (8, 101)
            wall_instance.wh = (12, 38)
            objects_map['fixed wall 6'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (144, 61)
            wall_instance.wh = (16, 37)
            objects_map['fixed wall 7'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (8, 61)
            wall_instance.wh = (8, 37)
            objects_map['fixed wall 8'] = wall_instance
            number_of_walls = 9
            i = 0
            while(objects_map.get(f"fixed wall {number_of_walls + i}")!= None):
                objects_map.pop(f"fixed wall {number_of_walls + i}")
                i += 1
        elif ram_state[28] == 7:
            wall_instance = LavaWall()
            wall_instance.xy = (136, 61)
            wall_instance.wh = (24, 37)
            objects_map['lava wall 0'] = wall_instance
            wall_instance = LavaWall()
            wall_instance.xy = (84, 61)
            wall_instance.wh = (44, 37)
            objects_map['lava wall 1'] = wall_instance
            wall_instance = LavaWall()
            wall_instance.xy = (32, 61)
            wall_instance.wh = (44, 37)
            objects_map['lava wall 2'] = wall_instance
            wall_instance = LavaWall()
            wall_instance.xy = (8, 61)
            wall_instance.wh = (16, 37)
            objects_map['lava wall 3'] = wall_instance
            number_of_lava_walls = 4
            i = 0
            while(objects_map.get(f"fixed wall {number_of_lava_walls + i}")!= None):
                objects_map.pop(f"fixed wall {number_of_lava_walls + i}")
                i += 1
            wall_instance = Wall()
            wall_instance.xy = (140, 21)
            wall_instance.wh = (20, 38)
            objects_map['fixed wall 0'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (88, 21)
            wall_instance.wh = (36, 38)
            objects_map['fixed wall 1'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (36, 21)
            wall_instance.wh = (36, 38)
            objects_map['fixed wall 2'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (8, 21)
            wall_instance.wh = (12, 38)
            objects_map['fixed wall 3'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (144, 101)
            wall_instance.wh = (16, 38)
            objects_map['fixed wall 4'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (8, 101)
            wall_instance.wh = (8, 38)
            objects_map['fixed wall 5'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (136, 61)
            wall_instance.wh = (24, 37)
            objects_map['fixed wall 6'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (84, 61)
            wall_instance.wh = (44, 37)
            objects_map['fixed wall 7'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (32, 61)
            wall_instance.wh = (44, 37)
            objects_map['fixed wall 8'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (8, 61)
            wall_instance.wh = (16, 37)
            objects_map['fixed wall 9'] = wall_instance
            number_of_walls = 10
            i = 0
            while(objects_map.get(f"fixed wall {number_of_walls + i}")!= None):
                objects_map.pop(f"fixed wall {number_of_walls + i}")
                i += 1
        elif ram_state[28] == 8:
            wall_instance = LavaWall()
            wall_instance.xy = (88, 61)
            wall_instance.wh = (72, 37)
            objects_map['lava wall 0'] = wall_instance
            wall_instance = LavaWall()
            wall_instance.xy = (8, 61)
            wall_instance.wh = (64, 37)
            objects_map['lava wall 1'] = wall_instance
            number_of_lava_walls = 2
            i = 0
            while(objects_map.get(f"fixed wall {number_of_lava_walls + i}")!= None):
                objects_map.pop(f"fixed wall {number_of_lava_walls + i}")
                i += 1
            wall_instance = Wall()
            wall_instance.xy = (144, 21)
            wall_instance.wh = (16, 38)
            objects_map['fixed wall 0'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (8, 21)
            wall_instance.wh = (8, 38)
            objects_map['fixed wall 1'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (144, 101)
            wall_instance.wh = (16, 38)
            objects_map['fixed wall 2'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (8, 101)
            wall_instance.wh = (8, 38)
            objects_map['fixed wall 3'] = wall_instance
            number_of_walls = 4
            i = 0
            while(objects_map.get(f"fixed wall {number_of_walls + i}")!= None):
                objects_map.pop(f"fixed wall {number_of_walls + i}")
                i += 1
        elif ram_state[28] == 9:
            wall_instance = LavaWall()
            wall_instance.xy = (96, 61)
            wall_instance.wh = (64, 37)
            objects_map['lava wall 0'] = wall_instance
            wall_instance = LavaWall()
            wall_instance.xy = (8, 61)
            wall_instance.wh = (56, 37)
            objects_map['lava wall 1'] = wall_instance
            number_of_lava_walls = 2
            i = 0
            while(objects_map.get(f"fixed wall {number_of_lava_walls + i}")!= None):
                objects_map.pop(f"fixed wall {number_of_lava_walls + i}")
                i += 1
            wall_instance = Wall()
            wall_instance.xy = (144, 21)
            wall_instance.wh = (16, 38)
            objects_map['fixed wall 0'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (8, 21)
            wall_instance.wh = (8, 38)
            objects_map['fixed wall 1'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (136, 101)
            wall_instance.wh = (24, 38)
            objects_map['fixed wall 2'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (8, 101)
            wall_instance.wh = (16, 38)
            objects_map['fixed wall 3'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (96, 61)
            wall_instance.wh = (64, 37)
            objects_map['fixed wall 4'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (8, 61)
            wall_instance.wh = (56, 37)
            objects_map['fixed wall 5'] = wall_instance
            number_of_walls = 6
            i = 0
            while(objects_map.get(f"fixed wall {number_of_walls + i}")!= None):
                objects_map.pop(f"fixed wall {number_of_walls + i}")
                i += 1
        elif ram_state[28] == 10:
            wall_instance = LavaWall()
            wall_instance.xy = (48, 61)
            wall_instance.wh = (64, 37)
            objects_map['lava wall 0'] = wall_instance
            number_of_lava_walls = 1
            i = 0
            while(objects_map.get(f"fixed wall {number_of_lava_walls + i}")!= None):
                objects_map.pop(f"fixed wall {number_of_lava_walls + i}")
                i += 1
            wall_instance = Wall()
            wall_instance.xy = (136, 21)
            wall_instance.wh = (24, 38)
            objects_map['fixed wall 0'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (8, 21)
            wall_instance.wh = (16, 38)
            objects_map['fixed wall 1'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (128, 101)
            wall_instance.wh = (32, 38)
            objects_map['fixed wall 2'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (8, 101)
            wall_instance.wh = (24, 38)
            objects_map['fixed wall 3'] = wall_instance
            number_of_walls = 4
            i = 0
            while(objects_map.get(f"fixed wall {number_of_walls + i}")!= None):
                objects_map.pop(f"fixed wall {number_of_walls + i}")
                i += 1
        elif ram_state[28] == 11:
            number_of_lava_walls = 0
            i = 0
            while(objects_map.get(f"fixed wall {number_of_lava_walls + i}")!= None):
                objects_map.pop(f"fixed wall {number_of_lava_walls + i}")
                i += 1
            wall_instance = Wall()
            wall_instance.xy = (8, 21)
            wall_instance.wh = (152, 38)
            objects_map['fixed wall 0'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (132, 101)
            wall_instance.wh = (28, 38)
            objects_map['fixed wall 1'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (8, 101)
            wall_instance.wh = (20, 38)
            objects_map['fixed wall 2'] = wall_instance
            number_of_walls = 3
            i = 0
            while(objects_map.get(f"fixed wall {number_of_walls + i}")!= None):
                objects_map.pop(f"fixed wall {number_of_walls + i}")
                i += 1
        elif ram_state[28] == 12:
            number_of_lava_walls = 0
            i = 0
            while(objects_map.get(f"fixed wall {number_of_lava_walls + i}")!= None):
                objects_map.pop(f"fixed wall {number_of_lava_walls + i}")
                i += 1
            wall_instance = Wall()
            wall_instance.xy = (8, 21)
            wall_instance.wh = (152, 38)
            objects_map['fixed wall 0'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (136, 101)
            wall_instance.wh = (24, 38)
            objects_map['fixed wall 1'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (72, 101)
            wall_instance.wh = (16, 38)
            objects_map['fixed wall 2'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (8, 101)
            wall_instance.wh = (16, 38)
            objects_map['fixed wall 3'] = wall_instance
            number_of_walls = 4
            i = 0
            while(objects_map.get(f"fixed wall {number_of_walls + i}")!= None):
                objects_map.pop(f"fixed wall {number_of_walls + i}")
                i += 1
        elif ram_state[28] == 13:
            wall_instance = LavaWall()
            wall_instance.xy = (72, 61)
            wall_instance.wh = (16, 37)
            objects_map['lava wall 0'] = wall_instance
            number_of_lava_walls = 1
            i = 0
            while(objects_map.get(f"fixed wall {number_of_lava_walls + i}")!= None):
                objects_map.pop(f"fixed wall {number_of_lava_walls + i}")
                i += 1
            wall_instance = Wall()
            wall_instance.xy = (8, 21)
            wall_instance.wh = (152, 38)
            objects_map['fixed wall 0'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (136, 101)
            wall_instance.wh = (24, 38)
            objects_map['fixed wall 1'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (8, 101)
            wall_instance.wh = (16, 38)
            objects_map['fixed wall 2'] = wall_instance
            number_of_walls = 3
            i = 0
            while(objects_map.get(f"fixed wall {number_of_walls + i}")!= None):
                objects_map.pop(f"fixed wall {number_of_walls + i}")
                i += 1
        elif ram_state[28] == 14:
            number_of_lava_walls = 0
            i = 0
            while(objects_map.get(f"fixed wall {number_of_lava_walls + i}")!= None):
                objects_map.pop(f"fixed wall {number_of_lava_walls + i}")
                i += 1
            wall_instance = Wall()
            wall_instance.xy = (8, 21)
            wall_instance.wh = (152, 38)
            objects_map['fixed wall 0'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (120, 101)
            wall_instance.wh = (40, 38)
            objects_map['fixed wall 1'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (72, 101)
            wall_instance.wh = (16, 38)
            objects_map['fixed wall 2'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (8, 101)
            wall_instance.wh = (32, 38)
            objects_map['fixed wall 3'] = wall_instance
            number_of_walls = 4
            i = 0
            while(objects_map.get(f"fixed wall {number_of_walls + i}")!= None):
                objects_map.pop(f"fixed wall {number_of_walls + i}")
                i += 1
        elif ram_state[28] == 15:
            number_of_lava_walls = 0
            i = 0
            while(objects_map.get(f"fixed wall {number_of_lava_walls + i}")!= None):
                objects_map.pop(f"fixed wall {number_of_lava_walls + i}")
                i += 1
            wall_instance = Wall()
            wall_instance.xy = (8, 21)
            wall_instance.wh = (152, 38)
            objects_map['fixed wall 0'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (8, 101)
            wall_instance.wh = (152, 38)
            objects_map['fixed wall 1'] = wall_instance
            number_of_walls = 2
            i = 0
            while(objects_map.get(f"fixed wall {number_of_walls + i}")!= None):
                objects_map.pop(f"fixed wall {number_of_walls + i}")
                i += 1

    elif ram_state[117] == 10:
        if ram_state[28] == 0:
            wall_instance = LavaWall()
            wall_instance.xy = (140, 61)
            wall_instance.wh = (20, 37)
            objects_map['lava wall 0'] = wall_instance
            wall_instance = LavaWall()
            wall_instance.xy = (8, 61)
            wall_instance.wh = (12, 37)
            objects_map['lava wall 1'] = wall_instance
            number_of_lava_walls = 2
            i = 0
            while(objects_map.get(f"fixed wall {number_of_lava_walls + i}")!= None):
                objects_map.pop(f"fixed wall {number_of_lava_walls + i}")
                i += 1
            wall_instance = Wall()
            wall_instance.xy = (136, 21)
            wall_instance.wh = (24, 38)
            objects_map['fixed wall 0'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (8, 21)
            wall_instance.wh = (16, 38)
            objects_map['fixed wall 1'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (88, 101)
            wall_instance.wh = (72, 38)
            objects_map['fixed wall 2'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (8, 101)
            wall_instance.wh = (64, 38)
            objects_map['fixed wall 3'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (140, 61)
            wall_instance.wh = (20, 37)
            objects_map['fixed wall 4'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (8, 61)
            wall_instance.wh = (12, 37)
            objects_map['fixed wall 5'] = wall_instance
            number_of_walls = 6
            i = 0
            while(objects_map.get(f"fixed wall {number_of_walls + i}")!= None):
                objects_map.pop(f"fixed wall {number_of_walls + i}")
                i += 1
        elif ram_state[28] == 1:
            wall_instance = LavaWall()
            wall_instance.xy = (88, 61)
            wall_instance.wh = (72, 37)
            objects_map['lava wall 0'] = wall_instance
            wall_instance = LavaWall()
            wall_instance.xy = (8, 61)
            wall_instance.wh = (64, 37)
            objects_map['lava wall 1'] = wall_instance
            number_of_lava_walls = 2
            i = 0
            while(objects_map.get(f"fixed wall {number_of_lava_walls + i}")!= None):
                objects_map.pop(f"fixed wall {number_of_lava_walls + i}")
                i += 1
            wall_instance = Wall()
            wall_instance.xy = (88, 21)
            wall_instance.wh = (72, 38)
            objects_map['fixed wall 0'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (8, 21)
            wall_instance.wh = (64, 38)
            objects_map['fixed wall 1'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (112, 101)
            wall_instance.wh = (48, 38)
            objects_map['fixed wall 2'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (8, 101)
            wall_instance.wh = (40, 38)
            objects_map['fixed wall 3'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (88, 61)
            wall_instance.wh = (72, 37)
            objects_map['fixed wall 4'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (8, 61)
            wall_instance.wh = (64, 37)
            objects_map['fixed wall 5'] = wall_instance
            number_of_walls = 6
            i = 0
            while(objects_map.get(f"fixed wall {number_of_walls + i}")!= None):
                objects_map.pop(f"fixed wall {number_of_walls + i}")
                i += 1
        elif ram_state[28] == 2:
            wall_instance = LavaWall()
            wall_instance.xy = (144, 61)
            wall_instance.wh = (16, 37)
            objects_map['lava wall 0'] = wall_instance
            wall_instance = LavaWall()
            wall_instance.xy = (72, 61)
            wall_instance.wh = (16, 37)
            objects_map['lava wall 1'] = wall_instance
            wall_instance = LavaWall()
            wall_instance.xy = (8, 61)
            wall_instance.wh = (8, 37)
            objects_map['lava wall 2'] = wall_instance
            number_of_lava_walls = 3
            i = 0
            while(objects_map.get(f"fixed wall {number_of_lava_walls + i}")!= None):
                objects_map.pop(f"fixed wall {number_of_lava_walls + i}")
                i += 1
            wall_instance = Wall()
            wall_instance.xy = (112, 21)
            wall_instance.wh = (48, 38)
            objects_map['fixed wall 0'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (8, 21)
            wall_instance.wh = (40, 38)
            objects_map['fixed wall 1'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (140, 101)
            wall_instance.wh = (20, 38)
            objects_map['fixed wall 2'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (28, 101)
            wall_instance.wh = (104, 38)
            objects_map['fixed wall 3'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (8, 101)
            wall_instance.wh = (12, 38)
            objects_map['fixed wall 4'] = wall_instance
            number_of_walls = 5
            i = 0
            while(objects_map.get(f"fixed wall {number_of_walls + i}")!= None):
                objects_map.pop(f"fixed wall {number_of_walls + i}")
                i += 1
        elif ram_state[28] == 3:
            wall_instance = LavaWall()
            wall_instance.xy = (144, 61)
            wall_instance.wh = (16, 37)
            objects_map['lava wall 0'] = wall_instance
            wall_instance = LavaWall()
            wall_instance.xy = (8, 61)
            wall_instance.wh = (8, 37)
            objects_map['lava wall 1'] = wall_instance
            number_of_lava_walls = 2
            i = 0
            while(objects_map.get(f"fixed wall {number_of_lava_walls + i}")!= None):
                objects_map.pop(f"fixed wall {number_of_lava_walls + i}")
                i += 1
            wall_instance = Wall()
            wall_instance.xy = (140, 21)
            wall_instance.wh = (20, 38)
            objects_map['fixed wall 0'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (28, 21)
            wall_instance.wh = (104, 38)
            objects_map['fixed wall 1'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (8, 21)
            wall_instance.wh = (12, 38)
            objects_map['fixed wall 2'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (88, 101)
            wall_instance.wh = (72, 38)
            objects_map['fixed wall 3'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (8, 101)
            wall_instance.wh = (64, 38)
            objects_map['fixed wall 4'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (144, 61)
            wall_instance.wh = (16, 37)
            objects_map['fixed wall 5'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (8, 61)
            wall_instance.wh = (8, 37)
            objects_map['fixed wall 6'] = wall_instance
            number_of_walls = 7
            i = 0
            while(objects_map.get(f"fixed wall {number_of_walls + i}")!= None):
                objects_map.pop(f"fixed wall {number_of_walls + i}")
                i += 1
        elif ram_state[28] == 4:
            wall_instance = LavaWall()
            wall_instance.xy = (144, 61)
            wall_instance.wh = (16, 37)
            objects_map['lava wall 0'] = wall_instance
            wall_instance = LavaWall()
            wall_instance.xy = (92, 61)
            wall_instance.wh = (12, 37)
            objects_map['lava wall 1'] = wall_instance
            wall_instance = LavaWall()
            wall_instance.xy = (56, 61)
            wall_instance.wh = (12, 37)
            objects_map['lava wall 2'] = wall_instance
            wall_instance = LavaWall()
            wall_instance.xy = (8, 61)
            wall_instance.wh = (8, 37)
            objects_map['lava wall 3'] = wall_instance
            number_of_lava_walls = 4
            i = 0
            while(objects_map.get(f"fixed wall {number_of_lava_walls + i}")!= None):
                objects_map.pop(f"fixed wall {number_of_lava_walls + i}")
                i += 1
            wall_instance = Wall()
            wall_instance.xy = (88, 21)
            wall_instance.wh = (72, 38)
            objects_map['fixed wall 0'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (8, 21)
            wall_instance.wh = (64, 38)
            objects_map['fixed wall 1'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (140, 101)
            wall_instance.wh = (20, 38)
            objects_map['fixed wall 2'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (116, 101)
            wall_instance.wh = (16, 38)
            objects_map['fixed wall 3'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (84, 101)
            wall_instance.wh = (24, 38)
            objects_map['fixed wall 4'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (52, 101)
            wall_instance.wh = (24, 38)
            objects_map['fixed wall 5'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (28, 101)
            wall_instance.wh = (16, 38)
            objects_map['fixed wall 6'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (8, 101)
            wall_instance.wh = (12, 38)
            objects_map['fixed wall 7'] = wall_instance
            number_of_walls = 8
            i = 0
            while(objects_map.get(f"fixed wall {number_of_walls + i}")!= None):
                objects_map.pop(f"fixed wall {number_of_walls + i}")
                i += 1
        elif ram_state[28] == 5:
            wall_instance = LavaWall()
            wall_instance.xy = (140, 61)
            wall_instance.wh = (20, 37)
            objects_map['lava wall 0'] = wall_instance
            wall_instance = LavaWall()
            wall_instance.xy = (120, 61)
            wall_instance.wh = (12, 37)
            objects_map['lava wall 1'] = wall_instance
            wall_instance = LavaWall()
            wall_instance.xy = (28, 61)
            wall_instance.wh = (12, 37)
            objects_map['lava wall 2'] = wall_instance
            wall_instance = LavaWall()
            wall_instance.xy = (8, 61)
            wall_instance.wh = (12, 37)
            objects_map['lava wall 3'] = wall_instance
            number_of_lava_walls = 4
            i = 0
            while(objects_map.get(f"fixed wall {number_of_lava_walls + i}")!= None):
                objects_map.pop(f"fixed wall {number_of_lava_walls + i}")
                i += 1
            wall_instance = Wall()
            wall_instance.xy = (140, 21)
            wall_instance.wh = (20, 38)
            objects_map['fixed wall 0'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (116, 21)
            wall_instance.wh = (16, 38)
            objects_map['fixed wall 1'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (84, 21)
            wall_instance.wh = (24, 38)
            objects_map['fixed wall 2'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (52, 21)
            wall_instance.wh = (24, 38)
            objects_map['fixed wall 3'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (28, 21)
            wall_instance.wh = (16, 38)
            objects_map['fixed wall 4'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (8, 21)
            wall_instance.wh = (12, 38)
            objects_map['fixed wall 5'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (140, 101)
            wall_instance.wh = (20, 38)
            objects_map['fixed wall 6'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (28, 101)
            wall_instance.wh = (104, 38)
            objects_map['fixed wall 7'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (8, 101)
            wall_instance.wh = (12, 38)
            objects_map['fixed wall 8'] = wall_instance
            number_of_walls = 9
            i = 0
            while(objects_map.get(f"fixed wall {number_of_walls + i}")!= None):
                objects_map.pop(f"fixed wall {number_of_walls + i}")
                i += 1
        elif ram_state[28] == 6:
            wall_instance = LavaWall()
            wall_instance.xy = (144, 61)
            wall_instance.wh = (16, 37)
            objects_map['lava wall 0'] = wall_instance
            wall_instance = LavaWall()
            wall_instance.xy = (8, 61)
            wall_instance.wh = (8, 37)
            objects_map['lava wall 1'] = wall_instance
            number_of_lava_walls = 2
            i = 0
            while(objects_map.get(f"fixed wall {number_of_lava_walls + i}")!= None):
                objects_map.pop(f"fixed wall {number_of_lava_walls + i}")
                i += 1
            wall_instance = Wall()
            wall_instance.xy = (140, 21)
            wall_instance.wh = (20, 38)
            objects_map['fixed wall 0'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (28, 21)
            wall_instance.wh = (104, 38)
            objects_map['fixed wall 1'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (8, 21)
            wall_instance.wh = (12, 38)
            objects_map['fixed wall 2'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (112, 101)
            wall_instance.wh = (48, 38)
            objects_map['fixed wall 3'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (8, 101)
            wall_instance.wh = (40, 38)
            objects_map['fixed wall 4'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (144, 61)
            wall_instance.wh = (16, 37)
            objects_map['fixed wall 5'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (8, 61)
            wall_instance.wh = (8, 37)
            objects_map['fixed wall 6'] = wall_instance
            number_of_walls = 7
            i = 0
            while(objects_map.get(f"fixed wall {number_of_walls + i}")!= None):
                objects_map.pop(f"fixed wall {number_of_walls + i}")
                i += 1
        elif ram_state[28] == 7:
            wall_instance = LavaWall()
            wall_instance.xy = (88, 61)
            wall_instance.wh = (72, 37)
            objects_map['lava wall 0'] = wall_instance
            wall_instance = LavaWall()
            wall_instance.xy = (8, 61)
            wall_instance.wh = (64, 37)
            objects_map['lava wall 1'] = wall_instance
            number_of_lava_walls = 2
            i = 0
            while(objects_map.get(f"fixed wall {number_of_lava_walls + i}")!= None):
                objects_map.pop(f"fixed wall {number_of_lava_walls + i}")
                i += 1
            wall_instance = Wall()
            wall_instance.xy = (112, 21)
            wall_instance.wh = (48, 38)
            objects_map['fixed wall 0'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (8, 21)
            wall_instance.wh = (40, 38)
            objects_map['fixed wall 1'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (144, 101)
            wall_instance.wh = (16, 38)
            objects_map['fixed wall 2'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (8, 101)
            wall_instance.wh = (8, 38)
            objects_map['fixed wall 3'] = wall_instance
            number_of_walls = 4
            i = 0
            while(objects_map.get(f"fixed wall {number_of_walls + i}")!= None):
                objects_map.pop(f"fixed wall {number_of_walls + i}")
                i += 1
        elif ram_state[28] == 8:
            wall_instance = LavaWall()
            wall_instance.xy = (104, 61)
            wall_instance.wh = (56, 37)
            objects_map['lava wall 0'] = wall_instance
            wall_instance = LavaWall()
            wall_instance.xy = (72, 61)
            wall_instance.wh = (16, 37)
            objects_map['lava wall 1'] = wall_instance
            wall_instance = LavaWall()
            wall_instance.xy = (8, 61)
            wall_instance.wh = (48, 37)
            objects_map['lava wall 2'] = wall_instance
            number_of_lava_walls = 3
            i = 0
            while(objects_map.get(f"fixed wall {number_of_lava_walls + i}")!= None):
                objects_map.pop(f"fixed wall {number_of_lava_walls + i}")
                i += 1
            wall_instance = Wall()
            wall_instance.xy = (144, 21)
            wall_instance.wh = (16, 38)
            objects_map['fixed wall 0'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (8, 21)
            wall_instance.wh = (8, 38)
            objects_map['fixed wall 1'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (144, 101)
            wall_instance.wh = (16, 38)
            objects_map['fixed wall 2'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (8, 101)
            wall_instance.wh = (8, 38)
            objects_map['fixed wall 3'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (104, 61)
            wall_instance.wh = (56, 37)
            objects_map['fixed wall 4'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (72, 61)
            wall_instance.wh = (16, 37)
            objects_map['fixed wall 5'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (8, 61)
            wall_instance.wh = (48, 37)
            objects_map['fixed wall 6'] = wall_instance
            number_of_walls = 7
            i = 0
            while(objects_map.get(f"fixed wall {number_of_walls + i}")!= None):
                objects_map.pop(f"fixed wall {number_of_walls + i}")
                i += 1
        elif ram_state[28] == 9:
            wall_instance = LavaWall()
            wall_instance.xy = (88, 61)
            wall_instance.wh = (72, 37)
            objects_map['lava wall 0'] = wall_instance
            wall_instance = LavaWall()
            wall_instance.xy = (8, 61)
            wall_instance.wh = (64, 37)
            objects_map['lava wall 1'] = wall_instance
            number_of_lava_walls = 2
            i = 0
            while(objects_map.get(f"fixed wall {number_of_lava_walls + i}")!= None):
                objects_map.pop(f"fixed wall {number_of_lava_walls + i}")
                i += 1
            wall_instance = Wall()
            wall_instance.xy = (144, 21)
            wall_instance.wh = (16, 38)
            objects_map['fixed wall 0'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (8, 21)
            wall_instance.wh = (8, 38)
            objects_map['fixed wall 1'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (112, 101)
            wall_instance.wh = (48, 38)
            objects_map['fixed wall 2'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (8, 101)
            wall_instance.wh = (40, 38)
            objects_map['fixed wall 3'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (88, 61)
            wall_instance.wh = (72, 37)
            objects_map['fixed wall 4'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (8, 61)
            wall_instance.wh = (64, 37)
            objects_map['fixed wall 5'] = wall_instance
            number_of_walls = 6
            i = 0
            while(objects_map.get(f"fixed wall {number_of_walls + i}")!= None):
                objects_map.pop(f"fixed wall {number_of_walls + i}")
                i += 1
        elif ram_state[28] == 10:
            number_of_lava_walls = 0
            i = 0
            while(objects_map.get(f"fixed wall {number_of_lava_walls + i}")!= None):
                objects_map.pop(f"fixed wall {number_of_lava_walls + i}")
                i += 1
            wall_instance = Wall()
            wall_instance.xy = (112, 21)
            wall_instance.wh = (48, 38)
            objects_map['fixed wall 0'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (8, 21)
            wall_instance.wh = (40, 38)
            objects_map['fixed wall 1'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (136, 101)
            wall_instance.wh = (24, 38)
            objects_map['fixed wall 2'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (68, 101)
            wall_instance.wh = (24, 38)
            objects_map['fixed wall 3'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (8, 101)
            wall_instance.wh = (16, 38)
            objects_map['fixed wall 4'] = wall_instance
            number_of_walls = 5
            i = 0
            while(objects_map.get(f"fixed wall {number_of_walls + i}")!= None):
                objects_map.pop(f"fixed wall {number_of_walls + i}")
                i += 1
        elif ram_state[28] == 11:
            number_of_lava_walls = 0
            i = 0
            while(objects_map.get(f"fixed wall {number_of_lava_walls + i}")!= None):
                objects_map.pop(f"fixed wall {number_of_lava_walls + i}")
                i += 1
            wall_instance = Wall()
            wall_instance.xy = (8, 21)
            wall_instance.wh = (152, 38)
            objects_map['fixed wall 0'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (128, 101)
            wall_instance.wh = (32, 38)
            objects_map['fixed wall 1'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (72, 101)
            wall_instance.wh = (16, 38)
            objects_map['fixed wall 2'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (8, 101)
            wall_instance.wh = (24, 38)
            objects_map['fixed wall 3'] = wall_instance
            number_of_walls = 4
            i = 0
            while(objects_map.get(f"fixed wall {number_of_walls + i}")!= None):
                objects_map.pop(f"fixed wall {number_of_walls + i}")
                i += 1
        elif ram_state[28] == 12:
            wall_instance = LavaWall()
            wall_instance.xy = (72, 61)
            wall_instance.wh = (16, 37)
            objects_map['lava wall 0'] = wall_instance
            number_of_lava_walls = 1
            i = 0
            while(objects_map.get(f"fixed wall {number_of_lava_walls + i}")!= None):
                objects_map.pop(f"fixed wall {number_of_lava_walls + i}")
                i += 1
            wall_instance = Wall()
            wall_instance.xy = (8, 21)
            wall_instance.wh = (152, 38)
            objects_map['fixed wall 0'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (136, 101)
            wall_instance.wh = (24, 38)
            objects_map['fixed wall 1'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (8, 101)
            wall_instance.wh = (16, 38)
            objects_map['fixed wall 2'] = wall_instance
            number_of_walls = 3
            i = 0
            while(objects_map.get(f"fixed wall {number_of_walls + i}")!= None):
                objects_map.pop(f"fixed wall {number_of_walls + i}")
                i += 1
        elif ram_state[28] == 13:
            number_of_lava_walls = 0
            i = 0
            while(objects_map.get(f"fixed wall {number_of_lava_walls + i}")!= None):
                objects_map.pop(f"fixed wall {number_of_lava_walls + i}")
                i += 1
            wall_instance = Wall()
            wall_instance.xy = (8, 21)
            wall_instance.wh = (152, 38)
            objects_map['fixed wall 0'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (112, 101)
            wall_instance.wh = (48, 38)
            objects_map['fixed wall 1'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (64, 101)
            wall_instance.wh = (32, 38)
            objects_map['fixed wall 2'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (8, 101)
            wall_instance.wh = (40, 38)
            objects_map['fixed wall 3'] = wall_instance
            number_of_walls = 4
            i = 0
            while(objects_map.get(f"fixed wall {number_of_walls + i}")!= None):
                objects_map.pop(f"fixed wall {number_of_walls + i}")
                i += 1
        elif ram_state[28] == 14:
            number_of_lava_walls = 0
            i = 0
            while(objects_map.get(f"fixed wall {number_of_lava_walls + i}")!= None):
                objects_map.pop(f"fixed wall {number_of_lava_walls + i}")
                i += 1
            wall_instance = Wall()
            wall_instance.xy = (8, 21)
            wall_instance.wh = (152, 38)
            objects_map['fixed wall 0'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (136, 101)
            wall_instance.wh = (24, 38)
            objects_map['fixed wall 1'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (48, 101)
            wall_instance.wh = (64, 38)
            objects_map['fixed wall 2'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (8, 101)
            wall_instance.wh = (16, 38)
            objects_map['fixed wall 3'] = wall_instance
            number_of_walls = 4
            i = 0
            while(objects_map.get(f"fixed wall {number_of_walls + i}")!= None):
                objects_map.pop(f"fixed wall {number_of_walls + i}")
                i += 1
        elif ram_state[28] == 15:
            number_of_lava_walls = 0
            i = 0
            while(objects_map.get(f"fixed wall {number_of_lava_walls + i}")!= None):
                objects_map.pop(f"fixed wall {number_of_lava_walls + i}")
                i += 1
            wall_instance = Wall()
            wall_instance.xy = (8, 21)
            wall_instance.wh = (152, 38)
            objects_map['fixed wall 0'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (8, 101)
            wall_instance.wh = (152, 38)
            objects_map['fixed wall 1'] = wall_instance
            number_of_walls = 2
            i = 0
            while(objects_map.get(f"fixed wall {number_of_walls + i}")!= None):
                objects_map.pop(f"fixed wall {number_of_walls + i}")
                i += 1

    elif ram_state[117] == 11:
        if ram_state[28] == 0:
            wall_instance = LavaWall()
            wall_instance.xy = (132, 61)
            wall_instance.wh = (28, 37)
            objects_map['lava wall 0'] = wall_instance
            wall_instance = LavaWall()
            wall_instance.xy = (8, 61)
            wall_instance.wh = (20, 37)
            objects_map['lava wall 1'] = wall_instance
            number_of_lava_walls = 2
            i = 0
            while(objects_map.get(f"fixed wall {number_of_lava_walls + i}")!= None):
                objects_map.pop(f"fixed wall {number_of_lava_walls + i}")
                i += 1
            wall_instance = Wall()
            wall_instance.xy = (136, 21)
            wall_instance.wh = (24, 38)
            objects_map['fixed wall 0'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (8, 21)
            wall_instance.wh = (16, 38)
            objects_map['fixed wall 1'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (88, 101)
            wall_instance.wh = (72, 38)
            objects_map['fixed wall 2'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (8, 101)
            wall_instance.wh = (64, 38)
            objects_map['fixed wall 3'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (132, 61)
            wall_instance.wh = (28, 37)
            objects_map['fixed wall 4'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (8, 61)
            wall_instance.wh = (20, 37)
            objects_map['fixed wall 5'] = wall_instance
            number_of_walls = 6
            i = 0
            while(objects_map.get(f"fixed wall {number_of_walls + i}")!= None):
                objects_map.pop(f"fixed wall {number_of_walls + i}")
                i += 1
        elif ram_state[28] == 1:
            wall_instance = LavaWall()
            wall_instance.xy = (136, 61)
            wall_instance.wh = (24, 37)
            objects_map['lava wall 0'] = wall_instance
            wall_instance = LavaWall()
            wall_instance.xy = (8, 61)
            wall_instance.wh = (16, 37)
            objects_map['lava wall 1'] = wall_instance
            number_of_lava_walls = 2
            i = 0
            while(objects_map.get(f"fixed wall {number_of_lava_walls + i}")!= None):
                objects_map.pop(f"fixed wall {number_of_lava_walls + i}")
                i += 1
            wall_instance = Wall()
            wall_instance.xy = (88, 21)
            wall_instance.wh = (72, 38)
            objects_map['fixed wall 0'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (8, 21)
            wall_instance.wh = (64, 38)
            objects_map['fixed wall 1'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (132, 101)
            wall_instance.wh = (28, 38)
            objects_map['fixed wall 2'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (36, 101)
            wall_instance.wh = (88, 38)
            objects_map['fixed wall 3'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (8, 101)
            wall_instance.wh = (20, 38)
            objects_map['fixed wall 4'] = wall_instance
            number_of_walls = 5
            i = 0
            while(objects_map.get(f"fixed wall {number_of_walls + i}")!= None):
                objects_map.pop(f"fixed wall {number_of_walls + i}")
                i += 1
        elif ram_state[28] == 2:
            wall_instance = LavaWall()
            wall_instance.xy = (144, 61)
            wall_instance.wh = (16, 37)
            objects_map['lava wall 0'] = wall_instance
            wall_instance = LavaWall()
            wall_instance.xy = (8, 61)
            wall_instance.wh = (8, 37)
            objects_map['lava wall 1'] = wall_instance
            number_of_lava_walls = 2
            i = 0
            while(objects_map.get(f"fixed wall {number_of_lava_walls + i}")!= None):
                objects_map.pop(f"fixed wall {number_of_lava_walls + i}")
                i += 1
            wall_instance = Wall()
            wall_instance.xy = (132, 21)
            wall_instance.wh = (28, 38)
            objects_map['fixed wall 0'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (36, 21)
            wall_instance.wh = (88, 38)
            objects_map['fixed wall 1'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (8, 21)
            wall_instance.wh = (20, 38)
            objects_map['fixed wall 2'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (8, 101)
            wall_instance.wh = (152, 38)
            objects_map['fixed wall 3'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (144, 61)
            wall_instance.wh = (16, 37)
            objects_map['fixed wall 4'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (8, 61)
            wall_instance.wh = (8, 37)
            objects_map['fixed wall 5'] = wall_instance
            number_of_walls = 6
            i = 0
            while(objects_map.get(f"fixed wall {number_of_walls + i}")!= None):
                objects_map.pop(f"fixed wall {number_of_walls + i}")
                i += 1
        elif ram_state[28] == 3:
            wall_instance = LavaWall()
            wall_instance.xy = (144, 61)
            wall_instance.wh = (16, 37)
            objects_map['lava wall 0'] = wall_instance
            wall_instance = LavaWall()
            wall_instance.xy = (8, 61)
            wall_instance.wh = (8, 37)
            objects_map['lava wall 1'] = wall_instance
            number_of_lava_walls = 2
            i = 0
            while(objects_map.get(f"fixed wall {number_of_lava_walls + i}")!= None):
                objects_map.pop(f"fixed wall {number_of_lava_walls + i}")
                i += 1
            wall_instance = Wall()
            wall_instance.xy = (8, 21)
            wall_instance.wh = (152, 38)
            objects_map['fixed wall 0'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (120, 101)
            wall_instance.wh = (40, 38)
            objects_map['fixed wall 1'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (48, 101)
            wall_instance.wh = (64, 38)
            objects_map['fixed wall 2'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (8, 101)
            wall_instance.wh = (32, 38)
            objects_map['fixed wall 3'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (144, 61)
            wall_instance.wh = (16, 37)
            objects_map['fixed wall 4'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (8, 61)
            wall_instance.wh = (8, 37)
            objects_map['fixed wall 5'] = wall_instance
            number_of_walls = 6
            i = 0
            while(objects_map.get(f"fixed wall {number_of_walls + i}")!= None):
                objects_map.pop(f"fixed wall {number_of_walls + i}")
                i += 1
        elif ram_state[28] == 4:
            wall_instance = LavaWall()
            wall_instance.xy = (144, 61)
            wall_instance.wh = (16, 37)
            objects_map['lava wall 0'] = wall_instance
            wall_instance = LavaWall()
            wall_instance.xy = (8, 61)
            wall_instance.wh = (8, 37)
            objects_map['lava wall 1'] = wall_instance
            number_of_lava_walls = 2
            i = 0
            while(objects_map.get(f"fixed wall {number_of_lava_walls + i}")!= None):
                objects_map.pop(f"fixed wall {number_of_lava_walls + i}")
                i += 1
            wall_instance = Wall()
            wall_instance.xy = (120, 21)
            wall_instance.wh = (40, 38)
            objects_map['fixed wall 0'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (48, 21)
            wall_instance.wh = (64, 38)
            objects_map['fixed wall 1'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (8, 21)
            wall_instance.wh = (32, 38)
            objects_map['fixed wall 2'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (88, 101)
            wall_instance.wh = (72, 38)
            objects_map['fixed wall 3'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (8, 101)
            wall_instance.wh = (64, 38)
            objects_map['fixed wall 4'] = wall_instance
            number_of_walls = 5
            i = 0
            while(objects_map.get(f"fixed wall {number_of_walls + i}")!= None):
                objects_map.pop(f"fixed wall {number_of_walls + i}")
                i += 1
        elif ram_state[28] == 5:
            wall_instance = LavaWall()
            wall_instance.xy = (120, 61)
            wall_instance.wh = (40, 37)
            objects_map['lava wall 0'] = wall_instance
            wall_instance = LavaWall()
            wall_instance.xy = (8, 61)
            wall_instance.wh = (32, 37)
            objects_map['lava wall 1'] = wall_instance
            number_of_lava_walls = 2
            i = 0
            while(objects_map.get(f"fixed wall {number_of_lava_walls + i}")!= None):
                objects_map.pop(f"fixed wall {number_of_lava_walls + i}")
                i += 1
            wall_instance = Wall()
            wall_instance.xy = (88, 21)
            wall_instance.wh = (72, 38)
            objects_map['fixed wall 0'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (8, 21)
            wall_instance.wh = (64, 38)
            objects_map['fixed wall 1'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (144, 101)
            wall_instance.wh = (16, 38)
            objects_map['fixed wall 2'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (48, 101)
            wall_instance.wh = (64, 38)
            objects_map['fixed wall 3'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (8, 101)
            wall_instance.wh = (8, 38)
            objects_map['fixed wall 4'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (120, 61)
            wall_instance.wh = (40, 37)
            objects_map['fixed wall 5'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (8, 61)
            wall_instance.wh = (32, 37)
            objects_map['fixed wall 6'] = wall_instance
            number_of_walls = 7
            i = 0
            while(objects_map.get(f"fixed wall {number_of_walls + i}")!= None):
                objects_map.pop(f"fixed wall {number_of_walls + i}")
                i += 1
        elif ram_state[28] == 6:
            wall_instance = LavaWall()
            wall_instance.xy = (128, 61)
            wall_instance.wh = (32, 37)
            objects_map['lava wall 0'] = wall_instance
            wall_instance = LavaWall()
            wall_instance.xy = (40, 61)
            wall_instance.wh = (80, 37)
            objects_map['lava wall 1'] = wall_instance
            wall_instance = LavaWall()
            wall_instance.xy = (8, 61)
            wall_instance.wh = (24, 37)
            objects_map['lava wall 2'] = wall_instance
            number_of_lava_walls = 3
            i = 0
            while(objects_map.get(f"fixed wall {number_of_lava_walls + i}")!= None):
                objects_map.pop(f"fixed wall {number_of_lava_walls + i}")
                i += 1
            wall_instance = Wall()
            wall_instance.xy = (144, 21)
            wall_instance.wh = (16, 38)
            objects_map['fixed wall 0'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (48, 21)
            wall_instance.wh = (64, 38)
            objects_map['fixed wall 1'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (8, 21)
            wall_instance.wh = (8, 38)
            objects_map['fixed wall 2'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (136, 101)
            wall_instance.wh = (24, 38)
            objects_map['fixed wall 3'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (8, 101)
            wall_instance.wh = (16, 38)
            objects_map['fixed wall 4'] = wall_instance
            number_of_walls = 5
            i = 0
            while(objects_map.get(f"fixed wall {number_of_walls + i}")!= None):
                objects_map.pop(f"fixed wall {number_of_walls + i}")
                i += 1
        elif ram_state[28] == 7:
            wall_instance = LavaWall()
            wall_instance.xy = (144, 61)
            wall_instance.wh = (16, 37)
            objects_map['lava wall 0'] = wall_instance
            wall_instance = LavaWall()
            wall_instance.xy = (8, 61)
            wall_instance.wh = (8, 37)
            objects_map['lava wall 1'] = wall_instance
            number_of_lava_walls = 2
            i = 0
            while(objects_map.get(f"fixed wall {number_of_lava_walls + i}")!= None):
                objects_map.pop(f"fixed wall {number_of_lava_walls + i}")
                i += 1
            wall_instance = Wall()
            wall_instance.xy = (136, 21)
            wall_instance.wh = (24, 38)
            objects_map['fixed wall 0'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (8, 21)
            wall_instance.wh = (16, 38)
            objects_map['fixed wall 1'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (8, 101)
            wall_instance.wh = (152, 38)
            objects_map['fixed wall 2'] = wall_instance
            number_of_walls = 3
            i = 0
            while(objects_map.get(f"fixed wall {number_of_walls + i}")!= None):
                objects_map.pop(f"fixed wall {number_of_walls + i}")
                i += 1
        elif ram_state[28] == 8:
            wall_instance = LavaWall()
            wall_instance.xy = (144, 61)
            wall_instance.wh = (16, 37)
            objects_map['lava wall 0'] = wall_instance
            wall_instance = LavaWall()
            wall_instance.xy = (60, 61)
            wall_instance.wh = (40, 37)
            objects_map['lava wall 1'] = wall_instance
            wall_instance = LavaWall()
            wall_instance.xy = (8, 61)
            wall_instance.wh = (8, 37)
            objects_map['lava wall 2'] = wall_instance
            number_of_lava_walls = 3
            i = 0
            while(objects_map.get(f"fixed wall {number_of_lava_walls + i}")!= None):
                objects_map.pop(f"fixed wall {number_of_lava_walls + i}")
                i += 1
            wall_instance = Wall()
            wall_instance.xy = (8, 21)
            wall_instance.wh = (152, 38)
            objects_map['fixed wall 0'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (112, 101)
            wall_instance.wh = (48, 38)
            objects_map['fixed wall 1'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (8, 101)
            wall_instance.wh = (40, 38)
            objects_map['fixed wall 2'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (144, 61)
            wall_instance.wh = (16, 37)
            objects_map['fixed wall 3'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (60, 61)
            wall_instance.wh = (40, 37)
            objects_map['fixed wall 4'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (8, 61)
            wall_instance.wh = (8, 37)
            objects_map['fixed wall 5'] = wall_instance
            number_of_walls = 6
            i = 0
            while(objects_map.get(f"fixed wall {number_of_walls + i}")!= None):
                objects_map.pop(f"fixed wall {number_of_walls + i}")
                i += 1
        elif ram_state[28] == 9:
            wall_instance = LavaWall()
            wall_instance.xy = (144, 61)
            wall_instance.wh = (16, 37)
            objects_map['lava wall 0'] = wall_instance
            wall_instance = LavaWall()
            wall_instance.xy = (56, 61)
            wall_instance.wh = (48, 37)
            objects_map['lava wall 1'] = wall_instance
            wall_instance = LavaWall()
            wall_instance.xy = (8, 61)
            wall_instance.wh = (8, 37)
            objects_map['lava wall 2'] = wall_instance
            number_of_lava_walls = 3
            i = 0
            while(objects_map.get(f"fixed wall {number_of_lava_walls + i}")!= None):
                objects_map.pop(f"fixed wall {number_of_lava_walls + i}")
                i += 1
            wall_instance = Wall()
            wall_instance.xy = (112, 21)
            wall_instance.wh = (48, 38)
            objects_map['fixed wall 0'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (8, 21)
            wall_instance.wh = (40, 38)
            objects_map['fixed wall 1'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (112, 101)
            wall_instance.wh = (48, 38)
            objects_map['fixed wall 2'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (8, 101)
            wall_instance.wh = (40, 38)
            objects_map['fixed wall 3'] = wall_instance
            number_of_walls = 4
            i = 0
            while(objects_map.get(f"fixed wall {number_of_walls + i}")!= None):
                objects_map.pop(f"fixed wall {number_of_walls + i}")
                i += 1
        elif ram_state[28] == 10:
            wall_instance = LavaWall()
            wall_instance.xy = (72, 61)
            wall_instance.wh = (16, 37)
            objects_map['lava wall 0'] = wall_instance
            number_of_lava_walls = 1
            i = 0
            while(objects_map.get(f"fixed wall {number_of_lava_walls + i}")!= None):
                objects_map.pop(f"fixed wall {number_of_lava_walls + i}")
                i += 1
            wall_instance = Wall()
            wall_instance.xy = (112, 21)
            wall_instance.wh = (48, 38)
            objects_map['fixed wall 0'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (8, 21)
            wall_instance.wh = (40, 38)
            objects_map['fixed wall 1'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (136, 101)
            wall_instance.wh = (24, 38)
            objects_map['fixed wall 2'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (68, 101)
            wall_instance.wh = (24, 38)
            objects_map['fixed wall 3'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (8, 101)
            wall_instance.wh = (16, 38)
            objects_map['fixed wall 4'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (72, 61)
            wall_instance.wh = (16, 37)
            objects_map['fixed wall 5'] = wall_instance
            number_of_walls = 6
            i = 0
            while(objects_map.get(f"fixed wall {number_of_walls + i}")!= None):
                objects_map.pop(f"fixed wall {number_of_walls + i}")
                i += 1
        elif ram_state[28] == 11:
            number_of_lava_walls = 0
            i = 0
            while(objects_map.get(f"fixed wall {number_of_lava_walls + i}")!= None):
                objects_map.pop(f"fixed wall {number_of_lava_walls + i}")
                i += 1
            wall_instance = Wall()
            wall_instance.xy = (8, 21)
            wall_instance.wh = (152, 38)
            objects_map['fixed wall 0'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (144, 101)
            wall_instance.wh = (16, 38)
            objects_map['fixed wall 1'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (68, 101)
            wall_instance.wh = (24, 38)
            objects_map['fixed wall 2'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (8, 101)
            wall_instance.wh = (8, 38)
            objects_map['fixed wall 3'] = wall_instance
            number_of_walls = 4
            i = 0
            while(objects_map.get(f"fixed wall {number_of_walls + i}")!= None):
                objects_map.pop(f"fixed wall {number_of_walls + i}")
                i += 1
        elif ram_state[28] == 12:
            number_of_lava_walls = 0
            i = 0
            while(objects_map.get(f"fixed wall {number_of_lava_walls + i}")!= None):
                objects_map.pop(f"fixed wall {number_of_lava_walls + i}")
                i += 1
            wall_instance = Wall()
            wall_instance.xy = (8, 21)
            wall_instance.wh = (152, 38)
            objects_map['fixed wall 0'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (112, 101)
            wall_instance.wh = (48, 38)
            objects_map['fixed wall 1'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (8, 101)
            wall_instance.wh = (40, 38)
            objects_map['fixed wall 2'] = wall_instance
            number_of_walls = 3
            i = 0
            while(objects_map.get(f"fixed wall {number_of_walls + i}")!= None):
                objects_map.pop(f"fixed wall {number_of_walls + i}")
                i += 1
        elif ram_state[28] == 13:
            number_of_lava_walls = 0
            i = 0
            while(objects_map.get(f"fixed wall {number_of_lava_walls + i}")!= None):
                objects_map.pop(f"fixed wall {number_of_lava_walls + i}")
                i += 1
            wall_instance = Wall()
            wall_instance.xy = (8, 21)
            wall_instance.wh = (152, 38)
            objects_map['fixed wall 0'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (144, 101)
            wall_instance.wh = (16, 38)
            objects_map['fixed wall 1'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (72, 101)
            wall_instance.wh = (16, 38)
            objects_map['fixed wall 2'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (8, 101)
            wall_instance.wh = (8, 38)
            objects_map['fixed wall 3'] = wall_instance
            number_of_walls = 4
            i = 0
            while(objects_map.get(f"fixed wall {number_of_walls + i}")!= None):
                objects_map.pop(f"fixed wall {number_of_walls + i}")
                i += 1
        elif ram_state[28] == 14:
            wall_instance = LavaWall()
            wall_instance.xy = (72, 61)
            wall_instance.wh = (16, 37)
            objects_map['lava wall 0'] = wall_instance
            number_of_lava_walls = 1
            i = 0
            while(objects_map.get(f"fixed wall {number_of_lava_walls + i}")!= None):
                objects_map.pop(f"fixed wall {number_of_lava_walls + i}")
                i += 1
            wall_instance = Wall()
            wall_instance.xy = (8, 21)
            wall_instance.wh = (152, 38)
            objects_map['fixed wall 0'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (136, 101)
            wall_instance.wh = (24, 38)
            objects_map['fixed wall 1'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (8, 101)
            wall_instance.wh = (16, 38)
            objects_map['fixed wall 2'] = wall_instance
            number_of_walls = 3
            i = 0
            while(objects_map.get(f"fixed wall {number_of_walls + i}")!= None):
                objects_map.pop(f"fixed wall {number_of_walls + i}")
                i += 1
        elif ram_state[28] == 15:
            number_of_lava_walls = 0
            i = 0
            while(objects_map.get(f"fixed wall {number_of_lava_walls + i}")!= None):
                objects_map.pop(f"fixed wall {number_of_lava_walls + i}")
                i += 1
            wall_instance = Wall()
            wall_instance.xy = (8, 21)
            wall_instance.wh = (152, 38)
            objects_map['fixed wall 0'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (112, 101)
            wall_instance.wh = (48, 38)
            objects_map['fixed wall 1'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (8, 101)
            wall_instance.wh = (40, 38)
            objects_map['fixed wall 2'] = wall_instance
            number_of_walls = 3
            i = 0
            while(objects_map.get(f"fixed wall {number_of_walls + i}")!= None):
                objects_map.pop(f"fixed wall {number_of_walls + i}")
                i += 1

    elif ram_state[117] == 12:
        if ram_state[28] == 0:
            wall_instance = LavaWall()
            wall_instance.xy = (144, 61)
            wall_instance.wh = (16, 37)
            objects_map['lava wall 0'] = wall_instance
            wall_instance = LavaWall()
            wall_instance.xy = (8, 61)
            wall_instance.wh = (8, 37)
            objects_map['lava wall 1'] = wall_instance
            number_of_lava_walls = 2
            i = 0
            while(objects_map.get(f"fixed wall {number_of_lava_walls + i}")!= None):
                objects_map.pop(f"fixed wall {number_of_lava_walls + i}")
                i += 1
            wall_instance = Wall()
            wall_instance.xy = (136, 21)
            wall_instance.wh = (24, 38)
            objects_map['fixed wall 0'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (8, 21)
            wall_instance.wh = (16, 38)
            objects_map['fixed wall 1'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (88, 101)
            wall_instance.wh = (72, 38)
            objects_map['fixed wall 2'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (8, 101)
            wall_instance.wh = (64, 38)
            objects_map['fixed wall 3'] = wall_instance
            number_of_walls = 4
            i = 0
            while(objects_map.get(f"fixed wall {number_of_walls + i}")!= None):
                objects_map.pop(f"fixed wall {number_of_walls + i}")
                i += 1
        elif ram_state[28] == 1:
            wall_instance = LavaWall()
            wall_instance.xy = (144, 61)
            wall_instance.wh = (16, 37)
            objects_map['lava wall 0'] = wall_instance
            wall_instance = LavaWall()
            wall_instance.xy = (92, 61)
            wall_instance.wh = (12, 37)
            objects_map['lava wall 1'] = wall_instance
            wall_instance = LavaWall()
            wall_instance.xy = (56, 61)
            wall_instance.wh = (12, 37)
            objects_map['lava wall 2'] = wall_instance
            wall_instance = LavaWall()
            wall_instance.xy = (8, 61)
            wall_instance.wh = (8, 37)
            objects_map['lava wall 3'] = wall_instance
            number_of_lava_walls = 4
            i = 0
            while(objects_map.get(f"fixed wall {number_of_lava_walls + i}")!= None):
                objects_map.pop(f"fixed wall {number_of_lava_walls + i}")
                i += 1
            wall_instance = Wall()
            wall_instance.xy = (88, 21)
            wall_instance.wh = (72, 38)
            objects_map['fixed wall 0'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (8, 21)
            wall_instance.wh = (64, 38)
            objects_map['fixed wall 1'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (140, 101)
            wall_instance.wh = (20, 38)
            objects_map['fixed wall 2'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (116, 101)
            wall_instance.wh = (16, 38)
            objects_map['fixed wall 3'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (88, 101)
            wall_instance.wh = (20, 38)
            objects_map['fixed wall 4'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (52, 101)
            wall_instance.wh = (20, 38)
            objects_map['fixed wall 5'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (28, 101)
            wall_instance.wh = (16, 38)
            objects_map['fixed wall 6'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (8, 101)
            wall_instance.wh = (12, 38)
            objects_map['fixed wall 7'] = wall_instance
            number_of_walls = 8
            i = 0
            while(objects_map.get(f"fixed wall {number_of_walls + i}")!= None):
                objects_map.pop(f"fixed wall {number_of_walls + i}")
                i += 1
        elif ram_state[28] == 2:
            wall_instance = LavaWall()
            wall_instance.xy = (140, 61)
            wall_instance.wh = (20, 37)
            objects_map['lava wall 0'] = wall_instance
            wall_instance = LavaWall()
            wall_instance.xy = (120, 61)
            wall_instance.wh = (12, 37)
            objects_map['lava wall 1'] = wall_instance
            wall_instance = LavaWall()
            wall_instance.xy = (28, 61)
            wall_instance.wh = (12, 37)
            objects_map['lava wall 2'] = wall_instance
            wall_instance = LavaWall()
            wall_instance.xy = (8, 61)
            wall_instance.wh = (12, 37)
            objects_map['lava wall 3'] = wall_instance
            number_of_lava_walls = 4
            i = 0
            while(objects_map.get(f"fixed wall {number_of_lava_walls + i}")!= None):
                objects_map.pop(f"fixed wall {number_of_lava_walls + i}")
                i += 1
            wall_instance = Wall()
            wall_instance.xy = (140, 21)
            wall_instance.wh = (20, 38)
            objects_map['fixed wall 0'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (116, 21)
            wall_instance.wh = (16, 38)
            objects_map['fixed wall 1'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (88, 21)
            wall_instance.wh = (20, 38)
            objects_map['fixed wall 2'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (52, 21)
            wall_instance.wh = (20, 38)
            objects_map['fixed wall 3'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (28, 21)
            wall_instance.wh = (16, 38)
            objects_map['fixed wall 4'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (8, 21)
            wall_instance.wh = (12, 38)
            objects_map['fixed wall 5'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (144, 101)
            wall_instance.wh = (16, 38)
            objects_map['fixed wall 6'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (32, 101)
            wall_instance.wh = (96, 38)
            objects_map['fixed wall 7'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (8, 101)
            wall_instance.wh = (8, 38)
            objects_map['fixed wall 8'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (140, 61)
            wall_instance.wh = (20, 37)
            objects_map['fixed wall 9'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (120, 61)
            wall_instance.wh = (12, 37)
            objects_map['fixed wall 10'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (28, 61)
            wall_instance.wh = (12, 37)
            objects_map['fixed wall 11'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (8, 61)
            wall_instance.wh = (12, 37)
            objects_map['fixed wall 12'] = wall_instance
            number_of_walls = 13
            i = 0
            while(objects_map.get(f"fixed wall {number_of_walls + i}")!= None):
                objects_map.pop(f"fixed wall {number_of_walls + i}")
                i += 1
        elif ram_state[28] == 3:
            wall_instance = LavaWall()
            wall_instance.xy = (140, 61)
            wall_instance.wh = (20, 37)
            objects_map['lava wall 0'] = wall_instance
            wall_instance = LavaWall()
            wall_instance.xy = (8, 61)
            wall_instance.wh = (12, 37)
            objects_map['lava wall 1'] = wall_instance
            number_of_lava_walls = 2
            i = 0
            while(objects_map.get(f"fixed wall {number_of_lava_walls + i}")!= None):
                objects_map.pop(f"fixed wall {number_of_lava_walls + i}")
                i += 1
            wall_instance = Wall()
            wall_instance.xy = (144, 21)
            wall_instance.wh = (16, 38)
            objects_map['fixed wall 0'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (32, 21)
            wall_instance.wh = (96, 38)
            objects_map['fixed wall 1'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (8, 21)
            wall_instance.wh = (8, 38)
            objects_map['fixed wall 2'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (120, 101)
            wall_instance.wh = (40, 38)
            objects_map['fixed wall 3'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (48, 101)
            wall_instance.wh = (64, 38)
            objects_map['fixed wall 4'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (8, 101)
            wall_instance.wh = (32, 38)
            objects_map['fixed wall 5'] = wall_instance
            number_of_walls = 6
            i = 0
            while(objects_map.get(f"fixed wall {number_of_walls + i}")!= None):
                objects_map.pop(f"fixed wall {number_of_walls + i}")
                i += 1
        elif ram_state[28] == 4:
            wall_instance = LavaWall()
            wall_instance.xy = (128, 61)
            wall_instance.wh = (32, 37)
            objects_map['lava wall 0'] = wall_instance
            wall_instance = LavaWall()
            wall_instance.xy = (8, 61)
            wall_instance.wh = (24, 37)
            objects_map['lava wall 1'] = wall_instance
            number_of_lava_walls = 2
            i = 0
            while(objects_map.get(f"fixed wall {number_of_lava_walls + i}")!= None):
                objects_map.pop(f"fixed wall {number_of_lava_walls + i}")
                i += 1
            wall_instance = Wall()
            wall_instance.xy = (120, 21)
            wall_instance.wh = (40, 38)
            objects_map['fixed wall 0'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (48, 21)
            wall_instance.wh = (64, 38)
            objects_map['fixed wall 1'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (8, 21)
            wall_instance.wh = (32, 38)
            objects_map['fixed wall 2'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (144, 101)
            wall_instance.wh = (16, 38)
            objects_map['fixed wall 3'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (40, 101)
            wall_instance.wh = (80, 38)
            objects_map['fixed wall 4'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (8, 101)
            wall_instance.wh = (8, 38)
            objects_map['fixed wall 5'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (128, 61)
            wall_instance.wh = (32, 37)
            objects_map['fixed wall 6'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (8, 61)
            wall_instance.wh = (24, 37)
            objects_map['fixed wall 7'] = wall_instance
            number_of_walls = 8
            i = 0
            while(objects_map.get(f"fixed wall {number_of_walls + i}")!= None):
                objects_map.pop(f"fixed wall {number_of_walls + i}")
                i += 1
        elif ram_state[28] == 5:
            wall_instance = LavaWall()
            wall_instance.xy = (136, 61)
            wall_instance.wh = (24, 37)
            objects_map['lava wall 0'] = wall_instance
            wall_instance = LavaWall()
            wall_instance.xy = (40, 61)
            wall_instance.wh = (80, 37)
            objects_map['lava wall 1'] = wall_instance
            wall_instance = LavaWall()
            wall_instance.xy = (8, 61)
            wall_instance.wh = (16, 37)
            objects_map['lava wall 2'] = wall_instance
            number_of_lava_walls = 3
            i = 0
            while(objects_map.get(f"fixed wall {number_of_lava_walls + i}")!= None):
                objects_map.pop(f"fixed wall {number_of_lava_walls + i}")
                i += 1
            wall_instance = Wall()
            wall_instance.xy = (144, 21)
            wall_instance.wh = (16, 38)
            objects_map['fixed wall 0'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (40, 21)
            wall_instance.wh = (80, 38)
            objects_map['fixed wall 1'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (8, 21)
            wall_instance.wh = (8, 38)
            objects_map['fixed wall 2'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (144, 101)
            wall_instance.wh = (16, 38)
            objects_map['fixed wall 3'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (32, 101)
            wall_instance.wh = (96, 38)
            objects_map['fixed wall 4'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (8, 101)
            wall_instance.wh = (8, 38)
            objects_map['fixed wall 5'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (136, 61)
            wall_instance.wh = (24, 37)
            objects_map['fixed wall 6'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (40, 61)
            wall_instance.wh = (80, 37)
            objects_map['fixed wall 7'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (8, 61)
            wall_instance.wh = (16, 37)
            objects_map['fixed wall 8'] = wall_instance
            number_of_walls = 9
            i = 0
            while(objects_map.get(f"fixed wall {number_of_walls + i}")!= None):
                objects_map.pop(f"fixed wall {number_of_walls + i}")
                i += 1
        elif ram_state[28] == 6:
            wall_instance = LavaWall()
            wall_instance.xy = (144, 61)
            wall_instance.wh = (16, 37)
            objects_map['lava wall 0'] = wall_instance
            wall_instance = LavaWall()
            wall_instance.xy = (40, 61)
            wall_instance.wh = (80, 37)
            objects_map['lava wall 1'] = wall_instance
            wall_instance = LavaWall()
            wall_instance.xy = (8, 61)
            wall_instance.wh = (8, 37)
            objects_map['lava wall 2'] = wall_instance
            number_of_lava_walls = 3
            i = 0
            while(objects_map.get(f"fixed wall {number_of_lava_walls + i}")!= None):
                objects_map.pop(f"fixed wall {number_of_lava_walls + i}")
                i += 1
            wall_instance = Wall()
            wall_instance.xy = (144, 21)
            wall_instance.wh = (16, 38)
            objects_map['fixed wall 0'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (32, 21)
            wall_instance.wh = (96, 38)
            objects_map['fixed wall 1'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (8, 21)
            wall_instance.wh = (8, 38)
            objects_map['fixed wall 2'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (8, 101)
            wall_instance.wh = (152, 38)
            objects_map['fixed wall 3'] = wall_instance
            number_of_walls = 4
            i = 0
            while(objects_map.get(f"fixed wall {number_of_walls + i}")!= None):
                objects_map.pop(f"fixed wall {number_of_walls + i}")
                i += 1
        elif ram_state[28] == 7:
            wall_instance = LavaWall()
            wall_instance.xy = (144, 61)
            wall_instance.wh = (16, 37)
            objects_map['lava wall 0'] = wall_instance
            wall_instance = LavaWall()
            wall_instance.xy = (8, 61)
            wall_instance.wh = (8, 37)
            objects_map['lava wall 1'] = wall_instance
            number_of_lava_walls = 2
            i = 0
            while(objects_map.get(f"fixed wall {number_of_lava_walls + i}")!= None):
                objects_map.pop(f"fixed wall {number_of_lava_walls + i}")
                i += 1
            wall_instance = Wall()
            wall_instance.xy = (8, 21)
            wall_instance.wh = (152, 38)
            objects_map['fixed wall 0'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (88, 101)
            wall_instance.wh = (72, 38)
            objects_map['fixed wall 1'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (8, 101)
            wall_instance.wh = (64, 38)
            objects_map['fixed wall 2'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (144, 61)
            wall_instance.wh = (16, 37)
            objects_map['fixed wall 3'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (8, 61)
            wall_instance.wh = (8, 37)
            objects_map['fixed wall 4'] = wall_instance
            number_of_walls = 5
            i = 0
            while(objects_map.get(f"fixed wall {number_of_walls + i}")!= None):
                objects_map.pop(f"fixed wall {number_of_walls + i}")
                i += 1
        elif ram_state[28] == 8:
            number_of_lava_walls = 0
            i = 0
            while(objects_map.get(f"fixed wall {number_of_lava_walls + i}")!= None):
                objects_map.pop(f"fixed wall {number_of_lava_walls + i}")
                i += 1
            wall_instance = Wall()
            wall_instance.xy = (88, 21)
            wall_instance.wh = (72, 38)
            objects_map['fixed wall 0'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (8, 21)
            wall_instance.wh = (64, 38)
            objects_map['fixed wall 1'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (116, 101)
            wall_instance.wh = (44, 38)
            objects_map['fixed wall 2'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (52, 101)
            wall_instance.wh = (56, 38)
            objects_map['fixed wall 3'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (8, 101)
            wall_instance.wh = (36, 38)
            objects_map['fixed wall 4'] = wall_instance
            number_of_walls = 5
            i = 0
            while(objects_map.get(f"fixed wall {number_of_walls + i}")!= None):
                objects_map.pop(f"fixed wall {number_of_walls + i}")
                i += 1
        elif ram_state[28] == 9:
            wall_instance = LavaWall()
            wall_instance.xy = (144, 61)
            wall_instance.wh = (16, 37)
            objects_map['lava wall 0'] = wall_instance
            wall_instance = LavaWall()
            wall_instance.xy = (8, 61)
            wall_instance.wh = (8, 37)
            objects_map['lava wall 1'] = wall_instance
            number_of_lava_walls = 2
            i = 0
            while(objects_map.get(f"fixed wall {number_of_lava_walls + i}")!= None):
                objects_map.pop(f"fixed wall {number_of_lava_walls + i}")
                i += 1
            wall_instance = Wall()
            wall_instance.xy = (116, 21)
            wall_instance.wh = (44, 38)
            objects_map['fixed wall 0'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (52, 21)
            wall_instance.wh = (56, 38)
            objects_map['fixed wall 1'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (8, 21)
            wall_instance.wh = (36, 38)
            objects_map['fixed wall 2'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (8, 101)
            wall_instance.wh = (152, 38)
            objects_map['fixed wall 3'] = wall_instance
            number_of_walls = 4
            i = 0
            while(objects_map.get(f"fixed wall {number_of_walls + i}")!= None):
                objects_map.pop(f"fixed wall {number_of_walls + i}")
                i += 1
        elif ram_state[28] == 10:
            number_of_lava_walls = 0
            i = 0
            while(objects_map.get(f"fixed wall {number_of_lava_walls + i}")!= None):
                objects_map.pop(f"fixed wall {number_of_lava_walls + i}")
                i += 1
            wall_instance = Wall()
            wall_instance.xy = (8, 21)
            wall_instance.wh = (152, 38)
            objects_map['fixed wall 0'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (8, 101)
            wall_instance.wh = (152, 38)
            objects_map['fixed wall 1'] = wall_instance
            number_of_walls = 2
            i = 0
            while(objects_map.get(f"fixed wall {number_of_walls + i}")!= None):
                objects_map.pop(f"fixed wall {number_of_walls + i}")
                i += 1
        elif ram_state[28] == 11:
            number_of_lava_walls = 0
            i = 0
            while(objects_map.get(f"fixed wall {number_of_lava_walls + i}")!= None):
                objects_map.pop(f"fixed wall {number_of_lava_walls + i}")
                i += 1
            wall_instance = Wall()
            wall_instance.xy = (8, 21)
            wall_instance.wh = (152, 38)
            objects_map['fixed wall 0'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (136, 101)
            wall_instance.wh = (24, 38)
            objects_map['fixed wall 1'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (68, 101)
            wall_instance.wh = (24, 38)
            objects_map['fixed wall 2'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (8, 101)
            wall_instance.wh = (16, 38)
            objects_map['fixed wall 3'] = wall_instance
            number_of_walls = 4
            i = 0
            while(objects_map.get(f"fixed wall {number_of_walls + i}")!= None):
                objects_map.pop(f"fixed wall {number_of_walls + i}")
                i += 1
        elif ram_state[28] == 12:
            wall_instance = LavaWall()
            wall_instance.xy = (68, 61)
            wall_instance.wh = (24, 37)
            objects_map['lava wall 0'] = wall_instance
            number_of_lava_walls = 1
            i = 0
            while(objects_map.get(f"fixed wall {number_of_lava_walls + i}")!= None):
                objects_map.pop(f"fixed wall {number_of_lava_walls + i}")
                i += 1
            wall_instance = Wall()
            wall_instance.xy = (8, 21)
            wall_instance.wh = (152, 38)
            objects_map['fixed wall 0'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (136, 101)
            wall_instance.wh = (24, 38)
            objects_map['fixed wall 1'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (8, 101)
            wall_instance.wh = (16, 38)
            objects_map['fixed wall 2'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (68, 61)
            wall_instance.wh = (24, 37)
            objects_map['fixed wall 3'] = wall_instance
            number_of_walls = 4
            i = 0
            while(objects_map.get(f"fixed wall {number_of_walls + i}")!= None):
                objects_map.pop(f"fixed wall {number_of_walls + i}")
                i += 1
        elif ram_state[28] == 13:
            number_of_lava_walls = 0
            i = 0
            while(objects_map.get(f"fixed wall {number_of_lava_walls + i}")!= None):
                objects_map.pop(f"fixed wall {number_of_lava_walls + i}")
                i += 1
            wall_instance = Wall()
            wall_instance.xy = (8, 21)
            wall_instance.wh = (152, 38)
            objects_map['fixed wall 0'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (136, 101)
            wall_instance.wh = (24, 38)
            objects_map['fixed wall 1'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (72, 101)
            wall_instance.wh = (16, 38)
            objects_map['fixed wall 2'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (8, 101)
            wall_instance.wh = (16, 38)
            objects_map['fixed wall 3'] = wall_instance
            number_of_walls = 4
            i = 0
            while(objects_map.get(f"fixed wall {number_of_walls + i}")!= None):
                objects_map.pop(f"fixed wall {number_of_walls + i}")
                i += 1
        elif ram_state[28] == 14:
            number_of_lava_walls = 0
            i = 0
            while(objects_map.get(f"fixed wall {number_of_lava_walls + i}")!= None):
                objects_map.pop(f"fixed wall {number_of_lava_walls + i}")
                i += 1
            wall_instance = Wall()
            wall_instance.xy = (8, 21)
            wall_instance.wh = (152, 38)
            objects_map['fixed wall 0'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (112, 101)
            wall_instance.wh = (48, 38)
            objects_map['fixed wall 1'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (64, 101)
            wall_instance.wh = (32, 38)
            objects_map['fixed wall 2'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (8, 101)
            wall_instance.wh = (40, 38)
            objects_map['fixed wall 3'] = wall_instance
            number_of_walls = 4
            i = 0
            while(objects_map.get(f"fixed wall {number_of_walls + i}")!= None):
                objects_map.pop(f"fixed wall {number_of_walls + i}")
                i += 1
        elif ram_state[28] == 15:
            number_of_lava_walls = 0
            i = 0
            while(objects_map.get(f"fixed wall {number_of_lava_walls + i}")!= None):
                objects_map.pop(f"fixed wall {number_of_lava_walls + i}")
                i += 1
            wall_instance = Wall()
            wall_instance.xy = (8, 21)
            wall_instance.wh = (152, 38)
            objects_map['fixed wall 0'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (112, 101)
            wall_instance.wh = (48, 38)
            objects_map['fixed wall 1'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (8, 101)
            wall_instance.wh = (40, 38)
            objects_map['fixed wall 2'] = wall_instance
            number_of_walls = 3
            i = 0
            while(objects_map.get(f"fixed wall {number_of_walls + i}")!= None):
                objects_map.pop(f"fixed wall {number_of_walls + i}")
                i += 1

    elif ram_state[117] == 13:
        if ram_state[28] == 0:
            wall_instance = LavaWall()
            wall_instance.xy = (144, 61)
            wall_instance.wh = (16, 37)
            objects_map['lava wall 0'] = wall_instance
            wall_instance = LavaWall()
            wall_instance.xy = (8, 61)
            wall_instance.wh = (8, 37)
            objects_map['lava wall 1'] = wall_instance
            number_of_lava_walls = 2
            i = 0
            while(objects_map.get(f"fixed wall {number_of_lava_walls + i}")!= None):
                objects_map.pop(f"fixed wall {number_of_lava_walls + i}")
                i += 1
            wall_instance = Wall()
            wall_instance.xy = (136, 21)
            wall_instance.wh = (24, 38)
            objects_map['fixed wall 0'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (8, 21)
            wall_instance.wh = (16, 38)
            objects_map['fixed wall 1'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (88, 101)
            wall_instance.wh = (72, 38)
            objects_map['fixed wall 2'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (8, 101)
            wall_instance.wh = (64, 38)
            objects_map['fixed wall 3'] = wall_instance
            number_of_walls = 4
            i = 0
            while(objects_map.get(f"fixed wall {number_of_walls + i}")!= None):
                objects_map.pop(f"fixed wall {number_of_walls + i}")
                i += 1
        elif ram_state[28] == 1:
            wall_instance = LavaWall()
            wall_instance.xy = (80, 61)
            wall_instance.wh = (16, 37)
            objects_map['lava wall 0'] = wall_instance
            wall_instance = LavaWall()
            wall_instance.xy = (8, 61)
            wall_instance.wh = (8, 37)
            objects_map['lava wall 1'] = wall_instance
            number_of_lava_walls = 2
            i = 0
            while(objects_map.get(f"fixed wall {number_of_lava_walls + i}")!= None):
                objects_map.pop(f"fixed wall {number_of_lava_walls + i}")
                i += 1
            wall_instance = Wall()
            wall_instance.xy = (88, 21)
            wall_instance.wh = (72, 38)
            objects_map['fixed wall 0'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (8, 21)
            wall_instance.wh = (64, 38)
            objects_map['fixed wall 1'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (8, 101)
            wall_instance.wh = (152, 38)
            objects_map['fixed wall 2'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (80, 61)
            wall_instance.wh = (16, 37)
            objects_map['fixed wall 3'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (8, 61)
            wall_instance.wh = (8, 37)
            objects_map['fixed wall 4'] = wall_instance
            number_of_walls = 5
            i = 0
            while(objects_map.get(f"fixed wall {number_of_walls + i}")!= None):
                objects_map.pop(f"fixed wall {number_of_walls + i}")
                i += 1
        elif ram_state[28] == 2:
            wall_instance = LavaWall()
            wall_instance.xy = (144, 61)
            wall_instance.wh = (16, 37)
            objects_map['lava wall 0'] = wall_instance
            wall_instance = LavaWall()
            wall_instance.xy = (8, 61)
            wall_instance.wh = (8, 37)
            objects_map['lava wall 1'] = wall_instance
            number_of_lava_walls = 2
            i = 0
            while(objects_map.get(f"fixed wall {number_of_lava_walls + i}")!= None):
                objects_map.pop(f"fixed wall {number_of_lava_walls + i}")
                i += 1
            wall_instance = Wall()
            wall_instance.xy = (8, 21)
            wall_instance.wh = (152, 38)
            objects_map['fixed wall 0'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (88, 101)
            wall_instance.wh = (72, 38)
            objects_map['fixed wall 1'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (8, 101)
            wall_instance.wh = (64, 38)
            objects_map['fixed wall 2'] = wall_instance
            number_of_walls = 3
            i = 0
            while(objects_map.get(f"fixed wall {number_of_walls + i}")!= None):
                objects_map.pop(f"fixed wall {number_of_walls + i}")
                i += 1
        elif ram_state[28] == 3:
            wall_instance = LavaWall()
            wall_instance.xy = (144, 61)
            wall_instance.wh = (16, 37)
            objects_map['lava wall 0'] = wall_instance
            wall_instance = LavaWall()
            wall_instance.xy = (8, 61)
            wall_instance.wh = (8, 37)
            objects_map['lava wall 1'] = wall_instance
            number_of_lava_walls = 2
            i = 0
            while(objects_map.get(f"fixed wall {number_of_lava_walls + i}")!= None):
                objects_map.pop(f"fixed wall {number_of_lava_walls + i}")
                i += 1
            wall_instance = Wall()
            wall_instance.xy = (88, 21)
            wall_instance.wh = (72, 38)
            objects_map['fixed wall 0'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (8, 21)
            wall_instance.wh = (64, 38)
            objects_map['fixed wall 1'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (8, 101)
            wall_instance.wh = (152, 38)
            objects_map['fixed wall 2'] = wall_instance
            number_of_walls = 3
            i = 0
            while(objects_map.get(f"fixed wall {number_of_walls + i}")!= None):
                objects_map.pop(f"fixed wall {number_of_walls + i}")
                i += 1
        elif ram_state[28] == 4:
            wall_instance = LavaWall()
            wall_instance.xy = (144, 61)
            wall_instance.wh = (16, 37)
            objects_map['lava wall 0'] = wall_instance
            wall_instance = LavaWall()
            wall_instance.xy = (8, 61)
            wall_instance.wh = (8, 37)
            objects_map['lava wall 1'] = wall_instance
            number_of_lava_walls = 2
            i = 0
            while(objects_map.get(f"fixed wall {number_of_lava_walls + i}")!= None):
                objects_map.pop(f"fixed wall {number_of_lava_walls + i}")
                i += 1
            wall_instance = Wall()
            wall_instance.xy = (8, 21)
            wall_instance.wh = (152, 38)
            objects_map['fixed wall 0'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (136, 101)
            wall_instance.wh = (24, 38)
            objects_map['fixed wall 1'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (88, 101)
            wall_instance.wh = (32, 38)
            objects_map['fixed wall 2'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (40, 101)
            wall_instance.wh = (32, 38)
            objects_map['fixed wall 3'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (8, 101)
            wall_instance.wh = (16, 38)
            objects_map['fixed wall 4'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (144, 61)
            wall_instance.wh = (16, 37)
            objects_map['fixed wall 5'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (8, 61)
            wall_instance.wh = (8, 37)
            objects_map['fixed wall 6'] = wall_instance
            number_of_walls = 7
            i = 0
            while(objects_map.get(f"fixed wall {number_of_walls + i}")!= None):
                objects_map.pop(f"fixed wall {number_of_walls + i}")
                i += 1
        elif ram_state[28] == 5:
            wall_instance = LavaWall()
            wall_instance.xy = (84, 61)
            wall_instance.wh = (76, 37)
            objects_map['lava wall 0'] = wall_instance
            wall_instance = LavaWall()
            wall_instance.xy = (8, 61)
            wall_instance.wh = (68, 37)
            objects_map['lava wall 1'] = wall_instance
            number_of_lava_walls = 2
            i = 0
            while(objects_map.get(f"fixed wall {number_of_lava_walls + i}")!= None):
                objects_map.pop(f"fixed wall {number_of_lava_walls + i}")
                i += 1
            wall_instance = Wall()
            wall_instance.xy = (136, 21)
            wall_instance.wh = (24, 38)
            objects_map['fixed wall 0'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (88, 21)
            wall_instance.wh = (32, 38)
            objects_map['fixed wall 1'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (40, 21)
            wall_instance.wh = (32, 38)
            objects_map['fixed wall 2'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (8, 21)
            wall_instance.wh = (16, 38)
            objects_map['fixed wall 3'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (112, 101)
            wall_instance.wh = (48, 38)
            objects_map['fixed wall 4'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (8, 101)
            wall_instance.wh = (40, 38)
            objects_map['fixed wall 5'] = wall_instance
            number_of_walls = 6
            i = 0
            while(objects_map.get(f"fixed wall {number_of_walls + i}")!= None):
                objects_map.pop(f"fixed wall {number_of_walls + i}")
                i += 1
        elif ram_state[28] == 6:
            wall_instance = LavaWall()
            wall_instance.xy = (128, 61)
            wall_instance.wh = (32, 37)
            objects_map['lava wall 0'] = wall_instance
            wall_instance = LavaWall()
            wall_instance.xy = (48, 61)
            wall_instance.wh = (48, 37)
            objects_map['lava wall 1'] = wall_instance
            wall_instance = LavaWall()
            wall_instance.xy = (8, 61)
            wall_instance.wh = (8, 37)
            objects_map['lava wall 2'] = wall_instance
            number_of_lava_walls = 3
            i = 0
            while(objects_map.get(f"fixed wall {number_of_lava_walls + i}")!= None):
                objects_map.pop(f"fixed wall {number_of_lava_walls + i}")
                i += 1
            wall_instance = Wall()
            wall_instance.xy = (112, 21)
            wall_instance.wh = (48, 38)
            objects_map['fixed wall 0'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (8, 21)
            wall_instance.wh = (40, 38)
            objects_map['fixed wall 1'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (140, 101)
            wall_instance.wh = (20, 38)
            objects_map['fixed wall 2'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (44, 101)
            wall_instance.wh = (72, 38)
            objects_map['fixed wall 3'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (8, 101)
            wall_instance.wh = (12, 38)
            objects_map['fixed wall 4'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (128, 61)
            wall_instance.wh = (32, 37)
            objects_map['fixed wall 5'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (48, 61)
            wall_instance.wh = (48, 37)
            objects_map['fixed wall 6'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (8, 61)
            wall_instance.wh = (8, 37)
            objects_map['fixed wall 7'] = wall_instance
            number_of_walls = 8
            i = 0
            while(objects_map.get(f"fixed wall {number_of_walls + i}")!= None):
                objects_map.pop(f"fixed wall {number_of_walls + i}")
                i += 1
        elif ram_state[28] == 7:
            wall_instance = LavaWall()
            wall_instance.xy = (144, 61)
            wall_instance.wh = (16, 37)
            objects_map['lava wall 0'] = wall_instance
            wall_instance = LavaWall()
            wall_instance.xy = (8, 61)
            wall_instance.wh = (8, 37)
            objects_map['lava wall 1'] = wall_instance
            number_of_lava_walls = 2
            i = 0
            while(objects_map.get(f"fixed wall {number_of_lava_walls + i}")!= None):
                objects_map.pop(f"fixed wall {number_of_lava_walls + i}")
                i += 1
            wall_instance = Wall()
            wall_instance.xy = (140, 21)
            wall_instance.wh = (20, 38)
            objects_map['fixed wall 0'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (44, 21)
            wall_instance.wh = (72, 38)
            objects_map['fixed wall 1'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (8, 21)
            wall_instance.wh = (12, 38)
            objects_map['fixed wall 2'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (8, 101)
            wall_instance.wh = (152, 38)
            objects_map['fixed wall 3'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (144, 61)
            wall_instance.wh = (16, 37)
            objects_map['fixed wall 4'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (8, 61)
            wall_instance.wh = (8, 37)
            objects_map['fixed wall 5'] = wall_instance
            number_of_walls = 6
            i = 0
            while(objects_map.get(f"fixed wall {number_of_walls + i}")!= None):
                objects_map.pop(f"fixed wall {number_of_walls + i}")
                i += 1
        elif ram_state[28] == 8:
            wall_instance = LavaWall()
            wall_instance.xy = (144, 61)
            wall_instance.wh = (16, 37)
            objects_map['lava wall 0'] = wall_instance
            wall_instance = LavaWall()
            wall_instance.xy = (8, 61)
            wall_instance.wh = (8, 37)
            objects_map['lava wall 1'] = wall_instance
            number_of_lava_walls = 2
            i = 0
            while(objects_map.get(f"fixed wall {number_of_lava_walls + i}")!= None):
                objects_map.pop(f"fixed wall {number_of_lava_walls + i}")
                i += 1
            wall_instance = Wall()
            wall_instance.xy = (8, 21)
            wall_instance.wh = (152, 38)
            objects_map['fixed wall 0'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (136, 101)
            wall_instance.wh = (24, 38)
            objects_map['fixed wall 1'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (52, 101)
            wall_instance.wh = (56, 38)
            objects_map['fixed wall 2'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (8, 101)
            wall_instance.wh = (16, 38)
            objects_map['fixed wall 3'] = wall_instance
            number_of_walls = 4
            i = 0
            while(objects_map.get(f"fixed wall {number_of_walls + i}")!= None):
                objects_map.pop(f"fixed wall {number_of_walls + i}")
                i += 1
        elif ram_state[28] == 9:
            wall_instance = LavaWall()
            wall_instance.xy = (120, 61)
            wall_instance.wh = (40, 37)
            objects_map['lava wall 0'] = wall_instance
            wall_instance = LavaWall()
            wall_instance.xy = (8, 61)
            wall_instance.wh = (32, 37)
            objects_map['lava wall 1'] = wall_instance
            number_of_lava_walls = 2
            i = 0
            while(objects_map.get(f"fixed wall {number_of_lava_walls + i}")!= None):
                objects_map.pop(f"fixed wall {number_of_lava_walls + i}")
                i += 1
            wall_instance = Wall()
            wall_instance.xy = (136, 21)
            wall_instance.wh = (24, 38)
            objects_map['fixed wall 0'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (52, 21)
            wall_instance.wh = (56, 38)
            objects_map['fixed wall 1'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (8, 21)
            wall_instance.wh = (16, 38)
            objects_map['fixed wall 2'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (84, 101)
            wall_instance.wh = (76, 38)
            objects_map['fixed wall 3'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (8, 101)
            wall_instance.wh = (68, 38)
            objects_map['fixed wall 4'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (120, 61)
            wall_instance.wh = (40, 37)
            objects_map['fixed wall 5'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (8, 61)
            wall_instance.wh = (32, 37)
            objects_map['fixed wall 6'] = wall_instance
            number_of_walls = 7
            i = 0
            while(objects_map.get(f"fixed wall {number_of_walls + i}")!= None):
                objects_map.pop(f"fixed wall {number_of_walls + i}")
                i += 1
        elif ram_state[28] == 10:
            number_of_lava_walls = 0
            i = 0
            while(objects_map.get(f"fixed wall {number_of_lava_walls + i}")!= None):
                objects_map.pop(f"fixed wall {number_of_lava_walls + i}")
                i += 1
            wall_instance = Wall()
            wall_instance.xy = (84, 21)
            wall_instance.wh = (76, 38)
            objects_map['fixed wall 0'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (8, 21)
            wall_instance.wh = (68, 38)
            objects_map['fixed wall 1'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (140, 101)
            wall_instance.wh = (20, 38)
            objects_map['fixed wall 2'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (8, 101)
            wall_instance.wh = (12, 38)
            objects_map['fixed wall 3'] = wall_instance
            number_of_walls = 4
            i = 0
            while(objects_map.get(f"fixed wall {number_of_walls + i}")!= None):
                objects_map.pop(f"fixed wall {number_of_walls + i}")
                i += 1
        elif ram_state[28] == 11:
            number_of_lava_walls = 0
            i = 0
            while(objects_map.get(f"fixed wall {number_of_lava_walls + i}")!= None):
                objects_map.pop(f"fixed wall {number_of_lava_walls + i}")
                i += 1
            wall_instance = Wall()
            wall_instance.xy = (8, 21)
            wall_instance.wh = (152, 38)
            objects_map['fixed wall 0'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (136, 101)
            wall_instance.wh = (24, 38)
            objects_map['fixed wall 1'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (68, 101)
            wall_instance.wh = (24, 38)
            objects_map['fixed wall 2'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (8, 101)
            wall_instance.wh = (16, 38)
            objects_map['fixed wall 3'] = wall_instance
            number_of_walls = 4
            i = 0
            while(objects_map.get(f"fixed wall {number_of_walls + i}")!= None):
                objects_map.pop(f"fixed wall {number_of_walls + i}")
                i += 1
        elif ram_state[28] == 12:
            wall_instance = LavaWall()
            wall_instance.xy = (68, 61)
            wall_instance.wh = (24, 37)
            objects_map['lava wall 0'] = wall_instance
            number_of_lava_walls = 1
            i = 0
            while(objects_map.get(f"fixed wall {number_of_lava_walls + i}")!= None):
                objects_map.pop(f"fixed wall {number_of_lava_walls + i}")
                i += 1
            wall_instance = Wall()
            wall_instance.xy = (8, 21)
            wall_instance.wh = (152, 38)
            objects_map['fixed wall 0'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (136, 101)
            wall_instance.wh = (24, 38)
            objects_map['fixed wall 1'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (8, 101)
            wall_instance.wh = (16, 38)
            objects_map['fixed wall 2'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (68, 61)
            wall_instance.wh = (24, 37)
            objects_map['fixed wall 3'] = wall_instance
            number_of_walls = 4
            i = 0
            while(objects_map.get(f"fixed wall {number_of_walls + i}")!= None):
                objects_map.pop(f"fixed wall {number_of_walls + i}")
                i += 1
        elif ram_state[28] == 13:
            number_of_lava_walls = 0
            i = 0
            while(objects_map.get(f"fixed wall {number_of_lava_walls + i}")!= None):
                objects_map.pop(f"fixed wall {number_of_lava_walls + i}")
                i += 1
            wall_instance = Wall()
            wall_instance.xy = (8, 21)
            wall_instance.wh = (152, 38)
            objects_map['fixed wall 0'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (136, 101)
            wall_instance.wh = (24, 38)
            objects_map['fixed wall 1'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (72, 101)
            wall_instance.wh = (16, 38)
            objects_map['fixed wall 2'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (8, 101)
            wall_instance.wh = (16, 38)
            objects_map['fixed wall 3'] = wall_instance
            number_of_walls = 4
            i = 0
            while(objects_map.get(f"fixed wall {number_of_walls + i}")!= None):
                objects_map.pop(f"fixed wall {number_of_walls + i}")
                i += 1
        elif ram_state[28] == 14:
            number_of_lava_walls = 0
            i = 0
            while(objects_map.get(f"fixed wall {number_of_lava_walls + i}")!= None):
                objects_map.pop(f"fixed wall {number_of_lava_walls + i}")
                i += 1
            wall_instance = Wall()
            wall_instance.xy = (8, 21)
            wall_instance.wh = (152, 38)
            objects_map['fixed wall 0'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (136, 101)
            wall_instance.wh = (24, 38)
            objects_map['fixed wall 1'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (96, 101)
            wall_instance.wh = (16, 38)
            objects_map['fixed wall 2'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (48, 101)
            wall_instance.wh = (16, 38)
            objects_map['fixed wall 3'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (8, 101)
            wall_instance.wh = (16, 38)
            objects_map['fixed wall 4'] = wall_instance
            number_of_walls = 5
            i = 0
            while(objects_map.get(f"fixed wall {number_of_walls + i}")!= None):
                objects_map.pop(f"fixed wall {number_of_walls + i}")
                i += 1
        elif ram_state[28] == 15:
            number_of_lava_walls = 0
            i = 0
            while(objects_map.get(f"fixed wall {number_of_lava_walls + i}")!= None):
                objects_map.pop(f"fixed wall {number_of_lava_walls + i}")
                i += 1
            wall_instance = Wall()
            wall_instance.xy = (8, 21)
            wall_instance.wh = (152, 38)
            objects_map['fixed wall 0'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (112, 101)
            wall_instance.wh = (48, 38)
            objects_map['fixed wall 1'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (72, 101)
            wall_instance.wh = (16, 38)
            objects_map['fixed wall 2'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (8, 101)
            wall_instance.wh = (40, 38)
            objects_map['fixed wall 3'] = wall_instance
            number_of_walls = 4
            i = 0
            while(objects_map.get(f"fixed wall {number_of_walls + i}")!= None):
                objects_map.pop(f"fixed wall {number_of_walls + i}")
                i += 1

    elif ram_state[117] == 14:
        if ram_state[28] == 0:
            wall_instance = LavaWall()
            wall_instance.xy = (144, 61)
            wall_instance.wh = (16, 37)
            objects_map['lava wall 0'] = wall_instance
            wall_instance = LavaWall()
            wall_instance.xy = (8, 61)
            wall_instance.wh = (8, 37)
            objects_map['lava wall 1'] = wall_instance
            number_of_lava_walls = 2
            i = 0
            while(objects_map.get(f"fixed wall {number_of_lava_walls + i}")!= None):
                objects_map.pop(f"fixed wall {number_of_lava_walls + i}")
                i += 1
            wall_instance = Wall()
            wall_instance.xy = (136, 21)
            wall_instance.wh = (24, 38)
            objects_map['fixed wall 0'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (8, 21)
            wall_instance.wh = (16, 38)
            objects_map['fixed wall 1'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (88, 101)
            wall_instance.wh = (72, 38)
            objects_map['fixed wall 2'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (8, 101)
            wall_instance.wh = (64, 38)
            objects_map['fixed wall 3'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (144, 61)
            wall_instance.wh = (16, 37)
            objects_map['fixed wall 4'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (8, 61)
            wall_instance.wh = (8, 37)
            objects_map['fixed wall 5'] = wall_instance
            number_of_walls = 6
            i = 0
            while(objects_map.get(f"fixed wall {number_of_walls + i}")!= None):
                objects_map.pop(f"fixed wall {number_of_walls + i}")
                i += 1
        elif ram_state[28] == 1:
            wall_instance = LavaWall()
            wall_instance.xy = (124, 61)
            wall_instance.wh = (36, 37)
            objects_map['lava wall 0'] = wall_instance
            wall_instance = LavaWall()
            wall_instance.xy = (8, 61)
            wall_instance.wh = (28, 37)
            objects_map['lava wall 1'] = wall_instance
            number_of_lava_walls = 2
            i = 0
            while(objects_map.get(f"fixed wall {number_of_lava_walls + i}")!= None):
                objects_map.pop(f"fixed wall {number_of_lava_walls + i}")
                i += 1
            wall_instance = Wall()
            wall_instance.xy = (88, 21)
            wall_instance.wh = (72, 38)
            objects_map['fixed wall 0'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (8, 21)
            wall_instance.wh = (64, 38)
            objects_map['fixed wall 1'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (112, 101)
            wall_instance.wh = (48, 38)
            objects_map['fixed wall 2'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (56, 101)
            wall_instance.wh = (48, 38)
            objects_map['fixed wall 3'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (8, 101)
            wall_instance.wh = (40, 38)
            objects_map['fixed wall 4'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (124, 61)
            wall_instance.wh = (36, 37)
            objects_map['fixed wall 5'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (8, 61)
            wall_instance.wh = (28, 37)
            objects_map['fixed wall 6'] = wall_instance
            number_of_walls = 7
            i = 0
            while(objects_map.get(f"fixed wall {number_of_walls + i}")!= None):
                objects_map.pop(f"fixed wall {number_of_walls + i}")
                i += 1
        elif ram_state[28] == 2:
            wall_instance = LavaWall()
            wall_instance.xy = (144, 61)
            wall_instance.wh = (16, 37)
            objects_map['lava wall 0'] = wall_instance
            wall_instance = LavaWall()
            wall_instance.xy = (64, 61)
            wall_instance.wh = (56, 37)
            objects_map['lava wall 1'] = wall_instance
            wall_instance = LavaWall()
            wall_instance.xy = (8, 61)
            wall_instance.wh = (32, 37)
            objects_map['lava wall 2'] = wall_instance
            number_of_lava_walls = 3
            i = 0
            while(objects_map.get(f"fixed wall {number_of_lava_walls + i}")!= None):
                objects_map.pop(f"fixed wall {number_of_lava_walls + i}")
                i += 1
            wall_instance = Wall()
            wall_instance.xy = (112, 21)
            wall_instance.wh = (48, 38)
            objects_map['fixed wall 0'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (56, 21)
            wall_instance.wh = (48, 38)
            objects_map['fixed wall 1'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (8, 21)
            wall_instance.wh = (40, 38)
            objects_map['fixed wall 2'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (104, 101)
            wall_instance.wh = (56, 38)
            objects_map['fixed wall 3'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (8, 101)
            wall_instance.wh = (48, 38)
            objects_map['fixed wall 4'] = wall_instance
            number_of_walls = 5
            i = 0
            while(objects_map.get(f"fixed wall {number_of_walls + i}")!= None):
                objects_map.pop(f"fixed wall {number_of_walls + i}")
                i += 1
        elif ram_state[28] == 3:
            wall_instance = LavaWall()
            wall_instance.xy = (144, 61)
            wall_instance.wh = (16, 37)
            objects_map['lava wall 0'] = wall_instance
            wall_instance = LavaWall()
            wall_instance.xy = (8, 61)
            wall_instance.wh = (8, 37)
            objects_map['lava wall 1'] = wall_instance
            number_of_lava_walls = 2
            i = 0
            while(objects_map.get(f"fixed wall {number_of_lava_walls + i}")!= None):
                objects_map.pop(f"fixed wall {number_of_lava_walls + i}")
                i += 1
            wall_instance = Wall()
            wall_instance.xy = (104, 21)
            wall_instance.wh = (56, 38)
            objects_map['fixed wall 0'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (8, 21)
            wall_instance.wh = (48, 38)
            objects_map['fixed wall 1'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (128, 101)
            wall_instance.wh = (32, 38)
            objects_map['fixed wall 2'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (40, 101)
            wall_instance.wh = (80, 38)
            objects_map['fixed wall 3'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (8, 101)
            wall_instance.wh = (24, 38)
            objects_map['fixed wall 4'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (144, 61)
            wall_instance.wh = (16, 37)
            objects_map['fixed wall 5'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (8, 61)
            wall_instance.wh = (8, 37)
            objects_map['fixed wall 6'] = wall_instance
            number_of_walls = 7
            i = 0
            while(objects_map.get(f"fixed wall {number_of_walls + i}")!= None):
                objects_map.pop(f"fixed wall {number_of_walls + i}")
                i += 1
        elif ram_state[28] == 4:
            wall_instance = LavaWall()
            wall_instance.xy = (144, 61)
            wall_instance.wh = (16, 37)
            objects_map['lava wall 0'] = wall_instance
            wall_instance = LavaWall()
            wall_instance.xy = (8, 61)
            wall_instance.wh = (8, 37)
            objects_map['lava wall 1'] = wall_instance
            number_of_lava_walls = 2
            i = 0
            while(objects_map.get(f"fixed wall {number_of_lava_walls + i}")!= None):
                objects_map.pop(f"fixed wall {number_of_lava_walls + i}")
                i += 1
            wall_instance = Wall()
            wall_instance.xy = (128, 21)
            wall_instance.wh = (32, 38)
            objects_map['fixed wall 0'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (40, 21)
            wall_instance.wh = (80, 38)
            objects_map['fixed wall 1'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (8, 21)
            wall_instance.wh = (24, 38)
            objects_map['fixed wall 2'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (96, 101)
            wall_instance.wh = (64, 38)
            objects_map['fixed wall 3'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (8, 101)
            wall_instance.wh = (56, 38)
            objects_map['fixed wall 4'] = wall_instance
            number_of_walls = 5
            i = 0
            while(objects_map.get(f"fixed wall {number_of_walls + i}")!= None):
                objects_map.pop(f"fixed wall {number_of_walls + i}")
                i += 1
        elif ram_state[28] == 5:
            wall_instance = LavaWall()
            wall_instance.xy = (144, 61)
            wall_instance.wh = (16, 37)
            objects_map['lava wall 0'] = wall_instance
            wall_instance = LavaWall()
            wall_instance.xy = (8, 61)
            wall_instance.wh = (8, 37)
            objects_map['lava wall 1'] = wall_instance
            number_of_lava_walls = 2
            i = 0
            while(objects_map.get(f"fixed wall {number_of_lava_walls + i}")!= None):
                objects_map.pop(f"fixed wall {number_of_lava_walls + i}")
                i += 1
            wall_instance = Wall()
            wall_instance.xy = (96, 21)
            wall_instance.wh = (64, 38)
            objects_map['fixed wall 0'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (8, 21)
            wall_instance.wh = (56, 38)
            objects_map['fixed wall 1'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (136, 101)
            wall_instance.wh = (24, 38)
            objects_map['fixed wall 2'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (84, 101)
            wall_instance.wh = (44, 38)
            objects_map['fixed wall 3'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (32, 101)
            wall_instance.wh = (44, 38)
            objects_map['fixed wall 4'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (8, 101)
            wall_instance.wh = (16, 38)
            objects_map['fixed wall 5'] = wall_instance
            number_of_walls = 6
            i = 0
            while(objects_map.get(f"fixed wall {number_of_walls + i}")!= None):
                objects_map.pop(f"fixed wall {number_of_walls + i}")
                i += 1
        elif ram_state[28] == 6:
            wall_instance = LavaWall()
            wall_instance.xy = (144, 61)
            wall_instance.wh = (16, 37)
            objects_map['lava wall 0'] = wall_instance
            wall_instance = LavaWall()
            wall_instance.xy = (64, 61)
            wall_instance.wh = (32, 37)
            objects_map['lava wall 1'] = wall_instance
            wall_instance = LavaWall()
            wall_instance.xy = (8, 61)
            wall_instance.wh = (8, 37)
            objects_map['lava wall 2'] = wall_instance
            number_of_lava_walls = 3
            i = 0
            while(objects_map.get(f"fixed wall {number_of_lava_walls + i}")!= None):
                objects_map.pop(f"fixed wall {number_of_lava_walls + i}")
                i += 1
            wall_instance = Wall()
            wall_instance.xy = (136, 21)
            wall_instance.wh = (24, 38)
            objects_map['fixed wall 0'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (84, 21)
            wall_instance.wh = (44, 38)
            objects_map['fixed wall 1'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (32, 21)
            wall_instance.wh = (44, 38)
            objects_map['fixed wall 2'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (8, 21)
            wall_instance.wh = (16, 38)
            objects_map['fixed wall 3'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (136, 101)
            wall_instance.wh = (24, 38)
            objects_map['fixed wall 4'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (48, 101)
            wall_instance.wh = (64, 38)
            objects_map['fixed wall 5'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (8, 101)
            wall_instance.wh = (16, 38)
            objects_map['fixed wall 6'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (144, 61)
            wall_instance.wh = (16, 37)
            objects_map['fixed wall 7'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (64, 61)
            wall_instance.wh = (32, 37)
            objects_map['fixed wall 8'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (8, 61)
            wall_instance.wh = (8, 37)
            objects_map['fixed wall 9'] = wall_instance
            number_of_walls = 10
            i = 0
            while(objects_map.get(f"fixed wall {number_of_walls + i}")!= None):
                objects_map.pop(f"fixed wall {number_of_walls + i}")
                i += 1
        elif ram_state[28] == 7:
            wall_instance = LavaWall()
            wall_instance.xy = (144, 61)
            wall_instance.wh = (16, 37)
            objects_map['lava wall 0'] = wall_instance
            wall_instance = LavaWall()
            wall_instance.xy = (8, 61)
            wall_instance.wh = (8, 37)
            objects_map['lava wall 1'] = wall_instance
            number_of_lava_walls = 2
            i = 0
            while(objects_map.get(f"fixed wall {number_of_lava_walls + i}")!= None):
                objects_map.pop(f"fixed wall {number_of_lava_walls + i}")
                i += 1
            wall_instance = Wall()
            wall_instance.xy = (136, 21)
            wall_instance.wh = (24, 38)
            objects_map['fixed wall 0'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (48, 21)
            wall_instance.wh = (64, 38)
            objects_map['fixed wall 1'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (8, 21)
            wall_instance.wh = (16, 38)
            objects_map['fixed wall 2'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (136, 101)
            wall_instance.wh = (24, 38)
            objects_map['fixed wall 3'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (32, 101)
            wall_instance.wh = (96, 38)
            objects_map['fixed wall 4'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (8, 101)
            wall_instance.wh = (16, 38)
            objects_map['fixed wall 5'] = wall_instance
            number_of_walls = 6
            i = 0
            while(objects_map.get(f"fixed wall {number_of_walls + i}")!= None):
                objects_map.pop(f"fixed wall {number_of_walls + i}")
                i += 1
        elif ram_state[28] == 8:
            wall_instance = LavaWall()
            wall_instance.xy = (144, 61)
            wall_instance.wh = (16, 37)
            objects_map['lava wall 0'] = wall_instance
            wall_instance = LavaWall()
            wall_instance.xy = (8, 61)
            wall_instance.wh = (8, 37)
            objects_map['lava wall 1'] = wall_instance
            number_of_lava_walls = 2
            i = 0
            while(objects_map.get(f"fixed wall {number_of_lava_walls + i}")!= None):
                objects_map.pop(f"fixed wall {number_of_lava_walls + i}")
                i += 1
            wall_instance = Wall()
            wall_instance.xy = (136, 21)
            wall_instance.wh = (24, 38)
            objects_map['fixed wall 0'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (32, 21)
            wall_instance.wh = (96, 38)
            objects_map['fixed wall 1'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (8, 21)
            wall_instance.wh = (16, 38)
            objects_map['fixed wall 2'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (136, 101)
            wall_instance.wh = (24, 38)
            objects_map['fixed wall 3'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (84, 101)
            wall_instance.wh = (44, 38)
            objects_map['fixed wall 4'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (32, 101)
            wall_instance.wh = (44, 38)
            objects_map['fixed wall 5'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (8, 101)
            wall_instance.wh = (16, 38)
            objects_map['fixed wall 6'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (144, 61)
            wall_instance.wh = (16, 37)
            objects_map['fixed wall 7'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (8, 61)
            wall_instance.wh = (8, 37)
            objects_map['fixed wall 8'] = wall_instance
            number_of_walls = 9
            i = 0
            while(objects_map.get(f"fixed wall {number_of_walls + i}")!= None):
                objects_map.pop(f"fixed wall {number_of_walls + i}")
                i += 1
        elif ram_state[28] == 9:
            wall_instance = LavaWall()
            wall_instance.xy = (84, 61)
            wall_instance.wh = (76, 37)
            objects_map['lava wall 0'] = wall_instance
            wall_instance = LavaWall()
            wall_instance.xy = (8, 61)
            wall_instance.wh = (68, 37)
            objects_map['lava wall 1'] = wall_instance
            number_of_lava_walls = 2
            i = 0
            while(objects_map.get(f"fixed wall {number_of_lava_walls + i}")!= None):
                objects_map.pop(f"fixed wall {number_of_lava_walls + i}")
                i += 1
            wall_instance = Wall()
            wall_instance.xy = (136, 21)
            wall_instance.wh = (24, 38)
            objects_map['fixed wall 0'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (84, 21)
            wall_instance.wh = (44, 38)
            objects_map['fixed wall 1'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (32, 21)
            wall_instance.wh = (44, 38)
            objects_map['fixed wall 2'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (8, 21)
            wall_instance.wh = (16, 38)
            objects_map['fixed wall 3'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (88, 101)
            wall_instance.wh = (72, 38)
            objects_map['fixed wall 4'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (8, 101)
            wall_instance.wh = (64, 38)
            objects_map['fixed wall 5'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (84, 61)
            wall_instance.wh = (76, 37)
            objects_map['fixed wall 6'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (8, 61)
            wall_instance.wh = (68, 37)
            objects_map['fixed wall 7'] = wall_instance
            number_of_walls = 8
            i = 0
            while(objects_map.get(f"fixed wall {number_of_walls + i}")!= None):
                objects_map.pop(f"fixed wall {number_of_walls + i}")
                i += 1
        elif ram_state[28] == 10:
            number_of_lava_walls = 0
            i = 0
            while(objects_map.get(f"fixed wall {number_of_lava_walls + i}")!= None):
                objects_map.pop(f"fixed wall {number_of_lava_walls + i}")
                i += 1
            wall_instance = Wall()
            wall_instance.xy = (88, 21)
            wall_instance.wh = (72, 38)
            objects_map['fixed wall 0'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (8, 21)
            wall_instance.wh = (64, 38)
            objects_map['fixed wall 1'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (120, 101)
            wall_instance.wh = (40, 38)
            objects_map['fixed wall 2'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (8, 101)
            wall_instance.wh = (32, 38)
            objects_map['fixed wall 3'] = wall_instance
            number_of_walls = 4
            i = 0
            while(objects_map.get(f"fixed wall {number_of_walls + i}")!= None):
                objects_map.pop(f"fixed wall {number_of_walls + i}")
                i += 1
        elif ram_state[28] == 11:
            number_of_lava_walls = 0
            i = 0
            while(objects_map.get(f"fixed wall {number_of_lava_walls + i}")!= None):
                objects_map.pop(f"fixed wall {number_of_lava_walls + i}")
                i += 1
            wall_instance = Wall()
            wall_instance.xy = (8, 21)
            wall_instance.wh = (152, 38)
            objects_map['fixed wall 0'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (144, 101)
            wall_instance.wh = (16, 38)
            objects_map['fixed wall 1'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (72, 101)
            wall_instance.wh = (16, 38)
            objects_map['fixed wall 2'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (8, 101)
            wall_instance.wh = (8, 38)
            objects_map['fixed wall 3'] = wall_instance
            number_of_walls = 4
            i = 0
            while(objects_map.get(f"fixed wall {number_of_walls + i}")!= None):
                objects_map.pop(f"fixed wall {number_of_walls + i}")
                i += 1
        elif ram_state[28] == 12:
            number_of_lava_walls = 0
            i = 0
            while(objects_map.get(f"fixed wall {number_of_lava_walls + i}")!= None):
                objects_map.pop(f"fixed wall {number_of_lava_walls + i}")
                i += 1
            wall_instance = Wall()
            wall_instance.xy = (8, 21)
            wall_instance.wh = (152, 38)
            objects_map['fixed wall 0'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (144, 101)
            wall_instance.wh = (16, 38)
            objects_map['fixed wall 1'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (64, 101)
            wall_instance.wh = (32, 38)
            objects_map['fixed wall 2'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (8, 101)
            wall_instance.wh = (8, 38)
            objects_map['fixed wall 3'] = wall_instance
            number_of_walls = 4
            i = 0
            while(objects_map.get(f"fixed wall {number_of_walls + i}")!= None):
                objects_map.pop(f"fixed wall {number_of_walls + i}")
                i += 1
        elif ram_state[28] == 13:
            wall_instance = LavaWall()
            wall_instance.xy = (48, 61)
            wall_instance.wh = (64, 37)
            objects_map['lava wall 0'] = wall_instance
            number_of_lava_walls = 1
            i = 0
            while(objects_map.get(f"fixed wall {number_of_lava_walls + i}")!= None):
                objects_map.pop(f"fixed wall {number_of_lava_walls + i}")
                i += 1
            wall_instance = Wall()
            wall_instance.xy = (8, 21)
            wall_instance.wh = (152, 38)
            objects_map['fixed wall 0'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (136, 101)
            wall_instance.wh = (24, 38)
            objects_map['fixed wall 1'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (8, 101)
            wall_instance.wh = (16, 38)
            objects_map['fixed wall 2'] = wall_instance
            number_of_walls = 3
            i = 0
            while(objects_map.get(f"fixed wall {number_of_walls + i}")!= None):
                objects_map.pop(f"fixed wall {number_of_walls + i}")
                i += 1
        elif ram_state[28] == 14:
            number_of_lava_walls = 0
            i = 0
            while(objects_map.get(f"fixed wall {number_of_lava_walls + i}")!= None):
                objects_map.pop(f"fixed wall {number_of_lava_walls + i}")
                i += 1
            wall_instance = Wall()
            wall_instance.xy = (8, 21)
            wall_instance.wh = (152, 38)
            objects_map['fixed wall 0'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (8, 101)
            wall_instance.wh = (152, 38)
            objects_map['fixed wall 1'] = wall_instance
            number_of_walls = 2
            i = 0
            while(objects_map.get(f"fixed wall {number_of_walls + i}")!= None):
                objects_map.pop(f"fixed wall {number_of_walls + i}")
                i += 1
        elif ram_state[28] == 15:
            number_of_lava_walls = 0
            i = 0
            while(objects_map.get(f"fixed wall {number_of_lava_walls + i}")!= None):
                objects_map.pop(f"fixed wall {number_of_lava_walls + i}")
                i += 1
            wall_instance = Wall()
            wall_instance.xy = (8, 21)
            wall_instance.wh = (152, 38)
            objects_map['fixed wall 0'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (112, 101)
            wall_instance.wh = (48, 38)
            objects_map['fixed wall 1'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (60, 101)
            wall_instance.wh = (40, 38)
            objects_map['fixed wall 2'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (8, 101)
            wall_instance.wh = (40, 38)
            objects_map['fixed wall 3'] = wall_instance
            number_of_walls = 4
            i = 0
            while(objects_map.get(f"fixed wall {number_of_walls + i}")!= None):
                objects_map.pop(f"fixed wall {number_of_walls + i}")
                i += 1

    elif ram_state[117] == 15:
        if ram_state[28] == 0:
            wall_instance = LavaWall()
            wall_instance.xy = (144, 61)
            wall_instance.wh = (16, 37)
            objects_map['lava wall 0'] = wall_instance
            wall_instance = LavaWall()
            wall_instance.xy = (8, 61)
            wall_instance.wh = (8, 37)
            objects_map['lava wall 1'] = wall_instance
            number_of_lava_walls = 2
            i = 0
            while(objects_map.get(f"fixed wall {number_of_lava_walls + i}")!= None):
                objects_map.pop(f"fixed wall {number_of_lava_walls + i}")
                i += 1
            wall_instance = Wall()
            wall_instance.xy = (136, 21)
            wall_instance.wh = (24, 38)
            objects_map['fixed wall 0'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (8, 21)
            wall_instance.wh = (16, 38)
            objects_map['fixed wall 1'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (136, 101)
            wall_instance.wh = (24, 38)
            objects_map['fixed wall 2'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (88, 101)
            wall_instance.wh = (40, 38)
            objects_map['fixed wall 3'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (32, 101)
            wall_instance.wh = (40, 38)
            objects_map['fixed wall 4'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (8, 101)
            wall_instance.wh = (16, 38)
            objects_map['fixed wall 5'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (144, 61)
            wall_instance.wh = (16, 37)
            objects_map['fixed wall 6'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (8, 61)
            wall_instance.wh = (8, 37)
            objects_map['fixed wall 7'] = wall_instance
            number_of_walls = 8
            i = 0
            while(objects_map.get(f"fixed wall {number_of_walls + i}")!= None):
                objects_map.pop(f"fixed wall {number_of_walls + i}")
                i += 1
        elif ram_state[28] == 1:
            wall_instance = LavaWall()
            wall_instance.xy = (144, 61)
            wall_instance.wh = (16, 37)
            objects_map['lava wall 0'] = wall_instance
            wall_instance = LavaWall()
            wall_instance.xy = (64, 61)
            wall_instance.wh = (32, 37)
            objects_map['lava wall 1'] = wall_instance
            wall_instance = LavaWall()
            wall_instance.xy = (8, 61)
            wall_instance.wh = (8, 37)
            objects_map['lava wall 2'] = wall_instance
            number_of_lava_walls = 3
            i = 0
            while(objects_map.get(f"fixed wall {number_of_lava_walls + i}")!= None):
                objects_map.pop(f"fixed wall {number_of_lava_walls + i}")
                i += 1
            wall_instance = Wall()
            wall_instance.xy = (136, 21)
            wall_instance.wh = (24, 38)
            objects_map['fixed wall 0'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (88, 21)
            wall_instance.wh = (40, 38)
            objects_map['fixed wall 1'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (32, 21)
            wall_instance.wh = (40, 38)
            objects_map['fixed wall 2'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (8, 21)
            wall_instance.wh = (16, 38)
            objects_map['fixed wall 3'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (8, 101)
            wall_instance.wh = (152, 38)
            objects_map['fixed wall 4'] = wall_instance
            number_of_walls = 5
            i = 0
            while(objects_map.get(f"fixed wall {number_of_walls + i}")!= None):
                objects_map.pop(f"fixed wall {number_of_walls + i}")
                i += 1
        elif ram_state[28] == 2:
            wall_instance = LavaWall()
            wall_instance.xy = (144, 61)
            wall_instance.wh = (16, 37)
            objects_map['lava wall 0'] = wall_instance
            wall_instance = LavaWall()
            wall_instance.xy = (68, 61)
            wall_instance.wh = (24, 37)
            objects_map['lava wall 1'] = wall_instance
            wall_instance = LavaWall()
            wall_instance.xy = (8, 61)
            wall_instance.wh = (8, 37)
            objects_map['lava wall 2'] = wall_instance
            number_of_lava_walls = 3
            i = 0
            while(objects_map.get(f"fixed wall {number_of_lava_walls + i}")!= None):
                objects_map.pop(f"fixed wall {number_of_lava_walls + i}")
                i += 1
            wall_instance = Wall()
            wall_instance.xy = (8, 21)
            wall_instance.wh = (152, 38)
            objects_map['fixed wall 0'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (128, 101)
            wall_instance.wh = (32, 38)
            objects_map['fixed wall 1'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (8, 101)
            wall_instance.wh = (24, 38)
            objects_map['fixed wall 2'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (144, 61)
            wall_instance.wh = (16, 37)
            objects_map['fixed wall 3'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (68, 61)
            wall_instance.wh = (24, 37)
            objects_map['fixed wall 4'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (8, 61)
            wall_instance.wh = (8, 37)
            objects_map['fixed wall 5'] = wall_instance
            number_of_walls = 6
            i = 0
            while(objects_map.get(f"fixed wall {number_of_walls + i}")!= None):
                objects_map.pop(f"fixed wall {number_of_walls + i}")
                i += 1
        elif ram_state[28] == 3:
            wall_instance = LavaWall()
            wall_instance.xy = (104, 61)
            wall_instance.wh = (56, 37)
            objects_map['lava wall 0'] = wall_instance
            wall_instance = LavaWall()
            wall_instance.xy = (8, 61)
            wall_instance.wh = (48, 37)
            objects_map['lava wall 1'] = wall_instance
            number_of_lava_walls = 2
            i = 0
            while(objects_map.get(f"fixed wall {number_of_lava_walls + i}")!= None):
                objects_map.pop(f"fixed wall {number_of_lava_walls + i}")
                i += 1
            wall_instance = Wall()
            wall_instance.xy = (128, 21)
            wall_instance.wh = (32, 38)
            objects_map['fixed wall 0'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (8, 21)
            wall_instance.wh = (24, 38)
            objects_map['fixed wall 1'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (112, 101)
            wall_instance.wh = (48, 38)
            objects_map['fixed wall 2'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (8, 101)
            wall_instance.wh = (40, 38)
            objects_map['fixed wall 3'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (104, 61)
            wall_instance.wh = (56, 37)
            objects_map['fixed wall 4'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (8, 61)
            wall_instance.wh = (48, 37)
            objects_map['fixed wall 5'] = wall_instance
            number_of_walls = 6
            i = 0
            while(objects_map.get(f"fixed wall {number_of_walls + i}")!= None):
                objects_map.pop(f"fixed wall {number_of_walls + i}")
                i += 1
        elif ram_state[28] == 4:
            wall_instance = LavaWall()
            wall_instance.xy = (144, 61)
            wall_instance.wh = (16, 37)
            objects_map['lava wall 0'] = wall_instance
            wall_instance = LavaWall()
            wall_instance.xy = (72, 61)
            wall_instance.wh = (16, 37)
            objects_map['lava wall 1'] = wall_instance
            wall_instance = LavaWall()
            wall_instance.xy = (8, 61)
            wall_instance.wh = (8, 37)
            objects_map['lava wall 2'] = wall_instance
            number_of_lava_walls = 3
            i = 0
            while(objects_map.get(f"fixed wall {number_of_lava_walls + i}")!= None):
                objects_map.pop(f"fixed wall {number_of_lava_walls + i}")
                i += 1
            wall_instance = Wall()
            wall_instance.xy = (112, 21)
            wall_instance.wh = (48, 38)
            objects_map['fixed wall 0'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (8, 21)
            wall_instance.wh = (40, 38)
            objects_map['fixed wall 1'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (140, 101)
            wall_instance.wh = (20, 38)
            objects_map['fixed wall 2'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (28, 101)
            wall_instance.wh = (104, 38)
            objects_map['fixed wall 3'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (8, 101)
            wall_instance.wh = (12, 38)
            objects_map['fixed wall 4'] = wall_instance
            number_of_walls = 5
            i = 0
            while(objects_map.get(f"fixed wall {number_of_walls + i}")!= None):
                objects_map.pop(f"fixed wall {number_of_walls + i}")
                i += 1
        elif ram_state[28] == 5:
            wall_instance = LavaWall()
            wall_instance.xy = (144, 61)
            wall_instance.wh = (16, 37)
            objects_map['lava wall 0'] = wall_instance
            wall_instance = LavaWall()
            wall_instance.xy = (68, 61)
            wall_instance.wh = (24, 37)
            objects_map['lava wall 1'] = wall_instance
            wall_instance = LavaWall()
            wall_instance.xy = (8, 61)
            wall_instance.wh = (8, 37)
            objects_map['lava wall 2'] = wall_instance
            number_of_lava_walls = 3
            i = 0
            while(objects_map.get(f"fixed wall {number_of_lava_walls + i}")!= None):
                objects_map.pop(f"fixed wall {number_of_lava_walls + i}")
                i += 1
            wall_instance = Wall()
            wall_instance.xy = (140, 21)
            wall_instance.wh = (20, 38)
            objects_map['fixed wall 0'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (28, 21)
            wall_instance.wh = (104, 38)
            objects_map['fixed wall 1'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (8, 21)
            wall_instance.wh = (12, 38)
            objects_map['fixed wall 2'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (108, 101)
            wall_instance.wh = (52, 38)
            objects_map['fixed wall 3'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (8, 101)
            wall_instance.wh = (44, 38)
            objects_map['fixed wall 4'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (144, 61)
            wall_instance.wh = (16, 37)
            objects_map['fixed wall 5'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (68, 61)
            wall_instance.wh = (24, 37)
            objects_map['fixed wall 6'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (8, 61)
            wall_instance.wh = (8, 37)
            objects_map['fixed wall 7'] = wall_instance
            number_of_walls = 8
            i = 0
            while(objects_map.get(f"fixed wall {number_of_walls + i}")!= None):
                objects_map.pop(f"fixed wall {number_of_walls + i}")
                i += 1
        elif ram_state[28] == 6:
            wall_instance = LavaWall()
            wall_instance.xy = (104, 61)
            wall_instance.wh = (56, 37)
            objects_map['lava wall 0'] = wall_instance
            wall_instance = LavaWall()
            wall_instance.xy = (64, 61)
            wall_instance.wh = (32, 37)
            objects_map['lava wall 1'] = wall_instance
            wall_instance = LavaWall()
            wall_instance.xy = (8, 61)
            wall_instance.wh = (48, 37)
            objects_map['lava wall 2'] = wall_instance
            number_of_lava_walls = 3
            i = 0
            while(objects_map.get(f"fixed wall {number_of_lava_walls + i}")!= None):
                objects_map.pop(f"fixed wall {number_of_lava_walls + i}")
                i += 1
            wall_instance = Wall()
            wall_instance.xy = (108, 21)
            wall_instance.wh = (52, 38)
            objects_map['fixed wall 0'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (8, 21)
            wall_instance.wh = (44, 38)
            objects_map['fixed wall 1'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (144, 101)
            wall_instance.wh = (16, 38)
            objects_map['fixed wall 2'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (8, 101)
            wall_instance.wh = (8, 38)
            objects_map['fixed wall 3'] = wall_instance
            number_of_walls = 4
            i = 0
            while(objects_map.get(f"fixed wall {number_of_walls + i}")!= None):
                objects_map.pop(f"fixed wall {number_of_walls + i}")
                i += 1
        elif ram_state[28] == 7:
            wall_instance = LavaWall()
            wall_instance.xy = (84, 61)
            wall_instance.wh = (76, 37)
            objects_map['lava wall 0'] = wall_instance
            wall_instance = LavaWall()
            wall_instance.xy = (8, 61)
            wall_instance.wh = (68, 37)
            objects_map['lava wall 1'] = wall_instance
            number_of_lava_walls = 2
            i = 0
            while(objects_map.get(f"fixed wall {number_of_lava_walls + i}")!= None):
                objects_map.pop(f"fixed wall {number_of_lava_walls + i}")
                i += 1
            wall_instance = Wall()
            wall_instance.xy = (144, 21)
            wall_instance.wh = (16, 38)
            objects_map['fixed wall 0'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (8, 21)
            wall_instance.wh = (8, 38)
            objects_map['fixed wall 1'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (144, 101)
            wall_instance.wh = (16, 38)
            objects_map['fixed wall 2'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (8, 101)
            wall_instance.wh = (8, 38)
            objects_map['fixed wall 3'] = wall_instance
            number_of_walls = 4
            i = 0
            while(objects_map.get(f"fixed wall {number_of_walls + i}")!= None):
                objects_map.pop(f"fixed wall {number_of_walls + i}")
                i += 1
        elif ram_state[28] == 8:
            wall_instance = LavaWall()
            wall_instance.xy = (112, 61)
            wall_instance.wh = (48, 37)
            objects_map['lava wall 0'] = wall_instance
            wall_instance = LavaWall()
            wall_instance.xy = (84, 61)
            wall_instance.wh = (20, 37)
            objects_map['lava wall 1'] = wall_instance
            wall_instance = LavaWall()
            wall_instance.xy = (56, 61)
            wall_instance.wh = (20, 37)
            objects_map['lava wall 2'] = wall_instance
            wall_instance = LavaWall()
            wall_instance.xy = (8, 61)
            wall_instance.wh = (40, 37)
            objects_map['lava wall 3'] = wall_instance
            number_of_lava_walls = 4
            i = 0
            while(objects_map.get(f"fixed wall {number_of_lava_walls + i}")!= None):
                objects_map.pop(f"fixed wall {number_of_lava_walls + i}")
                i += 1
            wall_instance = Wall()
            wall_instance.xy = (144, 21)
            wall_instance.wh = (16, 38)
            objects_map['fixed wall 0'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (8, 21)
            wall_instance.wh = (8, 38)
            objects_map['fixed wall 1'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (144, 101)
            wall_instance.wh = (16, 38)
            objects_map['fixed wall 2'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (8, 101)
            wall_instance.wh = (8, 38)
            objects_map['fixed wall 3'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (112, 61)
            wall_instance.wh = (48, 37)
            objects_map['fixed wall 4'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (84, 61)
            wall_instance.wh = (20, 37)
            objects_map['fixed wall 5'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (56, 61)
            wall_instance.wh = (20, 37)
            objects_map['fixed wall 6'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (8, 61)
            wall_instance.wh = (40, 37)
            objects_map['fixed wall 7'] = wall_instance
            number_of_walls = 8
            i = 0
            while(objects_map.get(f"fixed wall {number_of_walls + i}")!= None):
                objects_map.pop(f"fixed wall {number_of_walls + i}")
                i += 1
        elif ram_state[28] == 9:
            wall_instance = LavaWall()
            wall_instance.xy = (92, 61)
            wall_instance.wh = (68, 37)
            objects_map['lava wall 0'] = wall_instance
            wall_instance = LavaWall()
            wall_instance.xy = (8, 61)
            wall_instance.wh = (60, 37)
            objects_map['lava wall 1'] = wall_instance
            number_of_lava_walls = 2
            i = 0
            while(objects_map.get(f"fixed wall {number_of_lava_walls + i}")!= None):
                objects_map.pop(f"fixed wall {number_of_lava_walls + i}")
                i += 1
            wall_instance = Wall()
            wall_instance.xy = (144, 21)
            wall_instance.wh = (16, 38)
            objects_map['fixed wall 0'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (8, 21)
            wall_instance.wh = (8, 38)
            objects_map['fixed wall 1'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (128, 101)
            wall_instance.wh = (32, 38)
            objects_map['fixed wall 2'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (8, 101)
            wall_instance.wh = (24, 38)
            objects_map['fixed wall 3'] = wall_instance
            number_of_walls = 4
            i = 0
            while(objects_map.get(f"fixed wall {number_of_walls + i}")!= None):
                objects_map.pop(f"fixed wall {number_of_walls + i}")
                i += 1
        elif ram_state[28] == 10:
            wall_instance = LavaWall()
            wall_instance.xy = (72, 61)
            wall_instance.wh = (16, 37)
            objects_map['lava wall 0'] = wall_instance
            number_of_lava_walls = 1
            i = 0
            while(objects_map.get(f"fixed wall {number_of_lava_walls + i}")!= None):
                objects_map.pop(f"fixed wall {number_of_lava_walls + i}")
                i += 1
            wall_instance = Wall()
            wall_instance.xy = (128, 21)
            wall_instance.wh = (32, 38)
            objects_map['fixed wall 0'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (8, 21)
            wall_instance.wh = (24, 38)
            objects_map['fixed wall 1'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (136, 101)
            wall_instance.wh = (24, 38)
            objects_map['fixed wall 2'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (8, 101)
            wall_instance.wh = (16, 38)
            objects_map['fixed wall 3'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (72, 61)
            wall_instance.wh = (16, 37)
            objects_map['fixed wall 4'] = wall_instance
            number_of_walls = 5
            i = 0
            while(objects_map.get(f"fixed wall {number_of_walls + i}")!= None):
                objects_map.pop(f"fixed wall {number_of_walls + i}")
                i += 1
        elif ram_state[28] == 11:
            wall_instance = LavaWall()
            wall_instance.xy = (48, 61)
            wall_instance.wh = (64, 37)
            objects_map['lava wall 0'] = wall_instance
            number_of_lava_walls = 1
            i = 0
            while(objects_map.get(f"fixed wall {number_of_lava_walls + i}")!= None):
                objects_map.pop(f"fixed wall {number_of_lava_walls + i}")
                i += 1
            wall_instance = Wall()
            wall_instance.xy = (8, 21)
            wall_instance.wh = (152, 38)
            objects_map['fixed wall 0'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (136, 101)
            wall_instance.wh = (24, 38)
            objects_map['fixed wall 1'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (8, 101)
            wall_instance.wh = (16, 38)
            objects_map['fixed wall 2'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (48, 61)
            wall_instance.wh = (64, 37)
            objects_map['fixed wall 3'] = wall_instance
            number_of_walls = 4
            i = 0
            while(objects_map.get(f"fixed wall {number_of_walls + i}")!= None):
                objects_map.pop(f"fixed wall {number_of_walls + i}")
                i += 1
        elif ram_state[28] == 12:
            number_of_lava_walls = 0
            i = 0
            while(objects_map.get(f"fixed wall {number_of_lava_walls + i}")!= None):
                objects_map.pop(f"fixed wall {number_of_lava_walls + i}")
                i += 1
            wall_instance = Wall()
            wall_instance.xy = (8, 21)
            wall_instance.wh = (152, 38)
            objects_map['fixed wall 0'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (132, 101)
            wall_instance.wh = (28, 38)
            objects_map['fixed wall 1'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (72, 101)
            wall_instance.wh = (16, 38)
            objects_map['fixed wall 2'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (8, 101)
            wall_instance.wh = (20, 38)
            objects_map['fixed wall 3'] = wall_instance
            number_of_walls = 4
            i = 0
            while(objects_map.get(f"fixed wall {number_of_walls + i}")!= None):
                objects_map.pop(f"fixed wall {number_of_walls + i}")
                i += 1
        elif ram_state[28] == 13:
            wall_instance = LavaWall()
            wall_instance.xy = (40, 61)
            wall_instance.wh = (80, 37)
            objects_map['lava wall 0'] = wall_instance
            number_of_lava_walls = 1
            i = 0
            while(objects_map.get(f"fixed wall {number_of_lava_walls + i}")!= None):
                objects_map.pop(f"fixed wall {number_of_lava_walls + i}")
                i += 1
            wall_instance = Wall()
            wall_instance.xy = (8, 21)
            wall_instance.wh = (152, 38)
            objects_map['fixed wall 0'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (136, 101)
            wall_instance.wh = (24, 38)
            objects_map['fixed wall 1'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (8, 101)
            wall_instance.wh = (16, 38)
            objects_map['fixed wall 2'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (40, 61)
            wall_instance.wh = (80, 37)
            objects_map['fixed wall 3'] = wall_instance
            number_of_walls = 4
            i = 0
            while(objects_map.get(f"fixed wall {number_of_walls + i}")!= None):
                objects_map.pop(f"fixed wall {number_of_walls + i}")
                i += 1
        elif ram_state[28] == 14:
            number_of_lava_walls = 0
            i = 0
            while(objects_map.get(f"fixed wall {number_of_lava_walls + i}")!= None):
                objects_map.pop(f"fixed wall {number_of_lava_walls + i}")
                i += 1
            wall_instance = Wall()
            wall_instance.xy = (8, 21)
            wall_instance.wh = (152, 38)
            objects_map['fixed wall 0'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (128, 101)
            wall_instance.wh = (32, 38)
            objects_map['fixed wall 1'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (68, 101)
            wall_instance.wh = (24, 38)
            objects_map['fixed wall 2'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (8, 101)
            wall_instance.wh = (24, 38)
            objects_map['fixed wall 3'] = wall_instance
            number_of_walls = 4
            i = 0
            while(objects_map.get(f"fixed wall {number_of_walls + i}")!= None):
                objects_map.pop(f"fixed wall {number_of_walls + i}")
                i += 1
        elif ram_state[28] == 15:
            wall_instance = LavaWall()
            wall_instance.xy = (72, 61)
            wall_instance.wh = (16, 37)
            objects_map['lava wall 0'] = wall_instance
            number_of_lava_walls = 1
            i = 0
            while(objects_map.get(f"fixed wall {number_of_lava_walls + i}")!= None):
                objects_map.pop(f"fixed wall {number_of_lava_walls + i}")
                i += 1
            wall_instance = Wall()
            wall_instance.xy = (8, 21)
            wall_instance.wh = (152, 38)
            objects_map['fixed wall 0'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (112, 101)
            wall_instance.wh = (48, 38)
            objects_map['fixed wall 1'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (8, 101)
            wall_instance.wh = (40, 38)
            objects_map['fixed wall 2'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (72, 61)
            wall_instance.wh = (16, 37)
            objects_map['fixed wall 3'] = wall_instance
            number_of_walls = 4
            i = 0
            while(objects_map.get(f"fixed wall {number_of_walls + i}")!= None):
                objects_map.pop(f"fixed wall {number_of_walls + i}")
                i += 1

    elif ram_state[117] == 16:
        if ram_state[28] == 0:
            wall_instance = LavaWall()
            wall_instance.xy = (144, 61)
            wall_instance.wh = (16, 37)
            objects_map['lava wall 0'] = wall_instance
            wall_instance = LavaWall()
            wall_instance.xy = (8, 61)
            wall_instance.wh = (8, 37)
            objects_map['lava wall 1'] = wall_instance
            number_of_lava_walls = 2
            i = 0
            while(objects_map.get(f"fixed wall {number_of_lava_walls + i}")!= None):
                objects_map.pop(f"fixed wall {number_of_lava_walls + i}")
                i += 1
            wall_instance = Wall()
            wall_instance.xy = (136, 21)
            wall_instance.wh = (24, 38)
            objects_map['fixed wall 0'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (8, 21)
            wall_instance.wh = (16, 38)
            objects_map['fixed wall 1'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (88, 101)
            wall_instance.wh = (72, 38)
            objects_map['fixed wall 2'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (8, 101)
            wall_instance.wh = (64, 38)
            objects_map['fixed wall 3'] = wall_instance
            number_of_walls = 4
            i = 0
            while(objects_map.get(f"fixed wall {number_of_walls + i}")!= None):
                objects_map.pop(f"fixed wall {number_of_walls + i}")
                i += 1
        elif ram_state[28] == 1:
            wall_instance = LavaWall()
            wall_instance.xy = (128, 61)
            wall_instance.wh = (32, 37)
            objects_map['lava wall 0'] = wall_instance
            wall_instance = LavaWall()
            wall_instance.xy = (8, 61)
            wall_instance.wh = (24, 37)
            objects_map['lava wall 1'] = wall_instance
            number_of_lava_walls = 2
            i = 0
            while(objects_map.get(f"fixed wall {number_of_lava_walls + i}")!= None):
                objects_map.pop(f"fixed wall {number_of_lava_walls + i}")
                i += 1
            wall_instance = Wall()
            wall_instance.xy = (88, 21)
            wall_instance.wh = (72, 38)
            objects_map['fixed wall 0'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (8, 21)
            wall_instance.wh = (64, 38)
            objects_map['fixed wall 1'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (144, 101)
            wall_instance.wh = (16, 38)
            objects_map['fixed wall 2'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (48, 101)
            wall_instance.wh = (64, 38)
            objects_map['fixed wall 3'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (8, 101)
            wall_instance.wh = (8, 38)
            objects_map['fixed wall 4'] = wall_instance
            number_of_walls = 5
            i = 0
            while(objects_map.get(f"fixed wall {number_of_walls + i}")!= None):
                objects_map.pop(f"fixed wall {number_of_walls + i}")
                i += 1
        elif ram_state[28] == 2:
            wall_instance = LavaWall()
            wall_instance.xy = (136, 61)
            wall_instance.wh = (24, 37)
            objects_map['lava wall 0'] = wall_instance
            wall_instance = LavaWall()
            wall_instance.xy = (40, 61)
            wall_instance.wh = (80, 37)
            objects_map['lava wall 1'] = wall_instance
            wall_instance = LavaWall()
            wall_instance.xy = (8, 61)
            wall_instance.wh = (16, 37)
            objects_map['lava wall 2'] = wall_instance
            number_of_lava_walls = 3
            i = 0
            while(objects_map.get(f"fixed wall {number_of_lava_walls + i}")!= None):
                objects_map.pop(f"fixed wall {number_of_lava_walls + i}")
                i += 1
            wall_instance = Wall()
            wall_instance.xy = (144, 21)
            wall_instance.wh = (16, 38)
            objects_map['fixed wall 0'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (48, 21)
            wall_instance.wh = (64, 38)
            objects_map['fixed wall 1'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (8, 21)
            wall_instance.wh = (8, 38)
            objects_map['fixed wall 2'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (128, 101)
            wall_instance.wh = (32, 38)
            objects_map['fixed wall 3'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (8, 101)
            wall_instance.wh = (24, 38)
            objects_map['fixed wall 4'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (136, 61)
            wall_instance.wh = (24, 37)
            objects_map['fixed wall 5'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (40, 61)
            wall_instance.wh = (80, 37)
            objects_map['fixed wall 6'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (8, 61)
            wall_instance.wh = (16, 37)
            objects_map['fixed wall 7'] = wall_instance
            number_of_walls = 8
            i = 0
            while(objects_map.get(f"fixed wall {number_of_walls + i}")!= None):
                objects_map.pop(f"fixed wall {number_of_walls + i}")
                i += 1
        elif ram_state[28] == 3:
            number_of_lava_walls = 0
            i = 0
            while(objects_map.get(f"fixed wall {number_of_lava_walls + i}")!= None):
                objects_map.pop(f"fixed wall {number_of_lava_walls + i}")
                i += 1
            wall_instance = Wall()
            wall_instance.xy = (128, 21)
            wall_instance.wh = (32, 38)
            objects_map['fixed wall 0'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (8, 21)
            wall_instance.wh = (24, 38)
            objects_map['fixed wall 1'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (144, 101)
            wall_instance.wh = (16, 38)
            objects_map['fixed wall 2'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (8, 101)
            wall_instance.wh = (8, 38)
            objects_map['fixed wall 3'] = wall_instance
            number_of_walls = 4
            i = 0
            while(objects_map.get(f"fixed wall {number_of_walls + i}")!= None):
                objects_map.pop(f"fixed wall {number_of_walls + i}")
                i += 1
        elif ram_state[28] == 4:
            wall_instance = LavaWall()
            wall_instance.xy = (104, 61)
            wall_instance.wh = (56, 37)
            objects_map['lava wall 0'] = wall_instance
            wall_instance = LavaWall()
            wall_instance.xy = (8, 61)
            wall_instance.wh = (48, 37)
            objects_map['lava wall 1'] = wall_instance
            number_of_lava_walls = 2
            i = 0
            while(objects_map.get(f"fixed wall {number_of_lava_walls + i}")!= None):
                objects_map.pop(f"fixed wall {number_of_lava_walls + i}")
                i += 1
            wall_instance = Wall()
            wall_instance.xy = (144, 21)
            wall_instance.wh = (16, 38)
            objects_map['fixed wall 0'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (8, 21)
            wall_instance.wh = (8, 38)
            objects_map['fixed wall 1'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (112, 101)
            wall_instance.wh = (48, 38)
            objects_map['fixed wall 2'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (8, 101)
            wall_instance.wh = (40, 38)
            objects_map['fixed wall 3'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (104, 61)
            wall_instance.wh = (56, 37)
            objects_map['fixed wall 4'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (8, 61)
            wall_instance.wh = (48, 37)
            objects_map['fixed wall 5'] = wall_instance
            number_of_walls = 6
            i = 0
            while(objects_map.get(f"fixed wall {number_of_walls + i}")!= None):
                objects_map.pop(f"fixed wall {number_of_walls + i}")
                i += 1
        elif ram_state[28] == 5:
            wall_instance = LavaWall()
            wall_instance.xy = (104, 61)
            wall_instance.wh = (56, 37)
            objects_map['lava wall 0'] = wall_instance
            wall_instance = LavaWall()
            wall_instance.xy = (8, 61)
            wall_instance.wh = (48, 37)
            objects_map['lava wall 1'] = wall_instance
            number_of_lava_walls = 2
            i = 0
            while(objects_map.get(f"fixed wall {number_of_lava_walls + i}")!= None):
                objects_map.pop(f"fixed wall {number_of_lava_walls + i}")
                i += 1
            wall_instance = Wall()
            wall_instance.xy = (112, 21)
            wall_instance.wh = (48, 38)
            objects_map['fixed wall 0'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (8, 21)
            wall_instance.wh = (40, 38)
            objects_map['fixed wall 1'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (84, 101)
            wall_instance.wh = (76, 38)
            objects_map['fixed wall 2'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (8, 101)
            wall_instance.wh = (68, 38)
            objects_map['fixed wall 3'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (104, 61)
            wall_instance.wh = (56, 37)
            objects_map['fixed wall 4'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (8, 61)
            wall_instance.wh = (48, 37)
            objects_map['fixed wall 5'] = wall_instance
            number_of_walls = 6
            i = 0
            while(objects_map.get(f"fixed wall {number_of_walls + i}")!= None):
                objects_map.pop(f"fixed wall {number_of_walls + i}")
                i += 1
        elif ram_state[28] == 6:
            wall_instance = LavaWall()
            wall_instance.xy = (144, 61)
            wall_instance.wh = (16, 37)
            objects_map['lava wall 0'] = wall_instance
            wall_instance = LavaWall()
            wall_instance.xy = (8, 61)
            wall_instance.wh = (8, 37)
            objects_map['lava wall 1'] = wall_instance
            number_of_lava_walls = 2
            i = 0
            while(objects_map.get(f"fixed wall {number_of_lava_walls + i}")!= None):
                objects_map.pop(f"fixed wall {number_of_lava_walls + i}")
                i += 1
            wall_instance = Wall()
            wall_instance.xy = (84, 21)
            wall_instance.wh = (76, 38)
            objects_map['fixed wall 0'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (8, 21)
            wall_instance.wh = (68, 38)
            objects_map['fixed wall 1'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (136, 101)
            wall_instance.wh = (24, 38)
            objects_map['fixed wall 2'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (32, 101)
            wall_instance.wh = (96, 38)
            objects_map['fixed wall 3'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (8, 101)
            wall_instance.wh = (16, 38)
            objects_map['fixed wall 4'] = wall_instance
            number_of_walls = 5
            i = 0
            while(objects_map.get(f"fixed wall {number_of_walls + i}")!= None):
                objects_map.pop(f"fixed wall {number_of_walls + i}")
                i += 1
        elif ram_state[28] == 7:
            wall_instance = LavaWall()
            wall_instance.xy = (144, 61)
            wall_instance.wh = (16, 37)
            objects_map['lava wall 0'] = wall_instance
            wall_instance = LavaWall()
            wall_instance.xy = (8, 61)
            wall_instance.wh = (8, 37)
            objects_map['lava wall 1'] = wall_instance
            number_of_lava_walls = 2
            i = 0
            while(objects_map.get(f"fixed wall {number_of_lava_walls + i}")!= None):
                objects_map.pop(f"fixed wall {number_of_lava_walls + i}")
                i += 1
            wall_instance = Wall()
            wall_instance.xy = (136, 21)
            wall_instance.wh = (24, 38)
            objects_map['fixed wall 0'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (32, 21)
            wall_instance.wh = (96, 38)
            objects_map['fixed wall 1'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (8, 21)
            wall_instance.wh = (16, 38)
            objects_map['fixed wall 2'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (8, 101)
            wall_instance.wh = (152, 38)
            objects_map['fixed wall 3'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (144, 61)
            wall_instance.wh = (16, 37)
            objects_map['fixed wall 4'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (8, 61)
            wall_instance.wh = (8, 37)
            objects_map['fixed wall 5'] = wall_instance
            number_of_walls = 6
            i = 0
            while(objects_map.get(f"fixed wall {number_of_walls + i}")!= None):
                objects_map.pop(f"fixed wall {number_of_walls + i}")
                i += 1
        elif ram_state[28] == 8:
            wall_instance = LavaWall()
            wall_instance.xy = (80, 61)
            wall_instance.wh = (32, 37)
            objects_map['lava wall 0'] = wall_instance
            wall_instance = LavaWall()
            wall_instance.xy = (8, 61)
            wall_instance.wh = (24, 37)
            objects_map['lava wall 1'] = wall_instance
            number_of_lava_walls = 2
            i = 0
            while(objects_map.get(f"fixed wall {number_of_lava_walls + i}")!= None):
                objects_map.pop(f"fixed wall {number_of_lava_walls + i}")
                i += 1
            wall_instance = Wall()
            wall_instance.xy = (8, 21)
            wall_instance.wh = (152, 38)
            objects_map['fixed wall 0'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (136, 101)
            wall_instance.wh = (24, 38)
            objects_map['fixed wall 1'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (8, 101)
            wall_instance.wh = (16, 38)
            objects_map['fixed wall 2'] = wall_instance
            number_of_walls = 3
            i = 0
            while(objects_map.get(f"fixed wall {number_of_walls + i}")!= None):
                objects_map.pop(f"fixed wall {number_of_walls + i}")
                i += 1
        elif ram_state[28] == 9:
            wall_instance = LavaWall()
            wall_instance.xy = (84, 61)
            wall_instance.wh = (76, 37)
            objects_map['lava wall 0'] = wall_instance
            wall_instance = LavaWall()
            wall_instance.xy = (8, 61)
            wall_instance.wh = (68, 37)
            objects_map['lava wall 1'] = wall_instance
            number_of_lava_walls = 2
            i = 0
            while(objects_map.get(f"fixed wall {number_of_lava_walls + i}")!= None):
                objects_map.pop(f"fixed wall {number_of_lava_walls + i}")
                i += 1
            wall_instance = Wall()
            wall_instance.xy = (136, 21)
            wall_instance.wh = (24, 38)
            objects_map['fixed wall 0'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (8, 21)
            wall_instance.wh = (16, 38)
            objects_map['fixed wall 1'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (108, 101)
            wall_instance.wh = (52, 38)
            objects_map['fixed wall 2'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (8, 101)
            wall_instance.wh = (44, 38)
            objects_map['fixed wall 3'] = wall_instance
            number_of_walls = 4
            i = 0
            while(objects_map.get(f"fixed wall {number_of_walls + i}")!= None):
                objects_map.pop(f"fixed wall {number_of_walls + i}")
                i += 1
        elif ram_state[28] == 10:
            number_of_lava_walls = 0
            i = 0
            while(objects_map.get(f"fixed wall {number_of_lava_walls + i}")!= None):
                objects_map.pop(f"fixed wall {number_of_lava_walls + i}")
                i += 1
            wall_instance = Wall()
            wall_instance.xy = (108, 21)
            wall_instance.wh = (52, 38)
            objects_map['fixed wall 0'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (8, 21)
            wall_instance.wh = (44, 38)
            objects_map['fixed wall 1'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (136, 101)
            wall_instance.wh = (24, 38)
            objects_map['fixed wall 2'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (36, 101)
            wall_instance.wh = (88, 38)
            objects_map['fixed wall 3'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (8, 101)
            wall_instance.wh = (16, 38)
            objects_map['fixed wall 4'] = wall_instance
            number_of_walls = 5
            i = 0
            while(objects_map.get(f"fixed wall {number_of_walls + i}")!= None):
                objects_map.pop(f"fixed wall {number_of_walls + i}")
                i += 1
        elif ram_state[28] == 11:
            number_of_lava_walls = 0
            i = 0
            while(objects_map.get(f"fixed wall {number_of_lava_walls + i}")!= None):
                objects_map.pop(f"fixed wall {number_of_lava_walls + i}")
                i += 1
            wall_instance = Wall()
            wall_instance.xy = (8, 21)
            wall_instance.wh = (152, 38)
            objects_map['fixed wall 0'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (132, 101)
            wall_instance.wh = (28, 38)
            objects_map['fixed wall 1'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (8, 101)
            wall_instance.wh = (20, 38)
            objects_map['fixed wall 2'] = wall_instance
            number_of_walls = 3
            i = 0
            while(objects_map.get(f"fixed wall {number_of_walls + i}")!= None):
                objects_map.pop(f"fixed wall {number_of_walls + i}")
                i += 1
        elif ram_state[28] == 12:
            number_of_lava_walls = 0
            i = 0
            while(objects_map.get(f"fixed wall {number_of_lava_walls + i}")!= None):
                objects_map.pop(f"fixed wall {number_of_lava_walls + i}")
                i += 1
            wall_instance = Wall()
            wall_instance.xy = (8, 21)
            wall_instance.wh = (152, 38)
            objects_map['fixed wall 0'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (132, 101)
            wall_instance.wh = (28, 38)
            objects_map['fixed wall 1'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (72, 101)
            wall_instance.wh = (16, 38)
            objects_map['fixed wall 2'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (8, 101)
            wall_instance.wh = (20, 38)
            objects_map['fixed wall 3'] = wall_instance
            number_of_walls = 4
            i = 0
            while(objects_map.get(f"fixed wall {number_of_walls + i}")!= None):
                objects_map.pop(f"fixed wall {number_of_walls + i}")
                i += 1
        elif ram_state[28] == 13:
            number_of_lava_walls = 0
            i = 0
            while(objects_map.get(f"fixed wall {number_of_lava_walls + i}")!= None):
                objects_map.pop(f"fixed wall {number_of_lava_walls + i}")
                i += 1
            wall_instance = Wall()
            wall_instance.xy = (8, 21)
            wall_instance.wh = (152, 38)
            objects_map['fixed wall 0'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (132, 101)
            wall_instance.wh = (28, 38)
            objects_map['fixed wall 1'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (72, 101)
            wall_instance.wh = (16, 38)
            objects_map['fixed wall 2'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (8, 101)
            wall_instance.wh = (20, 38)
            objects_map['fixed wall 3'] = wall_instance
            number_of_walls = 4
            i = 0
            while(objects_map.get(f"fixed wall {number_of_walls + i}")!= None):
                objects_map.pop(f"fixed wall {number_of_walls + i}")
                i += 1
        elif ram_state[28] == 14:
            wall_instance = LavaWall()
            wall_instance.xy = (48, 61)
            wall_instance.wh = (64, 37)
            objects_map['lava wall 0'] = wall_instance
            number_of_lava_walls = 1
            i = 0
            while(objects_map.get(f"fixed wall {number_of_lava_walls + i}")!= None):
                objects_map.pop(f"fixed wall {number_of_lava_walls + i}")
                i += 1
            wall_instance = Wall()
            wall_instance.xy = (8, 21)
            wall_instance.wh = (152, 38)
            objects_map['fixed wall 0'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (136, 101)
            wall_instance.wh = (24, 38)
            objects_map['fixed wall 1'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (8, 101)
            wall_instance.wh = (16, 38)
            objects_map['fixed wall 2'] = wall_instance
            number_of_walls = 3
            i = 0
            while(objects_map.get(f"fixed wall {number_of_walls + i}")!= None):
                objects_map.pop(f"fixed wall {number_of_walls + i}")
                i += 1
        elif ram_state[28] == 15:
            number_of_lava_walls = 0
            i = 0
            while(objects_map.get(f"fixed wall {number_of_lava_walls + i}")!= None):
                objects_map.pop(f"fixed wall {number_of_lava_walls + i}")
                i += 1
            wall_instance = Wall()
            wall_instance.xy = (8, 21)
            wall_instance.wh = (152, 38)
            objects_map['fixed wall 0'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (124, 101)
            wall_instance.wh = (36, 38)
            objects_map['fixed wall 1'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (8, 101)
            wall_instance.wh = (28, 38)
            objects_map['fixed wall 2'] = wall_instance
            number_of_walls = 3
            i = 0
            while(objects_map.get(f"fixed wall {number_of_walls + i}")!= None):
                objects_map.pop(f"fixed wall {number_of_walls + i}")
                i += 1

    elif ram_state[117] == 17:
        if ram_state[28] == 0:
            wall_instance = LavaWall()
            wall_instance.xy = (144, 61)
            wall_instance.wh = (16, 37)
            objects_map['lava wall 0'] = wall_instance
            wall_instance = LavaWall()
            wall_instance.xy = (8, 61)
            wall_instance.wh = (8, 37)
            objects_map['lava wall 1'] = wall_instance
            number_of_lava_walls = 2
            i = 0
            while(objects_map.get(f"fixed wall {number_of_lava_walls + i}")!= None):
                objects_map.pop(f"fixed wall {number_of_lava_walls + i}")
                i += 1
            wall_instance = Wall()
            wall_instance.xy = (136, 21)
            wall_instance.wh = (24, 38)
            objects_map['fixed wall 0'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (8, 21)
            wall_instance.wh = (16, 38)
            objects_map['fixed wall 1'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (88, 101)
            wall_instance.wh = (72, 38)
            objects_map['fixed wall 2'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (8, 101)
            wall_instance.wh = (64, 38)
            objects_map['fixed wall 3'] = wall_instance
            number_of_walls = 4
            i = 0
            while(objects_map.get(f"fixed wall {number_of_walls + i}")!= None):
                objects_map.pop(f"fixed wall {number_of_walls + i}")
                i += 1
        elif ram_state[28] == 1:
            wall_instance = LavaWall()
            wall_instance.xy = (144, 61)
            wall_instance.wh = (16, 37)
            objects_map['lava wall 0'] = wall_instance
            wall_instance = LavaWall()
            wall_instance.xy = (8, 61)
            wall_instance.wh = (8, 37)
            objects_map['lava wall 1'] = wall_instance
            number_of_lava_walls = 2
            i = 0
            while(objects_map.get(f"fixed wall {number_of_lava_walls + i}")!= None):
                objects_map.pop(f"fixed wall {number_of_lava_walls + i}")
                i += 1
            wall_instance = Wall()
            wall_instance.xy = (88, 21)
            wall_instance.wh = (72, 38)
            objects_map['fixed wall 0'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (8, 21)
            wall_instance.wh = (64, 38)
            objects_map['fixed wall 1'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (136, 101)
            wall_instance.wh = (24, 38)
            objects_map['fixed wall 2'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (48, 101)
            wall_instance.wh = (64, 38)
            objects_map['fixed wall 3'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (8, 101)
            wall_instance.wh = (16, 38)
            objects_map['fixed wall 4'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (144, 61)
            wall_instance.wh = (16, 37)
            objects_map['fixed wall 5'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (8, 61)
            wall_instance.wh = (8, 37)
            objects_map['fixed wall 6'] = wall_instance
            number_of_walls = 7
            i = 0
            while(objects_map.get(f"fixed wall {number_of_walls + i}")!= None):
                objects_map.pop(f"fixed wall {number_of_walls + i}")
                i += 1
        elif ram_state[28] == 2:
            wall_instance = LavaWall()
            wall_instance.xy = (144, 61)
            wall_instance.wh = (16, 37)
            objects_map['lava wall 0'] = wall_instance
            wall_instance = LavaWall()
            wall_instance.xy = (36, 61)
            wall_instance.wh = (88, 37)
            objects_map['lava wall 1'] = wall_instance
            wall_instance = LavaWall()
            wall_instance.xy = (8, 61)
            wall_instance.wh = (8, 37)
            objects_map['lava wall 2'] = wall_instance
            number_of_lava_walls = 3
            i = 0
            while(objects_map.get(f"fixed wall {number_of_lava_walls + i}")!= None):
                objects_map.pop(f"fixed wall {number_of_lava_walls + i}")
                i += 1
            wall_instance = Wall()
            wall_instance.xy = (136, 21)
            wall_instance.wh = (24, 38)
            objects_map['fixed wall 0'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (48, 21)
            wall_instance.wh = (64, 38)
            objects_map['fixed wall 1'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (8, 21)
            wall_instance.wh = (16, 38)
            objects_map['fixed wall 2'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (132, 101)
            wall_instance.wh = (28, 38)
            objects_map['fixed wall 3'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (48, 101)
            wall_instance.wh = (64, 38)
            objects_map['fixed wall 4'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (8, 101)
            wall_instance.wh = (20, 38)
            objects_map['fixed wall 5'] = wall_instance
            number_of_walls = 6
            i = 0
            while(objects_map.get(f"fixed wall {number_of_walls + i}")!= None):
                objects_map.pop(f"fixed wall {number_of_walls + i}")
                i += 1
        elif ram_state[28] == 3:
            wall_instance = LavaWall()
            wall_instance.xy = (144, 61)
            wall_instance.wh = (16, 37)
            objects_map['lava wall 0'] = wall_instance
            wall_instance = LavaWall()
            wall_instance.xy = (8, 61)
            wall_instance.wh = (8, 37)
            objects_map['lava wall 1'] = wall_instance
            number_of_lava_walls = 2
            i = 0
            while(objects_map.get(f"fixed wall {number_of_lava_walls + i}")!= None):
                objects_map.pop(f"fixed wall {number_of_lava_walls + i}")
                i += 1
            wall_instance = Wall()
            wall_instance.xy = (132, 21)
            wall_instance.wh = (28, 38)
            objects_map['fixed wall 0'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (48, 21)
            wall_instance.wh = (64, 38)
            objects_map['fixed wall 1'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (8, 21)
            wall_instance.wh = (20, 38)
            objects_map['fixed wall 2'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (88, 101)
            wall_instance.wh = (72, 38)
            objects_map['fixed wall 3'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (8, 101)
            wall_instance.wh = (64, 38)
            objects_map['fixed wall 4'] = wall_instance
            number_of_walls = 5
            i = 0
            while(objects_map.get(f"fixed wall {number_of_walls + i}")!= None):
                objects_map.pop(f"fixed wall {number_of_walls + i}")
                i += 1
        elif ram_state[28] == 4:
            wall_instance = LavaWall()
            wall_instance.xy = (144, 61)
            wall_instance.wh = (16, 37)
            objects_map['lava wall 0'] = wall_instance
            wall_instance = LavaWall()
            wall_instance.xy = (8, 61)
            wall_instance.wh = (8, 37)
            objects_map['lava wall 1'] = wall_instance
            number_of_lava_walls = 2
            i = 0
            while(objects_map.get(f"fixed wall {number_of_lava_walls + i}")!= None):
                objects_map.pop(f"fixed wall {number_of_lava_walls + i}")
                i += 1
            wall_instance = Wall()
            wall_instance.xy = (88, 21)
            wall_instance.wh = (72, 38)
            objects_map['fixed wall 0'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (8, 21)
            wall_instance.wh = (64, 38)
            objects_map['fixed wall 1'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (136, 101)
            wall_instance.wh = (24, 38)
            objects_map['fixed wall 2'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (32, 101)
            wall_instance.wh = (96, 38)
            objects_map['fixed wall 3'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (8, 101)
            wall_instance.wh = (16, 38)
            objects_map['fixed wall 4'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (144, 61)
            wall_instance.wh = (16, 37)
            objects_map['fixed wall 5'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (8, 61)
            wall_instance.wh = (8, 37)
            objects_map['fixed wall 6'] = wall_instance
            number_of_walls = 7
            i = 0
            while(objects_map.get(f"fixed wall {number_of_walls + i}")!= None):
                objects_map.pop(f"fixed wall {number_of_walls + i}")
                i += 1
        elif ram_state[28] == 5:
            wall_instance = LavaWall()
            wall_instance.xy = (144, 61)
            wall_instance.wh = (16, 37)
            objects_map['lava wall 0'] = wall_instance
            wall_instance = LavaWall()
            wall_instance.xy = (8, 61)
            wall_instance.wh = (8, 37)
            objects_map['lava wall 1'] = wall_instance
            number_of_lava_walls = 2
            i = 0
            while(objects_map.get(f"fixed wall {number_of_lava_walls + i}")!= None):
                objects_map.pop(f"fixed wall {number_of_lava_walls + i}")
                i += 1
            wall_instance = Wall()
            wall_instance.xy = (136, 21)
            wall_instance.wh = (24, 38)
            objects_map['fixed wall 0'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (32, 21)
            wall_instance.wh = (96, 38)
            objects_map['fixed wall 1'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (8, 21)
            wall_instance.wh = (16, 38)
            objects_map['fixed wall 2'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (8, 101)
            wall_instance.wh = (152, 38)
            objects_map['fixed wall 3'] = wall_instance
            number_of_walls = 4
            i = 0
            while(objects_map.get(f"fixed wall {number_of_walls + i}")!= None):
                objects_map.pop(f"fixed wall {number_of_walls + i}")
                i += 1
        elif ram_state[28] == 6:
            wall_instance = LavaWall()
            wall_instance.xy = (144, 61)
            wall_instance.wh = (16, 37)
            objects_map['lava wall 0'] = wall_instance
            wall_instance = LavaWall()
            wall_instance.xy = (8, 61)
            wall_instance.wh = (8, 37)
            objects_map['lava wall 1'] = wall_instance
            number_of_lava_walls = 2
            i = 0
            while(objects_map.get(f"fixed wall {number_of_lava_walls + i}")!= None):
                objects_map.pop(f"fixed wall {number_of_lava_walls + i}")
                i += 1
            wall_instance = Wall()
            wall_instance.xy = (8, 21)
            wall_instance.wh = (152, 38)
            objects_map['fixed wall 0'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (128, 101)
            wall_instance.wh = (32, 38)
            objects_map['fixed wall 1'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (68, 101)
            wall_instance.wh = (24, 38)
            objects_map['fixed wall 2'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (8, 101)
            wall_instance.wh = (24, 38)
            objects_map['fixed wall 3'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (144, 61)
            wall_instance.wh = (16, 37)
            objects_map['fixed wall 4'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (8, 61)
            wall_instance.wh = (8, 37)
            objects_map['fixed wall 5'] = wall_instance
            number_of_walls = 6
            i = 0
            while(objects_map.get(f"fixed wall {number_of_walls + i}")!= None):
                objects_map.pop(f"fixed wall {number_of_walls + i}")
                i += 1
        elif ram_state[28] == 7:
            wall_instance = LavaWall()
            wall_instance.xy = (112, 61)
            wall_instance.wh = (48, 37)
            objects_map['lava wall 0'] = wall_instance
            wall_instance = LavaWall()
            wall_instance.xy = (8, 61)
            wall_instance.wh = (40, 37)
            objects_map['lava wall 1'] = wall_instance
            number_of_lava_walls = 2
            i = 0
            while(objects_map.get(f"fixed wall {number_of_lava_walls + i}")!= None):
                objects_map.pop(f"fixed wall {number_of_lava_walls + i}")
                i += 1
            wall_instance = Wall()
            wall_instance.xy = (128, 21)
            wall_instance.wh = (32, 38)
            objects_map['fixed wall 0'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (68, 21)
            wall_instance.wh = (24, 38)
            objects_map['fixed wall 1'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (8, 21)
            wall_instance.wh = (24, 38)
            objects_map['fixed wall 2'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (84, 101)
            wall_instance.wh = (76, 38)
            objects_map['fixed wall 3'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (8, 101)
            wall_instance.wh = (68, 38)
            objects_map['fixed wall 4'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (112, 61)
            wall_instance.wh = (48, 37)
            objects_map['fixed wall 5'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (8, 61)
            wall_instance.wh = (40, 37)
            objects_map['fixed wall 6'] = wall_instance
            number_of_walls = 7
            i = 0
            while(objects_map.get(f"fixed wall {number_of_walls + i}")!= None):
                objects_map.pop(f"fixed wall {number_of_walls + i}")
                i += 1
        elif ram_state[28] == 8:
            wall_instance = LavaWall()
            wall_instance.xy = (84, 61)
            wall_instance.wh = (76, 37)
            objects_map['lava wall 0'] = wall_instance
            wall_instance = LavaWall()
            wall_instance.xy = (8, 61)
            wall_instance.wh = (68, 37)
            objects_map['lava wall 1'] = wall_instance
            number_of_lava_walls = 2
            i = 0
            while(objects_map.get(f"fixed wall {number_of_lava_walls + i}")!= None):
                objects_map.pop(f"fixed wall {number_of_lava_walls + i}")
                i += 1
            wall_instance = Wall()
            wall_instance.xy = (84, 21)
            wall_instance.wh = (76, 38)
            objects_map['fixed wall 0'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (8, 21)
            wall_instance.wh = (68, 38)
            objects_map['fixed wall 1'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (84, 101)
            wall_instance.wh = (76, 38)
            objects_map['fixed wall 2'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (8, 101)
            wall_instance.wh = (68, 38)
            objects_map['fixed wall 3'] = wall_instance
            number_of_walls = 4
            i = 0
            while(objects_map.get(f"fixed wall {number_of_walls + i}")!= None):
                objects_map.pop(f"fixed wall {number_of_walls + i}")
                i += 1
        elif ram_state[28] == 9:
            wall_instance = LavaWall()
            wall_instance.xy = (144, 61)
            wall_instance.wh = (16, 37)
            objects_map['lava wall 0'] = wall_instance
            wall_instance = LavaWall()
            wall_instance.xy = (92, 61)
            wall_instance.wh = (12, 37)
            objects_map['lava wall 1'] = wall_instance
            wall_instance = LavaWall()
            wall_instance.xy = (56, 61)
            wall_instance.wh = (12, 37)
            objects_map['lava wall 2'] = wall_instance
            wall_instance = LavaWall()
            wall_instance.xy = (8, 61)
            wall_instance.wh = (8, 37)
            objects_map['lava wall 3'] = wall_instance
            number_of_lava_walls = 4
            i = 0
            while(objects_map.get(f"fixed wall {number_of_lava_walls + i}")!= None):
                objects_map.pop(f"fixed wall {number_of_lava_walls + i}")
                i += 1
            wall_instance = Wall()
            wall_instance.xy = (84, 21)
            wall_instance.wh = (76, 38)
            objects_map['fixed wall 0'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (8, 21)
            wall_instance.wh = (68, 38)
            objects_map['fixed wall 1'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (140, 101)
            wall_instance.wh = (20, 38)
            objects_map['fixed wall 2'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (112, 101)
            wall_instance.wh = (20, 38)
            objects_map['fixed wall 3'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (84, 101)
            wall_instance.wh = (20, 38)
            objects_map['fixed wall 4'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (56, 101)
            wall_instance.wh = (20, 38)
            objects_map['fixed wall 5'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (28, 101)
            wall_instance.wh = (20, 38)
            objects_map['fixed wall 6'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (8, 101)
            wall_instance.wh = (12, 38)
            objects_map['fixed wall 7'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (144, 61)
            wall_instance.wh = (16, 37)
            objects_map['fixed wall 8'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (92, 61)
            wall_instance.wh = (12, 37)
            objects_map['fixed wall 9'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (56, 61)
            wall_instance.wh = (12, 37)
            objects_map['fixed wall 10'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (8, 61)
            wall_instance.wh = (8, 37)
            objects_map['fixed wall 11'] = wall_instance
            number_of_walls = 12
            i = 0
            while(objects_map.get(f"fixed wall {number_of_walls + i}")!= None):
                objects_map.pop(f"fixed wall {number_of_walls + i}")
                i += 1
        elif ram_state[28] == 10:
            wall_instance = LavaWall()
            wall_instance.xy = (116, 61)
            wall_instance.wh = (12, 37)
            objects_map['lava wall 0'] = wall_instance
            wall_instance = LavaWall()
            wall_instance.xy = (32, 61)
            wall_instance.wh = (12, 37)
            objects_map['lava wall 1'] = wall_instance
            number_of_lava_walls = 2
            i = 0
            while(objects_map.get(f"fixed wall {number_of_lava_walls + i}")!= None):
                objects_map.pop(f"fixed wall {number_of_lava_walls + i}")
                i += 1
            wall_instance = Wall()
            wall_instance.xy = (140, 21)
            wall_instance.wh = (20, 38)
            objects_map['fixed wall 0'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (112, 21)
            wall_instance.wh = (20, 38)
            objects_map['fixed wall 1'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (84, 21)
            wall_instance.wh = (20, 38)
            objects_map['fixed wall 2'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (56, 21)
            wall_instance.wh = (20, 38)
            objects_map['fixed wall 3'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (28, 21)
            wall_instance.wh = (20, 38)
            objects_map['fixed wall 4'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (8, 21)
            wall_instance.wh = (12, 38)
            objects_map['fixed wall 5'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (8, 101)
            wall_instance.wh = (152, 38)
            objects_map['fixed wall 6'] = wall_instance
            number_of_walls = 7
            i = 0
            while(objects_map.get(f"fixed wall {number_of_walls + i}")!= None):
                objects_map.pop(f"fixed wall {number_of_walls + i}")
                i += 1
        elif ram_state[28] == 11:
            number_of_lava_walls = 0
            i = 0
            while(objects_map.get(f"fixed wall {number_of_lava_walls + i}")!= None):
                objects_map.pop(f"fixed wall {number_of_lava_walls + i}")
                i += 1
            wall_instance = Wall()
            wall_instance.xy = (8, 21)
            wall_instance.wh = (152, 38)
            objects_map['fixed wall 0'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (132, 101)
            wall_instance.wh = (28, 38)
            objects_map['fixed wall 1'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (8, 101)
            wall_instance.wh = (20, 38)
            objects_map['fixed wall 2'] = wall_instance
            number_of_walls = 3
            i = 0
            while(objects_map.get(f"fixed wall {number_of_walls + i}")!= None):
                objects_map.pop(f"fixed wall {number_of_walls + i}")
                i += 1
        elif ram_state[28] == 12:
            wall_instance = LavaWall()
            wall_instance.xy = (48, 61)
            wall_instance.wh = (64, 37)
            objects_map['lava wall 0'] = wall_instance
            number_of_lava_walls = 1
            i = 0
            while(objects_map.get(f"fixed wall {number_of_lava_walls + i}")!= None):
                objects_map.pop(f"fixed wall {number_of_lava_walls + i}")
                i += 1
            wall_instance = Wall()
            wall_instance.xy = (8, 21)
            wall_instance.wh = (152, 38)
            objects_map['fixed wall 0'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (136, 101)
            wall_instance.wh = (24, 38)
            objects_map['fixed wall 1'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (8, 101)
            wall_instance.wh = (16, 38)
            objects_map['fixed wall 2'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (48, 61)
            wall_instance.wh = (64, 37)
            objects_map['fixed wall 3'] = wall_instance
            number_of_walls = 4
            i = 0
            while(objects_map.get(f"fixed wall {number_of_walls + i}")!= None):
                objects_map.pop(f"fixed wall {number_of_walls + i}")
                i += 1
        elif ram_state[28] == 13:
            number_of_lava_walls = 0
            i = 0
            while(objects_map.get(f"fixed wall {number_of_lava_walls + i}")!= None):
                objects_map.pop(f"fixed wall {number_of_lava_walls + i}")
                i += 1
            wall_instance = Wall()
            wall_instance.xy = (8, 21)
            wall_instance.wh = (152, 38)
            objects_map['fixed wall 0'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (132, 101)
            wall_instance.wh = (28, 38)
            objects_map['fixed wall 1'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (72, 101)
            wall_instance.wh = (16, 38)
            objects_map['fixed wall 2'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (8, 101)
            wall_instance.wh = (20, 38)
            objects_map['fixed wall 3'] = wall_instance
            number_of_walls = 4
            i = 0
            while(objects_map.get(f"fixed wall {number_of_walls + i}")!= None):
                objects_map.pop(f"fixed wall {number_of_walls + i}")
                i += 1
        elif ram_state[28] == 14:
            number_of_lava_walls = 0
            i = 0
            while(objects_map.get(f"fixed wall {number_of_lava_walls + i}")!= None):
                objects_map.pop(f"fixed wall {number_of_lava_walls + i}")
                i += 1
            wall_instance = Wall()
            wall_instance.xy = (8, 21)
            wall_instance.wh = (152, 38)
            objects_map['fixed wall 0'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (112, 101)
            wall_instance.wh = (48, 38)
            objects_map['fixed wall 1'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (8, 101)
            wall_instance.wh = (40, 38)
            objects_map['fixed wall 2'] = wall_instance
            number_of_walls = 3
            i = 0
            while(objects_map.get(f"fixed wall {number_of_walls + i}")!= None):
                objects_map.pop(f"fixed wall {number_of_walls + i}")
                i += 1
        elif ram_state[28] == 15:
            wall_instance = LavaWall()
            wall_instance.xy = (72, 61)
            wall_instance.wh = (16, 37)
            objects_map['lava wall 0'] = wall_instance
            number_of_lava_walls = 1
            i = 0
            while(objects_map.get(f"fixed wall {number_of_lava_walls + i}")!= None):
                objects_map.pop(f"fixed wall {number_of_lava_walls + i}")
                i += 1
            wall_instance = Wall()
            wall_instance.xy = (8, 21)
            wall_instance.wh = (152, 38)
            objects_map['fixed wall 0'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (120, 101)
            wall_instance.wh = (40, 38)
            objects_map['fixed wall 1'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (8, 101)
            wall_instance.wh = (32, 38)
            objects_map['fixed wall 2'] = wall_instance
            number_of_walls = 3
            i = 0
            while(objects_map.get(f"fixed wall {number_of_walls + i}")!= None):
                objects_map.pop(f"fixed wall {number_of_walls + i}")
                i += 1

    elif ram_state[117] == 18:
        if ram_state[28] == 0:
            wall_instance = LavaWall()
            wall_instance.xy = (144, 61)
            wall_instance.wh = (16, 37)
            objects_map['lava wall 0'] = wall_instance
            wall_instance = LavaWall()
            wall_instance.xy = (8, 61)
            wall_instance.wh = (8, 37)
            objects_map['lava wall 1'] = wall_instance
            number_of_lava_walls = 2
            i = 0
            while(objects_map.get(f"fixed wall {number_of_lava_walls + i}")!= None):
                objects_map.pop(f"fixed wall {number_of_lava_walls + i}")
                i += 1
            wall_instance = Wall()
            wall_instance.xy = (136, 21)
            wall_instance.wh = (24, 38)
            objects_map['fixed wall 0'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (8, 21)
            wall_instance.wh = (16, 38)
            objects_map['fixed wall 1'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (84, 101)
            wall_instance.wh = (76, 38)
            objects_map['fixed wall 2'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (8, 101)
            wall_instance.wh = (68, 38)
            objects_map['fixed wall 3'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (144, 61)
            wall_instance.wh = (16, 37)
            objects_map['fixed wall 4'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (8, 61)
            wall_instance.wh = (8, 37)
            objects_map['fixed wall 5'] = wall_instance
            number_of_walls = 6
            i = 0
            while(objects_map.get(f"fixed wall {number_of_walls + i}")!= None):
                objects_map.pop(f"fixed wall {number_of_walls + i}")
                i += 1
        elif ram_state[28] == 1:
            wall_instance = LavaWall()
            wall_instance.xy = (144, 61)
            wall_instance.wh = (16, 37)
            objects_map['lava wall 0'] = wall_instance
            wall_instance = LavaWall()
            wall_instance.xy = (8, 61)
            wall_instance.wh = (8, 37)
            objects_map['lava wall 1'] = wall_instance
            number_of_lava_walls = 2
            i = 0
            while(objects_map.get(f"fixed wall {number_of_lava_walls + i}")!= None):
                objects_map.pop(f"fixed wall {number_of_lava_walls + i}")
                i += 1
            wall_instance = Wall()
            wall_instance.xy = (84, 21)
            wall_instance.wh = (76, 38)
            objects_map['fixed wall 0'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (8, 21)
            wall_instance.wh = (68, 38)
            objects_map['fixed wall 1'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (120, 101)
            wall_instance.wh = (40, 38)
            objects_map['fixed wall 2'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (48, 101)
            wall_instance.wh = (64, 38)
            objects_map['fixed wall 3'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (8, 101)
            wall_instance.wh = (32, 38)
            objects_map['fixed wall 4'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (144, 61)
            wall_instance.wh = (16, 37)
            objects_map['fixed wall 5'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (8, 61)
            wall_instance.wh = (8, 37)
            objects_map['fixed wall 6'] = wall_instance
            number_of_walls = 7
            i = 0
            while(objects_map.get(f"fixed wall {number_of_walls + i}")!= None):
                objects_map.pop(f"fixed wall {number_of_walls + i}")
                i += 1
        elif ram_state[28] == 2:
            wall_instance = LavaWall()
            wall_instance.xy = (148, 61)
            wall_instance.wh = (12, 37)
            objects_map['lava wall 0'] = wall_instance
            wall_instance = LavaWall()
            wall_instance.xy = (68, 61)
            wall_instance.wh = (40, 37)
            objects_map['lava wall 1'] = wall_instance
            wall_instance = LavaWall()
            wall_instance.xy = (8, 61)
            wall_instance.wh = (20, 37)
            objects_map['lava wall 2'] = wall_instance
            number_of_lava_walls = 3
            i = 0
            while(objects_map.get(f"fixed wall {number_of_lava_walls + i}")!= None):
                objects_map.pop(f"fixed wall {number_of_lava_walls + i}")
                i += 1
            wall_instance = Wall()
            wall_instance.xy = (120, 21)
            wall_instance.wh = (40, 38)
            objects_map['fixed wall 0'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (48, 21)
            wall_instance.wh = (64, 38)
            objects_map['fixed wall 1'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (8, 21)
            wall_instance.wh = (32, 38)
            objects_map['fixed wall 2'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (100, 101)
            wall_instance.wh = (60, 38)
            objects_map['fixed wall 3'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (8, 101)
            wall_instance.wh = (52, 38)
            objects_map['fixed wall 4'] = wall_instance
            number_of_walls = 5
            i = 0
            while(objects_map.get(f"fixed wall {number_of_walls + i}")!= None):
                objects_map.pop(f"fixed wall {number_of_walls + i}")
                i += 1
        elif ram_state[28] == 3:
            wall_instance = LavaWall()
            wall_instance.xy = (128, 61)
            wall_instance.wh = (32, 37)
            objects_map['lava wall 0'] = wall_instance
            wall_instance = LavaWall()
            wall_instance.xy = (8, 61)
            wall_instance.wh = (24, 37)
            objects_map['lava wall 1'] = wall_instance
            number_of_lava_walls = 2
            i = 0
            while(objects_map.get(f"fixed wall {number_of_lava_walls + i}")!= None):
                objects_map.pop(f"fixed wall {number_of_lava_walls + i}")
                i += 1
            wall_instance = Wall()
            wall_instance.xy = (100, 21)
            wall_instance.wh = (60, 38)
            objects_map['fixed wall 0'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (8, 21)
            wall_instance.wh = (52, 38)
            objects_map['fixed wall 1'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (144, 101)
            wall_instance.wh = (16, 38)
            objects_map['fixed wall 2'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (44, 101)
            wall_instance.wh = (72, 38)
            objects_map['fixed wall 3'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (8, 101)
            wall_instance.wh = (8, 38)
            objects_map['fixed wall 4'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (128, 61)
            wall_instance.wh = (32, 37)
            objects_map['fixed wall 5'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (8, 61)
            wall_instance.wh = (24, 37)
            objects_map['fixed wall 6'] = wall_instance
            number_of_walls = 7
            i = 0
            while(objects_map.get(f"fixed wall {number_of_walls + i}")!= None):
                objects_map.pop(f"fixed wall {number_of_walls + i}")
                i += 1
        elif ram_state[28] == 4:
            wall_instance = LavaWall()
            wall_instance.xy = (136, 61)
            wall_instance.wh = (24, 37)
            objects_map['lava wall 0'] = wall_instance
            wall_instance = LavaWall()
            wall_instance.xy = (56, 61)
            wall_instance.wh = (64, 37)
            objects_map['lava wall 1'] = wall_instance
            wall_instance = LavaWall()
            wall_instance.xy = (8, 61)
            wall_instance.wh = (32, 37)
            objects_map['lava wall 2'] = wall_instance
            number_of_lava_walls = 3
            i = 0
            while(objects_map.get(f"fixed wall {number_of_lava_walls + i}")!= None):
                objects_map.pop(f"fixed wall {number_of_lava_walls + i}")
                i += 1
            wall_instance = Wall()
            wall_instance.xy = (144, 21)
            wall_instance.wh = (16, 38)
            objects_map['fixed wall 0'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (44, 21)
            wall_instance.wh = (72, 38)
            objects_map['fixed wall 1'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (8, 21)
            wall_instance.wh = (8, 38)
            objects_map['fixed wall 2'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (144, 101)
            wall_instance.wh = (16, 38)
            objects_map['fixed wall 3'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (36, 101)
            wall_instance.wh = (88, 38)
            objects_map['fixed wall 4'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (8, 101)
            wall_instance.wh = (8, 38)
            objects_map['fixed wall 5'] = wall_instance
            number_of_walls = 6
            i = 0
            while(objects_map.get(f"fixed wall {number_of_walls + i}")!= None):
                objects_map.pop(f"fixed wall {number_of_walls + i}")
                i += 1
        elif ram_state[28] == 5:
            wall_instance = LavaWall()
            wall_instance.xy = (136, 61)
            wall_instance.wh = (24, 37)
            objects_map['lava wall 0'] = wall_instance
            wall_instance = LavaWall()
            wall_instance.xy = (8, 61)
            wall_instance.wh = (16, 37)
            objects_map['lava wall 1'] = wall_instance
            number_of_lava_walls = 2
            i = 0
            while(objects_map.get(f"fixed wall {number_of_lava_walls + i}")!= None):
                objects_map.pop(f"fixed wall {number_of_lava_walls + i}")
                i += 1
            wall_instance = Wall()
            wall_instance.xy = (144, 21)
            wall_instance.wh = (16, 38)
            objects_map['fixed wall 0'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (36, 21)
            wall_instance.wh = (88, 38)
            objects_map['fixed wall 1'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (8, 21)
            wall_instance.wh = (8, 38)
            objects_map['fixed wall 2'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (84, 101)
            wall_instance.wh = (76, 38)
            objects_map['fixed wall 3'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (8, 101)
            wall_instance.wh = (68, 38)
            objects_map['fixed wall 4'] = wall_instance
            number_of_walls = 5
            i = 0
            while(objects_map.get(f"fixed wall {number_of_walls + i}")!= None):
                objects_map.pop(f"fixed wall {number_of_walls + i}")
                i += 1
        elif ram_state[28] == 6:
            wall_instance = LavaWall()
            wall_instance.xy = (92, 61)
            wall_instance.wh = (68, 37)
            objects_map['lava wall 0'] = wall_instance
            wall_instance = LavaWall()
            wall_instance.xy = (8, 61)
            wall_instance.wh = (60, 37)
            objects_map['lava wall 1'] = wall_instance
            number_of_lava_walls = 2
            i = 0
            while(objects_map.get(f"fixed wall {number_of_lava_walls + i}")!= None):
                objects_map.pop(f"fixed wall {number_of_lava_walls + i}")
                i += 1
            wall_instance = Wall()
            wall_instance.xy = (84, 21)
            wall_instance.wh = (76, 38)
            objects_map['fixed wall 0'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (8, 21)
            wall_instance.wh = (68, 38)
            objects_map['fixed wall 1'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (112, 101)
            wall_instance.wh = (48, 38)
            objects_map['fixed wall 2'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (8, 101)
            wall_instance.wh = (40, 38)
            objects_map['fixed wall 3'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (92, 61)
            wall_instance.wh = (68, 37)
            objects_map['fixed wall 4'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (8, 61)
            wall_instance.wh = (60, 37)
            objects_map['fixed wall 5'] = wall_instance
            number_of_walls = 6
            i = 0
            while(objects_map.get(f"fixed wall {number_of_walls + i}")!= None):
                objects_map.pop(f"fixed wall {number_of_walls + i}")
                i += 1
        elif ram_state[28] == 7:
            number_of_lava_walls = 0
            i = 0
            while(objects_map.get(f"fixed wall {number_of_lava_walls + i}")!= None):
                objects_map.pop(f"fixed wall {number_of_lava_walls + i}")
                i += 1
            wall_instance = Wall()
            wall_instance.xy = (112, 21)
            wall_instance.wh = (48, 38)
            objects_map['fixed wall 0'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (8, 21)
            wall_instance.wh = (40, 38)
            objects_map['fixed wall 1'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (116, 101)
            wall_instance.wh = (44, 38)
            objects_map['fixed wall 2'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (8, 101)
            wall_instance.wh = (36, 38)
            objects_map['fixed wall 3'] = wall_instance
            number_of_walls = 4
            i = 0
            while(objects_map.get(f"fixed wall {number_of_walls + i}")!= None):
                objects_map.pop(f"fixed wall {number_of_walls + i}")
                i += 1
        elif ram_state[28] == 8:
            wall_instance = LavaWall()
            wall_instance.xy = (88, 61)
            wall_instance.wh = (72, 37)
            objects_map['lava wall 0'] = wall_instance
            wall_instance = LavaWall()
            wall_instance.xy = (8, 61)
            wall_instance.wh = (64, 37)
            objects_map['lava wall 1'] = wall_instance
            number_of_lava_walls = 2
            i = 0
            while(objects_map.get(f"fixed wall {number_of_lava_walls + i}")!= None):
                objects_map.pop(f"fixed wall {number_of_lava_walls + i}")
                i += 1
            wall_instance = Wall()
            wall_instance.xy = (116, 21)
            wall_instance.wh = (44, 38)
            objects_map['fixed wall 0'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (8, 21)
            wall_instance.wh = (36, 38)
            objects_map['fixed wall 1'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (144, 101)
            wall_instance.wh = (16, 38)
            objects_map['fixed wall 2'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (8, 101)
            wall_instance.wh = (8, 38)
            objects_map['fixed wall 3'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (88, 61)
            wall_instance.wh = (72, 37)
            objects_map['fixed wall 4'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (8, 61)
            wall_instance.wh = (64, 37)
            objects_map['fixed wall 5'] = wall_instance
            number_of_walls = 6
            i = 0
            while(objects_map.get(f"fixed wall {number_of_walls + i}")!= None):
                objects_map.pop(f"fixed wall {number_of_walls + i}")
                i += 1
        elif ram_state[28] == 9:
            wall_instance = LavaWall()
            wall_instance.xy = (96, 61)
            wall_instance.wh = (64, 37)
            objects_map['lava wall 0'] = wall_instance
            wall_instance = LavaWall()
            wall_instance.xy = (72, 61)
            wall_instance.wh = (16, 37)
            objects_map['lava wall 1'] = wall_instance
            wall_instance = LavaWall()
            wall_instance.xy = (8, 61)
            wall_instance.wh = (56, 37)
            objects_map['lava wall 2'] = wall_instance
            number_of_lava_walls = 3
            i = 0
            while(objects_map.get(f"fixed wall {number_of_lava_walls + i}")!= None):
                objects_map.pop(f"fixed wall {number_of_lava_walls + i}")
                i += 1
            wall_instance = Wall()
            wall_instance.xy = (144, 21)
            wall_instance.wh = (16, 38)
            objects_map['fixed wall 0'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (8, 21)
            wall_instance.wh = (8, 38)
            objects_map['fixed wall 1'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (128, 101)
            wall_instance.wh = (32, 38)
            objects_map['fixed wall 2'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (8, 101)
            wall_instance.wh = (24, 38)
            objects_map['fixed wall 3'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (96, 61)
            wall_instance.wh = (64, 37)
            objects_map['fixed wall 4'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (72, 61)
            wall_instance.wh = (16, 37)
            objects_map['fixed wall 5'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (8, 61)
            wall_instance.wh = (56, 37)
            objects_map['fixed wall 6'] = wall_instance
            number_of_walls = 7
            i = 0
            while(objects_map.get(f"fixed wall {number_of_walls + i}")!= None):
                objects_map.pop(f"fixed wall {number_of_walls + i}")
                i += 1
        elif ram_state[28] == 10:
            number_of_lava_walls = 0
            i = 0
            while(objects_map.get(f"fixed wall {number_of_lava_walls + i}")!= None):
                objects_map.pop(f"fixed wall {number_of_lava_walls + i}")
                i += 1
            wall_instance = Wall()
            wall_instance.xy = (128, 21)
            wall_instance.wh = (32, 38)
            objects_map['fixed wall 0'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (8, 21)
            wall_instance.wh = (24, 38)
            objects_map['fixed wall 1'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (140, 101)
            wall_instance.wh = (20, 38)
            objects_map['fixed wall 2'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (8, 101)
            wall_instance.wh = (12, 38)
            objects_map['fixed wall 3'] = wall_instance
            number_of_walls = 4
            i = 0
            while(objects_map.get(f"fixed wall {number_of_walls + i}")!= None):
                objects_map.pop(f"fixed wall {number_of_walls + i}")
                i += 1
        elif ram_state[28] == 11:
            number_of_lava_walls = 0
            i = 0
            while(objects_map.get(f"fixed wall {number_of_lava_walls + i}")!= None):
                objects_map.pop(f"fixed wall {number_of_lava_walls + i}")
                i += 1
            wall_instance = Wall()
            wall_instance.xy = (8, 21)
            wall_instance.wh = (152, 38)
            objects_map['fixed wall 0'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (132, 101)
            wall_instance.wh = (28, 38)
            objects_map['fixed wall 1'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (8, 101)
            wall_instance.wh = (20, 38)
            objects_map['fixed wall 2'] = wall_instance
            number_of_walls = 3
            i = 0
            while(objects_map.get(f"fixed wall {number_of_walls + i}")!= None):
                objects_map.pop(f"fixed wall {number_of_walls + i}")
                i += 1
        elif ram_state[28] == 12:
            wall_instance = LavaWall()
            wall_instance.xy = (48, 61)
            wall_instance.wh = (64, 37)
            objects_map['lava wall 0'] = wall_instance
            number_of_lava_walls = 1
            i = 0
            while(objects_map.get(f"fixed wall {number_of_lava_walls + i}")!= None):
                objects_map.pop(f"fixed wall {number_of_lava_walls + i}")
                i += 1
            wall_instance = Wall()
            wall_instance.xy = (8, 21)
            wall_instance.wh = (152, 38)
            objects_map['fixed wall 0'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (136, 101)
            wall_instance.wh = (24, 38)
            objects_map['fixed wall 1'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (8, 101)
            wall_instance.wh = (16, 38)
            objects_map['fixed wall 2'] = wall_instance
            number_of_walls = 3
            i = 0
            while(objects_map.get(f"fixed wall {number_of_walls + i}")!= None):
                objects_map.pop(f"fixed wall {number_of_walls + i}")
                i += 1
        elif ram_state[28] == 13:
            number_of_lava_walls = 0
            i = 0
            while(objects_map.get(f"fixed wall {number_of_lava_walls + i}")!= None):
                objects_map.pop(f"fixed wall {number_of_lava_walls + i}")
                i += 1
            wall_instance = Wall()
            wall_instance.xy = (8, 21)
            wall_instance.wh = (152, 38)
            objects_map['fixed wall 0'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (128, 101)
            wall_instance.wh = (32, 38)
            objects_map['fixed wall 1'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (72, 101)
            wall_instance.wh = (16, 38)
            objects_map['fixed wall 2'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (8, 101)
            wall_instance.wh = (24, 38)
            objects_map['fixed wall 3'] = wall_instance
            number_of_walls = 4
            i = 0
            while(objects_map.get(f"fixed wall {number_of_walls + i}")!= None):
                objects_map.pop(f"fixed wall {number_of_walls + i}")
                i += 1
        elif ram_state[28] == 14:
            wall_instance = LavaWall()
            wall_instance.xy = (72, 61)
            wall_instance.wh = (16, 37)
            objects_map['lava wall 0'] = wall_instance
            number_of_lava_walls = 1
            i = 0
            while(objects_map.get(f"fixed wall {number_of_lava_walls + i}")!= None):
                objects_map.pop(f"fixed wall {number_of_lava_walls + i}")
                i += 1
            wall_instance = Wall()
            wall_instance.xy = (8, 21)
            wall_instance.wh = (152, 38)
            objects_map['fixed wall 0'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (132, 101)
            wall_instance.wh = (28, 38)
            objects_map['fixed wall 1'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (8, 101)
            wall_instance.wh = (20, 38)
            objects_map['fixed wall 2'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (72, 61)
            wall_instance.wh = (16, 37)
            objects_map['fixed wall 3'] = wall_instance
            number_of_walls = 4
            i = 0
            while(objects_map.get(f"fixed wall {number_of_walls + i}")!= None):
                objects_map.pop(f"fixed wall {number_of_walls + i}")
                i += 1
        elif ram_state[28] == 15:
            wall_instance = LavaWall()
            wall_instance.xy = (72, 61)
            wall_instance.wh = (16, 37)
            objects_map['lava wall 0'] = wall_instance
            number_of_lava_walls = 1
            i = 0
            while(objects_map.get(f"fixed wall {number_of_lava_walls + i}")!= None):
                objects_map.pop(f"fixed wall {number_of_lava_walls + i}")
                i += 1
            wall_instance = Wall()
            wall_instance.xy = (8, 21)
            wall_instance.wh = (152, 38)
            objects_map['fixed wall 0'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (112, 101)
            wall_instance.wh = (48, 38)
            objects_map['fixed wall 1'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (8, 101)
            wall_instance.wh = (40, 38)
            objects_map['fixed wall 2'] = wall_instance
            number_of_walls = 3
            i = 0
            while(objects_map.get(f"fixed wall {number_of_walls + i}")!= None):
                objects_map.pop(f"fixed wall {number_of_walls + i}")
                i += 1

    elif ram_state[117] == 19:
        if ram_state[28] == 0:
            wall_instance = LavaWall()
            wall_instance.xy = (144, 61)
            wall_instance.wh = (16, 37)
            objects_map['lava wall 0'] = wall_instance
            wall_instance = LavaWall()
            wall_instance.xy = (8, 61)
            wall_instance.wh = (8, 37)
            objects_map['lava wall 1'] = wall_instance
            number_of_lava_walls = 2
            i = 0
            while(objects_map.get(f"fixed wall {number_of_lava_walls + i}")!= None):
                objects_map.pop(f"fixed wall {number_of_lava_walls + i}")
                i += 1
            wall_instance = Wall()
            wall_instance.xy = (136, 21)
            wall_instance.wh = (24, 38)
            objects_map['fixed wall 0'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (8, 21)
            wall_instance.wh = (16, 38)
            objects_map['fixed wall 1'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (84, 101)
            wall_instance.wh = (76, 38)
            objects_map['fixed wall 2'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (8, 101)
            wall_instance.wh = (68, 38)
            objects_map['fixed wall 3'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (144, 61)
            wall_instance.wh = (16, 37)
            objects_map['fixed wall 4'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (8, 61)
            wall_instance.wh = (8, 37)
            objects_map['fixed wall 5'] = wall_instance
            number_of_walls = 6
            i = 0
            while(objects_map.get(f"fixed wall {number_of_walls + i}")!= None):
                objects_map.pop(f"fixed wall {number_of_walls + i}")
                i += 1
        elif ram_state[28] == 1:
            wall_instance = LavaWall()
            wall_instance.xy = (144, 61)
            wall_instance.wh = (16, 37)
            objects_map['lava wall 0'] = wall_instance
            wall_instance = LavaWall()
            wall_instance.xy = (8, 61)
            wall_instance.wh = (8, 37)
            objects_map['lava wall 1'] = wall_instance
            number_of_lava_walls = 2
            i = 0
            while(objects_map.get(f"fixed wall {number_of_lava_walls + i}")!= None):
                objects_map.pop(f"fixed wall {number_of_lava_walls + i}")
                i += 1
            wall_instance = Wall()
            wall_instance.xy = (84, 21)
            wall_instance.wh = (76, 38)
            objects_map['fixed wall 0'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (8, 21)
            wall_instance.wh = (68, 38)
            objects_map['fixed wall 1'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (136, 101)
            wall_instance.wh = (24, 38)
            objects_map['fixed wall 2'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (48, 101)
            wall_instance.wh = (64, 38)
            objects_map['fixed wall 3'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (8, 101)
            wall_instance.wh = (16, 38)
            objects_map['fixed wall 4'] = wall_instance
            number_of_walls = 5
            i = 0
            while(objects_map.get(f"fixed wall {number_of_walls + i}")!= None):
                objects_map.pop(f"fixed wall {number_of_walls + i}")
                i += 1
        elif ram_state[28] == 2:
            number_of_lava_walls = 0
            i = 0
            while(objects_map.get(f"fixed wall {number_of_lava_walls + i}")!= None):
                objects_map.pop(f"fixed wall {number_of_lava_walls + i}")
                i += 1
            wall_instance = Wall()
            wall_instance.xy = (136, 21)
            wall_instance.wh = (24, 38)
            objects_map['fixed wall 0'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (48, 21)
            wall_instance.wh = (64, 38)
            objects_map['fixed wall 1'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (8, 21)
            wall_instance.wh = (16, 38)
            objects_map['fixed wall 2'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (144, 101)
            wall_instance.wh = (16, 38)
            objects_map['fixed wall 3'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (8, 101)
            wall_instance.wh = (8, 38)
            objects_map['fixed wall 4'] = wall_instance
            number_of_walls = 5
            i = 0
            while(objects_map.get(f"fixed wall {number_of_walls + i}")!= None):
                objects_map.pop(f"fixed wall {number_of_walls + i}")
                i += 1
        elif ram_state[28] == 3:
            wall_instance = LavaWall()
            wall_instance.xy = (128, 61)
            wall_instance.wh = (32, 37)
            objects_map['lava wall 0'] = wall_instance
            wall_instance = LavaWall()
            wall_instance.xy = (40, 61)
            wall_instance.wh = (80, 37)
            objects_map['lava wall 1'] = wall_instance
            wall_instance = LavaWall()
            wall_instance.xy = (8, 61)
            wall_instance.wh = (24, 37)
            objects_map['lava wall 2'] = wall_instance
            number_of_lava_walls = 3
            i = 0
            while(objects_map.get(f"fixed wall {number_of_lava_walls + i}")!= None):
                objects_map.pop(f"fixed wall {number_of_lava_walls + i}")
                i += 1
            wall_instance = Wall()
            wall_instance.xy = (144, 21)
            wall_instance.wh = (16, 38)
            objects_map['fixed wall 0'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (8, 21)
            wall_instance.wh = (8, 38)
            objects_map['fixed wall 1'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (144, 101)
            wall_instance.wh = (16, 38)
            objects_map['fixed wall 2'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (8, 101)
            wall_instance.wh = (8, 38)
            objects_map['fixed wall 3'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (128, 61)
            wall_instance.wh = (32, 37)
            objects_map['fixed wall 4'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (40, 61)
            wall_instance.wh = (80, 37)
            objects_map['fixed wall 5'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (8, 61)
            wall_instance.wh = (24, 37)
            objects_map['fixed wall 6'] = wall_instance
            number_of_walls = 7
            i = 0
            while(objects_map.get(f"fixed wall {number_of_walls + i}")!= None):
                objects_map.pop(f"fixed wall {number_of_walls + i}")
                i += 1
        elif ram_state[28] == 4:
            wall_instance = LavaWall()
            wall_instance.xy = (104, 61)
            wall_instance.wh = (56, 37)
            objects_map['lava wall 0'] = wall_instance
            wall_instance = LavaWall()
            wall_instance.xy = (8, 61)
            wall_instance.wh = (48, 37)
            objects_map['lava wall 1'] = wall_instance
            number_of_lava_walls = 2
            i = 0
            while(objects_map.get(f"fixed wall {number_of_lava_walls + i}")!= None):
                objects_map.pop(f"fixed wall {number_of_lava_walls + i}")
                i += 1
            wall_instance = Wall()
            wall_instance.xy = (144, 21)
            wall_instance.wh = (16, 38)
            objects_map['fixed wall 0'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (8, 21)
            wall_instance.wh = (8, 38)
            objects_map['fixed wall 1'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (144, 101)
            wall_instance.wh = (16, 38)
            objects_map['fixed wall 2'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (8, 101)
            wall_instance.wh = (8, 38)
            objects_map['fixed wall 3'] = wall_instance
            number_of_walls = 4
            i = 0
            while(objects_map.get(f"fixed wall {number_of_walls + i}")!= None):
                objects_map.pop(f"fixed wall {number_of_walls + i}")
                i += 1
        elif ram_state[28] == 5:
            wall_instance = LavaWall()
            wall_instance.xy = (92, 61)
            wall_instance.wh = (68, 37)
            objects_map['lava wall 0'] = wall_instance
            wall_instance = LavaWall()
            wall_instance.xy = (8, 61)
            wall_instance.wh = (60, 37)
            objects_map['lava wall 1'] = wall_instance
            number_of_lava_walls = 2
            i = 0
            while(objects_map.get(f"fixed wall {number_of_lava_walls + i}")!= None):
                objects_map.pop(f"fixed wall {number_of_lava_walls + i}")
                i += 1
            wall_instance = Wall()
            wall_instance.xy = (144, 21)
            wall_instance.wh = (16, 38)
            objects_map['fixed wall 0'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (8, 21)
            wall_instance.wh = (8, 38)
            objects_map['fixed wall 1'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (136, 101)
            wall_instance.wh = (24, 38)
            objects_map['fixed wall 2'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (8, 101)
            wall_instance.wh = (16, 38)
            objects_map['fixed wall 3'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (92, 61)
            wall_instance.wh = (68, 37)
            objects_map['fixed wall 4'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (8, 61)
            wall_instance.wh = (60, 37)
            objects_map['fixed wall 5'] = wall_instance
            number_of_walls = 6
            i = 0
            while(objects_map.get(f"fixed wall {number_of_walls + i}")!= None):
                objects_map.pop(f"fixed wall {number_of_walls + i}")
                i += 1
        elif ram_state[28] == 6:
            wall_instance = LavaWall()
            wall_instance.xy = (144, 61)
            wall_instance.wh = (16, 37)
            objects_map['lava wall 0'] = wall_instance
            wall_instance = LavaWall()
            wall_instance.xy = (48, 61)
            wall_instance.wh = (64, 37)
            objects_map['lava wall 1'] = wall_instance
            wall_instance = LavaWall()
            wall_instance.xy = (8, 61)
            wall_instance.wh = (8, 37)
            objects_map['lava wall 2'] = wall_instance
            number_of_lava_walls = 3
            i = 0
            while(objects_map.get(f"fixed wall {number_of_lava_walls + i}")!= None):
                objects_map.pop(f"fixed wall {number_of_lava_walls + i}")
                i += 1
            wall_instance = Wall()
            wall_instance.xy = (136, 21)
            wall_instance.wh = (24, 38)
            objects_map['fixed wall 0'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (8, 21)
            wall_instance.wh = (16, 38)
            objects_map['fixed wall 1'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (120, 101)
            wall_instance.wh = (40, 38)
            objects_map['fixed wall 2'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (8, 101)
            wall_instance.wh = (32, 38)
            objects_map['fixed wall 3'] = wall_instance
            number_of_walls = 4
            i = 0
            while(objects_map.get(f"fixed wall {number_of_walls + i}")!= None):
                objects_map.pop(f"fixed wall {number_of_walls + i}")
                i += 1
        elif ram_state[28] == 7:
            wall_instance = LavaWall()
            wall_instance.xy = (112, 61)
            wall_instance.wh = (48, 37)
            objects_map['lava wall 0'] = wall_instance
            wall_instance = LavaWall()
            wall_instance.xy = (56, 61)
            wall_instance.wh = (48, 37)
            objects_map['lava wall 1'] = wall_instance
            wall_instance = LavaWall()
            wall_instance.xy = (8, 61)
            wall_instance.wh = (40, 37)
            objects_map['lava wall 2'] = wall_instance
            number_of_lava_walls = 3
            i = 0
            while(objects_map.get(f"fixed wall {number_of_lava_walls + i}")!= None):
                objects_map.pop(f"fixed wall {number_of_lava_walls + i}")
                i += 1
            wall_instance = Wall()
            wall_instance.xy = (120, 21)
            wall_instance.wh = (40, 38)
            objects_map['fixed wall 0'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (8, 21)
            wall_instance.wh = (32, 38)
            objects_map['fixed wall 1'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (136, 101)
            wall_instance.wh = (24, 38)
            objects_map['fixed wall 2'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (64, 101)
            wall_instance.wh = (32, 38)
            objects_map['fixed wall 3'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (8, 101)
            wall_instance.wh = (16, 38)
            objects_map['fixed wall 4'] = wall_instance
            number_of_walls = 5
            i = 0
            while(objects_map.get(f"fixed wall {number_of_walls + i}")!= None):
                objects_map.pop(f"fixed wall {number_of_walls + i}")
                i += 1
        elif ram_state[28] == 8:
            wall_instance = LavaWall()
            wall_instance.xy = (144, 61)
            wall_instance.wh = (16, 37)
            objects_map['lava wall 0'] = wall_instance
            wall_instance = LavaWall()
            wall_instance.xy = (56, 61)
            wall_instance.wh = (48, 37)
            objects_map['lava wall 1'] = wall_instance
            wall_instance = LavaWall()
            wall_instance.xy = (8, 61)
            wall_instance.wh = (8, 37)
            objects_map['lava wall 2'] = wall_instance
            number_of_lava_walls = 3
            i = 0
            while(objects_map.get(f"fixed wall {number_of_lava_walls + i}")!= None):
                objects_map.pop(f"fixed wall {number_of_lava_walls + i}")
                i += 1
            wall_instance = Wall()
            wall_instance.xy = (136, 21)
            wall_instance.wh = (24, 38)
            objects_map['fixed wall 0'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (64, 21)
            wall_instance.wh = (32, 38)
            objects_map['fixed wall 1'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (8, 21)
            wall_instance.wh = (16, 38)
            objects_map['fixed wall 2'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (128, 101)
            wall_instance.wh = (32, 38)
            objects_map['fixed wall 3'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (64, 101)
            wall_instance.wh = (32, 38)
            objects_map['fixed wall 4'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (8, 101)
            wall_instance.wh = (24, 38)
            objects_map['fixed wall 5'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (144, 61)
            wall_instance.wh = (16, 37)
            objects_map['fixed wall 6'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (56, 61)
            wall_instance.wh = (48, 37)
            objects_map['fixed wall 7'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (8, 61)
            wall_instance.wh = (8, 37)
            objects_map['fixed wall 8'] = wall_instance
            number_of_walls = 9
            i = 0
            while(objects_map.get(f"fixed wall {number_of_walls + i}")!= None):
                objects_map.pop(f"fixed wall {number_of_walls + i}")
                i += 1
        elif ram_state[28] == 9:
            wall_instance = LavaWall()
            wall_instance.xy = (112, 61)
            wall_instance.wh = (48, 37)
            objects_map['lava wall 0'] = wall_instance
            wall_instance = LavaWall()
            wall_instance.xy = (56, 61)
            wall_instance.wh = (48, 37)
            objects_map['lava wall 1'] = wall_instance
            wall_instance = LavaWall()
            wall_instance.xy = (8, 61)
            wall_instance.wh = (40, 37)
            objects_map['lava wall 2'] = wall_instance
            number_of_lava_walls = 3
            i = 0
            while(objects_map.get(f"fixed wall {number_of_lava_walls + i}")!= None):
                objects_map.pop(f"fixed wall {number_of_lava_walls + i}")
                i += 1
            wall_instance = Wall()
            wall_instance.xy = (128, 21)
            wall_instance.wh = (32, 38)
            objects_map['fixed wall 0'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (64, 21)
            wall_instance.wh = (32, 38)
            objects_map['fixed wall 1'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (8, 21)
            wall_instance.wh = (24, 38)
            objects_map['fixed wall 2'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (140, 101)
            wall_instance.wh = (20, 38)
            objects_map['fixed wall 3'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (64, 101)
            wall_instance.wh = (32, 38)
            objects_map['fixed wall 4'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (8, 101)
            wall_instance.wh = (12, 38)
            objects_map['fixed wall 5'] = wall_instance
            number_of_walls = 6
            i = 0
            while(objects_map.get(f"fixed wall {number_of_walls + i}")!= None):
                objects_map.pop(f"fixed wall {number_of_walls + i}")
                i += 1
        elif ram_state[28] == 10:
            number_of_lava_walls = 0
            i = 0
            while(objects_map.get(f"fixed wall {number_of_lava_walls + i}")!= None):
                objects_map.pop(f"fixed wall {number_of_lava_walls + i}")
                i += 1
            wall_instance = Wall()
            wall_instance.xy = (140, 21)
            wall_instance.wh = (20, 38)
            objects_map['fixed wall 0'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (64, 21)
            wall_instance.wh = (32, 38)
            objects_map['fixed wall 1'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (8, 21)
            wall_instance.wh = (12, 38)
            objects_map['fixed wall 2'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (140, 101)
            wall_instance.wh = (20, 38)
            objects_map['fixed wall 3'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (8, 101)
            wall_instance.wh = (12, 38)
            objects_map['fixed wall 4'] = wall_instance
            number_of_walls = 5
            i = 0
            while(objects_map.get(f"fixed wall {number_of_walls + i}")!= None):
                objects_map.pop(f"fixed wall {number_of_walls + i}")
                i += 1
        elif ram_state[28] == 11:
            wall_instance = LavaWall()
            wall_instance.xy = (40, 61)
            wall_instance.wh = (80, 37)
            objects_map['lava wall 0'] = wall_instance
            number_of_lava_walls = 1
            i = 0
            while(objects_map.get(f"fixed wall {number_of_lava_walls + i}")!= None):
                objects_map.pop(f"fixed wall {number_of_lava_walls + i}")
                i += 1
            wall_instance = Wall()
            wall_instance.xy = (8, 21)
            wall_instance.wh = (152, 38)
            objects_map['fixed wall 0'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (136, 101)
            wall_instance.wh = (24, 38)
            objects_map['fixed wall 1'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (8, 101)
            wall_instance.wh = (16, 38)
            objects_map['fixed wall 2'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (40, 61)
            wall_instance.wh = (80, 37)
            objects_map['fixed wall 3'] = wall_instance
            number_of_walls = 4
            i = 0
            while(objects_map.get(f"fixed wall {number_of_walls + i}")!= None):
                objects_map.pop(f"fixed wall {number_of_walls + i}")
                i += 1
        elif ram_state[28] == 12:
            wall_instance = LavaWall()
            wall_instance.xy = (72, 61)
            wall_instance.wh = (16, 37)
            objects_map['lava wall 0'] = wall_instance
            number_of_lava_walls = 1
            i = 0
            while(objects_map.get(f"fixed wall {number_of_lava_walls + i}")!= None):
                objects_map.pop(f"fixed wall {number_of_lava_walls + i}")
                i += 1
            wall_instance = Wall()
            wall_instance.xy = (8, 21)
            wall_instance.wh = (152, 38)
            objects_map['fixed wall 0'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (132, 101)
            wall_instance.wh = (28, 38)
            objects_map['fixed wall 1'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (8, 101)
            wall_instance.wh = (20, 38)
            objects_map['fixed wall 2'] = wall_instance
            number_of_walls = 3
            i = 0
            while(objects_map.get(f"fixed wall {number_of_walls + i}")!= None):
                objects_map.pop(f"fixed wall {number_of_walls + i}")
                i += 1
        elif ram_state[28] == 13:
            wall_instance = LavaWall()
            wall_instance.xy = (64, 61)
            wall_instance.wh = (32, 37)
            objects_map['lava wall 0'] = wall_instance
            number_of_lava_walls = 1
            i = 0
            while(objects_map.get(f"fixed wall {number_of_lava_walls + i}")!= None):
                objects_map.pop(f"fixed wall {number_of_lava_walls + i}")
                i += 1
            wall_instance = Wall()
            wall_instance.xy = (8, 21)
            wall_instance.wh = (152, 38)
            objects_map['fixed wall 0'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (128, 101)
            wall_instance.wh = (32, 38)
            objects_map['fixed wall 1'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (8, 101)
            wall_instance.wh = (24, 38)
            objects_map['fixed wall 2'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (64, 61)
            wall_instance.wh = (32, 37)
            objects_map['fixed wall 3'] = wall_instance
            number_of_walls = 4
            i = 0
            while(objects_map.get(f"fixed wall {number_of_walls + i}")!= None):
                objects_map.pop(f"fixed wall {number_of_walls + i}")
                i += 1
        elif ram_state[28] == 14:
            wall_instance = LavaWall()
            wall_instance.xy = (72, 61)
            wall_instance.wh = (16, 37)
            objects_map['lava wall 0'] = wall_instance
            number_of_lava_walls = 1
            i = 0
            while(objects_map.get(f"fixed wall {number_of_lava_walls + i}")!= None):
                objects_map.pop(f"fixed wall {number_of_lava_walls + i}")
                i += 1
            wall_instance = Wall()
            wall_instance.xy = (8, 21)
            wall_instance.wh = (152, 38)
            objects_map['fixed wall 0'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (132, 101)
            wall_instance.wh = (28, 38)
            objects_map['fixed wall 1'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (8, 101)
            wall_instance.wh = (20, 38)
            objects_map['fixed wall 2'] = wall_instance
            number_of_walls = 3
            i = 0
            while(objects_map.get(f"fixed wall {number_of_walls + i}")!= None):
                objects_map.pop(f"fixed wall {number_of_walls + i}")
                i += 1
        elif ram_state[28] == 15:
            wall_instance = LavaWall()
            wall_instance.xy = (72, 61)
            wall_instance.wh = (16, 37)
            objects_map['lava wall 0'] = wall_instance
            number_of_lava_walls = 1
            i = 0
            while(objects_map.get(f"fixed wall {number_of_lava_walls + i}")!= None):
                objects_map.pop(f"fixed wall {number_of_lava_walls + i}")
                i += 1
            wall_instance = Wall()
            wall_instance.xy = (8, 21)
            wall_instance.wh = (152, 38)
            objects_map['fixed wall 0'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (112, 101)
            wall_instance.wh = (48, 38)
            objects_map['fixed wall 1'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (8, 101)
            wall_instance.wh = (40, 38)
            objects_map['fixed wall 2'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (72, 61)
            wall_instance.wh = (16, 37)
            objects_map['fixed wall 3'] = wall_instance
            number_of_walls = 4
            i = 0
            while(objects_map.get(f"fixed wall {number_of_walls + i}")!= None):
                objects_map.pop(f"fixed wall {number_of_walls + i}")
                i += 1

    return objects_map
