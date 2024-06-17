import random


class Game:
    def __init__(self, min_value=0, max_value=6, max_attempts=3):
        self.min_value = min_value
        self.max_value = max_value
        self.max_attempts = max_attempts
        self.target_number = None
        self.attempts_left = None
        self.last_guess = None
        self.higher_lower = None

    def reset(self):
        self.target_number = random.randint(self.min_value, self.max_value)
        self.attempts_left = self.max_attempts
        self.last_guess = -1
        self.higher_lower = None
        state = [self.min_value, self.max_value, self.attempts_left, self.last_guess]
        return state

    def step(self, guess):
        self.attempts_left -= 1
        self.last_guess = guess
        print(str(guess) + " " + str(self.target_number))
        if guess == self.target_number:
            reward = 2  # High reward for correct guess
            done = True
            feedback = 0  # Correct guess
            
        else:
            # Calculate reward based on the distance from the target number
            distance = abs(guess - self.target_number)
            reward = 1 / (distance + 1)  # Smaller distance yields higher reward

            if guess < self.target_number:
                done = False
                feedback = -1  # Too low
            else:
                done = False
                feedback = 1  # Too high

        if self.attempts_left == 0:
            done = True

        return reward, done, feedback

    def render(self):
        pass
        # print(f"Attempts left: {self.attempts_left}")

    def is_done(self):
        return self.attempts_left == 0
