from machi_koro.cards import Card, Color
from typing import Iterable, List

def _ways_12(x):
    if x ==  2: return 1
    if x ==  3: return 2
    if x ==  4: return 3
    if x ==  5: return 4
    if x ==  6: return 5
    if x ==  7: return 6
    if x ==  8: return 5
    if x ==  9: return 4
    if x == 10: return 3
    if x == 11: return 2
    if x == 12: return 1
    return 0

def _roll_probability(numbers: Iterable[int], two_dice: bool) -> float:
    if two_dice:
        return sum(_ways_12(x) for x in card.activates_on) / 36
    else:
        return len(card.activates_on) / 6

def expected_value(card: Card, hand: List[Card], two_dice: bool, num_players: int) -> float:
    """The average revenue a card will yield on a turn when it can be activated."""
    probability = _roll_probability(card.activates_on, two_dice)
    return probability * card.revenue(hand, num_players)

def expected_revenue_my_turn(hand: List[Card], two_dice: bool, num_players: int):
    """The average revenue a hand will yield on your turn."""
    active_cards = [c for c in hand if c.color in [Color.BLUE, Color.GREEN, Color.PURPLE]]
    return sum(expected_value(c, hand, two_dice, num_players) for c in active_cards)

def expected_revenue_other_turn(hand: List[Card], two_dice: bool, num_players: int):
    """The average revenue a hand will yield on another player's turn."""
    active_cards = [c for c in hand if c.color in [Color.RED, Color.BLUE]]
    return sum(expected_value(c, hand, two_dice, num_players) for c in active_cards)
