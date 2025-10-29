from .game_objects import GameObject, NoObject
from .utils import find_objects, find_mc_objects, most_common_color, match_objects, match_blinking_objects
import numpy as np

objects_colors = {"Player": [132, 144, 252], "Enemy_Shot": [[132, 144, 252], [198, 108, 58]],
                  "Player_Shot": [[84, 92, 214], [132, 144, 252], [252, 224, 112], [232, 232, 74], [210, 210, 64], [198, 108, 58], [236, 140, 224]],
                  "Bomber": [84, 92, 214], "Baiter": [84, 92, 214], "Pod": [252, 224, 112], "Swarm": [232, 232, 74],
                  "Lander": [210, 210, 64], "Humanoide_Lander": [198, 108, 58], "Human": [132, 144, 252],
                  "Radar_Enemy": [[210, 210, 64], [252, 224, 112], [232, 232, 74], [198, 108, 58], [84, 92, 214]],
                  "Radar_Human": [232, 232, 74], "Score": [232, 232, 74], "Lives_and_Bombs": [132, 144, 252]}


class Player(GameObject):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.rgb = [132, 144, 252]
        self.num_frames_invisible = -1
        self.max_frames_invisible = 3
        self.expected_dist = 2


class Player_Shot(GameObject):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.rgb = [132, 144, 252]
        self.num_frames_invisible = -1
        self.max_frames_invisible = 4
        self.expected_dist = 5


class Enemy_Shot(GameObject):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.rgb = [132, 144, 252]
        self.num_frames_invisible = -1
        self.max_frames_invisible = 8
        self.expected_dist = 10


class Bomber(GameObject):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.rgb = [84, 92, 214]
        self.num_frames_invisible = -1
        self.max_frames_invisible = 8
        self.expected_dist = 20


class Baiter(GameObject):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.rgb = [84, 92, 214]
        self.num_frames_invisible = -1
        self.max_frames_invisible = 8
        self.expected_dist = 20


class Pod(GameObject):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.rgb = [252, 224, 112]
        self.num_frames_invisible = -1
        self.max_frames_invisible = 8
        self.expected_dist = 10


class Swarm(GameObject):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.rgb = [232, 232, 74]
        self.num_frames_invisible = -1
        self.max_frames_invisible = 8
        self.expected_dist = 10


class Lander(GameObject):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.rgb = [210, 210, 64]
        self.num_frames_invisible = -1
        self.max_frames_invisible = 8
        self.expected_dist = 10


class Humanoide_Lander(GameObject):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.rgb = [198, 108, 58]
        self.num_frames_invisible = -1
        self.max_frames_invisible = 8
        self.expected_dist = 10


class Human(GameObject):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.rgb = [132, 144, 252]
        self.num_frames_invisible = -1
        self.max_frames_invisible = 11
        self.expected_dist = 25


class Radar_Player(GameObject):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.rgb = [232, 232, 74]
        self.num_frames_invisible = -1
        self.max_frames_invisible = 16
        self.expected_dist = 2


class Radar_Enemy(GameObject):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.rgb = [210, 210, 64]
        self.num_frames_invisible = -1
        self.max_frames_invisible = 8
        self.expected_dist = 2


class Radar_Human(GameObject):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.rgb = [232, 232, 74]
        self.num_frames_invisible = -1
        self.max_frames_invisible = 8
        self.expected_dist = 2


class City_Scape(GameObject):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.rgb = [84, 92, 214]


#  ---- HUD -----
class Score(GameObject):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.rgb = [232, 232, 74]


class Lives(GameObject):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.rgb = [132, 144, 252]


class Smart_Bomb_Count(GameObject):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.rgb = [132, 144, 252]


