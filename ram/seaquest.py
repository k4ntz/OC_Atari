from ._helper_methods import _convert_number


def _augment_info_seaquest_raw(info, ram_state):
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

def _augment_info_seaquest_human(info, ram_state):
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
    info["player_x"] = ram_state[70] - 21  # start x = 76, rightmost pos. x = 134 and leftmost reachable pos. x = 21
    info["player_y"] = ram_state[97] - 13  # starts at y = 13, underground at y = 108
    info["oxygen"] = (ram_state[102]/64) * 100 # oxygen in percent
    info["lives"] = ram_state[59]   # renders correctly up until 6 lives
    info["score"] = (_convert_number(ram_state[57]) * 100) + _convert_number(ram_state[58])  # the game saves these
    # numbers in 4 bit intervals (hexadecimal) but only displays the decimal numbers
    info["level"] = ram_state[61]  # changes enemies, speed, ... the higher the value the harder the game currently is
    info["divers_collected"] = ram_state[62]  # renders correctly up until 6 divers collected
    info["player_missiles_x"] = ram_state[103]

    if ram_state[86] == 0:
        info["player_direction"] = "rechts"
    else:
        info["player_direction"] = "links"
    
    info["enemy_x"] = {"first lane (lowest)": ram_state[30] - 21,  # the x-position of the left most enemy in that lane
                       "second lane": ram_state[31] - 21,  # even when that enemy is not displayed
                       "third lane": ram_state[32] - 21,
                       "fourth lane": ram_state[33] - 21,
                       "fifth lane (highest)": ram_state[118] - 21  # only moves if top_enemy_enabled is 2 or higher
                       }

    info["divers_x_or_enemy_missiles"] = {"first lane (lowest)": ram_state[71] - 21,
                                          "second lane": ram_state[72] - 21,
                                          "third lane": ram_state[73] - 21,
                                          "fourth lane": ram_state[74] - 21
                                          }  # relative to the leftmost and rightmost position of the player
    info["top_enemy_enabled"] = ram_state[60] >= 2  # enables the top ship if higher/equal than 2
    info["lane_y_position"] = {"first lane (lowest)": 87,
                               "second lane": 62,
                               "third lane": 37,
                               "fourth lane": 12,
                               "water surface": 0
                               }  # relative to the highest point of the player_position

    enemy_list = []
    for i in range(4):
        if ram_state[36+ i] % 8 == 0:
            enemy_list.append("no enemy")
        elif ram_state[36+ i] % 8 == 1:
            enemy_list.append("right enemy")
        elif ram_state[36+ i] % 8 == 2:
            enemy_list.append("middle enemy")
        elif ram_state[36+ i] % 8 == 3:
            enemy_list.append("right and middle enemy")
        elif ram_state[36+ i] % 8 == 4:
            enemy_list.append("left enemy")
        elif ram_state[36+ i] % 8 == 5:
            enemy_list.append("right and left enemy")
        elif ram_state[36+ i] % 8 == 6:
            enemy_list.append("middle and left enemy")
        elif ram_state[36+ i] % 8 == 7:
            enemy_list.append("right, middle and left enemy")

    info["enemy_variations"] = {"first lane (lowest)": enemy_list[1],
                                "second lane": enemy_list[2],
                                "third lane": enemy_list[3],
                                "fourth lane": enemy_list[4]}
    
    print(ram_state)

def _augment_info_seaquest_revised(info, ram_state):
    pass
