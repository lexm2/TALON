import random


class Game:
    def __init__(self, min_value=0, max_value=6, max_attempts=6, num_episodes=10000):
        self.min_value = min_value
        self.max_value = max_value
        self.max_attempts = max_attempts
        self.num_episodes = num_episodes
        self.target_number = None
        self.attempts_left = None
        self.last_guess = None
        self.higher_lower = None

    def reset(self):
        self.target_number = random.randint(self.min_value, self.max_value)
        self.attempts_left = self.max_attempts
        self.last_guess = None
        self.higher_lower = None
        state = [self.min_value, self.max_value, self.attempts_left]
        return state

    def step(self, guess):
        self.attempts_left -= 1
        self.last_guess = guess
        if (self.num_episodes < 11):
            print(str(guess) + " " + str(self.target_number))
        if guess == self.target_number:
            reward = 10 / (self.max_attempts / (self.attempts_left + 1))  # Smaller attempts left yields higher reward
            done = True
            feedback = [0, 0]

        else:
            # Calculate reward based on the distance from the target number
            distance = abs(guess - self.target_number)
            reward = 3 / (distance + 1)  # Smaller distance yields higher reward
            if (self.last_guess is not None) and (self.last_guess == guess):
                reward = -4  # If the guess is the same as the last guess

            if guess < self.target_number:
                done = False
                feedback = [-1, self.last_guess]
            else:
                done = False
                feedback = [1, self.last_guess]

        if self.attempts_left == 0:
            done = True

        return reward, done, feedback

    def render(self):
        pass
        # print(f"Attempts left: {self.attempts_left}")

    def is_done(self):
        return self.attempts_left == 0
