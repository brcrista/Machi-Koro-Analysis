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
# While not technically needed (we *could* just math out every round number for the cards we want),
# pass in the player state to make implementing a strategy easier.
Strategy = Callable[["PlayerState", int], Tuple[bool, Optional[Card]]]

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
    num_players: int

    def __init__(self, num_players: int):
        # This is what each player gets for the start of the game.
        self.hand = [cards.WheatField(), cards.Bakery()]
        self.coins = 3
        self.num_players = num_players

    def update_my_turn(self, strategy: Strategy, round_number: int) -> Optional[Card]:
        two_dice, card_to_buy = strategy(self, round_number)
        self.coins += expected_revenue_my_turn(self.hand, two_dice, self.num_players)
        if card_to_buy is not None:
            self.hand.append(card_to_buy)
            self.coins -= card_to_buy.cost
            if self.coins < 0:
                raise InvalidStrategyError(f"Buying a {card_to_buy.name} in round {round_number} is expected to result in a negative number of coins ({self.coins}).")
        return card_to_buy

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

    player_state = PlayerState(num_players)
    victory_cards, cards = _partition(player_state.hand, _is_victory_card)
    game_log = {
        "Round": [0],
        "Turn": [None],
        "Coins": [player_state.coins],
        "# Cards": [len(cards)],
        "# Victory Cards": [len(victory_cards)],
        "Bought Card": [None]
    }

    # Buying no cards except for the victory cards, in any order, is expected to win in well under 100 rounds.
    MAX_ROUNDS = 100
    for round_number in range(1, MAX_ROUNDS + 1):
        for turn_number in range(1, player_state.num_players + 1):
            # Assume the one player we're keeping track of goes first in each round.
            if turn_number == 1:
                bought_card = player_state.update_my_turn(strategy, round_number)
            else:
                player_state.update_other_turn(round_number)
                bought_card = None

            victory_cards, cards = _partition(player_state.hand, _is_victory_card)
            game_log["Round"].append(round_number)
            game_log["Turn"].append(turn_number)
            game_log["Coins"].append(player_state.coins)
            game_log["# Cards"].append(len(cards))
            game_log["# Victory Cards"].append(len(victory_cards))
            game_log["Bought Card"].append(bought_card)
            if player_state.is_winner():
                return pd.DataFrame(game_log)
    raise InvalidStrategyError("The strategy does not buy all four victory cards within 100 rounds.")

def _next_card(build_order: List[Card], player_state):
    for card in build_order:
        if not card in player_state.hand:
            return card
    else:
        return None

def _from_build_order(build_order: List[Card], roll_two) -> Strategy:
    """
    Implement a strategy by defining a list of cards to buy in order
    and a predicate for when to roll two dice.
    """
    next_card = None
    def strategy(player_state, round_number) -> Tuple[bool, Card]:
        nonlocal next_card
        if next_card is None:
            next_card = build_order.pop(0)
        two_dice = roll_two(player_state)
        if player_state.coins >= next_card.cost:
            result = (two_dice, next_card)
            next_card = None
            return result
        else:
            return (two_dice, None)
    return strategy

# Buy a shopping mall first since it adds a bonus to our bakery.
# We expect 1/6 + 1/12 = 1/4 coins per roll = 1 coin per turn in a 4-player game.
# Buying the shopping mall will double our bakery's expected value,
# giving us 1/6 + 1/6 = 1/3 coins per roll = 4/3 coins per turn.
# With this optimization, we expect to win one round faster (40 vs. 41).
# The radio tower will also bump up our expected coins, but we aren't accounting for that yet in our model.
buy_nothing = _from_build_order([
        cards.ShoppingMall(),
        cards.RadioTower(),
        cards.TrainStation(),
        cards.AmusementPark()
    ],
    roll_two=lambda player_state: False)

buy_everything = _from_build_order([
        cards.WheatField(),
        cards.Ranch(),
        cards.Ranch(),
        cards.Bakery(),
        cards.Cafe(),
        cards.ConvenienceStore(),
        cards.Forest(),
        cards.Forest(),
        cards.Stadium(),
        # cards.TvStation(),
        # cards.BusinessCenter(),
        cards.CheeseFactory(),
        cards.FurnitureFactory(),
        cards.AppleOrchard(),
        cards.TrainStation(),
        cards.Mine(),
        cards.FruitVegetableMarket(),
        cards.ShoppingMall(),
        cards.Mine(),
        cards.AmusementPark(),
        cards.AppleOrchard(),
        cards.Mine(),
        cards.RadioTower()
    ],
    roll_two=lambda player_state: cards.TrainStation() in player_state.hand)

big_convenience_store = _from_build_order([
        cards.WheatField(),
        cards.Ranch(),
        cards.Ranch(),
        cards.ConvenienceStore(),
        cards.ConvenienceStore(),
        cards.Ranch(),
        cards.ConvenienceStore(),
        cards.Forest(),
        cards.Bakery(),
        cards.ShoppingMall(),
        cards.ConvenienceStore(),
        cards.RadioTower(),
        cards.TrainStation(),
        cards.AmusementPark(),
    ],
    roll_two=lambda player_state: False)

big_ranch = _from_build_order([
        cards.Ranch(),
        cards.Cafe(),
        cards.Ranch(),
        cards.Cafe(),
        cards.Ranch(),
        cards.Cafe(),
        cards.WheatField(),
        cards.Forest(),
        cards.Stadium(),
        cards.ShoppingMall(),
        cards.RadioTower(),
        cards.TrainStation(),
        cards.AmusementPark(),
    ],
    roll_two=lambda player_state: False)