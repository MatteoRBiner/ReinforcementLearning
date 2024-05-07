from collections import defaultdict
import python_blackjack_simulator as bj
import numpy as np


class BlackJackAgentV1:
    def __init__(self,
                 learning_rate: float,
                 initial_epsilon: float,
                 epsilon_decay: float,
                 final_epsilon: float,
                 discount_factor: float = 0.95):
        self.q_values = np.zeros(420)
        self.lr = learning_rate
        self.epsilon = initial_epsilon
        self.epsilon_decay = epsilon_decay
        self.final_epsilon = final_epsilon
        self.discount_factor = discount_factor
        self.training_error = []

    def get_action(self, player_hand, dealer_hand):
        if np.random.random() < self.epsilon:
            if np.random.random() < 0.5:
                return 'h'
            else:
                return 's'
        else:
            if self.q_values[self.get_index(player_hand, dealer_hand)] > 0.5:
                return 's'
            else:
                return 'h'

    def decay_epsilon(self):
        self.epsilon = max(self.final_epsilon, self.epsilon - self.epsilon_decay)

    def get_index(self, player_hand, dealer_hand):
        player_value = bj.total(player_hand)
        dealer_value = bj.total(dealer_hand)
        has_ace = 0
        for card in player_hand:
            if card == 'A':
                has_ace = 1
        return player_value + 21 * dealer_value + 210 * has_ace
