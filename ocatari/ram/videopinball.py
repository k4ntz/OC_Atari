from .game_objects import GameObject

"""
RAM extraction for the game Fishing Derby.
"""

MAX_NB_OBJECTS = {"Player1FishingString": 1,
                  "Player2FishingString": 1, "Fish": 6, "Shark": 1}
MAX_NB_OBJECTS_HUD = {"Player1FishingString": 1, "Player2FishingString": 1, "Fish": 6, "Shark": 1, "ScoreP1": 1,
                      "ScoreP2": 1}

bumpers = (((104, 112), (16, 32)), ((104, 48), (4, 32)), ((116, 48), (4, 32)), ((40, 112), (16, 32)),
           ((40, 48), (4, 32)), ((52, 48), (4, 32)), ((72, 104), (16, 8)), ((72, 48), (16, 32)))
droptgts = (((60, 24), (7, 14)), ((76, 24), (7, 14)), ((92, 24), (7, 14)),
            ((47, 58), (3, 12)), ((79, 58), (3, 12)), ((109, 58), (7, 12)),
            ((47, 122), (3, 12)), ((77, 122), (7, 12)), ((111, 122), (3, 12)),
            ((60, 154), (7, 12)), ((76, 154), (7, 12)), ((92, 154), (7, 12)))
dp_follow_list = [72, 73, 74,
                  75, 76, 77,
                  81, 82, 83,
                  84, 85, 86]
left_flip_map = {0: (64, 184, 13, 6), 16: (64, 181, 13, 9),
                 32: (64, 181, 13, 9), 48: (64, 181, 13, 9)}
right_flip_map = {128: (83, 184, 13, 6), 144: (
    83, 181, 13, 9), 160: (83, 181, 13, 9), 176: (83, 181, 13, 9)}


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
            if tg is not None:
                dptgts[i] = None
        else:
            if tg is None:
                tg = DropTarget(*droptgts[i])
                dptgts[i] = tg
            if st == 80:  # diamond
                tg.value = 20
            elif st == 115:  # Atari
                tg.value = 40
            else:
                tg.value = st // 8


class Flipper(GameObject):
    def __init__(self, left, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.xy = (64, 184) if left else (83, 184)
        self.wh = 13, 6
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
    def __init__(self, left, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.xy = (30, 91) if left else (126, 91)
        self.wh = 6, 10
        self.rgb = 236, 236, 236
        self.hud = False


class DropTarget(GameObject):
    def __init__(self, xy, wh, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.xy = xy
        self.wh = wh
        self.rgb = 210, 164, 74
        self.hud = False
        self.value = 1


class Plunger(GameObject):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.rgb = 187, 159, 71
        self.hud = False


class Bumper(GameObject):
    def __init__(self, xy, wh, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.xy = xy
        self.wh = wh
        self.rgb = 104, 72, 198
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
    objects = [Flipper(True), Flipper(False), Ball(),
               Spinner(True), Spinner(False)]
    objects.extend([None for _ in dp_follow_list])
    for b_xy, b_wh in bumpers:
        objects.append(Bumper(b_xy, b_wh))
    objects.append(None)
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
    drop_targets = objects[5:5+12]
    manage_dptgts(drop_targets, ram_state)
    objects[5:5+12] = drop_targets
    if hud:
        score, lifeu, difflvl = objects[-3:]
        score.value = compute_score(ram_state)
        lifeu.value = ram_state[25]
    return objects


def _detect_objects_videopinball_raw(info, ram_state):
    return
