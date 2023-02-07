from .game_objects import GameObject
from ._helper_methods import _convert_number


class Player(GameObject):
    class Player(GameObject):
        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)
            self.rgb = 187, 187, 53
            self._xy = 0, 0
            self.wh = 8, 11  # at some point 16, 11. advanced other player (oblix) is (6, 11)
            self.hud = False


class Cauldron(GameObject):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.rgb = 167, 26, 26
        self._xy = 0, 0
        self.wh = 7, 10
        self.hud = False


class Enemy(GameObject):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.rgb = 228, 111, 111
        self._xy = 0, 0
        self.wh = 7, 11
        self.hud = False


class Score(GameObject):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.rgb = 187, 187, 53
        self._xy = 0, 0
        self.wh = 8, 11
        self.hud = True


class Lives(GameObject):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.rgb = 187, 187, 53
        self._xy = 0, 0
        self.wh = 6, 7
        self.hud = True


class Helmet(GameObject):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.rgb = 240, 128, 128
        self._xy = 0, 0
        self.wh = 7, 11
        self.hud = False


class Shield(GameObject):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.rgb = 214, 214, 214
        self._xy = 0, 0
        self.wh = 5, 11
        self.hud = False


class Lamp(GameObject):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.rgb = 187, 53, 53
        self._xy = 0, 0
        self.wh = 8, 11
        self.hud = False


class Apple(GameObject):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.rgb = 184, 50, 50
        self._xy = 0, 0
        self.wh = 8, 11
        self.hud = False


class Fish(GameObject):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.rgb = 198, 89, 179
        self._xy = 0, 0
        self.wh = 8, 5
        self.hud = False


class Meat(GameObject):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.rgb = 184, 50, 50
        self._xy = 0, 0
        self.wh = 5, 11
        self.hud = False


class Mug(GameObject):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.rgb = 184, 50, 50
        self._xy = 0, 0
        self.wh = 7, 11
        self.hud = False


class Reward50(GameObject):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.rgb = 198, 89, 179
        # self.visible = True
        self._xy = 0, 0
        self.wh = 6, 11
        self.hud = False


class Reward100(GameObject):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.rgb = 135, 183, 84
        # self.visible = True
        self._xy = 0, 0
        self.wh = 8, 11
        self.hud = False


class Reward200(GameObject):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.rgb = 195, 144, 61
        # self.visible = True
        self._xy = 0, 0
        self.wh = 8, 11
        self.hud = False


class Reward300(GameObject):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.rgb = 213, 130, 74
        # self.visible = True
        self._xy = 0, 0
        self.wh = 8, 11
        self.hud = False


class Reward400(GameObject):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.rgb = 135, 183, 84
        # self.visible = True
        self._xy = 0, 0
        self.wh = 8, 11
        self.hud = False


class Reward500(GameObject):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.rgb = 163, 57, 21
        self._xy = 0, 0
        self.wh = 8, 11
        self.hud = False


def _init_objects_asterix_ram(hud=False):
    """
    (Re)Initialize the objects
    """
    objects = [Player()]
    if hud:
        objects.extend([Score(), Lives(), Lives()])

    return objects


def _detect_objects_asterix_raw(info, ram_state):
    info["x_positions"] = ram_state[41:50]  # 41 for player, 42 for obj in upper lane...
    info["y_player"] = ram_state[39]  # from 0 to 7 (8 lanes)
    info["score"] = ram_state[94:97]  # on ram in decimal/ on screen in hex(like other 2 games)
    info["score_dec"] = ram_state[94:97]
    info["lives"] = ram_state[83]
    info["kind_of_visible_objs"] = ram_state[54] % 8
    info["rewards_visible"] = ram_state[73:81]
    info["enemy_or_eatable_object"] = ram_state[29:37] % 2  # = 1 for enemy

    # info["maybe_useful"] = ram_state[10:18], ram_state[40], ram_state[19:27], ram_state[29:37], ram_state[87]
    # not known what they are for exactly
    print(ram_state)


