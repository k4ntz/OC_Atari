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
    info["player_x"] = ram_state[25]  # can go up to 150 (170 and you are back to the left side)
    info["player_y"] = ram_state[26]  # constant 120
    info["score"] = _convert_number(ram_state[107])
    #info["speed"] = ram_state[14] or ram[20] both seem to have very similar behavior
    info["time"] = _time_skiing(ram_state)
    info["object_y"] = ram_state[86:93]    # 93 is the newest object, 86 is the oldest
    info["object_x"] = ram_state[62:69]    # 69 is the newest object, 62 is the oldest
    info["object_type"] = ram_state[70:77] # 77 is the newest object, 70 is the oldest   | 85 for tree | 2 for flag | 5 for mogul
    info["object_colour"] = ram_state[78:85] # 85 is the newest object, 78 is the oldest  |probably not important
    print(ram_state)


# Seaquest
def _augment_info_seaquest(info, ram_state):
    """
    The game SEAQUEST displays the enemies and divers at specific lanes, where they move from the right side to the left
    or from the left side to the right. Thus there y-Position is fixed.
    Illustration:

    x=0                             x=158
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ (Surface, Lane 5)

    -------------------------------- (Lane 4)

    -------------------------------- (Lane 3)

    -------------------------------- (Lane 2)

    -------------------------------- (Lane 1)

    _________________________________ (Underground)

    """
    info["player_x"] = ram_state[70]  # start x = 76, rightmost pos. x = 134 and leftmost reachable pos. x = 21
    info["player_y"] = ram_state[97]  # starts at y = 13, underground at y = 108
    info["oxygen"] = ram_state[102]  # 0-64: 64 is full oxygen
    info["lives"] = ram_state[59]  # renders correctly up until 6 lives
    info["score"] = (_convert_number(ram_state[57]) * 100) + _convert_number(ram_state[58])  # the game saves these
    # numbers in 4 bit intervals (hexadecimal) but only displays the decimal numbers
    info["level"] = ram_state[61]  # changes enemies, speed, ... the higher the value the harder the game currently is
    info["divers_collected"] = ram_state[62]  # renders correctly up until 6 divers collected
    info["player_missiles_x"] = ram_state[103]
    info["player_direction"] = ram_state[86]  # 0: player faces to the right and 8: player faces to the left
    info["enemy_x"] = {"first lane (lowest)": ram_state[30],  # the x-position of the left most enemy in that lane
                       "second lane": ram_state[31],  # even when that enemy is not displayed
                       "third lane": ram_state[32],
                       "fourth lane": ram_state[33],
                       "fifth lane (highest)": ram_state[118]  # only moves if top_enemy_enabled is 2 or higher
                       }
    info["divers_x_or_enemy_missiles"] = {"first lane (lowest)": ram_state[71],
                                          "second lane": ram_state[72],
                                          "third lane": ram_state[73],
                                          "fourth lane": ram_state[74]
                                          }  # divers and enemy missiles share these RAM positions
    info["top_enemy_enabled"] = ram_state[60]  # enables the top ship if higher/equal than 2
    info["lane_y_position"] = {"first lane (lowest)": 100,
                               "second lane": 75,
                               "third lane": 50,
                               "fourth lane": 25,
                               "water surface": 13
                               }  # the lanes actual y-positions are not saved within the RAM, therefore these
    # are educated guesses
    info["enemy_variations"] = {"first lane (lowest)": ram_state[36] % 8,
                                "second lane": ram_state[37] % 8,
                                "third lane": ram_state[38] % 8,
                                "fourth lane": ram_state[39] % 8}
    # 0: no enemy; 1: only right enemy displayed; 2: only middle enemy ; 3: right and middle enemy;
    # 4: only left enemy; 5: right and left enemy ; 6: middle and left enemy; 7: left, middle, right enemy;
    # 8: same as 0; 9: same as 1 -> modulo 8
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


def _saturation_addition(x, offset):
    """
    The game SEAQUEST displays all enemies from x=0 (left side of the screen) up to x=158 (right side of the screen).
    These coordinates correspond to the player x-position and enemy x-position of the lowest lane extracted from the
    RAM. However the extracted value 0 for the other enemy lanes do not correspond to the left hand side of the screen.
    Thus they have to be manipulated by adding an offset, if the sum is over 255 the next value should be 0 because
    only values up to 255 are shown in the RAM.
    """

    return (x + offset) % 256
