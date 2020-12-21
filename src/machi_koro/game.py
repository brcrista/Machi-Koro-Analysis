from typing import List, NamedTuple

from .cards import Card

class PlayerState(NamedTuple):
    hand: List[Card]
    money: int
