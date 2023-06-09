from ._helper_methods import _convert_number
from .game_objects import GameObject

"""
RAM extraction for the game ASTEROIDS. Supported modes: raw

Revised is missing the x-Position for Asteroids and Player. The RAM states for these values are found (look at raw) but
they were not interpretable. One x Value corresponds to multiple positions on the rendered image. So either there is
another RAM state which separates them into quadrants or the x-Axis is moving.
"""

MAX_NB_OBJECTS = {'Player': 1, 'PlayerMissile': 2, 'Asteroid': 50}  # Asteroid count can get really high
MAX_NB_OBJECTS_HUD = {'Lives': 1, 'PlayerScore': 5}


class Player(GameObject):
    def __init__(self):
        self._xy = 84, 99
        self.wh = 5, 10
        self.rgb = 240, 128, 128
        self.hud = False


class Asteroid(GameObject):
    def __init__(self):
        super().__init__()
        self.xy = 8, 87
        self.wh = 16, 28
        self.rgb = 180, 122, 48
        self.hud = False


class PlayerMissile(GameObject):
    def __init__(self):
        self._xy = 0, 0
        self.wh = 1, 2
        self.rgb = 117, 181, 239
        self.hud = False


class PlayerScore(GameObject):
    def __init__(self):
        self._xy = 68, 5
        self.rgb = 184, 50, 50
        self.wh = 12, 10
        self.hud = True

    def __eq__(self, o):
        return isinstance(o, PlayerScore) and self.xy == o.xy


class Lives(GameObject):
    def __init__(self):
        self._xy = 132, 5
        self.rgb = 184, 50, 50
        self.wh = 12, 10
        self.hud = True


asteroids_colors = {"brown": [180, 122, 48], "purple": [104, 72, 198], "yellow": [136, 146, 62],
                    "lightyellow": [187, 187, 53], "grey": [214, 214, 214], "lightblue": [117, 181, 239],
                    "pink": [184, 70, 162], "red": [184, 50, 50]}

player_missile_colors = {"blue": [117, 181, 239], "red": [240, 128, 128]}


def _init_objects_asteroids_ram(hud=False):
    """
    (Re)Initialize the objects
    """
    objects = [Player()]

    if hud:
        objects.extend([Lives(), PlayerScore()])
    return objects


def _detect_objects_asteroids_revised(objects, ram_state, hud=False):
    """
       For all objects:
       (x, y, w, h, r, g, b)
    """
    player = objects[0]
    player.xy = 100, 100 + (2 * (ram_state[74] - 41))

    if hud:
        del objects[3:]
    else:
        del objects[1:]

    # 0 und 1 asteroids on left
    # 9, 10 asteroids on right
    for i in range(16):
        if (ram_state[21 + i] == 0 and ram_state[3 + i] == 0) or ram_state[3 + i] == 224:
            continue
        else:
            asteroid = Asteroid()
            y = 0
            x = 0
            if i >= 8:
                x = round(ram_state[21 + i] / 3)
            else:
                x = 25
            if ram_state[3 + i] > 200:
                y = 18
            else:
                y = 184 - 2 * (80 - ram_state[3 + i])
            asteroid.xy = x, y
            print(str(i) + " " + str(ram_state[21 + i]) + ", " + str(ram_state[3 + i]))
            objects.append(asteroid)

    if hud:
        lives, score = objects[1:3]
        score_value = _convert_number(ram_state[61]) * 1000 + _convert_number(ram_state[62]) * 10
        if score_value >= 10:
            sc = PlayerScore()
            sc.xy = 52, 5
            objects.append(sc)

        if score_value >= 100:
            sc = PlayerScore()
            sc.xy = 36, 5
            objects.append(sc)

        if score_value >= 1000:
            sc = PlayerScore()
            sc.xy = 20, 5
            objects.append(sc)

        if score_value >= 10000:
            sc = PlayerScore()
            sc.xy = 4, 5
            objects.append(sc)


