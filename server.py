import socket
import torch
import torch.nn as nn
import torch.optim as optim

# Define the neural network architecture
class Net(nn.Module):
    def __init__(self):
        super(Net, self).__init__()
        self.fc1 = nn.Linear(1, 1)  # Adjust the input size to match the number of features
        self.fc2 = nn.Linear(1, 1)

    def forward(self, x):
        x = torch.relu(self.fc1(x))
        x = self.fc2(x)
        return x

# Initialize the AI model
ai_model = Net()

# Function to train the AI model
def train(game_data, winner):
    data = torch.tensor([float(x) for x in game_data.split(',')], dtype=torch.float32)
    X = data.view(1, -1)  # Reshape the input data to (1, num_features)
    y = torch.tensor([[winner]], dtype=torch.float32)   # Labels

    criterion = nn.MSELoss()
    optimizer = optim.SGD(ai_model.parameters(), lr=0.01)

    # Train
    for _ in range(100):
        optimizer.zero_grad()
        output = ai_model(X)
        loss = criterion(output, y)
        loss.backward()
        optimizer.step()
        
# Function to handle client connections
def handle_client(client_socket):
    try:
        # Send the AI model to the client
        model_data = []
        for param in ai_model.parameters():
            model_data.extend(param.data.numpy().flatten().tolist())
        model_str = ','.join(map(str, model_data))
        client_socket.send(model_str.encode('utf-8'))

        # Receive game data and winner from the client
        data = client_socket.recv(1024).decode('utf-8')
        if not data:
            raise ConnectionResetError("Client closed the connection")
        game_data, winner = data.split(',')
        winner = int(winner)

        # Train the AI model with the received game data and winner
        train(game_data, winner)

    except ConnectionResetError as e:
        print(f"Client connection reset: {e}")
    finally:
        client_socket.close()
        
# Function to run the server
def run_server():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(('localhost', 8888))
    server_socket.listen(1)

    print("Server is listening on port 8888...")

    while True:
        client_socket, address = server_socket.accept()
        print(f"Connected to client: {address}")

        handle_client(client_socket)

if __name__ == '__main__':
    run_server()
