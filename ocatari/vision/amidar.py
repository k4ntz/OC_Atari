from .game_objects import GameObject, NoObject
from .utils import find_objects, match_objects, match_blinking_objects

objects_colors = {"yellow": [252, 252, 84], "green": [135, 183, 84], "red": [214, 92, 92]}


class Player(GameObject):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.rgb = [252, 252, 84]


# class GameObject(GameObject):
#     def __init__(self, *args, **kwargs):
#         super().__init__(*args, **kwargs)
#         self.rgb = [135, 183, 84]


class Warrior(GameObject):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.rgb = [135, 183, 84]
        self.num_frames_invisible = -1
        self.max_frames_invisible = 10


class Pig(GameObject):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.rgb = [214, 92, 92]
        self.num_frames_invisible = -1
        self.max_frames_invisible = 4


class Chicken(GameObject):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.rgb = [252, 252, 84]
        self.num_frames_invisible = -1
        self.max_frames_invisible = 4

#  ---- HUD -----
class Score(GameObject):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.rgb = [252, 252, 84]


class Life(GameObject):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.rgb = [252, 252, 84]


def _detect_objects(objects, obs, hud=False):
    enemy_bb = []
    chicken_bb = []
    enemy_type = Warrior
    player = objects[0]
    yellow = find_objects(obs, objects_colors["yellow"], maxy=170)
    for bb in yellow:
        if bb[2] > 6:
            player.xy = bb[:2]
        else:
            chicken_bb.append(bb)
    green = find_objects(obs, objects_colors["green"])
    for bb in green:
        enemy_bb.append(bb) # or *bb?
        enemy_type = Warrior

    red = find_objects(obs, objects_colors["red"])
    for bb in red:
        enemy_bb.append(bb) # or *bb?
        enemy_type = Pig

    if all([enemy_type != type(objects[1+i]) for i in range(6)]): #Deletes the previous enemys if the type of enemies has changed
        objects[1:7] = [NoObject()] * 6

    match_blinking_objects(objects, enemy_bb, 1, 6, enemy_type)

    match_blinking_objects(objects, chicken_bb, 7, 6, Chicken)

    if hud:
        score = objects[13]
        lives_bbs = find_objects(obs, objects_colors["yellow"], miny=175, closing_dist=4, min_distance=1)
        for bb in lives_bbs:
            if bb[2] > 4:
                score.xywh = bb
                lives_bbs.remove(bb)
                break
        match_objects(objects, lives_bbs, 14, 3, Life)
