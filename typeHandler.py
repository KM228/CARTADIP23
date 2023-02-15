from enum import Enum, auto


class TileTypes(Enum):

    EMPTY = auto()
    ENTRY = auto()
    EXIT = auto()
    HAZARD = auto()
    CHEST = auto()
    GEM = auto()


tileType = {}


tileType[TileTypes.EMPTY] = "Empty"
tileType[TileTypes.ENTRY] = "ENTRY"
tileType[TileTypes.EXIT] = "EXIT"
tileType[TileTypes.HAZARD] = "Hazard"
tileType[TileTypes.CHEST] = "Chest"
tileType[TileTypes.GEM] = "Gem"

print (tileType[TileTypes.EMPTY])
