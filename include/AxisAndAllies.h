#ifndef AXIS_AND_ALLIES_H
#define AXIS_AND_ALLIES_H

#include <vector>
#include <string>

class AxisAndAllies {
public:
    AxisAndAllies();
    void run();

private:
    std::vector<std::vector<char>> board;
    char currentPlayer;

    void resetBoard();
    void printBoard();
    bool makeMove(int row, int col);
    bool checkWin();
    bool isBoardFull();
    std::string getBoardState();
    int getServerMove();
    void sendGameState(const std::string& state, int winner);
};

#endif