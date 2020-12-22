from abc import ABCMeta, abstractmethod
from dataclasses import dataclass
from enum import Enum
from typing import List, Set

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

class Card(metaclass=ABCMeta):
    name: str
    color: Color
    symbol: Symbol
    cost: int
    activates_on: Set[int]

    @abstractmethod
    def revenue(self, hand: List['Card'], num_players: int) -> int:
        pass

class WheatField(Card):
    def __init__(self):
        self.name = "Wheat Field"
        self.color = Color.BLUE
        self.symbol = Symbol.WHEAT
        self.cost = 1
        self.activates_on = set([1])

    def revenue(self, hand: List[Card], num_players: int) -> int:
        return 1

class Ranch(Card):
    def __init__(self):
        self.name = "Ranch"
        self.color = Color.BLUE
        self.symbol = Symbol.COW
        self.cost = 1
        self.activates_on = set([2])

    def revenue(self, hand: List[Card], num_players: int) -> int:
        return 1

class Bakery(Card):
    def __init__(self):
        self.name = "Bakery"
        self.color = Color.GREEN
        self.symbol = Symbol.BOX
        self.cost = 1
        self.activates_on = set([2, 3])

    def revenue(self, hand: List[Card], num_players: int) -> int:
        return 1 + ShoppingMall.bonus(hand)

class Cafe(Card):
    def __init__(self):
        self.name = "Cafe"
        self.color = Color.RED
        self.symbol = Symbol.CUP
        self.cost = 2
        self.activates_on = set([2, 3])

    def revenue(self, hand: List[Card], num_players: int) -> int:
        return 1 + ShoppingMall.bonus(hand)

class ConvenienceStore(Card):
    def __init__(self):
        self.name = "Convenience Store"
        self.color = Color.GREEN
        self.symbol = Symbol.BOX
        self.cost = 2
        self.activates_on = set([4])

    def revenue(self, hand: List[Card], num_players: int) -> int:
        return 3 + ShoppingMall.bonus(hand)

class Forest(Card):
    def __init__(self):
        self.name = "Forest"
        self.color = Color.BLUE
        self.symbol = Symbol.GEAR
        self.cost = 3
        self.activates_on = set([5])

    def revenue(self, hand: List[Card], num_players: int) -> int:
        return 1

class Stadium(Card):
    def __init__(self):
        self.name = "Stadium"
        self.color = Color.PURPLE
        self.symbol = Symbol.TOWER
        self.cost = 6
        self.activates_on = set([6])

    def revenue(self, hand: List[Card], num_players: int) -> int:
        return 2 * (num_players - 1)

class TvStation(Card):
    def __init__(self):
        self.name = "TV Station"
        self.color = Color.PURPLE
        self.symbol = Symbol.TOWER
        self.cost = 7
        self.activates_on = set([6])

    def revenue(self, hand: List[Card], num_players: int) -> int:
        return 5

class BusinessCenter(Card):
    def __init__(self):
        self.name = "Business Center"
        self.color = Color.PURPLE
        self.symbol = Symbol.TOWER
        self.cost = 8
        self.activates_on = set([6])

    def revenue(self, hand: List[Card], num_players: int) -> int:
        return 0

class CheeseFactory(Card):
    def __init__(self):
        self.name = "Cheese Factory"
        self.color = Color.GREEN
        self.symbol = Symbol.FACTORY
        self.cost = 5
        self.activates_on = set([7])

    def revenue(self, hand: List[Card], num_players: int) -> int:
        cow_cards = [x for x in hand if x.symbol == Symbol.COW]
        return 3 * len(cow_cards)

class FurnitureFactory(Card):
    def __init__(self):
        self.name = "Furniture Factory"
        self.color = Color.GREEN
        self.symbol = Symbol.FACTORY
        self.cost = 3
        self.activates_on = set([8])

    def revenue(self, hand: List[Card], num_players: int) -> int:
        gear_cards = [x for x in hand if x.symbol == Symbol.GEAR]
        return 3 * len(gear_cards)

class Mine(Card):
    def __init__(self):
        self.name = "Mine"
        self.color = Color.BLUE
        self.symbol = Symbol.GEAR
        self.cost = 6
        self.activates_on = set([9])

    def revenue(self, hand: List[Card], num_players: int) -> int:
        return 5

class FamilyRestaurant(Card):
    def __init__(self):
        self.name = "Family Restaurant"
        self.color = Color.RED
        self.symbol = Symbol.CUP
        self.cost = 3
        self.activates_on = set([9, 10])

    def revenue(self, hand: List[Card], num_players: int) -> int:
        return 2 + ShoppingMall.bonus(hand)

class AppleOrchard(Card):
    def __init__(self):
        self.name = "Apple Orchard"
        self.color = Color.BLUE
        self.symbol = Symbol.WHEAT
        self.cost = 3
        self.activates_on = set([10])

    def revenue(self, hand: List[Card], num_players: int) -> int:
        return 3

class FruitVegetableMarket(Card):
    def __init__(self):
        self.name = "Fruit and Vegetable Market"
        self.color = Color.GREEN
        self.symbol = Symbol.FRUIT
        self.cost = 2
        self.activates_on = set([11, 12])

    def revenue(self, hand: List[Card], num_players: int) -> int:
        wheat_cards = [x for x in hand if x.symbol == Symbol.WHEAT]
        return 2 * len(wheat_cards)

class TrainStation(Card):
    def __init__(self):
        self.name = "Train Station"
        self.color = Color.GOLD
        self.symbol = Symbol.TOWER
        self.cost = 4
        self.activates_on = set()

    def revenue(self, hand: List[Card], num_players: int) -> int:
        return 0

class ShoppingMall(Card):
    def __init__(self):
        self.name = "Shopping Mall"
        self.color = Color.GOLD
        self.symbol = Symbol.TOWER
        self.cost = 10
        self.activates_on = set()

    def revenue(self, hand: List[Card], num_players: int) -> int:
        return 0

    @staticmethod
    def bonus(hand: List[Card]) -> int:
        if any(isinstance(c, ShoppingMall) for c in hand):
            return 1
        else:
            return 0

class AmusementPark(Card):
    def __init__(self):
        self.name = "Amusement Park"
        self.color = Color.GOLD
        self.symbol = Symbol.TOWER
        self.cost = 16
        self.activates_on = set()

    def revenue(self, hand: List[Card], num_players: int) -> int:
        return 0

class RadioTower(Card):
    def __init__(self):
        self.name = "Radio Tower"
        self.color = Color.GOLD
        self.symbol = Symbol.TOWER
        self.cost = 22
        self.activates_on = set()

    def revenue(self, hand: List[Card], num_players: int) -> int:
        return 0
