from .utils import find_objects, find_mc_objects
from .game_objects import GameObject

objects_colors = {
    "Player": [236, 236, 236], 
    "DivingEnemy": [135, 183, 84],
    "PlayerMissile": [210, 164, 74],
    "EnemyShip": [[[110, 156, 66], [232, 204, 99], [192, 192, 192]], 
                 [[84, 92, 214], [232, 204, 99], [184, 70, 162]]]
    
                  }


class Player(GameObject):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.rgb = 236, 236, 236


class DivingEnemy(GameObject):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.rgb = 135, 183, 84


class PlayerMissile(GameObject):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.rgb = 210, 164, 74


class EnemyShip(GameObject):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.rgb = 110, 156, 66

def _detect_objects(objects, obs, hud=True):
    objects.clear()
    player = find_objects(obs, objects_colors["Player"], miny=166)
    for play in player:
        objects.append(Player(*play))
    diving_enemies = find_objects(obs, objects_colors["DivingEnemy"])
    for sent in diving_enemies:
        objects.append(DivingEnemy(*sent))
    player_missiles = find_objects(obs, objects_colors["PlayerMissile"]) #size=(1,39)
    for missile in player_missiles:
        objects.append(PlayerMissile(*missile))
    for color in objects_colors["EnemyShip"]:
        enemy_ships = find_mc_objects(obs, color)
        for enemy in enemy_ships:
            objects.append(EnemyShip(*enemy))
