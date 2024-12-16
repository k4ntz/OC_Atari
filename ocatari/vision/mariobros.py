
from .utils import find_objects, find_mc_objects, match_objects
from .game_objects import GameObject


objects_colors = {
    'player': [[252, 188, 116], [181, 83, 40], [104, 72, 198], [134, 106, 38]],
    'fireball': [227, 151, 89],
    'pow_block': [[210, 164, 74], [210, 210, 64], [192, 192, 192]],
    'platforms': {
        'normal': [228, 111, 111],
        'slippery': [78, 50, 181]
    },
    # 'bonus_block': [[132,200,252], [80, 0, 132], [134,134,29],[20,60,0], [162,162,42],
    #                 [128,232,128], [187,187,53], [134, 106, 38],[181,83,40], [111,210,111],
    #                 [188,144,252], [132,0,100], [184,70,162], [169,128,240],
    #                 [200,252,132], [180,231,117], [240,170,103], [236,236,236], [200,72,72],
    #                 [144,28,0], [232,204,99], [0,48,100], [132,224,252],[210,164,74],
    #                 [210,210,64], [252,252,84], [20,60,0], [162,134,56], [66,136,176],
    #                 [45,129,105], [72,44,0], [198,108,58], [0,0,148], [184,70,162], [136,146,62],
    #                 [104,72,198],[134, 106,30]],
    # 'bonus_block': {'same':[[181,83,40], [104,72,198], [134, 106,30], [111,210,111]],
    #                 'below_1': [[188,144,252],[132,0,100],[184,70,162],[187,187,53],[169,128,240], [200,252,132]],
    #                 'below_2': [[136,146,62],[0,0,148],[187,187,53],[188,144,252],[132,0,100],[184,70,162]],
    #                 'below_3': [[180,231,117],[240,170,103],[236,236,236],[200,72,72],[144,28,0]],
    #                 'below_4': [[236,236,236], [200,72,72], [144,28,0], [232,204,99],[0,48,100], [132,224,252]]},
    'pests': {'turtle': [136, 146, 62],
              'crab': [198, 108, 58],
              'bunny': [146, 70, 192],
              'ice': [101, 183, 217]},
    'bonus_coin': [104, 72, 198],
    'score': [78, 50, 181],
    'life': [78, 50, 181]
}


class Player(GameObject):
    def __init__(self, x, y, w, h):
        super(Player, self).__init__(x, y, w, h)
        self._xy = x, y
        self.wh = w, h
        self.rgb = 181, 83, 40
        self.hud = False


class Fireball(GameObject):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.rgb = 227, 151, 89


class Platform(GameObject):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


class PowBlock(GameObject):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.rgb = 201, 164, 74


class BonusBlock(GameObject):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.rgb = 100, 100, 100


class Pest(GameObject):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.rgb = 0, 0, 0


class BonusCoin(GameObject):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.rgb = 104, 72, 198


class Time(GameObject):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.rgb = 204, 216, 110


class Score(GameObject):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.rgb = 78, 50, 181


class Life(GameObject):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.rgb = 78, 50, 181


class Level(GameObject):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.rgb = 204, 216, 110


def _detect_objects(objects, obs, hud=False):

    player = objects[0]
    player_bb = find_mc_objects(obs, objects_colors['player'], size=(11, 22), tol_s=4,
                                maxy=175, all_colors=False)
    if player_bb:
        player.xywh = player_bb[0]

    fireball = objects[2]
    fireball_bb = find_objects(obs, objects_colors['fireball'], size=(9, 14))
    if fireball_bb:
        fireball.xywh = fireball_bb[0]
    match_objects(objects, fireball_bb, 2, 1, Fireball)

    power_block = objects[1]
    power_block_bb = find_mc_objects(
        obs, objects_colors['pow_block'], size=(16, 7), tol_s=2, all_colors=False)
    if power_block_bb:
        power_block.xywh = power_block_bb[0]
    match_objects(objects, power_block_bb, 1, 1, PowBlock)

    pests_bb = []
    for i in objects_colors['pests']:
        pests_bb.extend([list(bb) + objects_colors['pests'][i]
                        for bb in find_objects(obs, objects_colors['pests'][i], size=(9, 14), tol_s=5)])
    match_objects(objects, pests_bb, 3, 4, Pest)

    # for i in objects_colors['platforms']:
    #     platform = find_objects(obs, objects_colors['platforms'][i], size=())
    #     for bb in platform:
    #         plat = Platform(*bb)
    #         plat.rgb = objects_colors['platforms'][i]
    #         objects.append(plat)

    coin_positions = [(13, 20, 40, 40), (0, 60, 11, 85), (50, 100, 65, 120), (0, 140, 15, 165),  # right side
                      (130, 20, 150, 40), (145, 60, 160, 85), (90, 100, 115, 120), (140, 140, 160, 165)]  # left side

    bonus_coins_bb = []
    for pos in coin_positions:
        bonus_coins_bb.extend([list(bb) for bb in find_objects(obs, objects_colors['bonus_coin'], size=(
            9, 13), tol_s=(4, 4), minx=pos[0], miny=pos[1], maxx=pos[2], maxy=pos[3])])
    match_objects(objects, bonus_coins_bb, 8, 8, BonusCoin)

    if hud:
        score_bb = find_objects(obs, objects_colors['score'], closing_dist=5)
        match_objects(objects, score_bb, len(objects)-2, 1, Score)

        life_bb = find_objects(obs, objects_colors['life'], closing_dist=5)
        match_objects(objects, life_bb, len(objects)-1, 1, Life)
