"""
RAM Processing submodule of OCAtari
"""


from .extract_vision_info import detect_objects_vision
from .game_objects import GameObject

__all__ = [
    "detect_objects_vision",
]
