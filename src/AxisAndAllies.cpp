#include "AxisAndAllies.h"
#include <iostream>
#include <sstream>
#include <cstdlib>
#include <cstring>
#include <sys/socket.h>
#include <arpa/inet.h>
#include <unistd.h>
#include <algorithm>
#include <limits>

AxisAndAllies::AxisAndAllies()
{
    resetBoard();
}

void AxisAndAllies::run()
{
    playGame();
}

void AxisAndAllies::resetBoard()
{
    board_occupied.clear();
    board_player.clear();
    board_occupied.resize(3, std::vector<bool>(3, false));
    board_player.resize(3, std::vector<bool>(3, false));
    current_player = true;
}

void AxisAndAllies::printBoard()
{
    // ... (print the board)
}

bool AxisAndAllies::isValidMove(int row, int col)
{
    return !board_occupied[row][col];
}

bool AxisAndAllies::isGameOver()
{
    for (int i = 0; i < 3; ++i)
    {
        bool allOccupied = true;
        bool allSamePlayer = true;
        for (int j = 0; j < 3; ++j)
        {
            allOccupied &= board_occupied[i][j];
            allSamePlayer &= (board_player[i][j] == current_player);
        }
        if (allOccupied && allSamePlayer)
        {
            return true;
        }
    }

    for (int j = 0; j < 3; ++j)
    {
        if (board_occupied[0][j] && board_occupied[1][j] && board_occupied[2][j] &&
            board_player[0][j] == current_player && board_player[1][j] == current_player && board_player[2][j] == current_player)
        {
            return true;
        }
    }

    if (board_occupied[0][0] && board_occupied[1][1] && board_occupied[2][2] &&
        board_player[0][0] == current_player && board_player[1][1] == current_player && board_player[2][2] == current_player)
    {
        return true;
    }
    if (board_occupied[0][2] && board_occupied[1][1] && board_occupied[2][0] &&
        board_player[0][2] == current_player && board_player[1][1] == current_player && board_player[2][0] == current_player)
    {
        return true;
    }

    return false;
}

std::vector<float> AxisAndAllies::getAIModel()
{
    int serverSocket, clientSocket;
    struct sockaddr_in serverAddress, clientAddress;
    char buffer[1024] = {0};

    // Create socket
    if ((serverSocket = socket(AF_INET, SOCK_STREAM, 0)) == 0)
    {
        std::cerr << "Socket creation failed" << std::endl;
        exit(EXIT_FAILURE);
    }

    // Set server address
    serverAddress.sin_family = AF_INET;
    serverAddress.sin_addr.s_addr = INADDR_ANY;
    serverAddress.sin_port = htons(8888);

    // Connect to the server
    if (connect(serverSocket, (struct sockaddr *)&serverAddress, sizeof(serverAddress)) < 0)
    {
        std::cerr << "Connection failed" << std::endl;
        exit(EXIT_FAILURE);
    }

    // Receive the AI model from the server
    int bytesRead = read(serverSocket, buffer, 1024);
    if (bytesRead <= 0)
    {
        std::cerr << "Failed to receive AI model from the server." << std::endl;
        close(serverSocket);
        exit(EXIT_FAILURE);
    }

    close(serverSocket);

    std::string modelStr(buffer, bytesRead);
    std::vector<float> model;
    std::stringstream ss(modelStr);
    std::string value;
    while (std::getline(ss, value, ','))
    {
        model.push_back(std::stof(value));
    }

    return model;
}


std::pair<int, int> AxisAndAllies::getMove()
{
    std::vector<float> model = getAIModel();

    int bestScore = current_player ? std::numeric_limits<int>::min() : std::numeric_limits<int>::max();
    std::pair<int, int> bestMove = {-1, -1};

    for (int i = 0; i < 3; ++i)
    {
        for (int j = 0; j < 3; ++j)
        {
            if (isValidMove(i, j))
            {
                board_occupied[i][j] = true;
                board_player[i][j] = current_player;
                int score = evaluateBoard(model);
                board_occupied[i][j] = false;
                board_player[i][j] = false;

                if (current_player)
                {
                    if (score > bestScore)
                    {
                        bestScore = score;
                        bestMove = {i, j};
                    }
                }
                else
                {
                    if (score < bestScore)
                    {
                        bestScore = score;
                        bestMove = {i, j};
                    }
                }
            }
        }
    }

    return bestMove;
}

