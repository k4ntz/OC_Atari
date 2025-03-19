from .utils import find_objects, match_objects, match_blinking_objects
from .game_objects import GameObject, NoObject


hud_color = [132, 144, 252]
player_colors = [[132, 144, 252], [252, 144, 144]]
egg_colors = [[252, 252, 84], [132, 252, 212], [
    252, 144, 144], [236, 140, 224], [132, 144, 252]]
alien_colors = [[236, 140, 224], [252, 252, 84], [132, 252, 212], [101, 111, 228]]
rocket = [252, 252, 84]
pulsar_colors = [[252, 144, 144]]


class Player(GameObject):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.rgb = 132, 144, 252
        self.hud = False


class Egg(GameObject):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.rgb = 0, 0, 0
        self.hud = False
        self.num_frames_invisible = -1
        self.max_frames_invisible = 2


class Alien(GameObject):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.rgb = 132, 252, 212
        self.hud = False
        self.num_frames_invisible = -1
        self.max_frames_invisible = 2


class Pulsar(GameObject):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.rgb = 252, 144, 144
        self.hud = False
        self.num_frames_invisible = -1
        self.max_frames_invisible = 2


class Rocket(GameObject):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.rgb = 252, 252, 84
        self.hud = False


class Score(GameObject):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.rgb = 132, 144, 252
        self.hud = True


class Life(GameObject):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.rgb = 132, 144, 252
        self.count = 0
        self.hud = True


# def _detect_eggs_alien(objects, obs, hud=False):
#     objects.clear()
#     for color in egg_colors:
#         eggs = find_objects(obs, color,size=(1,2), tol_s=1, min_distance=2, minx=86, maxy=24)
#         for e in eggs:
#             eg=Egg(*e)
#             eg.rgb=color
#             objects.append(eg)


def _detect_objects(objects, obs, hud=False):
    # detection and filtering
    for color in player_colors:
        player = find_objects(obs, color, size=(4, 13),
                              tol_s=4, min_distance=1)
        for e in player:
            if type(objects[0]) is NoObject:
                objects[0] = Player(*e)
            objects[0].xywh = e
            objects[0].rgb = color

    aliens = []
    for color in alien_colors:
        alien = find_objects(obs, color, size=(8, 13),
                              tol_s=4, min_distance=1)
        for a in alien:
            # print(alien, alien[0])
            aliens.append([a, color])
    if aliens:
        i = 0
        for e in aliens:
            if type(objects[1+i]) is NoObject:
                objects[1+i] = Alien(*e[0])
            objects[1+i].rgb = e[1]
            i+=1
        match_blinking_objects(objects, [item[0] for item in aliens], 1, 3, Alien)
    else:
        for i in range(3):
            objects[1+i] = NoObject()
            
    for color in pulsar_colors:
        pulsars = find_objects(obs, color, size=(6, 5),
                               tol_s=2, min_distance=1)
        match_blinking_objects(objects, pulsars, 4, 1, Pulsar)
    
    rocket_bb = find_objects(obs, rocket, size=(8,5), tol_s=3, closing_active=False)
    if rocket_bb:
        if type(objects[6]) is NoObject:
            objects[5] = Rocket(*rocket_bb[0])
    else:
        objects[5] = NoObject()

    if all(isinstance(x, NoObject) for x in objects[7:84]):
        eggs = []
        for color in egg_colors:
            eggs.extend(find_objects(obs, color, size=(1, 2), tol_s=2, min_distance=1))
        match_blinking_objects(objects, [item for item in eggs if item[0] < 80], 7, 78, Egg)
        

    for i in range(7, 84):
        if type(objects[i]) is not NoObject:
            x, y = objects[i].xy
            if obs[y][x][0] == 45:
                objects[i].num_frames_invisible+=1
                if objects[i].num_frames_invisible >= objects[i].max_frames_invisible:
                    objects[i] = NoObject()
            else:
                objects[i].num_frames_invisible = -1

    if all(isinstance(x, NoObject) for x in objects[85:163]):
        eggs = []
        for color in egg_colors:
            eggs.extend(find_objects(obs, color, size=(1, 2), tol_s=2, min_distance=1))
        match_blinking_objects(objects, [item for item in eggs if item[0] > 80], 85, 78, Egg)
        

    for i in range(85, 163):
        if type(objects[i]) is not NoObject:
            x, y = objects[i].xy
            if obs[y][x][0] == 45:
                objects[i].num_frames_invisible+=1
                if objects[i].num_frames_invisible >= objects[i].max_frames_invisible:
                    objects[i] = NoObject()
            else:
                objects[i].num_frames_invisible = -1


    if hud:
        score = find_objects(obs, hud_color, miny=174, maxy=183)
        for s in score:
            objects.append(Score(*s))
        count_pulsars = find_objects(
            obs, hud_color, closing_active=False, miny=183, maxy=192)
        for c in count_pulsars:
            objects.append(Life(*c))
