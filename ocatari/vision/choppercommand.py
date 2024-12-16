from .game_objects import GameObject
from .utils import *
from dataclasses import dataclass


# Vision

object_colors = {"most": [223, 183, 85], "truck": [0, 0, 0], "enemy_helicopter": [236, 236, 236],
                 "enemy_plane": [0, 0, 148], "shot": [20, 0, 144], "mini_player": [124, 44, 0],
                 "mini_others": [236, 200, 96]}

# most = Player, bomb, Score, Life1, Life2
# mini_others = MiniEnemy, MiniTruck


class Player(GameObject):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.rgb = 223, 183, 85


class MiniPlayer(GameObject):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.rgb = 124, 44, 0


class Truck(GameObject):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.rgb = 0, 0, 0


class MiniTruck(GameObject):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.rgb = 236, 200, 96


class EnemyHelicopter(GameObject):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.rgb = 236, 236, 236


class EnemyPlane(GameObject):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.rgb = 0, 0, 148


class MiniEnemy(GameObject):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.rgb = 236, 200, 96


class Bomb(GameObject):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.rgb = 223, 183, 85


class Shot(GameObject):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.rgb = 0, 0, 100  # blau ist höher, aber sonst random


class Score(GameObject):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.rgb = 223, 183, 85


class Life(GameObject):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.rgb = 223, 183, 85

# Mini-Spielbereich: (minx,miny,maxX,maxY): (55,178,103,186)
# Spielbereich: (18,64,150,163)


def _init_objects_ram(hud):
    # gibt Liste von GameObjects zurück
    """
    (Re)Initialize the objects
    """
    objects = [Player(), MiniPlayer()]
    for i in range(2):
        objects.append(Truck())
    for i in range(9):
        objects.append(MiniTruck())
    for i in range(11):
        objects.append(MiniEnemy())

    if hud:
        objects.extend([Score(), Life(), Life()])
    return objects


@dataclass
class MiniPlayArea:
    (minx, miny, maxx, maxy) = (56, 178, 103, 187)


@dataclass
class PlayArea:
    (minx, miny, maxx, maxy) = (18, 64, 150, 163)


def _detect_objects(objects, obs, hud=False):
    objects.clear()

    # most = Player, bomb, Score, Life1, Life2
    player = find_objects(obs, object_colors["most"], size=(16, 9), minx=PlayArea.minx, maxx=PlayArea.maxx,
                          miny=PlayArea.miny, maxy=PlayArea.maxy)
    bomb = find_objects(obs, object_colors["most"], size=(2, 2), minx=PlayArea.minx, maxx=PlayArea.maxx,
                        miny=PlayArea.miny, maxy=PlayArea.maxy)

    for bb in player:
        objects.append(Player(*bb))

    for bb in bomb:
        objects.append(Bomb(*bb))

    # truck
    truck = find_objects(obs, object_colors["truck"], size=(
        8, 7), minx=8, miny=161, maxy=167)
    for bb in truck:
        objects.append(Truck(*bb))

    # enemy_helicopter
    enemy_helicopter = find_objects(
        obs, object_colors["enemy_helicopter"], size=(8, 9))
    for bb in enemy_helicopter:
        objects.append(EnemyHelicopter(*bb))

    # enemy_plane
    enemy_plane = find_objects(obs, object_colors["enemy_plane"], size=(8, 6))
    for bb in enemy_plane:
        objects.append(EnemyPlane(*bb))

    # shot
    # (180, 122, 48) is the background, (0,0,0) is the black edge
    shot = find_objects_in_color_range(obs, color_min=(0, 0, 20), color_max=(179, 128, 255),
                                       miny=PlayArea.miny, maxy=PlayArea.maxy)
    for bb in shot:
        # enemy_plane is in the color range
        if not (bb in enemy_plane):
            objects.append(Shot(*bb))

    # mini_player (case object in another object)
    mini_player = find_rectangle_objects(obs, object_colors["mini_player"], max_size=(2, 2),
                                         minx=MiniPlayArea.minx, maxx=MiniPlayArea.maxx, miny=MiniPlayArea.miny, maxy=184)
    for bb in mini_player:
        objects.append(MiniPlayer(*bb))

    # mini_others = MiniEnemy, MiniTruck
    mini_enemy = find_rectangle_objects(obs, object_colors["mini_others"], max_size=(2, 2),
                                        minx=MiniPlayArea.minx, maxx=MiniPlayArea.maxx, miny=MiniPlayArea.miny, maxy=184)
    mini_enemy.extend(find_rectangle_objects(obs, object_colors["mini_others"], max_size=(2, 1),
                                             minx=MiniPlayArea.minx, maxx=MiniPlayArea.maxx, miny=183, maxy=184))
    mini_truck = find_rectangle_objects(obs, object_colors["mini_others"], max_size=(1, 2),
                                        minx=MiniPlayArea.minx, maxx=MiniPlayArea.maxx, miny=185, maxy=MiniPlayArea.maxy)
    for bb in mini_enemy:
        objects.append(MiniEnemy(*bb))

    for bb in mini_truck:
        objects.append(MiniTruck(*bb))

    if hud:
        score = find_objects(obs, object_colors["most"], size=(6, 7), miny=16, maxy=23, min_distance=2,
                             closing_active=False)
        life = list()
        for i in range(15):
            life.extend(find_objects(obs, object_colors["most"], size=(8, 9), minx=33+8*i, maxx=33+8*(i+1),
                                     miny=24, maxy=33))

        for bb in score:
            objects.append(Score(*bb))
        for bb in life:
            objects.append(Life(*bb))
