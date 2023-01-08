from ._helper_methods import _convert_number


def _augment_info_mspacman_raw(info, ram_state):
    """
    returns unprocessed list with
    player_x, player_y, ghosts_position_x, enemy_position_y, fruit_x, fruit_y
    """
    objects = {}
    objects["player_x"] = ram_state[10]
    objects["player_y"] = ram_state[16]
    objects["enemy_amount"] = ram_state[19]
    objects["ghosts_position_x"] = {"orange": ram_state[6],
                                    "cyan": ram_state[7],
                                    "pink": ram_state[8],
                                    "red": ram_state[9]
                                    }
    objects["enemy_position_y"] = {"orange": ram_state[12],
                                   "cyan": ram_state[13],
                                   "pink": ram_state[14],
                                   "red": ram_state[15]
                                    }
    objects["fruit_x"] = ram_state[11]
    objects["fruit_y"] = ram_state[17]
    info["object-list"] = objects


def _augment_info_mspacman_revised(info, ram_state):

    """
    There is a total of 4 levels
    If no more lives are displayed you will lose the game upon the next hit 
    """
    objects = {}
    
    objects["level"] = ram_state[0] # there is a total of 4 levels 0-3
    objects["score"] = (_convert_number(ram_state[122]) * 10000) + (_convert_number(ram_state[121]) * 100) + _convert_number(ram_state[120])
    objects["lives"] = ram_state[123] # If this state is 0 the game will be over upon the next hit
    
    objects["player_x"] = ram_state[10]
    objects["player_y"] = ram_state[16]

    objects["enemy_amount"] = ram_state[19]
    objects["ghosts_position_x"] = {"orange": ram_state[6],     
                                 "cyan": ram_state[7], 
                                 "pink": ram_state[8],     
                                 "red": ram_state[9]         
                                }
    objects["enemy_position_y"] = {"orange": ram_state[12], 
                                "cyan": ram_state[13],  
                                "pink": ram_state[14],   
                                "red": ram_state[15] 
                                }
    eatable = []
    eatable.append(ram_state[1] > 139)
    eatable.append(ram_state[2] > 124)
    eatable.append(ram_state[3] > 140)
    eatable.append(ram_state[4] > 130)
    objects["enemy_eatable"] = {   "orange": eatable[0], 
                                "cyan": eatable[1],  
                                "pink": eatable[2],  
                                "red": eatable[3]    
                                }
    objects["fruit_x"] = ram_state[11]
    objects["fruit_y"] = ram_state[17]
    objects["fruit_in_play"] = not (ram_state[11] == 0 and ram_state[17] == 0)

    if ram_state[123] < 16:
        collectable = "cherry"
    elif ram_state[123] < 32:
        collectable = "strawberry"
    elif ram_state[123] < 48:
        collectable = "orange"
    elif ram_state[123] < 64:
        collectable = "pretzel"
    elif ram_state[123] < 80:
        collectable = "apple"
    elif ram_state[123] < 96:
        collectable = "pear"
    elif ram_state[123] < 112:
        collectable = "banana"
    
    objects["fruit_type"] = collectable #  every value above will result in a glitched collectable
    
    objects["pac-dots_collected"] = ram_state[119]

    info["objects"] = objects
