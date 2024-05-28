import python_blackjack_simulator as bj
import numpy as np
import strategies
from collections import defaultdict

class BlackJackAgentV2:
    def __init__(self,
                 learning_rate: float,
                 initial_epsilon: float,
                 epsilon_decay: float,
                 final_epsilon: float):

        self.q_values = defaultdict(lambda: np.zeros(2))
        self.lr = learning_rate
        self.epsilon = initial_epsilon
        self.epsilon_decay = epsilon_decay
        self.final_epsilon = final_epsilon

    def get_action(self, players_hand, player_hand, dealer_hand):
        other_players_sum = 0
        for hand in players_hand: 
            other_players_sum += bj.total(hand)
        player_sum , used_aces = bj.total(player_hand, True)
        has_ace = 0
        for card in players_hand:
            if card == 'A':
                has_ace += 1

        usable_aces = has_ace - used_aces
        obs = tuple[player_sum, dealer_hand, usable_aces, other_players_sum]

        if np.random.random() < self.epsilon:
            if np.random.random() < 0.5:
                return "h"
            else:
                return "s"
        else:
            action = int(np.argmax(self.q_values[obs]))
            if action == 0:
                return "s"
            else:
                return "h"

    def get_action_final(self, players_hand, player_hand, dealer_hand):
        other_players_sum = 0
        for hand in players_hand: 
            other_players_sum += bj.total(hand)
        player_sum , used_aces = bj.total(player_hand, True)
        has_ace = 0
        for card in players_hand:
            if card == 'A':
                has_ace += 1

        usable_aces = has_ace - used_aces
        obs = tuple[player_sum, dealer_hand, usable_aces, other_players_sum]

        action = int(np.argmax(self.q_values[obs]))
        if action == 0:
            return "s"
        else:
            return "h"

    def decay_epsilon(self):
        self.epsilon = max(self.final_epsilon, self.epsilon - self.epsilon_decay)

    def train(self, repetitions):
        total_reward = 0

        for i in range(repetitions):
            reward, player_data, final_state = bj.game(self.get_action, strategies.expected_value_strategy)
            total_reward += reward[0]
            
            if not(player_data[0] == []):
                counter = 0
                for action in player_data[0]:
                    if action == "s":
                        action_n = 0
                    else:
                        action_n = 1
                    
                    players_hand = final_state[0]
                    player_hand = final_state[0][0][0:(1+counter)]
                    dealer_hand = final_state[1][0]

                    other_players_sum = 0
                    for hand in players_hand: 
                        other_players_sum += bj.total(hand[0:1])
                    player_sum , used_aces = bj.total(player_hand, True)
                    has_ace = 0
                    for card in players_hand:
                        if card == 'A':
                            has_ace += 1

                    usable_aces = has_ace - used_aces
                    obs = tuple[player_sum, dealer_hand, usable_aces, other_players_sum]

                    if action == "s":
                        temporal_difference = (reward[0] - self.q_values[obs][action_n])
                    else:
                        player_hand = final_state[0][0][0:(2+counter)]
                        player_sum , used_aces = bj.total(player_hand, True)
                        has_ace = 0
                        for card in players_hand:
                            if card == 'A':
                                has_ace += 1
                        new_obs = tuple[player_sum, dealer_hand, usable_aces, other_players_sum]
                        temporal_difference = (reward[0] + 0.95 * np.max(self.q_values[new_obs]) - self.q_values[obs][action_n])
                    
                    self.q_values[obs][action_n] = (self.q_values[obs][action_n] + self.lr * temporal_difference)
                    self.decay_epsilon()
                    counter += 1

        print(f"Average reward during training: {total_reward/i}")

if __name__ == "__main__":
    repetitions = 5000
    agent = BlackJackAgentV2(0.01, 1, 2/repetitions, 0.1)
    agent.train(repetitions)
