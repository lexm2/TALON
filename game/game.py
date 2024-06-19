import random


class Game:
    def __init__(self, min_value=0, max_value=6, max_attempts=6, num_episodes=10000):
        self.min_value = min_value
        self.max_value = max_value
        self.max_attempts = max_attempts
        self.num_episodes = num_episodes
        self.target_number = None
        self.attempts_left = None
        self.guesses = []
        self.evals = []
        self.last_guess = None
        self.higher_lower = None

    def reset(self):
        self.target_number = random.randint(self.min_value, self.max_value)
        self.attempts_left = self.max_attempts
        self.guesses = [-1] * self.max_attempts
        self.evals = [0] * self.max_attempts
        self.last_guess = -1
        
        state = [
            self.min_value,
            self.max_value,
            self.attempts_left,
            *self.guesses,
            *self.evals,
        ]
        return state

    def step(self, guess):
        self.attempts_left -= 1
        index = self.max_attempts - self.attempts_left - 1
        self.guesses[index] = guess
        

        
        if self.num_episodes < 11:
            print(str(guess) + " " + str(self.target_number))
        if guess == self.target_number:
            reward = 10
            done = True
            feedback = [0]
        else:
            reward = 0
            if guess == self.last_guess:
                reward = -10
                done = True
            if guess < self.target_number:
                done = False
                self.higher_lower = -1
            else:
                done = False
                self.higher_lower = 1
            feedback = [self.higher_lower]

        if self.attempts_left == 0:
            done = True
        
        self.evals[index] = self.higher_lower if self.higher_lower is not None else 0
        self.last_guess = guess
        return reward, done, feedback

    def render(self):
        pass

    def is_done(self):
        return self.attempts_left == 0