int AxisAndAllies::evaluateBoard(const std::vector<float>& model)
{
    std::string boardState = getBoardState();
    std::vector<float> features;
    for (char c : boardState)
    {
        features.push_back(c - '0');
    }

    float score = 0.0f;
    for (size_t i = 0; i < model.size(); ++i)
    {
        score += model[i] * features[i];
    }

    return static_cast<int>(score);
}

int AxisAndAllies::minimax(int depth, bool isMaximizing, int alpha, int beta, const std::vector<float>& model)
{
    if (isGameOver() || depth == 5)
    {
        return evaluateBoard(model);
    }

    if (isMaximizing)
    {
        int bestScore = std::numeric_limits<int>::min();
        for (int i = 0; i < 3; ++i)
        {
            for (int j = 0; j < 3; ++j)
            {
                if (isValidMove(i, j))
                {
                    board_occupied[i][j] = true;
                    board_player[i][j] = current_player;
                    int score = minimax(depth + 1, !isMaximizing, alpha, beta, model);
                    board_occupied[i][j] = false;
                    board_player[i][j] = false;
                    bestScore = std::max(score, bestScore);
                    alpha = std::max(alpha, bestScore);
                    if (beta <= alpha)
                    {
                        break;
                    }
                }
            }
        }
        return bestScore;
    }
    else
    {
        int bestScore = std::numeric_limits<int>::max();
        for (int i = 0; i < 3; ++i)
        {
            for (int j = 0; j < 3; ++j)
            {
                if (isValidMove(i, j))
                {
                    board_occupied[i][j] = true;
                    board_player[i][j] = !current_player;
                    int score = minimax(depth + 1, !isMaximizing, alpha, beta, model);
                    board_occupied[i][j] = false;
                    board_player[i][j] = false;
                    bestScore = std::min(score, bestScore);
                    beta = std::min(beta, bestScore);
                    if (beta <= alpha)
                    {
                        break;
                    }
                }
            }
        }
        return bestScore;
    }
}

void AxisAndAllies::makeMove(int row, int col)
{
    board_occupied[row][col] = true;
    board_player[row][col] = current_player;
}

void AxisAndAllies::playGame()
{
    resetBoard();

    while (!isGameOver())
    {
        printBoard();

        std::pair<int, int> move = getMove();
        makeMove(move.first, move.second);

        std::cout << "Player " << (current_player ? "1" : "2") << " plays: (" << move.first << ", " << move.second << ")" << std::endl;

        current_player = !current_player;
    }

    printBoard();

    int winner = evaluateBoard(getAIModel());
    std::string gameData = getBoardState();
    sendGameState(gameData, winner);

    if (winner > 0)
    {
        std::cout << "Player 1 wins!" << std::endl;
    }
    else if (winner < 0)
    {
        std::cout << "Player 2 wins!" << std::endl;
    }
    else
    {
        std::cout << "Draw!" << std::endl;
    }
}

std::string AxisAndAllies::getBoardState()
{
    std::string boardState;
    for (const auto& row : board_occupied)
    {
        for (bool cell : row)
        {
            boardState += cell ? "1" : "0";
        }
    }
    for (const auto& row : board_player)
    {
        for (bool cell : row)
        {
            boardState += cell ? "1" : "0";
        }
    }
    return boardState;
}

void AxisAndAllies::sendGameState(const std::string& state, int winner)
{
    int serverSocket, clientSocket;
    struct sockaddr_in serverAddress, clientAddress;
    char buffer[1024] = {0};

    // Create socket
    if ((serverSocket = socket(AF_INET, SOCK_STREAM, 0)) == 0)
    {
        std::cerr << "Socket creation failed" << std::endl;
        exit(EXIT_FAILURE);
    }

    // Set server address
    serverAddress.sin_family = AF_INET;
    serverAddress.sin_addr.s_addr = INADDR_ANY;
    serverAddress.sin_port = htons(8888);

    // Connect to the server
    if (connect(serverSocket, (struct sockaddr *)&serverAddress, sizeof(serverAddress)) < 0)
    {
        std::cerr << "Connection failed" << std::endl;
        exit(EXIT_FAILURE);
    }

    // Send the game state and winner to the server
    std::string gameData = state + "," + std::to_string(winner);
    send(serverSocket, gameData.c_str(), gameData.length(), 0);

    close(serverSocket);
}
