import strategies
import python_blackjack_simulator as bj

"""
define number of repetitions and action
"""
repetitions = 100000
action = strategies.hit_until_17

if __name__ == "__main__":
    total_reward = 0
    for i in range(repetitions):
        reward, _, _ = bj.game(action)
        total_reward += reward
    total_reward /= repetitions
    print("Reward: " + str(total_reward))
