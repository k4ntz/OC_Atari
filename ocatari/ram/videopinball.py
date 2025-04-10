from .game_objects import GameObject, NoObject

"""
RAM extraction for the game Fishing Derby.
"""

MAX_NB_OBJECTS = {"Flipper": 2, "Ball": 1, "Spinner": 2, "DropTarget": 12, "Bumper": 8, "Plunger": 1}
MAX_NB_OBJECTS_HUD = {"Flipper": 2, "Ball": 1, "Spinner": 2, "DropTarget": 12, "Bumper": 8, "Plunger": 1, "Score": 1,
                      "LifeUsed": 1, "DifficultyLevel": 1}

bumpers = (((104, 112), (16, 32)), ((104, 48), (4, 32)), ((116, 48), (4, 32)), ((40, 112), (16, 32)),
           ((40, 48), (4, 32)), ((52, 48), (4, 32)), ((72, 104), (16, 8)), ((72, 48), (16, 32)))
droptgts = (((60, 24), (7, 14)), ((76, 24), (7, 14)), ((92, 24), (7, 14)),
            ((47, 58), (3, 12)), ((79, 58), (3, 12)), ((109, 58), (7, 12)),
            ((47, 122), (3, 12)), ((77, 120), (7, 14)), ((111, 122), (3, 12)),
            ((60, 154), (7, 12)), ((76, 154), (7, 12)), ((92, 154), (7, 12)))
dp_follow_list = [72, 73, 74,
                  75, 76, 77,
                  81, 82, 83,
                  84, 85, 86]
left_flip_map = {0: (64, 184, 13, 8), 16: (64, 184, 13, 6),
                 32: (64, 181, 13, 9), 48: (64, 177, 13, 13)}
right_flip_map = {128: (83, 184, 13, 8), 144: (
    83, 184, 13, 6), 160: (83, 181, 13, 9), 176: (84, 177, 13, 13)}


def compute_score(ram):
    score = 0
    for i in range(3):
        buf = ram[48+2*i]
        sc = 10 * (buf // 16) + buf % 16
        score += sc * 100**i
    return score


def manage_dptgts(dptgts, ram):
    for i, (tg, pos) in enumerate(zip(dptgts, dp_follow_list)):
        st = ram[pos]
        if st == 0:
            if type(tg) is not NoObject:
                dptgts[i] = NoObject()
        else:
            if type(tg) is NoObject:
                tg = DropTarget()
                tg.xy = droptgts[i][0]
                tg.wh = droptgts[i][1]
                dptgts[i] = tg
            if st == 80:  # diamond
                tg.value = 20
            elif st == 115:  # Atari
                tg.value = 40
            else:
                tg.value = st // 8


class Flipper(GameObject):
    def __init__(self, left=True, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.xy = (64, 184) if left else (83, 184)
        self.wh = 13, 7
        self.rgb = 236, 236, 236
        self.left = left
        self.hud = False


class Ball(GameObject):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.xy = 149, 129
        self.wh = 2, 4
        self.rgb = 104, 72, 198
        self.hud = False


class Spinner(GameObject):
    def __init__(self, left=True, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.xy = (30, 91) if left else (126, 91)
        self.wh = 6, 10
        self.rgb = 236, 236, 236
        self.hud = False


class DropTarget(GameObject):
    def __init__(self, x=0, y=0, w=0, h=0, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.xy = x, y
        self.wh = w, h
        self.rgb = 210, 164, 74
        self.hud = False
        self.value = 1


class Bumper(GameObject):
    def __init__(self, x=0, y=0, w=0, h=0, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.xy = x, y
        self.wh = w, h
        self.rgb = 104, 72, 198
        self.hud = False


class Plunger(GameObject):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.xy = 149, 133
        self.wh = 2, 41
        self.rgb = 187, 159, 71
        self.hud = False


class Score(GameObject):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.value = 0
        self.xy = 64, 3
        self.wh = 92, 10
        self.rgb = 187, 159, 71
        self.hud = True


class LifeUsed(GameObject):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.value = 0
        self.xy = 36, 3
        self.wh = 12, 10
        self.rgb = 187, 159, 71
        self.hud = True


class DifficultyLevel(GameObject):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.xy = 4, 3
        self.wh = 12, 10
        self.value = 1
        self.rgb = 187, 159, 71
        self.hud = True


def _get_max_objects(hud=False):
    return


def _init_objects_ram(hud=False):
    objects = [Flipper(left=True), Flipper(left=False), Ball(),
               Spinner(left=True), Spinner(left=False)]
    objects.extend([NoObject() for _ in dp_follow_list])
    for b_xy, b_wh in bumpers:
        objects.append(Bumper(b_xy[0], b_xy[1], b_wh[0], b_wh[1]))
    objects.append(Plunger())
    if hud:
        objects.extend([Score(), LifeUsed(), DifficultyLevel()])
    return objects


def _detect_objects_ram(objects, ram_state, hud=False):
    flipl, flipr, ball = objects[:3]
    flipl.xy = left_flip_map[ram_state[98]][:2]
    flipl.wh = left_flip_map[ram_state[98]][2:]
    flipr.xy = right_flip_map[ram_state[102]][:2]
    flipr.wh = right_flip_map[ram_state[102]][2:]
    ball.xy = ram_state[67], ram_state[68]-3
    drop_targets = objects[5:17]
    manage_dptgts(drop_targets, ram_state)
    objects[5:17] = drop_targets

    # plunger
    objects[25].xywh = 149, ram_state[70]*2 - 1, 2, (88-ram_state[70])*2 - 1

    if hud:
        score, lifeu, difflvl = objects[-3:]
        score.value = compute_score(ram_state)
        lifeu.value = ram_state[25]
    return objects


def _detect_objects_videopinball_raw(info, ram_state):
    return
