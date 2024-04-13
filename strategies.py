import python_blackjack_simulator as bj

def hit_until_17(player_hand, dealer_hand):
  """
  Hit until score > 17 or bust
  :param player_hand: list of cards
  :param dealer_hand: single card
  :return: (action, empty)
  """
  action = "h"
  if bj.total(player_hand) >= 17:
    action = "s"
  return action, ()