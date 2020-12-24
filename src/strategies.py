import pandas as pd

from analysis import expected_value_my_turn, expected_value_other_turn
from dataclasses import dataclass
from machi_koro import cards
from machi_koro.cards import Card, Color
from typing import Callable, List, Tuple

def expected_revenue_my_turn(hand: List[Card], two_dice: bool, num_players: int) -> float:
    """The average revenue a hand will yield on your turn."""
    return sum(expected_value_my_turn(c, hand, two_dice, num_players) for c in hand)

def expected_revenue_other_turn(hand: List[Card], two_dice: bool, num_players: int) -> float:
    """The average revenue a hand will yield on another player's turn."""
    return sum(expected_value_other_turn(c, hand, two_dice, num_players) for c in hand)

def _is_victory_card(card):
    return card.color == Color.GOLD

VICTORY_CARDS = [c for c in cards.distinct_cards if _is_victory_card(c)]

# A strategy maps a round number to whether to roll two dice and a card to buy.
Strategy = Callable[[int], Tuple[bool, Card]]

@dataclass
class PlayerState:
    hand: List[Card]
    coins: float
    strategy: Strategy
    num_players: int

    def __init__(self, strategy: Strategy, num_players: int):
        # This is what each player gets for the start of the game.
        self.hand = [cards.WheatField(), cards.Bakery()]
        self.coins = 3
        self.strategy = strategy
        self.num_players = num_players

    def update_my_turn(self, round_number: int) -> None:
        two_dice, card_to_buy = self.strategy(round_number)
        self.coins += expected_revenue_my_turn(self.hand, two_dice, self.num_players)
        self.hand.append(card_to_buy)
        self.coins -= card_to_buy.cost

    def update_other_turn(self, round_number: int) -> None:
        # Assume that other players always roll one die.
        two_dice = False
        self.coins += expected_revenue_other_turn(self.hand, two_dice, self.num_players)

    def is_winner(self) -> bool:
        return all(c in self.hand for c in VICTORY_CARDS)

def _count(start: int):
    while True:
        yield start
        start += 1

def _partition(xs, predicate):
    return [x for x in xs if predicate(x)], [x for x in xs if not predicate(x)]

def simulate(strategy: Strategy, num_players: int) -> pd.DataFrame:
    if not (2 <= num_players <= 4):
        raise ValueError()

    player_state = PlayerState(strategy, num_players)
    game_log = {
        "Round": [],
        "Turn": [],
        "Coins": [],
        "# Cards": [],
        "# Victory Cards": []
    }

    victory_cards, cards = _partition(player_state.hand, _is_victory_card)
    game_log["Round"] = [0]
    game_log["Turn"] = [None]
    game_log["Coins"] = [player_state.coins]
    game_log["# Cards"] = [len(cards)]
    game_log["# Victory Cards"] = [len(victory_cards)]

    for round_number in _count(1):
        for turn_number in range(1, player_state.num_players + 1):
            # Assume the one player we're keeping track of goes first in each round.
            if turn_number == 1:
                player_state.update_my_turn(round_number)
            else:
                player_state.update_other_turn(round_number)

            victory_cards, cards = _partition(player_state.hand, _is_victory_card)
            game_log["Round"].append(round_number)
            game_log["Turn"].append(turn_number)
            game_log["Coins"].append(player_state.coins)
            game_log["# Cards"].append(len(cards))
            game_log["# Victory Cards"].append(len(victory_cards))
            if player_state.is_winner():
                return pd.DataFrame(game_log)
    assert False

def to_strategy(xs: List[Tuple[Card, bool]]):
    def _strategy(i: int):
        # Turns start from 1, so re-index the 0-based list.
        xs_from_1 = [None] + xs
        return xs_from_1[i]
    return _strategy