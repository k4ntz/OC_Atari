from .game_objects import GameObject
import numpy as np

# MAX_NB_OBJS = {  # quentin's code (for skiing?)
#     "Player": 1,
#     "Tree": 4,
#     "Mogul": 3,
#     "Flag": 4
# }


class Player(GameObject):
    def __init__(self, num, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if num == 1:
            self.rgb = 92, 186, 92  # green
        else:
            self.rgb = 162, 134, 56  # yellow
        self.player_num = num
        self._xy = 0, 185
        self.wh = 7, 10
        self.hud = False


class Alien(GameObject):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.rgb = 134, 134, 29
        self._xy = 0, 0
        self.wh = 8, 10
        self.hud = False


class Satellite(GameObject):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.rgb = 151, 25, 122
        self._xy = 0, 0
        self.wh = 7, 8
        self.hud = False


class Shield(GameObject):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.rgb = 181, 83, 40
        self._xy = 0, 0
        self.wh = 8, 18
        self.hud = False


class Bullet(GameObject):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.rgb = 142, 142, 142
        self._xy = 0, 0
        # self.wh =
        self.hud = False


class Score(GameObject):
    def __init__(self, num, x, *args, **kwargs):  # , num,
        super().__init__(*args, **kwargs)
        if num == 1:
            self.rgb = 92, 186, 92
        else:
            self.rgb = 162, 134, 56
        self._xy = x, 10
        self.wh = 60, 10
        self.hud = True


class Lives(GameObject):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.rgb = 162, 134, 56
        self._xy = 84, 185
        self.wh = 12, 10
        self.hud = True


def _detect_objects_space_invaders_raw(info, ram_state):
    info["aliens"] = ram_state[16:24]
    info["x_positions"] = ram_state[26:31]
    info["shields"] = ram_state[43:70]
    info["lives"] = ram_state[73]
    info["bullets"] = ram_state[81:89]
    info["score"] = ram_state[102:106]
    # info["aliens_y"] = ram_state[16] % 32  # taking only the first 5 bits on the right
    # # ram_state[16] has also y of frame of players with shields together
    #
    # info["number_enemies"] = ram_state[17]  # number of alive aliens. if they are less the make the game quicker
    #
    # # positions of enemies from left to right are the individual, set bits from right to left
    # # rows are counted from bottom
    # # the two msb-bits are to be discarded. they remain 0
    # info["row_1"] = ram_state[18]
    # info["row_2"] = ram_state[19]
    # info["row_3"] = ram_state[20]
    # info["row_4"] = ram_state[21]
    # info["row_5"] = ram_state[22]
    # info["row_6"] = ram_state[23]
    # # ram[32:38] have the same value as ram[17:23] initialized. sense still not known
    #
    # info["visibility_players_shields"] = ram_state[24]
    #
    # info["aliens_x"] = ram_state[26]  # x of all aliens is common
    # info["shields_x"] = ram_state[27]  # shield_left is reference
    # info["player_green_x"] = ram_state[28]  # begins with 35. (0 < player_x < 255)
    # info["player_yellow_x"] = ram_state[29]  # begins with 117. (0 < player_x < 255)
    # info["satellite_dish_x"] = ram_state[30]
    #
    # info["graphics"] = ram_state[42]  # graphics of players being destroyed and visibility of score
    #
    # info["shields"] = ram_state[43:70]  # the 3 shields. they are represented in the same order as in the ram (from
    # left to right)
    # info["shield_left"] = ram_state[43:52]  # represented row by row in ram as single cell by another in same order
    # info["shield_middle"] = ram_state[52:61]  # represented row by row in ram as single cell by another in same order
    # info["shield_right"] = ram_state[61:70]  # represented row by row in ram as single cell by another in same order
    #
    # info["objects_colours"] = ram_state[71]  # colours
    # info["changing_symbols_enemies"] = ram_state[72]  # when destroyed
    #
    # info["lives"] = ram_state[73]  # you have 3 lives from beginning. they decrease and after 1 it gets set on 3
    #
    # info["temporal_reference"] = ram_state[74]  # works as temporal reference for the game
    #
    # # bullets
    # info["bullet_1_enemy_y"] = ram_state[81]
    # info["bullet_2_enemy_y"] = ram_state[82]
    # info["bullet_1_enemy_x"] = ram_state[83]
    # info["bullet_2_enemy_x"] = ram_state[84]
    # info["bullet_player_green_y"] = ram_state[85]
    # info["bullet_player_yellow_y"] = ram_state[86]
    # info["bullet_player_green_x"] = ram_state[87]
    # info["bullet_player_yellow_x"] = ram_state[88]
    # # you get able to shoot the other bullet, once the flying one disappears,
    #
    # # for an array-value for score there is two digits and arithmetic transfer(like from ram_state[104]) gets added
    # # to most significant digits (ram_state[102])
    # info["score_player_green"] = {ram_state[102], ram_state[104]}  # score is saved in hexadecimal in this order
    # info["score_player_yellow"] = {ram_state[103], ram_state[105]}  # score is saved in hexadecimal
    # # 200 points for destroying satellite dish
    # # x*5 points for destroying an alien from row_x
    print(ram_state)


def _init_objects_space_invaders_ram(hud=False):
    """
    (Re)Initialize the objects
    """
    objects = [Player(1)]  # , Alien()]  # , Satellite(), Shield(), Bullet()]
    if hud:
        objects.extend([Score(1, 4), Score(2, 84), Lives()])
    return objects


global prevRam

global aliens
# aliens = [[Alien() for a in range(6)] for b in range(6)]  # ~ 2-dim

global player
firstCall = True
lives_ctr = 30
global scores
global prevRam
prevRam = [i for i in range(256)]
global bullets


def _detect_objects_space_invaders_revised(objects, ram_state, hud=False):
    global firstCall
    global aliens
    global player
    global prevRam
    global lives_ctr
    global scores
    global bullets

    if lives_ctr:
        lives_ctr -= 1
    # print(lives_ctr)
    if lives_ctr == 0:
        # objects = [x for x in objects if not isinstance(x, Lives)]  # this line was the problem
        for i, obj in enumerate(objects):
            if isinstance(obj, Lives):
                objects.pop(i)
    # if something:
    #     objects.insert(3, Lives())

    if firstCall:  # works correctly
        player = objects[0]
        player.wh = 7, 10
        player.rgb = 92, 186, 92
        aliens = [Alien() for a in range(36)]  # ~ 1-dim
        for alien in aliens:
            # alien.rgb = 134, 134, 29
            alien.wh = 8, 10
        for i in range(3):
            objects.insert(4, Shield())
            objects[4].xy = 42 + i*32, 157
        bullets = [Bullet() for i in range(3)]
        if not hud:
            del objects[1:4]
        else:
            scores = objects[1:3]
        firstCall = False

    # PLAYER
    # updating player position
    player.xy = ram_state[28] - 1, 185
    # handle player flickering?

    # ALIENS
    # aliens deletion from objects:
    alien_poss = np.where([isinstance(a, Alien) for a in objects])[0]
    if len(alien_poss) > 0:
        # print(alien_poss[0], alien_poss[-1])
        del objects[alien_poss[0]:alien_poss[-1]+1]  # faster

    # aliens (permanent) deletion from array aliens:
    for i in range(6):
        for j in range(6):
            if not (ram_state[18 + i] % pow(2, j+1) >= pow(2, j)):  # enemies alive are saved in given ram_state
                aliens[(5-i)*6 + j] = None  # 5 here is max(range(6)) so we are counting lines in the other way around

    # updating positions of aliens
    x, y = ram_state[26], ram_state[16] % 16  # is %16 correct?
    for i in range(6):
        for j in range(6):
            if aliens[i*6 + j]:
                # if y >= 20:  # this is somehow broken! the 31 does not get added after y = 20
                #     aliens[i*6 + j].xy = x-1 + j*16, 31 + y*2 + i*18 + 32  # + 22 for x
                # else:
                aliens[i*6 + j].xy = x-1 + j*16, 31 + y*2 + i*18  # + 22 for x

    # adding aliens to array objects:
    objects.extend([x for x in aliens if x is not None])

    # SCORE
    if hud and not firstCall:
        if ram_state[30] != prevRam[30]:
            sat_checked = False
            for obj in objects:
                if isinstance(obj, Satellite):
                    obj.xy = ram_state[30]-1, 12
                    sat_checked = True
                if isinstance(obj, Score):
                    objects.remove(obj)
            if not sat_checked:
                sat_dish = Satellite()
                sat_dish.xy = ram_state[30]-1, 12
                objects.append(sat_dish)
        else:
            score_in = False
            for obj in objects:
                if isinstance(obj, Score):
                    score_in = True
            if not score_in:
                objects.insert(1, scores[0])
                objects.insert(2, scores[1])

    # visibility of shields
    for alien in aliens:
        if alien and alien.xy[1] + alien.wh[1] >= 157:
            for obj in objects:
                if isinstance(obj, Shield):
                    objects.remove(obj)

    prevRam = ram_state
    return objects
