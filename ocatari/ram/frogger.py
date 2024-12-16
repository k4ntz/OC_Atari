from .game_objects import GameObject, NoObject

"""
RAM extraction for the game Frogger.

"""

MAX_NB_OBJECTS = {'Frog': 1, 'Car': 26, 'Log': 8, 'Alligator': 2, 'Turtle': 10,
                  'LadyFrog': 1, 'Fly': 1, 'AlligatorHead': 1, 'HappyFrog': 5, 'Snake': 2}
MAX_NB_OBJECTS_HUD = {'Frog': 1, 'Car': 26, 'Log': 8, 'Alligator': 2, 'Turtle': 10, 'LadyFrog': 1,
                      'Fly': 1, 'AlligatorHead': 1, 'HappyFrog': 5, 'Snake': 2, 'Score': 1, 'Time': 1, 'Lives': 1}

car_colors = [[195, 144, 61], [164, 89, 208], [
    82, 126, 45], [198, 89, 179], [236, 236, 236]]


class Frog(GameObject):
    """
    The player figure i.e., the frog.
    """

    def __init__(self):
        super(Frog, self).__init__()
        self._xy = 0, 0
        self.wh = 7, 7
        self.rgb = 110, 156, 66
        self.hud = False


class Car(GameObject):
    """
    A car.
    """

    def __init__(self):
        super(Car, self).__init__()
        self._xy = 0, 0
        self.wh = 14, 7
        self.rgb = 195, 144, 61
        self.hud = False


class Log(GameObject):
    def __init__(self):
        super().__init__()
        self.rgb = 105, 105, 15


class Turtle(GameObject):
    def __init__(self):
        super().__init__()
        self.rgb = 144, 72, 17


class Alligator(GameObject):
    def __init__(self):
        super().__init__()
        self.rgb = 105, 105, 15


class LadyFrog(GameObject):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.rgb = 236, 236, 236


class HappyFrog(GameObject):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # self._xy = 0, 0
        # self.wh = 8, 10
        self.rgb = 82, 126, 45


class AlligatorHead(GameObject):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.rgb = 110, 156, 66
        # self.wh = 8, 10


class Fly(GameObject):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.rgb = 110, 156, 66


class Snake(GameObject):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.rgb = 82, 126, 45


class Score(GameObject):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.rgb = 195, 144, 61
        self.hud = True


class Lives(GameObject):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.rgb = 236, 236, 236
        self.hud = True


class Time(GameObject):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.rgb = 0, 0, 0
        self.hud = True


def _init_objects_ram(hud=False):
    """
    (Re)Initialize the objects
    """
    cars = [Car() for _ in range(26)]
    logs = [NoObject()] * 8
    aligators = [NoObject()] * 2
    turtles = [NoObject()] * 10
    ladyfrogs = [NoObject()]
    happyfrogs = [NoObject()]*5
    flys = [NoObject()]
    heads = [NoObject()]
    snakes = [NoObject()]*2
    score = [NoObject()]
    time = [NoObject()]
    lives = [NoObject()]
    return [Frog()] + cars + logs + aligators + turtles + ladyfrogs + heads + flys + happyfrogs + snakes + score + time + lives


