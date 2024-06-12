from .game_objects import GameObject
from .utils import find_objects, find_mc_objects, most_common_color
import numpy as np

objects_colors = {'pink': [168, 48, 143], 'dark_pink': [151, 25, 122], 'grey': [170, 170, 170], 'dark_grey': [111, 111, 111],
                  'purple': [78, 50, 181], 'dark_purple': [151, 25, 122], 'yellow': [134, 134, 29], 'dark_yellow': [82, 126, 45],
                  'green': [50, 132, 50] ,'dark_green': [82, 126, 45], 'red': [167, 26, 26], 'light_red': [184, 50, 50], 'orange': [181, 83, 40], 'blue': [45, 87, 176]}


class Player(GameObject):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.rgb = [168, 48, 143]


class Shot(GameObject):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.rgb = [168, 48, 143]


class Hallmonsters(GameObject):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.rgb = [82, 126, 45]


class Goblin(GameObject):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.rgb = [78, 50, 181]


class Serpant(GameObject):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.rgb = [82, 126, 45]


class Skeleton(GameObject):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.rgb = [111, 111, 111]


class Wall(GameObject):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.rgb = [181, 83, 40]


class TwoHeaded(GameObject):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.rgb = [184, 50, 50]


class Troll(GameObject):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.rgb = [111, 111, 111]


class Dragon(GameObject):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.rgb = [134, 134, 29]


class Spider(GameObject):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.rgb = [181, 83, 40]


class Yellow_Collectable(GameObject):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.rgb = [134, 134, 29]


class Grey_Collectable(GameObject):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.rgb = [111, 111, 111]


class Pink_Collectable(GameObject):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.rgb = [151, 25, 122]


class Purple_Collectable(GameObject):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.rgb = [78, 50, 181]


class Green_Collectable(GameObject):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.rgb = [50, 132, 50]


#  ---- HUD -----
class Score(GameObject):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.rgb = [170, 170, 170]


class Life(GameObject):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.rgb = [168, 48, 143]

global static_bricks
static_bricks = None

def _detect_objects(objects, obs, hud=False):
    objects.clear()

    mcc = most_common_color(obs, True)
    
    player = find_objects(obs, objects_colors['red'])
    for bb in player:
        # ply = Player(*bb)
        # ply.rgb = 167, 26, 26
        objects.append(Player(*bb))

    if mcc == (168, 48, 143):
        player2 = find_objects(obs, objects_colors['pink'], size=(1,1), tol_s=1, closing_dist=1)
    else:
        player2 = find_objects(obs, objects_colors['blue'], size=(1,1), tol_s=1, closing_dist=1)
    for bb in player2:
        if len(player) == 0:
            objects.append(Player(*bb))
            hall = find_objects(obs, objects_colors['dark_yellow'])
            for bb in hall:
                objects.append(Hallmonsters(*bb))
        else:
            objects.append(Shot(*bb))
            serpant = find_objects(obs, objects_colors['dark_green'])
            for bb in serpant:
                objects.append(Serpant(*bb))

    spider = find_objects(obs, objects_colors['orange'], size=(8,14), tol_s=1)
    for bb in spider:
        objects.append(Spider(*bb))
    
    wall = find_objects(obs, objects_colors['orange'])
    if len(spider) == 0:
        for bb in wall:
            objects.append(Spider(*bb))

    skeleton = None
    if len(wall) == 0:
        grey = find_objects(obs, objects_colors['dark_grey'])
        yellow = find_objects(obs, objects_colors['yellow'])
        if mcc == (168, 48, 143):
            for bb in grey:
                objects.append(Skeleton(*bb))

            if len(grey):
                purple = find_objects(obs, objects_colors['purple'])
                for bb in purple:
                    objects.append(Purple_Collectable(*bb))
            for bb in yellow:
                objects.append(Yellow_Collectable(*bb))
            
        else:
            if len(grey) != 0 and len(yellow) != 0:
                for bb in grey:
                    objects.append(Troll(*bb))
                for bb in yellow:
                    objects.append(Yellow_Collectable(*bb))

            else:
                for bb in yellow:
                    if mcc == (168, 48, 143):
                        objects.append(Yellow_Collectable(*bb))
                    else:
                        objects.append(Dragon(*bb))
                for bb in grey:
                    objects.append(Grey_Collectable(*bb))
    else:
        grey = find_objects(obs, objects_colors['dark_grey'])
        for bb in grey:
            objects.append(Grey_Collectable(*bb))
    
    if skeleton is None or len(skeleton) == 0:
        goblin = find_objects(obs, objects_colors['purple'])
        for bb in goblin:
            objects.append(Goblin(*bb))

    head = find_objects(obs, objects_colors['light_red'])
    for bb in head:
        objects.append(TwoHeaded(*bb))

    col_pink = find_objects(obs, objects_colors['dark_pink'])
    for bb in col_pink:
        objects.append(Pink_Collectable(*bb))

    col_green = find_objects(obs, objects_colors['green'])
    for bb in col_green:
        objects.append(Green_Collectable(*bb))

    if hud:
        scores = find_objects(obs, objects_colors['grey'], maxy=17, closing_dist=8)
        for bb in scores:
            objects.append(Score(*bb))

        life = find_objects(obs, objects_colors['pink'], maxy=17)
        for bb in life:
            objects.append(Life(*bb))
