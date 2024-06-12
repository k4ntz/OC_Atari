from .utils import find_objects
from .game_objects import GameObject

objects_colors = {"player": [252, 224, 144], "life": [72, 176, 110], "score": [0, 0, 0],
                  "ghosts": {"pink": [252, 144, 200], "eatable": [252, 144, 200]}, 
                  "powerpill": [252, 144, 200], 
                  }


class Player(GameObject):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.rgb = 210, 164, 74


class Ghost(GameObject):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.rgb = 180, 122, 48


class Fruit(GameObject):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.rgb = 252, 144, 200


class Score(GameObject):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.rgb = 0, 0, 0


class Life(GameObject):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.rgb = 72, 176, 110


class PowerPill(GameObject):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.rgb = 228, 111, 111
        self.hud = False


pps = [(6, 39), (6, 171), (150, 39), (150, 171)]
def _detect_objects(objects, obs, hud=True):
    objects.clear()
    player = find_objects(obs, objects_colors["player"], min_distance=1)
    for bb in player:
        objects.append(Player(*bb))

    for i in objects_colors["ghosts"]:
        ghosts = find_objects(obs, objects_colors["ghosts"][i], min_distance=1)
        for bb in ghosts:
            if bb[2] != 4 and bb[3] != 10:
                ghs = Ghost(*bb)
                ghs.rgb = objects_colors["ghosts"][i]
                objects.append(ghs)
    for pp in pps:
        powp = find_objects(obs, objects_colors["powerpill"], minx=pp[0], miny=pp[1], 
                            maxx=pp[0]+6, maxy=pp[1]+12)
        if powp:
            objects.append(PowerPill(*powp[0])) 
    if hud:
        scores = find_objects(obs, objects_colors["score"], closing_dist=5, min_distance=1, miny=206)
        for s in scores:
            objects.append(Score(*s))
        life = find_objects(obs, objects_colors["life"], min_distance=1, miny=216, maxy=224, closing_dist=10)
        for l1 in life:
            objects.append(Life(*l1))
