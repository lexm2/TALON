#ifndef AXIS_AND_ALLIES_H
#define AXIS_AND_ALLIES_H

#include <vector>
#include <string>

class AxisAndAllies
{
public:
    AxisAndAllies();
    void run();

private:
    std::vector<std::vector<bool>> board_occupied;
    std::vector<std::vector<bool>> board_player;
    bool current_player;

    void resetBoard();
    void printBoard();
    bool isValidMove(int row, int col);
    bool isGameOver();
    int evaluateBoard(const std::vector<float> &model);
    std::pair<int, int> getMove();
    int minimax(int depth, bool isMaximizing, int alpha, int beta, const std::vector<float> &model);
    void makeMove(int row, int col);
    void playGame();
    void connectToServer();
    std::vector<float> getAIModel();

    std::string getBoardState();
    void sendGameState(const std::string &state, int winner);
};

#endif
