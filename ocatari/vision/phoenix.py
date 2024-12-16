from .utils import find_objects, find_mc_objects
from .game_objects import GameObject


objects_colors = {"player": [213, 130, 74], "player_projectile": [158, 208, 101], "enemy_projectile": [236, 236, 236], "enemy_projectile2": [227, 151, 89],
                  "phoenix_base": [125, 48, 173], "phoenix_orange": [227, 151, 89], "phoenix_green": [158, 208, 101],
                  "bat_blue1": [24, 26, 167], "bat_blue2": [45, 50, 184], "bat_blue3": [84, 92, 214], "bat_blue4": [101, 111, 228], "bat_blue5": [132, 144, 252],
                  "bat_red1": [151, 25, 122], "bat_red2": [167, 26, 26], "bat_red3": [184, 50, 50], "bat_red4": [200, 72, 72], "bat_red5": [214, 92, 92],
                  "block_green": [135, 183, 84], "block_blue": [45, 87, 176], "block_red": [167, 26, 26], "boss": [24, 59, 157], "score": [180, 231, 117]}


class Player(GameObject):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.rgb = 213, 130, 74


class Player_Projectile(GameObject):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.rgb = 158, 208, 101


class Phoenix(GameObject):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.rgb = 227, 151, 89


class Enemy_Projectile(GameObject):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.rgb = 227, 151, 89


class Bat(GameObject):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.rgb = 24, 26, 167


class Boss(GameObject):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.rgb = 24, 59, 157


class Boss_Block_Green(GameObject):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.rgb = 135, 183, 84


class Boss_Block_Blue(GameObject):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.rgb = 45, 87, 176


class Boss_Block_Red(GameObject):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.rgb = 167, 26, 26


class Score(GameObject):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.rgb = 180, 231, 117


class Life(GameObject):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.rgb = 213, 130, 74


def _detect_objects(objects, obs, hud=False):
    # detection and filtering
    objects.clear()

    player = find_objects(obs, objects_colors["player"], miny=100)
    for el in player:
        objects.append(Player(*el))

    pproj = find_objects(obs, objects_colors["player_projectile"])
    for el in pproj:
        if el[2] == 1:
            objects.append(Player_Projectile(*el))

    phoenix1 = find_mc_objects(
        obs, [objects_colors["phoenix_orange"], objects_colors["phoenix_base"]])
    for el in phoenix1:
        if el[2] > 1:
            objects.append(Phoenix(*el))

    phoenix2 = find_mc_objects(
        obs, [objects_colors["phoenix_green"], objects_colors["phoenix_base"]])
    for el in phoenix2:
        if el[2] > 1:
            ph = Phoenix(*el)
            ph.rgb = objects_colors["phoenix_green"]
            objects.append(ph)

    green = find_objects(obs, objects_colors["block_green"])
    for el in green:
        objects.append(Boss_Block_Green(*el))

    blue = find_objects(obs, objects_colors["block_blue"])
    for el in blue:
        # if obs[el[1]][el[0]][0] == 45:
        for y in range(int(el[3]/3)):
            for x in range(int(el[2]/4)):
                if obs[el[1]+3*y][el[0]+4*x][0] == 45:
                    objects.append(Boss_Block_Blue(el[0]+4*x, el[1]+3*y, 4, 3))

    boss = find_mc_objects(
        obs, [objects_colors["block_red"], objects_colors["boss"]])
    for el in boss:
        objects.append(Boss(*el))

    if len(green) > 0:
        red = find_objects(obs, objects_colors["block_red"])
        for el in red:
            if obs[el[1]][el[0]][0] == 167:
                for y in range(int(el[3]/3)):
                    for x in range(int(el[2]/4)):
                        if obs[el[1]+3*y][el[0]+4*x][0] == 167:
                            objects.append(Boss_Block_Red(
                                el[0]+4*x, el[1]+3*y, 4, 3))
    else:
        bat2 = find_mc_objects(obs, [objects_colors["bat_red1"], objects_colors["bat_red2"],
                               objects_colors["bat_red3"], objects_colors["bat_red4"], objects_colors["bat_red5"]], all_colors=False)
        for el in bat2:
            if el[2] > 1:
                ph = Bat(*el)
                ph.rgb = objects_colors["bat_red2"]
                objects.append(ph)
            else:
                objects.append(Enemy_Projectile(*el))

    bat1 = find_mc_objects(obs, [objects_colors["bat_blue1"], objects_colors["bat_blue2"],
                           objects_colors["bat_blue3"], objects_colors["bat_blue4"], objects_colors["bat_blue5"]], all_colors=False)
    for el in bat1:
        if el[2] > 1:
            objects.append(Bat(*el))
        else:
            objects.append(Enemy_Projectile(*el))

    eproj = find_objects(obs, objects_colors["enemy_projectile"])
    eproj.extend(find_objects(obs, objects_colors["enemy_projectile2"]))
    for el in eproj:
        if el[2] == 1:
            objects.append(Enemy_Projectile(*el))

    if hud:
        score = find_objects(
            obs, objects_colors["score"], maxy=50, closing_dist=20)
        for el in score:
            objects.append(Score(*el))

        life = find_objects(
            obs, objects_colors["player"], maxy=50, closing_active=False)
        for el in life:
            objects.append(Life(*el))
