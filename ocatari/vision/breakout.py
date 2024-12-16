from .utils import find_objects, match_objects
from .game_objects import GameObject, NoObject

objects_colors = {"background": [0, 0, 0], "player": [200, 72, 72], "ball": [200, 72, 72], "lives": [142, 142, 142],
                  "score": [142, 142, 142], "player_num": [142, 142, 142], "background_2": [142, 142, 142]}

block_colors = list(reversed([[66, 72, 200], [72, 160, 72], [162, 162, 42],
                              [180, 122, 48], [198, 108, 58], [200, 72, 72]]))


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
    player_bb = find_objects(
        obs, objects_colors["player"], min_distance=1, maxx=151)
    player = objects[0]
    for p in player_bb:
        if p[3] == 4 and p[2] > 4:
            if type(player) is NoObject:
                player = Player()
            player.xywh = p

    ball_bb = find_objects(
        obs, objects_colors["ball"], min_distance=1, size=(2, 4), tol_s=1)
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
    for i, blockRowColor in enumerate(block_colors):
        block_row = find_objects(
            obs, blockRowColor, min_distance=1, miny=57+6*i, maxy=63+6*i)
        for bb in block_row:
            if bb[2] == 2 and bb[3] == 4:
                block_row.remove(bb)
        block_row = sorted(block_row, key=lambda x: x[0])
        next_bb = block_row.pop(0) if block_row else None
        for j in range(18):
            if next_bb and next_bb[0] == 8 * (j + 1):
                if not objects[2 + i * 18 + j]:
                    objects[2 + i * 18 + j] = Block(*next_bb)
                else:
                    objects[2 + i * 18 + j].xywh = next_bb
                    objects[2 + i * 18 + j].rgb = blockRowColor
                next_bb = block_row.pop(0) if block_row else None
            else:
                if objects[2 + i * 18 + j]:
                    objects[2 + i * 18 + j] = NoObject()

    # old representation
    # for blockRowColor in block_colors.values():
    #     block_row = find_objects(obs, blockRowColor, min_distance=1, maxy=100)
    #     for br in block_row:
    #         if br[3] == 6:
    #             base_list = int(2 + (br[0]-8)/4 + 6*(87-br[1]))
    #             x, y = br[0], br[1]
    #             for i in range(int(br[2]/4)):
    #                 if type(objects[i+base_list]) is NoObject:
    #                     objects[i+base_list] = Block(x, y, 4, 6)
    #                     objects[i+base_list].rgb = blockRowColor
    #                 x+=4

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
