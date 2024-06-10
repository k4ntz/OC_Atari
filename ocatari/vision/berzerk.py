from .utils import find_objects
from .game_objects import GameObject

objects_colors = {"player": [240, 170, 103], "walls": [84, 92, 214], "background": [0, 0, 0], "enemy": [210, 210, 64],
                  "logo": [232, 232, 74], "player_missile": [240, 170, 103], "score": [232, 232, 74],
                  "room_cleared": [232, 232, 74]}


enemy_colors = {"yellow": [210, 210, 64], "orange": [198, 108, 58], "gray": [214, 214, 214], "green": [111, 210, 111],
                "rose": [240, 128, 128], "blue": [84, 160, 197], "lightyellow": [232, 204, 99], "pink": [198, 89, 179]}


class Player(GameObject):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.rgb = 240, 170, 103


class PlayerMissile(GameObject):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.rgb = 240, 170, 103


class Enemy(GameObject):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.rgb = 210, 210, 64


class EnemyMissile(GameObject):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.rgb = 210, 210, 64


class Logo(GameObject):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.rgb = 232, 232, 74


class PlayerScore(GameObject):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.rgb = 232, 232, 74


class RoomCleared(GameObject):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.rgb = 232, 232, 74


def _detect_objects(objects, obs, hud=False):
    objects.clear()
    player = find_objects(obs, objects_colors["player"], min_distance=0.1)
    for p in player:
        if p[2] >= 4 and p[3] > 4:
            objects.append(Player(*p))
        else:
            objects.append(PlayerMissile(*p))

    for enemyColor in enemy_colors.values():
        enemy = find_objects(obs, enemyColor, min_distance=1)
        for e in enemy:
            if e[2] > 4 and e[3] > 4:
                enemy_inst = Enemy(*e)
                enemy_inst.rgb = enemyColor
                objects.append(enemy_inst)
            else:
                missile_inst = EnemyMissile(*e)
                missile_inst.rgb = enemyColor
                objects.append(missile_inst)

    if hud:
        logo = find_objects(obs, objects_colors["logo"], min_distance=1, closing_dist=3)
        for log in logo:
            if (log[0] == 86 and log[2] == 17) or (log[0] == 63 and log[2] == 20):
                objects.append(Logo(*log))
            elif log[0] == 56 and log[1] == 183 and log[2] == 14 and log[3] == 7:
                objects.append(RoomCleared(*log))
            else:
                objects.append(PlayerScore(*log))
