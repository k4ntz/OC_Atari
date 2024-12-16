from .utils import find_objects, find_objects_in_color_range, match_objects, match_blinking_objects
from .game_objects import GameObject, NoObject

object_colors = {
    "player": [214, 92, 92],
    "enemy": [[213, 130, 74], [240, 170, 103]],
    "player_score": [101, 160, 225]
}


class Player(GameObject):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.rgb = 214, 92, 92


class PlayerMissile(GameObject):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.rgb = 214, 92, 92


class BombThrower(GameObject):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.rgb = 10, 10, 10


class Bomb(GameObject):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.rgb = 10, 10, 10


class FlyingEnemy(GameObject):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.rgb = 10, 10, 10
        self.num_frames_invisible = -1
        self.max_frames_invisible = 5


class PlayerScore(GameObject):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.rgb = 101, 160, 225


class Lives(GameObject):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.rgb = 214, 92, 92


def _detect_objects(objects, obs, hud=False):
    # detection and filtering

    # Player
    player_bb = find_objects(
        obs, object_colors["player"], miny=50, size=(8, 4), tol_s=1)
    match_objects(objects, player_bb, 0, 1, Player)

    # Missile
    # a little bit problematic as when our spaceship explodes the pieces have the same size
    missile_bb = find_objects_in_color_range(obs, [10, 10, 10], [250, 250, 250],
                                             size=(8, 1), tol_s=0)
    if len(missile_bb) <= 1:
        match_objects(objects, missile_bb, 1, 1, PlayerMissile)

    # Bomb Thrower
    bomb_thrower_bb = find_objects_in_color_range(obs, [10, 10, 10], [250, 250, 250],
                                                  miny=35, maxy=50)
    match_objects(objects, bomb_thrower_bb, 2, 1, BombThrower)

    # Bomb
    # Starting Menu!!
    bomb_bb = find_objects_in_color_range(obs, [10, 10, 10], [250, 250, 250],
                                          size=(4, 1), tol_s=0)
    match_objects(objects, bomb_bb, 3, 1, Bomb)

    # Level 1 Enemy
    # Only 1 enemy is visible in each frame!
    flying_enemy_bb = find_objects_in_color_range(obs, [10, 10, 10], [250, 250, 250], miny=50,
                                                  size=(7, 10), tol_s=2)
    match_blinking_objects(objects, flying_enemy_bb, 4, 3, FlyingEnemy)

    # Player Score & Lives
    if hud:
        player_score_bb = find_objects(
            obs, object_colors["player_score"], maxy=25, closing_dist=10)
        match_objects(objects, player_score_bb, 7, 1, PlayerScore)

        lives_bb = find_objects(
            obs, object_colors["player"], miny=20, maxy=30, closing_dist=16)
        match_objects(objects, lives_bb, 8, 1, Lives)
