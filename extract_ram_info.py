import numpy as np


def augment_info(info, ram_state, game_name):
    """
    Augment the info dictionary with object centric information
    """
    if game_name == "Breakout":
        _augment_info_breakout(info, ram_state)
    if game_name == "Skiing":
        _augment_info_skiing(info, ram_state)
    if game_name == "Seaquest":
        _augment_info_seaquest(info, ram_state)


# Pong
def _augment_info_pong(info, ram_state):
    print("FIND OFFSET")
    info["ball"] = ram_state[99], ram_state[101]
    info["player"] = ram_state[72], ram_state[51]
    # TODO
    # info["enemy"] = ram_state[2]


# Breakout
def _augment_info_breakout(info, ram_state):
    info["block_bitmap"] = _make_block_bitmap(ram_state)
    info["ball"] = ram_state[99], ram_state[101]
    info["player"] = ram_state[72] - 47, 189
    print(ram_state)


# Skiing
def _augment_info_skiing(info, ram_state):
    # player start bei x = 76
    info["player_x"] = ram_state[25]        # can go up to 150 (170 and you are back to the left side)
    info["player_y"] = ram_state[26]        # constant 120
    info["score"] = _convert_number(ram_state[107])
    info["speed"] = ram_state[14]
    info["time"] = _time_skiing(ram_state)
    info["objects_y"] = ram_state[86:93]    # you cannot assign to specific objects. they are random
    print(ram_state)


# Seaquest
def _augment_info_seaquest(info, ram_state):
    info["player_x"] = ram_state[70] #starts at x = 76, rightmost position is x = 134 and leftmost position is x = 21
    info["player_y"] = ram_state[97] #starts at y = 13 the lowest it can go is y = 108
    info["oxygen"] = ram_state[102] #0-64: 64 is full oxygen
    info["Enemy_x"] = ram_state[30-33] #probably bigger but first level only has max 4 enemies
    info["divers_x"] = {73 : ram_state[73], 74 : ram_state[74]} #probably also bigger in later levels
    info["divers_collected"] = ram_state[62] #renders correctly up till 6 divers collected
    info["lives"] = ram_state[59] #renders correctly up till 6 lives
    info["score"] = _convert_number(ram_state[57]) , _convert_number(ram_state[58]) #the game saves these numbers in 4 bit intervals (hexadecimal) but only displays the decimal numbers
    #1 has something to do with seed or level (changes the spawns but doesnt really make it more difficult) at 253-255 it goes crazy

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
    time = {}
    # minutes
    time["minutes"] = _convert_number(ram_state[104])
    # seconds
    time["seconds"] = _convert_number(ram_state[105])
    # milliseconds
    time["milli_seconds"] = _convert_number(ram_state[106])
    return time


def _convert_number(number):
    """
    The game SKIING displays the time/score in hexadecimal numbers, while the ram extraction displays it as an integer.
    This results in a required conversion from the extracted ram number (in dec) to a hex number, which we then display
    as a dec number.

    e.g.: game shows 10 seconds, but the ram display saves it as 16
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
