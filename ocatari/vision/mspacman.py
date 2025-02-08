from .utils import find_objects, match_objects, match_blinking_objects
from .game_objects import GameObject, NoObject

objects_colors = {"player": [210, 164, 74], "life": [187, 187, 53], "score": [195, 144, 61],
                  "ghosts": {"orange": [180, 122, 48], "cyan": [84, 184, 153],
                             "pink": [198, 89, 179], "red": [200, 72, 72], "eatable": [66, 114, 194]},
                  "fruit": {"cherry/strawberry/Apple": [184, 50, 50], "pretzel": [162, 162, 42],
                            "orange/banana": [198, 108, 58], "pear": [110, 156, 66]},
                  "pills": [228, 111, 111]
                  }


class Player(GameObject):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.rgb = 210, 164, 74


class Ghost(GameObject):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.rgb = 180, 122, 48
        self.num_frames_invisible = -1
        self.max_frames_invisible = 4
        self.expected_dist = 10


class Fruit(GameObject):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.rgb = 184, 50, 50

class PowerPill(GameObject):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.rgb = 228, 111, 111
        self.num_frames_invisible = -1
        self.max_frames_invisible = 10
        self.expected_dist = 2

class Pill(GameObject):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.rgb = 228, 111, 111

class Score(GameObject):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.rgb = 195, 144, 61


class Life(GameObject):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.rgb = 187, 187, 53


def _detect_objects(objects, obs, hud=True):

    player = find_objects(obs, objects_colors["player"], min_distance=1)
    if len(player):
        objects[0].xywh = player[0]

    i = 0
    for color in objects_colors["ghosts"]:
        ghosts = find_objects(
            obs, objects_colors["ghosts"][color], min_distance=1)
        match_blinking_objects(objects, ghosts, 1+i, 1, Ghost)
        # if ghosts:
        #     if type(objects[1+i]) is NoObject:
        #         objects[1+i] = Ghost(*ghosts[0])
        #         objects[1+i].rgb = objects_colors["ghosts"][color]
        #     else:
        #         match_blinking_objects(objects, ghosts, 1+i, 1, Ghost)
        #         # objects[1+i].xywh = ghosts[0]
        # else:
        #     objects[1+i] = NoObject()
        i += 1
    
    i = 0
    for color in objects_colors["fruit"]:
        fruits = find_objects(
            obs, objects_colors["fruit"][color], min_distance=1, maxy=170)
        if fruits:
            if type(objects[1+i]) is NoObject:
                objects[5] = Fruit(*fruits[0])
                objects[5].rgb = objects_colors["fruit"][color]
                break
            else:
                objects[5].xywh = fruits[0]
                break
        else:
            objects[5] = NoObject()
        i += 1

    powerpills = find_objects(obs, objects_colors["pills"], minx=5, miny=3, maxx=154, maxy=168, size=(4,7), tol_s=0, closing_active=False)
    match_blinking_objects(objects, powerpills, 6, 4, PowerPill)

    # if type(objects[10]) is NoObject:
    if all(isinstance(x, NoObject) for x in objects[10:262]):
        pills = find_objects(obs, objects_colors["pills"], minx=5, miny=3, maxx=154, maxy=168, size=(4,2), tol_s=0, closing_active=False)
        match_objects(objects, pills, 10, 252, Pill)
        # i = 10
        # for bb in pills:
        #     objects[i] = Pill(*bb)
        #     i+=1

    for i in range(10,262):
        if type(objects[i]) is not NoObject:
            x, y = objects[i].xy
            if obs[y][x][0] == 0:
                objects[i] = NoObject()

    if hud:
        fruit = []
        for i in objects_colors["fruit"]:
            fruit.extend(find_objects(
                obs, objects_colors["fruit"][i], min_distance=1, miny=170))

            if fruit:
                if type(objects[-3]) is NoObject:
                    objects[-3] = Fruit(*fruit[0])
                    objects[-3].rgb = objects_colors["fruit"][i]
                break
        if not fruit:
            objects[-3] = NoObject()

        score = find_objects(
            obs, objects_colors["score"], closing_dist=8, min_distance=1)
        objects[-2].xywh = score[0]

        life = find_objects(
            obs, objects_colors["life"], min_distance=1, closing_dist=20)
        if life:
            if type(objects[-1]) is NoObject:
                objects[-1] = Life(*life[0])
            else:
                objects[-1].xywh = life[0]
