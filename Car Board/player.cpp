#include "player.h"

const std::map<enum Direction, enum Direction> turn_right = { //couldnt figure out how to implement
    { NORTH, EAST },
    { WEST, NORTH },
    { SOUTH, WEST },
    { EAST, SOUTH}
};

const std::map<enum Direction, enum Direction> turn_left = {
    { NORTH, WEST },
    { WEST, SOUTH },
    { SOUTH, EAST },
    { EAST, NORTH}
};

Position::Position()
{
    //TODO
}


Position::Position(int x, int y)
{
    //TODO
    this->x = x;
    this->y = y;
}

Player::Player()
{
    //TODO
    
}

void Player::initialisePlayer(Position* position, Direction direction)
{
    //TODO
    this->position = *position; //initializes player
    this->direction = direction;      
    this->moves = 0;
}

void Player::turnDirection(TurnDirection turnDirection)
{
    //TODO
    if (turnDirection == TURN_RIGHT) //mixed up these direction but they work out in the end
    {
        if (this->direction == NORTH)
        {
            this->direction = WEST;
        }
        else if (this->direction == EAST)
        {
            this->direction = NORTH;
        }
        else if (this->direction == SOUTH)
        {
            this->direction = EAST;
        }
        else if (this->direction == WEST)
        {
            this->direction = SOUTH;
        }
    }

    if (turnDirection == TURN_LEFT) 
    {
        if (this->direction == NORTH)
        {
            this->direction = EAST;
        }
        else if (this->direction == EAST)
        {
            this->direction = SOUTH;
        }
        else if (this->direction == SOUTH)
        {
            this->direction = WEST;
        }
        else if (this->direction == WEST)
        {
            this->direction = NORTH;
        }
    }
}

Position Player::getNextForwardPosition()
{
    //TODO
    Position newPosition; // declares new dummy position
    newPosition.x = this->position.x;
    newPosition.y = this->position.y;
    if (this->direction == NORTH) //checks direction
    {
        newPosition.x = this->position.x - 1; //gets new position and fixes turn directionmix up
    }
    else if (this->direction == SOUTH)
    {
        newPosition.x = this->position.x + 1;
    }
    else if (this->direction == EAST)
    {
        newPosition.y = this->position.y + 1;
    }
    else if (this->direction == WEST)
    {
        newPosition.y = this->position.y - 1;
    }

    return newPosition; // returns new position
}

void Player::updatePosition(Position position) //updates position
{
    //TODO
    this->position.x = position.x;
    this->position.y = position.y;
    this->moves = moves + 1; 

}

void Player::displayDirection() //outputs the players direction onto the board
{
    //TODO
    if (this->direction == NORTH) 
    {
        std::cout << DIRECTION_ARROW_OUTPUT_NORTH;
    }
    if (this->direction == EAST) 
    {
        std::cout << DIRECTION_ARROW_OUTPUT_EAST;
    }
    if (this->direction == SOUTH) 
    {
        std::cout << DIRECTION_ARROW_OUTPUT_SOUTH;
    }
    if (this->direction == WEST) 
    {
        std::cout << DIRECTION_ARROW_OUTPUT_WEST;
    }
}