def _detect_objects_asterix_revised(objects, ram_state, hud=False):
    lives_nr = ram_state[83]
    if hud:
        del objects[2+lives_nr-1:]
    else:
        del objects[1:]
    const = ram_state[54] % 8

    rewards = []
    reward_lanes = []
    ctr = 0
    for i in range(8):
        if ram_state[73 + i]:  # set to lane number if there is reward in that lane
            reward_lanes.append(i)  # 0-7 instead actual 1-8
            x, y = ram_state[42 + i], 26 + i * 16
            if const == 0:  # 50 reward
                rew = Reward50()
                rewards.append(rew)
                rew.xy = x, y
                objects.append(rew)
            elif const == 1:  # 100 reward
                rew = Reward100()
                rew.xy = x, y
                rewards.append(rew)
                objects.append(rew)
            elif const == 2:  # 200 reward
                rew = Reward200()
                rew.xy = x, y
                rewards.append(rew)
                objects.append(rew)
            elif const == 3:  # 300 reward
                rew = Reward300()
                rew.xy = x, y
                rewards.append(rew)
                objects.append(rew)
            elif const == 4:  # 400 reward
                rew = Reward400()
                rew.xy = x, y
                rewards.append(rew)
                objects.append(rew)
            else:  # 500 reward
                rew = Reward500()
                rew.xy = x, y
                rewards.append(rew)
                objects.append(rew)
            ctr += 1

    eatable = []
    enemy_lanes = []
    ctr = 0
    if const == 0:
        for i in range(8):
            if i in reward_lanes:
                continue
            if ram_state[29+i] % 2 == 1:
                enemy_lanes.append(i)
                continue
            else:
                x, y = ram_state[42 + i] + 1, 26 + i * 16 + 1
                if const == 0:
                    instance = Cauldron()
                    eatable.append(instance)
                    instance.xy = x, y
                    objects.append(instance)
                elif const == 1:
                    instance = Helmet()
                    eatable.append(instance)
                    instance.xy = x, y
                    objects.append(instance)
                elif const == 2:
                    eatable.append(Shield())
                    eatable[ctr].xy = x, y
                    objects.append(eatable[ctr])
                elif const == 3:
                    eatable.append(Lamp())
                    eatable[ctr].xy = x, y
                    objects.append(eatable[ctr])
                elif const == 4:
                    eatable.append(Apple())
                    eatable[ctr].xy = x, y
                    objects.append(eatable[ctr])
                elif const == 5:
                    eatable.append(Fish())
                    eatable[ctr].xy = x, y
                    objects.append(eatable[ctr])
                elif const == 6:
                    eatable.append(Meat())
                    eatable[ctr].xy = x, y
                    objects.append(eatable[ctr])
                elif const == 7:
                    eatable.append(Mug())
                    eatable[ctr].xy = x, y
                    objects.append(eatable[ctr])
                ctr += 1

    enemy = []
    ctr = 0
    for i in enemy_lanes:
        enemy.append(Enemy())
        enemy[ctr].xy = ram_state[42 + i], 26 + i * 16
        objects.append(enemy[ctr])
        ctr += 1

    player = objects[0]
    player.xy = ram_state[41], 26 + ram_state[39] * 16  # 84, 90   84 26 90-26 /4 = 16
    if ram_state[71] < 82:
        player.wh = 8, 11
    else:
        player.wh = 16, 11
    player.rgb = 187, 187, 53

    if hud:
        score = objects[1]
        digits = 0
        if _convert_number(ram_state[94]) > 9:
            digits = 5
        elif _convert_number(ram_state[94]) > 0:
            digits = 4
        elif _convert_number(ram_state[95]) > 9:
            digits = 3
        elif _convert_number(ram_state[95]) > 0:
            digits = 2
        elif _convert_number(ram_state[96]) > 0:
            digits = 1
        score.xy = 96 - digits * 8, 184
        score.wh = 6 + digits * 8, 7

        if lives_nr >= 2:
            lives = objects[2]
            lives.xy = 60, 169
            lives.wh = 8, 11
        elif isinstance(objects[2], Lives):
            del objects[2]

        if lives_nr >= 3:
            lives = objects[3]
            lives.xy = 60 + 16, 169
            lives.wh = 8, 11
        elif isinstance(objects[3], Lives):
            del objects[3]