def _augment_info_asteroids_revised(info, ram_state):
    """
    For all objects:
    (x, y, w, h, r, g, b)
    """
    objects = {}
    if ram_state[74] <= 80:
        objects["player"] = 81 - (2 * (ram_state[77])), 100 + (2 * (ram_state[74] - 41)), 10, 10, 240, 128, 128
        print("Player Pos: " + str(81 - round(1.5 * ram_state[77])) + " " + str(100))

    for i in range(16):
        if ram_state[3 + i] != 0 and ram_state[21 + 1] != 0:
            if ram_state[21 + i] <= 160:
                prev_y = ram_state[3 + i] % 80
                x, y = ram_state[21 + i], 210 - round(prev_y * 2.5)
                # print("x: " + str(x) + " y: " + str(y) + " i: " + str(i))
                objects[f"asteroi_{i}"] = x, y, 16, 28, 255
    # objects["asteroid"] = 0, round(ram_state[3] * 2.625), 16, 28, 0, 0, 0
    info["score"] = _convert_number(ram_state[61]) * 1000 + _convert_number(ram_state[62]) * 10
    info["objects"] = objects


def _detect_objects_asteroids_raw(info, ram_state):
    """
    Actions:
    0: NOP
    1: shoot
    2: move  forward
    3: rotate right
    4: rotate left
    5: random teleport
    y = 0 top
    y = 85 bottom
    """
    info["player_x"] = ram_state[73]    # starts at x = 29
    info["player_y"] = ram_state[74]    # starts at y = 41
    info["diff_to_start_x"] = ram_state[77]     # starts at 255, goes down if go to right and up to the left
    info["player_direction"] = ram_state[60]    # 64: looking up, 78: up and right, 76: to the right, 74: down and right
    # 72: down, 70: down and left, 68: left, 66: up and left
    info["score_high"] = _convert_number(ram_state[61])
    info["score_low"] = _convert_number(ram_state[62])  # 153 = 990 at 160 again 0
    info["score"] = _convert_number(ram_state[61]) * 1000 + _convert_number(ram_state[62]) * 10
    info["player_missile_1_x"] = ram_state[83]  # beginning x = 253, y = 224
    info["player_missile_2_x"] = ram_state[84]  # blue one
    info["player_missile_1_y"] = ram_state[86]
    info["player_missile_2_y"] = ram_state[87]
    info["player_missile_1_dir"] = ram_state[89]    # 0 if not flying
    info["player_missile_2_dir"] = ram_state[90]
    info["asteroid_1"] = {ram_state[21]: ram_state[3]}
    info["asteroid_2"] = {ram_state[22]: ram_state[4]}
    info["asteroid_3"] = {ram_state[23]: ram_state[5]}
    info["asteroid_4"] = {ram_state[24]: ram_state[6]}
    info["asteroid_5"] = {ram_state[25]: ram_state[7]}
    info["asteroid_6"] = {ram_state[26]: ram_state[8]}
    info["asteroid_7"] = {ram_state[27]: ram_state[9]}
    info["asteroid_8"] = {ram_state[28]: ram_state[10]}
    info["asteroid_9"] = {ram_state[29]: ram_state[11]}
    info["asteroid_10"] = {ram_state[30]: ram_state[12]}
    info["asteroid_11"] = {ram_state[31]: ram_state[13]}
    info["asteroid_12"] = {ram_state[32]: ram_state[14]}
    info["asteroid_13"] = {ram_state[33]: ram_state[15]}
    info["asteroid_14"] = {ram_state[34]: ram_state[16]}
    info["asteroid_15"] = {ram_state[35]: ram_state[17]}
    info["asteroid_16"] = {ram_state[36]: ram_state[18]}
    info["asteroid_17"] = {ram_state[37]: ram_state[19]}
    info["asteroid_variation"] = ram_state[39:57]
