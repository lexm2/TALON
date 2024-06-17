from game import Game
from nn import DQN
from rl import Agent

def main():
    input_size = 2  # Current guess and attempts left
    hidden_size = 64
    output_size = 7  # Range of numbers from 0 to 6
    learning_rate = 0.001
    discount_factor = 0.99
    epsilon = 0.1
    num_episodes = 1000

    game = Game(min_value=0, max_value=6)
    model = DQN(input_size, hidden_size, output_size)
    agent = Agent(model, learning_rate, discount_factor, epsilon)

    for episode in range(num_episodes):
        state = game.reset()
        done = False

        while not done:
            action = agent.select_action(state)
            reward, done, feedback = game.step(action)
            next_state = [action, game.attempts_left]
            agent.train(state, action, reward, next_state, done, feedback)
            state = next_state

        print(f"Episode {episode + 1}: Attempts left = {game.attempts_left}")

if __name__ == "__main__":
    main()