from enum import Enum

from .game_objects import GameObject
from .utils import find_objects

objects_colors = {"brown walls": [[144, 72, 17], [162, 98, 33], [180, 122, 48]],
                  "green walls": [[26, 102, 26], [50, 132, 50], [72, 160, 72]],
                  "blue walls": [[24, 59, 157], [45, 87, 176], [66, 114, 194]],
                  "grey walls": [[74, 74, 74], [111, 111, 111], [142, 142, 142]],
                  "lava wall": [167, 26, 26], "platform": [232, 232, 74],
                  "enemy": [[210, 164, 74], [195, 144, 61], [180, 122, 48], [162, 98, 33], [142, 142, 142]],
                  "snake": [[111, 210, 111], [50, 132, 50]],
                  "tentacle": [101, 183, 217], "player": [84, 138, 210],
                  "bomb": [184, 50, 50], "laser beam": [200, 72, 72], "end NPC": [92, 186, 92], "lamp": [142, 142, 142],
                  "powerbar full": [232, 232, 74], "powerbar depleted": [167, 26, 26], "life": [45, 87, 176],
                  "score": [214, 214, 214], "life": [45, 87, 176]}

Y_MIN_GAMEZONE = 20
Y_MAX_GAMEZONE = 138
X_MIN_GAMEZONE = 8
X_MAX_GAMEZONE = 142


# breakable walls are a certain size (<12px approximately) and can't touch the border (x=8/x=159) of the screen


class Wall(GameObject):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.destructible: bool = False


class LavaWall(GameObject):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.destructible: bool = False


class Platform(GameObject):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


class EnemyType(Enum):
    Spider = 1
    Bat = 2
    Moth = 3
    Snake = 4
    Tentacle = 5


class Enemy(GameObject):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.type: EnemyType


class Snake(GameObject):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


class Player(GameObject):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.rgb = 144, 72, 17
        self.wh = 6, 25


class LaserBeam(GameObject):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


class Bomb(GameObject):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


class EndNPC(GameObject):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


class Lamp(GameObject):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


class PowerBar(GameObject):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.value = 1


class BombStock(GameObject):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


class Life(GameObject):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


