from .utils import find_objects, find_mc_objects, find_objects_in_color_range, match_objects
from .game_objects import GameObject, NoObject
import numpy as np
import matplotlib as plt


objects_colors = {
    "Player": [[162, 98, 33], [198, 108, 58], [142, 142, 142], [162, 162, 42]],
    "Bear":[[111, 111, 111],[214,214,214]],
    "House": [142, 142, 142],
    "Door" : [[0,0,0],[213,130,74]],
    "Bird": [132, 144, 252],
    "Crab": [213, 130, 74],
    "Clam": [210, 210, 64], 
    "Greenfish": [111, 210, 111],
    "FloatingBlock": [[214, 214, 214], [84, 138, 210]],
    "hud_objs": [132, 144, 252],  
}


plate_per_col = [6, 6, 6, 6]
birds_per_col = [2,2,2,2]
floors = floors = [[82, 105], [108, 130], [134, 155], [160, 180]]


class Player(GameObject):
    """
    The player figure: Frostbite Bailey.
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._xy = 0, 0
        self.wh = (8, 18)
        self.rgb = 198, 108, 58
        self.hud = False


class Bear(GameObject):
    """
    The dangerous grizzly polar bears on the shore (level 4).
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.rgb = 111, 111, 111
        self.hud = False
        self.wh = (14, 16)
        self._xy = 0, 0


class House(GameObject):
    """
    The igloo Frostbite Bailey is trying to build.
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.rgb = 142, 142, 142
        self.hud = False
        self.wh = (8, 18)
        self._xy = 0, 0


class Door(GameObject):
    """
    The finished igloo.
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._xy = 123, 47
        self.rgb = 0, 0, 0
        self.hud = False
        self.wh = 8, 8


class FloatingBlock(GameObject):
    """
    The white, untouched ice floes, turning blue once jumped over.
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.rgb = 214, 214, 214
        self.hud = False
        self.wh = 24, 7
        self._xy = 0, 0

class Bird(GameObject):
    """
    The wild snowgeese.
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.rgb = 132, 144, 252
        self.hud = False
        self.wh = (8, 7)
        self._xy = 0, 0


class Crab(GameObject):
    """
    The dangerous Alaskan king crabs.
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.rgb = 213, 130, 74
        self.hud = False
        self.wh = (8, 7)
        self._xy = 0, 0


class GreenFish(GameObject):
    """
    The fresh fish swimming by regularly.
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.rgb = 111, 210, 111
        self.wh = (8, 6)
        self.hud = False
        self._xy = 0, 0


class Clam(GameObject):
    """
    The dangerous clams.
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.rgb = 210, 210, 64
        self.hud = False
        self._xy = 0, 0
        self.wh = (8, 7)


class Lives(GameObject):
    """
    The indicator for the player's lives.
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._xy = 63, 22
        self.rgb = 132, 144, 252
        self.hud = True
        self.wh = 6, 8


class Temperature(GameObject):
    """
    The temperature display.
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._xy = 23, 22
        self.wh = 18, 8
        self.rgb = 132, 144, 252
        self.hud = True


class Score(GameObject):
    """
    The player's score display.
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._xy = 63, 10
        self.rgb = 132, 144, 252
        self.hud = True
        self.wh = 6, 8



def _detect_objects(objects, obs, hud=False):
    
    # detection and filtering
    
    #Player
    player = objects[0]
    player_bb = find_mc_objects(obs, objects_colors["Player"], size=(8, 17), tol_s=2, closing_active=False)
    if player_bb:
        player.xywh = player_bb[0]
    start_idx = 1
    
    #Bear
    bear_bb = []
    for color in objects_colors["Bear"]:
        bear_bb += find_objects(
            obs, color, miny=13, maxy=75, size=(14, 15), tol_s=5)
    match_objects(objects, bear_bb, start_idx, 1, Bear)
    start_idx += 1
    
    #House
    house_bb = find_objects(
        obs, objects_colors["House"], minx=112, miny=42, maxx=155, maxy=62, closing_active=True, closing_dist= 10)
    match_objects(objects, house_bb, start_idx, 1, House)
    start_idx +=1
    
    #Door 
    door_bb = []
    for color in objects_colors["Door"]:
        door_bb += find_objects(obs, color , miny=43, maxy=56, minx=120, maxx=133)
    if door_bb: 
        objects[start_idx] = Door(*door_bb[0])
    else:
        objects[start_idx] = NoObject()
    start_idx += 1
        
    #Birds
    for nbbirds, (miny, maxy) in zip(birds_per_col, floors):
        birds_bb = [list(bb) for bb in find_objects(obs, objects_colors["Bird"], closing_active= False, size=(8, 7), tol_s=2, miny=miny, maxy=maxy)]
        match_objects(objects, birds_bb, start_idx, nbbirds, Bird)
        start_idx += nbbirds

    #Crabs
    for nbcrabs, (miny, maxy) in zip(birds_per_col, floors):
        crabs_bb = [list(bb) for bb in find_objects(obs, objects_colors["Crab"], miny=miny, maxy=maxy)]
        match_objects(objects, crabs_bb, start_idx, nbcrabs, Crab)
        start_idx += nbcrabs
    
    #Clams
    for nbclams, (miny, maxy) in zip(birds_per_col, floors):
        clams_bb = [list(bb) for bb in find_objects(obs, objects_colors["Clam"], miny=miny, maxy=maxy)]
        match_objects(objects, clams_bb, start_idx, nbclams, Clam)
        start_idx += nbclams
    
    #GreenFish
    for nbfish, (miny, maxy) in zip(birds_per_col, floors):
        fish_bb = [list(bb) for bb in find_objects(obs, objects_colors["Greenfish"], size=(8, 6), tol_s=2, miny=miny, maxy=maxy)]
        match_objects(objects, fish_bb, start_idx, nbclams, GreenFish)
        start_idx += nbfish
    
    for nbblock, (miny, maxy) in zip(plate_per_col, floors):
        plates_bb = []
        for color in objects_colors["FloatingBlock"]:
            plates_bb += [list(bb) + [color] for bb in find_objects(
            obs, color, closing_active=False, min_distance=0 , size=(20, 7), miny=miny, maxy=maxy)]
        match_objects(objects, plates_bb, start_idx, nbblock, FloatingBlock)
        start_idx += nbblock


    if hud:
        lifecount_bb = find_objects(
            obs, objects_colors["hud_objs"], closing_dist=10, minx=50, miny=19, maxx=75, maxy=32)
        if lifecount_bb:
            objects[start_idx] = Lives(*lifecount_bb[0])
        else:
            objects[start_idx] = NoObject()
        start_idx += 1

        degrees_bb = find_objects(
            obs, objects_colors["hud_objs"], closing_dist=10, minx=19, miny=19, maxx=37, maxy=30)
        match_objects(objects, degrees_bb, start_idx, 1, Temperature)
        start_idx += 1

        score_bb = find_objects(
            obs, objects_colors["hud_objs"], closing_dist=10, minx=40, miny=8, maxx=75, maxy=18)
        match_objects(objects, score_bb, start_idx, 1, Score)