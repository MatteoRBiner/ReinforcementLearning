from collections import defaultdict
import python_blackjack_simulator as bj
import numpy as np
import strategies


class BlackJackAgentV1:
    def __init__(self,
                 learning_rate: float,
                 initial_epsilon: float,
                 epsilon_decay: float,
                 final_epsilon: float,
                 discount_factor: float = 0.95):
        self.q_values = np.zeros(472)
        self.lr = learning_rate
        self.epsilon = initial_epsilon
        self.epsilon_decay = epsilon_decay
        self.final_epsilon = final_epsilon
        self.discount_factor = discount_factor
        self.training_error = []

    def get_action(self, players_hand, player_hand, dealer_hand):
        if np.random.random() < self.epsilon:
            if np.random.random() < 0.5:
                return "h"
            else:
                return "s"
        else:
            if self.q_values[self.get_index(players_hand, player_hand, dealer_hand)] > -0.007:
                return "s"
            else:
                return "h"

    def decay_epsilon(self):
        self.epsilon = max(self.final_epsilon, self.epsilon * self.epsilon_decay)

    def get_index(self, players_hand, player_hand, dealer_hand):
        other_players_value = 0
        for hand in players_hand: 
            other_players_value += bj.total(hand)
        player_value = bj.total(str(player_hand))
        dealer_value = bj.total(str(dealer_hand))
        has_ace = 0
        if 'A' in str(player_hand):
            has_ace = 1
        return player_value + 21 * (dealer_value-1) + 231 * has_ace

    def train(self, repetitions):
        total_reward = 0
        for i in range(repetitions):
            reward, player_data, final_state = bj.game(self.get_action, strategies.expected_value_strategy)
            total_reward += reward[0]
            if bj.total(final_state[0][0]) > 21:
                self.q_values[self.get_index(final_state[0], final_state[0][0][:len(final_state[0][0])-1], final_state[1][0])] += self.lr*reward[0]
                self.q_values[self.get_index(final_state[0], final_state[0][0][:len(final_state[0][0])-1], final_state[1][0])] /= 2
            else:
                self.q_values[self.get_index(final_state[0], final_state[0][0], final_state[1][0])] += self.lr * reward[0]
                self.q_values[self.get_index(final_state[0], final_state[0][0], final_state[1][0])] /= 2
            self.decay_epsilon()
        print(f"Average reward during training: " + total_reward/i)

repetitions = 10000

if __name__ == "__main__":
    agent = BlackJackAgentV1(0.01, 0.5, 0.9, 0.001)
    agent.train(repetitions)