class Score(GameObject):
    """
    The player's score display (HUD).
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.value = 0


def _detect_objects(objects, obs, hud=True):
    objects.clear()
    possible_wall_colors = ["brown", "green", "blue", "grey"]
    stage_zone_y = [20, 60, 100, 150]
    color_is_found = False
    destructible_wall_is_added = False

    for i in range(3):
        for lava_wall in find_objects(obs, objects_colors["lava wall"], miny=stage_zone_y[i] + 1,
                                      maxy=stage_zone_y[i + 1], minx=X_MIN_GAMEZONE, closing_dist=2):
            if lava_wall[3] > 12:
                wall_instance = LavaWall(*lava_wall)
                if wall_instance.x > 8 and wall_instance.x + wall_instance.w < 149 and wall_instance.w < 12:
                    wall_instance.destructible = True
                    destructible_wall_is_added = True
                    wall_instance.wh = wall_instance.w, 79
                objects.append(wall_instance)

    for color in possible_wall_colors:
        if len(find_objects(obs, objects_colors[color + " walls"][0], miny=20, maxy=60)) > 0:
            for i in range(3):
                for wall in find_objects(obs, objects_colors[color + " walls"][i], miny=stage_zone_y[i] + 1,
                                         maxy=stage_zone_y[i + 1], minx=X_MIN_GAMEZONE, closing_dist=2):
                    if wall[3] > 15:
                        wall_instance = Wall(*wall)
                        wall_instance.rgb = objects_colors[color + " walls"][i]
                        if wall_instance.x > 8 and wall_instance.x + wall_instance.w < 149 and wall_instance.w < 12 and not destructible_wall_is_added:
                            destructible_wall_is_added = True
                            wall_instance.destructible = True
                            wall_instance.wh = wall_instance.w, 79
                        objects.append(wall_instance)
                        color_is_found = True
            if color_is_found:
                break

    for enemy in find_objects(obs, objects_colors["enemy"][0], closing_dist=6, miny=Y_MIN_GAMEZONE,
                              maxy=Y_MAX_GAMEZONE, minx=X_MIN_GAMEZONE):
        list_of_x = []
        list_of_y = []
        for color in objects_colors["enemy"][0:3]:
            for enemy_pixel in find_objects(obs, color, minx=enemy[0] - 6, maxx=enemy[0] + 6,
                                            miny=enemy[1] - 6, maxy=enemy[1] + 6):
                list_of_x.append(enemy_pixel[0])
                list_of_x.append(enemy_pixel[0] + enemy_pixel[2])
                list_of_y.append(enemy_pixel[1])
                list_of_y.append(enemy_pixel[1] + enemy_pixel[3])
        x, y = min(list_of_x), min(list_of_y)
        w, h = max(list_of_x) - x, max(list_of_y) - y + 1
        objects.append(Enemy(x, y, w, h))

    # if we encouter a moth
    for enemy in find_objects(obs, objects_colors["enemy"][3], closing_dist=6, miny=Y_MIN_GAMEZONE,
                              maxy=Y_MAX_GAMEZONE, minx=X_MIN_GAMEZONE):
        list_of_x = []
        list_of_y = []
        if enemy[3]< 7:
            for enemy_pixel in find_objects(obs, objects_colors["enemy"][4], minx=enemy[0] - 6, maxx=enemy[0] + 6,
                                                miny=enemy[1] - 6, maxy=enemy[1] + 6):
                list_of_x.append(enemy_pixel[0])
                list_of_x.append(enemy_pixel[0] + enemy_pixel[2])
                list_of_y.append(enemy_pixel[1])
                list_of_y.append(enemy_pixel[1] + enemy_pixel[3])
            if len(list_of_x) !=0:
                x, y = min(list_of_x), min(list_of_y)
                w, h = max(list_of_x) - x, max(list_of_y) - y
                objects.append(Enemy(x, y, w, h))

    for snake in find_objects(obs, objects_colors["snake"][0], miny=Y_MIN_GAMEZONE,
                              maxy=Y_MAX_GAMEZONE, minx=X_MIN_GAMEZONE):
        snake_instance = Enemy(*snake)
        for snake_head in find_objects(obs, objects_colors["snake"][1], miny=snake_instance.y - 4,
                                       maxy=snake_instance.y + 4, minx=X_MIN_GAMEZONE, closing_dist=4):
            snake_instance.xy = snake_instance.x, snake_head[1]
            snake_instance.type = 4
        objects.append(snake_instance)

    for player in find_objects(obs, objects_colors["player"], miny=Y_MIN_GAMEZONE, maxy=Y_MAX_GAMEZONE,
                               minx=X_MIN_GAMEZONE):
        player_instance = Player(*player)
        player_instance.xy = player_instance.x, player_instance.y - 8
        objects.append(player_instance)
        for laser_beam in find_objects(obs, objects_colors["laser beam"],
                                       miny=max(Y_MIN_GAMEZONE, player_instance.y - 10),
                                       maxy=max(Y_MIN_GAMEZONE + 1,
                                                min(10 + player_instance.y, Y_MAX_GAMEZONE)),
                                       minx=max(player_instance.x - 10, X_MIN_GAMEZONE),
                                       maxx=min(player_instance.x + 10, X_MAX_GAMEZONE)):
            if laser_beam[2] > 6:
                objects.append(LaserBeam(*laser_beam))

        for bomb in find_objects(obs, objects_colors["bomb"], miny=Y_MIN_GAMEZONE, maxy=Y_MAX_GAMEZONE,
                                 minx=X_MIN_GAMEZONE):
            bomb_instance = Bomb(*bomb)
            bomb_instance.xy = bomb_instance.x, bomb_instance.y - 5
            bomb_instance.wh = bomb_instance.w, bomb_instance.h + 5
            if not (player_instance.y + 2 >= bomb_instance.y >= player_instance.y - 2) :

                objects.append(bomb_instance)

    for end_npc in find_objects(obs, objects_colors["end NPC"], miny=Y_MIN_GAMEZONE, maxy=Y_MAX_GAMEZONE,
                                minx=X_MIN_GAMEZONE):
        end_npc_instance = EndNPC(*end_npc)
        end_npc_instance.xy = end_npc_instance.x - 1, end_npc_instance.y - 5
        end_npc_instance.wh = 6, end_npc_instance.h + 8
        objects.append(end_npc_instance)

    for tentacle in find_objects(obs, objects_colors["tentacle"], miny=120, maxy=Y_MAX_GAMEZONE,
                                 minx=X_MIN_GAMEZONE):
        tentacle = Enemy(*tentacle)
        tentacle.type = 5
        objects.append(tentacle)

    for platform in find_objects(obs, objects_colors["platform"], miny=135, maxy=Y_MAX_GAMEZONE,
                                 minx=X_MIN_GAMEZONE):
        platform = Platform(*platform)
        objects.append(platform)

    for lamp in find_objects(obs, objects_colors["lamp"], miny=Y_MIN_GAMEZONE, maxy=Y_MAX_GAMEZONE,
                             minx=X_MIN_GAMEZONE):
        lamp = Lamp(*lamp)
        lamp.wh = lamp.w, lamp.h + 1
        if lamp.h < 10 and lamp.h > 2:
            objects.append(lamp)

    if hud:
        for life in find_objects(obs, objects_colors["life"], miny=159,
                                 minx=X_MIN_GAMEZONE, closing_dist=7):
            life_instance = Life(*life)
            life_instance.xy = life_instance.x - 1, life_instance.y - 7
            life_instance.wh = life_instance.w + 1, 12
            objects.append(life_instance)

        for bomb in find_objects(obs, objects_colors["bomb"], miny=170, maxy=178, minx=X_MIN_GAMEZONE, closing_dist=7):
            bomb_instance = BombStock(*bomb)
            bomb_instance.value = len(find_objects(obs, objects_colors["bomb"], miny=1, minx=X_MIN_GAMEZONE))
            bomb_instance.xy = bomb_instance.x, bomb_instance.y - 5
            bomb_instance.wh = bomb_instance.w, bomb_instance.h + 5
            objects.append(bomb_instance)

        power_instance = PowerBar(49, 145, 0, 0)
        for power in find_objects(obs, objects_colors["powerbar full"], miny=143, maxy=150,
                                  minx=X_MIN_GAMEZONE):
            x, y, w, h = power
            power_instance.wh = w, h

        for power in find_objects(obs, objects_colors["powerbar depleted"], miny=143, maxy=150,
                                  minx=X_MIN_GAMEZONE):
            x, y, w, h = power
            power_instance.wh = power_instance.w + w, h
            power_instance.value = w / power_instance.w
        objects.append(power_instance)

        for score in find_objects(obs, objects_colors["score"], miny=178, maxy=187,
                                  minx=X_MIN_GAMEZONE, closing_dist=8):
            objects.append(Score(*score))
    # for wall in find_objects(obs, objects_colors["wall"]):
    #     objects.append(Wall(*wall))
    return objects
