import socket
import random
import numpy as np

# Initialize the game board
board = np.zeros((3, 3), dtype=int)

# Function to check if a move is valid
def is_valid_move(row, col):
    return board[row][col] == 0

# Function to check if the game is over
def is_game_over():
    # Check rows
    for i in range(3):
        if np.all(board[i] == board[i][0]) and board[i][0] != 0:
            return True

    # Check columns
    for j in range(3):
        if np.all(board[:, j] == board[0][j]) and board[0][j] != 0:
            return True

    # Check diagonals
    if np.all(np.diag(board) == board[0][0]) and board[0][0] != 0:
        return True
    if np.all(np.diag(np.fliplr(board)) == board[0][2]) and board[0][2] != 0:
        return True

    return False

# Function to evaluate the board state
def evaluate_board():
    # Check rows
    for i in range(3):
        if np.all(board[i] == 1):
            return 1
        elif np.all(board[i] == -1):
            return -1

    # Check columns
    for j in range(3):
        if np.all(board[:, j] == 1):
            return 1
        elif np.all(board[:, j] == -1):
            return -1

    # Check diagonals
    if np.all(np.diag(board) == 1) or np.all(np.diag(np.fliplr(board)) == 1):
        return 1
    elif np.all(np.diag(board) == -1) or np.all(np.diag(np.fliplr(board)) == -1):
        return -1

    return 0

# Function to train the AI model
def train(state, winner):
    # Update the AI model based on the game state and winner
    # You can implement your own training logic here
    pass

# Function to get the best move from the AI model
def get_move(state):
    # Use the AI model to predict the best move based on the current game state
    # You can implement your own move prediction logic here
    available_moves = [(i, j) for i in range(3) for j in range(3) if state[i][j] == ' ']
    return random.choice(available_moves)

# Function to handle client connections
def handle_client(client_socket):
    global board

    while True:
        # Receive the board state from the client
        data = client_socket.recv(1024).decode('utf-8')

        if not data:
            break

        if ',' in data:
            # Received game state and winner for training
            state, winner = data.split(',')
            winner = int(winner)
            train(state, winner)
            break
        else:
            # Received board state for move prediction
            board = np.array([list(data[i:i+3]) for i in range(0, 9, 3)])
            board[board == 'X'] = 1
            board[board == 'O'] = -1
            board[board == ' '] = 0

            move = get_move(board)
            client_socket.send(str(move[0] * 3 + move[1]).encode('utf-8'))

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
