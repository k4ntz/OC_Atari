from .utils import find_objects, match_objects
from .game_objects import GameObject, NoObject

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
        self._visible = True


class Ball(GameObject):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.rgb = 200, 72, 72
        self._visible = True


class Block(GameObject):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.rgb = 66, 72, 200
        self._visible = True


class PlayerScore(GameObject):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.rgb = 142, 142, 142
        self._visible = True


class Live(GameObject):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.rgb = 142, 142, 142
        self._visible = True


class PlayerNumber(GameObject):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.rgb = 142, 142, 142
        self._visible = True


def _detect_objects(objects, obs, hud=False):

    player_bb = find_objects(obs, objects_colors["player"], min_distance=1, maxx=151)
    player = objects[0]
    for p in player_bb:
        if p[3] == 4 and p[2] > 4:
            if type(player) is NoObject:
                player = Player()
            player.xywh = p

    ball_bb = find_objects(obs, objects_colors["ball"], min_distance=1, size=(2, 4), tol_s=1)
    ball = objects[1]
    if len(ball_bb):
        for b in ball_bb:
            if type(ball) is NoObject:
                ball = Ball(*b)
            else:
                ball.xywh = b
        objects[1] = ball
    else:
        objects[1] = NoObject()

    base_list = 2
    for blockRowColor in blockRow_colors.values():
        block_row = find_objects(obs, blockRowColor, min_distance=1, maxy=100)
        for br in block_row:
            print(br)
            if br[3] == 6:
                base_list = int(2 + (br[0]-8)/4 + 6*(87-br[1]))
                x, y = br[0], br[1]
                for i in range(int(br[2]/4)):
                    # print(i+base_list)
                    if type(objects[i+base_list]) is NoObject:
                        objects[i+base_list] = Block(x, y, 4, 6)
                        objects[i+base_list].rgb = blockRowColor
                    x+=4


    # HUD section removed, due to being static

    # if hud:
        # score and lives are not detected because it detects the background, which has the same color
        # score = find_objects(obs, objects_colors["score"], min_distance=1, closing_dist=2)
        # for s in score:
        #     if s[2] < 160 and s[0] < 90:
        #         objects.append(PlayerScore(*s))

        # live = find_objects(obs, objects_colors["lives"], min_distance=1, closing_dist=1)
        # for l1 in live:
        #     if l1[2] < 160 and 136 > l1[0] > 97:
        #         objects.append(Live(*l1))

        # num = find_objects(obs, objects_colors["lives"], min_distance=1, closing_dist=1)
        # for nu in num:
        #     if nu[2] < 160 and nu[0] > 120:
        #         objects.append(PlayerNumber(*nu))
