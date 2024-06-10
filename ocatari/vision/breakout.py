from .utils import find_objects
from .game_objects import GameObject

objects_colors = {"background": [0, 0, 0], "player": [200, 72, 72], "ball": [200, 72, 72], "lives": [142, 142, 142],
                  "score": [142, 142, 142], "player_num": [142, 142, 142], "background_2": [142, 142, 142]}

blockRow_colors = {"block_row_first": [66, 72, 200],
                   "block_row_second": [72, 160, 72], "block_row_third": [162, 162, 42],
                   "block_row_fourth": [180, 122, 48],
                   "block_row_fifth": [198, 108, 58], "block_row_sixth": [200, 72, 72]}


class Player(GameObject):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.rgb = 200, 72, 72


class Ball(GameObject):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.rgb = 200, 72, 72


class BlockRow(GameObject):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.rgb = 66, 72, 200


class PlayerScore(GameObject):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.rgb = 142, 142, 142


class Live(GameObject):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.rgb = 142, 142, 142


class PlayerNumber(GameObject):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.rgb = 142, 142, 142


def _detect_objects(objects, obs, hud=False):
    objects.clear()

    player = find_objects(obs, objects_colors["player"], min_distance=1, maxx=151)
    for p in player:
        if p[3] == 4 and p[2] > 4:
            player = Player(*p)
            player.wh = 16, 4
            objects.append(player)

    ball = find_objects(obs, objects_colors["ball"], min_distance=1)
    for b in ball:
        if b[2] == 2 and b[3] == 4:
            objects.append(Ball(*b))

    for blockRowColor in blockRow_colors.values():
        block_row = find_objects(obs, blockRowColor, min_distance=1)
        for br in block_row:
            if br[3] == 6 and br[1] < 100:
                blockrow_inst = BlockRow(*br)
                blockrow_inst.rgb = blockRowColor
                objects.append(blockrow_inst)

    if hud:
        # score and lives are not detected because it detects the background, which has the same color
        score = find_objects(obs, objects_colors["score"], min_distance=1, closing_dist=2)
        for s in score:
            if s[2] < 160 and s[0] < 90:
                objects.append(PlayerScore(*s))

        live = find_objects(obs, objects_colors["lives"], min_distance=1, closing_dist=1)
        for l1 in live:
            if l1[2] < 160 and 136 > l1[0] > 97:
                objects.append(Live(*l1))

        num = find_objects(obs, objects_colors["lives"], min_distance=1, closing_dist=1)
        for nu in num:
            if nu[2] < 160 and nu[0] > 120:
                objects.append(PlayerNumber(*nu))
