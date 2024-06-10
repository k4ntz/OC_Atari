"""
RAM Processing submodule of OCAtari
"""

from os.path import dirname, basename, isfile, join
import glob
modules = glob.glob(join(dirname(__file__), "*.py"))
modules = [mod for mod in modules if not "_old" in mod]

__all__ = [basename(f)[:-3] for f in modules if isfile(f) and not f.endswith('__init__.py')]

from .game_objects import GameObject  # To avoid circular imports
from . import *
