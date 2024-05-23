import strategies
import BlackJackAgentV1 as ag
import python_blackjack_simulator as bj

"""
define number of repetitions and action
"""
repetitions = 10000

if __name__ == "__main__":
    total_reward = 0
    agent = ag.BlackJackAgentV1(0.01, 0.5, 0.9, 0.001)
    agent.train(repetitions)
    action = agent.get_action
    for i in range(repetitions):
        reward, _, _ = bj.game(action, strategies.expected_value_strategy)
        total_reward += reward[0]
    total_reward /= repetitions
    print("Reward: " + str(total_reward))
