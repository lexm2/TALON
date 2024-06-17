import torch
import numpy as np
import random


class Agent:
    def __init__(self, model, learning_rate, discount_factor, epsilon, device):
        self.model = model
        self.optimizer = torch.optim.Adam(model.parameters(), lr=learning_rate)
        self.discount_factor = discount_factor
        self.epsilon = epsilon
        self.device = device

    def select_action(self, state):
        if random.random() < self.epsilon:
            action = random.randint(state[0], state[1])  # Range of numbers from min_value to max_value
        else:
            # Exploit: select the action with the highest Q-value
            state_tensor = torch.FloatTensor(state).to(self.device)
            q_values = self.model(state_tensor)
            action = torch.argmax(q_values).item()

        return action

    def train(self, state, action, reward, next_state, done, feedback):
        state_tensor = torch.FloatTensor(state).to(self.device)
        next_state_tensor = torch.FloatTensor(next_state).to(self.device)
        feedback_tensor = torch.FloatTensor([feedback]).to(self.device)  # Convert feedback to tensor
        q_values = self.model(state_tensor)
        target_q_values = q_values.clone()

        if done:
            target_q_value = reward
        else:
            next_q_values = self.model(next_state_tensor)
            target_q_value = reward + self.discount_factor * torch.max(next_q_values)

        target_q_values[action - state[0]] = target_q_value  # Adjust index based on min_value

        # Incorporate feedback into the loss calculation
        loss = torch.mean((q_values - target_q_values) ** 2 + feedback_tensor**2)
        self.optimizer.zero_grad()
        loss.backward()
        self.optimizer.step()
