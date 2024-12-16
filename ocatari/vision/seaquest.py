from .utils import find_objects, match_objects
from .game_objects import GameObject, NoObject

objects_colors = {"player": [[187, 187, 53], [236, 236, 236]], "diver": [66, 72, 200], "background_water": [0, 28, 136],
                  "player_score": [210, 210, 64], "oxygen_bar": [214, 214, 214], "lives": [210, 210, 64],
                  "logo": [66, 72, 200], "player_missile": [187, 187, 53], "oxygen_bar_depleted": [163, 57, 21],
                  "oxygen_logo": [0, 0, 0], "collected_diver": [24, 26, 167], "enemy_missile": [66, 72, 200],
                  "submarine": [170, 170, 170]}

enemy_colors = {"green": [92, 186, 92], "orange": [198, 108, 58], "yellow": [160, 171, 79], "lightgreen": [72, 160, 72],
                "pink": [198, 89, 179]}


class Player(GameObject):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.rgb = 187, 187, 53


class Diver(GameObject):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.rgb = 66, 72, 200


class Shark(GameObject):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.rgb = 92, 186, 92


class Submarine(GameObject):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.rgb = 170, 170, 170


class PlayerMissile(GameObject):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.rgb = 187, 187, 53


class OxygenBar(GameObject):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.rgb = 214, 214, 214


class OxygenBarDepleted(GameObject):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.rgb = 163, 57, 21


class OxygenBarLogo(GameObject):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.rgb = 0, 0, 0


class PlayerScore(GameObject):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.rgb = 210, 210, 64


class Lives(GameObject):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.rgb = 210, 210, 64


class CollectedDiver(GameObject):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.rgb = 24, 26, 167


class EnemyMissile(GameObject):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.rgb = 66, 72, 200


def _detect_objects(objects, obs, hud=False):
    player = []
    for color in objects_colors["player"]:
        player.extend(find_objects(obs, color, closing_dist=8))

    for p in player:
        if p[1] > 30 and p[3] > 6:
            objects[0].xywh = p
            player.remove(p)
            break
    if player:
        for p in player:
            if p[1] > 30 and p[3] == 1 and p[2] == 8:
                if type(objects[34]) is NoObject:
                    objects[34] = PlayerMissile(*p)
                else:
                    objects[34].xywh = p
                break
    else:
        objects[34] = NoObject()

    divers_and_missiles = find_objects(
        obs, objects_colors["diver"], closing_dist=1)
    divers = []
    missiles = []
    for dm in divers_and_missiles:
        if dm[1] < 190 and dm[2] > 2 and dm[3] > 5:
            divers.append(dm)
        elif dm[1] < 190 and dm[2] > 2:
            missiles.append(dm)

    match_objects(objects, divers, 25, 4, Diver)
    match_objects(objects, missiles, 29, 4, EnemyMissile)

    shark = []
    for enemyColor in enemy_colors.values():
        shark.extend(find_objects(obs, enemyColor, min_distance=1))

    match_objects(objects, shark, 1, 12, Shark)

    submarine = find_objects(obs, objects_colors["submarine"], min_distance=1)
    match_objects(objects, submarine, 13, 12, Submarine)

    oxygen_bar = find_objects(
        obs, objects_colors["oxygen_bar"], min_distance=1)
    if oxygen_bar:
        if type(objects[35]) is NoObject:
            objects[35] = OxygenBar(*oxygen_bar[0])
        else:
            objects[35].xywh = oxygen_bar[0]
    else:
        objects[35] = NoObject()

    coll_diver = find_objects(obs, objects_colors["collected_diver"])

    if coll_diver:
        x, y, w, h = coll_diver[0]
        for i in range(6):
            if i < w/8:
                if type(objects[36+i]) is NoObject:
                    objects[36+i] = CollectedDiver(x+8*i, y, 8, h)
            else:
                objects[36+i] = NoObject()
    else:
        for i in range(6):
            if type(objects[36+i]) != NoObject:
                objects[36+i] = NoObject()

    if hud:
        score = find_objects(
            obs, objects_colors["player_score"], maxy=17, min_distance=1, closing_dist=5)
        objects[-4].xywh = score[0]

        lives = find_objects(
            obs, objects_colors["player_score"], miny=22, maxy=30, min_distance=1, closing_dist=10)
        objects[-3].xywh = lives[0]

        oxygen_bar_depl = find_objects(
            obs, objects_colors["oxygen_bar_depleted"], min_distance=1)
        if oxygen_bar_depl:
            if type(objects[-2]) is NoObject:
                objects[-2] = OxygenBarDepleted(*oxygen_bar_depl[0])
            else:
                objects[-2].xywh = oxygen_bar_depl[0]
        else:
            objects[-2] = NoObject()

        # oxygen_logo = find_objects(obs, objects_colors["oxygen_logo"], min_distance=1)
        # for ox_logo in oxygen_logo:
        #     if ox_logo[0] > 0:
        #         objects.append(OxygenBarLogo(*ox_logo))
