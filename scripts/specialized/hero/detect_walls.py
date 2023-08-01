from ocatari.vision import GameObject
from ocatari.vision.utils import find_objects

Y_MIN_GAMEZONE = 20
Y_MAX_GAMEZONE = 138
X_MIN_GAMEZONE = 8
X_MAX_GAMEZONE = 150

objects_colors = {"brown walls": [[144, 72, 17], [162, 98, 33], [180, 122, 48]],
                  "green walls": [[26, 102, 26], [50, 132, 150], [72, 160, 72]],
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

    for lava_wall in find_objects(obs, objects_colors["lava wall"], closing_dist=4, miny=Y_MIN_GAMEZONE,
                                  maxy=Y_MAX_GAMEZONE, minx=X_MIN_GAMEZONE):
        walls.append(LavaWall(*lava_wall))

    return walls

def add_walls_to_object_list(ram_state, objects, objects_map):
    if ram_state[117] == 0:
        if ram_state[28] == 0:
            wall_instance = Wall()
            wall_instance.xy = (136, 21)
            wall_instance.wh = (24, 38)
            objects.append(wall_instance)
            objects_map['fixed_wall 0'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (8, 21)
            wall_instance.wh = (16, 38)
            objects.append(wall_instance)
            objects_map['fixed_wall 1'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (144, 61)
            wall_instance.wh = (16, 37)
            objects.append(wall_instance)
            objects_map['fixed_wall 2'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (8, 61)
            wall_instance.wh = (8, 37)
            objects.append(wall_instance)
            objects_map['fixed_wall 3'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (88, 101)
            wall_instance.wh = (72, 38)
            objects.append(wall_instance)
            objects_map['fixed_wall 4'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (8, 101)
            wall_instance.wh = (64, 38)
            objects.append(wall_instance)
            objects_map['fixed_wall 5'] = wall_instance
            number_of_walls = 6
            i = 0
            while(objects_map.get(f"fixed wall {number_of_walls + i}")!= None):
                objects_map.pop(f"fixed wall {number_of_walls + i}")
                i += 1
        elif ram_state[28] == 1:
            wall_instance = Wall()
            wall_instance.xy = (88, 21)
            wall_instance.wh = (72, 38)
            objects.append(wall_instance)
            objects_map['fixed_wall 0'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (8, 21)
            wall_instance.wh = (64, 38)
            objects.append(wall_instance)
            objects_map['fixed_wall 1'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (136, 61)
            wall_instance.wh = (24, 37)
            objects.append(wall_instance)
            objects_map['fixed_wall 2'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (8, 61)
            wall_instance.wh = (16, 37)
            objects.append(wall_instance)
            objects_map['fixed_wall 3'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (8, 101)
            wall_instance.wh = (152, 38)
            objects.append(wall_instance)
            objects_map['fixed_wall 4'] = wall_instance
            number_of_walls = 5
            i = 0
            while(objects_map.get(f"fixed wall {number_of_walls + i}")!= None):
                objects_map.pop(f"fixed wall {number_of_walls + i}")
                i += 1

    elif ram_state[117] == 1:
        if ram_state[28] == 0:
            wall_instance = Wall()
            wall_instance.xy = (136, 21)
            wall_instance.wh = (24, 39)
            objects.append(wall_instance)
            objects_map['fixed_wall 0'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (8, 21)
            wall_instance.wh = (16, 39)
            objects.append(wall_instance)
            objects_map['fixed_wall 1'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (144, 62)
            wall_instance.wh = (16, 37)
            objects.append(wall_instance)
            objects_map['fixed_wall 2'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (8, 62)
            wall_instance.wh = (8, 37)
            objects.append(wall_instance)
            objects_map['fixed_wall 3'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (88, 101)
            wall_instance.wh = (72, 39)
            objects.append(wall_instance)
            objects_map['fixed_wall 4'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (8, 101)
            wall_instance.wh = (64, 39)
            objects.append(wall_instance)
            objects_map['fixed_wall 5'] = wall_instance
            number_of_walls = 6
            i = 0
            while(objects_map.get(f"fixed wall {number_of_walls + i}")!= None):
                objects_map.pop(f"fixed wall {number_of_walls + i}")
                i += 1
        elif ram_state[28] == 1:
            wall_instance = Wall()
            wall_instance.xy = (88, 21)
            wall_instance.wh = (72, 38)
            objects.append(wall_instance)
            objects_map['fixed_wall 0'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (8, 21)
            wall_instance.wh = (64, 38)
            objects.append(wall_instance)
            objects_map['fixed_wall 1'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (144, 61)
            wall_instance.wh = (16, 37)
            objects.append(wall_instance)
            objects_map['fixed_wall 2'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (8, 61)
            wall_instance.wh = (8, 37)
            objects.append(wall_instance)
            objects_map['fixed_wall 3'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (120, 101)
            wall_instance.wh = (40, 38)
            objects.append(wall_instance)
            objects_map['fixed_wall 4'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (48, 101)
            wall_instance.wh = (64, 38)
            objects.append(wall_instance)
            objects_map['fixed_wall 5'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (8, 101)
            wall_instance.wh = (32, 38)
            objects.append(wall_instance)
            objects_map['fixed_wall 6'] = wall_instance
            number_of_walls = 7
            i = 0
            while(objects_map.get(f"fixed wall {number_of_walls + i}")!= None):
                objects_map.pop(f"fixed wall {number_of_walls + i}")
                i += 1
        elif ram_state[28] == 2:
            wall_instance = Wall()
            wall_instance.xy = (120, 21)
            wall_instance.wh = (40, 38)
            objects.append(wall_instance)
            objects_map['fixed_wall 0'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (48, 21)
            wall_instance.wh = (64, 38)
            objects.append(wall_instance)
            objects_map['fixed_wall 1'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (8, 21)
            wall_instance.wh = (32, 38)
            objects.append(wall_instance)
            objects_map['fixed_wall 2'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (144, 61)
            wall_instance.wh = (16, 37)
            objects.append(wall_instance)
            objects_map['fixed_wall 3'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (64, 61)
            wall_instance.wh = (44, 37)
            objects.append(wall_instance)
            objects_map['fixed_wall 4'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (8, 61)
            wall_instance.wh = (20, 37)
            objects.append(wall_instance)
            objects_map['fixed_wall 5'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (104, 101)
            wall_instance.wh = (56, 38)
            objects.append(wall_instance)
            objects_map['fixed_wall 6'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (8, 101)
            wall_instance.wh = (48, 38)
            objects.append(wall_instance)
            objects_map['fixed_wall 7'] = wall_instance
            number_of_walls = 8
            i = 0
            while(objects_map.get(f"fixed wall {number_of_walls + i}")!= None):
                objects_map.pop(f"fixed wall {number_of_walls + i}")
                i += 1
        elif ram_state[28] == 3:
            wall_instance = Wall()
            wall_instance.xy = (104, 21)
            wall_instance.wh = (56, 38)
            objects.append(wall_instance)
            objects_map['fixed_wall 0'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (8, 21)
            wall_instance.wh = (48, 38)
            objects.append(wall_instance)
            objects_map['fixed_wall 1'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (136, 61)
            wall_instance.wh = (24, 37)
            objects.append(wall_instance)
            objects_map['fixed_wall 2'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (8, 61)
            wall_instance.wh = (16, 37)
            objects.append(wall_instance)
            objects_map['fixed_wall 3'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (8, 101)
            wall_instance.wh = (152, 38)
            objects.append(wall_instance)
            objects_map['fixed_wall 4'] = wall_instance
            number_of_walls = 5
            i = 0
            while(objects_map.get(f"fixed wall {number_of_walls + i}")!= None):
                objects_map.pop(f"fixed wall {number_of_walls + i}")
                i += 1

    elif ram_state[117] == 2:
        if ram_state[28] == 0:
            wall_instance = Wall()
            wall_instance.xy = (136, 21)
            wall_instance.wh = (24, 38)
            objects.append(wall_instance)
            objects_map['fixed_wall 0'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (8, 21)
            wall_instance.wh = (16, 38)
            objects.append(wall_instance)
            objects_map['fixed_wall 1'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (144, 61)
            wall_instance.wh = (16, 37)
            objects.append(wall_instance)
            objects_map['fixed_wall 2'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (8, 61)
            wall_instance.wh = (8, 37)
            objects.append(wall_instance)
            objects_map['fixed_wall 3'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (88, 101)
            wall_instance.wh = (72, 38)
            objects.append(wall_instance)
            objects_map['fixed_wall 4'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (8, 101)
            wall_instance.wh = (64, 38)
            objects.append(wall_instance)
            objects_map['fixed_wall 5'] = wall_instance
            number_of_walls = 6
            i = 0
            while(objects_map.get(f"fixed wall {number_of_walls + i}")!= None):
                objects_map.pop(f"fixed wall {number_of_walls + i}")
                i += 1
        elif ram_state[28] == 1:
            wall_instance = Wall()
            wall_instance.xy = (88, 21)
            wall_instance.wh = (72, 38)
            objects.append(wall_instance)
            objects_map['fixed_wall 0'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (8, 21)
            wall_instance.wh = (64, 38)
            objects.append(wall_instance)
            objects_map['fixed_wall 1'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (144, 61)
            wall_instance.wh = (16, 37)
            objects.append(wall_instance)
            objects_map['fixed_wall 2'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (8, 61)
            wall_instance.wh = (8, 37)
            objects.append(wall_instance)
            objects_map['fixed_wall 3'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (136, 101)
            wall_instance.wh = (24, 38)
            objects.append(wall_instance)
            objects_map['fixed_wall 4'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (8, 101)
            wall_instance.wh = (16, 38)
            objects.append(wall_instance)
            objects_map['fixed_wall 5'] = wall_instance
            number_of_walls = 6
            i = 0
            while(objects_map.get(f"fixed wall {number_of_walls + i}")!= None):
                objects_map.pop(f"fixed wall {number_of_walls + i}")
                i += 1
        elif ram_state[28] == 2:
            wall_instance = Wall()
            wall_instance.xy = (136, 21)
            wall_instance.wh = (24, 38)
            objects.append(wall_instance)
            objects_map['fixed_wall 0'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (8, 21)
            wall_instance.wh = (16, 38)
            objects.append(wall_instance)
            objects_map['fixed_wall 1'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (144, 61)
            wall_instance.wh = (16, 37)
            objects.append(wall_instance)
            objects_map['fixed_wall 2'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (8, 61)
            wall_instance.wh = (8, 37)
            objects.append(wall_instance)
            objects_map['fixed_wall 3'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (112, 101)
            wall_instance.wh = (48, 38)
            objects.append(wall_instance)
            objects_map['fixed_wall 4'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (56, 101)
            wall_instance.wh = (48, 38)
            objects.append(wall_instance)
            objects_map['fixed_wall 5'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (8, 101)
            wall_instance.wh = (40, 38)
            objects.append(wall_instance)
            objects_map['fixed_wall 6'] = wall_instance
            number_of_walls = 7
            i = 0
            while(objects_map.get(f"fixed wall {number_of_walls + i}")!= None):
                objects_map.pop(f"fixed wall {number_of_walls + i}")
                i += 1
        elif ram_state[28] == 3:
            wall_instance = Wall()
            wall_instance.xy = (112, 21)
            wall_instance.wh = (48, 38)
            objects.append(wall_instance)
            objects_map['fixed_wall 0'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (56, 21)
            wall_instance.wh = (48, 38)
            objects.append(wall_instance)
            objects_map['fixed_wall 1'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (8, 21)
            wall_instance.wh = (40, 38)
            objects.append(wall_instance)
            objects_map['fixed_wall 2'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (144, 61)
            wall_instance.wh = (16, 37)
            objects.append(wall_instance)
            objects_map['fixed_wall 3'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (8, 61)
            wall_instance.wh = (8, 37)
            objects.append(wall_instance)
            objects_map['fixed_wall 4'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (120, 101)
            wall_instance.wh = (40, 38)
            objects.append(wall_instance)
            objects_map['fixed_wall 5'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (48, 101)
            wall_instance.wh = (64, 38)
            objects.append(wall_instance)
            objects_map['fixed_wall 6'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (8, 101)
            wall_instance.wh = (32, 38)
            objects.append(wall_instance)
            objects_map['fixed_wall 7'] = wall_instance
            number_of_walls = 8
            i = 0
            while(objects_map.get(f"fixed wall {number_of_walls + i}")!= None):
                objects_map.pop(f"fixed wall {number_of_walls + i}")
                i += 1
        elif ram_state[28] == 4:
            wall_instance = Wall()
            wall_instance.xy = (120, 21)
            wall_instance.wh = (40, 38)
            objects.append(wall_instance)
            objects_map['fixed_wall 0'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (48, 21)
            wall_instance.wh = (64, 38)
            objects.append(wall_instance)
            objects_map['fixed_wall 1'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (8, 21)
            wall_instance.wh = (32, 38)
            objects.append(wall_instance)
            objects_map['fixed_wall 2'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (144, 61)
            wall_instance.wh = (16, 37)
            objects.append(wall_instance)
            objects_map['fixed_wall 3'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (8, 61)
            wall_instance.wh = (8, 37)
            objects.append(wall_instance)
            objects_map['fixed_wall 4'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (88, 101)
            wall_instance.wh = (72, 38)
            objects.append(wall_instance)
            objects_map['fixed_wall 5'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (8, 101)
            wall_instance.wh = (64, 38)
            objects.append(wall_instance)
            objects_map['fixed_wall 6'] = wall_instance
            number_of_walls = 7
            i = 0
            while(objects_map.get(f"fixed wall {number_of_walls + i}")!= None):
                objects_map.pop(f"fixed wall {number_of_walls + i}")
                i += 1
        elif ram_state[28] == 5:
            wall_instance = Wall()
            wall_instance.xy = (88, 21)
            wall_instance.wh = (72, 38)
            objects.append(wall_instance)
            objects_map['fixed_wall 0'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (8, 21)
            wall_instance.wh = (64, 38)
            objects.append(wall_instance)
            objects_map['fixed_wall 1'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (136, 61)
            wall_instance.wh = (24, 37)
            objects.append(wall_instance)
            objects_map['fixed_wall 2'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (8, 61)
            wall_instance.wh = (16, 37)
            objects.append(wall_instance)
            objects_map['fixed_wall 3'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (8, 101)
            wall_instance.wh = (152, 38)
            objects.append(wall_instance)
            objects_map['fixed_wall 4'] = wall_instance
            number_of_walls = 5
            i = 0
            while(objects_map.get(f"fixed wall {number_of_walls + i}")!= None):
                objects_map.pop(f"fixed wall {number_of_walls + i}")
                i += 1

    elif ram_state[117] == 3:
        if ram_state[28] == 0:
            wall_instance = Wall()
            wall_instance.xy = (136, 21)
            wall_instance.wh = (24, 38)
            objects.append(wall_instance)
            objects_map['fixed_wall 0'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (8, 21)
            wall_instance.wh = (16, 38)
            objects.append(wall_instance)
            objects_map['fixed_wall 1'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (140, 61)
            wall_instance.wh = (20, 37)
            objects.append(wall_instance)
            objects_map['fixed_wall 2'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (8, 61)
            wall_instance.wh = (12, 37)
            objects.append(wall_instance)
            objects_map['fixed_wall 3'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (88, 101)
            wall_instance.wh = (72, 38)
            objects.append(wall_instance)
            objects_map['fixed_wall 4'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (8, 101)
            wall_instance.wh = (64, 38)
            objects.append(wall_instance)
            objects_map['fixed_wall 5'] = wall_instance
            number_of_walls = 6
            i = 0
            while(objects_map.get(f"fixed wall {number_of_walls + i}")!= None):
                objects_map.pop(f"fixed wall {number_of_walls + i}")
                i += 1
        elif ram_state[28] == 1:
            wall_instance = Wall()
            wall_instance.xy = (88, 21)
            wall_instance.wh = (72, 38)
            objects.append(wall_instance)
            objects_map['fixed_wall 0'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (8, 21)
            wall_instance.wh = (64, 38)
            objects.append(wall_instance)
            objects_map['fixed_wall 1'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (144, 61)
            wall_instance.wh = (16, 37)
            objects.append(wall_instance)
            objects_map['fixed_wall 2'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (8, 61)
            wall_instance.wh = (8, 37)
            objects.append(wall_instance)
            objects_map['fixed_wall 3'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (140, 101)
            wall_instance.wh = (20, 38)
            objects.append(wall_instance)
            objects_map['fixed_wall 4'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (28, 101)
            wall_instance.wh = (104, 38)
            objects.append(wall_instance)
            objects_map['fixed_wall 5'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (8, 101)
            wall_instance.wh = (12, 38)
            objects.append(wall_instance)
            objects_map['fixed_wall 6'] = wall_instance
            number_of_walls = 7
            i = 0
            while(objects_map.get(f"fixed wall {number_of_walls + i}")!= None):
                objects_map.pop(f"fixed wall {number_of_walls + i}")
                i += 1
        elif ram_state[28] == 2:
            wall_instance = Wall()
            wall_instance.xy = (140, 21)
            wall_instance.wh = (20, 38)
            objects.append(wall_instance)
            objects_map['fixed_wall 0'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (28, 21)
            wall_instance.wh = (104, 38)
            objects.append(wall_instance)
            objects_map['fixed_wall 1'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (8, 21)
            wall_instance.wh = (12, 38)
            objects.append(wall_instance)
            objects_map['fixed_wall 2'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (144, 61)
            wall_instance.wh = (16, 37)
            objects.append(wall_instance)
            objects_map['fixed_wall 3'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (40, 61)
            wall_instance.wh = (80, 37)
            objects.append(wall_instance)
            objects_map['fixed_wall 4'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (8, 61)
            wall_instance.wh = (8, 37)
            objects.append(wall_instance)
            objects_map['fixed_wall 5'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (128, 101)
            wall_instance.wh = (32, 38)
            objects.append(wall_instance)
            objects_map['fixed_wall 6'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (44, 101)
            wall_instance.wh = (72, 38)
            objects.append(wall_instance)
            objects_map['fixed_wall 7'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (8, 101)
            wall_instance.wh = (24, 38)
            objects.append(wall_instance)
            objects_map['fixed_wall 8'] = wall_instance
            number_of_walls = 9
            i = 0
            while(objects_map.get(f"fixed wall {number_of_walls + i}")!= None):
                objects_map.pop(f"fixed wall {number_of_walls + i}")
                i += 1
        elif ram_state[28] == 3:
            wall_instance = Wall()
            wall_instance.xy = (128, 21)
            wall_instance.wh = (32, 38)
            objects.append(wall_instance)
            objects_map['fixed_wall 0'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (44, 21)
            wall_instance.wh = (72, 38)
            objects.append(wall_instance)
            objects_map['fixed_wall 1'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (8, 21)
            wall_instance.wh = (24, 38)
            objects.append(wall_instance)
            objects_map['fixed_wall 2'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (140, 61)
            wall_instance.wh = (20, 37)
            objects.append(wall_instance)
            objects_map['fixed_wall 3'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (48, 61)
            wall_instance.wh = (64, 37)
            objects.append(wall_instance)
            objects_map['fixed_wall 4'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (8, 61)
            wall_instance.wh = (12, 37)
            objects.append(wall_instance)
            objects_map['fixed_wall 5'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (144, 101)
            wall_instance.wh = (16, 38)
            objects.append(wall_instance)
            objects_map['fixed_wall 6'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (32, 101)
            wall_instance.wh = (96, 38)
            objects.append(wall_instance)
            objects_map['fixed_wall 7'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (8, 101)
            wall_instance.wh = (8, 38)
            objects.append(wall_instance)
            objects_map['fixed_wall 8'] = wall_instance
            number_of_walls = 9
            i = 0
            while(objects_map.get(f"fixed wall {number_of_walls + i}")!= None):
                objects_map.pop(f"fixed wall {number_of_walls + i}")
                i += 1
        elif ram_state[28] == 4:
            wall_instance = Wall()
            wall_instance.xy = (144, 21)
            wall_instance.wh = (16, 38)
            objects.append(wall_instance)
            objects_map['fixed_wall 0'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (32, 21)
            wall_instance.wh = (96, 38)
            objects.append(wall_instance)
            objects_map['fixed_wall 1'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (8, 21)
            wall_instance.wh = (8, 38)
            objects.append(wall_instance)
            objects_map['fixed_wall 2'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (140, 61)
            wall_instance.wh = (20, 37)
            objects.append(wall_instance)
            objects_map['fixed_wall 3'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (8, 61)
            wall_instance.wh = (12, 37)
            objects.append(wall_instance)
            objects_map['fixed_wall 4'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (88, 101)
            wall_instance.wh = (72, 38)
            objects.append(wall_instance)
            objects_map['fixed_wall 5'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (8, 101)
            wall_instance.wh = (64, 38)
            objects.append(wall_instance)
            objects_map['fixed_wall 6'] = wall_instance
            number_of_walls = 7
            i = 0
            while(objects_map.get(f"fixed wall {number_of_walls + i}")!= None):
                objects_map.pop(f"fixed wall {number_of_walls + i}")
                i += 1
        elif ram_state[28] == 5:
            wall_instance = Wall()
            wall_instance.xy = (88, 21)
            wall_instance.wh = (72, 38)
            objects.append(wall_instance)
            objects_map['fixed_wall 0'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (8, 21)
            wall_instance.wh = (64, 38)
            objects.append(wall_instance)
            objects_map['fixed_wall 1'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (144, 61)
            wall_instance.wh = (16, 37)
            objects.append(wall_instance)
            objects_map['fixed_wall 2'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (8, 61)
            wall_instance.wh = (8, 37)
            objects.append(wall_instance)
            objects_map['fixed_wall 3'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (140, 101)
            wall_instance.wh = (20, 38)
            objects.append(wall_instance)
            objects_map['fixed_wall 4'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (28, 101)
            wall_instance.wh = (104, 38)
            objects.append(wall_instance)
            objects_map['fixed_wall 5'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (8, 101)
            wall_instance.wh = (12, 38)
            objects.append(wall_instance)
            objects_map['fixed_wall 6'] = wall_instance
            number_of_walls = 7
            i = 0
            while(objects_map.get(f"fixed wall {number_of_walls + i}")!= None):
                objects_map.pop(f"fixed wall {number_of_walls + i}")
                i += 1
        elif ram_state[28] == 6:
            wall_instance = Wall()
            wall_instance.xy = (140, 21)
            wall_instance.wh = (20, 38)
            objects.append(wall_instance)
            objects_map['fixed_wall 0'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (28, 21)
            wall_instance.wh = (104, 38)
            objects.append(wall_instance)
            objects_map['fixed_wall 1'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (8, 21)
            wall_instance.wh = (12, 38)
            objects.append(wall_instance)
            objects_map['fixed_wall 2'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (144, 61)
            wall_instance.wh = (16, 37)
            objects.append(wall_instance)
            objects_map['fixed_wall 3'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (8, 61)
            wall_instance.wh = (8, 37)
            objects.append(wall_instance)
            objects_map['fixed_wall 4'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (100, 101)
            wall_instance.wh = (60, 38)
            objects.append(wall_instance)
            objects_map['fixed_wall 5'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (8, 101)
            wall_instance.wh = (52, 38)
            objects.append(wall_instance)
            objects_map['fixed_wall 6'] = wall_instance
            number_of_walls = 7
            i = 0
            while(objects_map.get(f"fixed wall {number_of_walls + i}")!= None):
                objects_map.pop(f"fixed wall {number_of_walls + i}")
                i += 1
        elif ram_state[28] == 7:
            wall_instance = Wall()
            wall_instance.xy = (100, 21)
            wall_instance.wh = (60, 38)
            objects.append(wall_instance)
            objects_map['fixed_wall 0'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (8, 21)
            wall_instance.wh = (52, 38)
            objects.append(wall_instance)
            objects_map['fixed_wall 1'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (136, 61)
            wall_instance.wh = (24, 37)
            objects.append(wall_instance)
            objects_map['fixed_wall 2'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (72, 61)
            wall_instance.wh = (16, 37)
            objects.append(wall_instance)
            objects_map['fixed_wall 3'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (8, 61)
            wall_instance.wh = (16, 37)
            objects.append(wall_instance)
            objects_map['fixed_wall 4'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (8, 101)
            wall_instance.wh = (152, 38)
            objects.append(wall_instance)
            objects_map['fixed_wall 5'] = wall_instance
            number_of_walls = 6
            i = 0
            while(objects_map.get(f"fixed wall {number_of_walls + i}")!= None):
                objects_map.pop(f"fixed wall {number_of_walls + i}")
                i += 1

    elif ram_state[117] == 4:
        if ram_state[28] == 0:
            wall_instance = Wall()
            wall_instance.xy = (136, 21)
            wall_instance.wh = (24, 38)
            objects.append(wall_instance)
            objects_map['fixed_wall 0'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (8, 21)
            wall_instance.wh = (16, 38)
            objects.append(wall_instance)
            objects_map['fixed_wall 1'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (144, 61)
            wall_instance.wh = (16, 37)
            objects.append(wall_instance)
            objects_map['fixed_wall 2'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (8, 61)
            wall_instance.wh = (8, 37)
            objects.append(wall_instance)
            objects_map['fixed_wall 3'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (88, 101)
            wall_instance.wh = (72, 38)
            objects.append(wall_instance)
            objects_map['fixed_wall 4'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (8, 101)
            wall_instance.wh = (64, 38)
            objects.append(wall_instance)
            objects_map['fixed_wall 5'] = wall_instance
            number_of_walls = 6
            i = 0
            while(objects_map.get(f"fixed wall {number_of_walls + i}")!= None):
                objects_map.pop(f"fixed wall {number_of_walls + i}")
                i += 1
        elif ram_state[28] == 1:
            wall_instance = Wall()
            wall_instance.xy = (88, 21)
            wall_instance.wh = (72, 38)
            objects.append(wall_instance)
            objects_map['fixed_wall 0'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (8, 21)
            wall_instance.wh = (64, 38)
            objects.append(wall_instance)
            objects_map['fixed_wall 1'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (8, 101)
            wall_instance.wh = (152, 38)
            objects.append(wall_instance)
            objects_map['fixed_wall 2'] = wall_instance
            number_of_walls = 3
            i = 0
            while(objects_map.get(f"fixed wall {number_of_walls + i}")!= None):
                objects_map.pop(f"fixed wall {number_of_walls + i}")
                i += 1
        elif ram_state[28] == 2:
            wall_instance = Wall()
            wall_instance.xy = (8, 21)
            wall_instance.wh = (152, 38)
            objects.append(wall_instance)
            objects_map['fixed_wall 0'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (144, 61)
            wall_instance.wh = (16, 37)
            objects.append(wall_instance)
            objects_map['fixed_wall 1'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (8, 61)
            wall_instance.wh = (8, 37)
            objects.append(wall_instance)
            objects_map['fixed_wall 2'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (136, 101)
            wall_instance.wh = (24, 38)
            objects.append(wall_instance)
            objects_map['fixed_wall 3'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (8, 101)
            wall_instance.wh = (16, 38)
            objects.append(wall_instance)
            objects_map['fixed_wall 4'] = wall_instance
            number_of_walls = 5
            i = 0
            while(objects_map.get(f"fixed wall {number_of_walls + i}")!= None):
                objects_map.pop(f"fixed wall {number_of_walls + i}")
                i += 1
        elif ram_state[28] == 3:
            wall_instance = Wall()
            wall_instance.xy = (136, 21)
            wall_instance.wh = (24, 38)
            objects.append(wall_instance)
            objects_map['fixed_wall 0'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (8, 21)
            wall_instance.wh = (16, 38)
            objects.append(wall_instance)
            objects_map['fixed_wall 1'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (84, 101)
            wall_instance.wh = (76, 38)
            objects.append(wall_instance)
            objects_map['fixed_wall 2'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (8, 101)
            wall_instance.wh = (68, 38)
            objects.append(wall_instance)
            objects_map['fixed_wall 3'] = wall_instance
            number_of_walls = 4
            i = 0
            while(objects_map.get(f"fixed wall {number_of_walls + i}")!= None):
                objects_map.pop(f"fixed wall {number_of_walls + i}")
                i += 1
        elif ram_state[28] == 4:
            wall_instance = Wall()
            wall_instance.xy = (84, 21)
            wall_instance.wh = (76, 38)
            objects.append(wall_instance)
            objects_map['fixed_wall 0'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (8, 21)
            wall_instance.wh = (68, 38)
            objects.append(wall_instance)
            objects_map['fixed_wall 1'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (144, 61)
            wall_instance.wh = (16, 37)
            objects.append(wall_instance)
            objects_map['fixed_wall 2'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (8, 61)
            wall_instance.wh = (8, 37)
            objects.append(wall_instance)
            objects_map['fixed_wall 3'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (136, 101)
            wall_instance.wh = (24, 38)
            objects.append(wall_instance)
            objects_map['fixed_wall 4'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (32, 101)
            wall_instance.wh = (96, 38)
            objects.append(wall_instance)
            objects_map['fixed_wall 5'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (8, 101)
            wall_instance.wh = (16, 38)
            objects.append(wall_instance)
            objects_map['fixed_wall 6'] = wall_instance
            number_of_walls = 7
            i = 0
            while(objects_map.get(f"fixed wall {number_of_walls + i}")!= None):
                objects_map.pop(f"fixed wall {number_of_walls + i}")
                i += 1
        elif ram_state[28] == 5:
            wall_instance = Wall()
            wall_instance.xy = (136, 21)
            wall_instance.wh = (24, 38)
            objects.append(wall_instance)
            objects_map['fixed_wall 0'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (32, 21)
            wall_instance.wh = (96, 38)
            objects.append(wall_instance)
            objects_map['fixed_wall 1'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (8, 21)
            wall_instance.wh = (16, 38)
            objects.append(wall_instance)
            objects_map['fixed_wall 2'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (88, 101)
            wall_instance.wh = (72, 38)
            objects.append(wall_instance)
            objects_map['fixed_wall 3'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (8, 101)
            wall_instance.wh = (64, 38)
            objects.append(wall_instance)
            objects_map['fixed_wall 4'] = wall_instance
            number_of_walls = 5
            i = 0
            while(objects_map.get(f"fixed wall {number_of_walls + i}")!= None):
                objects_map.pop(f"fixed wall {number_of_walls + i}")
                i += 1
        elif ram_state[28] == 6:
            wall_instance = Wall()
            wall_instance.xy = (88, 21)
            wall_instance.wh = (72, 38)
            objects.append(wall_instance)
            objects_map['fixed_wall 0'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (8, 21)
            wall_instance.wh = (64, 38)
            objects.append(wall_instance)
            objects_map['fixed_wall 1'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (120, 101)
            wall_instance.wh = (40, 38)
            objects.append(wall_instance)
            objects_map['fixed_wall 2'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (48, 101)
            wall_instance.wh = (64, 38)
            objects.append(wall_instance)
            objects_map['fixed_wall 3'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (8, 101)
            wall_instance.wh = (32, 38)
            objects.append(wall_instance)
            objects_map['fixed_wall 4'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (144, 61)
            wall_instance.wh = (16, 37)
            objects.append(wall_instance)
            objects_map['fixed_wall 5'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (8, 61)
            wall_instance.wh = (8, 37)
            objects.append(wall_instance)
            objects_map['fixed_wall 6'] = wall_instance
            number_of_walls = 7
            i = 0
            while(objects_map.get(f"fixed wall {number_of_walls + i}")!= None):
                objects_map.pop(f"fixed wall {number_of_walls + i}")
                i += 1
        elif ram_state[28] == 7:
            wall_instance = Wall()
            wall_instance.xy = (120, 21)
            wall_instance.wh = (40, 38)
            objects.append(wall_instance)
            objects_map['fixed_wall 0'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (48, 21)
            wall_instance.wh = (64, 38)
            objects.append(wall_instance)
            objects_map['fixed_wall 1'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (8, 21)
            wall_instance.wh = (32, 38)
            objects.append(wall_instance)
            objects_map['fixed_wall 2'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (144, 61)
            wall_instance.wh = (16, 37)
            objects.append(wall_instance)
            objects_map['fixed_wall 3'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (8, 61)
            wall_instance.wh = (8, 37)
            objects.append(wall_instance)
            objects_map['fixed_wall 4'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (8, 101)
            wall_instance.wh = (152, 38)
            objects.append(wall_instance)
            objects_map['fixed_wall 5'] = wall_instance
            number_of_walls = 6
            i = 0
            while(objects_map.get(f"fixed wall {number_of_walls + i}")!= None):
                objects_map.pop(f"fixed wall {number_of_walls + i}")
                i += 1

    elif ram_state[117] == 5:
        if ram_state[28] == 0:
            wall_instance = Wall()
            wall_instance.xy = (136, 21)
            wall_instance.wh = (24, 38)
            objects.append(wall_instance)
            objects_map['fixed_wall 0'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (8, 21)
            wall_instance.wh = (16, 38)
            objects.append(wall_instance)
            objects_map['fixed_wall 1'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (88, 101)
            wall_instance.wh = (72, 38)
            objects.append(wall_instance)
            objects_map['fixed_wall 2'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (8, 101)
            wall_instance.wh = (64, 38)
            objects.append(wall_instance)
            objects_map['fixed_wall 3'] = wall_instance
            number_of_walls = 4
            i = 0
            while(objects_map.get(f"fixed wall {number_of_walls + i}")!= None):
                objects_map.pop(f"fixed wall {number_of_walls + i}")
                i += 1
        elif ram_state[28] == 1:
            wall_instance = Wall()
            wall_instance.xy = (88, 21)
            wall_instance.wh = (72, 38)
            objects.append(wall_instance)
            objects_map['fixed_wall 0'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (8, 21)
            wall_instance.wh = (64, 38)
            objects.append(wall_instance)
            objects_map['fixed_wall 1'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (144, 61)
            wall_instance.wh = (16, 37)
            objects.append(wall_instance)
            objects_map['fixed_wall 2'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (8, 61)
            wall_instance.wh = (8, 37)
            objects.append(wall_instance)
            objects_map['fixed_wall 3'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (140, 101)
            wall_instance.wh = (20, 38)
            objects.append(wall_instance)
            objects_map['fixed_wall 4'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (56, 101)
            wall_instance.wh = (48, 38)
            objects.append(wall_instance)
            objects_map['fixed_wall 5'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (8, 101)
            wall_instance.wh = (12, 38)
            objects.append(wall_instance)
            objects_map['fixed_wall 6'] = wall_instance
            number_of_walls = 7
            i = 0
            while(objects_map.get(f"fixed wall {number_of_walls + i}")!= None):
                objects_map.pop(f"fixed wall {number_of_walls + i}")
                i += 1
        elif ram_state[28] == 2:
            wall_instance = Wall()
            wall_instance.xy = (140, 21)
            wall_instance.wh = (20, 38)
            objects.append(wall_instance)
            objects_map['fixed_wall 0'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (56, 21)
            wall_instance.wh = (48, 38)
            objects.append(wall_instance)
            objects_map['fixed_wall 1'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (8, 21)
            wall_instance.wh = (12, 38)
            objects.append(wall_instance)
            objects_map['fixed_wall 2'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (88, 101)
            wall_instance.wh = (72, 38)
            objects.append(wall_instance)
            objects_map['fixed_wall 3'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (8, 101)
            wall_instance.wh = (64, 38)
            objects.append(wall_instance)
            objects_map['fixed_wall 4'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (144, 61)
            wall_instance.wh = (16, 37)
            objects.append(wall_instance)
            objects_map['fixed_wall 5'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (8, 61)
            wall_instance.wh = (8, 37)
            objects.append(wall_instance)
            objects_map['fixed_wall 6'] = wall_instance
            number_of_walls = 7
            i = 0
            while(objects_map.get(f"fixed wall {number_of_walls + i}")!= None):
                objects_map.pop(f"fixed wall {number_of_walls + i}")
                i += 1
        elif ram_state[28] == 3:
            wall_instance = Wall()
            wall_instance.xy = (88, 21)
            wall_instance.wh = (72, 38)
            objects.append(wall_instance)
            objects_map['fixed_wall 0'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (8, 21)
            wall_instance.wh = (64, 38)
            objects.append(wall_instance)
            objects_map['fixed_wall 1'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (136, 61)
            wall_instance.wh = (24, 37)
            objects.append(wall_instance)
            objects_map['fixed_wall 2'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (8, 61)
            wall_instance.wh = (16, 37)
            objects.append(wall_instance)
            objects_map['fixed_wall 3'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (132, 101)
            wall_instance.wh = (28, 38)
            objects.append(wall_instance)
            objects_map['fixed_wall 4'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (104, 101)
            wall_instance.wh = (20, 38)
            objects.append(wall_instance)
            objects_map['fixed_wall 5'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (64, 101)
            wall_instance.wh = (32, 38)
            objects.append(wall_instance)
            objects_map['fixed_wall 6'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (36, 101)
            wall_instance.wh = (20, 38)
            objects.append(wall_instance)
            objects_map['fixed_wall 7'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (8, 101)
            wall_instance.wh = (20, 38)
            objects.append(wall_instance)
            objects_map['fixed_wall 8'] = wall_instance
            number_of_walls = 9
            i = 0
            while(objects_map.get(f"fixed wall {number_of_walls + i}")!= None):
                objects_map.pop(f"fixed wall {number_of_walls + i}")
                i += 1
        elif ram_state[28] == 4:
            wall_instance = Wall()
            wall_instance.xy = (132, 21)
            wall_instance.wh = (28, 38)
            objects.append(wall_instance)
            objects_map['fixed_wall 0'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (104, 21)
            wall_instance.wh = (20, 38)
            objects.append(wall_instance)
            objects_map['fixed_wall 1'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (64, 21)
            wall_instance.wh = (32, 38)
            objects.append(wall_instance)
            objects_map['fixed_wall 2'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (36, 21)
            wall_instance.wh = (20, 38)
            objects.append(wall_instance)
            objects_map['fixed_wall 3'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (8, 21)
            wall_instance.wh = (20, 38)
            objects.append(wall_instance)
            objects_map['fixed_wall 4'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (108, 101)
            wall_instance.wh = (52, 38)
            objects.append(wall_instance)
            objects_map['fixed_wall 5'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (60, 101)
            wall_instance.wh = (40, 38)
            objects.append(wall_instance)
            objects_map['fixed_wall 6'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (8, 101)
            wall_instance.wh = (44, 38)
            objects.append(wall_instance)
            objects_map['fixed_wall 7'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (112, 61)
            wall_instance.wh = (48, 37)
            objects.append(wall_instance)
            objects_map['fixed_wall 8'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (8, 61)
            wall_instance.wh = (40, 37)
            objects.append(wall_instance)
            objects_map['fixed_wall 9'] = wall_instance
            number_of_walls = 10
            i = 0
            while(objects_map.get(f"fixed wall {number_of_walls + i}")!= None):
                objects_map.pop(f"fixed wall {number_of_walls + i}")
                i += 1
        elif ram_state[28] == 5:
            wall_instance = Wall()
            wall_instance.xy = (108, 21)
            wall_instance.wh = (52, 38)
            objects.append(wall_instance)
            objects_map['fixed_wall 0'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (60, 21)
            wall_instance.wh = (40, 38)
            objects.append(wall_instance)
            objects_map['fixed_wall 1'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (8, 21)
            wall_instance.wh = (44, 38)
            objects.append(wall_instance)
            objects_map['fixed_wall 2'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (132, 61)
            wall_instance.wh = (28, 37)
            objects.append(wall_instance)
            objects_map['fixed_wall 3'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (52, 61)
            wall_instance.wh = (44, 37)
            objects.append(wall_instance)
            objects_map['fixed_wall 4'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (8, 61)
            wall_instance.wh = (8, 37)
            objects.append(wall_instance)
            objects_map['fixed_wall 5'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (120, 101)
            wall_instance.wh = (40, 38)
            objects.append(wall_instance)
            objects_map['fixed_wall 6'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (8, 101)
            wall_instance.wh = (32, 38)
            objects.append(wall_instance)
            objects_map['fixed_wall 7'] = wall_instance
            number_of_walls = 8
            i = 0
            while(objects_map.get(f"fixed wall {number_of_walls + i}")!= None):
                objects_map.pop(f"fixed wall {number_of_walls + i}")
                i += 1
        elif ram_state[28] == 6:
            wall_instance = Wall()
            wall_instance.xy = (120, 21)
            wall_instance.wh = (40, 38)
            objects.append(wall_instance)
            objects_map['fixed_wall 0'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (8, 21)
            wall_instance.wh = (32, 38)
            objects.append(wall_instance)
            objects_map['fixed_wall 1'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (136, 101)
            wall_instance.wh = (24, 38)
            objects.append(wall_instance)
            objects_map['fixed_wall 2'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (32, 101)
            wall_instance.wh = (96, 38)
            objects.append(wall_instance)
            objects_map['fixed_wall 3'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (8, 101)
            wall_instance.wh = (16, 38)
            objects.append(wall_instance)
            objects_map['fixed_wall 4'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (144, 61)
            wall_instance.wh = (16, 37)
            objects.append(wall_instance)
            objects_map['fixed_wall 5'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (8, 61)
            wall_instance.wh = (8, 37)
            objects.append(wall_instance)
            objects_map['fixed_wall 6'] = wall_instance
            number_of_walls = 7
            i = 0
            while(objects_map.get(f"fixed wall {number_of_walls + i}")!= None):
                objects_map.pop(f"fixed wall {number_of_walls + i}")
                i += 1
        elif ram_state[28] == 7:
            wall_instance = Wall()
            wall_instance.xy = (136, 21)
            wall_instance.wh = (24, 38)
            objects.append(wall_instance)
            objects_map['fixed_wall 0'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (32, 21)
            wall_instance.wh = (96, 38)
            objects.append(wall_instance)
            objects_map['fixed_wall 1'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (8, 21)
            wall_instance.wh = (16, 38)
            objects.append(wall_instance)
            objects_map['fixed_wall 2'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (144, 61)
            wall_instance.wh = (16, 37)
            objects.append(wall_instance)
            objects_map['fixed_wall 3'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (8, 61)
            wall_instance.wh = (8, 37)
            objects.append(wall_instance)
            objects_map['fixed_wall 4'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (112, 101)
            wall_instance.wh = (48, 38)
            objects.append(wall_instance)
            objects_map['fixed_wall 5'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (56, 101)
            wall_instance.wh = (48, 38)
            objects.append(wall_instance)
            objects_map['fixed_wall 6'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (8, 101)
            wall_instance.wh = (40, 38)
            objects.append(wall_instance)
            objects_map['fixed_wall 7'] = wall_instance
            number_of_walls = 8
            i = 0
            while(objects_map.get(f"fixed wall {number_of_walls + i}")!= None):
                objects_map.pop(f"fixed wall {number_of_walls + i}")
                i += 1
        elif ram_state[28] == 8:
            wall_instance = Wall()
            wall_instance.xy = (112, 21)
            wall_instance.wh = (48, 38)
            objects.append(wall_instance)
            objects_map['fixed_wall 0'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (56, 21)
            wall_instance.wh = (48, 38)
            objects.append(wall_instance)
            objects_map['fixed_wall 1'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (8, 21)
            wall_instance.wh = (40, 38)
            objects.append(wall_instance)
            objects_map['fixed_wall 2'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (88, 101)
            wall_instance.wh = (72, 38)
            objects.append(wall_instance)
            objects_map['fixed_wall 3'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (8, 101)
            wall_instance.wh = (64, 38)
            objects.append(wall_instance)
            objects_map['fixed_wall 4'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (136, 61)
            wall_instance.wh = (24, 37)
            objects.append(wall_instance)
            objects_map['fixed_wall 5'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (8, 61)
            wall_instance.wh = (16, 37)
            objects.append(wall_instance)
            objects_map['fixed_wall 6'] = wall_instance
            number_of_walls = 7
            i = 0
            while(objects_map.get(f"fixed wall {number_of_walls + i}")!= None):
                objects_map.pop(f"fixed wall {number_of_walls + i}")
                i += 1
        elif ram_state[28] == 9:
            wall_instance = Wall()
            wall_instance.xy = (88, 21)
            wall_instance.wh = (72, 38)
            objects.append(wall_instance)
            objects_map['fixed_wall 0'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (8, 21)
            wall_instance.wh = (64, 38)
            objects.append(wall_instance)
            objects_map['fixed_wall 1'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (136, 61)
            wall_instance.wh = (24, 37)
            objects.append(wall_instance)
            objects_map['fixed_wall 2'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (8, 61)
            wall_instance.wh = (16, 37)
            objects.append(wall_instance)
            objects_map['fixed_wall 3'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (8, 101)
            wall_instance.wh = (152, 38)
            objects.append(wall_instance)
            objects_map['fixed_wall 4'] = wall_instance
            number_of_walls = 5
            i = 0
            while(objects_map.get(f"fixed wall {number_of_walls + i}")!= None):
                objects_map.pop(f"fixed wall {number_of_walls + i}")
                i += 1

    elif ram_state[117] == 6:
        if ram_state[28] == 0:
            wall_instance = Wall()
            wall_instance.xy = (136, 21)
            wall_instance.wh = (24, 38)
            objects.append(wall_instance)
            objects_map['fixed_wall 0'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (8, 21)
            wall_instance.wh = (16, 38)
            objects.append(wall_instance)
            objects_map['fixed_wall 1'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (88, 101)
            wall_instance.wh = (72, 38)
            objects.append(wall_instance)
            objects_map['fixed_wall 2'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (8, 101)
            wall_instance.wh = (64, 38)
            objects.append(wall_instance)
            objects_map['fixed_wall 3'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (140, 61)
            wall_instance.wh = (20, 37)
            objects.append(wall_instance)
            objects_map['fixed_wall 4'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (8, 61)
            wall_instance.wh = (12, 37)
            objects.append(wall_instance)
            objects_map['fixed_wall 5'] = wall_instance
            number_of_walls = 6
            i = 0
            while(objects_map.get(f"fixed wall {number_of_walls + i}")!= None):
                objects_map.pop(f"fixed wall {number_of_walls + i}")
                i += 1
        elif ram_state[28] == 1:
            wall_instance = Wall()
            wall_instance.xy = (88, 21)
            wall_instance.wh = (72, 38)
            objects.append(wall_instance)
            objects_map['fixed_wall 0'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (8, 21)
            wall_instance.wh = (64, 38)
            objects.append(wall_instance)
            objects_map['fixed_wall 1'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (140, 61)
            wall_instance.wh = (20, 37)
            objects.append(wall_instance)
            objects_map['fixed_wall 2'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (8, 61)
            wall_instance.wh = (12, 37)
            objects.append(wall_instance)
            objects_map['fixed_wall 3'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (136, 101)
            wall_instance.wh = (24, 38)
            objects.append(wall_instance)
            objects_map['fixed_wall 4'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (32, 101)
            wall_instance.wh = (96, 38)
            objects.append(wall_instance)
            objects_map['fixed_wall 5'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (8, 101)
            wall_instance.wh = (16, 38)
            objects.append(wall_instance)
            objects_map['fixed_wall 6'] = wall_instance
            number_of_walls = 7
            i = 0
            while(objects_map.get(f"fixed wall {number_of_walls + i}")!= None):
                objects_map.pop(f"fixed wall {number_of_walls + i}")
                i += 1
        elif ram_state[28] == 2:
            wall_instance = Wall()
            wall_instance.xy = (136, 21)
            wall_instance.wh = (24, 38)
            objects.append(wall_instance)
            objects_map['fixed_wall 0'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (32, 21)
            wall_instance.wh = (96, 38)
            objects.append(wall_instance)
            objects_map['fixed_wall 1'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (8, 21)
            wall_instance.wh = (16, 38)
            objects.append(wall_instance)
            objects_map['fixed_wall 2'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (84, 101)
            wall_instance.wh = (76, 38)
            objects.append(wall_instance)
            objects_map['fixed_wall 3'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (8, 101)
            wall_instance.wh = (68, 38)
            objects.append(wall_instance)
            objects_map['fixed_wall 4'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (144, 61)
            wall_instance.wh = (16, 37)
            objects.append(wall_instance)
            objects_map['fixed_wall 5'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (8, 61)
            wall_instance.wh = (8, 37)
            objects.append(wall_instance)
            objects_map['fixed_wall 6'] = wall_instance
            number_of_walls = 7
            i = 0
            while(objects_map.get(f"fixed wall {number_of_walls + i}")!= None):
                objects_map.pop(f"fixed wall {number_of_walls + i}")
                i += 1
        elif ram_state[28] == 3:
            wall_instance = Wall()
            wall_instance.xy = (84, 21)
            wall_instance.wh = (76, 38)
            objects.append(wall_instance)
            objects_map['fixed_wall 0'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (8, 21)
            wall_instance.wh = (68, 38)
            objects.append(wall_instance)
            objects_map['fixed_wall 1'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (112, 61)
            wall_instance.wh = (48, 37)
            objects.append(wall_instance)
            objects_map['fixed_wall 2'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (8, 61)
            wall_instance.wh = (40, 37)
            objects.append(wall_instance)
            objects_map['fixed_wall 3'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (108, 101)
            wall_instance.wh = (52, 38)
            objects.append(wall_instance)
            objects_map['fixed_wall 4'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (60, 101)
            wall_instance.wh = (40, 38)
            objects.append(wall_instance)
            objects_map['fixed_wall 5'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (8, 101)
            wall_instance.wh = (44, 38)
            objects.append(wall_instance)
            objects_map['fixed_wall 6'] = wall_instance
            number_of_walls = 7
            i = 0
            while(objects_map.get(f"fixed wall {number_of_walls + i}")!= None):
                objects_map.pop(f"fixed wall {number_of_walls + i}")
                i += 1
        elif ram_state[28] == 4:
            wall_instance = Wall()
            wall_instance.xy = (108, 21)
            wall_instance.wh = (52, 38)
            objects.append(wall_instance)
            objects_map['fixed_wall 0'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (60, 21)
            wall_instance.wh = (40, 38)
            objects.append(wall_instance)
            objects_map['fixed_wall 1'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (8, 21)
            wall_instance.wh = (44, 38)
            objects.append(wall_instance)
            objects_map['fixed_wall 2'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (136, 101)
            wall_instance.wh = (24, 38)
            objects.append(wall_instance)
            objects_map['fixed_wall 3'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (40, 101)
            wall_instance.wh = (80, 38)
            objects.append(wall_instance)
            objects_map['fixed_wall 4'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (8, 101)
            wall_instance.wh = (16, 38)
            objects.append(wall_instance)
            objects_map['fixed_wall 5'] = wall_instance
            number_of_walls = 6
            i = 0
            while(objects_map.get(f"fixed wall {number_of_walls + i}")!= None):
                objects_map.pop(f"fixed wall {number_of_walls + i}")
                i += 1
        elif ram_state[28] == 5:
            wall_instance = Wall()
            wall_instance.xy = (136, 21)
            wall_instance.wh = (24, 38)
            objects.append(wall_instance)
            objects_map['fixed_wall 0'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (40, 21)
            wall_instance.wh = (80, 38)
            objects.append(wall_instance)
            objects_map['fixed_wall 1'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (8, 21)
            wall_instance.wh = (16, 38)
            objects.append(wall_instance)
            objects_map['fixed_wall 2'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (128, 61)
            wall_instance.wh = (32, 37)
            objects.append(wall_instance)
            objects_map['fixed_wall 3'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (8, 61)
            wall_instance.wh = (24, 37)
            objects.append(wall_instance)
            objects_map['fixed_wall 4'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (144, 101)
            wall_instance.wh = (16, 38)
            objects.append(wall_instance)
            objects_map['fixed_wall 5'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (48, 101)
            wall_instance.wh = (64, 38)
            objects.append(wall_instance)
            objects_map['fixed_wall 6'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (8, 101)
            wall_instance.wh = (8, 38)
            objects.append(wall_instance)
            objects_map['fixed_wall 7'] = wall_instance
            number_of_walls = 8
            i = 0
            while(objects_map.get(f"fixed wall {number_of_walls + i}")!= None):
                objects_map.pop(f"fixed wall {number_of_walls + i}")
                i += 1
        elif ram_state[28] == 6:
            wall_instance = Wall()
            wall_instance.xy = (144, 21)
            wall_instance.wh = (16, 38)
            objects.append(wall_instance)
            objects_map['fixed_wall 0'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (48, 21)
            wall_instance.wh = (64, 38)
            objects.append(wall_instance)
            objects_map['fixed_wall 1'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (8, 21)
            wall_instance.wh = (8, 38)
            objects.append(wall_instance)
            objects_map['fixed_wall 2'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (144, 101)
            wall_instance.wh = (16, 38)
            objects.append(wall_instance)
            objects_map['fixed_wall 3'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (36, 101)
            wall_instance.wh = (88, 38)
            objects.append(wall_instance)
            objects_map['fixed_wall 4'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (8, 101)
            wall_instance.wh = (8, 38)
            objects.append(wall_instance)
            objects_map['fixed_wall 5'] = wall_instance
            number_of_walls = 6
            i = 0
            while(objects_map.get(f"fixed wall {number_of_walls + i}")!= None):
                objects_map.pop(f"fixed wall {number_of_walls + i}")
                i += 1
        elif ram_state[28] == 7:
            wall_instance = Wall()
            wall_instance.xy = (144, 21)
            wall_instance.wh = (16, 38)
            objects.append(wall_instance)
            objects_map['fixed_wall 0'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (36, 21)
            wall_instance.wh = (88, 38)
            objects.append(wall_instance)
            objects_map['fixed_wall 1'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (8, 21)
            wall_instance.wh = (8, 38)
            objects.append(wall_instance)
            objects_map['fixed_wall 2'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (132, 61)
            wall_instance.wh = (28, 37)
            objects.append(wall_instance)
            objects_map['fixed_wall 3'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (8, 61)
            wall_instance.wh = (20, 37)
            objects.append(wall_instance)
            objects_map['fixed_wall 4'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (88, 101)
            wall_instance.wh = (72, 38)
            objects.append(wall_instance)
            objects_map['fixed_wall 5'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (8, 101)
            wall_instance.wh = (64, 38)
            objects.append(wall_instance)
            objects_map['fixed_wall 6'] = wall_instance
            number_of_walls = 7
            i = 0
            while(objects_map.get(f"fixed wall {number_of_walls + i}")!= None):
                objects_map.pop(f"fixed wall {number_of_walls + i}")
                i += 1
        elif ram_state[28] == 8:
            wall_instance = Wall()
            wall_instance.xy = (88, 21)
            wall_instance.wh = (72, 38)
            objects.append(wall_instance)
            objects_map['fixed_wall 0'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (8, 21)
            wall_instance.wh = (64, 38)
            objects.append(wall_instance)
            objects_map['fixed_wall 1'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (128, 101)
            wall_instance.wh = (32, 38)
            objects.append(wall_instance)
            objects_map['fixed_wall 2'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (48, 101)
            wall_instance.wh = (64, 38)
            objects.append(wall_instance)
            objects_map['fixed_wall 3'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (8, 101)
            wall_instance.wh = (24, 38)
            objects.append(wall_instance)
            objects_map['fixed_wall 4'] = wall_instance
            number_of_walls = 5
            i = 0
            while(objects_map.get(f"fixed wall {number_of_walls + i}")!= None):
                objects_map.pop(f"fixed wall {number_of_walls + i}")
                i += 1
        elif ram_state[28] == 9:
            wall_instance = Wall()
            wall_instance.xy = (128, 21)
            wall_instance.wh = (32, 38)
            objects.append(wall_instance)
            objects_map['fixed_wall 0'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (48, 21)
            wall_instance.wh = (64, 38)
            objects.append(wall_instance)
            objects_map['fixed_wall 1'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (8, 21)
            wall_instance.wh = (24, 38)
            objects.append(wall_instance)
            objects_map['fixed_wall 2'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (136, 61)
            wall_instance.wh = (24, 37)
            objects.append(wall_instance)
            objects_map['fixed_wall 3'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (8, 61)
            wall_instance.wh = (16, 37)
            objects.append(wall_instance)
            objects_map['fixed_wall 4'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (96, 101)
            wall_instance.wh = (64, 38)
            objects.append(wall_instance)
            objects_map['fixed_wall 5'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (72, 101)
            wall_instance.wh = (16, 38)
            objects.append(wall_instance)
            objects_map['fixed_wall 6'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (8, 101)
            wall_instance.wh = (56, 38)
            objects.append(wall_instance)
            objects_map['fixed_wall 7'] = wall_instance
            number_of_walls = 8
            i = 0
            while(objects_map.get(f"fixed wall {number_of_walls + i}")!= None):
                objects_map.pop(f"fixed wall {number_of_walls + i}")
                i += 1
        elif ram_state[28] == 10:
            wall_instance = Wall()
            wall_instance.xy = (96, 21)
            wall_instance.wh = (64, 38)
            objects.append(wall_instance)
            objects_map['fixed_wall 0'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (72, 21)
            wall_instance.wh = (16, 38)
            objects.append(wall_instance)
            objects_map['fixed_wall 1'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (8, 21)
            wall_instance.wh = (56, 38)
            objects.append(wall_instance)
            objects_map['fixed_wall 2'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (128, 101)
            wall_instance.wh = (32, 38)
            objects.append(wall_instance)
            objects_map['fixed_wall 3'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (8, 101)
            wall_instance.wh = (24, 38)
            objects.append(wall_instance)
            objects_map['fixed_wall 4'] = wall_instance
            number_of_walls = 5
            i = 0
            while(objects_map.get(f"fixed wall {number_of_walls + i}")!= None):
                objects_map.pop(f"fixed wall {number_of_walls + i}")
                i += 1
        elif ram_state[28] == 11:
            wall_instance = Wall()
            wall_instance.xy = (8, 21)
            wall_instance.wh = (152, 38)
            objects.append(wall_instance)
            objects_map['fixed_wall 0'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (8, 101)
            wall_instance.wh = (152, 38)
            objects.append(wall_instance)
            objects_map['fixed_wall 1'] = wall_instance
            number_of_walls = 2
            i = 0
            while(objects_map.get(f"fixed wall {number_of_walls + i}")!= None):
                objects_map.pop(f"fixed wall {number_of_walls + i}")
                i += 1

    elif ram_state[117] == 7:
        if ram_state[28] == 0:
            wall_instance = Wall()
            wall_instance.xy = (136, 21)
            wall_instance.wh = (24, 38)
            objects.append(wall_instance)
            objects_map['fixed_wall 0'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (8, 21)
            wall_instance.wh = (16, 38)
            objects.append(wall_instance)
            objects_map['fixed_wall 1'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (88, 101)
            wall_instance.wh = (72, 38)
            objects.append(wall_instance)
            objects_map['fixed_wall 2'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (8, 101)
            wall_instance.wh = (64, 38)
            objects.append(wall_instance)
            objects_map['fixed_wall 3'] = wall_instance
            number_of_walls = 4
            i = 0
            while(objects_map.get(f"fixed wall {number_of_walls + i}")!= None):
                objects_map.pop(f"fixed wall {number_of_walls + i}")
                i += 1
        elif ram_state[28] == 1:
            wall_instance = Wall()
            wall_instance.xy = (88, 21)
            wall_instance.wh = (72, 38)
            objects.append(wall_instance)
            objects_map['fixed_wall 0'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (8, 21)
            wall_instance.wh = (64, 38)
            objects.append(wall_instance)
            objects_map['fixed_wall 1'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (112, 101)
            wall_instance.wh = (48, 38)
            objects.append(wall_instance)
            objects_map['fixed_wall 2'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (8, 101)
            wall_instance.wh = (40, 38)
            objects.append(wall_instance)
            objects_map['fixed_wall 3'] = wall_instance
            number_of_walls = 4
            i = 0
            while(objects_map.get(f"fixed wall {number_of_walls + i}")!= None):
                objects_map.pop(f"fixed wall {number_of_walls + i}")
                i += 1
        elif ram_state[28] == 2:
            wall_instance = Wall()
            wall_instance.xy = (112, 21)
            wall_instance.wh = (48, 38)
            objects.append(wall_instance)
            objects_map['fixed_wall 0'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (8, 21)
            wall_instance.wh = (40, 38)
            objects.append(wall_instance)
            objects_map['fixed_wall 1'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (88, 101)
            wall_instance.wh = (72, 38)
            objects.append(wall_instance)
            objects_map['fixed_wall 2'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (8, 101)
            wall_instance.wh = (64, 38)
            objects.append(wall_instance)
            objects_map['fixed_wall 3'] = wall_instance
            number_of_walls = 4
            i = 0
            while(objects_map.get(f"fixed wall {number_of_walls + i}")!= None):
                objects_map.pop(f"fixed wall {number_of_walls + i}")
                i += 1
        elif ram_state[28] == 3:
            wall_instance = Wall()
            wall_instance.xy = (88, 21)
            wall_instance.wh = (72, 38)
            objects.append(wall_instance)
            objects_map['fixed_wall 0'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (8, 21)
            wall_instance.wh = (64, 38)
            objects.append(wall_instance)
            objects_map['fixed_wall 1'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (112, 101)
            wall_instance.wh = (48, 38)
            objects.append(wall_instance)
            objects_map['fixed_wall 2'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (56, 101)
            wall_instance.wh = (48, 38)
            objects.append(wall_instance)
            objects_map['fixed_wall 3'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (8, 101)
            wall_instance.wh = (40, 38)
            objects.append(wall_instance)
            objects_map['fixed_wall 4'] = wall_instance
            number_of_walls = 5
            i = 0
            while(objects_map.get(f"fixed wall {number_of_walls + i}")!= None):
                objects_map.pop(f"fixed wall {number_of_walls + i}")
                i += 1
        elif ram_state[28] == 4:
            wall_instance = Wall()
            wall_instance.xy = (112, 21)
            wall_instance.wh = (48, 38)
            objects.append(wall_instance)
            objects_map['fixed_wall 0'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (56, 21)
            wall_instance.wh = (48, 38)
            objects.append(wall_instance)
            objects_map['fixed_wall 1'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (8, 21)
            wall_instance.wh = (40, 38)
            objects.append(wall_instance)
            objects_map['fixed_wall 2'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (128, 101)
            wall_instance.wh = (32, 38)
            objects.append(wall_instance)
            objects_map['fixed_wall 3'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (52, 101)
            wall_instance.wh = (56, 38)
            objects.append(wall_instance)
            objects_map['fixed_wall 4'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (8, 101)
            wall_instance.wh = (24, 38)
            objects.append(wall_instance)
            objects_map['fixed_wall 5'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (124, 61)
            wall_instance.wh = (36, 37)
            objects.append(wall_instance)
            objects_map['fixed_wall 6'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (60, 61)
            wall_instance.wh = (40, 37)
            objects.append(wall_instance)
            objects_map['fixed_wall 7'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (8, 61)
            wall_instance.wh = (28, 37)
            objects.append(wall_instance)
            objects_map['fixed_wall 8'] = wall_instance
            number_of_walls = 9
            i = 0
            while(objects_map.get(f"fixed wall {number_of_walls + i}")!= None):
                objects_map.pop(f"fixed wall {number_of_walls + i}")
                i += 1
        elif ram_state[28] == 5:
            wall_instance = Wall()
            wall_instance.xy = (128, 21)
            wall_instance.wh = (32, 38)
            objects.append(wall_instance)
            objects_map['fixed_wall 0'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (52, 21)
            wall_instance.wh = (56, 38)
            objects.append(wall_instance)
            objects_map['fixed_wall 1'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (8, 21)
            wall_instance.wh = (24, 38)
            objects.append(wall_instance)
            objects_map['fixed_wall 2'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (88, 101)
            wall_instance.wh = (72, 38)
            objects.append(wall_instance)
            objects_map['fixed_wall 3'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (8, 101)
            wall_instance.wh = (64, 38)
            objects.append(wall_instance)
            objects_map['fixed_wall 4'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (124, 61)
            wall_instance.wh = (36, 37)
            objects.append(wall_instance)
            objects_map['fixed_wall 5'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (8, 61)
            wall_instance.wh = (28, 37)
            objects.append(wall_instance)
            objects_map['fixed_wall 6'] = wall_instance
            number_of_walls = 7
            i = 0
            while(objects_map.get(f"fixed wall {number_of_walls + i}")!= None):
                objects_map.pop(f"fixed wall {number_of_walls + i}")
                i += 1
        elif ram_state[28] == 6:
            wall_instance = Wall()
            wall_instance.xy = (88, 21)
            wall_instance.wh = (72, 38)
            objects.append(wall_instance)
            objects_map['fixed_wall 0'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (8, 21)
            wall_instance.wh = (64, 38)
            objects.append(wall_instance)
            objects_map['fixed_wall 1'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (136, 101)
            wall_instance.wh = (24, 38)
            objects.append(wall_instance)
            objects_map['fixed_wall 2'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (32, 101)
            wall_instance.wh = (96, 38)
            objects.append(wall_instance)
            objects_map['fixed_wall 3'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (8, 101)
            wall_instance.wh = (16, 38)
            objects.append(wall_instance)
            objects_map['fixed_wall 4'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (144, 61)
            wall_instance.wh = (16, 37)
            objects.append(wall_instance)
            objects_map['fixed_wall 5'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (8, 61)
            wall_instance.wh = (8, 37)
            objects.append(wall_instance)
            objects_map['fixed_wall 6'] = wall_instance
            number_of_walls = 7
            i = 0
            while(objects_map.get(f"fixed wall {number_of_walls + i}")!= None):
                objects_map.pop(f"fixed wall {number_of_walls + i}")
                i += 1
        elif ram_state[28] == 7:
            wall_instance = Wall()
            wall_instance.xy = (136, 21)
            wall_instance.wh = (24, 38)
            objects.append(wall_instance)
            objects_map['fixed_wall 0'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (32, 21)
            wall_instance.wh = (96, 38)
            objects.append(wall_instance)
            objects_map['fixed_wall 1'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (8, 21)
            wall_instance.wh = (16, 38)
            objects.append(wall_instance)
            objects_map['fixed_wall 2'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (112, 101)
            wall_instance.wh = (48, 38)
            objects.append(wall_instance)
            objects_map['fixed_wall 3'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (56, 101)
            wall_instance.wh = (48, 38)
            objects.append(wall_instance)
            objects_map['fixed_wall 4'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (8, 101)
            wall_instance.wh = (40, 38)
            objects.append(wall_instance)
            objects_map['fixed_wall 5'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (144, 61)
            wall_instance.wh = (16, 37)
            objects.append(wall_instance)
            objects_map['fixed_wall 6'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (64, 61)
            wall_instance.wh = (32, 37)
            objects.append(wall_instance)
            objects_map['fixed_wall 7'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (8, 61)
            wall_instance.wh = (8, 37)
            objects.append(wall_instance)
            objects_map['fixed_wall 8'] = wall_instance
            number_of_walls = 9
            i = 0
            while(objects_map.get(f"fixed wall {number_of_walls + i}")!= None):
                objects_map.pop(f"fixed wall {number_of_walls + i}")
                i += 1
        elif ram_state[28] == 8:
            wall_instance = Wall()
            wall_instance.xy = (112, 21)
            wall_instance.wh = (48, 38)
            objects.append(wall_instance)
            objects_map['fixed_wall 0'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (56, 21)
            wall_instance.wh = (48, 38)
            objects.append(wall_instance)
            objects_map['fixed_wall 1'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (8, 21)
            wall_instance.wh = (40, 38)
            objects.append(wall_instance)
            objects_map['fixed_wall 2'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (144, 101)
            wall_instance.wh = (16, 38)
            objects.append(wall_instance)
            objects_map['fixed_wall 3'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (56, 101)
            wall_instance.wh = (48, 38)
            objects.append(wall_instance)
            objects_map['fixed_wall 4'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (8, 101)
            wall_instance.wh = (8, 38)
            objects.append(wall_instance)
            objects_map['fixed_wall 5'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (132, 61)
            wall_instance.wh = (28, 37)
            objects.append(wall_instance)
            objects_map['fixed_wall 6'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (72, 61)
            wall_instance.wh = (16, 37)
            objects.append(wall_instance)
            objects_map['fixed_wall 7'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (8, 61)
            wall_instance.wh = (20, 37)
            objects.append(wall_instance)
            objects_map['fixed_wall 8'] = wall_instance
            number_of_walls = 9
            i = 0
            while(objects_map.get(f"fixed wall {number_of_walls + i}")!= None):
                objects_map.pop(f"fixed wall {number_of_walls + i}")
                i += 1
        elif ram_state[28] == 9:
            wall_instance = Wall()
            wall_instance.xy = (144, 21)
            wall_instance.wh = (16, 38)
            objects.append(wall_instance)
            objects_map['fixed_wall 0'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (56, 21)
            wall_instance.wh = (48, 38)
            objects.append(wall_instance)
            objects_map['fixed_wall 1'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (8, 21)
            wall_instance.wh = (8, 38)
            objects.append(wall_instance)
            objects_map['fixed_wall 2'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (136, 101)
            wall_instance.wh = (24, 38)
            objects.append(wall_instance)
            objects_map['fixed_wall 3'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (64, 101)
            wall_instance.wh = (32, 38)
            objects.append(wall_instance)
            objects_map['fixed_wall 4'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (8, 101)
            wall_instance.wh = (16, 38)
            objects.append(wall_instance)
            objects_map['fixed_wall 5'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (128, 61)
            wall_instance.wh = (32, 37)
            objects.append(wall_instance)
            objects_map['fixed_wall 6'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (48, 61)
            wall_instance.wh = (64, 37)
            objects.append(wall_instance)
            objects_map['fixed_wall 7'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (8, 61)
            wall_instance.wh = (24, 37)
            objects.append(wall_instance)
            objects_map['fixed_wall 8'] = wall_instance
            number_of_walls = 9
            i = 0
            while(objects_map.get(f"fixed wall {number_of_walls + i}")!= None):
                objects_map.pop(f"fixed wall {number_of_walls + i}")
                i += 1
        elif ram_state[28] == 10:
            wall_instance = Wall()
            wall_instance.xy = (136, 21)
            wall_instance.wh = (24, 38)
            objects.append(wall_instance)
            objects_map['fixed_wall 0'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (64, 21)
            wall_instance.wh = (32, 38)
            objects.append(wall_instance)
            objects_map['fixed_wall 1'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (8, 21)
            wall_instance.wh = (16, 38)
            objects.append(wall_instance)
            objects_map['fixed_wall 2'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (120, 101)
            wall_instance.wh = (40, 38)
            objects.append(wall_instance)
            objects_map['fixed_wall 3'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (8, 101)
            wall_instance.wh = (32, 38)
            objects.append(wall_instance)
            objects_map['fixed_wall 4'] = wall_instance
            number_of_walls = 5
            i = 0
            while(objects_map.get(f"fixed wall {number_of_walls + i}")!= None):
                objects_map.pop(f"fixed wall {number_of_walls + i}")
                i += 1
        elif ram_state[28] == 11:
            wall_instance = Wall()
            wall_instance.xy = (8, 21)
            wall_instance.wh = (152, 38)
            objects.append(wall_instance)
            objects_map['fixed_wall 0'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (56, 61)
            wall_instance.wh = (48, 37)
            objects.append(wall_instance)
            objects_map['fixed_wall 1'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (116, 101)
            wall_instance.wh = (44, 38)
            objects.append(wall_instance)
            objects_map['fixed_wall 2'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (8, 101)
            wall_instance.wh = (36, 38)
            objects.append(wall_instance)
            objects_map['fixed_wall 3'] = wall_instance
            number_of_walls = 4
            i = 0
            while(objects_map.get(f"fixed wall {number_of_walls + i}")!= None):
                objects_map.pop(f"fixed wall {number_of_walls + i}")
                i += 1
        elif ram_state[28] == 12:
            wall_instance = Wall()
            wall_instance.xy = (8, 21)
            wall_instance.wh = (152, 38)
            objects.append(wall_instance)
            objects_map['fixed_wall 0'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (128, 101)
            wall_instance.wh = (32, 38)
            objects.append(wall_instance)
            objects_map['fixed_wall 1'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (72, 101)
            wall_instance.wh = (16, 38)
            objects.append(wall_instance)
            objects_map['fixed_wall 2'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (8, 101)
            wall_instance.wh = (24, 38)
            objects.append(wall_instance)
            objects_map['fixed_wall 3'] = wall_instance
            number_of_walls = 4
            i = 0
            while(objects_map.get(f"fixed wall {number_of_walls + i}")!= None):
                objects_map.pop(f"fixed wall {number_of_walls + i}")
                i += 1
        elif ram_state[28] == 13:
            wall_instance = Wall()
            wall_instance.xy = (8, 21)
            wall_instance.wh = (152, 38)
            objects.append(wall_instance)
            objects_map['fixed_wall 0'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (8, 101)
            wall_instance.wh = (152, 38)
            objects.append(wall_instance)
            objects_map['fixed_wall 1'] = wall_instance
            number_of_walls = 2
            i = 0
            while(objects_map.get(f"fixed wall {number_of_walls + i}")!= None):
                objects_map.pop(f"fixed wall {number_of_walls + i}")
                i += 1

    elif ram_state[117] == 8:
        if ram_state[28] == 0:
            wall_instance = Wall()
            wall_instance.xy = (136, 21)
            wall_instance.wh = (24, 38)
            objects.append(wall_instance)
            objects_map['fixed_wall 0'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (8, 21)
            wall_instance.wh = (16, 38)
            objects.append(wall_instance)
            objects_map['fixed_wall 1'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (88, 101)
            wall_instance.wh = (72, 38)
            objects.append(wall_instance)
            objects_map['fixed_wall 2'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (8, 101)
            wall_instance.wh = (64, 38)
            objects.append(wall_instance)
            objects_map['fixed_wall 3'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (144, 61)
            wall_instance.wh = (16, 37)
            objects.append(wall_instance)
            objects_map['fixed_wall 4'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (8, 61)
            wall_instance.wh = (8, 37)
            objects.append(wall_instance)
            objects_map['fixed_wall 5'] = wall_instance
            number_of_walls = 6
            i = 0
            while(objects_map.get(f"fixed wall {number_of_walls + i}")!= None):
                objects_map.pop(f"fixed wall {number_of_walls + i}")
                i += 1
        elif ram_state[28] == 1:
            wall_instance = Wall()
            wall_instance.xy = (88, 21)
            wall_instance.wh = (72, 38)
            objects.append(wall_instance)
            objects_map['fixed_wall 0'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (8, 21)
            wall_instance.wh = (64, 38)
            objects.append(wall_instance)
            objects_map['fixed_wall 1'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (136, 101)
            wall_instance.wh = (24, 38)
            objects.append(wall_instance)
            objects_map['fixed_wall 2'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (40, 101)
            wall_instance.wh = (80, 38)
            objects.append(wall_instance)
            objects_map['fixed_wall 3'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (8, 101)
            wall_instance.wh = (16, 38)
            objects.append(wall_instance)
            objects_map['fixed_wall 4'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (144, 61)
            wall_instance.wh = (16, 37)
            objects.append(wall_instance)
            objects_map['fixed_wall 5'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (8, 61)
            wall_instance.wh = (8, 37)
            objects.append(wall_instance)
            objects_map['fixed_wall 6'] = wall_instance
            number_of_walls = 7
            i = 0
            while(objects_map.get(f"fixed wall {number_of_walls + i}")!= None):
                objects_map.pop(f"fixed wall {number_of_walls + i}")
                i += 1
        elif ram_state[28] == 2:
            wall_instance = Wall()
            wall_instance.xy = (136, 21)
            wall_instance.wh = (24, 38)
            objects.append(wall_instance)
            objects_map['fixed_wall 0'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (40, 21)
            wall_instance.wh = (80, 38)
            objects.append(wall_instance)
            objects_map['fixed_wall 1'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (8, 21)
            wall_instance.wh = (16, 38)
            objects.append(wall_instance)
            objects_map['fixed_wall 2'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (136, 101)
            wall_instance.wh = (24, 38)
            objects.append(wall_instance)
            objects_map['fixed_wall 3'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (8, 101)
            wall_instance.wh = (16, 38)
            objects.append(wall_instance)
            objects_map['fixed_wall 4'] = wall_instance
            number_of_walls = 5
            i = 0
            while(objects_map.get(f"fixed wall {number_of_walls + i}")!= None):
                objects_map.pop(f"fixed wall {number_of_walls + i}")
                i += 1
        elif ram_state[28] == 3:
            wall_instance = Wall()
            wall_instance.xy = (136, 21)
            wall_instance.wh = (24, 38)
            objects.append(wall_instance)
            objects_map['fixed_wall 0'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (8, 21)
            wall_instance.wh = (16, 38)
            objects.append(wall_instance)
            objects_map['fixed_wall 1'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (136, 101)
            wall_instance.wh = (24, 38)
            objects.append(wall_instance)
            objects_map['fixed_wall 2'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (8, 101)
            wall_instance.wh = (16, 38)
            objects.append(wall_instance)
            objects_map['fixed_wall 3'] = wall_instance
            number_of_walls = 4
            i = 0
            while(objects_map.get(f"fixed wall {number_of_walls + i}")!= None):
                objects_map.pop(f"fixed wall {number_of_walls + i}")
                i += 1
        elif ram_state[28] == 4:
            wall_instance = Wall()
            wall_instance.xy = (136, 21)
            wall_instance.wh = (24, 38)
            objects.append(wall_instance)
            objects_map['fixed_wall 0'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (8, 21)
            wall_instance.wh = (16, 38)
            objects.append(wall_instance)
            objects_map['fixed_wall 1'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (136, 101)
            wall_instance.wh = (24, 38)
            objects.append(wall_instance)
            objects_map['fixed_wall 2'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (8, 101)
            wall_instance.wh = (16, 38)
            objects.append(wall_instance)
            objects_map['fixed_wall 3'] = wall_instance
            number_of_walls = 4
            i = 0
            while(objects_map.get(f"fixed wall {number_of_walls + i}")!= None):
                objects_map.pop(f"fixed wall {number_of_walls + i}")
                i += 1
        elif ram_state[28] == 5:
            wall_instance = Wall()
            wall_instance.xy = (136, 21)
            wall_instance.wh = (24, 38)
            objects.append(wall_instance)
            objects_map['fixed_wall 0'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (8, 21)
            wall_instance.wh = (16, 38)
            objects.append(wall_instance)
            objects_map['fixed_wall 1'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (136, 101)
            wall_instance.wh = (24, 38)
            objects.append(wall_instance)
            objects_map['fixed_wall 2'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (8, 101)
            wall_instance.wh = (16, 38)
            objects.append(wall_instance)
            objects_map['fixed_wall 3'] = wall_instance
            number_of_walls = 4
            i = 0
            while(objects_map.get(f"fixed wall {number_of_walls + i}")!= None):
                objects_map.pop(f"fixed wall {number_of_walls + i}")
                i += 1
        elif ram_state[28] == 6:
            wall_instance = Wall()
            wall_instance.xy = (136, 21)
            wall_instance.wh = (24, 38)
            objects.append(wall_instance)
            objects_map['fixed_wall 0'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (8, 21)
            wall_instance.wh = (16, 38)
            objects.append(wall_instance)
            objects_map['fixed_wall 1'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (104, 101)
            wall_instance.wh = (56, 38)
            objects.append(wall_instance)
            objects_map['fixed_wall 2'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (72, 101)
            wall_instance.wh = (16, 38)
            objects.append(wall_instance)
            objects_map['fixed_wall 3'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (8, 101)
            wall_instance.wh = (48, 38)
            objects.append(wall_instance)
            objects_map['fixed_wall 4'] = wall_instance
            number_of_walls = 5
            i = 0
            while(objects_map.get(f"fixed wall {number_of_walls + i}")!= None):
                objects_map.pop(f"fixed wall {number_of_walls + i}")
                i += 1
        elif ram_state[28] == 7:
            wall_instance = Wall()
            wall_instance.xy = (104, 21)
            wall_instance.wh = (56, 38)
            objects.append(wall_instance)
            objects_map['fixed_wall 0'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (72, 21)
            wall_instance.wh = (16, 38)
            objects.append(wall_instance)
            objects_map['fixed_wall 1'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (8, 21)
            wall_instance.wh = (48, 38)
            objects.append(wall_instance)
            objects_map['fixed_wall 2'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (136, 101)
            wall_instance.wh = (24, 38)
            objects.append(wall_instance)
            objects_map['fixed_wall 3'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (32, 101)
            wall_instance.wh = (96, 38)
            objects.append(wall_instance)
            objects_map['fixed_wall 4'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (8, 101)
            wall_instance.wh = (16, 38)
            objects.append(wall_instance)
            objects_map['fixed_wall 5'] = wall_instance
            number_of_walls = 6
            i = 0
            while(objects_map.get(f"fixed wall {number_of_walls + i}")!= None):
                objects_map.pop(f"fixed wall {number_of_walls + i}")
                i += 1
        elif ram_state[28] == 8:
            wall_instance = Wall()
            wall_instance.xy = (136, 21)
            wall_instance.wh = (24, 38)
            objects.append(wall_instance)
            objects_map['fixed_wall 0'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (32, 21)
            wall_instance.wh = (96, 38)
            objects.append(wall_instance)
            objects_map['fixed_wall 1'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (8, 21)
            wall_instance.wh = (16, 38)
            objects.append(wall_instance)
            objects_map['fixed_wall 2'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (88, 101)
            wall_instance.wh = (72, 38)
            objects.append(wall_instance)
            objects_map['fixed_wall 3'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (8, 101)
            wall_instance.wh = (64, 38)
            objects.append(wall_instance)
            objects_map['fixed_wall 4'] = wall_instance
            number_of_walls = 5
            i = 0
            while(objects_map.get(f"fixed wall {number_of_walls + i}")!= None):
                objects_map.pop(f"fixed wall {number_of_walls + i}")
                i += 1
        elif ram_state[28] == 9:
            wall_instance = Wall()
            wall_instance.xy = (88, 21)
            wall_instance.wh = (72, 38)
            objects.append(wall_instance)
            objects_map['fixed_wall 0'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (8, 21)
            wall_instance.wh = (64, 38)
            objects.append(wall_instance)
            objects_map['fixed_wall 1'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (136, 101)
            wall_instance.wh = (24, 38)
            objects.append(wall_instance)
            objects_map['fixed_wall 2'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (8, 101)
            wall_instance.wh = (16, 38)
            objects.append(wall_instance)
            objects_map['fixed_wall 3'] = wall_instance
            number_of_walls = 4
            i = 0
            while(objects_map.get(f"fixed wall {number_of_walls + i}")!= None):
                objects_map.pop(f"fixed wall {number_of_walls + i}")
                i += 1
        elif ram_state[28] == 10:
            wall_instance = Wall()
            wall_instance.xy = (136, 21)
            wall_instance.wh = (24, 38)
            objects.append(wall_instance)
            objects_map['fixed_wall 0'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (8, 21)
            wall_instance.wh = (16, 38)
            objects.append(wall_instance)
            objects_map['fixed_wall 1'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (112, 101)
            wall_instance.wh = (48, 38)
            objects.append(wall_instance)
            objects_map['fixed_wall 2'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (8, 101)
            wall_instance.wh = (40, 38)
            objects.append(wall_instance)
            objects_map['fixed_wall 3'] = wall_instance
            number_of_walls = 4
            i = 0
            while(objects_map.get(f"fixed wall {number_of_walls + i}")!= None):
                objects_map.pop(f"fixed wall {number_of_walls + i}")
                i += 1
        elif ram_state[28] == 11:
            wall_instance = Wall()
            wall_instance.xy = (8, 21)
            wall_instance.wh = (152, 38)
            objects.append(wall_instance)
            objects_map['fixed_wall 0'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (128, 101)
            wall_instance.wh = (32, 38)
            objects.append(wall_instance)
            objects_map['fixed_wall 1'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (8, 101)
            wall_instance.wh = (24, 38)
            objects.append(wall_instance)
            objects_map['fixed_wall 2'] = wall_instance
            number_of_walls = 3
            i = 0
            while(objects_map.get(f"fixed wall {number_of_walls + i}")!= None):
                objects_map.pop(f"fixed wall {number_of_walls + i}")
                i += 1
        elif ram_state[28] == 12:
            wall_instance = Wall()
            wall_instance.xy = (8, 21)
            wall_instance.wh = (152, 38)
            objects.append(wall_instance)
            objects_map['fixed_wall 0'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (140, 101)
            wall_instance.wh = (20, 38)
            objects.append(wall_instance)
            objects_map['fixed_wall 1'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (72, 101)
            wall_instance.wh = (16, 38)
            objects.append(wall_instance)
            objects_map['fixed_wall 2'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (8, 101)
            wall_instance.wh = (12, 38)
            objects.append(wall_instance)
            objects_map['fixed_wall 3'] = wall_instance
            number_of_walls = 4
            i = 0
            while(objects_map.get(f"fixed wall {number_of_walls + i}")!= None):
                objects_map.pop(f"fixed wall {number_of_walls + i}")
                i += 1
        elif ram_state[28] == 13:
            wall_instance = Wall()
            wall_instance.xy = (8, 21)
            wall_instance.wh = (152, 38)
            objects.append(wall_instance)
            objects_map['fixed_wall 0'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (64, 61)
            wall_instance.wh = (32, 37)
            objects.append(wall_instance)
            objects_map['fixed_wall 1'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (112, 101)
            wall_instance.wh = (48, 38)
            objects.append(wall_instance)
            objects_map['fixed_wall 2'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (8, 101)
            wall_instance.wh = (40, 38)
            objects.append(wall_instance)
            objects_map['fixed_wall 3'] = wall_instance
            number_of_walls = 4
            i = 0
            while(objects_map.get(f"fixed wall {number_of_walls + i}")!= None):
                objects_map.pop(f"fixed wall {number_of_walls + i}")
                i += 1
        elif ram_state[28] == 14:
            wall_instance = Wall()
            wall_instance.xy = (8, 21)
            wall_instance.wh = (152, 38)
            objects.append(wall_instance)
            objects_map['fixed_wall 0'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (48, 61)
            wall_instance.wh = (64, 37)
            objects.append(wall_instance)
            objects_map['fixed_wall 1'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (136, 101)
            wall_instance.wh = (24, 38)
            objects.append(wall_instance)
            objects_map['fixed_wall 2'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (8, 101)
            wall_instance.wh = (16, 38)
            objects.append(wall_instance)
            objects_map['fixed_wall 3'] = wall_instance
            number_of_walls = 4
            i = 0
            while(objects_map.get(f"fixed wall {number_of_walls + i}")!= None):
                objects_map.pop(f"fixed wall {number_of_walls + i}")
                i += 1
        elif ram_state[28] == 15:
            wall_instance = Wall()
            wall_instance.xy = (8, 21)
            wall_instance.wh = (152, 38)
            objects.append(wall_instance)
            objects_map['fixed_wall 0'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (8, 101)
            wall_instance.wh = (152, 38)
            objects.append(wall_instance)
            objects_map['fixed_wall 1'] = wall_instance
            number_of_walls = 2
            i = 0
            while(objects_map.get(f"fixed wall {number_of_walls + i}")!= None):
                objects_map.pop(f"fixed wall {number_of_walls + i}")
                i += 1

    elif ram_state[117] == 9:
        if ram_state[28] == 0:
            wall_instance = Wall()
            wall_instance.xy = (136, 21)
            wall_instance.wh = (24, 38)
            objects.append(wall_instance)
            objects_map['fixed_wall 0'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (8, 21)
            wall_instance.wh = (16, 38)
            objects.append(wall_instance)
            objects_map['fixed_wall 1'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (88, 101)
            wall_instance.wh = (72, 38)
            objects.append(wall_instance)
            objects_map['fixed_wall 2'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (8, 101)
            wall_instance.wh = (64, 38)
            objects.append(wall_instance)
            objects_map['fixed_wall 3'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (144, 61)
            wall_instance.wh = (16, 37)
            objects.append(wall_instance)
            objects_map['fixed_wall 4'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (8, 61)
            wall_instance.wh = (8, 37)
            objects.append(wall_instance)
            objects_map['fixed_wall 5'] = wall_instance
            number_of_walls = 6
            i = 0
            while(objects_map.get(f"fixed wall {number_of_walls + i}")!= None):
                objects_map.pop(f"fixed wall {number_of_walls + i}")
                i += 1
        elif ram_state[28] == 1:
            wall_instance = Wall()
            wall_instance.xy = (88, 21)
            wall_instance.wh = (72, 38)
            objects.append(wall_instance)
            objects_map['fixed_wall 0'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (8, 21)
            wall_instance.wh = (64, 38)
            objects.append(wall_instance)
            objects_map['fixed_wall 1'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (136, 101)
            wall_instance.wh = (24, 38)
            objects.append(wall_instance)
            objects_map['fixed_wall 2'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (32, 101)
            wall_instance.wh = (96, 38)
            objects.append(wall_instance)
            objects_map['fixed_wall 3'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (8, 101)
            wall_instance.wh = (16, 38)
            objects.append(wall_instance)
            objects_map['fixed_wall 4'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (144, 61)
            wall_instance.wh = (16, 37)
            objects.append(wall_instance)
            objects_map['fixed_wall 5'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (8, 61)
            wall_instance.wh = (8, 37)
            objects.append(wall_instance)
            objects_map['fixed_wall 6'] = wall_instance
            number_of_walls = 7
            i = 0
            while(objects_map.get(f"fixed wall {number_of_walls + i}")!= None):
                objects_map.pop(f"fixed wall {number_of_walls + i}")
                i += 1
        elif ram_state[28] == 2:
            wall_instance = Wall()
            wall_instance.xy = (136, 21)
            wall_instance.wh = (24, 38)
            objects.append(wall_instance)
            objects_map['fixed_wall 0'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (32, 21)
            wall_instance.wh = (96, 38)
            objects.append(wall_instance)
            objects_map['fixed_wall 1'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (8, 21)
            wall_instance.wh = (16, 38)
            objects.append(wall_instance)
            objects_map['fixed_wall 2'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (84, 101)
            wall_instance.wh = (76, 38)
            objects.append(wall_instance)
            objects_map['fixed_wall 3'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (8, 101)
            wall_instance.wh = (68, 38)
            objects.append(wall_instance)
            objects_map['fixed_wall 4'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (144, 61)
            wall_instance.wh = (16, 37)
            objects.append(wall_instance)
            objects_map['fixed_wall 5'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (8, 61)
            wall_instance.wh = (8, 37)
            objects.append(wall_instance)
            objects_map['fixed_wall 6'] = wall_instance
            number_of_walls = 7
            i = 0
            while(objects_map.get(f"fixed wall {number_of_walls + i}")!= None):
                objects_map.pop(f"fixed wall {number_of_walls + i}")
                i += 1
        elif ram_state[28] == 3:
            wall_instance = Wall()
            wall_instance.xy = (84, 21)
            wall_instance.wh = (76, 38)
            objects.append(wall_instance)
            objects_map['fixed_wall 0'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (8, 21)
            wall_instance.wh = (68, 38)
            objects.append(wall_instance)
            objects_map['fixed_wall 1'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (132, 101)
            wall_instance.wh = (28, 38)
            objects.append(wall_instance)
            objects_map['fixed_wall 2'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (84, 101)
            wall_instance.wh = (40, 38)
            objects.append(wall_instance)
            objects_map['fixed_wall 3'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (36, 101)
            wall_instance.wh = (40, 38)
            objects.append(wall_instance)
            objects_map['fixed_wall 4'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (8, 101)
            wall_instance.wh = (20, 38)
            objects.append(wall_instance)
            objects_map['fixed_wall 5'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (144, 61)
            wall_instance.wh = (16, 37)
            objects.append(wall_instance)
            objects_map['fixed_wall 6'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (8, 61)
            wall_instance.wh = (8, 37)
            objects.append(wall_instance)
            objects_map['fixed_wall 7'] = wall_instance
            number_of_walls = 8
            i = 0
            while(objects_map.get(f"fixed wall {number_of_walls + i}")!= None):
                objects_map.pop(f"fixed wall {number_of_walls + i}")
                i += 1
        elif ram_state[28] == 4:
            wall_instance = Wall()
            wall_instance.xy = (132, 21)
            wall_instance.wh = (28, 38)
            objects.append(wall_instance)
            objects_map['fixed_wall 0'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (84, 21)
            wall_instance.wh = (40, 38)
            objects.append(wall_instance)
            objects_map['fixed_wall 1'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (36, 21)
            wall_instance.wh = (40, 38)
            objects.append(wall_instance)
            objects_map['fixed_wall 2'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (8, 21)
            wall_instance.wh = (20, 38)
            objects.append(wall_instance)
            objects_map['fixed_wall 3'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (132, 101)
            wall_instance.wh = (28, 38)
            objects.append(wall_instance)
            objects_map['fixed_wall 4'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (36, 101)
            wall_instance.wh = (88, 38)
            objects.append(wall_instance)
            objects_map['fixed_wall 5'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (8, 101)
            wall_instance.wh = (20, 38)
            objects.append(wall_instance)
            objects_map['fixed_wall 6'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (136, 61)
            wall_instance.wh = (24, 37)
            objects.append(wall_instance)
            objects_map['fixed_wall 7'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (56, 61)
            wall_instance.wh = (64, 37)
            objects.append(wall_instance)
            objects_map['fixed_wall 8'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (8, 61)
            wall_instance.wh = (32, 37)
            objects.append(wall_instance)
            objects_map['fixed_wall 9'] = wall_instance
            number_of_walls = 10
            i = 0
            while(objects_map.get(f"fixed wall {number_of_walls + i}")!= None):
                objects_map.pop(f"fixed wall {number_of_walls + i}")
                i += 1
        elif ram_state[28] == 5:
            wall_instance = Wall()
            wall_instance.xy = (132, 21)
            wall_instance.wh = (28, 38)
            objects.append(wall_instance)
            objects_map['fixed_wall 0'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (36, 21)
            wall_instance.wh = (88, 38)
            objects.append(wall_instance)
            objects_map['fixed_wall 1'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (8, 21)
            wall_instance.wh = (20, 38)
            objects.append(wall_instance)
            objects_map['fixed_wall 2'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (124, 101)
            wall_instance.wh = (36, 38)
            objects.append(wall_instance)
            objects_map['fixed_wall 3'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (48, 101)
            wall_instance.wh = (64, 38)
            objects.append(wall_instance)
            objects_map['fixed_wall 4'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (8, 101)
            wall_instance.wh = (28, 38)
            objects.append(wall_instance)
            objects_map['fixed_wall 5'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (144, 61)
            wall_instance.wh = (16, 37)
            objects.append(wall_instance)
            objects_map['fixed_wall 6'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (44, 61)
            wall_instance.wh = (72, 37)
            objects.append(wall_instance)
            objects_map['fixed_wall 7'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (8, 61)
            wall_instance.wh = (8, 37)
            objects.append(wall_instance)
            objects_map['fixed_wall 8'] = wall_instance
            number_of_walls = 9
            i = 0
            while(objects_map.get(f"fixed wall {number_of_walls + i}")!= None):
                objects_map.pop(f"fixed wall {number_of_walls + i}")
                i += 1
        elif ram_state[28] == 6:
            wall_instance = Wall()
            wall_instance.xy = (124, 21)
            wall_instance.wh = (36, 38)
            objects.append(wall_instance)
            objects_map['fixed_wall 0'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (48, 21)
            wall_instance.wh = (64, 38)
            objects.append(wall_instance)
            objects_map['fixed_wall 1'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (8, 21)
            wall_instance.wh = (28, 38)
            objects.append(wall_instance)
            objects_map['fixed_wall 2'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (140, 101)
            wall_instance.wh = (20, 38)
            objects.append(wall_instance)
            objects_map['fixed_wall 3'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (88, 101)
            wall_instance.wh = (36, 38)
            objects.append(wall_instance)
            objects_map['fixed_wall 4'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (36, 101)
            wall_instance.wh = (36, 38)
            objects.append(wall_instance)
            objects_map['fixed_wall 5'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (8, 101)
            wall_instance.wh = (12, 38)
            objects.append(wall_instance)
            objects_map['fixed_wall 6'] = wall_instance
            number_of_walls = 7
            i = 0
            while(objects_map.get(f"fixed wall {number_of_walls + i}")!= None):
                objects_map.pop(f"fixed wall {number_of_walls + i}")
                i += 1
        elif ram_state[28] == 7:
            wall_instance = Wall()
            wall_instance.xy = (140, 21)
            wall_instance.wh = (20, 38)
            objects.append(wall_instance)
            objects_map['fixed_wall 0'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (88, 21)
            wall_instance.wh = (36, 38)
            objects.append(wall_instance)
            objects_map['fixed_wall 1'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (36, 21)
            wall_instance.wh = (36, 38)
            objects.append(wall_instance)
            objects_map['fixed_wall 2'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (8, 21)
            wall_instance.wh = (12, 38)
            objects.append(wall_instance)
            objects_map['fixed_wall 3'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (144, 101)
            wall_instance.wh = (16, 38)
            objects.append(wall_instance)
            objects_map['fixed_wall 4'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (8, 101)
            wall_instance.wh = (8, 38)
            objects.append(wall_instance)
            objects_map['fixed_wall 5'] = wall_instance
            number_of_walls = 6
            i = 0
            while(objects_map.get(f"fixed wall {number_of_walls + i}")!= None):
                objects_map.pop(f"fixed wall {number_of_walls + i}")
                i += 1
        elif ram_state[28] == 8:
            wall_instance = Wall()
            wall_instance.xy = (144, 21)
            wall_instance.wh = (16, 38)
            objects.append(wall_instance)
            objects_map['fixed_wall 0'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (8, 21)
            wall_instance.wh = (8, 38)
            objects.append(wall_instance)
            objects_map['fixed_wall 1'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (144, 101)
            wall_instance.wh = (16, 38)
            objects.append(wall_instance)
            objects_map['fixed_wall 2'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (8, 101)
            wall_instance.wh = (8, 38)
            objects.append(wall_instance)
            objects_map['fixed_wall 3'] = wall_instance
            number_of_walls = 4
            i = 0
            while(objects_map.get(f"fixed wall {number_of_walls + i}")!= None):
                objects_map.pop(f"fixed wall {number_of_walls + i}")
                i += 1
        elif ram_state[28] == 9:
            wall_instance = Wall()
            wall_instance.xy = (144, 21)
            wall_instance.wh = (16, 38)
            objects.append(wall_instance)
            objects_map['fixed_wall 0'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (8, 21)
            wall_instance.wh = (8, 38)
            objects.append(wall_instance)
            objects_map['fixed_wall 1'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (136, 101)
            wall_instance.wh = (24, 38)
            objects.append(wall_instance)
            objects_map['fixed_wall 2'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (8, 101)
            wall_instance.wh = (16, 38)
            objects.append(wall_instance)
            objects_map['fixed_wall 3'] = wall_instance
            number_of_walls = 4
            i = 0
            while(objects_map.get(f"fixed wall {number_of_walls + i}")!= None):
                objects_map.pop(f"fixed wall {number_of_walls + i}")
                i += 1
        elif ram_state[28] == 10:
            wall_instance = Wall()
            wall_instance.xy = (136, 21)
            wall_instance.wh = (24, 38)
            objects.append(wall_instance)
            objects_map['fixed_wall 0'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (8, 21)
            wall_instance.wh = (16, 38)
            objects.append(wall_instance)
            objects_map['fixed_wall 1'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (128, 101)
            wall_instance.wh = (32, 38)
            objects.append(wall_instance)
            objects_map['fixed_wall 2'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (8, 101)
            wall_instance.wh = (24, 38)
            objects.append(wall_instance)
            objects_map['fixed_wall 3'] = wall_instance
            number_of_walls = 4
            i = 0
            while(objects_map.get(f"fixed wall {number_of_walls + i}")!= None):
                objects_map.pop(f"fixed wall {number_of_walls + i}")
                i += 1
        elif ram_state[28] == 11:
            wall_instance = Wall()
            wall_instance.xy = (8, 21)
            wall_instance.wh = (152, 38)
            objects.append(wall_instance)
            objects_map['fixed_wall 0'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (132, 101)
            wall_instance.wh = (28, 38)
            objects.append(wall_instance)
            objects_map['fixed_wall 1'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (8, 101)
            wall_instance.wh = (20, 38)
            objects.append(wall_instance)
            objects_map['fixed_wall 2'] = wall_instance
            number_of_walls = 3
            i = 0
            while(objects_map.get(f"fixed wall {number_of_walls + i}")!= None):
                objects_map.pop(f"fixed wall {number_of_walls + i}")
                i += 1
        elif ram_state[28] == 12:
            wall_instance = Wall()
            wall_instance.xy = (8, 21)
            wall_instance.wh = (152, 38)
            objects.append(wall_instance)
            objects_map['fixed_wall 0'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (136, 101)
            wall_instance.wh = (24, 38)
            objects.append(wall_instance)
            objects_map['fixed_wall 1'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (72, 101)
            wall_instance.wh = (16, 38)
            objects.append(wall_instance)
            objects_map['fixed_wall 2'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (8, 101)
            wall_instance.wh = (16, 38)
            objects.append(wall_instance)
            objects_map['fixed_wall 3'] = wall_instance
            number_of_walls = 4
            i = 0
            while(objects_map.get(f"fixed wall {number_of_walls + i}")!= None):
                objects_map.pop(f"fixed wall {number_of_walls + i}")
                i += 1
        elif ram_state[28] == 13:
            wall_instance = Wall()
            wall_instance.xy = (8, 21)
            wall_instance.wh = (152, 38)
            objects.append(wall_instance)
            objects_map['fixed_wall 0'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (136, 101)
            wall_instance.wh = (24, 38)
            objects.append(wall_instance)
            objects_map['fixed_wall 1'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (8, 101)
            wall_instance.wh = (16, 38)
            objects.append(wall_instance)
            objects_map['fixed_wall 2'] = wall_instance
            number_of_walls = 3
            i = 0
            while(objects_map.get(f"fixed wall {number_of_walls + i}")!= None):
                objects_map.pop(f"fixed wall {number_of_walls + i}")
                i += 1
        elif ram_state[28] == 14:
            wall_instance = Wall()
            wall_instance.xy = (8, 21)
            wall_instance.wh = (152, 38)
            objects.append(wall_instance)
            objects_map['fixed_wall 0'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (120, 101)
            wall_instance.wh = (40, 38)
            objects.append(wall_instance)
            objects_map['fixed_wall 1'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (72, 101)
            wall_instance.wh = (16, 38)
            objects.append(wall_instance)
            objects_map['fixed_wall 2'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (8, 101)
            wall_instance.wh = (32, 38)
            objects.append(wall_instance)
            objects_map['fixed_wall 3'] = wall_instance
            number_of_walls = 4
            i = 0
            while(objects_map.get(f"fixed wall {number_of_walls + i}")!= None):
                objects_map.pop(f"fixed wall {number_of_walls + i}")
                i += 1
        elif ram_state[28] == 15:
            wall_instance = Wall()
            wall_instance.xy = (8, 21)
            wall_instance.wh = (152, 38)
            objects.append(wall_instance)
            objects_map['fixed_wall 0'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (8, 101)
            wall_instance.wh = (152, 38)
            objects.append(wall_instance)
            objects_map['fixed_wall 1'] = wall_instance
            number_of_walls = 2
            i = 0
            while(objects_map.get(f"fixed wall {number_of_walls + i}")!= None):
                objects_map.pop(f"fixed wall {number_of_walls + i}")
                i += 1

    elif ram_state[117] == 10:
        if ram_state[28] == 0:
            wall_instance = Wall()
            wall_instance.xy = (136, 21)
            wall_instance.wh = (24, 38)
            objects.append(wall_instance)
            objects_map['fixed_wall 0'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (8, 21)
            wall_instance.wh = (16, 38)
            objects.append(wall_instance)
            objects_map['fixed_wall 1'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (88, 101)
            wall_instance.wh = (72, 38)
            objects.append(wall_instance)
            objects_map['fixed_wall 2'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (8, 101)
            wall_instance.wh = (64, 38)
            objects.append(wall_instance)
            objects_map['fixed_wall 3'] = wall_instance
            number_of_walls = 4
            i = 0
            while(objects_map.get(f"fixed wall {number_of_walls + i}")!= None):
                objects_map.pop(f"fixed wall {number_of_walls + i}")
                i += 1
        elif ram_state[28] == 1:
            wall_instance = Wall()
            wall_instance.xy = (88, 21)
            wall_instance.wh = (72, 38)
            objects.append(wall_instance)
            objects_map['fixed_wall 0'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (8, 21)
            wall_instance.wh = (64, 38)
            objects.append(wall_instance)
            objects_map['fixed_wall 1'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (112, 101)
            wall_instance.wh = (48, 38)
            objects.append(wall_instance)
            objects_map['fixed_wall 2'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (8, 101)
            wall_instance.wh = (40, 38)
            objects.append(wall_instance)
            objects_map['fixed_wall 3'] = wall_instance
            number_of_walls = 4
            i = 0
            while(objects_map.get(f"fixed wall {number_of_walls + i}")!= None):
                objects_map.pop(f"fixed wall {number_of_walls + i}")
                i += 1
        elif ram_state[28] == 2:
            wall_instance = Wall()
            wall_instance.xy = (112, 21)
            wall_instance.wh = (48, 38)
            objects.append(wall_instance)
            objects_map['fixed_wall 0'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (8, 21)
            wall_instance.wh = (40, 38)
            objects.append(wall_instance)
            objects_map['fixed_wall 1'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (140, 101)
            wall_instance.wh = (20, 38)
            objects.append(wall_instance)
            objects_map['fixed_wall 2'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (28, 101)
            wall_instance.wh = (104, 38)
            objects.append(wall_instance)
            objects_map['fixed_wall 3'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (8, 101)
            wall_instance.wh = (12, 38)
            objects.append(wall_instance)
            objects_map['fixed_wall 4'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (144, 61)
            wall_instance.wh = (16, 37)
            objects.append(wall_instance)
            objects_map['fixed_wall 5'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (72, 61)
            wall_instance.wh = (16, 37)
            objects.append(wall_instance)
            objects_map['fixed_wall 6'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (8, 61)
            wall_instance.wh = (8, 37)
            objects.append(wall_instance)
            objects_map['fixed_wall 7'] = wall_instance
            number_of_walls = 8
            i = 0
            while(objects_map.get(f"fixed wall {number_of_walls + i}")!= None):
                objects_map.pop(f"fixed wall {number_of_walls + i}")
                i += 1
        elif ram_state[28] == 3:
            wall_instance = Wall()
            wall_instance.xy = (140, 21)
            wall_instance.wh = (20, 38)
            objects.append(wall_instance)
            objects_map['fixed_wall 0'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (28, 21)
            wall_instance.wh = (104, 38)
            objects.append(wall_instance)
            objects_map['fixed_wall 1'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (8, 21)
            wall_instance.wh = (12, 38)
            objects.append(wall_instance)
            objects_map['fixed_wall 2'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (88, 101)
            wall_instance.wh = (72, 38)
            objects.append(wall_instance)
            objects_map['fixed_wall 3'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (8, 101)
            wall_instance.wh = (64, 38)
            objects.append(wall_instance)
            objects_map['fixed_wall 4'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (144, 61)
            wall_instance.wh = (16, 37)
            objects.append(wall_instance)
            objects_map['fixed_wall 5'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (8, 61)
            wall_instance.wh = (8, 37)
            objects.append(wall_instance)
            objects_map['fixed_wall 6'] = wall_instance
            number_of_walls = 7
            i = 0
            while(objects_map.get(f"fixed wall {number_of_walls + i}")!= None):
                objects_map.pop(f"fixed wall {number_of_walls + i}")
                i += 1
        elif ram_state[28] == 4:
            wall_instance = Wall()
            wall_instance.xy = (88, 21)
            wall_instance.wh = (72, 38)
            objects.append(wall_instance)
            objects_map['fixed_wall 0'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (8, 21)
            wall_instance.wh = (64, 38)
            objects.append(wall_instance)
            objects_map['fixed_wall 1'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (140, 101)
            wall_instance.wh = (20, 38)
            objects.append(wall_instance)
            objects_map['fixed_wall 2'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (116, 101)
            wall_instance.wh = (16, 38)
            objects.append(wall_instance)
            objects_map['fixed_wall 3'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (84, 101)
            wall_instance.wh = (24, 38)
            objects.append(wall_instance)
            objects_map['fixed_wall 4'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (52, 101)
            wall_instance.wh = (24, 38)
            objects.append(wall_instance)
            objects_map['fixed_wall 5'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (28, 101)
            wall_instance.wh = (16, 38)
            objects.append(wall_instance)
            objects_map['fixed_wall 6'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (8, 101)
            wall_instance.wh = (12, 38)
            objects.append(wall_instance)
            objects_map['fixed_wall 7'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (144, 61)
            wall_instance.wh = (16, 37)
            objects.append(wall_instance)
            objects_map['fixed_wall 8'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (92, 61)
            wall_instance.wh = (12, 37)
            objects.append(wall_instance)
            objects_map['fixed_wall 9'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (56, 61)
            wall_instance.wh = (12, 37)
            objects.append(wall_instance)
            objects_map['fixed_wall 10'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (8, 61)
            wall_instance.wh = (8, 37)
            objects.append(wall_instance)
            objects_map['fixed_wall 11'] = wall_instance
            number_of_walls = 12
            i = 0
            while(objects_map.get(f"fixed wall {number_of_walls + i}")!= None):
                objects_map.pop(f"fixed wall {number_of_walls + i}")
                i += 1
        elif ram_state[28] == 5:
            wall_instance = Wall()
            wall_instance.xy = (140, 21)
            wall_instance.wh = (20, 38)
            objects.append(wall_instance)
            objects_map['fixed_wall 0'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (116, 21)
            wall_instance.wh = (16, 38)
            objects.append(wall_instance)
            objects_map['fixed_wall 1'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (84, 21)
            wall_instance.wh = (24, 38)
            objects.append(wall_instance)
            objects_map['fixed_wall 2'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (52, 21)
            wall_instance.wh = (24, 38)
            objects.append(wall_instance)
            objects_map['fixed_wall 3'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (28, 21)
            wall_instance.wh = (16, 38)
            objects.append(wall_instance)
            objects_map['fixed_wall 4'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (8, 21)
            wall_instance.wh = (12, 38)
            objects.append(wall_instance)
            objects_map['fixed_wall 5'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (140, 101)
            wall_instance.wh = (20, 38)
            objects.append(wall_instance)
            objects_map['fixed_wall 6'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (28, 101)
            wall_instance.wh = (104, 38)
            objects.append(wall_instance)
            objects_map['fixed_wall 7'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (8, 101)
            wall_instance.wh = (12, 38)
            objects.append(wall_instance)
            objects_map['fixed_wall 8'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (140, 61)
            wall_instance.wh = (20, 37)
            objects.append(wall_instance)
            objects_map['fixed_wall 9'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (120, 61)
            wall_instance.wh = (12, 37)
            objects.append(wall_instance)
            objects_map['fixed_wall 10'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (28, 61)
            wall_instance.wh = (12, 37)
            objects.append(wall_instance)
            objects_map['fixed_wall 11'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (8, 61)
            wall_instance.wh = (12, 37)
            objects.append(wall_instance)
            objects_map['fixed_wall 12'] = wall_instance
            number_of_walls = 13
            i = 0
            while(objects_map.get(f"fixed wall {number_of_walls + i}")!= None):
                objects_map.pop(f"fixed wall {number_of_walls + i}")
                i += 1
        elif ram_state[28] == 6:
            wall_instance = Wall()
            wall_instance.xy = (140, 21)
            wall_instance.wh = (20, 38)
            objects.append(wall_instance)
            objects_map['fixed_wall 0'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (28, 21)
            wall_instance.wh = (104, 38)
            objects.append(wall_instance)
            objects_map['fixed_wall 1'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (8, 21)
            wall_instance.wh = (12, 38)
            objects.append(wall_instance)
            objects_map['fixed_wall 2'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (112, 101)
            wall_instance.wh = (48, 38)
            objects.append(wall_instance)
            objects_map['fixed_wall 3'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (8, 101)
            wall_instance.wh = (40, 38)
            objects.append(wall_instance)
            objects_map['fixed_wall 4'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (144, 61)
            wall_instance.wh = (16, 37)
            objects.append(wall_instance)
            objects_map['fixed_wall 5'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (8, 61)
            wall_instance.wh = (8, 37)
            objects.append(wall_instance)
            objects_map['fixed_wall 6'] = wall_instance
            number_of_walls = 7
            i = 0
            while(objects_map.get(f"fixed wall {number_of_walls + i}")!= None):
                objects_map.pop(f"fixed wall {number_of_walls + i}")
                i += 1
        elif ram_state[28] == 7:
            wall_instance = Wall()
            wall_instance.xy = (112, 21)
            wall_instance.wh = (48, 38)
            objects.append(wall_instance)
            objects_map['fixed_wall 0'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (8, 21)
            wall_instance.wh = (40, 38)
            objects.append(wall_instance)
            objects_map['fixed_wall 1'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (144, 101)
            wall_instance.wh = (16, 38)
            objects.append(wall_instance)
            objects_map['fixed_wall 2'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (8, 101)
            wall_instance.wh = (8, 38)
            objects.append(wall_instance)
            objects_map['fixed_wall 3'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (88, 61)
            wall_instance.wh = (72, 37)
            objects.append(wall_instance)
            objects_map['fixed_wall 4'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (8, 61)
            wall_instance.wh = (64, 37)
            objects.append(wall_instance)
            objects_map['fixed_wall 5'] = wall_instance
            number_of_walls = 6
            i = 0
            while(objects_map.get(f"fixed wall {number_of_walls + i}")!= None):
                objects_map.pop(f"fixed wall {number_of_walls + i}")
                i += 1
        elif ram_state[28] == 8:
            wall_instance = Wall()
            wall_instance.xy = (144, 21)
            wall_instance.wh = (16, 38)
            objects.append(wall_instance)
            objects_map['fixed_wall 0'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (8, 21)
            wall_instance.wh = (8, 38)
            objects.append(wall_instance)
            objects_map['fixed_wall 1'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (144, 101)
            wall_instance.wh = (16, 38)
            objects.append(wall_instance)
            objects_map['fixed_wall 2'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (8, 101)
            wall_instance.wh = (8, 38)
            objects.append(wall_instance)
            objects_map['fixed_wall 3'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (104, 61)
            wall_instance.wh = (56, 37)
            objects.append(wall_instance)
            objects_map['fixed_wall 4'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (72, 61)
            wall_instance.wh = (16, 37)
            objects.append(wall_instance)
            objects_map['fixed_wall 5'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (8, 61)
            wall_instance.wh = (48, 37)
            objects.append(wall_instance)
            objects_map['fixed_wall 6'] = wall_instance
            number_of_walls = 7
            i = 0
            while(objects_map.get(f"fixed wall {number_of_walls + i}")!= None):
                objects_map.pop(f"fixed wall {number_of_walls + i}")
                i += 1
        elif ram_state[28] == 9:
            wall_instance = Wall()
            wall_instance.xy = (144, 21)
            wall_instance.wh = (16, 38)
            objects.append(wall_instance)
            objects_map['fixed_wall 0'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (8, 21)
            wall_instance.wh = (8, 38)
            objects.append(wall_instance)
            objects_map['fixed_wall 1'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (112, 101)
            wall_instance.wh = (48, 38)
            objects.append(wall_instance)
            objects_map['fixed_wall 2'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (8, 101)
            wall_instance.wh = (40, 38)
            objects.append(wall_instance)
            objects_map['fixed_wall 3'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (88, 61)
            wall_instance.wh = (72, 37)
            objects.append(wall_instance)
            objects_map['fixed_wall 4'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (8, 61)
            wall_instance.wh = (64, 37)
            objects.append(wall_instance)
            objects_map['fixed_wall 5'] = wall_instance
            number_of_walls = 6
            i = 0
            while(objects_map.get(f"fixed wall {number_of_walls + i}")!= None):
                objects_map.pop(f"fixed wall {number_of_walls + i}")
                i += 1
        elif ram_state[28] == 10:
            wall_instance = Wall()
            wall_instance.xy = (112, 21)
            wall_instance.wh = (48, 38)
            objects.append(wall_instance)
            objects_map['fixed_wall 0'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (8, 21)
            wall_instance.wh = (40, 38)
            objects.append(wall_instance)
            objects_map['fixed_wall 1'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (104, 61)
            wall_instance.wh = (16, 37)
            objects.append(wall_instance)
            objects_map['fixed_wall 2'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (72, 61)
            wall_instance.wh = (16, 37)
            objects.append(wall_instance)
            objects_map['fixed_wall 3'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (40, 61)
            wall_instance.wh = (16, 37)
            objects.append(wall_instance)
            objects_map['fixed_wall 4'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (136, 101)
            wall_instance.wh = (24, 38)
            objects.append(wall_instance)
            objects_map['fixed_wall 5'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (68, 101)
            wall_instance.wh = (24, 38)
            objects.append(wall_instance)
            objects_map['fixed_wall 6'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (8, 101)
            wall_instance.wh = (16, 38)
            objects.append(wall_instance)
            objects_map['fixed_wall 7'] = wall_instance
            number_of_walls = 8
            i = 0
            while(objects_map.get(f"fixed wall {number_of_walls + i}")!= None):
                objects_map.pop(f"fixed wall {number_of_walls + i}")
                i += 1
        elif ram_state[28] == 11:
            wall_instance = Wall()
            wall_instance.xy = (8, 21)
            wall_instance.wh = (152, 38)
            objects.append(wall_instance)
            objects_map['fixed_wall 0'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (128, 101)
            wall_instance.wh = (32, 38)
            objects.append(wall_instance)
            objects_map['fixed_wall 1'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (72, 101)
            wall_instance.wh = (16, 38)
            objects.append(wall_instance)
            objects_map['fixed_wall 2'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (8, 101)
            wall_instance.wh = (24, 38)
            objects.append(wall_instance)
            objects_map['fixed_wall 3'] = wall_instance
            number_of_walls = 4
            i = 0
            while(objects_map.get(f"fixed wall {number_of_walls + i}")!= None):
                objects_map.pop(f"fixed wall {number_of_walls + i}")
                i += 1
        elif ram_state[28] == 12:
            wall_instance = Wall()
            wall_instance.xy = (8, 21)
            wall_instance.wh = (152, 38)
            objects.append(wall_instance)
            objects_map['fixed_wall 0'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (136, 101)
            wall_instance.wh = (24, 38)
            objects.append(wall_instance)
            objects_map['fixed_wall 1'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (8, 101)
            wall_instance.wh = (16, 38)
            objects.append(wall_instance)
            objects_map['fixed_wall 2'] = wall_instance
            number_of_walls = 3
            i = 0
            while(objects_map.get(f"fixed wall {number_of_walls + i}")!= None):
                objects_map.pop(f"fixed wall {number_of_walls + i}")
                i += 1
        elif ram_state[28] == 13:
            wall_instance = Wall()
            wall_instance.xy = (8, 21)
            wall_instance.wh = (152, 38)
            objects.append(wall_instance)
            objects_map['fixed_wall 0'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (112, 101)
            wall_instance.wh = (48, 38)
            objects.append(wall_instance)
            objects_map['fixed_wall 1'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (64, 101)
            wall_instance.wh = (32, 38)
            objects.append(wall_instance)
            objects_map['fixed_wall 2'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (8, 101)
            wall_instance.wh = (40, 38)
            objects.append(wall_instance)
            objects_map['fixed_wall 3'] = wall_instance
            number_of_walls = 4
            i = 0
            while(objects_map.get(f"fixed wall {number_of_walls + i}")!= None):
                objects_map.pop(f"fixed wall {number_of_walls + i}")
                i += 1
        elif ram_state[28] == 14:
            wall_instance = Wall()
            wall_instance.xy = (8, 21)
            wall_instance.wh = (152, 38)
            objects.append(wall_instance)
            objects_map['fixed_wall 0'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (136, 101)
            wall_instance.wh = (24, 38)
            objects.append(wall_instance)
            objects_map['fixed_wall 1'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (48, 101)
            wall_instance.wh = (64, 38)
            objects.append(wall_instance)
            objects_map['fixed_wall 2'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (8, 101)
            wall_instance.wh = (16, 38)
            objects.append(wall_instance)
            objects_map['fixed_wall 3'] = wall_instance
            number_of_walls = 4
            i = 0
            while(objects_map.get(f"fixed wall {number_of_walls + i}")!= None):
                objects_map.pop(f"fixed wall {number_of_walls + i}")
                i += 1
        elif ram_state[28] == 15:
            wall_instance = Wall()
            wall_instance.xy = (8, 21)
            wall_instance.wh = (152, 38)
            objects.append(wall_instance)
            objects_map['fixed_wall 0'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (8, 101)
            wall_instance.wh = (152, 38)
            objects.append(wall_instance)
            objects_map['fixed_wall 1'] = wall_instance
            number_of_walls = 2
            i = 0
            while(objects_map.get(f"fixed wall {number_of_walls + i}")!= None):
                objects_map.pop(f"fixed wall {number_of_walls + i}")
                i += 1

    elif ram_state[117] == 11:
        if ram_state[28] == 0:
            wall_instance = Wall()
            wall_instance.xy = (136, 21)
            wall_instance.wh = (24, 38)
            objects.append(wall_instance)
            objects_map['fixed_wall 0'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (8, 21)
            wall_instance.wh = (16, 38)
            objects.append(wall_instance)
            objects_map['fixed_wall 1'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (88, 101)
            wall_instance.wh = (72, 38)
            objects.append(wall_instance)
            objects_map['fixed_wall 2'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (8, 101)
            wall_instance.wh = (64, 38)
            objects.append(wall_instance)
            objects_map['fixed_wall 3'] = wall_instance
            number_of_walls = 4
            i = 0
            while(objects_map.get(f"fixed wall {number_of_walls + i}")!= None):
                objects_map.pop(f"fixed wall {number_of_walls + i}")
                i += 1
        elif ram_state[28] == 1:
            wall_instance = Wall()
            wall_instance.xy = (88, 21)
            wall_instance.wh = (72, 38)
            objects.append(wall_instance)
            objects_map['fixed_wall 0'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (8, 21)
            wall_instance.wh = (64, 38)
            objects.append(wall_instance)
            objects_map['fixed_wall 1'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (132, 101)
            wall_instance.wh = (28, 38)
            objects.append(wall_instance)
            objects_map['fixed_wall 2'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (36, 101)
            wall_instance.wh = (88, 38)
            objects.append(wall_instance)
            objects_map['fixed_wall 3'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (8, 101)
            wall_instance.wh = (20, 38)
            objects.append(wall_instance)
            objects_map['fixed_wall 4'] = wall_instance
            number_of_walls = 5
            i = 0
            while(objects_map.get(f"fixed wall {number_of_walls + i}")!= None):
                objects_map.pop(f"fixed wall {number_of_walls + i}")
                i += 1
        elif ram_state[28] == 2:
            wall_instance = Wall()
            wall_instance.xy = (132, 21)
            wall_instance.wh = (28, 38)
            objects.append(wall_instance)
            objects_map['fixed_wall 0'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (36, 21)
            wall_instance.wh = (88, 38)
            objects.append(wall_instance)
            objects_map['fixed_wall 1'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (8, 21)
            wall_instance.wh = (20, 38)
            objects.append(wall_instance)
            objects_map['fixed_wall 2'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (8, 101)
            wall_instance.wh = (152, 38)
            objects.append(wall_instance)
            objects_map['fixed_wall 3'] = wall_instance
            number_of_walls = 4
            i = 0
            while(objects_map.get(f"fixed wall {number_of_walls + i}")!= None):
                objects_map.pop(f"fixed wall {number_of_walls + i}")
                i += 1
        elif ram_state[28] == 3:
            wall_instance = Wall()
            wall_instance.xy = (8, 21)
            wall_instance.wh = (152, 38)
            objects.append(wall_instance)
            objects_map['fixed_wall 0'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (120, 101)
            wall_instance.wh = (40, 38)
            objects.append(wall_instance)
            objects_map['fixed_wall 1'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (48, 101)
            wall_instance.wh = (64, 38)
            objects.append(wall_instance)
            objects_map['fixed_wall 2'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (8, 101)
            wall_instance.wh = (32, 38)
            objects.append(wall_instance)
            objects_map['fixed_wall 3'] = wall_instance
            number_of_walls = 4
            i = 0
            while(objects_map.get(f"fixed wall {number_of_walls + i}")!= None):
                objects_map.pop(f"fixed wall {number_of_walls + i}")
                i += 1
        elif ram_state[28] == 4:
            wall_instance = Wall()
            wall_instance.xy = (120, 21)
            wall_instance.wh = (40, 38)
            objects.append(wall_instance)
            objects_map['fixed_wall 0'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (48, 21)
            wall_instance.wh = (64, 38)
            objects.append(wall_instance)
            objects_map['fixed_wall 1'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (8, 21)
            wall_instance.wh = (32, 38)
            objects.append(wall_instance)
            objects_map['fixed_wall 2'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (88, 101)
            wall_instance.wh = (72, 38)
            objects.append(wall_instance)
            objects_map['fixed_wall 3'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (8, 101)
            wall_instance.wh = (64, 38)
            objects.append(wall_instance)
            objects_map['fixed_wall 4'] = wall_instance
            number_of_walls = 5
            i = 0
            while(objects_map.get(f"fixed wall {number_of_walls + i}")!= None):
                objects_map.pop(f"fixed wall {number_of_walls + i}")
                i += 1
        elif ram_state[28] == 5:
            wall_instance = Wall()
            wall_instance.xy = (88, 21)
            wall_instance.wh = (72, 38)
            objects.append(wall_instance)
            objects_map['fixed_wall 0'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (8, 21)
            wall_instance.wh = (64, 38)
            objects.append(wall_instance)
            objects_map['fixed_wall 1'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (144, 101)
            wall_instance.wh = (16, 38)
            objects.append(wall_instance)
            objects_map['fixed_wall 2'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (48, 101)
            wall_instance.wh = (64, 38)
            objects.append(wall_instance)
            objects_map['fixed_wall 3'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (8, 101)
            wall_instance.wh = (8, 38)
            objects.append(wall_instance)
            objects_map['fixed_wall 4'] = wall_instance
            number_of_walls = 5
            i = 0
            while(objects_map.get(f"fixed wall {number_of_walls + i}")!= None):
                objects_map.pop(f"fixed wall {number_of_walls + i}")
                i += 1
        elif ram_state[28] == 6:
            wall_instance = Wall()
            wall_instance.xy = (144, 21)
            wall_instance.wh = (16, 38)
            objects.append(wall_instance)
            objects_map['fixed_wall 0'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (48, 21)
            wall_instance.wh = (64, 38)
            objects.append(wall_instance)
            objects_map['fixed_wall 1'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (8, 21)
            wall_instance.wh = (8, 38)
            objects.append(wall_instance)
            objects_map['fixed_wall 2'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (136, 101)
            wall_instance.wh = (24, 38)
            objects.append(wall_instance)
            objects_map['fixed_wall 3'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (8, 101)
            wall_instance.wh = (16, 38)
            objects.append(wall_instance)
            objects_map['fixed_wall 4'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (128, 61)
            wall_instance.wh = (32, 37)
            objects.append(wall_instance)
            objects_map['fixed_wall 5'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (40, 61)
            wall_instance.wh = (80, 37)
            objects.append(wall_instance)
            objects_map['fixed_wall 6'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (8, 61)
            wall_instance.wh = (24, 37)
            objects.append(wall_instance)
            objects_map['fixed_wall 7'] = wall_instance
            number_of_walls = 8
            i = 0
            while(objects_map.get(f"fixed wall {number_of_walls + i}")!= None):
                objects_map.pop(f"fixed wall {number_of_walls + i}")
                i += 1
        elif ram_state[28] == 7:
            wall_instance = Wall()
            wall_instance.xy = (136, 21)
            wall_instance.wh = (24, 38)
            objects.append(wall_instance)
            objects_map['fixed_wall 0'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (8, 21)
            wall_instance.wh = (16, 38)
            objects.append(wall_instance)
            objects_map['fixed_wall 1'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (8, 101)
            wall_instance.wh = (152, 38)
            objects.append(wall_instance)
            objects_map['fixed_wall 2'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (144, 61)
            wall_instance.wh = (16, 37)
            objects.append(wall_instance)
            objects_map['fixed_wall 3'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (8, 61)
            wall_instance.wh = (8, 37)
            objects.append(wall_instance)
            objects_map['fixed_wall 4'] = wall_instance
            number_of_walls = 5
            i = 0
            while(objects_map.get(f"fixed wall {number_of_walls + i}")!= None):
                objects_map.pop(f"fixed wall {number_of_walls + i}")
                i += 1
        elif ram_state[28] == 8:
            wall_instance = Wall()
            wall_instance.xy = (8, 21)
            wall_instance.wh = (152, 38)
            objects.append(wall_instance)
            objects_map['fixed_wall 0'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (112, 101)
            wall_instance.wh = (48, 38)
            objects.append(wall_instance)
            objects_map['fixed_wall 1'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (8, 101)
            wall_instance.wh = (40, 38)
            objects.append(wall_instance)
            objects_map['fixed_wall 2'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (144, 61)
            wall_instance.wh = (16, 37)
            objects.append(wall_instance)
            objects_map['fixed_wall 3'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (60, 61)
            wall_instance.wh = (40, 37)
            objects.append(wall_instance)
            objects_map['fixed_wall 4'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (8, 61)
            wall_instance.wh = (8, 37)
            objects.append(wall_instance)
            objects_map['fixed_wall 5'] = wall_instance
            number_of_walls = 6
            i = 0
            while(objects_map.get(f"fixed wall {number_of_walls + i}")!= None):
                objects_map.pop(f"fixed wall {number_of_walls + i}")
                i += 1
        elif ram_state[28] == 9:
            wall_instance = Wall()
            wall_instance.xy = (112, 21)
            wall_instance.wh = (48, 38)
            objects.append(wall_instance)
            objects_map['fixed_wall 0'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (8, 21)
            wall_instance.wh = (40, 38)
            objects.append(wall_instance)
            objects_map['fixed_wall 1'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (112, 101)
            wall_instance.wh = (48, 38)
            objects.append(wall_instance)
            objects_map['fixed_wall 2'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (8, 101)
            wall_instance.wh = (40, 38)
            objects.append(wall_instance)
            objects_map['fixed_wall 3'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (144, 61)
            wall_instance.wh = (16, 37)
            objects.append(wall_instance)
            objects_map['fixed_wall 4'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (56, 61)
            wall_instance.wh = (48, 37)
            objects.append(wall_instance)
            objects_map['fixed_wall 5'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (8, 61)
            wall_instance.wh = (8, 37)
            objects.append(wall_instance)
            objects_map['fixed_wall 6'] = wall_instance
            number_of_walls = 7
            i = 0
            while(objects_map.get(f"fixed wall {number_of_walls + i}")!= None):
                objects_map.pop(f"fixed wall {number_of_walls + i}")
                i += 1
        elif ram_state[28] == 10:
            wall_instance = Wall()
            wall_instance.xy = (112, 21)
            wall_instance.wh = (48, 38)
            objects.append(wall_instance)
            objects_map['fixed_wall 0'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (8, 21)
            wall_instance.wh = (40, 38)
            objects.append(wall_instance)
            objects_map['fixed_wall 1'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (136, 101)
            wall_instance.wh = (24, 38)
            objects.append(wall_instance)
            objects_map['fixed_wall 2'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (68, 101)
            wall_instance.wh = (24, 38)
            objects.append(wall_instance)
            objects_map['fixed_wall 3'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (8, 101)
            wall_instance.wh = (16, 38)
            objects.append(wall_instance)
            objects_map['fixed_wall 4'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (72, 61)
            wall_instance.wh = (16, 37)
            objects.append(wall_instance)
            objects_map['fixed_wall 5'] = wall_instance
            number_of_walls = 6
            i = 0
            while(objects_map.get(f"fixed wall {number_of_walls + i}")!= None):
                objects_map.pop(f"fixed wall {number_of_walls + i}")
                i += 1
        elif ram_state[28] == 11:
            wall_instance = Wall()
            wall_instance.xy = (8, 21)
            wall_instance.wh = (152, 38)
            objects.append(wall_instance)
            objects_map['fixed_wall 0'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (144, 101)
            wall_instance.wh = (16, 38)
            objects.append(wall_instance)
            objects_map['fixed_wall 1'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (68, 101)
            wall_instance.wh = (24, 38)
            objects.append(wall_instance)
            objects_map['fixed_wall 2'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (8, 101)
            wall_instance.wh = (8, 38)
            objects.append(wall_instance)
            objects_map['fixed_wall 3'] = wall_instance
            number_of_walls = 4
            i = 0
            while(objects_map.get(f"fixed wall {number_of_walls + i}")!= None):
                objects_map.pop(f"fixed wall {number_of_walls + i}")
                i += 1
        elif ram_state[28] == 12:
            wall_instance = Wall()
            wall_instance.xy = (8, 21)
            wall_instance.wh = (152, 38)
            objects.append(wall_instance)
            objects_map['fixed_wall 0'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (72, 61)
            wall_instance.wh = (16, 37)
            objects.append(wall_instance)
            objects_map['fixed_wall 1'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (112, 101)
            wall_instance.wh = (48, 38)
            objects.append(wall_instance)
            objects_map['fixed_wall 2'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (8, 101)
            wall_instance.wh = (40, 38)
            objects.append(wall_instance)
            objects_map['fixed_wall 3'] = wall_instance
            number_of_walls = 4
            i = 0
            while(objects_map.get(f"fixed wall {number_of_walls + i}")!= None):
                objects_map.pop(f"fixed wall {number_of_walls + i}")
                i += 1
        elif ram_state[28] == 13:
            wall_instance = Wall()
            wall_instance.xy = (8, 21)
            wall_instance.wh = (152, 38)
            objects.append(wall_instance)
            objects_map['fixed_wall 0'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (144, 101)
            wall_instance.wh = (16, 38)
            objects.append(wall_instance)
            objects_map['fixed_wall 1'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (72, 101)
            wall_instance.wh = (16, 38)
            objects.append(wall_instance)
            objects_map['fixed_wall 2'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (8, 101)
            wall_instance.wh = (8, 38)
            objects.append(wall_instance)
            objects_map['fixed_wall 3'] = wall_instance
            number_of_walls = 4
            i = 0
            while(objects_map.get(f"fixed wall {number_of_walls + i}")!= None):
                objects_map.pop(f"fixed wall {number_of_walls + i}")
                i += 1
        elif ram_state[28] == 14:
            wall_instance = Wall()
            wall_instance.xy = (8, 21)
            wall_instance.wh = (152, 38)
            objects.append(wall_instance)
            objects_map['fixed_wall 0'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (136, 101)
            wall_instance.wh = (24, 38)
            objects.append(wall_instance)
            objects_map['fixed_wall 1'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (8, 101)
            wall_instance.wh = (16, 38)
            objects.append(wall_instance)
            objects_map['fixed_wall 2'] = wall_instance
            number_of_walls = 3
            i = 0
            while(objects_map.get(f"fixed wall {number_of_walls + i}")!= None):
                objects_map.pop(f"fixed wall {number_of_walls + i}")
                i += 1
        elif ram_state[28] == 15:
            wall_instance = Wall()
            wall_instance.xy = (8, 21)
            wall_instance.wh = (152, 38)
            objects.append(wall_instance)
            objects_map['fixed_wall 0'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (112, 101)
            wall_instance.wh = (48, 38)
            objects.append(wall_instance)
            objects_map['fixed_wall 1'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (8, 101)
            wall_instance.wh = (40, 38)
            objects.append(wall_instance)
            objects_map['fixed_wall 2'] = wall_instance
            number_of_walls = 3
            i = 0
            while(objects_map.get(f"fixed wall {number_of_walls + i}")!= None):
                objects_map.pop(f"fixed wall {number_of_walls + i}")
                i += 1

    elif ram_state[117] == 12:
        if ram_state[28] == 0:
            wall_instance = Wall()
            wall_instance.xy = (136, 21)
            wall_instance.wh = (24, 38)
            objects.append(wall_instance)
            objects_map['fixed_wall 0'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (8, 21)
            wall_instance.wh = (16, 38)
            objects.append(wall_instance)
            objects_map['fixed_wall 1'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (88, 101)
            wall_instance.wh = (72, 38)
            objects.append(wall_instance)
            objects_map['fixed_wall 2'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (8, 101)
            wall_instance.wh = (64, 38)
            objects.append(wall_instance)
            objects_map['fixed_wall 3'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (144, 61)
            wall_instance.wh = (16, 37)
            objects.append(wall_instance)
            objects_map['fixed_wall 4'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (8, 61)
            wall_instance.wh = (8, 37)
            objects.append(wall_instance)
            objects_map['fixed_wall 5'] = wall_instance
            number_of_walls = 6
            i = 0
            while(objects_map.get(f"fixed wall {number_of_walls + i}")!= None):
                objects_map.pop(f"fixed wall {number_of_walls + i}")
                i += 1
        elif ram_state[28] == 1:
            wall_instance = Wall()
            wall_instance.xy = (88, 21)
            wall_instance.wh = (72, 38)
            objects.append(wall_instance)
            objects_map['fixed_wall 0'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (8, 21)
            wall_instance.wh = (64, 38)
            objects.append(wall_instance)
            objects_map['fixed_wall 1'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (140, 101)
            wall_instance.wh = (20, 38)
            objects.append(wall_instance)
            objects_map['fixed_wall 2'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (116, 101)
            wall_instance.wh = (16, 38)
            objects.append(wall_instance)
            objects_map['fixed_wall 3'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (88, 101)
            wall_instance.wh = (20, 38)
            objects.append(wall_instance)
            objects_map['fixed_wall 4'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (52, 101)
            wall_instance.wh = (20, 38)
            objects.append(wall_instance)
            objects_map['fixed_wall 5'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (28, 101)
            wall_instance.wh = (16, 38)
            objects.append(wall_instance)
            objects_map['fixed_wall 6'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (8, 101)
            wall_instance.wh = (12, 38)
            objects.append(wall_instance)
            objects_map['fixed_wall 7'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (144, 61)
            wall_instance.wh = (16, 37)
            objects.append(wall_instance)
            objects_map['fixed_wall 8'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (92, 61)
            wall_instance.wh = (12, 37)
            objects.append(wall_instance)
            objects_map['fixed_wall 9'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (56, 61)
            wall_instance.wh = (12, 37)
            objects.append(wall_instance)
            objects_map['fixed_wall 10'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (8, 61)
            wall_instance.wh = (8, 37)
            objects.append(wall_instance)
            objects_map['fixed_wall 11'] = wall_instance
            number_of_walls = 12
            i = 0
            while(objects_map.get(f"fixed wall {number_of_walls + i}")!= None):
                objects_map.pop(f"fixed wall {number_of_walls + i}")
                i += 1
        elif ram_state[28] == 2:
            wall_instance = Wall()
            wall_instance.xy = (140, 21)
            wall_instance.wh = (20, 38)
            objects.append(wall_instance)
            objects_map['fixed_wall 0'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (116, 21)
            wall_instance.wh = (16, 38)
            objects.append(wall_instance)
            objects_map['fixed_wall 1'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (88, 21)
            wall_instance.wh = (20, 38)
            objects.append(wall_instance)
            objects_map['fixed_wall 2'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (52, 21)
            wall_instance.wh = (20, 38)
            objects.append(wall_instance)
            objects_map['fixed_wall 3'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (28, 21)
            wall_instance.wh = (16, 38)
            objects.append(wall_instance)
            objects_map['fixed_wall 4'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (8, 21)
            wall_instance.wh = (12, 38)
            objects.append(wall_instance)
            objects_map['fixed_wall 5'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (144, 101)
            wall_instance.wh = (16, 38)
            objects.append(wall_instance)
            objects_map['fixed_wall 6'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (32, 101)
            wall_instance.wh = (96, 38)
            objects.append(wall_instance)
            objects_map['fixed_wall 7'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (8, 101)
            wall_instance.wh = (8, 38)
            objects.append(wall_instance)
            objects_map['fixed_wall 8'] = wall_instance
            number_of_walls = 9
            i = 0
            while(objects_map.get(f"fixed wall {number_of_walls + i}")!= None):
                objects_map.pop(f"fixed wall {number_of_walls + i}")
                i += 1
        elif ram_state[28] == 3:
            wall_instance = Wall()
            wall_instance.xy = (144, 21)
            wall_instance.wh = (16, 38)
            objects.append(wall_instance)
            objects_map['fixed_wall 0'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (32, 21)
            wall_instance.wh = (96, 38)
            objects.append(wall_instance)
            objects_map['fixed_wall 1'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (8, 21)
            wall_instance.wh = (8, 38)
            objects.append(wall_instance)
            objects_map['fixed_wall 2'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (120, 101)
            wall_instance.wh = (40, 38)
            objects.append(wall_instance)
            objects_map['fixed_wall 3'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (48, 101)
            wall_instance.wh = (64, 38)
            objects.append(wall_instance)
            objects_map['fixed_wall 4'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (8, 101)
            wall_instance.wh = (32, 38)
            objects.append(wall_instance)
            objects_map['fixed_wall 5'] = wall_instance
            number_of_walls = 6
            i = 0
            while(objects_map.get(f"fixed wall {number_of_walls + i}")!= None):
                objects_map.pop(f"fixed wall {number_of_walls + i}")
                i += 1
        elif ram_state[28] == 4:
            wall_instance = Wall()
            wall_instance.xy = (120, 21)
            wall_instance.wh = (40, 38)
            objects.append(wall_instance)
            objects_map['fixed_wall 0'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (48, 21)
            wall_instance.wh = (64, 38)
            objects.append(wall_instance)
            objects_map['fixed_wall 1'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (8, 21)
            wall_instance.wh = (32, 38)
            objects.append(wall_instance)
            objects_map['fixed_wall 2'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (144, 101)
            wall_instance.wh = (16, 38)
            objects.append(wall_instance)
            objects_map['fixed_wall 3'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (40, 101)
            wall_instance.wh = (80, 38)
            objects.append(wall_instance)
            objects_map['fixed_wall 4'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (8, 101)
            wall_instance.wh = (8, 38)
            objects.append(wall_instance)
            objects_map['fixed_wall 5'] = wall_instance
            number_of_walls = 6
            i = 0
            while(objects_map.get(f"fixed wall {number_of_walls + i}")!= None):
                objects_map.pop(f"fixed wall {number_of_walls + i}")
                i += 1
        elif ram_state[28] == 5:
            wall_instance = Wall()
            wall_instance.xy = (144, 21)
            wall_instance.wh = (16, 38)
            objects.append(wall_instance)
            objects_map['fixed_wall 0'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (40, 21)
            wall_instance.wh = (80, 38)
            objects.append(wall_instance)
            objects_map['fixed_wall 1'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (8, 21)
            wall_instance.wh = (8, 38)
            objects.append(wall_instance)
            objects_map['fixed_wall 2'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (144, 101)
            wall_instance.wh = (16, 38)
            objects.append(wall_instance)
            objects_map['fixed_wall 3'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (32, 101)
            wall_instance.wh = (96, 38)
            objects.append(wall_instance)
            objects_map['fixed_wall 4'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (8, 101)
            wall_instance.wh = (8, 38)
            objects.append(wall_instance)
            objects_map['fixed_wall 5'] = wall_instance
            number_of_walls = 6
            i = 0
            while(objects_map.get(f"fixed wall {number_of_walls + i}")!= None):
                objects_map.pop(f"fixed wall {number_of_walls + i}")
                i += 1
        elif ram_state[28] == 6:
            wall_instance = Wall()
            wall_instance.xy = (144, 21)
            wall_instance.wh = (16, 38)
            objects.append(wall_instance)
            objects_map['fixed_wall 0'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (32, 21)
            wall_instance.wh = (96, 38)
            objects.append(wall_instance)
            objects_map['fixed_wall 1'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (8, 21)
            wall_instance.wh = (8, 38)
            objects.append(wall_instance)
            objects_map['fixed_wall 2'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (8, 101)
            wall_instance.wh = (152, 38)
            objects.append(wall_instance)
            objects_map['fixed_wall 3'] = wall_instance
            number_of_walls = 4
            i = 0
            while(objects_map.get(f"fixed wall {number_of_walls + i}")!= None):
                objects_map.pop(f"fixed wall {number_of_walls + i}")
                i += 1
        elif ram_state[28] == 7:
            wall_instance = Wall()
            wall_instance.xy = (8, 21)
            wall_instance.wh = (152, 38)
            objects.append(wall_instance)
            objects_map['fixed_wall 0'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (88, 101)
            wall_instance.wh = (72, 38)
            objects.append(wall_instance)
            objects_map['fixed_wall 1'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (8, 101)
            wall_instance.wh = (64, 38)
            objects.append(wall_instance)
            objects_map['fixed_wall 2'] = wall_instance
            number_of_walls = 3
            i = 0
            while(objects_map.get(f"fixed wall {number_of_walls + i}")!= None):
                objects_map.pop(f"fixed wall {number_of_walls + i}")
                i += 1
        elif ram_state[28] == 8:
            wall_instance = Wall()
            wall_instance.xy = (88, 21)
            wall_instance.wh = (72, 38)
            objects.append(wall_instance)
            objects_map['fixed_wall 0'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (8, 21)
            wall_instance.wh = (64, 38)
            objects.append(wall_instance)
            objects_map['fixed_wall 1'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (144, 61)
            wall_instance.wh = (16, 37)
            objects.append(wall_instance)
            objects_map['fixed_wall 2'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (8, 61)
            wall_instance.wh = (8, 37)
            objects.append(wall_instance)
            objects_map['fixed_wall 3'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (116, 101)
            wall_instance.wh = (44, 38)
            objects.append(wall_instance)
            objects_map['fixed_wall 4'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (52, 101)
            wall_instance.wh = (56, 38)
            objects.append(wall_instance)
            objects_map['fixed_wall 5'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (8, 101)
            wall_instance.wh = (36, 38)
            objects.append(wall_instance)
            objects_map['fixed_wall 6'] = wall_instance
            number_of_walls = 7
            i = 0
            while(objects_map.get(f"fixed wall {number_of_walls + i}")!= None):
                objects_map.pop(f"fixed wall {number_of_walls + i}")
                i += 1
        elif ram_state[28] == 9:
            wall_instance = Wall()
            wall_instance.xy = (116, 21)
            wall_instance.wh = (44, 38)
            objects.append(wall_instance)
            objects_map['fixed_wall 0'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (52, 21)
            wall_instance.wh = (56, 38)
            objects.append(wall_instance)
            objects_map['fixed_wall 1'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (8, 21)
            wall_instance.wh = (36, 38)
            objects.append(wall_instance)
            objects_map['fixed_wall 2'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (8, 101)
            wall_instance.wh = (152, 38)
            objects.append(wall_instance)
            objects_map['fixed_wall 3'] = wall_instance
            number_of_walls = 4
            i = 0
            while(objects_map.get(f"fixed wall {number_of_walls + i}")!= None):
                objects_map.pop(f"fixed wall {number_of_walls + i}")
                i += 1
        elif ram_state[28] == 10:
            wall_instance = Wall()
            wall_instance.xy = (8, 21)
            wall_instance.wh = (152, 38)
            objects.append(wall_instance)
            objects_map['fixed_wall 0'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (8, 101)
            wall_instance.wh = (152, 38)
            objects.append(wall_instance)
            objects_map['fixed_wall 1'] = wall_instance
            number_of_walls = 2
            i = 0
            while(objects_map.get(f"fixed wall {number_of_walls + i}")!= None):
                objects_map.pop(f"fixed wall {number_of_walls + i}")
                i += 1
        elif ram_state[28] == 11:
            wall_instance = Wall()
            wall_instance.xy = (8, 21)
            wall_instance.wh = (152, 38)
            objects.append(wall_instance)
            objects_map['fixed_wall 0'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (136, 101)
            wall_instance.wh = (24, 38)
            objects.append(wall_instance)
            objects_map['fixed_wall 1'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (68, 101)
            wall_instance.wh = (24, 38)
            objects.append(wall_instance)
            objects_map['fixed_wall 2'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (8, 101)
            wall_instance.wh = (16, 38)
            objects.append(wall_instance)
            objects_map['fixed_wall 3'] = wall_instance
            number_of_walls = 4
            i = 0
            while(objects_map.get(f"fixed wall {number_of_walls + i}")!= None):
                objects_map.pop(f"fixed wall {number_of_walls + i}")
                i += 1
        elif ram_state[28] == 12:
            wall_instance = Wall()
            wall_instance.xy = (8, 21)
            wall_instance.wh = (152, 38)
            objects.append(wall_instance)
            objects_map['fixed_wall 0'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (136, 101)
            wall_instance.wh = (24, 38)
            objects.append(wall_instance)
            objects_map['fixed_wall 1'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (8, 101)
            wall_instance.wh = (16, 38)
            objects.append(wall_instance)
            objects_map['fixed_wall 2'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (68, 61)
            wall_instance.wh = (24, 37)
            objects.append(wall_instance)
            objects_map['fixed_wall 3'] = wall_instance
            number_of_walls = 4
            i = 0
            while(objects_map.get(f"fixed wall {number_of_walls + i}")!= None):
                objects_map.pop(f"fixed wall {number_of_walls + i}")
                i += 1
        elif ram_state[28] == 13:
            wall_instance = Wall()
            wall_instance.xy = (8, 21)
            wall_instance.wh = (152, 38)
            objects.append(wall_instance)
            objects_map['fixed_wall 0'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (136, 101)
            wall_instance.wh = (24, 38)
            objects.append(wall_instance)
            objects_map['fixed_wall 1'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (72, 101)
            wall_instance.wh = (16, 38)
            objects.append(wall_instance)
            objects_map['fixed_wall 2'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (8, 101)
            wall_instance.wh = (16, 38)
            objects.append(wall_instance)
            objects_map['fixed_wall 3'] = wall_instance
            number_of_walls = 4
            i = 0
            while(objects_map.get(f"fixed wall {number_of_walls + i}")!= None):
                objects_map.pop(f"fixed wall {number_of_walls + i}")
                i += 1
        elif ram_state[28] == 14:
            wall_instance = Wall()
            wall_instance.xy = (8, 21)
            wall_instance.wh = (152, 38)
            objects.append(wall_instance)
            objects_map['fixed_wall 0'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (112, 101)
            wall_instance.wh = (48, 38)
            objects.append(wall_instance)
            objects_map['fixed_wall 1'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (64, 101)
            wall_instance.wh = (32, 38)
            objects.append(wall_instance)
            objects_map['fixed_wall 2'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (8, 101)
            wall_instance.wh = (40, 38)
            objects.append(wall_instance)
            objects_map['fixed_wall 3'] = wall_instance
            number_of_walls = 4
            i = 0
            while(objects_map.get(f"fixed wall {number_of_walls + i}")!= None):
                objects_map.pop(f"fixed wall {number_of_walls + i}")
                i += 1
        elif ram_state[28] == 15:
            wall_instance = Wall()
            wall_instance.xy = (8, 21)
            wall_instance.wh = (152, 38)
            objects.append(wall_instance)
            objects_map['fixed_wall 0'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (112, 101)
            wall_instance.wh = (48, 38)
            objects.append(wall_instance)
            objects_map['fixed_wall 1'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (8, 101)
            wall_instance.wh = (40, 38)
            objects.append(wall_instance)
            objects_map['fixed_wall 2'] = wall_instance
            number_of_walls = 3
            i = 0
            while(objects_map.get(f"fixed wall {number_of_walls + i}")!= None):
                objects_map.pop(f"fixed wall {number_of_walls + i}")
                i += 1

    elif ram_state[117] == 13:
        if ram_state[28] == 0:
            wall_instance = Wall()
            wall_instance.xy = (136, 21)
            wall_instance.wh = (24, 38)
            objects.append(wall_instance)
            objects_map['fixed_wall 0'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (8, 21)
            wall_instance.wh = (16, 38)
            objects.append(wall_instance)
            objects_map['fixed_wall 1'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (88, 101)
            wall_instance.wh = (72, 38)
            objects.append(wall_instance)
            objects_map['fixed_wall 2'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (8, 101)
            wall_instance.wh = (64, 38)
            objects.append(wall_instance)
            objects_map['fixed_wall 3'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (144, 61)
            wall_instance.wh = (16, 37)
            objects.append(wall_instance)
            objects_map['fixed_wall 4'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (8, 61)
            wall_instance.wh = (8, 37)
            objects.append(wall_instance)
            objects_map['fixed_wall 5'] = wall_instance
            number_of_walls = 6
            i = 0
            while(objects_map.get(f"fixed wall {number_of_walls + i}")!= None):
                objects_map.pop(f"fixed wall {number_of_walls + i}")
                i += 1
        elif ram_state[28] == 1:
            wall_instance = Wall()
            wall_instance.xy = (88, 21)
            wall_instance.wh = (72, 38)
            objects.append(wall_instance)
            objects_map['fixed_wall 0'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (8, 21)
            wall_instance.wh = (64, 38)
            objects.append(wall_instance)
            objects_map['fixed_wall 1'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (8, 101)
            wall_instance.wh = (152, 38)
            objects.append(wall_instance)
            objects_map['fixed_wall 2'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (80, 61)
            wall_instance.wh = (16, 37)
            objects.append(wall_instance)
            objects_map['fixed_wall 3'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (8, 61)
            wall_instance.wh = (8, 37)
            objects.append(wall_instance)
            objects_map['fixed_wall 4'] = wall_instance
            number_of_walls = 5
            i = 0
            while(objects_map.get(f"fixed wall {number_of_walls + i}")!= None):
                objects_map.pop(f"fixed wall {number_of_walls + i}")
                i += 1
        elif ram_state[28] == 2:
            wall_instance = Wall()
            wall_instance.xy = (8, 21)
            wall_instance.wh = (152, 38)
            objects.append(wall_instance)
            objects_map['fixed_wall 0'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (88, 101)
            wall_instance.wh = (72, 38)
            objects.append(wall_instance)
            objects_map['fixed_wall 1'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (8, 101)
            wall_instance.wh = (64, 38)
            objects.append(wall_instance)
            objects_map['fixed_wall 2'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (144, 61)
            wall_instance.wh = (16, 37)
            objects.append(wall_instance)
            objects_map['fixed_wall 3'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (8, 61)
            wall_instance.wh = (8, 37)
            objects.append(wall_instance)
            objects_map['fixed_wall 4'] = wall_instance
            number_of_walls = 5
            i = 0
            while(objects_map.get(f"fixed wall {number_of_walls + i}")!= None):
                objects_map.pop(f"fixed wall {number_of_walls + i}")
                i += 1
        elif ram_state[28] == 3:
            wall_instance = Wall()
            wall_instance.xy = (88, 21)
            wall_instance.wh = (72, 38)
            objects.append(wall_instance)
            objects_map['fixed_wall 0'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (8, 21)
            wall_instance.wh = (64, 38)
            objects.append(wall_instance)
            objects_map['fixed_wall 1'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (8, 101)
            wall_instance.wh = (152, 38)
            objects.append(wall_instance)
            objects_map['fixed_wall 2'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (144, 61)
            wall_instance.wh = (16, 37)
            objects.append(wall_instance)
            objects_map['fixed_wall 3'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (8, 61)
            wall_instance.wh = (8, 37)
            objects.append(wall_instance)
            objects_map['fixed_wall 4'] = wall_instance
            number_of_walls = 5
            i = 0
            while(objects_map.get(f"fixed wall {number_of_walls + i}")!= None):
                objects_map.pop(f"fixed wall {number_of_walls + i}")
                i += 1
        elif ram_state[28] == 4:
            wall_instance = Wall()
            wall_instance.xy = (8, 21)
            wall_instance.wh = (152, 38)
            objects.append(wall_instance)
            objects_map['fixed_wall 0'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (136, 101)
            wall_instance.wh = (24, 38)
            objects.append(wall_instance)
            objects_map['fixed_wall 1'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (88, 101)
            wall_instance.wh = (32, 38)
            objects.append(wall_instance)
            objects_map['fixed_wall 2'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (40, 101)
            wall_instance.wh = (32, 38)
            objects.append(wall_instance)
            objects_map['fixed_wall 3'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (8, 101)
            wall_instance.wh = (16, 38)
            objects.append(wall_instance)
            objects_map['fixed_wall 4'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (144, 61)
            wall_instance.wh = (16, 37)
            objects.append(wall_instance)
            objects_map['fixed_wall 5'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (8, 61)
            wall_instance.wh = (8, 37)
            objects.append(wall_instance)
            objects_map['fixed_wall 6'] = wall_instance
            number_of_walls = 7
            i = 0
            while(objects_map.get(f"fixed wall {number_of_walls + i}")!= None):
                objects_map.pop(f"fixed wall {number_of_walls + i}")
                i += 1
        elif ram_state[28] == 5:
            wall_instance = Wall()
            wall_instance.xy = (136, 21)
            wall_instance.wh = (24, 38)
            objects.append(wall_instance)
            objects_map['fixed_wall 0'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (88, 21)
            wall_instance.wh = (32, 38)
            objects.append(wall_instance)
            objects_map['fixed_wall 1'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (40, 21)
            wall_instance.wh = (32, 38)
            objects.append(wall_instance)
            objects_map['fixed_wall 2'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (8, 21)
            wall_instance.wh = (16, 38)
            objects.append(wall_instance)
            objects_map['fixed_wall 3'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (112, 101)
            wall_instance.wh = (48, 38)
            objects.append(wall_instance)
            objects_map['fixed_wall 4'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (8, 101)
            wall_instance.wh = (40, 38)
            objects.append(wall_instance)
            objects_map['fixed_wall 5'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (88, 61)
            wall_instance.wh = (72, 37)
            objects.append(wall_instance)
            objects_map['fixed_wall 6'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (8, 61)
            wall_instance.wh = (64, 37)
            objects.append(wall_instance)
            objects_map['fixed_wall 7'] = wall_instance
            number_of_walls = 8
            i = 0
            while(objects_map.get(f"fixed wall {number_of_walls + i}")!= None):
                objects_map.pop(f"fixed wall {number_of_walls + i}")
                i += 1
        elif ram_state[28] == 6:
            wall_instance = Wall()
            wall_instance.xy = (112, 21)
            wall_instance.wh = (48, 38)
            objects.append(wall_instance)
            objects_map['fixed_wall 0'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (8, 21)
            wall_instance.wh = (40, 38)
            objects.append(wall_instance)
            objects_map['fixed_wall 1'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (140, 101)
            wall_instance.wh = (20, 38)
            objects.append(wall_instance)
            objects_map['fixed_wall 2'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (44, 101)
            wall_instance.wh = (72, 38)
            objects.append(wall_instance)
            objects_map['fixed_wall 3'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (8, 101)
            wall_instance.wh = (12, 38)
            objects.append(wall_instance)
            objects_map['fixed_wall 4'] = wall_instance
            number_of_walls = 5
            i = 0
            while(objects_map.get(f"fixed wall {number_of_walls + i}")!= None):
                objects_map.pop(f"fixed wall {number_of_walls + i}")
                i += 1
        elif ram_state[28] == 7:
            wall_instance = Wall()
            wall_instance.xy = (140, 21)
            wall_instance.wh = (20, 38)
            objects.append(wall_instance)
            objects_map['fixed_wall 0'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (44, 21)
            wall_instance.wh = (72, 38)
            objects.append(wall_instance)
            objects_map['fixed_wall 1'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (8, 21)
            wall_instance.wh = (12, 38)
            objects.append(wall_instance)
            objects_map['fixed_wall 2'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (8, 101)
            wall_instance.wh = (152, 38)
            objects.append(wall_instance)
            objects_map['fixed_wall 3'] = wall_instance
            number_of_walls = 4
            i = 0
            while(objects_map.get(f"fixed wall {number_of_walls + i}")!= None):
                objects_map.pop(f"fixed wall {number_of_walls + i}")
                i += 1
        elif ram_state[28] == 8:
            wall_instance = Wall()
            wall_instance.xy = (8, 21)
            wall_instance.wh = (152, 38)
            objects.append(wall_instance)
            objects_map['fixed_wall 0'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (136, 101)
            wall_instance.wh = (24, 38)
            objects.append(wall_instance)
            objects_map['fixed_wall 1'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (52, 101)
            wall_instance.wh = (56, 38)
            objects.append(wall_instance)
            objects_map['fixed_wall 2'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (8, 101)
            wall_instance.wh = (16, 38)
            objects.append(wall_instance)
            objects_map['fixed_wall 3'] = wall_instance
            number_of_walls = 4
            i = 0
            while(objects_map.get(f"fixed wall {number_of_walls + i}")!= None):
                objects_map.pop(f"fixed wall {number_of_walls + i}")
                i += 1
        elif ram_state[28] == 9:
            wall_instance = Wall()
            wall_instance.xy = (136, 21)
            wall_instance.wh = (24, 38)
            objects.append(wall_instance)
            objects_map['fixed_wall 0'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (52, 21)
            wall_instance.wh = (56, 38)
            objects.append(wall_instance)
            objects_map['fixed_wall 1'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (8, 21)
            wall_instance.wh = (16, 38)
            objects.append(wall_instance)
            objects_map['fixed_wall 2'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (84, 101)
            wall_instance.wh = (76, 38)
            objects.append(wall_instance)
            objects_map['fixed_wall 3'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (8, 101)
            wall_instance.wh = (68, 38)
            objects.append(wall_instance)
            objects_map['fixed_wall 4'] = wall_instance
            number_of_walls = 5
            i = 0
            while(objects_map.get(f"fixed wall {number_of_walls + i}")!= None):
                objects_map.pop(f"fixed wall {number_of_walls + i}")
                i += 1
        elif ram_state[28] == 10:
            wall_instance = Wall()
            wall_instance.xy = (84, 21)
            wall_instance.wh = (76, 38)
            objects.append(wall_instance)
            objects_map['fixed_wall 0'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (8, 21)
            wall_instance.wh = (68, 38)
            objects.append(wall_instance)
            objects_map['fixed_wall 1'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (104, 61)
            wall_instance.wh = (16, 37)
            objects.append(wall_instance)
            objects_map['fixed_wall 2'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (40, 61)
            wall_instance.wh = (16, 37)
            objects.append(wall_instance)
            objects_map['fixed_wall 3'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (140, 101)
            wall_instance.wh = (20, 38)
            objects.append(wall_instance)
            objects_map['fixed_wall 4'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (8, 101)
            wall_instance.wh = (12, 38)
            objects.append(wall_instance)
            objects_map['fixed_wall 5'] = wall_instance
            number_of_walls = 6
            i = 0
            while(objects_map.get(f"fixed wall {number_of_walls + i}")!= None):
                objects_map.pop(f"fixed wall {number_of_walls + i}")
                i += 1
        elif ram_state[28] == 11:
            wall_instance = Wall()
            wall_instance.xy = (8, 21)
            wall_instance.wh = (152, 38)
            objects.append(wall_instance)
            objects_map['fixed_wall 0'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (136, 101)
            wall_instance.wh = (24, 38)
            objects.append(wall_instance)
            objects_map['fixed_wall 1'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (68, 101)
            wall_instance.wh = (24, 38)
            objects.append(wall_instance)
            objects_map['fixed_wall 2'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (8, 101)
            wall_instance.wh = (16, 38)
            objects.append(wall_instance)
            objects_map['fixed_wall 3'] = wall_instance
            number_of_walls = 4
            i = 0
            while(objects_map.get(f"fixed wall {number_of_walls + i}")!= None):
                objects_map.pop(f"fixed wall {number_of_walls + i}")
                i += 1
        elif ram_state[28] == 12:
            wall_instance = Wall()
            wall_instance.xy = (8, 21)
            wall_instance.wh = (152, 38)
            objects.append(wall_instance)
            objects_map['fixed_wall 0'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (136, 101)
            wall_instance.wh = (24, 38)
            objects.append(wall_instance)
            objects_map['fixed_wall 1'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (8, 101)
            wall_instance.wh = (16, 38)
            objects.append(wall_instance)
            objects_map['fixed_wall 2'] = wall_instance
            number_of_walls = 3
            i = 0
            while(objects_map.get(f"fixed wall {number_of_walls + i}")!= None):
                objects_map.pop(f"fixed wall {number_of_walls + i}")
                i += 1
        elif ram_state[28] == 13:
            wall_instance = Wall()
            wall_instance.xy = (8, 21)
            wall_instance.wh = (152, 38)
            objects.append(wall_instance)
            objects_map['fixed_wall 0'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (136, 101)
            wall_instance.wh = (24, 38)
            objects.append(wall_instance)
            objects_map['fixed_wall 1'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (72, 101)
            wall_instance.wh = (16, 38)
            objects.append(wall_instance)
            objects_map['fixed_wall 2'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (8, 101)
            wall_instance.wh = (16, 38)
            objects.append(wall_instance)
            objects_map['fixed_wall 3'] = wall_instance
            number_of_walls = 4
            i = 0
            while(objects_map.get(f"fixed wall {number_of_walls + i}")!= None):
                objects_map.pop(f"fixed wall {number_of_walls + i}")
                i += 1
        elif ram_state[28] == 14:
            wall_instance = Wall()
            wall_instance.xy = (8, 21)
            wall_instance.wh = (152, 38)
            objects.append(wall_instance)
            objects_map['fixed_wall 0'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (136, 101)
            wall_instance.wh = (24, 38)
            objects.append(wall_instance)
            objects_map['fixed_wall 1'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (96, 101)
            wall_instance.wh = (16, 38)
            objects.append(wall_instance)
            objects_map['fixed_wall 2'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (48, 101)
            wall_instance.wh = (16, 38)
            objects.append(wall_instance)
            objects_map['fixed_wall 3'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (8, 101)
            wall_instance.wh = (16, 38)
            objects.append(wall_instance)
            objects_map['fixed_wall 4'] = wall_instance
            number_of_walls = 5
            i = 0
            while(objects_map.get(f"fixed wall {number_of_walls + i}")!= None):
                objects_map.pop(f"fixed wall {number_of_walls + i}")
                i += 1
        elif ram_state[28] == 15:
            wall_instance = Wall()
            wall_instance.xy = (8, 21)
            wall_instance.wh = (152, 38)
            objects.append(wall_instance)
            objects_map['fixed_wall 0'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (112, 101)
            wall_instance.wh = (48, 38)
            objects.append(wall_instance)
            objects_map['fixed_wall 1'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (72, 101)
            wall_instance.wh = (16, 38)
            objects.append(wall_instance)
            objects_map['fixed_wall 2'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (8, 101)
            wall_instance.wh = (40, 38)
            objects.append(wall_instance)
            objects_map['fixed_wall 3'] = wall_instance
            number_of_walls = 4
            i = 0
            while(objects_map.get(f"fixed wall {number_of_walls + i}")!= None):
                objects_map.pop(f"fixed wall {number_of_walls + i}")
                i += 1

    elif ram_state[117] == 14:
        if ram_state[28] == 0:
            wall_instance = Wall()
            wall_instance.xy = (136, 21)
            wall_instance.wh = (24, 38)
            objects.append(wall_instance)
            objects_map['fixed_wall 0'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (8, 21)
            wall_instance.wh = (16, 38)
            objects.append(wall_instance)
            objects_map['fixed_wall 1'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (88, 101)
            wall_instance.wh = (72, 38)
            objects.append(wall_instance)
            objects_map['fixed_wall 2'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (8, 101)
            wall_instance.wh = (64, 38)
            objects.append(wall_instance)
            objects_map['fixed_wall 3'] = wall_instance
            number_of_walls = 4
            i = 0
            while(objects_map.get(f"fixed wall {number_of_walls + i}")!= None):
                objects_map.pop(f"fixed wall {number_of_walls + i}")
                i += 1
        elif ram_state[28] == 1:
            wall_instance = Wall()
            wall_instance.xy = (88, 21)
            wall_instance.wh = (72, 38)
            objects.append(wall_instance)
            objects_map['fixed_wall 0'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (8, 21)
            wall_instance.wh = (64, 38)
            objects.append(wall_instance)
            objects_map['fixed_wall 1'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (112, 101)
            wall_instance.wh = (48, 38)
            objects.append(wall_instance)
            objects_map['fixed_wall 2'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (56, 101)
            wall_instance.wh = (48, 38)
            objects.append(wall_instance)
            objects_map['fixed_wall 3'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (8, 101)
            wall_instance.wh = (40, 38)
            objects.append(wall_instance)
            objects_map['fixed_wall 4'] = wall_instance
            number_of_walls = 5
            i = 0
            while(objects_map.get(f"fixed wall {number_of_walls + i}")!= None):
                objects_map.pop(f"fixed wall {number_of_walls + i}")
                i += 1
        elif ram_state[28] == 2:
            wall_instance = Wall()
            wall_instance.xy = (112, 21)
            wall_instance.wh = (48, 38)
            objects.append(wall_instance)
            objects_map['fixed_wall 0'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (56, 21)
            wall_instance.wh = (48, 38)
            objects.append(wall_instance)
            objects_map['fixed_wall 1'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (8, 21)
            wall_instance.wh = (40, 38)
            objects.append(wall_instance)
            objects_map['fixed_wall 2'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (104, 101)
            wall_instance.wh = (56, 38)
            objects.append(wall_instance)
            objects_map['fixed_wall 3'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (8, 101)
            wall_instance.wh = (48, 38)
            objects.append(wall_instance)
            objects_map['fixed_wall 4'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (144, 61)
            wall_instance.wh = (16, 37)
            objects.append(wall_instance)
            objects_map['fixed_wall 5'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (64, 61)
            wall_instance.wh = (56, 37)
            objects.append(wall_instance)
            objects_map['fixed_wall 6'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (8, 61)
            wall_instance.wh = (32, 37)
            objects.append(wall_instance)
            objects_map['fixed_wall 7'] = wall_instance
            number_of_walls = 8
            i = 0
            while(objects_map.get(f"fixed wall {number_of_walls + i}")!= None):
                objects_map.pop(f"fixed wall {number_of_walls + i}")
                i += 1
        elif ram_state[28] == 3:
            wall_instance = Wall()
            wall_instance.xy = (104, 21)
            wall_instance.wh = (56, 38)
            objects.append(wall_instance)
            objects_map['fixed_wall 0'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (8, 21)
            wall_instance.wh = (48, 38)
            objects.append(wall_instance)
            objects_map['fixed_wall 1'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (128, 101)
            wall_instance.wh = (32, 38)
            objects.append(wall_instance)
            objects_map['fixed_wall 2'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (40, 101)
            wall_instance.wh = (80, 38)
            objects.append(wall_instance)
            objects_map['fixed_wall 3'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (8, 101)
            wall_instance.wh = (24, 38)
            objects.append(wall_instance)
            objects_map['fixed_wall 4'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (144, 61)
            wall_instance.wh = (16, 37)
            objects.append(wall_instance)
            objects_map['fixed_wall 5'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (8, 61)
            wall_instance.wh = (8, 37)
            objects.append(wall_instance)
            objects_map['fixed_wall 6'] = wall_instance
            number_of_walls = 7
            i = 0
            while(objects_map.get(f"fixed wall {number_of_walls + i}")!= None):
                objects_map.pop(f"fixed wall {number_of_walls + i}")
                i += 1
        elif ram_state[28] == 4:
            wall_instance = Wall()
            wall_instance.xy = (128, 21)
            wall_instance.wh = (32, 38)
            objects.append(wall_instance)
            objects_map['fixed_wall 0'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (40, 21)
            wall_instance.wh = (80, 38)
            objects.append(wall_instance)
            objects_map['fixed_wall 1'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (8, 21)
            wall_instance.wh = (24, 38)
            objects.append(wall_instance)
            objects_map['fixed_wall 2'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (96, 101)
            wall_instance.wh = (64, 38)
            objects.append(wall_instance)
            objects_map['fixed_wall 3'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (8, 101)
            wall_instance.wh = (56, 38)
            objects.append(wall_instance)
            objects_map['fixed_wall 4'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (144, 61)
            wall_instance.wh = (16, 37)
            objects.append(wall_instance)
            objects_map['fixed_wall 5'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (8, 61)
            wall_instance.wh = (8, 37)
            objects.append(wall_instance)
            objects_map['fixed_wall 6'] = wall_instance
            number_of_walls = 7
            i = 0
            while(objects_map.get(f"fixed wall {number_of_walls + i}")!= None):
                objects_map.pop(f"fixed wall {number_of_walls + i}")
                i += 1
        elif ram_state[28] == 5:
            wall_instance = Wall()
            wall_instance.xy = (96, 21)
            wall_instance.wh = (64, 38)
            objects.append(wall_instance)
            objects_map['fixed_wall 0'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (8, 21)
            wall_instance.wh = (56, 38)
            objects.append(wall_instance)
            objects_map['fixed_wall 1'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (136, 101)
            wall_instance.wh = (24, 38)
            objects.append(wall_instance)
            objects_map['fixed_wall 2'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (84, 101)
            wall_instance.wh = (44, 38)
            objects.append(wall_instance)
            objects_map['fixed_wall 3'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (32, 101)
            wall_instance.wh = (44, 38)
            objects.append(wall_instance)
            objects_map['fixed_wall 4'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (8, 101)
            wall_instance.wh = (16, 38)
            objects.append(wall_instance)
            objects_map['fixed_wall 5'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (144, 61)
            wall_instance.wh = (16, 37)
            objects.append(wall_instance)
            objects_map['fixed_wall 6'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (8, 61)
            wall_instance.wh = (8, 37)
            objects.append(wall_instance)
            objects_map['fixed_wall 7'] = wall_instance
            number_of_walls = 8
            i = 0
            while(objects_map.get(f"fixed wall {number_of_walls + i}")!= None):
                objects_map.pop(f"fixed wall {number_of_walls + i}")
                i += 1
        elif ram_state[28] == 6:
            wall_instance = Wall()
            wall_instance.xy = (136, 21)
            wall_instance.wh = (24, 38)
            objects.append(wall_instance)
            objects_map['fixed_wall 0'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (84, 21)
            wall_instance.wh = (44, 38)
            objects.append(wall_instance)
            objects_map['fixed_wall 1'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (32, 21)
            wall_instance.wh = (44, 38)
            objects.append(wall_instance)
            objects_map['fixed_wall 2'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (8, 21)
            wall_instance.wh = (16, 38)
            objects.append(wall_instance)
            objects_map['fixed_wall 3'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (136, 101)
            wall_instance.wh = (24, 38)
            objects.append(wall_instance)
            objects_map['fixed_wall 4'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (48, 101)
            wall_instance.wh = (64, 38)
            objects.append(wall_instance)
            objects_map['fixed_wall 5'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (8, 101)
            wall_instance.wh = (16, 38)
            objects.append(wall_instance)
            objects_map['fixed_wall 6'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (144, 61)
            wall_instance.wh = (16, 37)
            objects.append(wall_instance)
            objects_map['fixed_wall 7'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (64, 61)
            wall_instance.wh = (32, 37)
            objects.append(wall_instance)
            objects_map['fixed_wall 8'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (8, 61)
            wall_instance.wh = (8, 37)
            objects.append(wall_instance)
            objects_map['fixed_wall 9'] = wall_instance
            number_of_walls = 10
            i = 0
            while(objects_map.get(f"fixed wall {number_of_walls + i}")!= None):
                objects_map.pop(f"fixed wall {number_of_walls + i}")
                i += 1
        elif ram_state[28] == 7:
            wall_instance = Wall()
            wall_instance.xy = (136, 21)
            wall_instance.wh = (24, 38)
            objects.append(wall_instance)
            objects_map['fixed_wall 0'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (48, 21)
            wall_instance.wh = (64, 38)
            objects.append(wall_instance)
            objects_map['fixed_wall 1'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (8, 21)
            wall_instance.wh = (16, 38)
            objects.append(wall_instance)
            objects_map['fixed_wall 2'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (136, 101)
            wall_instance.wh = (24, 38)
            objects.append(wall_instance)
            objects_map['fixed_wall 3'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (32, 101)
            wall_instance.wh = (96, 38)
            objects.append(wall_instance)
            objects_map['fixed_wall 4'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (8, 101)
            wall_instance.wh = (16, 38)
            objects.append(wall_instance)
            objects_map['fixed_wall 5'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (144, 61)
            wall_instance.wh = (16, 37)
            objects.append(wall_instance)
            objects_map['fixed_wall 6'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (8, 61)
            wall_instance.wh = (8, 37)
            objects.append(wall_instance)
            objects_map['fixed_wall 7'] = wall_instance
            number_of_walls = 8
            i = 0
            while(objects_map.get(f"fixed wall {number_of_walls + i}")!= None):
                objects_map.pop(f"fixed wall {number_of_walls + i}")
                i += 1
        elif ram_state[28] == 8:
            wall_instance = Wall()
            wall_instance.xy = (136, 21)
            wall_instance.wh = (24, 38)
            objects.append(wall_instance)
            objects_map['fixed_wall 0'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (32, 21)
            wall_instance.wh = (96, 38)
            objects.append(wall_instance)
            objects_map['fixed_wall 1'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (8, 21)
            wall_instance.wh = (16, 38)
            objects.append(wall_instance)
            objects_map['fixed_wall 2'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (136, 101)
            wall_instance.wh = (24, 38)
            objects.append(wall_instance)
            objects_map['fixed_wall 3'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (84, 101)
            wall_instance.wh = (44, 38)
            objects.append(wall_instance)
            objects_map['fixed_wall 4'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (32, 101)
            wall_instance.wh = (44, 38)
            objects.append(wall_instance)
            objects_map['fixed_wall 5'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (8, 101)
            wall_instance.wh = (16, 38)
            objects.append(wall_instance)
            objects_map['fixed_wall 6'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (144, 61)
            wall_instance.wh = (16, 37)
            objects.append(wall_instance)
            objects_map['fixed_wall 7'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (8, 61)
            wall_instance.wh = (8, 37)
            objects.append(wall_instance)
            objects_map['fixed_wall 8'] = wall_instance
            number_of_walls = 9
            i = 0
            while(objects_map.get(f"fixed wall {number_of_walls + i}")!= None):
                objects_map.pop(f"fixed wall {number_of_walls + i}")
                i += 1
        elif ram_state[28] == 9:
            wall_instance = Wall()
            wall_instance.xy = (136, 21)
            wall_instance.wh = (24, 38)
            objects.append(wall_instance)
            objects_map['fixed_wall 0'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (84, 21)
            wall_instance.wh = (44, 38)
            objects.append(wall_instance)
            objects_map['fixed_wall 1'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (32, 21)
            wall_instance.wh = (44, 38)
            objects.append(wall_instance)
            objects_map['fixed_wall 2'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (8, 21)
            wall_instance.wh = (16, 38)
            objects.append(wall_instance)
            objects_map['fixed_wall 3'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (88, 101)
            wall_instance.wh = (72, 38)
            objects.append(wall_instance)
            objects_map['fixed_wall 4'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (8, 101)
            wall_instance.wh = (64, 38)
            objects.append(wall_instance)
            objects_map['fixed_wall 5'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (96, 61)
            wall_instance.wh = (64, 37)
            objects.append(wall_instance)
            objects_map['fixed_wall 6'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (8, 61)
            wall_instance.wh = (56, 37)
            objects.append(wall_instance)
            objects_map['fixed_wall 7'] = wall_instance
            number_of_walls = 8
            i = 0
            while(objects_map.get(f"fixed wall {number_of_walls + i}")!= None):
                objects_map.pop(f"fixed wall {number_of_walls + i}")
                i += 1
        elif ram_state[28] == 10:
            wall_instance = Wall()
            wall_instance.xy = (88, 21)
            wall_instance.wh = (72, 38)
            objects.append(wall_instance)
            objects_map['fixed_wall 0'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (8, 21)
            wall_instance.wh = (64, 38)
            objects.append(wall_instance)
            objects_map['fixed_wall 1'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (128, 61)
            wall_instance.wh = (32, 37)
            objects.append(wall_instance)
            objects_map['fixed_wall 2'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (48, 61)
            wall_instance.wh = (32, 37)
            objects.append(wall_instance)
            objects_map['fixed_wall 3'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (120, 101)
            wall_instance.wh = (40, 38)
            objects.append(wall_instance)
            objects_map['fixed_wall 4'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (8, 101)
            wall_instance.wh = (32, 38)
            objects.append(wall_instance)
            objects_map['fixed_wall 5'] = wall_instance
            number_of_walls = 6
            i = 0
            while(objects_map.get(f"fixed wall {number_of_walls + i}")!= None):
                objects_map.pop(f"fixed wall {number_of_walls + i}")
                i += 1
        elif ram_state[28] == 11:
            wall_instance = Wall()
            wall_instance.xy = (8, 21)
            wall_instance.wh = (152, 38)
            objects.append(wall_instance)
            objects_map['fixed_wall 0'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (144, 101)
            wall_instance.wh = (16, 38)
            objects.append(wall_instance)
            objects_map['fixed_wall 1'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (72, 101)
            wall_instance.wh = (16, 38)
            objects.append(wall_instance)
            objects_map['fixed_wall 2'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (8, 101)
            wall_instance.wh = (8, 38)
            objects.append(wall_instance)
            objects_map['fixed_wall 3'] = wall_instance
            number_of_walls = 4
            i = 0
            while(objects_map.get(f"fixed wall {number_of_walls + i}")!= None):
                objects_map.pop(f"fixed wall {number_of_walls + i}")
                i += 1
        elif ram_state[28] == 12:
            wall_instance = Wall()
            wall_instance.xy = (8, 21)
            wall_instance.wh = (152, 38)
            objects.append(wall_instance)
            objects_map['fixed_wall 0'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (120, 61)
            wall_instance.wh = (16, 37)
            objects.append(wall_instance)
            objects_map['fixed_wall 1'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (40, 61)
            wall_instance.wh = (16, 37)
            objects.append(wall_instance)
            objects_map['fixed_wall 2'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (144, 101)
            wall_instance.wh = (16, 38)
            objects.append(wall_instance)
            objects_map['fixed_wall 3'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (64, 101)
            wall_instance.wh = (32, 38)
            objects.append(wall_instance)
            objects_map['fixed_wall 4'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (8, 101)
            wall_instance.wh = (8, 38)
            objects.append(wall_instance)
            objects_map['fixed_wall 5'] = wall_instance
            number_of_walls = 6
            i = 0
            while(objects_map.get(f"fixed wall {number_of_walls + i}")!= None):
                objects_map.pop(f"fixed wall {number_of_walls + i}")
                i += 1
        elif ram_state[28] == 13:
            wall_instance = Wall()
            wall_instance.xy = (8, 21)
            wall_instance.wh = (152, 38)
            objects.append(wall_instance)
            objects_map['fixed_wall 0'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (136, 101)
            wall_instance.wh = (24, 38)
            objects.append(wall_instance)
            objects_map['fixed_wall 1'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (8, 101)
            wall_instance.wh = (16, 38)
            objects.append(wall_instance)
            objects_map['fixed_wall 2'] = wall_instance
            number_of_walls = 3
            i = 0
            while(objects_map.get(f"fixed wall {number_of_walls + i}")!= None):
                objects_map.pop(f"fixed wall {number_of_walls + i}")
                i += 1
        elif ram_state[28] == 14:
            wall_instance = Wall()
            wall_instance.xy = (8, 21)
            wall_instance.wh = (152, 38)
            objects.append(wall_instance)
            objects_map['fixed_wall 0'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (8, 101)
            wall_instance.wh = (152, 38)
            objects.append(wall_instance)
            objects_map['fixed_wall 1'] = wall_instance
            number_of_walls = 2
            i = 0
            while(objects_map.get(f"fixed wall {number_of_walls + i}")!= None):
                objects_map.pop(f"fixed wall {number_of_walls + i}")
                i += 1
        elif ram_state[28] == 15:
            wall_instance = Wall()
            wall_instance.xy = (8, 21)
            wall_instance.wh = (152, 38)
            objects.append(wall_instance)
            objects_map['fixed_wall 0'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (112, 101)
            wall_instance.wh = (48, 38)
            objects.append(wall_instance)
            objects_map['fixed_wall 1'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (60, 101)
            wall_instance.wh = (40, 38)
            objects.append(wall_instance)
            objects_map['fixed_wall 2'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (8, 101)
            wall_instance.wh = (40, 38)
            objects.append(wall_instance)
            objects_map['fixed_wall 3'] = wall_instance
            number_of_walls = 4
            i = 0
            while(objects_map.get(f"fixed wall {number_of_walls + i}")!= None):
                objects_map.pop(f"fixed wall {number_of_walls + i}")
                i += 1

    elif ram_state[117] == 15:
        if ram_state[28] == 0:
            wall_instance = Wall()
            wall_instance.xy = (136, 21)
            wall_instance.wh = (24, 38)
            objects.append(wall_instance)
            objects_map['fixed_wall 0'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (8, 21)
            wall_instance.wh = (16, 38)
            objects.append(wall_instance)
            objects_map['fixed_wall 1'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (136, 101)
            wall_instance.wh = (24, 38)
            objects.append(wall_instance)
            objects_map['fixed_wall 2'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (88, 101)
            wall_instance.wh = (40, 38)
            objects.append(wall_instance)
            objects_map['fixed_wall 3'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (32, 101)
            wall_instance.wh = (40, 38)
            objects.append(wall_instance)
            objects_map['fixed_wall 4'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (8, 101)
            wall_instance.wh = (16, 38)
            objects.append(wall_instance)
            objects_map['fixed_wall 5'] = wall_instance
            number_of_walls = 6
            i = 0
            while(objects_map.get(f"fixed wall {number_of_walls + i}")!= None):
                objects_map.pop(f"fixed wall {number_of_walls + i}")
                i += 1
        elif ram_state[28] == 1:
            wall_instance = Wall()
            wall_instance.xy = (136, 21)
            wall_instance.wh = (24, 38)
            objects.append(wall_instance)
            objects_map['fixed_wall 0'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (88, 21)
            wall_instance.wh = (40, 38)
            objects.append(wall_instance)
            objects_map['fixed_wall 1'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (32, 21)
            wall_instance.wh = (40, 38)
            objects.append(wall_instance)
            objects_map['fixed_wall 2'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (8, 21)
            wall_instance.wh = (16, 38)
            objects.append(wall_instance)
            objects_map['fixed_wall 3'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (8, 101)
            wall_instance.wh = (152, 38)
            objects.append(wall_instance)
            objects_map['fixed_wall 4'] = wall_instance
            number_of_walls = 5
            i = 0
            while(objects_map.get(f"fixed wall {number_of_walls + i}")!= None):
                objects_map.pop(f"fixed wall {number_of_walls + i}")
                i += 1
        elif ram_state[28] == 2:
            wall_instance = Wall()
            wall_instance.xy = (8, 21)
            wall_instance.wh = (152, 38)
            objects.append(wall_instance)
            objects_map['fixed_wall 0'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (128, 101)
            wall_instance.wh = (32, 38)
            objects.append(wall_instance)
            objects_map['fixed_wall 1'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (8, 101)
            wall_instance.wh = (24, 38)
            objects.append(wall_instance)
            objects_map['fixed_wall 2'] = wall_instance
            number_of_walls = 3
            i = 0
            while(objects_map.get(f"fixed wall {number_of_walls + i}")!= None):
                objects_map.pop(f"fixed wall {number_of_walls + i}")
                i += 1
        elif ram_state[28] == 3:
            wall_instance = Wall()
            wall_instance.xy = (128, 21)
            wall_instance.wh = (32, 38)
            objects.append(wall_instance)
            objects_map['fixed_wall 0'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (8, 21)
            wall_instance.wh = (24, 38)
            objects.append(wall_instance)
            objects_map['fixed_wall 1'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (112, 101)
            wall_instance.wh = (48, 38)
            objects.append(wall_instance)
            objects_map['fixed_wall 2'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (8, 101)
            wall_instance.wh = (40, 38)
            objects.append(wall_instance)
            objects_map['fixed_wall 3'] = wall_instance
            number_of_walls = 4
            i = 0
            while(objects_map.get(f"fixed wall {number_of_walls + i}")!= None):
                objects_map.pop(f"fixed wall {number_of_walls + i}")
                i += 1
        elif ram_state[28] == 4:
            wall_instance = Wall()
            wall_instance.xy = (112, 21)
            wall_instance.wh = (48, 38)
            objects.append(wall_instance)
            objects_map['fixed_wall 0'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (8, 21)
            wall_instance.wh = (40, 38)
            objects.append(wall_instance)
            objects_map['fixed_wall 1'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (140, 101)
            wall_instance.wh = (20, 38)
            objects.append(wall_instance)
            objects_map['fixed_wall 2'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (28, 101)
            wall_instance.wh = (104, 38)
            objects.append(wall_instance)
            objects_map['fixed_wall 3'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (8, 101)
            wall_instance.wh = (12, 38)
            objects.append(wall_instance)
            objects_map['fixed_wall 4'] = wall_instance
            number_of_walls = 5
            i = 0
            while(objects_map.get(f"fixed wall {number_of_walls + i}")!= None):
                objects_map.pop(f"fixed wall {number_of_walls + i}")
                i += 1
        elif ram_state[28] == 5:
            wall_instance = Wall()
            wall_instance.xy = (140, 21)
            wall_instance.wh = (20, 38)
            objects.append(wall_instance)
            objects_map['fixed_wall 0'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (28, 21)
            wall_instance.wh = (104, 38)
            objects.append(wall_instance)
            objects_map['fixed_wall 1'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (8, 21)
            wall_instance.wh = (12, 38)
            objects.append(wall_instance)
            objects_map['fixed_wall 2'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (108, 101)
            wall_instance.wh = (52, 38)
            objects.append(wall_instance)
            objects_map['fixed_wall 3'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (8, 101)
            wall_instance.wh = (44, 38)
            objects.append(wall_instance)
            objects_map['fixed_wall 4'] = wall_instance
            number_of_walls = 5
            i = 0
            while(objects_map.get(f"fixed wall {number_of_walls + i}")!= None):
                objects_map.pop(f"fixed wall {number_of_walls + i}")
                i += 1
        elif ram_state[28] == 6:
            wall_instance = Wall()
            wall_instance.xy = (108, 21)
            wall_instance.wh = (52, 38)
            objects.append(wall_instance)
            objects_map['fixed_wall 0'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (8, 21)
            wall_instance.wh = (44, 38)
            objects.append(wall_instance)
            objects_map['fixed_wall 1'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (144, 101)
            wall_instance.wh = (16, 38)
            objects.append(wall_instance)
            objects_map['fixed_wall 2'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (8, 101)
            wall_instance.wh = (8, 38)
            objects.append(wall_instance)
            objects_map['fixed_wall 3'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (104, 61)
            wall_instance.wh = (56, 37)
            objects.append(wall_instance)
            objects_map['fixed_wall 4'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (64, 61)
            wall_instance.wh = (32, 37)
            objects.append(wall_instance)
            objects_map['fixed_wall 5'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (8, 61)
            wall_instance.wh = (48, 37)
            objects.append(wall_instance)
            objects_map['fixed_wall 6'] = wall_instance
            number_of_walls = 7
            i = 0
            while(objects_map.get(f"fixed wall {number_of_walls + i}")!= None):
                objects_map.pop(f"fixed wall {number_of_walls + i}")
                i += 1
        elif ram_state[28] == 7:
            wall_instance = Wall()
            wall_instance.xy = (144, 21)
            wall_instance.wh = (16, 38)
            objects.append(wall_instance)
            objects_map['fixed_wall 0'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (8, 21)
            wall_instance.wh = (8, 38)
            objects.append(wall_instance)
            objects_map['fixed_wall 1'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (144, 101)
            wall_instance.wh = (16, 38)
            objects.append(wall_instance)
            objects_map['fixed_wall 2'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (8, 101)
            wall_instance.wh = (8, 38)
            objects.append(wall_instance)
            objects_map['fixed_wall 3'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (88, 61)
            wall_instance.wh = (72, 37)
            objects.append(wall_instance)
            objects_map['fixed_wall 4'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (8, 61)
            wall_instance.wh = (64, 37)
            objects.append(wall_instance)
            objects_map['fixed_wall 5'] = wall_instance
            number_of_walls = 6
            i = 0
            while(objects_map.get(f"fixed wall {number_of_walls + i}")!= None):
                objects_map.pop(f"fixed wall {number_of_walls + i}")
                i += 1
        elif ram_state[28] == 8:
            wall_instance = Wall()
            wall_instance.xy = (144, 21)
            wall_instance.wh = (16, 38)
            objects.append(wall_instance)
            objects_map['fixed_wall 0'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (8, 21)
            wall_instance.wh = (8, 38)
            objects.append(wall_instance)
            objects_map['fixed_wall 1'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (144, 101)
            wall_instance.wh = (16, 38)
            objects.append(wall_instance)
            objects_map['fixed_wall 2'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (8, 101)
            wall_instance.wh = (8, 38)
            objects.append(wall_instance)
            objects_map['fixed_wall 3'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (112, 61)
            wall_instance.wh = (48, 37)
            objects.append(wall_instance)
            objects_map['fixed_wall 4'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (84, 61)
            wall_instance.wh = (20, 37)
            objects.append(wall_instance)
            objects_map['fixed_wall 5'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (56, 61)
            wall_instance.wh = (20, 37)
            objects.append(wall_instance)
            objects_map['fixed_wall 6'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (8, 61)
            wall_instance.wh = (40, 37)
            objects.append(wall_instance)
            objects_map['fixed_wall 7'] = wall_instance
            number_of_walls = 8
            i = 0
            while(objects_map.get(f"fixed wall {number_of_walls + i}")!= None):
                objects_map.pop(f"fixed wall {number_of_walls + i}")
                i += 1
        elif ram_state[28] == 9:
            wall_instance = Wall()
            wall_instance.xy = (144, 21)
            wall_instance.wh = (16, 38)
            objects.append(wall_instance)
            objects_map['fixed_wall 0'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (8, 21)
            wall_instance.wh = (8, 38)
            objects.append(wall_instance)
            objects_map['fixed_wall 1'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (128, 101)
            wall_instance.wh = (32, 38)
            objects.append(wall_instance)
            objects_map['fixed_wall 2'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (8, 101)
            wall_instance.wh = (24, 38)
            objects.append(wall_instance)
            objects_map['fixed_wall 3'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (88, 61)
            wall_instance.wh = (72, 37)
            objects.append(wall_instance)
            objects_map['fixed_wall 4'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (8, 61)
            wall_instance.wh = (64, 37)
            objects.append(wall_instance)
            objects_map['fixed_wall 5'] = wall_instance
            number_of_walls = 6
            i = 0
            while(objects_map.get(f"fixed wall {number_of_walls + i}")!= None):
                objects_map.pop(f"fixed wall {number_of_walls + i}")
                i += 1
        elif ram_state[28] == 10:
            wall_instance = Wall()
            wall_instance.xy = (128, 21)
            wall_instance.wh = (32, 38)
            objects.append(wall_instance)
            objects_map['fixed_wall 0'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (8, 21)
            wall_instance.wh = (24, 38)
            objects.append(wall_instance)
            objects_map['fixed_wall 1'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (136, 101)
            wall_instance.wh = (24, 38)
            objects.append(wall_instance)
            objects_map['fixed_wall 2'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (8, 101)
            wall_instance.wh = (16, 38)
            objects.append(wall_instance)
            objects_map['fixed_wall 3'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (72, 61)
            wall_instance.wh = (16, 37)
            objects.append(wall_instance)
            objects_map['fixed_wall 4'] = wall_instance
            number_of_walls = 5
            i = 0
            while(objects_map.get(f"fixed wall {number_of_walls + i}")!= None):
                objects_map.pop(f"fixed wall {number_of_walls + i}")
                i += 1
        elif ram_state[28] == 11:
            wall_instance = Wall()
            wall_instance.xy = (8, 21)
            wall_instance.wh = (152, 38)
            objects.append(wall_instance)
            objects_map['fixed_wall 0'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (136, 101)
            wall_instance.wh = (24, 38)
            objects.append(wall_instance)
            objects_map['fixed_wall 1'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (8, 101)
            wall_instance.wh = (16, 38)
            objects.append(wall_instance)
            objects_map['fixed_wall 2'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (48, 61)
            wall_instance.wh = (64, 37)
            objects.append(wall_instance)
            objects_map['fixed_wall 3'] = wall_instance
            number_of_walls = 4
            i = 0
            while(objects_map.get(f"fixed wall {number_of_walls + i}")!= None):
                objects_map.pop(f"fixed wall {number_of_walls + i}")
                i += 1
        elif ram_state[28] == 12:
            wall_instance = Wall()
            wall_instance.xy = (8, 21)
            wall_instance.wh = (152, 38)
            objects.append(wall_instance)
            objects_map['fixed_wall 0'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (132, 101)
            wall_instance.wh = (28, 38)
            objects.append(wall_instance)
            objects_map['fixed_wall 1'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (72, 101)
            wall_instance.wh = (16, 38)
            objects.append(wall_instance)
            objects_map['fixed_wall 2'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (8, 101)
            wall_instance.wh = (20, 38)
            objects.append(wall_instance)
            objects_map['fixed_wall 3'] = wall_instance
            number_of_walls = 4
            i = 0
            while(objects_map.get(f"fixed wall {number_of_walls + i}")!= None):
                objects_map.pop(f"fixed wall {number_of_walls + i}")
                i += 1
        elif ram_state[28] == 13:
            wall_instance = Wall()
            wall_instance.xy = (8, 21)
            wall_instance.wh = (152, 38)
            objects.append(wall_instance)
            objects_map['fixed_wall 0'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (136, 101)
            wall_instance.wh = (24, 38)
            objects.append(wall_instance)
            objects_map['fixed_wall 1'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (8, 101)
            wall_instance.wh = (16, 38)
            objects.append(wall_instance)
            objects_map['fixed_wall 2'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (40, 61)
            wall_instance.wh = (80, 37)
            objects.append(wall_instance)
            objects_map['fixed_wall 3'] = wall_instance
            number_of_walls = 4
            i = 0
            while(objects_map.get(f"fixed wall {number_of_walls + i}")!= None):
                objects_map.pop(f"fixed wall {number_of_walls + i}")
                i += 1
        elif ram_state[28] == 14:
            wall_instance = Wall()
            wall_instance.xy = (8, 21)
            wall_instance.wh = (152, 38)
            objects.append(wall_instance)
            objects_map['fixed_wall 0'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (128, 101)
            wall_instance.wh = (32, 38)
            objects.append(wall_instance)
            objects_map['fixed_wall 1'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (68, 101)
            wall_instance.wh = (24, 38)
            objects.append(wall_instance)
            objects_map['fixed_wall 2'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (8, 101)
            wall_instance.wh = (24, 38)
            objects.append(wall_instance)
            objects_map['fixed_wall 3'] = wall_instance
            number_of_walls = 4
            i = 0
            while(objects_map.get(f"fixed wall {number_of_walls + i}")!= None):
                objects_map.pop(f"fixed wall {number_of_walls + i}")
                i += 1
        elif ram_state[28] == 15:
            wall_instance = Wall()
            wall_instance.xy = (8, 21)
            wall_instance.wh = (152, 38)
            objects.append(wall_instance)
            objects_map['fixed_wall 0'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (112, 101)
            wall_instance.wh = (48, 38)
            objects.append(wall_instance)
            objects_map['fixed_wall 1'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (8, 101)
            wall_instance.wh = (40, 38)
            objects.append(wall_instance)
            objects_map['fixed_wall 2'] = wall_instance
            number_of_walls = 3
            i = 0
            while(objects_map.get(f"fixed wall {number_of_walls + i}")!= None):
                objects_map.pop(f"fixed wall {number_of_walls + i}")
                i += 1

    elif ram_state[117] == 16:
        if ram_state[28] == 0:
            wall_instance = Wall()
            wall_instance.xy = (136, 21)
            wall_instance.wh = (24, 38)
            objects.append(wall_instance)
            objects_map['fixed_wall 0'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (8, 21)
            wall_instance.wh = (16, 38)
            objects.append(wall_instance)
            objects_map['fixed_wall 1'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (88, 101)
            wall_instance.wh = (72, 38)
            objects.append(wall_instance)
            objects_map['fixed_wall 2'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (8, 101)
            wall_instance.wh = (64, 38)
            objects.append(wall_instance)
            objects_map['fixed_wall 3'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (144, 61)
            wall_instance.wh = (16, 37)
            objects.append(wall_instance)
            objects_map['fixed_wall 4'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (8, 61)
            wall_instance.wh = (8, 37)
            objects.append(wall_instance)
            objects_map['fixed_wall 5'] = wall_instance
            number_of_walls = 6
            i = 0
            while(objects_map.get(f"fixed wall {number_of_walls + i}")!= None):
                objects_map.pop(f"fixed wall {number_of_walls + i}")
                i += 1
        elif ram_state[28] == 1:
            wall_instance = Wall()
            wall_instance.xy = (88, 21)
            wall_instance.wh = (72, 38)
            objects.append(wall_instance)
            objects_map['fixed_wall 0'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (8, 21)
            wall_instance.wh = (64, 38)
            objects.append(wall_instance)
            objects_map['fixed_wall 1'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (144, 101)
            wall_instance.wh = (16, 38)
            objects.append(wall_instance)
            objects_map['fixed_wall 2'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (48, 101)
            wall_instance.wh = (64, 38)
            objects.append(wall_instance)
            objects_map['fixed_wall 3'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (8, 101)
            wall_instance.wh = (8, 38)
            objects.append(wall_instance)
            objects_map['fixed_wall 4'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (128, 61)
            wall_instance.wh = (32, 37)
            objects.append(wall_instance)
            objects_map['fixed_wall 5'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (8, 61)
            wall_instance.wh = (24, 37)
            objects.append(wall_instance)
            objects_map['fixed_wall 6'] = wall_instance
            number_of_walls = 7
            i = 0
            while(objects_map.get(f"fixed wall {number_of_walls + i}")!= None):
                objects_map.pop(f"fixed wall {number_of_walls + i}")
                i += 1
        elif ram_state[28] == 2:
            wall_instance = Wall()
            wall_instance.xy = (144, 21)
            wall_instance.wh = (16, 38)
            objects.append(wall_instance)
            objects_map['fixed_wall 0'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (48, 21)
            wall_instance.wh = (64, 38)
            objects.append(wall_instance)
            objects_map['fixed_wall 1'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (8, 21)
            wall_instance.wh = (8, 38)
            objects.append(wall_instance)
            objects_map['fixed_wall 2'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (128, 101)
            wall_instance.wh = (32, 38)
            objects.append(wall_instance)
            objects_map['fixed_wall 3'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (8, 101)
            wall_instance.wh = (24, 38)
            objects.append(wall_instance)
            objects_map['fixed_wall 4'] = wall_instance
            number_of_walls = 5
            i = 0
            while(objects_map.get(f"fixed wall {number_of_walls + i}")!= None):
                objects_map.pop(f"fixed wall {number_of_walls + i}")
                i += 1
        elif ram_state[28] == 3:
            wall_instance = Wall()
            wall_instance.xy = (128, 21)
            wall_instance.wh = (32, 38)
            objects.append(wall_instance)
            objects_map['fixed_wall 0'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (8, 21)
            wall_instance.wh = (24, 38)
            objects.append(wall_instance)
            objects_map['fixed_wall 1'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (112, 61)
            wall_instance.wh = (48, 37)
            objects.append(wall_instance)
            objects_map['fixed_wall 2'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (8, 61)
            wall_instance.wh = (40, 37)
            objects.append(wall_instance)
            objects_map['fixed_wall 3'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (144, 101)
            wall_instance.wh = (16, 38)
            objects.append(wall_instance)
            objects_map['fixed_wall 4'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (8, 101)
            wall_instance.wh = (8, 38)
            objects.append(wall_instance)
            objects_map['fixed_wall 5'] = wall_instance
            number_of_walls = 6
            i = 0
            while(objects_map.get(f"fixed wall {number_of_walls + i}")!= None):
                objects_map.pop(f"fixed wall {number_of_walls + i}")
                i += 1
        elif ram_state[28] == 4:
            wall_instance = Wall()
            wall_instance.xy = (144, 21)
            wall_instance.wh = (16, 38)
            objects.append(wall_instance)
            objects_map['fixed_wall 0'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (8, 21)
            wall_instance.wh = (8, 38)
            objects.append(wall_instance)
            objects_map['fixed_wall 1'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (112, 101)
            wall_instance.wh = (48, 38)
            objects.append(wall_instance)
            objects_map['fixed_wall 2'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (8, 101)
            wall_instance.wh = (40, 38)
            objects.append(wall_instance)
            objects_map['fixed_wall 3'] = wall_instance
            number_of_walls = 4
            i = 0
            while(objects_map.get(f"fixed wall {number_of_walls + i}")!= None):
                objects_map.pop(f"fixed wall {number_of_walls + i}")
                i += 1
        elif ram_state[28] == 5:
            wall_instance = Wall()
            wall_instance.xy = (112, 21)
            wall_instance.wh = (48, 38)
            objects.append(wall_instance)
            objects_map['fixed_wall 0'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (8, 21)
            wall_instance.wh = (40, 38)
            objects.append(wall_instance)
            objects_map['fixed_wall 1'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (84, 101)
            wall_instance.wh = (76, 38)
            objects.append(wall_instance)
            objects_map['fixed_wall 2'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (8, 101)
            wall_instance.wh = (68, 38)
            objects.append(wall_instance)
            objects_map['fixed_wall 3'] = wall_instance
            number_of_walls = 4
            i = 0
            while(objects_map.get(f"fixed wall {number_of_walls + i}")!= None):
                objects_map.pop(f"fixed wall {number_of_walls + i}")
                i += 1
        elif ram_state[28] == 6:
            wall_instance = Wall()
            wall_instance.xy = (84, 21)
            wall_instance.wh = (76, 38)
            objects.append(wall_instance)
            objects_map['fixed_wall 0'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (8, 21)
            wall_instance.wh = (68, 38)
            objects.append(wall_instance)
            objects_map['fixed_wall 1'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (136, 101)
            wall_instance.wh = (24, 38)
            objects.append(wall_instance)
            objects_map['fixed_wall 2'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (32, 101)
            wall_instance.wh = (96, 38)
            objects.append(wall_instance)
            objects_map['fixed_wall 3'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (8, 101)
            wall_instance.wh = (16, 38)
            objects.append(wall_instance)
            objects_map['fixed_wall 4'] = wall_instance
            number_of_walls = 5
            i = 0
            while(objects_map.get(f"fixed wall {number_of_walls + i}")!= None):
                objects_map.pop(f"fixed wall {number_of_walls + i}")
                i += 1
        elif ram_state[28] == 7:
            wall_instance = Wall()
            wall_instance.xy = (136, 21)
            wall_instance.wh = (24, 38)
            objects.append(wall_instance)
            objects_map['fixed_wall 0'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (32, 21)
            wall_instance.wh = (96, 38)
            objects.append(wall_instance)
            objects_map['fixed_wall 1'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (8, 21)
            wall_instance.wh = (16, 38)
            objects.append(wall_instance)
            objects_map['fixed_wall 2'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (8, 101)
            wall_instance.wh = (152, 38)
            objects.append(wall_instance)
            objects_map['fixed_wall 3'] = wall_instance
            number_of_walls = 4
            i = 0
            while(objects_map.get(f"fixed wall {number_of_walls + i}")!= None):
                objects_map.pop(f"fixed wall {number_of_walls + i}")
                i += 1
        elif ram_state[28] == 8:
            wall_instance = Wall()
            wall_instance.xy = (8, 21)
            wall_instance.wh = (152, 38)
            objects.append(wall_instance)
            objects_map['fixed_wall 0'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (136, 101)
            wall_instance.wh = (24, 38)
            objects.append(wall_instance)
            objects_map['fixed_wall 1'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (8, 101)
            wall_instance.wh = (16, 38)
            objects.append(wall_instance)
            objects_map['fixed_wall 2'] = wall_instance
            number_of_walls = 3
            i = 0
            while(objects_map.get(f"fixed wall {number_of_walls + i}")!= None):
                objects_map.pop(f"fixed wall {number_of_walls + i}")
                i += 1
        elif ram_state[28] == 9:
            wall_instance = Wall()
            wall_instance.xy = (136, 21)
            wall_instance.wh = (24, 38)
            objects.append(wall_instance)
            objects_map['fixed_wall 0'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (8, 21)
            wall_instance.wh = (16, 38)
            objects.append(wall_instance)
            objects_map['fixed_wall 1'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (108, 101)
            wall_instance.wh = (52, 38)
            objects.append(wall_instance)
            objects_map['fixed_wall 2'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (8, 101)
            wall_instance.wh = (44, 38)
            objects.append(wall_instance)
            objects_map['fixed_wall 3'] = wall_instance
            number_of_walls = 4
            i = 0
            while(objects_map.get(f"fixed wall {number_of_walls + i}")!= None):
                objects_map.pop(f"fixed wall {number_of_walls + i}")
                i += 1
        elif ram_state[28] == 10:
            wall_instance = Wall()
            wall_instance.xy = (108, 21)
            wall_instance.wh = (52, 38)
            objects.append(wall_instance)
            objects_map['fixed_wall 0'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (8, 21)
            wall_instance.wh = (44, 38)
            objects.append(wall_instance)
            objects_map['fixed_wall 1'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (136, 101)
            wall_instance.wh = (24, 38)
            objects.append(wall_instance)
            objects_map['fixed_wall 2'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (36, 101)
            wall_instance.wh = (88, 38)
            objects.append(wall_instance)
            objects_map['fixed_wall 3'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (8, 101)
            wall_instance.wh = (16, 38)
            objects.append(wall_instance)
            objects_map['fixed_wall 4'] = wall_instance
            number_of_walls = 5
            i = 0
            while(objects_map.get(f"fixed wall {number_of_walls + i}")!= None):
                objects_map.pop(f"fixed wall {number_of_walls + i}")
                i += 1
        elif ram_state[28] == 11:
            wall_instance = Wall()
            wall_instance.xy = (8, 21)
            wall_instance.wh = (152, 38)
            objects.append(wall_instance)
            objects_map['fixed_wall 0'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (48, 61)
            wall_instance.wh = (64, 37)
            objects.append(wall_instance)
            objects_map['fixed_wall 1'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (132, 101)
            wall_instance.wh = (28, 38)
            objects.append(wall_instance)
            objects_map['fixed_wall 2'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (8, 101)
            wall_instance.wh = (20, 38)
            objects.append(wall_instance)
            objects_map['fixed_wall 3'] = wall_instance
            number_of_walls = 4
            i = 0
            while(objects_map.get(f"fixed wall {number_of_walls + i}")!= None):
                objects_map.pop(f"fixed wall {number_of_walls + i}")
                i += 1
        elif ram_state[28] == 12:
            wall_instance = Wall()
            wall_instance.xy = (8, 21)
            wall_instance.wh = (152, 38)
            objects.append(wall_instance)
            objects_map['fixed_wall 0'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (132, 101)
            wall_instance.wh = (28, 38)
            objects.append(wall_instance)
            objects_map['fixed_wall 1'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (72, 101)
            wall_instance.wh = (16, 38)
            objects.append(wall_instance)
            objects_map['fixed_wall 2'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (8, 101)
            wall_instance.wh = (20, 38)
            objects.append(wall_instance)
            objects_map['fixed_wall 3'] = wall_instance
            number_of_walls = 4
            i = 0
            while(objects_map.get(f"fixed wall {number_of_walls + i}")!= None):
                objects_map.pop(f"fixed wall {number_of_walls + i}")
                i += 1
        elif ram_state[28] == 13:
            wall_instance = Wall()
            wall_instance.xy = (8, 21)
            wall_instance.wh = (152, 38)
            objects.append(wall_instance)
            objects_map['fixed_wall 0'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (132, 101)
            wall_instance.wh = (28, 38)
            objects.append(wall_instance)
            objects_map['fixed_wall 1'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (72, 101)
            wall_instance.wh = (16, 38)
            objects.append(wall_instance)
            objects_map['fixed_wall 2'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (8, 101)
            wall_instance.wh = (20, 38)
            objects.append(wall_instance)
            objects_map['fixed_wall 3'] = wall_instance
            number_of_walls = 4
            i = 0
            while(objects_map.get(f"fixed wall {number_of_walls + i}")!= None):
                objects_map.pop(f"fixed wall {number_of_walls + i}")
                i += 1
        elif ram_state[28] == 14:
            wall_instance = Wall()
            wall_instance.xy = (8, 21)
            wall_instance.wh = (152, 38)
            objects.append(wall_instance)
            objects_map['fixed_wall 0'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (136, 101)
            wall_instance.wh = (24, 38)
            objects.append(wall_instance)
            objects_map['fixed_wall 1'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (8, 101)
            wall_instance.wh = (16, 38)
            objects.append(wall_instance)
            objects_map['fixed_wall 2'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (48, 61)
            wall_instance.wh = (64, 37)
            objects.append(wall_instance)
            objects_map['fixed_wall 3'] = wall_instance
            number_of_walls = 4
            i = 0
            while(objects_map.get(f"fixed wall {number_of_walls + i}")!= None):
                objects_map.pop(f"fixed wall {number_of_walls + i}")
                i += 1
        elif ram_state[28] == 15:
            wall_instance = Wall()
            wall_instance.xy = (8, 21)
            wall_instance.wh = (152, 38)
            objects.append(wall_instance)
            objects_map['fixed_wall 0'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (124, 101)
            wall_instance.wh = (36, 38)
            objects.append(wall_instance)
            objects_map['fixed_wall 1'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (8, 101)
            wall_instance.wh = (28, 38)
            objects.append(wall_instance)
            objects_map['fixed_wall 2'] = wall_instance
            number_of_walls = 3
            i = 0
            while(objects_map.get(f"fixed wall {number_of_walls + i}")!= None):
                objects_map.pop(f"fixed wall {number_of_walls + i}")
                i += 1

    elif ram_state[117] == 17:
        if ram_state[28] == 0:
            wall_instance = Wall()
            wall_instance.xy = (136, 21)
            wall_instance.wh = (24, 38)
            objects.append(wall_instance)
            objects_map['fixed_wall 0'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (8, 21)
            wall_instance.wh = (16, 38)
            objects.append(wall_instance)
            objects_map['fixed_wall 1'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (88, 101)
            wall_instance.wh = (72, 38)
            objects.append(wall_instance)
            objects_map['fixed_wall 2'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (8, 101)
            wall_instance.wh = (64, 38)
            objects.append(wall_instance)
            objects_map['fixed_wall 3'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (144, 61)
            wall_instance.wh = (16, 37)
            objects.append(wall_instance)
            objects_map['fixed_wall 4'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (8, 61)
            wall_instance.wh = (8, 37)
            objects.append(wall_instance)
            objects_map['fixed_wall 5'] = wall_instance
            number_of_walls = 6
            i = 0
            while(objects_map.get(f"fixed wall {number_of_walls + i}")!= None):
                objects_map.pop(f"fixed wall {number_of_walls + i}")
                i += 1
        elif ram_state[28] == 1:
            wall_instance = Wall()
            wall_instance.xy = (88, 21)
            wall_instance.wh = (72, 38)
            objects.append(wall_instance)
            objects_map['fixed_wall 0'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (8, 21)
            wall_instance.wh = (64, 38)
            objects.append(wall_instance)
            objects_map['fixed_wall 1'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (136, 101)
            wall_instance.wh = (24, 38)
            objects.append(wall_instance)
            objects_map['fixed_wall 2'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (48, 101)
            wall_instance.wh = (64, 38)
            objects.append(wall_instance)
            objects_map['fixed_wall 3'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (8, 101)
            wall_instance.wh = (16, 38)
            objects.append(wall_instance)
            objects_map['fixed_wall 4'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (144, 61)
            wall_instance.wh = (16, 37)
            objects.append(wall_instance)
            objects_map['fixed_wall 5'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (8, 61)
            wall_instance.wh = (8, 37)
            objects.append(wall_instance)
            objects_map['fixed_wall 6'] = wall_instance
            number_of_walls = 7
            i = 0
            while(objects_map.get(f"fixed wall {number_of_walls + i}")!= None):
                objects_map.pop(f"fixed wall {number_of_walls + i}")
                i += 1
        elif ram_state[28] == 2:
            wall_instance = Wall()
            wall_instance.xy = (136, 21)
            wall_instance.wh = (24, 38)
            objects.append(wall_instance)
            objects_map['fixed_wall 0'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (48, 21)
            wall_instance.wh = (64, 38)
            objects.append(wall_instance)
            objects_map['fixed_wall 1'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (8, 21)
            wall_instance.wh = (16, 38)
            objects.append(wall_instance)
            objects_map['fixed_wall 2'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (132, 101)
            wall_instance.wh = (28, 38)
            objects.append(wall_instance)
            objects_map['fixed_wall 3'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (48, 101)
            wall_instance.wh = (64, 38)
            objects.append(wall_instance)
            objects_map['fixed_wall 4'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (8, 101)
            wall_instance.wh = (20, 38)
            objects.append(wall_instance)
            objects_map['fixed_wall 5'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (144, 61)
            wall_instance.wh = (16, 37)
            objects.append(wall_instance)
            objects_map['fixed_wall 6'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (36, 61)
            wall_instance.wh = (88, 37)
            objects.append(wall_instance)
            objects_map['fixed_wall 7'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (8, 61)
            wall_instance.wh = (8, 37)
            objects.append(wall_instance)
            objects_map['fixed_wall 8'] = wall_instance
            number_of_walls = 9
            i = 0
            while(objects_map.get(f"fixed wall {number_of_walls + i}")!= None):
                objects_map.pop(f"fixed wall {number_of_walls + i}")
                i += 1
        elif ram_state[28] == 3:
            wall_instance = Wall()
            wall_instance.xy = (132, 21)
            wall_instance.wh = (28, 38)
            objects.append(wall_instance)
            objects_map['fixed_wall 0'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (48, 21)
            wall_instance.wh = (64, 38)
            objects.append(wall_instance)
            objects_map['fixed_wall 1'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (8, 21)
            wall_instance.wh = (20, 38)
            objects.append(wall_instance)
            objects_map['fixed_wall 2'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (88, 101)
            wall_instance.wh = (72, 38)
            objects.append(wall_instance)
            objects_map['fixed_wall 3'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (8, 101)
            wall_instance.wh = (64, 38)
            objects.append(wall_instance)
            objects_map['fixed_wall 4'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (144, 61)
            wall_instance.wh = (16, 37)
            objects.append(wall_instance)
            objects_map['fixed_wall 5'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (8, 61)
            wall_instance.wh = (8, 37)
            objects.append(wall_instance)
            objects_map['fixed_wall 6'] = wall_instance
            number_of_walls = 7
            i = 0
            while(objects_map.get(f"fixed wall {number_of_walls + i}")!= None):
                objects_map.pop(f"fixed wall {number_of_walls + i}")
                i += 1
        elif ram_state[28] == 4:
            wall_instance = Wall()
            wall_instance.xy = (88, 21)
            wall_instance.wh = (72, 38)
            objects.append(wall_instance)
            objects_map['fixed_wall 0'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (8, 21)
            wall_instance.wh = (64, 38)
            objects.append(wall_instance)
            objects_map['fixed_wall 1'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (136, 101)
            wall_instance.wh = (24, 38)
            objects.append(wall_instance)
            objects_map['fixed_wall 2'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (32, 101)
            wall_instance.wh = (96, 38)
            objects.append(wall_instance)
            objects_map['fixed_wall 3'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (8, 101)
            wall_instance.wh = (16, 38)
            objects.append(wall_instance)
            objects_map['fixed_wall 4'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (144, 61)
            wall_instance.wh = (16, 37)
            objects.append(wall_instance)
            objects_map['fixed_wall 5'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (8, 61)
            wall_instance.wh = (8, 37)
            objects.append(wall_instance)
            objects_map['fixed_wall 6'] = wall_instance
            number_of_walls = 7
            i = 0
            while(objects_map.get(f"fixed wall {number_of_walls + i}")!= None):
                objects_map.pop(f"fixed wall {number_of_walls + i}")
                i += 1
        elif ram_state[28] == 5:
            wall_instance = Wall()
            wall_instance.xy = (136, 21)
            wall_instance.wh = (24, 38)
            objects.append(wall_instance)
            objects_map['fixed_wall 0'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (32, 21)
            wall_instance.wh = (96, 38)
            objects.append(wall_instance)
            objects_map['fixed_wall 1'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (8, 21)
            wall_instance.wh = (16, 38)
            objects.append(wall_instance)
            objects_map['fixed_wall 2'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (8, 101)
            wall_instance.wh = (152, 38)
            objects.append(wall_instance)
            objects_map['fixed_wall 3'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (144, 61)
            wall_instance.wh = (16, 37)
            objects.append(wall_instance)
            objects_map['fixed_wall 4'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (8, 61)
            wall_instance.wh = (8, 37)
            objects.append(wall_instance)
            objects_map['fixed_wall 5'] = wall_instance
            number_of_walls = 6
            i = 0
            while(objects_map.get(f"fixed wall {number_of_walls + i}")!= None):
                objects_map.pop(f"fixed wall {number_of_walls + i}")
                i += 1
        elif ram_state[28] == 6:
            wall_instance = Wall()
            wall_instance.xy = (8, 21)
            wall_instance.wh = (152, 38)
            objects.append(wall_instance)
            objects_map['fixed_wall 0'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (128, 101)
            wall_instance.wh = (32, 38)
            objects.append(wall_instance)
            objects_map['fixed_wall 1'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (68, 101)
            wall_instance.wh = (24, 38)
            objects.append(wall_instance)
            objects_map['fixed_wall 2'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (8, 101)
            wall_instance.wh = (24, 38)
            objects.append(wall_instance)
            objects_map['fixed_wall 3'] = wall_instance
            number_of_walls = 4
            i = 0
            while(objects_map.get(f"fixed wall {number_of_walls + i}")!= None):
                objects_map.pop(f"fixed wall {number_of_walls + i}")
                i += 1
        elif ram_state[28] == 7:
            wall_instance = Wall()
            wall_instance.xy = (128, 21)
            wall_instance.wh = (32, 38)
            objects.append(wall_instance)
            objects_map['fixed_wall 0'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (68, 21)
            wall_instance.wh = (24, 38)
            objects.append(wall_instance)
            objects_map['fixed_wall 1'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (8, 21)
            wall_instance.wh = (24, 38)
            objects.append(wall_instance)
            objects_map['fixed_wall 2'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (84, 101)
            wall_instance.wh = (76, 38)
            objects.append(wall_instance)
            objects_map['fixed_wall 3'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (8, 101)
            wall_instance.wh = (68, 38)
            objects.append(wall_instance)
            objects_map['fixed_wall 4'] = wall_instance
            number_of_walls = 5
            i = 0
            while(objects_map.get(f"fixed wall {number_of_walls + i}")!= None):
                objects_map.pop(f"fixed wall {number_of_walls + i}")
                i += 1
        elif ram_state[28] == 8:
            wall_instance = Wall()
            wall_instance.xy = (84, 21)
            wall_instance.wh = (76, 38)
            objects.append(wall_instance)
            objects_map['fixed_wall 0'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (8, 21)
            wall_instance.wh = (68, 38)
            objects.append(wall_instance)
            objects_map['fixed_wall 1'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (84, 101)
            wall_instance.wh = (76, 38)
            objects.append(wall_instance)
            objects_map['fixed_wall 2'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (8, 101)
            wall_instance.wh = (68, 38)
            objects.append(wall_instance)
            objects_map['fixed_wall 3'] = wall_instance
            number_of_walls = 4
            i = 0
            while(objects_map.get(f"fixed wall {number_of_walls + i}")!= None):
                objects_map.pop(f"fixed wall {number_of_walls + i}")
                i += 1
        elif ram_state[28] == 9:
            wall_instance = Wall()
            wall_instance.xy = (84, 21)
            wall_instance.wh = (76, 38)
            objects.append(wall_instance)
            objects_map['fixed_wall 0'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (8, 21)
            wall_instance.wh = (68, 38)
            objects.append(wall_instance)
            objects_map['fixed_wall 1'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (140, 101)
            wall_instance.wh = (20, 38)
            objects.append(wall_instance)
            objects_map['fixed_wall 2'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (112, 101)
            wall_instance.wh = (20, 38)
            objects.append(wall_instance)
            objects_map['fixed_wall 3'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (84, 101)
            wall_instance.wh = (20, 38)
            objects.append(wall_instance)
            objects_map['fixed_wall 4'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (56, 101)
            wall_instance.wh = (20, 38)
            objects.append(wall_instance)
            objects_map['fixed_wall 5'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (28, 101)
            wall_instance.wh = (20, 38)
            objects.append(wall_instance)
            objects_map['fixed_wall 6'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (8, 101)
            wall_instance.wh = (12, 38)
            objects.append(wall_instance)
            objects_map['fixed_wall 7'] = wall_instance
            number_of_walls = 8
            i = 0
            while(objects_map.get(f"fixed wall {number_of_walls + i}")!= None):
                objects_map.pop(f"fixed wall {number_of_walls + i}")
                i += 1
        elif ram_state[28] == 10:
            wall_instance = Wall()
            wall_instance.xy = (140, 21)
            wall_instance.wh = (20, 38)
            objects.append(wall_instance)
            objects_map['fixed_wall 0'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (112, 21)
            wall_instance.wh = (20, 38)
            objects.append(wall_instance)
            objects_map['fixed_wall 1'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (84, 21)
            wall_instance.wh = (20, 38)
            objects.append(wall_instance)
            objects_map['fixed_wall 2'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (56, 21)
            wall_instance.wh = (20, 38)
            objects.append(wall_instance)
            objects_map['fixed_wall 3'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (28, 21)
            wall_instance.wh = (20, 38)
            objects.append(wall_instance)
            objects_map['fixed_wall 4'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (8, 21)
            wall_instance.wh = (12, 38)
            objects.append(wall_instance)
            objects_map['fixed_wall 5'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (8, 101)
            wall_instance.wh = (152, 38)
            objects.append(wall_instance)
            objects_map['fixed_wall 6'] = wall_instance
            number_of_walls = 7
            i = 0
            while(objects_map.get(f"fixed wall {number_of_walls + i}")!= None):
                objects_map.pop(f"fixed wall {number_of_walls + i}")
                i += 1
        elif ram_state[28] == 11:
            wall_instance = Wall()
            wall_instance.xy = (8, 21)
            wall_instance.wh = (152, 38)
            objects.append(wall_instance)
            objects_map['fixed_wall 0'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (48, 61)
            wall_instance.wh = (64, 37)
            objects.append(wall_instance)
            objects_map['fixed_wall 1'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (132, 101)
            wall_instance.wh = (28, 38)
            objects.append(wall_instance)
            objects_map['fixed_wall 2'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (8, 101)
            wall_instance.wh = (20, 38)
            objects.append(wall_instance)
            objects_map['fixed_wall 3'] = wall_instance
            number_of_walls = 4
            i = 0
            while(objects_map.get(f"fixed wall {number_of_walls + i}")!= None):
                objects_map.pop(f"fixed wall {number_of_walls + i}")
                i += 1
        elif ram_state[28] == 12:
            wall_instance = Wall()
            wall_instance.xy = (8, 21)
            wall_instance.wh = (152, 38)
            objects.append(wall_instance)
            objects_map['fixed_wall 0'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (136, 101)
            wall_instance.wh = (24, 38)
            objects.append(wall_instance)
            objects_map['fixed_wall 1'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (8, 101)
            wall_instance.wh = (16, 38)
            objects.append(wall_instance)
            objects_map['fixed_wall 2'] = wall_instance
            number_of_walls = 3
            i = 0
            while(objects_map.get(f"fixed wall {number_of_walls + i}")!= None):
                objects_map.pop(f"fixed wall {number_of_walls + i}")
                i += 1
        elif ram_state[28] == 13:
            wall_instance = Wall()
            wall_instance.xy = (8, 21)
            wall_instance.wh = (152, 38)
            objects.append(wall_instance)
            objects_map['fixed_wall 0'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (132, 101)
            wall_instance.wh = (28, 38)
            objects.append(wall_instance)
            objects_map['fixed_wall 1'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (72, 101)
            wall_instance.wh = (16, 38)
            objects.append(wall_instance)
            objects_map['fixed_wall 2'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (8, 101)
            wall_instance.wh = (20, 38)
            objects.append(wall_instance)
            objects_map['fixed_wall 3'] = wall_instance
            number_of_walls = 4
            i = 0
            while(objects_map.get(f"fixed wall {number_of_walls + i}")!= None):
                objects_map.pop(f"fixed wall {number_of_walls + i}")
                i += 1
        elif ram_state[28] == 14:
            wall_instance = Wall()
            wall_instance.xy = (8, 21)
            wall_instance.wh = (152, 38)
            objects.append(wall_instance)
            objects_map['fixed_wall 0'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (112, 101)
            wall_instance.wh = (48, 38)
            objects.append(wall_instance)
            objects_map['fixed_wall 1'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (8, 101)
            wall_instance.wh = (40, 38)
            objects.append(wall_instance)
            objects_map['fixed_wall 2'] = wall_instance
            number_of_walls = 3
            i = 0
            while(objects_map.get(f"fixed wall {number_of_walls + i}")!= None):
                objects_map.pop(f"fixed wall {number_of_walls + i}")
                i += 1
        elif ram_state[28] == 15:
            wall_instance = Wall()
            wall_instance.xy = (8, 21)
            wall_instance.wh = (152, 38)
            objects.append(wall_instance)
            objects_map['fixed_wall 0'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (120, 101)
            wall_instance.wh = (40, 38)
            objects.append(wall_instance)
            objects_map['fixed_wall 1'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (8, 101)
            wall_instance.wh = (32, 38)
            objects.append(wall_instance)
            objects_map['fixed_wall 2'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (72, 61)
            wall_instance.wh = (16, 37)
            objects.append(wall_instance)
            objects_map['fixed_wall 3'] = wall_instance
            number_of_walls = 4
            i = 0
            while(objects_map.get(f"fixed wall {number_of_walls + i}")!= None):
                objects_map.pop(f"fixed wall {number_of_walls + i}")
                i += 1

    elif ram_state[117] == 18:
        if ram_state[28] == 0:
            wall_instance = Wall()
            wall_instance.xy = (136, 21)
            wall_instance.wh = (24, 38)
            objects.append(wall_instance)
            objects_map['fixed_wall 0'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (8, 21)
            wall_instance.wh = (16, 38)
            objects.append(wall_instance)
            objects_map['fixed_wall 1'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (84, 101)
            wall_instance.wh = (76, 38)
            objects.append(wall_instance)
            objects_map['fixed_wall 2'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (8, 101)
            wall_instance.wh = (68, 38)
            objects.append(wall_instance)
            objects_map['fixed_wall 3'] = wall_instance
            number_of_walls = 4
            i = 0
            while(objects_map.get(f"fixed wall {number_of_walls + i}")!= None):
                objects_map.pop(f"fixed wall {number_of_walls + i}")
                i += 1
        elif ram_state[28] == 1:
            wall_instance = Wall()
            wall_instance.xy = (84, 21)
            wall_instance.wh = (76, 38)
            objects.append(wall_instance)
            objects_map['fixed_wall 0'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (8, 21)
            wall_instance.wh = (68, 38)
            objects.append(wall_instance)
            objects_map['fixed_wall 1'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (120, 101)
            wall_instance.wh = (40, 38)
            objects.append(wall_instance)
            objects_map['fixed_wall 2'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (48, 101)
            wall_instance.wh = (64, 38)
            objects.append(wall_instance)
            objects_map['fixed_wall 3'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (8, 101)
            wall_instance.wh = (32, 38)
            objects.append(wall_instance)
            objects_map['fixed_wall 4'] = wall_instance
            number_of_walls = 5
            i = 0
            while(objects_map.get(f"fixed wall {number_of_walls + i}")!= None):
                objects_map.pop(f"fixed wall {number_of_walls + i}")
                i += 1
        elif ram_state[28] == 2:
            wall_instance = Wall()
            wall_instance.xy = (120, 21)
            wall_instance.wh = (40, 38)
            objects.append(wall_instance)
            objects_map['fixed_wall 0'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (48, 21)
            wall_instance.wh = (64, 38)
            objects.append(wall_instance)
            objects_map['fixed_wall 1'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (8, 21)
            wall_instance.wh = (32, 38)
            objects.append(wall_instance)
            objects_map['fixed_wall 2'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (100, 101)
            wall_instance.wh = (60, 38)
            objects.append(wall_instance)
            objects_map['fixed_wall 3'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (8, 101)
            wall_instance.wh = (52, 38)
            objects.append(wall_instance)
            objects_map['fixed_wall 4'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (148, 61)
            wall_instance.wh = (12, 37)
            objects.append(wall_instance)
            objects_map['fixed_wall 5'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (68, 61)
            wall_instance.wh = (40, 37)
            objects.append(wall_instance)
            objects_map['fixed_wall 6'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (8, 61)
            wall_instance.wh = (20, 37)
            objects.append(wall_instance)
            objects_map['fixed_wall 7'] = wall_instance
            number_of_walls = 8
            i = 0
            while(objects_map.get(f"fixed wall {number_of_walls + i}")!= None):
                objects_map.pop(f"fixed wall {number_of_walls + i}")
                i += 1
        elif ram_state[28] == 3:
            wall_instance = Wall()
            wall_instance.xy = (100, 21)
            wall_instance.wh = (60, 38)
            objects.append(wall_instance)
            objects_map['fixed_wall 0'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (8, 21)
            wall_instance.wh = (52, 38)
            objects.append(wall_instance)
            objects_map['fixed_wall 1'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (144, 101)
            wall_instance.wh = (16, 38)
            objects.append(wall_instance)
            objects_map['fixed_wall 2'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (44, 101)
            wall_instance.wh = (72, 38)
            objects.append(wall_instance)
            objects_map['fixed_wall 3'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (8, 101)
            wall_instance.wh = (8, 38)
            objects.append(wall_instance)
            objects_map['fixed_wall 4'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (128, 61)
            wall_instance.wh = (32, 37)
            objects.append(wall_instance)
            objects_map['fixed_wall 5'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (8, 61)
            wall_instance.wh = (24, 37)
            objects.append(wall_instance)
            objects_map['fixed_wall 6'] = wall_instance
            number_of_walls = 7
            i = 0
            while(objects_map.get(f"fixed wall {number_of_walls + i}")!= None):
                objects_map.pop(f"fixed wall {number_of_walls + i}")
                i += 1
        elif ram_state[28] == 4:
            wall_instance = Wall()
            wall_instance.xy = (144, 21)
            wall_instance.wh = (16, 38)
            objects.append(wall_instance)
            objects_map['fixed_wall 0'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (44, 21)
            wall_instance.wh = (72, 38)
            objects.append(wall_instance)
            objects_map['fixed_wall 1'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (8, 21)
            wall_instance.wh = (8, 38)
            objects.append(wall_instance)
            objects_map['fixed_wall 2'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (144, 101)
            wall_instance.wh = (16, 38)
            objects.append(wall_instance)
            objects_map['fixed_wall 3'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (36, 101)
            wall_instance.wh = (88, 38)
            objects.append(wall_instance)
            objects_map['fixed_wall 4'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (8, 101)
            wall_instance.wh = (8, 38)
            objects.append(wall_instance)
            objects_map['fixed_wall 5'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (136, 61)
            wall_instance.wh = (24, 37)
            objects.append(wall_instance)
            objects_map['fixed_wall 6'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (56, 61)
            wall_instance.wh = (64, 37)
            objects.append(wall_instance)
            objects_map['fixed_wall 7'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (8, 61)
            wall_instance.wh = (32, 37)
            objects.append(wall_instance)
            objects_map['fixed_wall 8'] = wall_instance
            number_of_walls = 9
            i = 0
            while(objects_map.get(f"fixed wall {number_of_walls + i}")!= None):
                objects_map.pop(f"fixed wall {number_of_walls + i}")
                i += 1
        elif ram_state[28] == 5:
            wall_instance = Wall()
            wall_instance.xy = (144, 21)
            wall_instance.wh = (16, 38)
            objects.append(wall_instance)
            objects_map['fixed_wall 0'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (36, 21)
            wall_instance.wh = (88, 38)
            objects.append(wall_instance)
            objects_map['fixed_wall 1'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (8, 21)
            wall_instance.wh = (8, 38)
            objects.append(wall_instance)
            objects_map['fixed_wall 2'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (84, 101)
            wall_instance.wh = (76, 38)
            objects.append(wall_instance)
            objects_map['fixed_wall 3'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (8, 101)
            wall_instance.wh = (68, 38)
            objects.append(wall_instance)
            objects_map['fixed_wall 4'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (136, 61)
            wall_instance.wh = (24, 37)
            objects.append(wall_instance)
            objects_map['fixed_wall 5'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (8, 61)
            wall_instance.wh = (16, 37)
            objects.append(wall_instance)
            objects_map['fixed_wall 6'] = wall_instance
            number_of_walls = 7
            i = 0
            while(objects_map.get(f"fixed wall {number_of_walls + i}")!= None):
                objects_map.pop(f"fixed wall {number_of_walls + i}")
                i += 1
        elif ram_state[28] == 6:
            wall_instance = Wall()
            wall_instance.xy = (84, 21)
            wall_instance.wh = (76, 38)
            objects.append(wall_instance)
            objects_map['fixed_wall 0'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (8, 21)
            wall_instance.wh = (68, 38)
            objects.append(wall_instance)
            objects_map['fixed_wall 1'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (112, 101)
            wall_instance.wh = (48, 38)
            objects.append(wall_instance)
            objects_map['fixed_wall 2'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (8, 101)
            wall_instance.wh = (40, 38)
            objects.append(wall_instance)
            objects_map['fixed_wall 3'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (88, 61)
            wall_instance.wh = (72, 37)
            objects.append(wall_instance)
            objects_map['fixed_wall 4'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (8, 61)
            wall_instance.wh = (64, 37)
            objects.append(wall_instance)
            objects_map['fixed_wall 5'] = wall_instance
            number_of_walls = 6
            i = 0
            while(objects_map.get(f"fixed wall {number_of_walls + i}")!= None):
                objects_map.pop(f"fixed wall {number_of_walls + i}")
                i += 1
        elif ram_state[28] == 7:
            wall_instance = Wall()
            wall_instance.xy = (112, 21)
            wall_instance.wh = (48, 38)
            objects.append(wall_instance)
            objects_map['fixed_wall 0'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (8, 21)
            wall_instance.wh = (40, 38)
            objects.append(wall_instance)
            objects_map['fixed_wall 1'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (152, 61)
            wall_instance.wh = (8, 37)
            objects.append(wall_instance)
            objects_map['fixed_wall 2'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (72, 61)
            wall_instance.wh = (48, 37)
            objects.append(wall_instance)
            objects_map['fixed_wall 3'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (8, 61)
            wall_instance.wh = (32, 37)
            objects.append(wall_instance)
            objects_map['fixed_wall 4'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (116, 101)
            wall_instance.wh = (44, 38)
            objects.append(wall_instance)
            objects_map['fixed_wall 5'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (8, 101)
            wall_instance.wh = (36, 38)
            objects.append(wall_instance)
            objects_map['fixed_wall 6'] = wall_instance
            number_of_walls = 7
            i = 0
            while(objects_map.get(f"fixed wall {number_of_walls + i}")!= None):
                objects_map.pop(f"fixed wall {number_of_walls + i}")
                i += 1
        elif ram_state[28] == 8:
            wall_instance = Wall()
            wall_instance.xy = (116, 21)
            wall_instance.wh = (44, 38)
            objects.append(wall_instance)
            objects_map['fixed_wall 0'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (8, 21)
            wall_instance.wh = (36, 38)
            objects.append(wall_instance)
            objects_map['fixed_wall 1'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (144, 101)
            wall_instance.wh = (16, 38)
            objects.append(wall_instance)
            objects_map['fixed_wall 2'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (8, 101)
            wall_instance.wh = (8, 38)
            objects.append(wall_instance)
            objects_map['fixed_wall 3'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (88, 61)
            wall_instance.wh = (72, 37)
            objects.append(wall_instance)
            objects_map['fixed_wall 4'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (8, 61)
            wall_instance.wh = (64, 37)
            objects.append(wall_instance)
            objects_map['fixed_wall 5'] = wall_instance
            number_of_walls = 6
            i = 0
            while(objects_map.get(f"fixed wall {number_of_walls + i}")!= None):
                objects_map.pop(f"fixed wall {number_of_walls + i}")
                i += 1
        elif ram_state[28] == 9:
            wall_instance = Wall()
            wall_instance.xy = (144, 21)
            wall_instance.wh = (16, 38)
            objects.append(wall_instance)
            objects_map['fixed_wall 0'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (8, 21)
            wall_instance.wh = (8, 38)
            objects.append(wall_instance)
            objects_map['fixed_wall 1'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (128, 101)
            wall_instance.wh = (32, 38)
            objects.append(wall_instance)
            objects_map['fixed_wall 2'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (8, 101)
            wall_instance.wh = (24, 38)
            objects.append(wall_instance)
            objects_map['fixed_wall 3'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (96, 61)
            wall_instance.wh = (64, 37)
            objects.append(wall_instance)
            objects_map['fixed_wall 4'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (72, 61)
            wall_instance.wh = (16, 37)
            objects.append(wall_instance)
            objects_map['fixed_wall 5'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (8, 61)
            wall_instance.wh = (56, 37)
            objects.append(wall_instance)
            objects_map['fixed_wall 6'] = wall_instance
            number_of_walls = 7
            i = 0
            while(objects_map.get(f"fixed wall {number_of_walls + i}")!= None):
                objects_map.pop(f"fixed wall {number_of_walls + i}")
                i += 1
        elif ram_state[28] == 10:
            wall_instance = Wall()
            wall_instance.xy = (128, 21)
            wall_instance.wh = (32, 38)
            objects.append(wall_instance)
            objects_map['fixed_wall 0'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (8, 21)
            wall_instance.wh = (24, 38)
            objects.append(wall_instance)
            objects_map['fixed_wall 1'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (92, 61)
            wall_instance.wh = (40, 37)
            objects.append(wall_instance)
            objects_map['fixed_wall 2'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (28, 61)
            wall_instance.wh = (40, 37)
            objects.append(wall_instance)
            objects_map['fixed_wall 3'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (140, 101)
            wall_instance.wh = (20, 38)
            objects.append(wall_instance)
            objects_map['fixed_wall 4'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (8, 101)
            wall_instance.wh = (12, 38)
            objects.append(wall_instance)
            objects_map['fixed_wall 5'] = wall_instance
            number_of_walls = 6
            i = 0
            while(objects_map.get(f"fixed wall {number_of_walls + i}")!= None):
                objects_map.pop(f"fixed wall {number_of_walls + i}")
                i += 1
        elif ram_state[28] == 11:
            wall_instance = Wall()
            wall_instance.xy = (8, 21)
            wall_instance.wh = (152, 38)
            objects.append(wall_instance)
            objects_map['fixed_wall 0'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (56, 61)
            wall_instance.wh = (48, 37)
            objects.append(wall_instance)
            objects_map['fixed_wall 1'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (132, 101)
            wall_instance.wh = (28, 38)
            objects.append(wall_instance)
            objects_map['fixed_wall 2'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (8, 101)
            wall_instance.wh = (20, 38)
            objects.append(wall_instance)
            objects_map['fixed_wall 3'] = wall_instance
            number_of_walls = 4
            i = 0
            while(objects_map.get(f"fixed wall {number_of_walls + i}")!= None):
                objects_map.pop(f"fixed wall {number_of_walls + i}")
                i += 1
        elif ram_state[28] == 12:
            wall_instance = Wall()
            wall_instance.xy = (8, 21)
            wall_instance.wh = (152, 38)
            objects.append(wall_instance)
            objects_map['fixed_wall 0'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (136, 101)
            wall_instance.wh = (24, 38)
            objects.append(wall_instance)
            objects_map['fixed_wall 1'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (8, 101)
            wall_instance.wh = (16, 38)
            objects.append(wall_instance)
            objects_map['fixed_wall 2'] = wall_instance
            number_of_walls = 3
            i = 0
            while(objects_map.get(f"fixed wall {number_of_walls + i}")!= None):
                objects_map.pop(f"fixed wall {number_of_walls + i}")
                i += 1
        elif ram_state[28] == 13:
            wall_instance = Wall()
            wall_instance.xy = (8, 21)
            wall_instance.wh = (152, 38)
            objects.append(wall_instance)
            objects_map['fixed_wall 0'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (128, 101)
            wall_instance.wh = (32, 38)
            objects.append(wall_instance)
            objects_map['fixed_wall 1'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (72, 101)
            wall_instance.wh = (16, 38)
            objects.append(wall_instance)
            objects_map['fixed_wall 2'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (8, 101)
            wall_instance.wh = (24, 38)
            objects.append(wall_instance)
            objects_map['fixed_wall 3'] = wall_instance
            number_of_walls = 4
            i = 0
            while(objects_map.get(f"fixed wall {number_of_walls + i}")!= None):
                objects_map.pop(f"fixed wall {number_of_walls + i}")
                i += 1
        elif ram_state[28] == 14:
            wall_instance = Wall()
            wall_instance.xy = (8, 21)
            wall_instance.wh = (152, 38)
            objects.append(wall_instance)
            objects_map['fixed_wall 0'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (132, 101)
            wall_instance.wh = (28, 38)
            objects.append(wall_instance)
            objects_map['fixed_wall 1'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (8, 101)
            wall_instance.wh = (20, 38)
            objects.append(wall_instance)
            objects_map['fixed_wall 2'] = wall_instance
            number_of_walls = 3
            i = 0
            while(objects_map.get(f"fixed wall {number_of_walls + i}")!= None):
                objects_map.pop(f"fixed wall {number_of_walls + i}")
                i += 1
        elif ram_state[28] == 15:
            wall_instance = Wall()
            wall_instance.xy = (8, 21)
            wall_instance.wh = (152, 38)
            objects.append(wall_instance)
            objects_map['fixed_wall 0'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (112, 101)
            wall_instance.wh = (48, 38)
            objects.append(wall_instance)
            objects_map['fixed_wall 1'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (8, 101)
            wall_instance.wh = (40, 38)
            objects.append(wall_instance)
            objects_map['fixed_wall 2'] = wall_instance
            number_of_walls = 3
            i = 0
            while(objects_map.get(f"fixed wall {number_of_walls + i}")!= None):
                objects_map.pop(f"fixed wall {number_of_walls + i}")
                i += 1

    elif ram_state[117] == 19:
        if ram_state[28] == 0:
            wall_instance = Wall()
            wall_instance.xy = (136, 21)
            wall_instance.wh = (24, 38)
            objects.append(wall_instance)
            objects_map['fixed_wall 0'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (8, 21)
            wall_instance.wh = (16, 38)
            objects.append(wall_instance)
            objects_map['fixed_wall 1'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (84, 101)
            wall_instance.wh = (76, 38)
            objects.append(wall_instance)
            objects_map['fixed_wall 2'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (8, 101)
            wall_instance.wh = (68, 38)
            objects.append(wall_instance)
            objects_map['fixed_wall 3'] = wall_instance
            number_of_walls = 4
            i = 0
            while(objects_map.get(f"fixed wall {number_of_walls + i}")!= None):
                objects_map.pop(f"fixed wall {number_of_walls + i}")
                i += 1
        elif ram_state[28] == 1:
            wall_instance = Wall()
            wall_instance.xy = (84, 21)
            wall_instance.wh = (76, 38)
            objects.append(wall_instance)
            objects_map['fixed_wall 0'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (8, 21)
            wall_instance.wh = (68, 38)
            objects.append(wall_instance)
            objects_map['fixed_wall 1'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (136, 101)
            wall_instance.wh = (24, 38)
            objects.append(wall_instance)
            objects_map['fixed_wall 2'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (48, 101)
            wall_instance.wh = (64, 38)
            objects.append(wall_instance)
            objects_map['fixed_wall 3'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (8, 101)
            wall_instance.wh = (16, 38)
            objects.append(wall_instance)
            objects_map['fixed_wall 4'] = wall_instance
            number_of_walls = 5
            i = 0
            while(objects_map.get(f"fixed wall {number_of_walls + i}")!= None):
                objects_map.pop(f"fixed wall {number_of_walls + i}")
                i += 1
        elif ram_state[28] == 2:
            wall_instance = Wall()
            wall_instance.xy = (136, 21)
            wall_instance.wh = (24, 38)
            objects.append(wall_instance)
            objects_map['fixed_wall 0'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (48, 21)
            wall_instance.wh = (64, 38)
            objects.append(wall_instance)
            objects_map['fixed_wall 1'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (8, 21)
            wall_instance.wh = (16, 38)
            objects.append(wall_instance)
            objects_map['fixed_wall 2'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (128, 61)
            wall_instance.wh = (32, 37)
            objects.append(wall_instance)
            objects_map['fixed_wall 3'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (40, 61)
            wall_instance.wh = (80, 37)
            objects.append(wall_instance)
            objects_map['fixed_wall 4'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (8, 61)
            wall_instance.wh = (24, 37)
            objects.append(wall_instance)
            objects_map['fixed_wall 5'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (144, 101)
            wall_instance.wh = (16, 38)
            objects.append(wall_instance)
            objects_map['fixed_wall 6'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (8, 101)
            wall_instance.wh = (8, 38)
            objects.append(wall_instance)
            objects_map['fixed_wall 7'] = wall_instance
            number_of_walls = 8
            i = 0
            while(objects_map.get(f"fixed wall {number_of_walls + i}")!= None):
                objects_map.pop(f"fixed wall {number_of_walls + i}")
                i += 1
        elif ram_state[28] == 3:
            wall_instance = Wall()
            wall_instance.xy = (144, 21)
            wall_instance.wh = (16, 38)
            objects.append(wall_instance)
            objects_map['fixed_wall 0'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (8, 21)
            wall_instance.wh = (8, 38)
            objects.append(wall_instance)
            objects_map['fixed_wall 1'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (144, 101)
            wall_instance.wh = (16, 38)
            objects.append(wall_instance)
            objects_map['fixed_wall 2'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (8, 101)
            wall_instance.wh = (8, 38)
            objects.append(wall_instance)
            objects_map['fixed_wall 3'] = wall_instance
            number_of_walls = 4
            i = 0
            while(objects_map.get(f"fixed wall {number_of_walls + i}")!= None):
                objects_map.pop(f"fixed wall {number_of_walls + i}")
                i += 1
        elif ram_state[28] == 4:
            wall_instance = Wall()
            wall_instance.xy = (144, 21)
            wall_instance.wh = (16, 38)
            objects.append(wall_instance)
            objects_map['fixed_wall 0'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (8, 21)
            wall_instance.wh = (8, 38)
            objects.append(wall_instance)
            objects_map['fixed_wall 1'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (144, 101)
            wall_instance.wh = (16, 38)
            objects.append(wall_instance)
            objects_map['fixed_wall 2'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (8, 101)
            wall_instance.wh = (8, 38)
            objects.append(wall_instance)
            objects_map['fixed_wall 3'] = wall_instance
            number_of_walls = 4
            i = 0
            while(objects_map.get(f"fixed wall {number_of_walls + i}")!= None):
                objects_map.pop(f"fixed wall {number_of_walls + i}")
                i += 1
        elif ram_state[28] == 5:
            wall_instance = Wall()
            wall_instance.xy = (144, 21)
            wall_instance.wh = (16, 38)
            objects.append(wall_instance)
            objects_map['fixed_wall 0'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (8, 21)
            wall_instance.wh = (8, 38)
            objects.append(wall_instance)
            objects_map['fixed_wall 1'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (136, 101)
            wall_instance.wh = (24, 38)
            objects.append(wall_instance)
            objects_map['fixed_wall 2'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (8, 101)
            wall_instance.wh = (16, 38)
            objects.append(wall_instance)
            objects_map['fixed_wall 3'] = wall_instance
            number_of_walls = 4
            i = 0
            while(objects_map.get(f"fixed wall {number_of_walls + i}")!= None):
                objects_map.pop(f"fixed wall {number_of_walls + i}")
                i += 1
        elif ram_state[28] == 6:
            wall_instance = Wall()
            wall_instance.xy = (136, 21)
            wall_instance.wh = (24, 38)
            objects.append(wall_instance)
            objects_map['fixed_wall 0'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (8, 21)
            wall_instance.wh = (16, 38)
            objects.append(wall_instance)
            objects_map['fixed_wall 1'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (120, 101)
            wall_instance.wh = (40, 38)
            objects.append(wall_instance)
            objects_map['fixed_wall 2'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (8, 101)
            wall_instance.wh = (32, 38)
            objects.append(wall_instance)
            objects_map['fixed_wall 3'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (144, 61)
            wall_instance.wh = (16, 37)
            objects.append(wall_instance)
            objects_map['fixed_wall 4'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (48, 61)
            wall_instance.wh = (64, 37)
            objects.append(wall_instance)
            objects_map['fixed_wall 5'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (8, 61)
            wall_instance.wh = (8, 37)
            objects.append(wall_instance)
            objects_map['fixed_wall 6'] = wall_instance
            number_of_walls = 7
            i = 0
            while(objects_map.get(f"fixed wall {number_of_walls + i}")!= None):
                objects_map.pop(f"fixed wall {number_of_walls + i}")
                i += 1
        elif ram_state[28] == 7:
            wall_instance = Wall()
            wall_instance.xy = (120, 21)
            wall_instance.wh = (40, 38)
            objects.append(wall_instance)
            objects_map['fixed_wall 0'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (8, 21)
            wall_instance.wh = (32, 38)
            objects.append(wall_instance)
            objects_map['fixed_wall 1'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (136, 101)
            wall_instance.wh = (24, 38)
            objects.append(wall_instance)
            objects_map['fixed_wall 2'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (64, 101)
            wall_instance.wh = (32, 38)
            objects.append(wall_instance)
            objects_map['fixed_wall 3'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (8, 101)
            wall_instance.wh = (16, 38)
            objects.append(wall_instance)
            objects_map['fixed_wall 4'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (112, 61)
            wall_instance.wh = (48, 37)
            objects.append(wall_instance)
            objects_map['fixed_wall 5'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (56, 61)
            wall_instance.wh = (48, 37)
            objects.append(wall_instance)
            objects_map['fixed_wall 6'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (8, 61)
            wall_instance.wh = (40, 37)
            objects.append(wall_instance)
            objects_map['fixed_wall 7'] = wall_instance
            number_of_walls = 8
            i = 0
            while(objects_map.get(f"fixed wall {number_of_walls + i}")!= None):
                objects_map.pop(f"fixed wall {number_of_walls + i}")
                i += 1
        elif ram_state[28] == 8:
            wall_instance = Wall()
            wall_instance.xy = (136, 21)
            wall_instance.wh = (24, 38)
            objects.append(wall_instance)
            objects_map['fixed_wall 0'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (64, 21)
            wall_instance.wh = (32, 38)
            objects.append(wall_instance)
            objects_map['fixed_wall 1'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (8, 21)
            wall_instance.wh = (16, 38)
            objects.append(wall_instance)
            objects_map['fixed_wall 2'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (128, 101)
            wall_instance.wh = (32, 38)
            objects.append(wall_instance)
            objects_map['fixed_wall 3'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (64, 101)
            wall_instance.wh = (32, 38)
            objects.append(wall_instance)
            objects_map['fixed_wall 4'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (8, 101)
            wall_instance.wh = (24, 38)
            objects.append(wall_instance)
            objects_map['fixed_wall 5'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (144, 61)
            wall_instance.wh = (16, 37)
            objects.append(wall_instance)
            objects_map['fixed_wall 6'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (56, 61)
            wall_instance.wh = (48, 37)
            objects.append(wall_instance)
            objects_map['fixed_wall 7'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (8, 61)
            wall_instance.wh = (8, 37)
            objects.append(wall_instance)
            objects_map['fixed_wall 8'] = wall_instance
            number_of_walls = 9
            i = 0
            while(objects_map.get(f"fixed wall {number_of_walls + i}")!= None):
                objects_map.pop(f"fixed wall {number_of_walls + i}")
                i += 1
        elif ram_state[28] == 9:
            wall_instance = Wall()
            wall_instance.xy = (128, 21)
            wall_instance.wh = (32, 38)
            objects.append(wall_instance)
            objects_map['fixed_wall 0'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (64, 21)
            wall_instance.wh = (32, 38)
            objects.append(wall_instance)
            objects_map['fixed_wall 1'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (8, 21)
            wall_instance.wh = (24, 38)
            objects.append(wall_instance)
            objects_map['fixed_wall 2'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (140, 101)
            wall_instance.wh = (20, 38)
            objects.append(wall_instance)
            objects_map['fixed_wall 3'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (64, 101)
            wall_instance.wh = (32, 38)
            objects.append(wall_instance)
            objects_map['fixed_wall 4'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (8, 101)
            wall_instance.wh = (12, 38)
            objects.append(wall_instance)
            objects_map['fixed_wall 5'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (112, 61)
            wall_instance.wh = (48, 37)
            objects.append(wall_instance)
            objects_map['fixed_wall 6'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (56, 61)
            wall_instance.wh = (48, 37)
            objects.append(wall_instance)
            objects_map['fixed_wall 7'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (8, 61)
            wall_instance.wh = (40, 37)
            objects.append(wall_instance)
            objects_map['fixed_wall 8'] = wall_instance
            number_of_walls = 9
            i = 0
            while(objects_map.get(f"fixed wall {number_of_walls + i}")!= None):
                objects_map.pop(f"fixed wall {number_of_walls + i}")
                i += 1
        elif ram_state[28] == 10:
            wall_instance = Wall()
            wall_instance.xy = (140, 21)
            wall_instance.wh = (20, 38)
            objects.append(wall_instance)
            objects_map['fixed_wall 0'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (64, 21)
            wall_instance.wh = (32, 38)
            objects.append(wall_instance)
            objects_map['fixed_wall 1'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (8, 21)
            wall_instance.wh = (12, 38)
            objects.append(wall_instance)
            objects_map['fixed_wall 2'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (32, 61)
            wall_instance.wh = (96, 37)
            objects.append(wall_instance)
            objects_map['fixed_wall 3'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (140, 101)
            wall_instance.wh = (20, 38)
            objects.append(wall_instance)
            objects_map['fixed_wall 4'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (8, 101)
            wall_instance.wh = (12, 38)
            objects.append(wall_instance)
            objects_map['fixed_wall 5'] = wall_instance
            number_of_walls = 6
            i = 0
            while(objects_map.get(f"fixed wall {number_of_walls + i}")!= None):
                objects_map.pop(f"fixed wall {number_of_walls + i}")
                i += 1
        elif ram_state[28] == 11:
            wall_instance = Wall()
            wall_instance.xy = (8, 21)
            wall_instance.wh = (152, 38)
            objects.append(wall_instance)
            objects_map['fixed_wall 0'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (136, 101)
            wall_instance.wh = (24, 38)
            objects.append(wall_instance)
            objects_map['fixed_wall 1'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (8, 101)
            wall_instance.wh = (16, 38)
            objects.append(wall_instance)
            objects_map['fixed_wall 2'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (40, 61)
            wall_instance.wh = (80, 37)
            objects.append(wall_instance)
            objects_map['fixed_wall 3'] = wall_instance
            number_of_walls = 4
            i = 0
            while(objects_map.get(f"fixed wall {number_of_walls + i}")!= None):
                objects_map.pop(f"fixed wall {number_of_walls + i}")
                i += 1
        elif ram_state[28] == 12:
            wall_instance = Wall()
            wall_instance.xy = (8, 21)
            wall_instance.wh = (152, 38)
            objects.append(wall_instance)
            objects_map['fixed_wall 0'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (132, 101)
            wall_instance.wh = (28, 38)
            objects.append(wall_instance)
            objects_map['fixed_wall 1'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (8, 101)
            wall_instance.wh = (20, 38)
            objects.append(wall_instance)
            objects_map['fixed_wall 2'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (72, 61)
            wall_instance.wh = (16, 37)
            objects.append(wall_instance)
            objects_map['fixed_wall 3'] = wall_instance
            number_of_walls = 4
            i = 0
            while(objects_map.get(f"fixed wall {number_of_walls + i}")!= None):
                objects_map.pop(f"fixed wall {number_of_walls + i}")
                i += 1
        elif ram_state[28] == 13:
            wall_instance = Wall()
            wall_instance.xy = (8, 21)
            wall_instance.wh = (152, 38)
            objects.append(wall_instance)
            objects_map['fixed_wall 0'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (128, 101)
            wall_instance.wh = (32, 38)
            objects.append(wall_instance)
            objects_map['fixed_wall 1'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (8, 101)
            wall_instance.wh = (24, 38)
            objects.append(wall_instance)
            objects_map['fixed_wall 2'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (64, 61)
            wall_instance.wh = (32, 37)
            objects.append(wall_instance)
            objects_map['fixed_wall 3'] = wall_instance
            number_of_walls = 4
            i = 0
            while(objects_map.get(f"fixed wall {number_of_walls + i}")!= None):
                objects_map.pop(f"fixed wall {number_of_walls + i}")
                i += 1
        elif ram_state[28] == 14:
            wall_instance = Wall()
            wall_instance.xy = (8, 21)
            wall_instance.wh = (152, 38)
            objects.append(wall_instance)
            objects_map['fixed_wall 0'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (132, 101)
            wall_instance.wh = (28, 38)
            objects.append(wall_instance)
            objects_map['fixed_wall 1'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (8, 101)
            wall_instance.wh = (20, 38)
            objects.append(wall_instance)
            objects_map['fixed_wall 2'] = wall_instance
            number_of_walls = 3
            i = 0
            while(objects_map.get(f"fixed wall {number_of_walls + i}")!= None):
                objects_map.pop(f"fixed wall {number_of_walls + i}")
                i += 1
        elif ram_state[28] == 15:
            wall_instance = Wall()
            wall_instance.xy = (8, 21)
            wall_instance.wh = (152, 38)
            objects.append(wall_instance)
            objects_map['fixed_wall 0'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (112, 101)
            wall_instance.wh = (48, 38)
            objects.append(wall_instance)
            objects_map['fixed_wall 1'] = wall_instance
            wall_instance = Wall()
            wall_instance.xy = (8, 101)
            wall_instance.wh = (40, 38)
            objects.append(wall_instance)
            objects_map['fixed_wall 2'] = wall_instance
            number_of_walls = 3
            i = 0
            while(objects_map.get(f"fixed wall {number_of_walls + i}")!= None):
                objects_map.pop(f"fixed wall {number_of_walls + i}")
                i += 1

    return objects, objects_map
