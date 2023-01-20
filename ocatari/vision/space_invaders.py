from .utils import find_objects
from .game_objects import GameObject


objects_colors = {"player": [50, 132, 50], "score": [50, 132, 50],
                  "player2": [162, 134, 56], "score2": [162, 134, 56],
                  "alien": [134, 134, 29], "shield": [181, 83, 40],
                  "satellite": [151, 25, 122], "bullet": [142, 142, 142],
                  "lives": [162, 134, 56]
                  }     # "ground": [80, 89, 22], "background": [0, 0, 0]}


class Player(GameObject):
    def __init__(self, x, y, w, h, num, *args, **kwargs):
        super().__init__(x, y, w, h, *args, **kwargs)
        if num == 1:
            self.rgb = 92, 186, 92
        else:
            self.rgb = 162, 134, 56
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


class Score(GameObject):
    def __init__(self, x, y, w, h, num, *args, **kwargs):
        super().__init__(x, y, w, h, *args, **kwargs)
        if num == 1:
            self.rgb = 92, 186, 92
        else:
            self.rgb = 162, 134, 56


class Lives(GameObject):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.rgb = 162, 134, 56


def _detect_objects_space_invaders(objects, obs, hud):
    objects.clear()
    for i, obj in enumerate(["player", "player2"]):
        scores = find_objects(obs, objects_colors[obj], maxy=30)
        for instance in scores:
            objects.append(Score(*instance, i+1))
        player = find_objects(obs, objects_colors[obj], closing_active=False,
                              miny=180, maxy=195)
        for instance in player:
            if instance[2] < 10:
                objects.append(Player(*instance, i+1))
            else:
                objects.append(Lives(*instance))
    aliens = find_objects(obs, objects_colors["alien"])
    for instance in aliens:
        objects.append(Alien(*instance))
    shields = find_objects(obs, objects_colors["shield"], closing_dist=10)
    for instance in shields:
        objects.append(Shield(*instance))
    satellites = find_objects(obs, objects_colors["satellite"])
    for instance in satellites:
        objects.append(Satellite(*instance))
    bullets = find_objects(obs, objects_colors["bullet"])
    for instance in bullets:
        objects.append(Bullet(*instance))
        # for obj in ["shield", "satellite", "bullets"]:

    # for k, v in objects_colors.items():
    #
    #     bb_by_color(detected, obs, v, k)
    #
    #     if k == "player_green":
    #         detected['bbs'] = [bb for bb in detected['bbs'] if
    #                            bb[5] != "player_green" or bb[0] > 140]
    #
    #     # dangerous. all digits get detected but its not expected because of separation. same for yellow
    #     elif k == "score_green":
    #         detected['bbs'] = [bb for bb in detected['bbs'] if
    #                            bb[5] != "score_green" or bb[0] < 140]
    #
    #     elif k == "player_yellow":
    #         detected['bbs'] = [bb for bb in detected['bbs'] if
    #                            bb[5] != "player_yellow" or bb[0] > 140]
    #
    #     elif k == "score_yellow":
    #         detected['bbs'] = [bb for bb in detected['bbs'] if
    #                            bb[5] != "score_yellow" or bb[0] < 140]
    #
    #     # special case!
    #     elif k == "wall_1":
    #         detected['bbs'] = [bb for bb in detected['bbs'] if
    #                            bb[5] != "wall_1" or 0 < bb[1] < 60]
    #     elif k == "wall_2":
    #         detected['bbs'] = [bb for bb in detected['bbs'] if
    #                            bb[5] != "wall_2" or 60 < bb[1] < 95]
    #     elif k == "wall_3":
    #         detected['bbs'] = [bb for bb in detected['bbs'] if
    #                            bb[5] != "wall_3" or 95 < bb[1] < 150]
    #     # bullets
    #     # one of the problems for bullets is that they could be in same position
    #
    # # objects = {}
    # alien_x = 0
    # import ipdb; ipdb.set_trace()
    # for obj in detected["bbs"]:
    #     x, y, w, h, type, name = obj
    #     r, g, b = objects_colors[name]
    #     if name == "alien":
    #         alien_str = "alien_" + str(alien_x)
    #         objects[alien_str] = (x, y, w, h, r, g, b)
    #         alien_x += 1
    #     else:
    #         objects[name] = (x, y, w, h, r, g, b)
    # info["objects"] = objects
