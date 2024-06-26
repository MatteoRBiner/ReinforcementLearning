import python_blackjack_simulator as bj
import numpy.random as rd

def random_action(player_hands, player_hand, dealer_hand):
    if rd.random() < 0.5:
        return "h"
    else:
        return "s"

def naive_action(player_hands, player_hand, dealer_hand):
  """
  Hit until bust.
  :param player_hand: list of cards
  :param dealer_hand: single card
  :return: action
  """
  return "h"

def hit_until_17(player_hands, player_hand, dealer_hand):
  """
  Hit until score > 17 or bust
  :param player_hand: list of cards
  :param dealer_hand: single card
  :return: action
  """
  action = "h"
  if bj.total(player_hand) >= 17:
    action = "s"
  return action

def expected_value_strategy(player_hands, player_hand, dealer_hand):
  """
  Hit if (score + (expected value of next cared)) <= 21
  :param player_hand: list of cards
  :param dealer_hand: single card
  :return: action
  """
  cards = 0
  value = 0
  for hand in player_hands:
     cards += len(hand) 
     value += bj.total(hand)
  number_of_remaining_cards = (52*bj.number_of_decks) - cards - 1
  total_A1 = (340*bj.number_of_decks)
  ace = False
  for card in player_hand:
    if card == "A":
        ace = True
  if not(ace):
    if not(dealer_hand == "A"):
        expected_value_1 = (total_A1 - value - bj.total(str(dealer_hand))) / number_of_remaining_cards
    else:
        expected_value_1 = (total_A1 - value - 1) / number_of_remaining_cards
    if bj.total(player_hand) + expected_value_1 <= 21:
        return "h"
    else:
        return "s"
  else:
    _ , used_aces = bj.total(player_hand, True)
    if used_aces == 1:
        if not(dealer_hand == "A"):
            expected_value_1 = (total_A1 + 10 - value - bj.total(str(dealer_hand))) / number_of_remaining_cards
        else:
            expected_value_1 = (total_A1 + 10 - value - 1) / number_of_remaining_cards
        # Compare cases like: (A + 9 = 20 -> stand) and (A + 5 = 16 -> hit)
        if bj.total(player_hand) + expected_value_1 <= 21 or (bj.total(player_hand) + expected_value_1 - 10 <= 21 and bj.total(player_hand) + expected_value_1 - 10 > bj.total(player_hand)) or (bj.total(player_hand) + expected_value_1 - 10 <= 21 and bj.total(player_hand) + 2*expected_value_1 - 10 > bj.total(player_hand) and bj.total(player_hand) + 2*expected_value_1 - 10 <= 21):
            return "h"
        else:
            return "s"
    else:
        if not(dealer_hand == "A"):
            expected_value_1 = (total_A1 - value - bj.total(str(dealer_hand))) / number_of_remaining_cards
        else:
            expected_value_1 = (total_A1 - value - 1) / number_of_remaining_cards
        if bj.total(player_hand) + expected_value_1 <= 21:
            return "h"
        else:
            return "s"
