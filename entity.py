from .game.types import Position2d, EntityType

class Entity:
    def __init__(self,
                 pos: Position2d = (0, 0),
                 type: EntityType = 'void'
                ):
        pass