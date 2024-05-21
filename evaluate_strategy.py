import strategies
import BlackJackAgentV1 as ag
import python_blackjack_simulator as bj

"""
define number of repetitions and action
"""
repetitions = 100000

if __name__ == "__main__":
    total_reward = 0
    agent = ag.BlackJackAgentV1(0.01, 0.5, 0.9, 0.001)
    agent.train(1000)
    action = agent.get_action
    for i in range(repetitions):
        reward, _, _ = bj.game(action)
        total_reward += reward
    total_reward /= repetitions
    print("Reward: " + str(total_reward))
