import numpy as np


def augment_info(info, ram_state, game_name):
    """
    Augment the info dictionary with object centric informations
    """
    if game_name == "Breakout":
        _augment_info_breakout(info, ram_state)
    if game_name == "Skiing":
        _augment_info_skiing(info, ram_state)

# Breakout
def _augment_info_pong(info, ram_state):
    print("FIND OFFSET")
    info["ball"] = ram_state[99], ram_state[101]
    info["player"] = ram_state[72], ram_state[51]
    #TODO
    #info["enemy"] = ram_state[2]

# Breakout
def _augment_info_breakout(info, ram_state):
    info["block_bitmap"] = _make_block_bitmap(ram_state)
    info["ball"] = ram_state[99], ram_state[101]
    info["player"] = ram_state[72] - 47, 189
    print(ram_state)

def _augment_info_skiing(info, ram_state):
    # player start bei x = 76
    info["player_x"] = ram_state[25]
    info["score"] = _score_skiing(ram_state)
    print(ram_state)


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

def _score_skiing(ram_state):
    # the starting score is 20 thus the offset 12
    if ram_state[107] == 32:
        return ram_state[107] - 12

    # the score of 10 to 19 is equivalent to the value 25 to 16 of position 107 thus a offset of 6 is needed
    elif ram_state[107] >= 16:
        return ram_state[107] - 6

    # the score of 0 to 9 is equivalent to the value 0 to 9 of position 107 thus no offset is needed
    else:
        return ram_state[107]

    # the other values interpret symbols which are not representative for the score