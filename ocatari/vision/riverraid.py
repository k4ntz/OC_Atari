from .utils import find_objects, find_mc_objects, match_objects
from .game_objects import GameObject, NoObject

objects_colors = {"player": [232, 232, 74], "logo": [232, 232, 74], "fuel_bar": [0, 0, 0], "lives": [232, 232, 74],
                  "score": [232, 232, 74], "player_missile": [232, 232, 74],
                  "helicopter": [[0, 64, 48], [0, 0, 148], [210, 164, 74]],
                  "house": [[214, 214, 214], [0, 0, 0],[158,208,101],[72,72,0]],
                  "tanker": [[84, 160, 197], [163, 57, 21], [0, 0, 0]],
                  "fuel_depot": [[214, 92, 92], [214, 214, 214]],
                  "jet": [[117, 204, 235], [117, 181, 239], [117, 128, 240]],
                  "bridge": [[187, 187, 53], [105, 105, 15], [134, 134, 29], [124, 44, 0]]}


class Player(GameObject):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.rgb = 232, 232, 74


class PlayerMissile(GameObject):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.rgb = 232, 232, 74


class Helicopter(GameObject):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.rgb = 0, 64, 48


class Tanker(GameObject):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.rgb = 84, 160, 197


class FuelDepot(GameObject):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.rgb = 210, 91, 94

class House(GameObject):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.rgb = 214, 214, 214
        
class Bridge(GameObject):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.rgb = 134, 134, 29


class Jet(GameObject):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.rgb = 117, 181, 239


class PlayerScore(GameObject):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.rgb = 232, 232, 74


class Lives(GameObject):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.rgb = 232, 232, 74


def _detect_objects(objects, obs, hud=False):
    
    #Player
    player_bb = find_objects(obs, objects_colors["player"], min_distance=1, size = (7,13), tol_s = (2,1))
    match_objects(objects, player_bb, 0, 1, Player)
    start_idx = 1

    #PlayerMissile
    missile_bb = find_objects(
        obs, objects_colors["player_missile"], min_distance=1, size=(1,8), tol_s=0)
    match_objects(objects, missile_bb, start_idx, 1, PlayerMissile)
    start_idx+=1
    
    #FuelDepot
    fuel_bb = find_mc_objects(obs, objects_colors["fuel_depot"], min_distance=1)
    match_objects(objects, fuel_bb, start_idx,4, FuelDepot)
    start_idx+=4
    
    #Tanker
    tanker_bb = find_mc_objects(
        obs, objects_colors["tanker"], min_distance=1, minx=10, miny=3, maxy=162, size=(17,9))
    match_objects(objects, tanker_bb, start_idx, 4, Tanker)
    start_idx+=4
    
    #Helicopter
    helicopter_bb = find_mc_objects(
        obs, objects_colors["helicopter"], min_distance=1, size= (8,10), tol_s=0)
    match_objects(objects, helicopter_bb, start_idx, 4, Helicopter)
    start_idx+=4
    
    
    #House
    house_bb = find_mc_objects(obs, objects_colors["house"], size= (17,20), minx=8, all_colors=False)
    match_objects(objects, house_bb, start_idx, 4, House)
    start_idx+=4

    #Jet
    jet_bb = find_mc_objects(obs, objects_colors["jet"], min_distance=1, size= (9,6))
    match_objects(objects, jet_bb, start_idx, 4, Jet)
    start_idx+=4

    #Bridge
    bridge_bb = find_mc_objects(obs, objects_colors["bridge"], min_distance=1)
    if bridge_bb:
        objects[start_idx]= Bridge(*bridge_bb[0])
    else:
        objects[start_idx]= NoObject()
    start_idx+=1
        
    if hud:
        lives_bb = find_objects(obs, objects_colors["lives"], min_distance=1, size=(6,8))
        if lives_bb:
            objects[start_idx]= Lives(*lives_bb[0])
        else:
            objects[start_idx]= NoObject()
        start_idx+=1
        
        score_bb = find_objects(
            obs, objects_colors["score"], miny=163, maxy=175, min_distance=1, closing_dist=6)
        if score_bb:
            objects[start_idx]= PlayerScore(*score_bb[0])

        
