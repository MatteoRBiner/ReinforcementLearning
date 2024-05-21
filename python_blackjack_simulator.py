""" Blackjack simulator, works for RL
  * Copied and modified from:
    https://gist.github.com/mjhea0/5680216
  * See function game(get_player_action) for instructions.
  * Requires Python 3.7
  * Handles 10M simulations in < 30 mins at Macbook Pro
  * Interactive play: python blackjack_simu.py
  * Might not implement blackjack rules perfectly
"""
import random
import logging
#logging.basicConfig(level=logging.INFO)


number_of_decks = 6
deck = [2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14]*(4 * number_of_decks)


def deal(deck):
  hand = []
  for i in range(2):
    random.shuffle(deck)
    card = deck.pop()
    if card == 11:card = "J"
    if card == 12:card = "Q"
    if card == 13:card = "K"
    if card == 14:card = "A"
    hand.append(card)
  return hand


def total(hand, return_usable_ace=False):
  total = 0
  aces = 0
  used_aces = 0
  for card in hand:
    if card == "J" or card == "Q" or card == "K":
      total += 10
    elif card == "A":
      total += 1
      aces += 1
    elif card != '[' and card != ',' and card != '\'' and card != ' ' and card != ']':
      total += int(card)
  if total < 11 and aces > 0:
    total += 10
    used_aces += 1
  if return_usable_ace:
    return (total, used_aces)
  else:
    return total


def hit(hand):
  card = deck.pop()
  if card == 11:card = "J"
  if card == 12:card = "Q"
  if card == 13:card = "K"
  if card == 14:card = "A"
  hand.append(card)
  return hand


def print_results(dealer_hand, player_hand):
  logging.info("The dealer has a " + str(dealer_hand) + " for a total of " + str(total(dealer_hand)))
  logging.info("You have a " + str(player_hand) + " for a total of " + str(total(player_hand)))


def score(dealer_hand, player_hand):
  print_results(dealer_hand, player_hand)
  if total(player_hand) == 21:
    logging.info("Congratulations! You got a Blackjack!\n")
    return 1.0
  elif total(dealer_hand) == 21:
    logging.info("Sorry, you lose. The dealer got a blackjack.\n")
    return -1.0
  elif total(player_hand) > 21:
    logging.info("Sorry. You busted. You lose.\n")
    return -1.0
  elif total(dealer_hand) > 21:
    logging.info("Dealer busts. You win!\n")
    return 1.0
  elif total(player_hand) < total(dealer_hand):
    logging.info("Sorry. Your score isn't higher than the dealer. You lose.\n")
    return -1.0
  elif total(player_hand) > total(dealer_hand):
    logging.info("Congratulations. Your score is higher than the dealer. You win\n" )
    return 1.0
  else:
    logging.info("A draw")
    return 0.0

def game(get_player_action):
  """ play a game of blackjack
  :param get_player_action: function(player_hand, dealer card) -> (action, data)
    - return value action is either h = hit or s = stand
    - return value data is arbitrary: for example state + action
  :returns: (
    reward from set {-1.0, 0.0, 1.0},
    list of data returned by function get_player_action,
    (final player hand, final dealer hand)
  )
  """
  # store list of data that
  player_data_lst = []
  #logging.info("WELCOME TO BLACKJACK!\n")
  global deck
  deck = [2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14]*(4*number_of_decks)
  dealer_hand = deal(deck)
  player_hand = deal(deck)
  choice = 0
  reward = -2.0
  while choice != "q":
    #logging.info("The dealer is showing a " + str(dealer_hand[0]))
    #logging.info("You have a " + str(player_hand) + " for a total of " + str(total(player_hand)))
    if total(player_hand) >= 21 or total(dealer_hand) >= 21:
      choice = "s"
    else:
      action_state = get_player_action(player_hand, dealer_hand[0])
      choice = action_state[0]
      player_data_lst.append(action_state)
    if choice == "h":
      hit(player_hand)
    elif choice == "s":
      while total(dealer_hand) < 17:
        hit(dealer_hand)
      reward = score(dealer_hand, player_hand)
      choice = "q"
  final_state = (player_hand, dealer_hand)
  return (reward, player_data_lst, final_state)


def interactive_action(player_hand, dealer_hand):
  """ ask the action from the user
  :param player_hand: list of cards from set: {2, 3, 4, ..., 9, 'J', ..., 'A'}
  :param dealer_hand: single card
  :return: (action, <empty>)
  """
  action = input("Do you want to [H]it, [S]tand, or [Q]uit: ").lower()
  assert action in ["s", "h", "q"]
  return (action, ())


if __name__ == "__main__":
  logging.getLogger().setLevel(logging.INFO)
  (reward, player_data_lst, final_state) = game(interactive_action)
  print(f"reward: {reward}")
  print(f"player_data_lst: {player_data_lst}")
  print(f"final_state: {final_state}")