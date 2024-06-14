#include "AxisAndAllies.h"
#include <iostream>
#include <sstream>
#include <cstdlib>
#include <cstring>
#include <sys/socket.h>
#include <arpa/inet.h>
#include <unistd.h>

Game::Game() : currentPlayer('X') {
    resetBoard();
}

void Game::run() {
    while (true) {
        printBoard();

        if (currentPlayer == 'X') {
            int row, col;
            std::cout << "Enter your move (row column): ";
            std::cin >> row >> col;
            if (!makeMove(row, col)) {
                std::cout << "Invalid move. Try again." << std::endl;
                continue;
            }
        } else {
            int move = getServerMove();
            int row = move / 3;
            int col = move % 3;
            makeMove(row, col);
            std::cout << "Server's move: " << row << " " << col << std::endl;
        }

        if (checkWin()) {
            printBoard();
            std::cout << "Player " << currentPlayer << " wins!" << std::endl;
            sendGameState(getBoardState(), currentPlayer == 'X' ? 1 : -1);
            break;
        }

        if (isBoardFull()) {
            printBoard();
            std::cout << "It's a draw!" << std::endl;
            sendGameState(getBoardState(), 0);
            break;
        }

        currentPlayer = (currentPlayer == 'X') ? 'O' : 'X';
    }
}

void Game::resetBoard() {
    board.clear();
    board.resize(3, std::vector<char>(3, ' '));
}

void Game::printBoard() {
    std::cout << "-------------" << std::endl;
    for (int i = 0; i < 3; ++i) {
        std::cout << "| ";
        for (int j = 0; j < 3; ++j) {
            std::cout << board[i][j] << " | ";
        }
        std::cout << std::endl << "-------------" << std::endl;
    }
}

bool Game::makeMove(int row, int col) {
    if (row < 0 || row >= 3 || col < 0 || col >= 3 || board[row][col] != ' ') {
        return false;
    }
    board[row][col] = currentPlayer;
    return true;
}

bool Game::checkWin() {
    // Check rows
    for (int i = 0; i < 3; ++i) {
        if (board[i][0] != ' ' && board[i][0] == board[i][1] && board[i][1] == board[i][2]) {
            return true;
        }
    }

    // Check columns
    for (int j = 0; j < 3; ++j) {
        if (board[0][j] != ' ' && board[0][j] == board[1][j] && board[1][j] == board[2][j]) {
            return true;
        }
    }

    // Check diagonals
    if (board[0][0] != ' ' && board[0][0] == board[1][1] && board[1][1] == board[2][2]) {
        return true;
    }
    if (board[0][2] != ' ' && board[0][2] == board[1][1] && board[1][1] == board[2][0]) {
        return true;
    }

    return false;
}

bool Game::isBoardFull() {
    for (int i = 0; i < 3; ++i) {
        for (int j = 0; j < 3; ++j) {
            if (board[i][j] == ' ') {
                return false;
            }
        }
    }
    return true;
}

std::string Game::getBoardState() {
    std::ostringstream oss;
    for (int i = 0; i < 3; ++i) {
        for (int j = 0; j < 3; ++j) {
            oss << board[i][j];
        }
    }
    return oss.str();
}

int Game::getServerMove() {
    int serverSocket, clientSocket;
    struct sockaddr_in serverAddress, clientAddress;
    char buffer[1024] = {0};

    // Create socket
    if ((serverSocket = socket(AF_INET, SOCK_STREAM, 0)) == 0) {
        std::cerr << "Socket creation failed" << std::endl;
        exit(EXIT_FAILURE);
    }

    // Set server address
    serverAddress.sin_family = AF_INET;
    serverAddress.sin_addr.s_addr = INADDR_ANY;
    serverAddress.sin_port = htons(8888);

    // Bind socket to the server address
    if (bind(serverSocket, (struct sockaddr*)&serverAddress, sizeof(serverAddress)) < 0) {
        std::cerr << "Binding failed" << std::endl;
        exit(EXIT_FAILURE);
    }

    // Listen for incoming connections
    if (listen(serverSocket, 1) < 0) {
        std::cerr << "Listening failed" << std::endl;
        exit(EXIT_FAILURE);
    }

    int clientAddressLength = sizeof(clientAddress);
    if ((clientSocket = accept(serverSocket, (struct sockaddr*)&clientAddress, (socklen_t*)&clientAddressLength)) < 0) {
        std::cerr << "Accepting connection failed" << std::endl;
        exit(EXIT_FAILURE);
    }

    // Send the current board state to the server
    std::string boardState = getBoardState();
    send(clientSocket, boardState.c_str(), boardState.length(), 0);

    // Receive the move from the server
    int valread = read(clientSocket, buffer, 1024);
    int move = std::stoi(buffer);

    close(clientSocket);
    close(serverSocket);

    return move;
}

void Game::sendGameState(const std::string& state, int winner) {
    int serverSocket, clientSocket;
    struct sockaddr_in serverAddress, clientAddress;
    char buffer[1024] = {0};

    // Create socket
    if ((serverSocket = socket(AF_INET, SOCK_STREAM, 0)) == 0) {
        std::cerr << "Socket creation failed" << std::endl;
        exit(EXIT_FAILURE);
    }

    // Set server address
    serverAddress.sin_family = AF_INET;
    serverAddress.sin_addr.s_addr = INADDR_ANY;
    serverAddress.sin_port = htons(8888);

    // Bind socket to the server address
    if (bind(serverSocket, (struct sockaddr*)&serverAddress, sizeof(serverAddress)) < 0) {
        std::cerr << "Binding failed" << std::endl;
        exit(EXIT_FAILURE);
    }

    // Listen for incoming connections
    if (listen(serverSocket, 1) < 0) {
        std::cerr << "Listening failed" << std::endl;
        exit(EXIT_FAILURE);
    }

    int clientAddressLength = sizeof(clientAddress);
    if ((clientSocket = accept(serverSocket, (struct sockaddr*)&clientAddress, (socklen_t*)&clientAddressLength)) < 0) {
        std::cerr << "Accepting connection failed" << std::endl;
        exit(EXIT_FAILURE);
    }

    // Send the game state and winner to the server
    std::string message = state + "," + std::to_string(winner);
    send(clientSocket, message.c_str(), message.length(), 0);

    close(clientSocket);
    close(serverSocket);
}