import random


class Game:
    def __init__(self, min_value=0, max_value=6, max_attempts=6):
        self.min_value = min_value
        self.max_value = max_value
        self.max_attempts = max_attempts
        self.target_number = None
        self.attempts_left = None
        self.guess1 = None
        self.guess1eval = None
        self.guess2 = None
        self.guess2eval = None
        self.guess3 = None
        self.guess3eval = None
        self.guess4 = None
        self.guess4eval = None
        self.guess5 = None
        self.guess5eval = None
        self.guess6 = None
        self.guess6eval = None
        self.last_guess = None

    def reset(self):
        self.target_number = random.randint(self.min_value, self.max_value)
        self.attempts_left = self.max_attempts
        self.guess1 = -1
        self.guess1eval = 0
        self.guess2 = -1
        self.guess2eval = 0
        self.guess3 = -1
        self.guess3eval = 0
        self.guess4 = -1
        self.guess4eval = 0
        self.guess5 = -1
        self.guess5eval = 0
        self.guess6 = -1
        self.guess6eval = 0
        self.last_guess = -1
        
        state = [
            self.min_value,
            self.max_value,
            self.attempts_left,
            self.guess1,
            self.guess1eval,
            self.guess2,
            self.guess2eval,
            self.guess3,
            self.guess3eval,
            self.guess4,
            self.guess4eval,
            self.guess5,
            self.guess5eval,
            self.guess6,
            self.guess6eval,
        ]
        return state

    def step(self, guess):
        higher_lower = 0
        
        self.attempts_left -= 1
        
        if guess == self.target_number:
            # reward = 10 / (self.max_attempts / (self.attempts_left + 1))  # Smaller attempts left yields higher reward
            reward = 10
            done = True
            feedback = [0]
        else:
            distance = abs(guess - self.target_number)
            # reward = 3 / (distance + 1)  # Smaller distance yields higher reward
            reward = 0
            if guess == self.last_guess:
                reward = -10
                done = True
            if guess < self.target_number:
                done = False
                higher_lower = -1
            else:
                done = False
                higher_lower = 1
            feedback = [higher_lower]     
        self.last_guess = guess
            
        if self.attempts_left == 5:
            self.guess1 = guess
            self.guess1eval = higher_lower
        elif self.attempts_left == 4:
            self.guess2 = guess
            self.guess2eval = higher_lower
        elif self.attempts_left == 3:
            self.guess3 = guess
            self.guess3eval = higher_lower
        elif self.attempts_left == 2:
            self.guess4 = guess
            self.guess4eval = higher_lower
        elif self.attempts_left == 1:
            self.guess5 = guess
            self.guess5eval = higher_lower
        elif self.attempts_left == 0:
            self.guess6 = guess
            self.guess6eval = higher_lower
            done = True

        return reward, done, feedback

    def render(self):
        pass
        # print(f"Attempts left: {self.attempts_left}")

    def is_done(self):
        return self.attempts_left == 0
