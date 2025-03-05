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


@dataclass
class MiniPlayArea:
    (minx, miny, maxx, maxy) = (56, 178, 103, 187)


@dataclass
class PlayArea:
    (minx, miny, maxx, maxy) = (18, 64, 150, 163)


def _detect_objects(objects, obs, hud=False):

    # most = Player, bomb, Score, Life1, Life2
    player = find_objects(obs, object_colors["most"], size=(16, 9), minx=PlayArea.minx, maxx=PlayArea.maxx,
                          miny=PlayArea.miny, maxy=PlayArea.maxy)
    bomb = find_objects(obs, object_colors["most"], size=(2, 2), minx=PlayArea.minx, maxx=PlayArea.maxx,
                        miny=PlayArea.miny, maxy=PlayArea.maxy)

    if player:
        objects[0].xywh = player[0]

    match_objects(objects, bomb[0:2], 12, 2, Bomb)


    # truck
    truck = find_objects(obs, object_colors["truck"], size=(8, 7), minx=8, miny=161, maxy=167)
    match_objects(objects, truck, 2, 3, Truck)


    # enemy_helicopter
    enemy_helicopter = find_objects(obs, object_colors["enemy_helicopter"], size=(8, 9))
    match_objects(objects, enemy_helicopter, 8, 3, EnemyHelicopter)

    # enemy_plane
    enemy_plane = find_objects(obs, object_colors["enemy_plane"], size=(8, 6))
    match_objects(objects, enemy_plane, 5, 3, EnemyPlane)

    # shot
    # (180, 122, 48) is the background, (0,0,0) is the black edge
    shot = find_objects_in_color_range(obs, color_min=(0, 0, 20), color_max=(179, 128, 255),
                                       miny=PlayArea.miny, maxy=PlayArea.maxy)
    for bb in shot:
        # enemy_plane is in the color range
        if not (bb in enemy_plane):
            if type(objects[1]) is NoObject:
                objects[1] = Shot(*bb)
            objects[1].xywh = bb
            break
    else:
        objects[1] = NoObject()

    # mini_player (case object in another object)
    mini_player = find_rectangle_objects(obs, object_colors["mini_player"], max_size=(2, 2),
                                         minx=MiniPlayArea.minx, maxx=MiniPlayArea.maxx, miny=MiniPlayArea.miny, maxy=184)
    if mini_player:
        objects[13].xywh = mini_player[0]

    # mini_others = MiniEnemy, MiniTruck
    mini_enemy = find_rectangle_objects(obs, object_colors["mini_others"], max_size=(2, 2),
                                        minx=MiniPlayArea.minx, maxx=MiniPlayArea.maxx, miny=MiniPlayArea.miny, maxy=184)
    mini_enemy.extend(find_rectangle_objects(obs, object_colors["mini_others"], max_size=(2, 1),
                                             minx=MiniPlayArea.minx, maxx=MiniPlayArea.maxx, miny=183, maxy=184))
    mini_truck = find_rectangle_objects(obs, object_colors["mini_others"], max_size=(1, 2),
                                        minx=MiniPlayArea.minx, maxx=MiniPlayArea.maxx, miny=185, maxy=MiniPlayArea.maxy)
    
    
    match_objects(objects, mini_truck, 14, 9, MiniTruck)
    match_objects(objects, mini_enemy, 23, 12, MiniEnemy)

    if hud:
        score = find_objects(obs, object_colors["most"], size=(6, 7), miny=16, maxy=23)
        life = find_objects(obs, object_colors["most"], size=(8, 9), miny=24, maxy=33)

        if score:
            objects[35].xywh = score[0]
        if life:
            objects[36].xywh = life[0]
