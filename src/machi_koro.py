"""
Defines types and functions for modeling Machi Koro.
"""

from enum import Enum
from typing import List, NamedTuple

class Color(Enum):
    RED = 0
    GREEN = 1
    BLUE = 2
    PURPLE = 3
    GOLD = 4

class Symbol(Enum):
    WHEAT = 0
    COW = 1
    BOX = 2
    CUP = 3
    GEAR = 4
    TOWER = 5
    FACTORY = 6
    FRUIT = 7

class Card(NamedTuple):
    name: str
    color: Color
    symbol: Symbol
    cost: int

class PlayerState(NamedTuple):
    hand: List[Card]
    money: int

deck = [
    Card("Wheat Field", Color.BLUE, Symbol.WHEAT, 1),
    Card("Ranch", Color.BLUE, Symbol.COW, 1),
    Card("Bakery", Color.GREEN, Symbol.BOX, 1),
    Card("Cafe", Color.RED, Symbol.CUP, 2),
    Card("Convenience Store", Color.GREEN, Symbol.BOX, 2),
    Card("Forest", Color.BLUE, Symbol.GEAR, 3),
    Card("Stadium", Color.PURPLE, Symbol.TOWER, 6),
    Card("TV Station", Color.PURPLE, Symbol.TOWER, 7),
    Card("Business Center", Color.PURPLE, Symbol.TOWER, 8),
    Card("Cheese Factory", Color.GREEN, Symbol.FACTORY, 5),
    Card("Furniture Factory", Color.GREEN, Symbol.FACTORY, 3),
    Card("Mine", Color.BLUE, Symbol.GEAR, 6),
    Card("Family Restaurant", Color.RED, Symbol.CUP, 3),
    Card("Apple Orchard", Color.BLUE, Symbol.WHEAT, 3),
    Card("Fruit and Vegetable Market", Color.GREEN, Symbol.FRUIT, 2),
    Card("Train Station", Color.GOLD, Symbol.TOWER, 4),
    Card("Shopping Mall", Color.GOLD, Symbol.TOWER, 10),
    Card("Amusement Park", Color.GOLD, Symbol.TOWER, 16),
    Card("Radio Tower", Color.GOLD, Symbol.TOWER, 22)
]