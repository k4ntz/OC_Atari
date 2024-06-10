import numpy as np
from .game_objects import GameObject
from ._helper_methods import _convert_number
import sys

"""
RAM extraction for the game BREAKOUT. Supported modes: ram
"""

# might be wrong
# blockrow could go very very high with a performing agent

MAX_NB_OBJECTS = {'Player': 1, 'Ball': 1, 'BlockRow': 50}    # blockrow could go very very high with a performing agent
MAX_NB_OBJECTS_HUD = {'Player': 1, 'PlayerScore': 3, 'Live': 1, 'PlayerNumber': 1, 'BlockRow': 50, 'Ball': 1}

class Player(GameObject):
    """
    The player figure i.e., the paddle. 
    """
    
    def __init__(self):
        super().__init__()
        self._xy = 99, 189
        self.wh = 16, 4
        self.rgb = 200, 72, 72
        self.hud = False


class Ball(GameObject):
    """
    The game ball. 
    """
    
    def __init__(self):
        super().__init__()
        self._xy = 0, 0
        self.wh = 2, 4
        self.rgb = 200, 72, 72
        self.hud = False


class PlayerScore(GameObject):
    """
    The player's score display (HUD).
    """
    
    def __init__(self):
        super().__init__()
        self._xy = 36, 6
        self.rgb = 142, 142, 142
        self.wh = 12, 10
        self.hud = True

    def __eq__(self, o):
        return isinstance(o, PlayerScore) and self.xy == o.xy


class Live(GameObject):
    """
    The indicator for the remaining balls (lives) (HUD).
    """
    
    def __init__(self):
        super().__init__()
        self._xy = 100, 5
        self.rgb = 142, 142, 142
        self.wh = 12, 10
        self.hud = True


class BlockRow(GameObject):
    """
    The rows of the brickwall.
    """
    
    def __init__(self):
        super().__init__()
        self.xy = 8, 87
        self.wh = 144, 6
        self.rgb = 66, 72, 200
        self.hud = False


class PlayerNumber(GameObject):
    """
    The player index display (HUD).
    """


    def __init__(self):
        super().__init__()
        self.xy = 136, 5
        self.wh = 4, 10
        self.rgb = 142, 142, 142
        self.hud = True


blockRow_colors = {"5": [66, 72, 200], "4": [72, 160, 72],
                   "3": [162, 162, 42], "2": [180, 122, 48],
                   "1": [198, 108, 58], "0": [200, 72, 72]}


# parses MAX_NB* dicts, returns default init list of objects
def _get_max_objects(hud=False):

    def fromdict(max_obj_dict):
        objects = []
        mod = sys.modules[__name__]
        for k, v in max_obj_dict.items():
            for _ in range(0, v):
                objects.append(getattr(mod, k)())    
        return objects

    if hud:
        return fromdict(MAX_NB_OBJECTS_HUD)
    return fromdict(MAX_NB_OBJECTS)

def _init_objects_ram(hud=False):
    """
    (Re)Initialize the objects
    """
    objects = [Player()]

    if hud:
        objects.extend([PlayerScore(), PlayerScore(), PlayerScore(), Live(), PlayerNumber()])

    y = 87
    objects.append(Ball())
    for color in blockRow_colors:
        row = BlockRow()
        row.rgb = (blockRow_colors.get(color))
        row.xy = 8, y
        objects.append(row)
        y -= 6
    return objects


def _make_block_bitmap(ram_state):
    """
    Create an ordered block bitmap of the game BREAKOUT from the ram state.

    input ram
    output ordered block bitmap
    """
    array = ram_state[:36].reshape(-1, 6)
    global previous_array_str
    blocks_str = ""
    for row in np.array(array).T:
        row_str = ""
        for j, bitnumber in enumerate(row):
            if j == 0:
                row_str = '{0:06b}'.format(bitnumber)[::-2] + row_str
            elif j == 5:
                row_str = '{0:08b}'.format(bitnumber)[1::-2] + row_str
            else:
                row_str = '{0:08b}'.format(bitnumber)[::-2] + row_str
        blocks_str = row_str + "\n" + blocks_str
    # convert str to binary array
    blocks_int = np.array([list(el) for el in blocks_str.split("\n") if el], dtype=int)
    correct_order = [0, 4, 3, 2, 1, 5, 6, 7, 8, 11, 12, 16, 15, 14, 13, 17, 18, 19]
    blocks_int = blocks_int.T[correct_order].T
    # diff(previous_array_str, str(blocks_int))
    # previous_array_str = str(blocks_int)
    return blocks_int


def _detect_objects_ram(objects, ram_state, hud=False):
    """
       For all objects:
       (x, y, w, h, r, g, b)
    """

    # set default coord if object does not exist
    player = objects[0]
    score1, score2, score3, lives, player_num = objects[1:6]

    # player
    player.xy = ram_state[72] - 47, 189

    if hud:
        del objects[6:]
    else:
        del objects[1:]

    # ball
    if ram_state[101] + 9 <= 196 and ram_state[101] != 0:  # else no ball
        ball = Ball()
        ball.xy = ram_state[99] - 49, ram_state[101] + 9
        objects.append(ball)

    blocks = _calculate_blocks(ram_state)
    objects.extend(blocks)

    if hud:
        # 1 is more thin than the other numbers
        if ram_state[57] == 1:
            lives.xy = 104, 5
            lives.wh = 4, 10
        elif ram_state[57] == 0:
            lives.xy = 100, 5
            lives.wh = 12, 10

        score1.xy = 68, 5
        score1.wh = 12, 10
        score2.xy = 52, 5
        score2.wh = 12, 10
        score3.xy = 36, 5
        score3.wh = 12, 10

        # 1 is more thin than the other numbers
        if _convert_number(ram_state[77]) % 10 == 1:
            score1.wh = 4, 10
            score1.xy = 72, 5

        if 9 < _convert_number(ram_state[77]) < 20:
            score2.wh = 4, 10
            score2.xy = 56, 5

        if _convert_number(ram_state[76] == 1):
            score3.xy = 40, 5
            score3.wh = 4, 10


def _calculate_blocks(ram_state):
    """
    Calculate the block lengths for all rows.
    """
    bitmap = _make_block_bitmap(ram_state)
    blocks = []

    for row in range(6):
        start_of_new_block = True
        row_empty = True
        x = 0
        width = 0
        for column in range(18):
            if bitmap[row, column] == 1 and start_of_new_block:
                x = 8 + column * 8
                start_of_new_block = False
                row_empty = False
                width = 0

            if bitmap[row, column] == 1:
                width += 8

            if (bitmap[row, column] == 0 or column == 17) and row_empty is False and start_of_new_block is False:
                block = BlockRow()
                block.rgb = blockRow_colors.get(str(row))  # uses the blockRow color dictionary
                block.xy = x, 57 + 6 * row
                block.wh = width, 6
                blocks.append(block)
                start_of_new_block = True
    return blocks


def _detect_objects_breakout_raw(info, ram_state):
    # player_x
    player = [ram_state[72]]
    # ball x and ball y
    ball = [ram_state[99], ram_state[101]]
    blocks = ram_state[0:36]
    relevant_objects = player + ball + blocks.tolist()
    info["relevant_objects"] = relevant_objects

    # additional info
    info["block_bitmap"] = _make_block_bitmap(ram_state)
    info["lives"] = ram_state[57]
    info["score"] = _convert_number(ram_state[76]) * 100 + _convert_number(ram_state[77])
