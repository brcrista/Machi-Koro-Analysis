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
        return sum(_ways_12(x) for x in numbers) / 36
    else:
        return sum([1 for n in numbers if 1 <= n <= 6]) / 6

def expected_value(card: Card, hand: List[Card], two_dice: bool, num_players: int) -> float:
    """The average revenue a card will yield on a turn when it can be activated."""
    probability = _roll_probability(card.activates_on, two_dice)
    return probability * card.revenue(hand, num_players)

def expected_value_my_turn(card: Card, hand: List[Card], two_dice: bool, num_players: int) -> float:
    """The average revenue a card will yield on your turn."""
    if card.color in [Color.BLUE, Color.GREEN, Color.PURPLE]:
        return expected_value(card, hand, two_dice, num_players)
    else:
        return 0

def expected_value_other_turn(card: Card, hand: List[Card], two_dice: bool, num_players: int) -> float:
    """The average revenue a card will yield on another player's turn."""
    if card.color in [Color.RED, Color.BLUE]:
        return expected_value(card, hand, two_dice, num_players)
    else:
        return 0

def gross_expected_value(card: Card, hand: List[Card], two_dice: bool, num_players: int) -> float:
    """The average revenue a card will yield, taking into account whether it is active or not."""
    my_turn = expected_value_my_turn(card, hand, two_dice, num_players)
    other_turn = expected_value_other_turn(card, hand, two_dice, num_players)
    return (my_turn + (num_players - 1) * other_turn) / num_players

def expected_revenue_my_turn(hand: List[Card], two_dice: bool, num_players: int):
    """The average revenue a hand will yield on your turn."""
    return sum(expected_value_my_turn(c, hand, two_dice, num_players) for c in hand)

def expected_revenue_other_turn(hand: List[Card], two_dice: bool, num_players: int):
    """The average revenue a hand will yield on another player's turn."""
    return sum(expected_value_other_turn(c, hand, two_dice, num_players) for c in hand)
