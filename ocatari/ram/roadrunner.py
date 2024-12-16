from .game_objects import GameObject
import sys

"""
RAM extraction for the game Road Runner.
"""

MAX_NB_OBJECTS = {"Player": 1, "Enemy": 1, "BirdSeeds": 1, "Truck": 6}
MAX_NB_OBJECTS_HUD = {'Cactus': 6, 'Sign': 1}  # 'Score': 1}


class Player(GameObject):
    """
    The player figure i.e, the Road Runner.
    """

    def __init__(self):
        super().__init__()
        self._xy = 0, 0
        self.wh = (8, 32)
        self.rgb = 101, 111, 228
        self.hud = False


class Enemy(GameObject):
    """
    Wile E. Coyote.
    """

    def __init__(self):
        super().__init__()
        self._xy = 0, 0
        self.wh = (7, 29)
        self.rgb = 198, 108, 58
        self.hud = False


class BirdSeeds(GameObject):
    """
    The collectable piles of birdseed on the roadway.
    """

    def __init__(self):
        super().__init__()
        self._xy = 0, 0
        self.wh = (5, 3)
        self.rgb = 84, 92, 214
        self.hud = False


class Truck(GameObject):
    """
    The speeding trucks.
    """

    def __init__(self):
        super().__init__()
        self._xy = 0, 0
        self.wh = (16, 18)
        self.rgb = 198, 108, 58
        self.hud = False


class RoadCrack(GameObject):
    """
    Damaged road segments (cliffs??).
    """

    def __init__(self):
        super().__init__()
        self._xy = 0, 0
        self.rgb = 181, 83, 40
        self.hud = False
        self.wh = (14, 32)


class AcmeMine(GameObject):
    """
    The landmines planted along the road.
    """

    def __init__(self):
        super().__init__()
        self.rgb = 255, 255, 255  # 84,92,214
        self.hud = False
        self._xy = 0, 0
        self.wh = (4, 3)


class Turret(GameObject):
    """
    Wile E. Coyote's cannons along the road.
    """

    def __init__(self):
        super().__init__()
        self.rgb = 66, 72, 200
        self.hud = False
        self._xy = 0, 0
        self.wh = (12, 8)


class TurretBall(GameObject):
    """
    The projectiles shot from the cannons.
    """

    def __init__(self):
        super().__init__()
        self.rgb = 198, 108, 58
        self.hud = False
        self._xy = 0, 0
        self.wh = (4, 4)


class Stone(GameObject):
    """
    The rocks tumbling down on the road.
    """

    def __init__(self):
        super().__init__()
        self.rgb = 181, 83, 40
        self.hud = False
        self._xy = 0, 0
        self.wh = (8, 11)


class Cactus(GameObject):
    """
    Cactus in the background (HUD).
    """

    def __init__(self):
        super().__init__()
        self._xy = 0, 0
        self.wh = (8, 8)
        self.rgb = 187, 187, 53
        self.hud = True


class Sign(GameObject):
    """
    The occasional road signs and billboards (HUD).
    """

    def __init__(self):
        super().__init__()
        self._xy = 0, 0
        self.wh = (16, 15)
        self.rgb = 0, 0, 0
        self.hud = True


class Bird(GameObject):
    """
    The birds flying by.
    """

    def __init__(self):
        super().__init__()
        self.rgb = 252, 188, 116
        self._xy = 0, 0
        self.wh = (6, 8)
        self.hud = True


class PlayerScore(GameObject):
    """
    The player's score display (HUD).
    """

    def __init__(self):
        super().__init__()
        self.rgb = 0, 0, 0
        self._xy = 0, 0
        self.wh = (7, 5)
        self.hud = True


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
    objects = [Player(), Enemy(), Truck(), BirdSeeds(), BirdSeeds(), BirdSeeds(
    ), BirdSeeds(), RoadCrack(), AcmeMine(), TurretBall(), Turret(), None]
    if hud:
        objects.extend([Sign(), Bird(), Bird(), Cactus(), Cactus()])
    return objects