def _detect_objects_ram(objects, ram_state, hud=False):
    """
    For all objects:
    (x, y, w, h, r, g, b)
    """
    frog = objects[0]
    frog.x = ram_state[48] - 1
    frog.wh = 7, 7
    if ram_state[44] == 255:
        frog.y = 171
    elif ram_state[44] == 5:
        frog.y = 95
    else:
        frog.y = - 13 * ram_state[44] + 161

    # first line first car
    car = objects[1]
    car.rgb = car_colors[0]
    car.y = 161
    car.h = 7
    if ram_state[11] < 1:
        car = NoObject()
    elif ram_state[11] < 8:
        car.x = 8
        car.w = ram_state[11] - 1
    elif ram_state[11] > 154:
        car = NoObject()
    else:
        car.x = ram_state[11] - 1
        if ram_state[11] > 146:
            car.w = 153 - ram_state[11]
        else:
            car.w = 8

    # first line second car
    car = objects[2]
    car.rgb = car_colors[0]
    car.y = 161
    car.h = 7
    if ram_state[0] < 1:
        car = NoObject()
    elif ram_state[0] < 8:
        car.x = 8
        car.w = ram_state[0] - 1
    elif ram_state[0] > 154:
        car = NoObject()
    else:
        car.x = ram_state[0] - 1
        if ram_state[0] > 146:
            car.w = 153 - ram_state[0]
        else:
            car.w = 8

    # second line first car
    car = objects[3]
    car.rgb = car_colors[1]
    car.y = 148
    car.h = 7
    if ram_state[12] < 1:
        car = NoObject()
    elif ram_state[12] < 8:
        car.x = 8
        car.w = ram_state[12] - 1
    elif ram_state[12] > 154:
        car = NoObject()
    else:
        car.x = ram_state[12] - 1
        if ram_state[12] > 147:
            car.w = 153 - ram_state[12]
        else:
            car.w = 7

    # second line second car
    car = objects[4]
    car.rgb = car_colors[1]
    car.y = 148
    car.h = 7
    if ram_state[1] < 1:
        car = NoObject()
    elif ram_state[1] < 8:
        car.x = 8
        car.w = ram_state[1] - 1
    elif ram_state[1] > 154:
        car = NoObject()
    else:
        car.x = ram_state[1] - 1
        if ram_state[1] > 147:
            car.w = 153 - ram_state[1]
        else:
            car.w = 7

    # third line first car
    car = objects[5]
    car.rgb = car_colors[2]
    car.y = 135
    car.h = 7
    if ram_state[13] < 1:
        car = NoObject()
    elif ram_state[13] < 8:
        car.x = 8
        car.w = ram_state[13] - 1
    elif ram_state[13] > 154:
        car = NoObject()
    else:
        car.x = ram_state[13] - 1
        if ram_state[13] > 147:
            car.w = 153 - ram_state[13]
        else:
            car.w = 8

    # third line second car
    car = objects[6]
    car.rgb = car_colors[2]
    car.y = 135
    car.h = 7
    pos = (ram_state[13] + 32) % 160
    if pos < 1:
        car = NoObject()
    elif pos < 8:
        car.x = 8
        car.w = pos - 1
    elif pos > 154:
        car = NoObject()
    else:
        car.x = pos - 1
        if pos > 147:
            car.w = 153 - pos
        else:
            car.w = 8

    # third line third car
    car = objects[7]
    car.rgb = car_colors[2]
    car.y = 135
    car.h = 7
    if ram_state[2] < 1:
        car = NoObject()
    elif ram_state[2] < 8:
        car.x = 8
        car.w = ram_state[2] - 1
    elif ram_state[2] > 154:
        car = NoObject()
    else:
        car.x = ram_state[2] - 1
        if ram_state[2] > 147:
            car.w = 153 - ram_state[2]
        else:
            car.w = 8

    # third line third car
    car = objects[8]
    car.rgb = car_colors[2]
    car.y = 135
    car.h = 7
    pos = (ram_state[13] + 112) % 160
    if pos < 1:
        car = NoObject()
    elif pos < 8:
        car.x = 8
        car.w = pos - 1
    elif pos > 154:
        car = NoObject()
    else:
        car.x = pos - 1
        if pos > 147:
            car.w = 153 - pos
        else:
            car.w = 8

    # fourth line first car
    car = objects[9]
    car.rgb = car_colors[3]
    car.y = 122
    car.h = 7
    if ram_state[14] < 1:
        car = NoObject()
    elif ram_state[14] < 8:
        car.x = 8
        car.w = ram_state[14] - 1
    elif ram_state[14] > 154:
        car = NoObject()
    else:
        car.x = ram_state[14] - 1
        if ram_state[14] > 147:
            car.w = 153 - ram_state[14]
        else:
            car.w = 8

    # fourth line second car
    car = objects[10]
    car.rgb = car_colors[3]
    car.y = 122
    car.h = 7
    if ram_state[3] < 1:
        car = NoObject()
    elif ram_state[3] < 8:
        car.x = 8
        car.w = ram_state[3] - 1
    elif ram_state[3] > 154:
        car = NoObject()
    else:
        car.x = ram_state[3] - 1
        if ram_state[3] > 147:
            car.w = 153 - ram_state[3]
        else:
            car.w = 8

    car = objects[11]
    car.rgb = car_colors[4]
    car.y = 109
    car.h = 7
    if ram_state[15] < 8:
        car.x = 8
        car.w = ram_state[15] + 7
    elif ram_state[15] > 155:
        car.x = 8
        car.w = ram_state[15] - 153
    else:
        car.x = ram_state[15]
        if ram_state[15] > 137:
            car.w = 152 - ram_state[15]
        else:
            car.w = 16

    car = objects[12]
    car.rgb = car_colors[4]
    car.y = 109
    car.h = 7
    if ram_state[4] < 8:
        car.x = 8
        car.w = ram_state[4] + 7
    elif ram_state[4] > 155:
        car.x = 8
        car.w = ram_state[4] - 153
    else:
        car.x = ram_state[4]
        if ram_state[4] > 137:
            car.w = 152 - ram_state[4]
        else:
            car.w = 16
