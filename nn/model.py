import torch
import torch.nn as nn


class DQN(nn.Module):
    def __init__(self, input_size, hidden_sizes, output_size, device):
        super(DQN, self).__init__()
        self.device = device
        self.layers = nn.ModuleList()

        # Input layer
        self.layers.append(nn.Linear(input_size, hidden_sizes[0]))
        self.layers.append(nn.ReLU())

        # Hidden layers
        for i in range(1, len(hidden_sizes)):
            self.layers.append(nn.Linear(hidden_sizes[i - 1], hidden_sizes[i]))
            self.layers.append(nn.ReLU())

        # Output layer
        self.layers.append(nn.Linear(hidden_sizes[-1], output_size))

        self.to(self.device)

    def forward(self, x):
        for layer in self.layers:
            x = layer(x)
        return x
