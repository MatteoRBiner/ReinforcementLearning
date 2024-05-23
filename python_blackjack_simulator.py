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
import strategies
import BlackJackAgentV1 as ag
#logging.basicConfig(level=logging.INFO)


number_of_decks = 6
number_of_players = 4
# there is either 1 or 0 agents. if there is an agent, then there are (number_of_players - 1) other players at the table
# if there is one agent, then he is Player0
number_of_agents = 1
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
  if total <= 11 and aces > 0:
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


def print_results(dealer_hand, player_hand, name):
  logging.info("The dealer has a " + str(dealer_hand) + " for a total of " + str(total(dealer_hand)))
  logging.info("Player" + name + " has a " + str(player_hand) + " for a total of " + str(total(player_hand)))


def score(dealer_hand, player_hand, name):
  print_results(dealer_hand, player_hand, name)
  if total(player_hand) == 21:
    logging.info("Congratulations! Player" + name + " got a Blackjack!\n")
    return 1.0
  elif total(dealer_hand) == 21:
    logging.info("Sorry, Player" + name +" loses. The dealer got a blackjack.\n")
    return -1.0
  elif total(player_hand) > 21:
    logging.info("Sorry. Player" + name +" busted. Player" + name +" loses.\n")
    return -1.0
  elif total(dealer_hand) > 21:
    logging.info("Dealer busts. Player" + name +" wins!\n")
    return 1.0
  elif total(player_hand) < total(dealer_hand):
    logging.info("Sorry. Player" + name +"s score isn't higher than the dealer. Player" + name +" loses.\n")
    return -1.0
  elif total(player_hand) > total(dealer_hand):
    logging.info("Congratulations. Player" + name +"s score is higher than the dealer. Player" + name +" wins.\n" )
    return 1.0
  else:
    logging.info("A draw.\n")
    return 0.0

def game(action_agent, get_player_action):
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
  players_data =[]
  player_data_lst = []
  #logging.info("WELCOME TO BLACKJACK!\n")
  global deck
  deck = [2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14]*(4*number_of_decks)
  dealer_hand = deal(deck)
  player_hands = []
  for _ in range(number_of_players):
    player_hand = deal(deck)
    player_hands.append(player_hand)
  reward = -2.0

  for i in range(len(player_hands)):
    choice = 0
    player_hand = player_hands[i]
    while choice != "q":
      #logging.info("The dealer is showing a " + str(dealer_hand[0]))
      #logging.info("Player" + str(i) + " has a " + str(player_hand) + " for a total of " + str(total(player_hand)))
      if total(player_hand) >= 21 or total(dealer_hand) >= 21:
        choice = "s"
      else:
        if number_of_agents == 1 and i == 0:
          action_state = action_agent(player_hands, player_hand, dealer_hand[0])
        else:
          action_state = get_player_action(player_hands, player_hand, dealer_hand[0])
        choice = action_state
        player_data_lst.append(action_state)
      if choice == "h":
        hit(player_hand)
        player_hands[i] = player_hand
      elif choice == "s":
        choice = "q"
    players_data.append(player_data_lst)
    player_data_lst = []
  
  rewards = []
  for i in range(len(player_hands)):
    player_hand = player_hands[i]
    while total(dealer_hand) < 17:
      hit(dealer_hand)
    reward = score(dealer_hand, player_hand, str(i))
    rewards.append(reward)
  final_state = (player_hands, dealer_hand)
  return (rewards, players_data, final_state)

def interactive_action(player_hands, player_hand, dealer_hand):
  """ ask the action from the user
  :param player_hand: list of cards from set: {2, 3, 4, ..., 9, 'J', ..., 'A'}
  :param dealer_hand: single card
  :return: (action, <empty>)
  """
  action = input("Do you want to [H]it, [S]tand, or [Q]uit: ").lower()
  assert action in ["s", "h", "q"]
  return (action, ())

agent = ag.BlackJackAgentV1(0.01, 0.5, 0.9, 0.001)
action_agent = agent.get_action

if __name__ == "__main__":
  logging.getLogger().setLevel(logging.INFO)
  (rewards, players_data, final_state) = game(action_agent, strategies.expected_value_strategy)
  for i in range(len(rewards)):
    print(f"player: {str(i)}")
    print(f"reward: {rewards[i]}")
    print(f"player_data_lst: {players_data[i]}")
    print(f"final_state: {final_state[0][i]}\n")
