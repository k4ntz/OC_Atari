from .utils import find_objects, find_mc_objects
from .game_objects import GameObject


objects_colors = {
    'player': [[181,83,40], [252,188,116], [104,72,198],[134,106,38]],
    'fireball': [227,151,89],
    'pow_block': [201,164,74],
    # 'bonus_block': [], # check here if the platform plays a role for the color
    'pests': {'turtle': [136, 146, 62],
              'crab': [198,108,58],
              'bunny': [146,70,192],
              'ice': [101,183,217]},
    'bonus_coin': [104,72,198],
}


class Player(GameObject):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


class Fireball(GameObject):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


class Platform(GameObject):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


class PowBlock(GameObject):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


class BonusBlock(GameObject):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


class Pest(GameObject):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


class BonusCoin(GameObject):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


class Time(GameObject):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


class Score(GameObject):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

class Life(GameObject):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)



def _detect_objects(objects, obs, hud=True):
    objects.clear()

    player = find_mc_objects(obs, objects_colors['player'])
    for bb in player:
        objects.append(Player(*bb))

    fireball = find_objects(obs, objects_colors['fireball'])
    for bb in fireball:
        objects.append(Fireball(*bb))

    power_block = find_objects(obs, objects_colors['pow_block'])
    for bb in power_block:
        objects.append(PowBlock(*bb))

    # bonus_block = find_mc_objects(obs, objects_colors['bonus_block'])
    # for bb in bonus_block:
    #     objects.append(BonusBlock(*bb))

    for i in objects_colors['pests']:
        pest = find_objects(obs, objects_colors['pests'][i])
        for bb in pest:
            pes = Pest(*bb)
            pes.rgb = objects_colors['pests'][i]
            objects.append(pes)