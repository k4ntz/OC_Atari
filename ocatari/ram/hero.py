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


class LavaWall(GameObject):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.xy = 0, 0
        self.wh = 8, 10


class EnemyType(Enum):
    Spider = 1
    Bat = 2
    Thing = 3


class Enemy(GameObject):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.xy = 0, 0
        self.wh = 8, 10
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
        self.wh = 8, 10
        self.wh = 5, 20


class LaserBeam(GameObject):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.xy = 0, 0
        self.wh = 8, 10


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
    return objects


def _detect_objects_hero_revised(objects, ram_state, hud=False):
    objects[0].xy = ram_state[27],ram_state[31]
    if hud:
        objects.append(PowerBar())
        objects[-1].value = ram_state[43]
        objects.append(BombStock())
        objects[-1].value = ram_state[50]
        objects.append(Score())
        objects[-1].value = ram_state[56]

    return


def _detect_objects_hero_raw(info, ram_state):
    return
