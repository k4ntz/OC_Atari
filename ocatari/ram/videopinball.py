from .game_objects import GameObject

"""
RAM extraction for the game Fishing Derby.
"""

MAX_NB_OBJECTS = {"Player1FishingString": 1, "Player2FishingString": 1, "Fish": 6, "Shark": 1}
MAX_NB_OBJECTS_HUD = {"Player1FishingString": 1, "Player2FishingString": 1, "Fish": 6, "Shark": 1, "ScoreP1": 1,
                      "ScoreP2": 1}


class Fish(GameObject):
    """
    The fish.

    :ivar hooked: Wether the fish is currently hooked
    :type: bool
    """

    def __init__(self):
        super().__init__()
        self.rgb = 232, 232, 74
        self.xy = 0, 0
        self.wh = 8, 10
        self.hooked: bool = False

def _get_max_objects(hud=False):
    return


def _init_objects_videopinball_ram(hud=False):
    if hud:
        objects = []
    else:
        objects = []
    return objects


def _detect_objects_videopinball_revised(objects, ram_state, hud=False):
    return


def _detect_objects_videopinball_raw(info, ram_state):
    return
