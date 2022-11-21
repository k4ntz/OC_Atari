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
    info["score"] = _convert_number(ram_state[107])
    info["time"] = _time_skiing(ram_state)
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


def _time_skiing(ram_state):
    time = []
    # minutes
    time["minutes"] = _convert_number(ram_state[104]) #Würde sinn ergeben, ist aber noch nicht getestet :D 
    # seconds
    time["seconds"] = _convert_number(ram_state[105])
    # milliseconds
    time["milli_seconds"] = _convert_number(ram_state[106])
    return time

def _convert_number(number):
    """
    The game SKIING displays the time/score in hexadecimal numbers, while the ram extraction displays it as an integer. This results in a
    required conversion from the extractet ram number (in dec) to a hex number, which we then display as a dec number.

    eg.: game shows 10 seconds, but the ram display saves it as 16
    """
    number_str = str(hex(number))
    number_list = [*number_str]
    number_str = ""
    count = 0
    for x in number_list:
        if count > 1:
            number_str += x
        count += 1
    return int(number_str)
