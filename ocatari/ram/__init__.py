"""
RAM Extraction submodule of OCAtari
"""


from .extract_ram_info_short import detect_objects_raw, detect_objects_revised
from .game_objects import GameObject

__all__ = [
    "detect_objects_raw", "detect_objects_revised"
    ]
