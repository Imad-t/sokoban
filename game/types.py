from typing import NamedTuple
from enum import Enum

class Position2d(NamedTuple('Position2d', [('x', int), ('y', int)])):
    pass

class EntityType(Enum):
    VOID = 1
    WALL = 2
    BOX = 3
    TARGET = 4
    PLAYER = 5
    pass

class ActionType(Enum):
    UP = 1
    DOWN = 2
    LEFT = 3
    RIGHT = 4
    pass
