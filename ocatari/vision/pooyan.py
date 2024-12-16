from .utils import find_objects, match_objects
from .game_objects import GameObject, NoObject

objects_colors = {
    # The second color is also used for bait.
    'player': [[236, 236, 236], [184, 70, 162]],
    'arrow': [236, 236, 236],
    'balloon': [[236, 236, 236],
                [127, 92, 213],
                [160, 171, 79],
                [187, 187, 53],
                [92, 186, 92],
                [214, 92, 92]],
    'enemy': [195, 144, 61],
    'stone': [[236, 236, 236],
              [127, 92, 213],
              [160, 171, 79],
              [187, 187, 53],
              [214, 92, 92],
              [92, 186, 92],
              [195, 144, 61],
              [162, 98, 33]],
    'rock': [162, 98, 33],
    'lives': [0, 0, 0]
}


class Player(GameObject):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.rgb = 236, 236, 236


class Arrow(GameObject):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.rgb = 236, 236, 236


class Bait(GameObject):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.rgb = 184, 70, 162


class Balloon(GameObject):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.rgb = 92, 186, 92


class Enemy(GameObject):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.rgb = 195, 164, 61


class Stone(GameObject):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.rgb = 92, 186, 92


class Rock(GameObject):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.rgb = 162, 98, 33


class PlayerScore(GameObject):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.rgb = 236, 236, 236
        self.hud = True


class Lives(GameObject):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.rgb = 0, 0, 0
        self.hud = True


def _detect_objects(objects, obs, hud=False):
    # detection and filtering

    # Player
    player = objects[0]
    white_players_bb = find_objects(obs, objects_colors["player"][0], tol_s=2,
                                    minx=129, miny=61, maxx=139, maxy=182)
    red_players_bb = find_objects(obs, objects_colors["player"][1], tol_s=2,
                                  minx=129, miny=61, maxx=139, maxy=182)
    if white_players_bb:
        player.xywh = white_players_bb[0]
    elif red_players_bb:
        player.xywh = red_players_bb[0]

    # Arrow
    arrows_bb = find_objects(obs, objects_colors['arrow'], size=(
        8, 1), tol_s=1, miny=61, maxx=129)
    match_objects(objects, arrows_bb, 1, 1, Arrow)

    # Bait
    unpicked_baits_bb = find_objects(obs, objects_colors['player'][0], size=(8, 4),
                                     tol_s=2, minx=129, miny=61, maxx=139, maxy=182)
    flying_baits_bb = find_objects(obs, objects_colors['player'][1], size=(8, 4),
                                   tol_s=2, miny=61, maxx=129)
    match_objects(objects, unpicked_baits_bb + flying_baits_bb, 2, 1, Bait)

    # Balloon
    minx = [43, 75, 107]
    maxx = [53, 85, 117]
    for i in range(6):
        balloons_bb = []
        balloons = find_objects(obs, objects_colors['balloon'][i],
                                minx=minx[i//2], miny=61, maxx=maxx[i//2], maxy=175)
        for balloon in balloons:
            if balloon[2] > 4 and balloon[3] > 4:
                balloons_bb.append(balloon)
        match_objects(objects, balloons_bb, 3+i, 1, Balloon)

    # Enemy
    for i in range(3):
        enemies_bb = []
        enemies = find_objects(obs, objects_colors['enemy'],
                               minx=minx[i], miny=69, maxx=maxx[i], maxy=184)
        for enemy in enemies:
            if enemy[2] > 4 and enemy[3] > 4:
                enemies_bb.append(enemy)
        match_objects(objects, enemies_bb, 9+i*2, 2, Enemy)
    climbing_enemies_bb = []
    for enemy in find_objects(obs, objects_colors['enemy'], minx=135, miny=69, maxy=184):
        if enemy[2] > 4 and enemy[3] > 4:
            climbing_enemies_bb.append(enemy)
    match_objects(objects, climbing_enemies_bb, 15, 1, Enemy)

    # Stone
    stone_bb = []
    for color in objects_colors['stone']:
        stone_bb += find_objects(obs, color, size=(4, 4), tol_s=0)
    match_objects(objects, stone_bb, 16, 1, Stone)

    # Rock
    rock_bb = find_objects(obs, objects_colors['rock'], size=(16, 11), tol_s=2)
    match_objects(objects, rock_bb, 17, 1, Rock)

    # PlayerScore
    if hud:
        player_score_bb = find_objects(
            obs, objects_colors["player"][0], maxy=13, closing_dist=8)
        match_objects(objects, player_score_bb, 18, 1, PlayerScore)

        lives_bb = find_objects(
            obs, objects_colors["lives"], miny=205, maxy=213, closing_dist=8)
        match_objects(objects, lives_bb, 19, 1, Lives)
