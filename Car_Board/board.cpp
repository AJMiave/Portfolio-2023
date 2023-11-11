
#include "board.h"
#include <map>

using std::vector;

const vector<vector<Cell>> Board::BOARD_1 =
{
    { BLOCKED, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY },
    { EMPTY, BLOCKED, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, BLOCKED, EMPTY, EMPTY },
    { EMPTY, EMPTY, BLOCKED, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY },
    { EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, BLOCKED, EMPTY, EMPTY },
    { EMPTY, EMPTY, EMPTY, EMPTY, BLOCKED, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY },
    { EMPTY, EMPTY, BLOCKED, EMPTY, EMPTY, BLOCKED, EMPTY, BLOCKED, EMPTY, EMPTY },
    { EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, BLOCKED, EMPTY, EMPTY, EMPTY },
    { EMPTY, EMPTY, BLOCKED, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY },
    { EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY },
    { EMPTY, EMPTY, BLOCKED, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, BLOCKED }
};

const vector<vector<Cell>> Board::BOARD_2 =
{
    { BLOCKED, BLOCKED, BLOCKED, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY },
    { EMPTY, BLOCKED, BLOCKED, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY },
    { EMPTY, BLOCKED, BLOCKED, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY },
    { EMPTY, EMPTY, EMPTY, EMPTY, BLOCKED, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY },
    { EMPTY, EMPTY, EMPTY, EMPTY, BLOCKED, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY },
    { EMPTY, BLOCKED, BLOCKED, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY },
    { EMPTY, EMPTY, EMPTY, EMPTY, BLOCKED, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY },
    { EMPTY, BLOCKED, BLOCKED, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY },
    { EMPTY, BLOCKED, BLOCKED, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY },
    { EMPTY, BLOCKED, BLOCKED, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY }
};

Board::Board()
{
    // TODO

        std::string** array = new std::string*[DEFAULT_BOARD_DIMENSION]; // initialzes 2d array in the heap
    for (int i = 0; i != DEFAULT_BOARD_DIMENSION; i++) {
        array[i] = new std::string[DEFAULT_BOARD_DIMENSION];
    }

    for (int i = 0; i < DEFAULT_BOARD_DIMENSION; i++) { // fills 2d array with EMPTY spaces 
        for (int j = 0; j < DEFAULT_BOARD_DIMENSION; j++) {
            array[i][j] = EMPTY_OUTPUT;
        }
    }

    std::cout << std::endl;

    std::cout << LINE_OUTPUT << EMPTY_OUTPUT << LINE_OUTPUT; // creates the top of the empty board
    for (int i = 0; i < DEFAULT_BOARD_DIMENSION; i++) {
        std::cout << i << LINE_OUTPUT;
    }
    std::cout << std::endl;

    for (int i = 0; i < DEFAULT_BOARD_DIMENSION; i++) { // creates the rest of the empty board
        std::cout << LINE_OUTPUT << i << LINE_OUTPUT;
        for (int j = 0; j < DEFAULT_BOARD_DIMENSION; j++) {
            std::cout << array[i][j] << LINE_OUTPUT;
        }
        std::cout << std::endl;
    }

    for (unsigned i = 0; i < DEFAULT_BOARD_DIMENSION; i++)
    {
        delete[] array[i];
    }
    delete[] array;
}

Board::~Board()
{
    // TODO
    delete this->board;    
    
}

void Board::load(int boardId)
{
    // TODO
    std::cout << std::endl;
    this->board = new vector<vector<Cell>>; //declares new board
    
    if (boardId == 1) //fills board with BOARD_1
    {
        for (unsigned i = 0; i != DEFAULT_BOARD_DIMENSION; i++) {
            this->board->push_back(BOARD_1[i]);
        }
    }
    
    if (boardId == 2) //fills board with BOARD_2
    {
        for (unsigned i = 0; i != DEFAULT_BOARD_DIMENSION; i++) {
            this->board->push_back(BOARD_2[i]);
        }
    }

}

bool Board::placePlayer(Position position)
{
    // TODO
    if (this->board->at(position.x)[position.y] == BLOCKED) //error checking blocked position
    {
        Helper::printInvalidInput();
    }
    else if (position.x > DEFAULT_BOARD_DIMENSION || position.y > DEFAULT_BOARD_DIMENSION) // error checking out of bounds
    {
        Helper::printInvalidInput();
    }
    else
    {
        this->board->at(position.x)[position.y] = PLAYER; //places player into board
        return true;
    }
    return false; // feel free to revise this line, depending on your implementation.
}

PlayerMove Board::movePlayerForward(Player* player)
{
    // TODO
    Position nxtPosition; //declares new position for the next position

    nxtPosition = player->getNextForwardPosition(); // stores the next postion forward

    
    if (nxtPosition.x >= 10 || nxtPosition.y >= 10 || nxtPosition.x < 0 || nxtPosition.y < 0) // error checking out of bounds
    {
        return OUTSIDE_BOUNDS;
    }
    else if (this->board->at(nxtPosition.x)[nxtPosition.y] == BLOCKED) //error checking blocked
    {
        return CELL_BLOCKED;
    }
    else 
    {
        this->board->at(player->position.x)[player->position.y] = EMPTY; //replaces old position with empty on the board
        this->board->at(nxtPosition.x)[nxtPosition.y] = PLAYER; //replaces new position with player on the board 
        player->updatePosition(nxtPosition); //updates position in the player object
    }
    return PLAYER_MOVED;
}

void Board::display(Player* player)
{
    // TODO
    std::cout << LINE_OUTPUT << EMPTY_OUTPUT << LINE_OUTPUT; // creates the top of the empty board
    for (int i = 0; i < DEFAULT_BOARD_DIMENSION; i++) 
    {
        std::cout << i << LINE_OUTPUT;
    }
    std::cout << std::endl;

    for (int i = 0; i < DEFAULT_BOARD_DIMENSION; i++) // output the rest of the board 
    { 
        std::cout << LINE_OUTPUT << i << LINE_OUTPUT;
        for (unsigned j = 0; j < DEFAULT_BOARD_DIMENSION; j++) {
            if (this->board->at(i)[j] == EMPTY) //outputs a empty space
            {
                std::cout << EMPTY_OUTPUT << LINE_OUTPUT;
            }
            if (this->board->at(i)[j] == BLOCKED) //outputs a blocked path
            {
                std::cout << BLOCKED_OUTPUT << LINE_OUTPUT;
            } 
            if (this->board->at(i)[j] == PLAYER) //outputs the player and the direction
            {
                player->displayDirection();
                std::cout << LINE_OUTPUT;
            } 
        }
        std::cout << std::endl;
    }
}