def _detect_objects_ram(objects, ram_state, hud=False):
    """
    For all 3 objects:
    (x, y, w, h, r, g, b)
    """
    player, enemy, truck = objects[:3]
    if ram_state[80] < 150:
        if player is None:
            player = Player()
            objects[0] = player
        if ram_state[22] == 1:
            player.xy = ram_state[80], ram_state[3]+102
        elif ram_state[22] == 3:
            player.xy = ram_state[80], ram_state[3]+85
        else:
            player.xy = ram_state[80], ram_state[3] + 95
        player.wh = (8, 24) if ram_state[41] == 6 else (8, 32)
    else:
        objects[0] = None

    if ram_state[81] > 143:  # Removing the enemy
        objects[1] = None
    else:
        if enemy is None:  # Setting back the enemy
            enemy = Enemy()
        if ram_state[22] == 1:
            enemy.xy = ram_state[81], ram_state[5] - 30
        else:
            enemy.xy = ram_state[81], ram_state[5] + 98
        objects[1] = enemy
    if ram_state[43] == 0:  # Removing the truck
        objects[2] = None
    elif truck is None:
        truck = Truck()
        objects[2] = truck
    if truck is not None:
        truck.xy = ram_state[42], 157 if (ram_state[43] == 1) else 127

    # BirdSeeds
    pos_init = ram_state[89]
    dist1 = [-30, -67, -49, 18, -59, -22, 18, -67]
    dist2 = [-30, 95, -47, 20, -56, -20, 20, 94]
    loc = ram_state[90]-1
    if ram_state[22] != 1:
        if ram_state[36] == 31 or ram_state[36] == 47:  # bottom seed or AcmeMine
            seed1, temp = whichobj(ram_state[36])
            seed1.xy = correction(pos_init+dist1[loc]+3*dist2[loc]+temp), 165
            objects[3] = seed1
        else:
            objects[3] = None
        if ram_state[37] == 31 or ram_state[37] == 47:  # second bottom seed or AcmeMine
            seed2, temp = whichobj(ram_state[37])
            seed2.xy = correction(pos_init+dist1[loc]+2*dist2[loc]+temp), 151
            objects[4] = seed2
        else:
            objects[4] = None

        if ram_state[38] == 31 or ram_state[38] == 47:  # second top seed or AcmeMine
            seed3, temp = whichobj(ram_state[38])
            seed3.xy = correction(pos_init+dist1[loc]+dist2[loc]+temp), 137
            objects[5] = seed3
        else:
            objects[5] = None

        if ram_state[39] == 31 or ram_state[39] == 47:  # top seed or AcmeMine
            seed4, temp = whichobj(ram_state[39])
            seed4.xy = correction(pos_init+dist1[loc]+temp), 124
            objects[6] = seed4
        else:
            objects[6] = None
    else:
        # On second level remove all the birdseeds
        objects[3] = None
        objects[4] = None
        objects[5] = None
        objects[6] = None

    # RoadCrack
    if ram_state[82] > 150 or ram_state[82] <= 8 or ram_state[22] != 1:
        objects[7] = None
    else:
        if ram_state[79] == 1:
            if ram_state[69] <= 18 and ram_state[69] >= 6:
                rc = RoadCrack()
                rc.xy = ram_state[82]-5, 125
                objects[7] = rc
            else:
                objects[7] = None
        elif ram_state[79] <= 10:
            if ram_state[69] <= 18 and ram_state[69] >= 6:
                rc = RoadCrack()
                rc.xy = ram_state[82]-5, 125
                objects[7] = rc
                rc2 = RoadCrack()
                rc2.xy = ram_state[82]-101, 125
                objects[10] = rc2
            else:
                objects[7] = None
                objects[10] = None
        elif ram_state[79] >= 11 and ram_state[79] < 20:
            if ram_state[69] <= 18 and ram_state[69] >= 6:
                rc = RoadCrack()
                rc.xy = ram_state[82]-5, 125
                objects[7] = rc
                rc2 = RoadCrack()
                rc2.xy = ram_state[82]-101, 125
                objects[10] = rc2
            else:
                objects[7] = None
                objects[10] = None
        elif ram_state[79] == 20:
            if ram_state[69] <= 18 and ram_state[69] >= 6:
                rc = RoadCrack()
                rc.xy = ram_state[82]-5, 125
                objects[7] = rc
                rc2 = RoadCrack()
                rc2.xy = ram_state[82]+59, 125
                objects[10] = rc2
            else:
                objects[7] = None
                objects[10] = None

        else:
            objects[7] = None
            objects[10] = None

    # AcmeMine
    if ram_state[89] > 150 or ram_state[89] <= 8 or ram_state[39] == 40 or ram_state[39] == 24:
        objects[8] = None
    else:
        am = BirdSeeds() if ram_state[39] == 31 else AcmeMine()
        temp = 6 if ram_state[39] == 31 else 4
        if ram_state[55] == 0:
            am.xy = ram_state[89]-temp, 147
            objects[8] = am
        elif ram_state[55] == 1:
            am.xy = ram_state[89]-temp, 131
            objects[8] = am
        else:
            objects[8] = None
    # TurretBall
    if ram_state[42] > 150 or ram_state[42] <= 8:
        objects[9] = None
    else:
        if objects[2] is None:
            tb = TurretBall()
            tb.xy = ram_state[42]-2, 128
            objects[9] = tb
        else:
            objects[9] = None

    # Turret
    if ram_state[55] > 150 or ram_state[55] <= 8 or ram_state[22] != 3:
        objects[10] = None
    else:
        t = Turret()
        t.xy = ram_state[55]-5, 128
        objects[10] = t

    if hud:
        # Signs
        if ram_state[82] > 145 or ram_state[82] <= 0 or ram_state[22] in [3, 5]:
            objects[12] = None
        else:
            if ram_state[69] == 0 or ram_state[69] == 1 or ram_state[69] == 2 or ram_state[69] == 16:
                twss = Sign()
                twss.xy = ram_state[82], 73
                objects[12] = twss
            else:
                objects[12] = None

        # birds
        if ram_state[68] == 32:
            objects[13] = None
            objects[14] = None
        elif ram_state[68] == 33:
            bird1 = Bird()
            bird1.xy = 55, 16
            objects[14] = None
            objects[13] = bird1
        elif ram_state[68] == 34:
            bird1 = Bird()
            bird1.xy = 63, 16
            bird2 = Bird()
            bird2.xy = 55, 16
            objects[14] = bird2
            objects[13] = bird1
        # cactus
        if ram_state[24] < 8 or ram_state[24] > 147:
            objects[14] = None
        else:
            u_cac = Cactus()
            u_cac.xy = ram_state[24], 46
            objects[15] = u_cac

        if ram_state[83] < 8 or ram_state[83] > 147:
            objects[16] = None
        else:
            l_cac = Cactus()
            l_cac.xy = ram_state[83], 55
            objects[16] = l_cac
        # Removing player score since they are not really needed and they create problems in some levels
        # ps1=PlayerScore()
        # ps2=PlayerScore()
        # ps3=PlayerScore()
        # if ram_state[13]==2:
        #     ps1.xy=80, 182
        #     ps1.wh=(1, 5)
        #     ps2.xy=83, 182
        #     ps2.wh=(3, 5)
        #     ps3.xy=87, 182
        #     ps3.wh=(3, 5)
        # elif ram_state[14]==1:
        #     ps1=None
        #     ps2=None
        #     ps3=None
        # else:
        #     ps1.xy=80, 182
        #     ps1.wh=(3, 5)
        #     ps2.xy=83, 182
        #     ps2.wh=(3, 5)
        #     ps3.xy=87, 182
        #     ps3.wh=(3, 5)
        # objects[14]=ps1; objects[15]=ps2; objects[16]=ps3

        # player score info
        # PlayerScore at (87, 182), (3, 5), PlayerScore at (83, 182), (3, 5), PlayerScore at (80, 182), (1, 5)


