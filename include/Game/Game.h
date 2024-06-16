#ifndef GAME_H
#define GAME_H

#include <vector>

class Game
{
public:
    bool over;
    Game(int size);
    std::vector<int> getState() const;
    void makeMove(int move);
    bool isGameOver() const;
    int getWinner() const;
    int getCurrentPlayer() const;

private:
    std::vector<int> board;
    int currentPlayer;
};

#endif