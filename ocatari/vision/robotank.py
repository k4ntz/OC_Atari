from .utils import find_objects, find_mc_objects
from .game_objects import GameObject, NoObject

objects_colors = {"player": [236, 236, 236], "blue": [84, 92, 214], "black": [0, 0, 0], "yellow": [134, 134, 29],
                  "radar": [146, 70, 192], "lives": [184, 50, 50]}


class Player_Crosshair(GameObject):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.rgb = 236, 236, 236


class PlayerShot(GameObject):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.rgb = 1, 1, 1


class EnemyTank(GameObject):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.rgb = 1, 1, 1


class EnemyShot(GameObject):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.rgb = 1, 1, 1


class EnemyRadarPosition(GameObject):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.rgb = 146, 70, 192


class VisionSensor(GameObject):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.rgb = 110, 156, 66


class RadarSensor(GameObject):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.rgb = 110, 156, 66


class CanonSensor(GameObject):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.rgb = 110, 156, 66


class TreadSensor(GameObject):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.rgb = 110, 156, 66


class Score(GameObject):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.rgb = 1, 1, 1


class Lives(GameObject):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.rgb = 184, 50, 50


class Clock(GameObject):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.rgb = 236, 236, 236


def _detect_objects(objects, obs, hud=False):

    player = find_mc_objects(obs, [objects_colors["player"], objects_colors["blue"]], closing_dist=10, miny=78, maxy=125, all_colors=False)
    if player:
        p = player[0]
        objects[0].xywh = p

        y = p[1] + 18
        other = find_objects(obs, objects_colors["black"], closing_dist=10, minx=8, miny=78, maxy=125)
        other.extend(find_objects(obs, objects_colors["yellow"], closing_dist=10, minx=8, miny=78, maxy=125))
        p_shot, enemy, e_shot = None, None, None

        for o in other:
            if o[2] < o[3]:
                e_shot = o
            elif o[1] <= y:
                enemy = o
            else:
                p_shot = o

        if p_shot:
            if type(objects[1]) is NoObject:
                objects[1] = PlayerShot(*p_shot)
            objects[1].xywh = p_shot
        else:
            objects[1] = NoObject()

        if enemy:
            if type(objects[2]) is NoObject:
                objects[2] = EnemyTank(*enemy)
            objects[2].xywh = enemy
        else:
            objects[2] = NoObject()

        if e_shot:
            if type(objects[3]) is NoObject:
                objects[3] = EnemyShot(*e_shot)
            objects[3].xywh = e_shot
        else:
            objects[3] = NoObject()
    else:
        for i in range(1,4):
            objects[i] = NoObject()

    radar = find_objects(obs, objects_colors["radar"], (1, 1), tol_s=1, closing_dist=2)
    if radar:
        if type(objects[4]) is NoObject:
            objects[4] = EnemyRadarPosition(*radar[0])
        objects[4].xywh = radar[0]
    else:
        objects[4] = NoObject()

    if hud:
        score = find_objects(obs, objects_colors["black"], closing_dist=10, minx=8, miny=15, maxy=40)
        if score:
            if type(objects[9]) is NoObject:
                objects[9] = Score(*score[0])
            objects[9].xywh = score[0]
        else:
            objects[9] = NoObject()
            
        lives = find_objects(obs, objects_colors["lives"], closing_dist=10, miny=172, maxy=185)
        if lives:
            if type(objects[10]) is NoObject:
                objects[10] = Lives(*lives[0])
            objects[10].xywh = lives[0]
        else:
            objects[10] = NoObject()
