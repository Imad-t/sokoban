from typing import NamedTuple
from enum import Enum

class Position2d(NamedTuple('Position2d', [('x', int), ('y', int)])):
    pass

class EntityType(Enum('Type', ["void", "wall", "box", "target", "player"])):
    pass
