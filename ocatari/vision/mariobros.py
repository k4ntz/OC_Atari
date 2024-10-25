from .utils import find_objects, find_mc_objects
from .game_objects import GameObject


objects_colors = {
    'player': [[252,188,116], [181,83,40], [104,72,198], [134,106,38]],
    'fireball': [227,151,89],
    'pow_block': [[210,164,74],[210,210,64], [192,192,192]],
    'platforms': {
        'normal': [228,111,111],
        'slippery': [78,50,181] 
    },
    'pests': {'turtle': [136, 146, 62],
              'crab': [198,108,58],
              'bunny': [146,70,192],
              'ice': [101,183,217]},
    'bonus_coin': [104,72,198],
    'score': [78,50,181],
    'life': [78,50,181]
}


class Player(GameObject):
    def __init__(self, x, y, w, h):
        super(Player, self).__init__(x,y,w,h)
        self._xy = x,y
        self.wh = w, h
        self.rgb = 181,83,40
        self.hud = False


class Fireball(GameObject):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.rgb = 227, 151,89


class Platform(GameObject):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


class PowBlock(GameObject):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.rgb = 201, 164,74


class BonusBlock(GameObject):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.rgb = 100, 100,100


class Pest(GameObject):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.rgb = 0,0,0


class BonusCoin(GameObject):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.rgb = 104,72,198


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



def _detect_objects(objects, obs, hud=True):
    objects.clear()

    player = find_mc_objects(obs, objects_colors['player'], size=(11, 22), tol_s=4,
                             maxy=175, all_colors=False)
    for bb in player:
        objects.append(Player(*bb))


    fireball = find_objects(obs, objects_colors['fireball'], size=(9,14))
    for bb in fireball:
        objects.append(Fireball(*bb))


    power_block = find_mc_objects(obs, objects_colors['pow_block'], size=(16,7), tol_s=2, all_colors=False)
    for bb in power_block:
        objects.append(PowBlock(*bb))


    for i in objects_colors['pests']:
        pest = find_objects(obs, objects_colors['pests'][i], size=(9, 14), tol_s=5)
        for bb in pest:
            pes = Pest(*bb)
            pes.rgb = objects_colors['pests'][i]
            objects.append(pes)


    for i in objects_colors['platforms']:
        platform = find_objects(obs, objects_colors['platforms'][i], miny=50)
        for bb in platform:
            plat = Platform(*bb)
            plat.rgb = objects_colors['platforms'][i]
            objects.append(plat)    


    coin_positions = [(13,20,40,40), (0,60,11,85), (50,100,65,120), (0,140,15,165), # right side
                      (130,20,150,40), (145,60,160,85), (90,100,115,120), (140,140,160,165)] # left side

    for pos in coin_positions:
        bonus_coins = find_objects(obs, objects_colors['bonus_coin'], size=(9,13), tol_s=(4,4),
                                   minx=pos[0], miny=pos[1], maxx=pos[2], maxy=pos[3])
        for bb in bonus_coins:
            objects.append(BonusCoin(*bb))


    if hud:
        score = find_objects(obs, objects_colors['score'], closing_dist=5)
        for bb in score:
            objects.append(Score(*bb))
        life = find_objects(obs, objects_colors['life'], closing_dist=5)
        for bb in life:
            objects.append(Life(*bb))