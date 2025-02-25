from .game_objects import GameObject, NoObject
from .utils import find_objects, find_mc_objects, most_common_color, match_blinking_objects
import numpy as np

objects_colors = {'pink': [168, 48, 143], 'dark_pink': [151, 25, 122], 'grey': [170, 170, 170], 'dark_grey': [111, 111, 111],
                  'purple': [78, 50, 181], 'dark_purple': [151, 25, 122], 'yellow': [134, 134, 29], 'dark_yellow': [82, 126, 45],
                  'green': [50, 132, 50], 'dark_green': [82, 126, 45], 'red': [167, 26, 26], 'light_red': [184, 50, 50], 'orange': [181, 83, 40], 'blue': [45, 87, 176]}


class Player(GameObject):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.rgb = [168, 48, 143]
        self.num_frames_invisible = -1
        self.max_frames_invisible = 2
        self.expected_dist = 10


class Shot(GameObject):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.rgb = [168, 48, 143]
        self.num_frames_invisible = -1
        self.max_frames_invisible = 2
        self.expected_dist = 10


class Hallmonsters(GameObject):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.rgb = [82, 126, 45]
        self.num_frames_invisible = -1
        self.max_frames_invisible = 2
        self.expected_dist = 10


class Goblin(GameObject):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.rgb = [78, 50, 181]
        self.num_frames_invisible = -1
        self.max_frames_invisible = 2
        self.expected_dist = 10


class Serpant(GameObject):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.rgb = [82, 126, 45]
        self.num_frames_invisible = -1
        self.max_frames_invisible = 2
        self.expected_dist = 10


class Skeleton(GameObject):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.rgb = [111, 111, 111]
        self.num_frames_invisible = -1
        self.max_frames_invisible = 2
        self.expected_dist = 10


class Wall(GameObject):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.rgb = [181, 83, 40]
        self.num_frames_invisible = -1
        self.max_frames_invisible = 2
        self.expected_dist = 10


class TwoHeaded(GameObject):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.rgb = [184, 50, 50]
        self.num_frames_invisible = -1
        self.max_frames_invisible = 2
        self.expected_dist = 10


class Troll(GameObject):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.rgb = [111, 111, 111]
        self.num_frames_invisible = -1
        self.max_frames_invisible = 2
        self.expected_dist = 10


class Dragon(GameObject):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.rgb = [134, 134, 29]
        self.num_frames_invisible = -1
        self.max_frames_invisible = 2
        self.expected_dist = 10


class Spider(GameObject):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.rgb = [181, 83, 40]
        self.num_frames_invisible = -1
        self.max_frames_invisible = 2
        self.expected_dist = 10


class Yellow_Collectable(GameObject):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.rgb = [134, 134, 29]
        self.num_frames_invisible = -1
        self.max_frames_invisible = 2
        self.expected_dist = 10


class Grey_Collectable(GameObject):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.rgb = [111, 111, 111]
        self.num_frames_invisible = -1
        self.max_frames_invisible = 2
        self.expected_dist = 10


class Pink_Collectable(GameObject):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.rgb = [151, 25, 122]
        self.num_frames_invisible = -1
        self.max_frames_invisible = 2
        self.expected_dist = 10


class Purple_Collectable(GameObject):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.rgb = [78, 50, 181]
        self.num_frames_invisible = -1
        self.max_frames_invisible = 2
        self.expected_dist = 10


class Green_Collectable(GameObject):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.rgb = [50, 132, 50]
        self.num_frames_invisible = -1
        self.max_frames_invisible = 2
        self.expected_dist = 10


#  ---- HUD -----
class Score(GameObject):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.rgb = [170, 170, 170]


class Life(GameObject):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.rgb = [168, 48, 143]


def _detect_objects(objects, obs, hud=False):

    mcc = most_common_color(obs, True)

    player = find_objects(obs, objects_colors['red'])

    if mcc == (168, 48, 143):
        player2 = find_objects(obs, objects_colors['pink'], size=(
            1, 1), tol_s=1, closing_dist=1)
    else:
        player2 = find_objects(obs, objects_colors['blue'], size=(
            1, 1), tol_s=1, closing_dist=1)
        
    if player:
        objects[0].xywh = player[0]

        if player2:
            if type(objects[1]) is NoObject:
                objects[1] = Shot(*player2[0])
            objects[1].xywh = player2[0]

        for i in range(2, 8):
            objects[i] = NoObject()

        serpant = find_objects(obs, objects_colors['dark_green'])
        match_blinking_objects(objects, serpant, 11, 3, Serpant)

        spider = find_objects(obs, objects_colors['orange'], size=(8, 14), tol_s=1)
        match_blinking_objects(objects, spider, 30, 3, Spider)

        if not spider:
            wall = find_objects(obs, objects_colors['orange'])
            match_blinking_objects(objects, wall, 17, 4, Wall)

        if not wall:
            grey = find_objects(obs, objects_colors['dark_grey'])
            yellow = find_objects(obs, objects_colors['yellow'])
            if mcc == (168, 48, 143):
                match_blinking_objects(objects, grey, 14, 3, Skeleton)
                purple = find_objects(obs, objects_colors['purple'])

                if grey:
                    match_blinking_objects(objects, purple, 8, 1, Purple_Collectable)
                else:
                    match_blinking_objects(objects, purple, 36, 1, Goblin)
                    match_blinking_objects(objects, yellow, 33, 1, Yellow_Collectable)

            else:
                if grey and yellow:
                    match_blinking_objects(objects, grey, 8, 3, Goblin)
                    match_blinking_objects(objects, yellow, 33, 1, Yellow_Collectable)

                else:
                    if mcc == (168, 48, 143):
                        match_blinking_objects(objects, yellow, 33, 1, Yellow_Collectable)
                    else:
                        match_blinking_objects(objects, yellow, 27, 3, Dragon)
                    match_blinking_objects(objects, grey, 35, 1, Grey_Collectable)
        else:
            grey = find_objects(obs, objects_colors['dark_grey'])
            match_blinking_objects(objects, grey, 35, 1, Grey_Collectable)

            goblin = find_objects(obs, objects_colors['purple'])
            match_blinking_objects(objects, goblin, 8, 3, Goblin)

        head = find_objects(obs, objects_colors['light_red'])
        match_blinking_objects(objects, head, 21, 3, TwoHeaded)

        col_pink = find_objects(obs, objects_colors['dark_pink'])
        match_blinking_objects(objects, col_pink, 34, 1, Pink_Collectable)

        col_green = find_objects(obs, objects_colors['green'])
        match_blinking_objects(objects, col_green, 37, 1, Pink_Collectable)
    
    else:
        if player2:
            objects[0].xywh = player2[0]

        hall = find_objects(obs, objects_colors['dark_yellow'])
        match_blinking_objects(objects, hall, 2, 6, Hallmonsters)

    if hud:

        life = find_objects(obs, objects_colors['pink'], maxy=17, closing_dist=8)
        if life:
            if type(objects[39]) is NoObject:
                objects[39] = Life(*life[0])
            objects[39].xywh = life[0]
        else:
            objects[39] = NoObject()
