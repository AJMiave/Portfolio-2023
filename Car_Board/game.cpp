#include "game.h"
// #include "board.cpp"
// #include "helper.cpp"

Game::Game()
{
    // TODO
    this->board = new Board(); //declares new board
    start();
}

Game::~Game() //deletes game contents
{
    // TODO
    delete this->board;
    delete this->player;
}


void Game::start()
{
    //TODO
    std::string userinput = Helper::readInput();
    if(loadBoard()) { // if user quits the code doesnt not continue
        if (initializePlayer()) {
            play();
        }
    }
    
}

bool Game::loadBoard()
{
    //TODO 
    std::string userinput;
    while (userinput != "quit" && userinput != "load 1" && userinput != "load 2" && !std::cin.eof()) { //valid inputs
        std::cout << "At this stage of the program, only two commands are acceptable:" << std::endl //output instructions
                  << "load <g>" << std::endl
                  << "quit" <<std::endl
                  << std::endl;

        userinput = Helper::readInput();
        if (userinput != "quit" && userinput != "load 1" && userinput != "load 2") { //error checking
            Helper::printInvalidInput();
        }
        if (userinput == "load 1") { //loads board
            this->board->load(1);

            return true;
        }
        if (userinput == "load 2") {
            this->board->load(2);

            return true;
        }
    }
    return false; // feel free to revise this line, depending on your implementation.
}

bool Game::initializePlayer()
{
    //TODO
    
    std::string userinput;
    while (userinput != "quit" && !std::cin.eof()) 
    {
        this->board->display(this->player);
        std::cout << std::endl;
        std::cout << "At this stage of the program, only three commands are acceptable:" << std::endl //outputs instructions
                << "load <g>" << std::endl
                << "init <x>,<y>,<direction>" << std::endl
                << "quit" << std::endl 
                << std::endl;
        
        userinput = Helper::readInput();

        if (userinput == "load 1") 
        {
            this->board->load(1);
        }
        if (userinput == "load 2") 
        {
            this->board->load(2);
        }
        
        std::vector<std::string> tokens; //used to store split user input
        std::vector<std::string> contents; //used to store string split by commas , 
        
        Helper::splitString(userinput, tokens, " "); //split by space

        if (tokens.at(0) != "quit" && tokens.at(0) != "init" && tokens.at(0) != "load") //error checking
        {
            Helper::printInvalidInput();
        }

        if (tokens.size() == 2) //checks size 
        {
            Helper::splitString(tokens[1], contents, ","); //splits string by , to collect contents
            int x =0;
            int y =0;

            this->player = new Player(); //declares new eplayer
            bool isdirection = 0; // checks if there is a direction for if statement
            Direction direction = NORTH; //default direction


            if (contents.size() == 3) //checks if contents is the correct size
            {

                if (contents.at(2) != "north" && contents.at(2) != "south" && contents.at(2) != "east" && contents.at(2) != "west") //error checking
                {
                    Helper::printInvalidInput();
                }
                if (contents.at(2) == "north") //fills direction with the users inputted direction
                {
                    direction = NORTH;
                    isdirection = 1; //key to access a different if statement
                }
                if (contents.at(2) == "south") 
                {
                    direction = SOUTH;
                    isdirection = 1;
                }
                if (contents.at(2) == "east") 
                {
                    direction = EAST;
                    isdirection = 1;
                }
                if (contents.at(2) == "west") 
                {
                    direction = WEST;
                    isdirection = 1;
                }
            }

            if (contents.size() == 3 && isdirection == 1) //checks if contents is the right size and if there is a direction
            {
                if (tokens.at(0) == "init") //checks if there is a init
                {
                    if (Helper::isNumber(contents.at(0))) 
                    {
                        x = std::stoi(contents.at(0));
                    }
                    if (Helper::isNumber(contents.at(1))) 
                    {
                        y = std::stoi(contents.at(1));
                    }

                    Position position(x, y); //initliase position
                    if (this->board->placePlayer(position)) //checks if player position is valid
                    {
                        this->player->initialisePlayer(&position, direction); //initializes player
                        return true;
                    }
                }

            }
        }
    }

    return false; // feel free to revise this line.
}

void Game::play()
{
    //TODO
    std::string userinput;
    while (userinput != "quit" && !std::cin.eof()) 
    {
        std::string check;
        check = userinput; //error checking
        if (check != "forward" && check != "f" && check != "turn_left" && check != "l" && check != "turn_right" && check != "r" && check != "quit" && check != "")
        {
            Helper::printInvalidInput();
        }
        
        this->board->display(this->player); //displays board

        std::cout << std::endl; //displays description
        std::cout << "At this stage of the program, only four commands are acceptable:" << std::endl
                << "forward (or f)" << std::endl
                << "turn_left (or l)" << std::endl
                << "turn_right (or r)" << std::endl 
                << "quit" << std::endl 
                << std::endl;

        userinput = Helper::readInput();
        if (userinput == "forward" || userinput == "f") //moves player forward
        {
            PlayerMove result;
            result = this->board->movePlayerForward(this->player);
            if (result == CELL_BLOCKED) 
            {
                std::cout << "Error: cannot move forward because road is blocked" << std::endl;
            }
            if (result == OUTSIDE_BOUNDS) 
            {
                std::cout << "Error: cannot move forward because there is no road" << std::endl;
            }
        }

        if (userinput == "turn_left" || userinput == "l") //turn player left
        {
            this->player->turnDirection(TURN_LEFT);
        }

        if (userinput == "turn_right" || userinput == "r") //turn player right
        {
            this->player->turnDirection(TURN_RIGHT);
        }
 
    }
}


