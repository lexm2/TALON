import os
import matplotlib.pyplot as plt
from game import Game
from nn import DQN
from rl import Agent
from tqdm import tqdm
import torch


def main():
    input_size = 4  # min_value, max_value, attempts_left, last_guess
    hidden_sizes = [32]  # BS sizes
    output_size = 7
    learning_rate = 0.001
    discount_factor = 0.99
    epsilon = 0.1
    num_episodes = 100000

    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    print("Using " + device.type)
    game = Game(min_value=0, max_value=6)
    model = DQN(input_size, hidden_sizes, output_size, device)
    agent = Agent(model, learning_rate, discount_factor, epsilon, device)

    checkpoint_path = "chekcpoint.pt"
    if os.path.exists(checkpoint_path):
        try:
            checkpoint = torch.load(checkpoint_path)
            model.load_state_dict(checkpoint["model_state_dict"])
            print("Loaded model parameters from checkpoint.")
        except:
            print("Failed to load model parameters from checkpoint. Will overwrite them.")

    rewards = []
    reward_avgs = []

    progress_bar = tqdm(range(num_episodes), desc="Training Episodes", total=num_episodes)

    for episode in range(num_episodes):
        state = game.reset()
        done = False
        episode_reward = 0

        while not done:
            action = agent.select_action(state)
            reward, done, feedback = game.step(action)
            next_state = [
                game.min_value,
                game.max_value,
                game.attempts_left,
                game.last_guess,
            ]
            agent.train(state, action, reward, next_state, done, feedback)
            state = next_state
            episode_reward += reward

        rewards.append(episode_reward)
        progress_bar.update()
        if (episode + 1) % (num_episodes / 100) == 0:
            reward_avgs.append(round(number=sum(rewards) / len(rewards), ndigits=7))
        # print(f"Episode {episode + 1}: Attempts left = {game.attempts_left}")

    torch.save({"model_state_dict": model.state_dict()}, checkpoint_path)
    print("Saved model parameters to checkpoint.")

    plt.plot(reward_avgs)
    plt.xlabel("Episode")
    plt.ylabel("Reward average")
    plt.title("Reward average over Episodes")
    plt.savefig("reward_plot.png")


if __name__ == "__main__":
    main()
