from .game_objects import GameObject
from .utils import find_objects, most_common_color

objects_offsets = {'centipede': 3, 'player_and_projectile_and_wall': 0,
                  'spider': 5, 'flea': 1, 'scorpion': 7}

life_and_score_c = [188, 144, 252]


base_colors = [(181, 83, 40), (45, 50, 184), (187, 187, 53), (184, 70, 162), 
               (184, 50, 50), (146, 70, 192), (110, 156, 66), (84, 138, 210)]

ground_colors = [(110, 156, 66), (66, 114, 194), (198, 108, 58), (66, 72, 200), 
                 (162, 162, 42), (184, 70, 162), (200, 72, 72), (146, 70, 192)]

class CentipedeSegment(GameObject):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.rgb = [184, 70, 162]


class Player(GameObject):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.rgb = [181, 83, 40]


class Projectile(GameObject):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.rgb = [181, 83, 40]


class Mushroom(GameObject):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.rgb = [181, 83, 40]


class Spider(GameObject):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.rgb = [146, 70, 192]


class Flea(GameObject):  
    def __init__(self, *args, **kwargs):  
        super().__init__(*args, **kwargs)
        self.rgb = [45, 50, 185]


class Scorpion(GameObject):
    def __init__(self, *args, **kwargs):  
        super().__init__(*args, **kwargs)
        self.rgb = [84, 138, 210]


class Life(GameObject):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.rgb = [188, 144, 252]


class Score(GameObject):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.rgb = [188, 144, 252]


class Ground(GameObject):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.rgb = [110, 156, 66]


def _detect_objects(objects, obs, hud=False):
    objects.clear()
    mccolor = most_common_color(obs[0:182, :, :])
    lvl = base_colors.index(mccolor)

    objcolor = base_colors[(lvl+objects_offsets['centipede'])%8]
    centipede = find_objects(obs, objcolor, min_distance=1)
    for bb in centipede:
        x, y, w, h = bb
        nb_segs = w // 3
        for i in range(nb_segs):
            obj = CentipedeSegment(x+i*3, y, 3, h)
            obj.rgb = objcolor
            objects.append(obj)

    objcolor = base_colors[(lvl+objects_offsets['player_and_projectile_and_wall'])%8]
    player_and_walls = find_objects(obs, objcolor, min_distance=1, closing_dist=1)
    for bb in player_and_walls:
        if bb[3] > 4:
            if bb[2] > 3:
                obj = Player(*bb)
            else:
                obj = Projectile(*bb)
        else:
            obj = Mushroom(*bb)
        obj.rgb = objcolor
        objects.append(obj)

    objcolor = base_colors[(lvl+objects_offsets['spider'])%8]
    spider = find_objects(obs, objcolor, min_distance=1)
    for bb in spider:
        obj = Spider(*bb)
        obj.rgb = objcolor
        objects.append(obj)
    
    objcolor = base_colors[(lvl+objects_offsets['flea'])%8]
    flea = find_objects(obs, objcolor, min_distance=1)
    for bb in flea:
        if bb[2] == 4 and bb[3] == 6: # otherwise score
            obj = Flea(*bb)
            obj.rgb = objcolor
            objects.append(obj)
    
    objcolor = base_colors[(lvl+objects_offsets['scorpion'])%8]
    ghost = find_objects(obs, objcolor, min_distance=1)
    for bb in ghost:
        if bb[2] == 8 and bb[3] == 6: # otherwise score
            obj = Scorpion(*bb)
            obj.rgb = objcolor
            objects.append(obj)

    if hud:
        life_and_score = find_objects(obs, life_and_score_c, min_distance=1, closing_dist=1)
        for bb in life_and_score:
            if bb[0] < 70:
                objects.append(Life(*bb))

            else:
                objects.append(Score(*bb))

        objcolor = ground_colors[lvl%8]
        ground = find_objects(obs, objcolor, min_distance=1)
        for bb in ground:
            obj = Ground(*bb)
            obj.rgb = objcolor
            objects.append(obj)
