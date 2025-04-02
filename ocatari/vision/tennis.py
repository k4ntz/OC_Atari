from .utils import find_objects, find_mc_objects, match_objects
from .game_objects import GameObject, NoObject

objects_colors = {
    "player": [240, 128, 128],
    "enemy": [117, 128, 240],
    "ball": [236, 236, 236],
    "ball_shadow": [74, 74, 74],
    "enemy_score": [117, 128, 240],
    "player_score": [240, 128, 128],
    "logo": [240, 128, 128]
    }

fixed_objects_pos = {
    "player_score": [39, 4, 16, 8],
    "enemy_score": [104, 4, 16, 8],
    "logo": [39, 193, 33, 7]
}


class Player(GameObject):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.rgb = 240, 128, 128


class Enemy(GameObject):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.rgb = 117, 128, 240


class Ball(GameObject):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.rgb = 236, 236, 236


class BallShadow(GameObject):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.rgb = 74, 74, 74


class EnemyScore(GameObject):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.rgb = 117, 128, 240


class PlayerScore(GameObject):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.rgb = 240, 128, 128


def _detect_objects(objects, obs, hud):
    
    #Player
    player = objects[0]
    player_bb = find_objects(
        obs, objects_colors["player"], size = (13,23), min_distance=1, closing_dist=1)
    if player_bb:
        player.xywh = player_bb[0]
    start_idx = 1

    enemy_bb = find_objects(
        obs, objects_colors["enemy"], min_distance=1, closing_dist=1, size = (13,23))
    match_objects(objects, enemy_bb, start_idx, 1, Enemy)
    start_idx+=1

    ball_bb = find_objects(obs, objects_colors["ball"], min_distance=1, closing_dist=1, size=(2,2))
    match_objects(objects, ball_bb, start_idx, 1, Ball)
    start_idx+=1

    shadow_bb = find_objects(
        obs, objects_colors["ball_shadow"], min_distance=1, size =(2,2))
    match_objects(objects, shadow_bb, start_idx, 1, BallShadow)
    start_idx+=1


    if hud:
        player_score = find_objects(
            obs, objects_colors["player_score"], min_distance=1, closing_dist=5, size=(6,7))
        match_objects(objects, player_score, start_idx, 1, PlayerScore)
        
        start_idx+=1
        
        enemy_score = find_objects(
            obs, objects_colors["enemy_score"], min_distance=1, closing_dist=5, size=(6,7))
        match_objects(objects, enemy_score, start_idx, 1, EnemyScore)
        start_idx+=1
            
