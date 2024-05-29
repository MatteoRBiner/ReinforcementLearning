import strategies
import BlackJackAgentV2 as ag
import python_blackjack_simulator as bj
import matplotlib.pyplot as plt

if __name__ == "__main__":
    repetitions = 10000
    total_reward = 0
    agent = ag.BlackJackAgentV2(0.01, 1, 2/repetitions, 0.1)
    agent.train(repetitions)
    action = agent.get_action_final
    reward_list = []
    average_reward = 0
    length_list = []
    average_length = 0
    for i in range(repetitions):
        reward, players_data, _ = bj.game(action, strategies.expected_value_strategy)
        average_reward = (i * average_reward + reward[0]) / (i+1)
        reward_list.append(average_reward)
        average_length = (i * average_length + len(players_data[0])) / (i+1)
        length_list.append(average_length)
        total_reward += reward[0]
    total_reward /= repetitions
    print("Averwage Reward with trained agent: " + str(total_reward))

    fig, axs = plt.subplots(ncols=2, figsize=(12, 5))
    axs[0].set_title("Episode average rewards")
    axs[0].plot(range(len(reward_list)), reward_list)
    axs[1].set_title("Episode average lengths")
    axs[1].plot(range(len(length_list)), length_list)
    plt.tight_layout()
    plt.show()
