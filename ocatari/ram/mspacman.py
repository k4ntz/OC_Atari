from .game_objects import GameObject


class Player(GameObject):
    def __init__(self):
        super(Player, self).__init__()
        self.visible = True
        self._xy = 78, 103
        self.wh = 9, 10
        self.rgb = 210, 164, 74
        self.hud = False


class Ghost(GameObject):
    def __init__(self, *args, **kwargs):
        super(Ghost, self).__init__()
        super().__init__(*args, **kwargs)
        self.visible = True
        self._xy = 79, 57
        self.wh = 9, 10
        self.rgb = 200, 72, 72
        self.hud = False


class Fruit(GameObject):
    def __init__(self, *args, **kwargs):
        super(Fruit, self).__init__()
        self.visible = True
        self._xy = 125, 173
        self.wh = 9, 10
        self.rgb = 184, 50, 50
        self.hud = False


class Score(GameObject):
    def __init__(self, *args, **kwargs):
        super(Score, self).__init__()
        self.visible = True
        self._xy = 95, 187
        self.wh = 7, 7
        self.rgb = 195, 144, 61
        self.hud = True


class Life(GameObject):
    def __init__(self, *args, **kwargs):
        super(Life, self).__init__()
        self.visible = True
        self._xy = 12, 171
        self.wh = 9, 10
        self.rgb = 187, 187, 53
        self.hud = True


def _init_objects_mspacman_ram(hud=False):
    """
    (Re)Initialize the objects
    """

    objects = [Player(), Ghost(), Ghost(), Ghost(), Ghost(), Fruit()]

    if hud:
        x = 95
        for i in range(6):
            score = Score()
            score.xy = x, 187
            objects.append(score)
            x -= 8

        x = 12
        for i in range(3):
            life = Life()
            life.xy = x, 173
            objects.append(life)
            x += 15
        objects.append(Fruit())

    return objects


def _detect_objects_mspacman_revised(objects, ram_state, hud=True):
    player, g1, g2, g3, g4, fruit = objects[:6]

    player.xy = ram_state[10] - 13, ram_state[16] + 1

    g1.xy = ram_state[6] - 13, ram_state[12] + 1
    g1.rgb = 180, 122, 48
    g2.xy = ram_state[7] - 13, ram_state[13] + 1
    g2.rgb = 84, 184, 153
    g3.xy = ram_state[8] - 13, ram_state[14] + 1
    g3.rgb = 198, 89, 179
    g4.xy = ram_state[9] - 13, ram_state[15] + 1
    # no rgb adjustment, since this colour is the default one

    if ram_state[11] > 0 and ram_state[17] > 0:
        fruit.xy = ram_state[11] - 13, ram_state[17] + 1
        fruit.rgb = get_fruit_rgb(ram_state[123])
    else:
        fruit.visible = False

    if hud:
        if ram_state[122] < 16:
            objects[11].visible = False
            if ram_state[122] == 0:
                objects[10].visible = False
                if ram_state[121] < 16:
                    objects[9].visible = False
                    if ram_state[121] == 0:
                        objects[8].visible = False
                        if ram_state[120] < 16:
                            objects[7].visible = False

        if ram_state[123] <= 2:
            objects[14].visible = False
            if ram_state[123] <= 1:
                objects[13].visible = False
                if ram_state[123] == 0:
                    objects[12].visible = False

        objects[15].rgb = get_fruit_rgb(ram_state[123])


def _detect_objects_mspacman_raw(info, ram_state):
    """
    returns unprocessed list with
    player_x, player_y, ghosts_position_x, enemy_position_y, fruit_x, fruit_y
    """

    object_info = {}
    object_info["player_x"] = ram_state[10]
    object_info["player_y"] = ram_state[16]
    object_info["enemy_amount"] = ram_state[19]
    object_info["ghosts_position_x"] = {"orange": ram_state[6],
                                        "cyan": ram_state[7],
                                        "pink": ram_state[8],
                                        "red": ram_state[9]
                                        }
    object_info["enemy_position_y"] = {"orange": ram_state[12],
                                       "cyan": ram_state[13],
                                       "pink": ram_state[14],
                                       "red": ram_state[15]
                                       }
    object_info["fruit_x"] = ram_state[11]
    object_info["fruit_y"] = ram_state[17]
    info["object-list"] = object_info


def get_fruit_rgb(ram_state):

    """
    every value of 112 and above will result in a glitched fruit
    """

    if ram_state < 16:
        return 184, 50, 50   # "cherry"
    elif ram_state < 32:
        return 184, 50, 50   # "strawberry"
    elif ram_state < 48:
        return 198, 108, 58  # "orange"
    elif ram_state < 64:
        return 162, 162, 42  # "pretzel"
    elif ram_state < 80:
        return 184, 50, 50   # "apple"
    elif ram_state < 96:
        return 110, 156, 66  # "pear"
    elif ram_state < 112:
        return 198, 108, 58  # "banana"
