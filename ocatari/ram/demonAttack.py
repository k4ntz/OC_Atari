

def _augment_info_demonAttack_raw(info, ram_state):
    info["lives"] = ram_state[114]  # 0-3 but renders correctly till 6
    info["player_x"] = ram_state[16]
    info["enemy_y"] = ram_state[69:71]  # 69 is topmost enemy 71 is lowest
    info["enemy_x"] = ram_state[13:15]  # 13 is topmost enemy 15 is lowest
    info["enemy_projectile_y"] = ram_state[37:46]
    """ kind of like a bit map. If a value is 0 then there is no projectile
    at that position the higher the value the thicker / more projectiles 
    at that position 37(ram) is highest possible enemy_position_y(lowest enemy)
    46(ram) is player position_y"""
    info["player_projectile_y"] = ram_state[21]
    info["player_projectile_x"] = ram_state[22]