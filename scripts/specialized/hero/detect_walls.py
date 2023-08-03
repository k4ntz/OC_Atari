from ocatari.vision import GameObject
from ocatari.vision.utils import find_objects


Y_MIN_GAMEZONE = 20
Y_MAX_GAMEZONE = 138
X_MIN_GAMEZONE = 8
X_MAX_GAMEZONE = 142

objects_colors = {"brown walls": [[144, 72, 17], [162, 98, 33], [180, 122, 48]],
                  "green walls": [[26, 102, 26], [50, 132, 50], [72, 160, 72]],
                  "blue walls": [[24, 59, 157], [45, 87, 176], [66, 114, 194]],
                  "grey walls": [[74, 74, 74], [111, 111, 111], [142, 142, 142]],
                  "lava wall": [167, 26, 26], }


class Wall(GameObject):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.destructible: bool = False


class LavaWall(GameObject):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.destructible: bool = False


"""
Detects the walls in an image of the Hero game.

So we know that each level in HERO has a predefined number of screens, the RAM only gives us the level we're at and 
at which screen of this level we are. So we want to map each screen of each level using the method detect walls.
"""


def detect_Walls(obs):
    walls = []
    possible_wall_colors = ["brown", "green", "blue", "grey"]
    stage_zone_y = [20, 60, 100, 150]
    color_is_found = False
    for color in possible_wall_colors:
        if len(find_objects(obs, objects_colors[color + " walls"][0], miny=20, maxy=60)) > 0:
            for i in range(3):
                for wall in find_objects(obs, objects_colors[color + " walls"][i], miny=stage_zone_y[i] + 1,
                                         maxy=stage_zone_y[i + 1], minx=X_MIN_GAMEZONE, closing_dist=2):
                    wall_instance = Wall(*wall)
                    if wall[3] > 12 and not (
                            wall_instance.x > 8 and wall_instance.x + wall_instance.w < 149 and wall_instance.w < 12):
                        walls.append(Wall(*wall))
                        color_is_found = True
            if color_is_found:
                break


    return walls


def detect_lava_walls(obs):
    stage_zone_y = [20, 60, 100, 142]
    lava_walls = []
    for i in range(3):
        for lava_wall in find_objects(obs, objects_colors["lava wall"], miny=stage_zone_y[i] + 1,
                                      maxy=stage_zone_y[i + 1], minx=X_MIN_GAMEZONE, closing_dist=2):
            wall_instance = LavaWall(*lava_wall)
            if wall_instance.x > 8 and wall_instance.x + wall_instance.w < 149 and wall_instance.w < 12:
                wall_instance.destructible = True
            lava_walls.append(wall_instance)
    # for lava_wall in find_objects(obs, [187,50,50], miny=stage_zone_y[i] + 1,
    #                          maxy=stage_zone_y[i + 1], minx=X_MIN_GAMEZONE, closing_dist=2):
    #     if lava_wall[3] > 12:
    #         wall_instance = LavaWall(*lava_wall)
    #         if wall_instance.x > 8 and wall_instance.x + wall_instance.w < 149 and wall_instance.w < 12:
    #             wall_instance.destructible = True
    #         lava_walls.append(wall_instance)
    return lava_walls

