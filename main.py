import os
import matplotlib.pyplot as plt
from game import Game
from nn import DQN
from rl import Agent
from tqdm import tqdm
import torch
import argparse

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")


def main():

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
    args = parser.parse_args()

    input_size = 15  # min_value, max_value, attempts_left, guesses, higher_lower
    hidden_sizes = [16, 64, 16]  # BS sizes
    output_size = 7
    learning_rate = 0.002
    discount_factor = 0.99
    epsilon = 0.8
    num_episodes = args.episodes

    if args.write:
        output_file = open("output.txt", "w")
    else:
        output_file = None

    print("Using " + device.type)
    game = Game(min_value=0, max_value=6)
    model = DQN(input_size, hidden_sizes, output_size, device)
    agent = Agent(model, learning_rate, discount_factor, epsilon, device)

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
                game.guess1,
                game.guess1eval,
                game.guess2,
                game.guess2eval,
                game.guess3,
                game.guess3eval,
                game.guess4,
                game.guess4eval,
                game.guess5,
                game.guess5eval,
                game.guess6,
                game.guess6eval,
            ]
            agent.train(state, action, reward, next_state, done, feedback)
            state = next_state
            episode_reward += reward

        rewards.append(episode_reward)
        progress_bar.update()
        if (episode + 1) % (num_episodes / 100) == 0:
            reward_avgs.append(round(number=sum(rewards) / len(rewards), ndigits=7))
        if (episode + 1) % args.save == 0:
            save_model_and_test_inputs(model, checkpoint_path, output_file=output_file)
        # print(f"Episode {episode + 1}: Attempts left = {game.attempts_left}")

    save_model_and_test_inputs(model, checkpoint_path=checkpoint_path, output_file=output_file)

    plot_reward_graph(reward_avgs)


def save_model_and_test_inputs(model, checkpoint_path, output_file=None):
    torch.save({"model_state_dict": model.state_dict()}, checkpoint_path)
    print("Saved model parameters to checkpoint.")

    if output_file is not None:
        output_file.write("Model Architecture:\n")
        output_file.write(str(model) + "\n")
        output_file.write("\nModel State Dict:\n")
        output_file.write(str(model.state_dict()) + "\n")

        test_inputs = [
            [0, 6, 6, -1, 0, -1, 0, -1, 0, -1, 0, -1, 0, -1, 0],  # Test input 1
            [0, 6, 4, 3, -1, -1, 0, -1, 0, -1, 0, -1, 0, -1, 0],  # Test input 2
            [0, 6, 2, 5, 1, 3, -1, -1, 0, -1, 0, -1, 0, -1, 0],  # Test input 3
        ]

        output_file.write("\nInput Tests:\n")
        for i, test_input in enumerate(test_inputs):
            test_input_tensor = torch.FloatTensor(test_input).to(device)
            output = model(test_input_tensor)
            output_file.write(f"Test Input {i+1}: {test_input}\n")
            output_file.write(f"Output: {output.tolist()}\n")


def plot_reward_graph(reward_avgs):
    plt.plot(reward_avgs)
    plt.xlabel("Episode")
    plt.ylabel("Reward average")
    plt.title("Reward average over Episodes")
    plt.savefig("reward_plot.png")


if __name__ == "__main__":
    main()
