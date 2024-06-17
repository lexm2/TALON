import random

class Game:
    def __init__(self, min_value=0, max_value=6, max_attempts=3):
        self.min_value = min_value
        self.max_value = max_value
        self.max_attempts = max_attempts
        self.target_number = None
        self.attempts_left = None

    def reset(self):
        self.target_number = random.randint(self.min_value, self.max_value)
        self.attempts_left = self.max_attempts
        state = [self.min_value, self.attempts_left]  # Initial state
        return state

    def step(self, guess):
        self.attempts_left -= 1
        if guess == self.target_number:
            reward = 1
            done = True
            feedback = 0  # Correct guess
            print("Correct")
        elif guess < self.target_number:
            reward = 0
            done = False
            feedback = -1  # Too low
            print("Low")
        else:
            reward = 0
            done = False
            feedback = 1  # Too high
            print("High")

        if self.attempts_left == 0:
            done = True
            print(f"The number was {self.target_number}.")

        return reward, done, feedback

    def render(self):
        print(f"Attempts left: {self.attempts_left}")

    def is_done(self):
        return self.attempts_left == 0