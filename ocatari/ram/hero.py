from enum import Enum

from .game_objects import GameObject

MAX_NB_OBJECTS = {"Wall": 15, "LavaWall": 15, "Enemy": 10, "Player": 1, "LaserBeam": 3, "Bomb": 5, "EndNPC": 1,
                  "Lamp": 1, "Snake": 5, }
MAX_NB_OBJECTS_HUD = {"Wall": 15, "LavaWall": 15, "Enemy": 10, "Player": 1, "LaserBeam": 3, "Bomb": 5, "EndNPC": 1,
                      "Lamp": 1, "Snake": 5, "PowerBar": 1, "BombStock": 1, "Life": 1, "Score": 1}


class Wall(GameObject):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.xy = 0, 0
        self.wh = 8, 10
        self.destructible: bool = False


class LavaWall(GameObject):
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
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.xy = 0, 0
        self.wh = 6, 10
        self.type: EnemyType


class Snake(GameObject):
    def __init__(self, *args, **kwargs):
        self.xy = 0, 0
        self.wh = 8, 10
        super().__init__(*args, **kwargs)


class Player(GameObject):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.xy = 0, 0
        self.wh = 5, 25


class LaserBeam(GameObject):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.xy = 0, 0
        self.wh = 7, 2


class Bomb(GameObject):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.xy = 0, 0
        self.wh = 8, 10


class EndNPC(GameObject):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.xy = 0, 0
        self.wh = 8, 10


class Lamp(GameObject):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.xy = 0, 0
        self.wh = 8, 10


class PowerBar(GameObject):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.xy = 0, 0
        self.wh = 8, 10
        self.value = 1


class BombStock(GameObject):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.xy = 0, 0
        self.wh = 8, 10
        self.value = 5


class Life(GameObject):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.xy = 0, 0
        self.wh = 8, 10


class Score(GameObject):
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
    # TODO switch case =function of ram_sate[28] + level = ram_state[117] + 1

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
            objects_map[f"destructible wall"] = destructible_wall_instance

    # Bomb / NPC position
    # If we're on the final part of the level --> NPC position else bomb position

    if hud:
        objects[1].value = ram_state[42] / 81
        objects[2].value = ram_state[51]
        objects[3].value = ram_state[53]
        objects[4].value = ram_state[56]
    print(ram_state)
    objects[:] = objects[0:base_length] + list(objects_map.values())


def _detect_objects_hero_raw(info, ram_state):
    return
