
from .utils import find_objects, find_mc_objects, match_objects
from .game_objects import GameObject, NoObject

grayscaled_objects_colors = {
    'player': [[[169, 169, 169], [131, 131, 131], [85, 85, 85], [151, 151, 151]],
               [[169, 169, 169], [131, 131, 131], [85, 85, 85], [228, 228, 228]]],
    'missile': [236, 236, 236],
    'building': [[114, 114, 114], [[114, 114, 114], [151, 151, 151]]],
    'enemy25': [[135, 135, 135], [151, 151, 151], [109, 109, 109], [197, 197, 197],
                [137, 137, 137], [116, 116, 116], [161, 161, 161]],
    'enemy50': [[129, 129, 129], [151, 151, 151]],
    'enemy75': [86, 86, 86],
    'enemy100': [[137, 137, 137], [116, 116, 116], [161, 161, 161], [199, 199, 199],
                 [118, 118, 118]],
    'player_score': [131, 131, 131],
    'lives': [151, 151, 151]
}

colored_objects_colors = {
    'player': [[[121, 181, 236], [87, 139, 201], [47, 90, 160], [212, 252, 144]],
               [[121, 181, 236], [87, 139, 201], [47, 90, 160], [140, 172, 72]]],
    'missile': [236, 236, 236],
    'building': [[150, 113, 26], [[150, 113, 26], [162, 128, 238]]],
    'enemy25': [
        [147, 111, 223], [151, 151, 151], [68, 116, 182], [128, 235, 180],
        [72, 176, 110], [160, 107, 50], [201, 154, 92]
    ],
    'enemy50': [[183, 92, 176], [162, 128, 238]],
    'enemy75': [72, 72, 194],
    'enemy100': [[72, 176, 110], [160, 107, 50], [201, 154, 92], [236, 194, 128],
                 [118, 118, 118]],
    'player_score': [87, 139, 201],
    'lives': [151, 151, 151]
}


class Player(GameObject):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.rgb = 236, 236, 236


class Building(GameObject):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.rgb = 184, 70, 162


class Enemy25(GameObject):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.rgb = 195, 164, 61


class Enemy50(GameObject):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.rgb = 195, 164, 61


class Enemy75(GameObject):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.rgb = 195, 164, 61


class Enemy100(GameObject):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.rgb = 195, 164, 61

# It would be better to separate player missiles and enemy missiles.
# (They have exact same shape and color)


class Missile(GameObject):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.rgb = 236, 236, 236

# class PlayerMissile(GameObject):
#     def __init__(self, *args, **kwargs):
#         super().__init__(*args, **kwargs)
#         self.rgb = 236, 236, 236

# class EnemyMissile(GameObject):
#     def __init__(self, *args, **kwargs):
#         super().__init__(*args, **kwargs)
#         self.rgb = 236, 236, 236


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

    grayscaled_players = []
    for color in grayscaled_objects_colors["player"]:
        grayscaled_players += find_mc_objects(obs, color)
    colored_players = []
    for color in colored_objects_colors["player"]:
        colored_players += find_mc_objects(obs, color)

    if grayscaled_players:
        player.xywh = grayscaled_players[0]
    elif colored_players:
        player.xywh = colored_players[0]

    # Building
    all_buildings = []
    grayscaled_undamaged_buildings = find_mc_objects(
        obs, grayscaled_objects_colors["building"][1], closing_dist=5)
    grayscaled_damaged_buildings = find_objects(
        obs, grayscaled_objects_colors["building"][0], closing_dist=5)
    for b in grayscaled_undamaged_buildings:
        all_buildings.append(b)
    for b in grayscaled_damaged_buildings:
        already_extracted = False
        for ud_b in grayscaled_undamaged_buildings:
            if b[0] == ud_b[0]:
                already_extracted = True
                break
        if already_extracted == False:
            all_buildings.append(b)

    colored_undamaged_buildings = find_mc_objects(
        obs, colored_objects_colors["building"][1], closing_dist=5)
    colored_damaged_buildings = find_objects(
        obs, colored_objects_colors["building"][0], closing_dist=5)
    for b in colored_undamaged_buildings:
        all_buildings.append(b)
    for b in colored_damaged_buildings:
        already_extracted = False
        for ud_b in colored_undamaged_buildings:
            if b[0] == ud_b[0]:
                already_extracted = True
                break
        if already_extracted == False:
            all_buildings.append(b)
    match_objects(objects, all_buildings, 1, 3, Building)

    # Enemy
    grayscaled_enemy25s = find_mc_objects(
        obs, grayscaled_objects_colors["enemy25"])
    colored_enemy25s = find_mc_objects(obs, colored_objects_colors["enemy25"])
    match_objects(objects, grayscaled_enemy25s +
                  colored_enemy25s, 4, 3, Enemy25)

    grayscaled_enemy50s = find_mc_objects(
        obs, grayscaled_objects_colors["enemy50"])
    colored_enemy50s = find_mc_objects(obs, colored_objects_colors["enemy50"])
    match_objects(objects, grayscaled_enemy50s +
                  colored_enemy50s, 7, 3, Enemy50)

    grayscaled_enemy75s = find_objects(
        obs, grayscaled_objects_colors["enemy75"])
    colored_enemy75s = find_objects(obs, colored_objects_colors["enemy75"])
    match_objects(objects, grayscaled_enemy75s +
                  colored_enemy75s, 10, 3, Enemy75)

    grayscaled_enemy100s = find_mc_objects(
        obs, grayscaled_objects_colors["enemy100"])
    colored_enemy100s = find_mc_objects(
        obs, colored_objects_colors["enemy100"])
    match_objects(objects, grayscaled_enemy100s +
                  colored_enemy100s, 13, 3, Enemy100)

    # Missiles
    # ERROR: The missiles flash and the function looses them.
    missiles = find_objects(obs, grayscaled_objects_colors['missile'],
                            size=(2, 2), tol_s=0, maxy=157)
    match_objects(objects, missiles, 16, 2, Missile)

    # PlayerScore & Lives
    if hud:
        grayscaled_player_score = find_objects(
            obs, grayscaled_objects_colors["player_score"], maxy=20, closing_dist=8)
        colored_player_score = find_objects(
            obs, colored_objects_colors["player_score"], maxy=20, closing_dist=8)
        all_player_scores = grayscaled_player_score + colored_player_score
        match_objects(objects, all_player_scores, 18, 1, PlayerScore)

        lives = find_objects(
            obs, grayscaled_objects_colors["lives"], miny=215, maxy=225, closing_dist=5)
        match_objects(objects, lives, 19, 1, PlayerScore)
