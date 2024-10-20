from entity import Entity
from game.types import EntityType, Position2d

pos = Position2d(15, 12)
mytype = EntityType.BOX
ent = Entity(pos, mytype)
print(type(mytype))