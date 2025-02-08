from .utils import find_objects, match_objects, match_blinking_objects
from .game_objects import GameObject, NoObject

objects_colors = {"player": [50, 132, 50], "score": [50, 132, 50],
                  "player2": [162, 134, 56], "score2": [162, 134, 56],
                  "alien": [134, 134, 29], "shield": [181, 83, 40],
                  "satellite": [151, 25, 122], "bullet": [142, 142, 142],
                  "lives": [162, 134, 56]
                  }


class Player(GameObject):
    def __init__(self, x, y, w, h, num=1, *args):
        super().__init__(x, y, w, h, *args)
        if num == 1:
            self.rgb = 92, 186, 92
        else:
            self.rgb = 162, 134, 56  # yellow
        self.player_num = num


class Alien(GameObject):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.rgb = 134, 134, 29


class Satellite(GameObject):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.rgb = 151, 25, 122


class Shield(GameObject):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.rgb = 181, 83, 40


class Bullet(GameObject):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.rgb = 142, 142, 142
        self.num_frames_invisible = -1
        self.max_frames_invisible = 4
        self.expected_dist = 3


class P1Score(GameObject):
    def __init__(self, x, y, w, h, *args):
        super().__init__(x, y, w, h, *args)
        self.rgb = 92, 186, 92


class P2Score(GameObject):
    def __init__(self, x, y, w, h, *args):
        super().__init__(x, y, w, h, *args)
        self.rgb = 162, 134, 56


class Lives(GameObject):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.rgb = 162, 134, 56

# MAX_NB_OBJECTS_HUD = {'Player': 1, 'Shield': 3, 'Bullet': 3, 'Satellite': 1, 'Alien': 36, 'Score': 2, 'Lives': 1}


def _detect_objects(objects, obs, hud):
    # objects.clear()
    player = objects[0]
    players_bb = find_objects(obs, objects_colors["player"], closing_active=False,
                              miny=180, maxy=195)
    if players_bb:
        player.xywh = players_bb[0]
    # for i, obj in enumerate(["player", "player2"]):
    #     players = find_objects(obs, objects_colors[obj], closing_active=False,
    #                            miny=180, maxy=195)
    #     for instance in players:
    #         if instance[2] < 10:  # width
    #             objects.append(Player(*instance, i + 1))
    #         elif hud and instance[2] > 10:
    #             objects.append(Lives(*instance))
    shields_bb = find_objects(
        obs, objects_colors["shield"], closing_dist=17, min_distance=20)
    match_objects(objects, shields_bb, 1, 3, Shield)

    bullets_bb = find_objects(obs, objects_colors["bullet"])
    match_blinking_objects(objects, bullets_bb, 4, 3, Bullet)

    satellites_bb = find_objects(obs, objects_colors["satellite"])
    match_objects(objects, satellites_bb, 7, 1, Satellite)

    aliens_bb = find_objects(obs, objects_colors["alien"])
    match_objects(objects, aliens_bb, 8, 36, Alien)

    if hud:
        score1 = objects[44]
        score1_bb = find_objects(
            obs, objects_colors["score"], closing_dist=12, maxy=30)
        if score1_bb:
            if score1:
                score1.xywh = score1_bb[0]
            else:
                objects[44] = P1Score(*score1_bb[0])
        elif score1:
            objects[44] = NoObject()
        score2 = objects[45]
        score2_bb = find_objects(
            obs, objects_colors["score2"], closing_dist=12, maxy=30)
        if score2_bb:
            if score2:
                score2.xywh = score2_bb[0]
            else:
                objects[45] = P2Score(*score2_bb[0])
        elif score2:
            objects[45] = NoObject()
        lives = objects[46]
        lives_bb = find_objects(
            obs, objects_colors["lives"], miny=184, maxy=195)
        if lives_bb:
            if lives:
                lives.xywh = lives_bb[0]
            else:
                objects[46] = Lives(*lives_bb[0])
        elif lives:
            objects[46] = NoObject()