def _detect_objects(objects, obs, hud=False):

    player = find_objects(obs, objects_colors["Player"], size=(7,5), tol_s=1, miny=37, maxy=173, closing_active=False)
    if player:
        objects[0].xywh = player[0]

    p_shot = find_mc_objects(obs, objects_colors["Player_Shot"], size=(32, 2), tol_s=4, miny=37, maxy=156, closing_active=False, all_colors=False)
    if p_shot:
        if type(objects[1]) is NoObject:
            objects[1] = Player_Shot(*p_shot[0])
        objects[1].xywh = p_shot[0]
    elif type(objects[1]) is not NoObject:
        if objects[1].num_frames_invisible > objects[1].max_frames_invisible:
            objects[1] = NoObject()
        else:
            objects[1].num_frames_invisible +=1


    e_shot = find_mc_objects(obs, objects_colors["Enemy_Shot"], size=(2, 2), tol_s=1, miny=37, maxy=156, closing_active=False, all_colors=False)
    if e_shot:
        if type(objects[2]) is NoObject:
            objects[2] = Enemy_Shot(*e_shot[0])
        objects[2].xywh = e_shot[0]
    elif type(objects[2]) is not NoObject:
        if objects[2].num_frames_invisible > objects[2].max_frames_invisible:
            objects[2] = NoObject()
        else:
            objects[2].num_frames_invisible +=1

    bomber = find_objects(obs, objects_colors["Bomber"], size=(6,4), tol_s=2, miny=37, maxy=156, closing_active=False)
    
    if bomber:
        for b in bomber:
            if bomber[0][2] < 6:
                if type(objects[3]) is NoObject:
                    objects[3] = Bomber(*b)
                objects[3].xywh = b
            else:
                if type(objects[4]) is NoObject:
                    objects[4] = Baiter(*b)
                objects[4].xywh = b
    else:
        if type(objects[3]) is not NoObject:
            if objects[3].num_frames_invisible > objects[3].max_frames_invisible:
                objects[3] = NoObject()
            else:
                objects[3].num_frames_invisible +=1

        if type(objects[4]) is not NoObject:
            if objects[4].num_frames_invisible > objects[4].max_frames_invisible:
                objects[4] = NoObject()
            else:
                objects[4].num_frames_invisible +=1
    
    pod = find_objects(obs, objects_colors["Pod"], size=(7,7), tol_s=1, miny=37, maxy=156, closing_active=False)
    match_blinking_objects(objects, pod, 5, 2, Pod)

    swarm = find_objects(obs, objects_colors["Swarm"], size=(8,7), tol_s=1, miny=37, maxy=156)
    match_blinking_objects(objects, swarm, 7, 2, Swarm)

    lander = find_objects(obs, objects_colors["Lander"], size=(8,7), tol_s=1, miny=37, maxy=156, closing_active=False)
    match_blinking_objects(objects, lander, 9, 5, Lander)

    hu_lander = find_objects(obs, objects_colors["Humanoide_Lander"], size=(8,7), tol_s=0, miny=37, maxy=156, closing_active=False)
    match_blinking_objects(objects, hu_lander, 14, 5, Humanoide_Lander)

    human = find_objects(obs, objects_colors["Human"], size=(2,4), tol_s=1, miny=37, maxy=173, closing_active=False)
    match_blinking_objects(objects, human, 19, 5, Human)

    radar_h = find_objects(obs, objects_colors["Radar_Human"], size=(4,2), tol_s=0, maxy=34, closing_active=False)
    match_blinking_objects(objects, radar_h, 24, 1, Radar_Player)

    radar_e = find_mc_objects(obs, objects_colors["Radar_Enemy"], size=(2, 2), tol_s=0, maxy=34, closing_active=False, all_colors=False)
    match_blinking_objects(objects, radar_e, 25, 8, Radar_Enemy)

    radar_h = find_objects(obs, objects_colors["Radar_Human"], size=(1,2), tol_s=0, maxy=35, closing_active=False)
    match_blinking_objects(objects, radar_h, 33, 5, Radar_Human)

    if hud:
        score = find_objects(
            obs, objects_colors["Score"],miny=175, closing_dist=4)
        if score:
            objects[-3].xywh = score[0]

        life = find_objects(obs, objects_colors["Lives_and_Bombs"], maxx=48, miny=175, closing_dist=12)
        if life:
            objects[-2].xywh = life[0]

        bombs = find_objects(obs, objects_colors["Lives_and_Bombs"], minx=110, miny=175, closing_dist=16)
        if life:
            objects[-1].xywh = bombs[0]
