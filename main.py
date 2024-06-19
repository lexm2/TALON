import os
import matplotlib.pyplot as plt
from game import Game
from nn import DQN
from rl import Agent
from tqdm import tqdm
from collections import deque
import torch
import argparse
import numpy as np
import multiprocessing

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")


def main():

    game = Game(min_value=0, max_value=6)
    args = parse_args()
    input_size = 3 + 2 * game.max_attempts  # min_value, max_value, attempts_left, guesses, higher_lower
    hidden_sizes = [16, 64, 128]  # BS sizes
    output_size = 7
    learning_rate = 0.002
    discount_factor = 0.99
    epsilon = 0.8
    model = DQN(input_size, hidden_sizes, output_size, device)
    agent = Agent(model, learning_rate, discount_factor, epsilon, device)
    num_episodes = args.episodes
    window_size = int(num_episodes / 100)
    rewards = deque(maxlen=window_size)
    attempts = deque(maxlen=window_size)
    reward_avgs = []
    attempts_avgs = []
    num_processes = multiprocessing.cpu_count()
    pool = multiprocessing.Pool(processes=num_processes)

    if args.write:
        output_file = open("output.txt", "w")
    else:
        output_file = None

    print("Using " + device.type)

    checkpoint_path = "chekcpoint.pt"
    if os.path.exists(checkpoint_path) and not args.overwrite:
        try:
            checkpoint = torch.load(checkpoint_path)
            model.load_state_dict(checkpoint["model_state_dict"])
            print("Loaded model parameters from checkpoint.")
            if args.manual:
                attempts, last_guess, higher_lower = args.manual
                print(agent.select_action([game.max_value, game.max_value, attempts, last_guess, higher_lower]))
                return
        except:
            if args.manual:
                print("Failed to load model, train the model before running the manual mode.")
            else:
                print("Failed to load model parameters from checkpoint. Will overwrite them.")

    progress_bar = tqdm(range(num_episodes), desc="Training Episodes", total=num_episodes)

    for episode in range(num_episodes):
        state = game.reset()
        done = False
        episode_reward = 0

        while not done:
            action = agent.select_action(state)
            reward, done, feedback = game.step(action)
            next_state = np.concatenate(
                ([game.min_value, game.max_value, game.attempts_left], game.guesses, game.evals)
            )
            agent.train(state, action, reward, next_state, done, feedback)
            state = next_state
            episode_reward += reward

        rewards.append(episode_reward)
        attempts.append(game.max_attempts - game.attempts_left)
        progress_bar.update()
        if (episode + 1) % window_size == 0:
            reward_avgs.append(round(sum(rewards) / window_size, ndigits=7))
            attempts_avgs.append(round(sum(attempts) / window_size, ndigits=7))
        if (episode + 1) % args.save == 0 and not num_episodes <= args.save:
            save_model_and_test_inputs(model, checkpoint_path, output_file=output_file)
        # print(f"Episode {episode + 1}: Attempts left = {game.attempts_left}")

    save_model_and_test_inputs(model, checkpoint_path=checkpoint_path, output_file=output_file)

    plot_reward_graph(reward_avgs, attempts_avgs)
    output_file.close()


def save_model_and_test_inputs(model, checkpoint_path, output_file=None):
    torch.save({"model_state_dict": model.state_dict()}, checkpoint_path)
    print("Saved model parameters to checkpoint.")

    if output_file is not None:
        output_file.write("Model Architecture:\n")
        output_file.write(str(model) + "\n")

        test_inputs = [
            [0, 6, 6] + [-1] * 6 + [0] * 6,  # Test input 1
            [0, 6, 4, 3] + [-1] * 5 + [-1] + [0] * 5,  # Test input 2
            [0, 6, 2, 5, 3] + [-1] * 4 + [-1, 1] + [0] * 4,  # Test input 3
        ]

        output_file.write("\nInput Tests:\n")
        for i, test_input in enumerate(test_inputs):
            test_input_tensor = torch.FloatTensor(test_input).to(device)
            output = model(test_input_tensor)
            output_file.write(f"Test Input {i+1}: {test_input}\n")
            output_file.write(f"Output: {output.tolist()}\n")
            output_file.write(f"Expected: {output.tolist()}\n")


def plot_reward_graph(reward_avgs, attempts_avgs):
    fig, ax1 = plt.subplots()

    # Plot reward average on the primary y-axis
    ax1.plot(reward_avgs, color="blue")
    ax1.set_xlabel("Episode")
    ax1.set_ylabel("Reward Average", color="blue")
    ax1.tick_params("y", colors="blue")

    # Create a secondary y-axis
    ax2 = ax1.twinx()

    # Plot attempt average on the secondary y-axis
    ax2.plot(attempts_avgs, color="red")
    ax2.set_ylabel("Attempt Average", color="red")
    ax2.tick_params("y", colors="red")

    plt.title("Reward and Attempt Averages over Episodes")
    plt.tight_layout()
    plt.savefig("reward_attempt_plot.png")
    plt.close()


def parse_args():
    parser = argparse.ArgumentParser(description="Number Guessing Game with Reinforcement Learning")
    parser.add_argument(
        "-e", "--episodes", type=int, default=100000, help="Number of training episodes (default: 100000)"
    )
    parser.add_argument("-s", "--save", type=int, default=10000, help="How often to make saves")
    parser.add_argument(
        "--manual",
        "-m",
        type=int,
        nargs=3,
        metavar=("ATTEMPTS", "LASTGUESS", "HIGHERLOWER"),
        help="Manualy run the neural network with the given parameters",
    )
    parser.add_argument("--write", "-w", action="store_true", help="Write output to a file")
    parser.add_argument("--overwrite", "-o", action="store_true", help="Overwrite the save file")
    return parser.parse_args()


if __name__ == "__main__":
    main()