def correction(pos):
    pos -= 2
    return pos % 160


def whichobj(pos):
    if pos == 47:
        return AcmeMine(), 4
    else:
        return BirdSeeds(), 0


def _detect_objects_roadrunner_raw(info, ram_state):
    """
    returns unprocessed list with
    ball_x, ball_y, enemy_y, player_y
    """
    info["objects_list"] = ram_state[32:36]


# def _detect_objects_roadrunner_revised_old(info, ram_state, hud=False):
#     """
#     For all 3 objects:
#     (x, y, w, h, r, g, b)
#     """
#     objects = {}
#     objects["player"] = ram_state[32]+5, ram_state[34]+38, 14, 46, 214, 214, 214
#     objects["enemy"] = ram_state[33]+4, ram_state[35]+38, 14, 46, 0, 0, 0
#     if hud:
#         objects["enemy_score"] = 111, 5, 6, 7, 0, 0, 0
#         if ram_state[19] < 10:
#             objects["enemy_score2"] = 0, 0, 0, 0, 0, 0, 0
#         else:
#             objects["enemy_score2"] = 103, 5, 6, 7, 0, 0, 0
#         objects["player_score"] = 47, 5, 6, 7, 214, 214, 214
#         if ram_state[18] < 10:
#             objects["player_score2"] = 0, 0, 0, 0, 0, 0, 0
#         else:
#             objects["player_score2"] = 39, 5, 6, 7, 214, 214, 214
#         objects["logo"] = 62, 189, 32, 7, 20, 60, 0
#         objects["time1"] = 63, 17, 6, 7, 20, 60, 0
#         objects["time2"] = 73, 18, 2, 5, 20, 60, 0
#         objects["time3"] = 79, 17, 6, 7, 20, 60, 0
#         objects["time4"] = 87, 17, 6, 7, 20, 60, 0
#     info["objects"] = objects

    # if ram_state[36]==31: #bottom seed
    #     seed1=BirdSeeds()
    #     if ram_state[90]==1:
    #         seed1.xy=correction(pos_init-60),166
    #     else:
    #         pass
    #     objects[3]=seed1
    # else:
    #     objects[3]=None
    # if ram_state[37]==31: #second bottom seed
    #     seed2=BirdSeeds()
    #     if ram_state[90]==1:
    #         seed2.xy=correction(pos_init-40),152
    #     else:
    #         pass
    #     objects[4]=seed2
    # else:
    #     objects[4]=None

    # if ram_state[38]==31: #second top seed
    #     seed3=BirdSeeds()
    #     if ram_state[90]==1:
    #         seed3.xy=correction(pos_init-20),138
    #     else:
    #         pass
    #     objects[5]=seed3
    # else:
    #     objects[5]=None

    # if ram_state[39]==31: #top seed
    #     seed4=BirdSeeds()
    #     if ram_state[90]==1:
    #         seed4.xy=correction(pos_init),124
    #     else:
    #         pass
    #     objects[6]=seed4
    # else:
    #     objects[6]=None
