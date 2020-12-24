import math

import pandas as pd

from analysis import expected_value_my_turn, expected_value_other_turn
from dataclasses import dataclass
from machi_koro import cards
from machi_koro.cards import Card, Color
from typing import Callable, List, Optional, Tuple

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
Strategy = Callable[[int], Tuple[bool, Optional[Card]]]

class InvalidStrategyError(Exception):
    """
    An exception raised when a `Strategy` tries to buy something it doesn't have the money for
    or doesn't try to buy all victory cards.
    """
    def __init__(self, message):
        self.message = message

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
        if card_to_buy is not None:
            self.hand.append(card_to_buy)
            self.coins -= card_to_buy.cost
            if self.coins < 0:
                raise InvalidStrategyError(f"Buying a {card_to_buy.name} in round {round_number} is expected to result in a negative number of coins ({self.coins}).")

    def update_other_turn(self, round_number: int) -> None:
        # Assume that other players always roll one die.
        two_dice = False
        self.coins += expected_revenue_other_turn(self.hand, two_dice, self.num_players)

    def is_winner(self) -> bool:
        return all(c in self.hand for c in VICTORY_CARDS)

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

    # Buying no cards except for the victory cards, in any order, is expected to win in well under 100 rounds.
    MAX_ROUNDS = 100
    for round_number in range(1, MAX_ROUNDS + 1):
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
    raise InvalidStrategyError("The strategy does not buy all four victory cards within 100 rounds.")

def to_strategy(xs: List[Tuple[Card, bool]]):
    def _strategy(i: int):
        # Turns start from 1, so re-index the 0-based list.
        xs_from_1 = [None] + xs
        return xs_from_1[i]
    return _strategy

def buy_nothing(round_number):
    # Buy a shopping mall first since it adds a bonus to our bakery.
    # We expect 1/6 + 1/12 = 1/4 coins per roll = 1 coin per turn in a 4-player game.
    # Buying the shopping mall will double our bakery's expected value,
    # giving us 1/6 + 1/6 = 1/3 coins per roll = 4/3 coins per turn.
    # The radio tower will also bump up our expected coins, but we aren't accounting for that yet in our model.
    FIRST_ROUND_NUMBER = 1
    SHOPPING_MALL_ROUND_NUMBER:  int = FIRST_ROUND_NUMBER + cards.ShoppingMall().cost - 3
    RADIO_TOWER_ROUND_NUMBER:    int = math.ceil(SHOPPING_MALL_ROUND_NUMBER + cards.RadioTower().cost * 3 / 4)
    TRAIN_STATION_ROUND_NUMBER:  int = math.ceil(RADIO_TOWER_ROUND_NUMBER + cards.TrainStation().cost * 3 / 4)
    AMUSEMENT_PARK_ROUND_NUMBER: int = math.ceil(TRAIN_STATION_ROUND_NUMBER + cards.AmusementPark().cost * 3 / 4)

    if round_number == SHOPPING_MALL_ROUND_NUMBER:
        return (False, cards.ShoppingMall())
    if round_number == RADIO_TOWER_ROUND_NUMBER:
        return (False, cards.RadioTower())
    if round_number == TRAIN_STATION_ROUND_NUMBER:
        return (False, cards.TrainStation())
    if round_number == AMUSEMENT_PARK_ROUND_NUMBER:
        return (False, cards.AmusementPark())
    else:
        return (False, None)