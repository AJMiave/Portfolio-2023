#include "game.h"
#include "helper.h"
// #include "game.cpp"

using std::string;

void showStudentInformation(string name, string id, string email){ //didnt see this last min
    // TODO
}

void menu ();
void printStudentInfo();
void howToPlayTheGame();

/**
     * 1. Describe (briefly) the approach you have taken in your implementation.
     * 2. Describe (briefly) any issues you encountered.
     * 3. Describe (briefly) potential improvements of the design of the given start-up code.
     * The approach that i had taken while implmenting this assignment was by using the 2d vector cell 
     * array pointer provided in board.h file to create and store the game. This was done by copying the
     * default boards in board.cpp into the new declared board in the heap. This board allowed me to read 
     * and chage its contents to play the game using objects like player, position, and direction. Some 
     * issues i had encountered was how to use the 2d vector pointer as i didnt fully understand it at the time
     * which lead to segmentation errors. Also i initially had trouble with the method 'getnextforwardposition'
     * as the return value was this->position, this was troublesome as i didnt know that i was able to change 
     * the return object as i thought i had to leave it unmodified.
     */

int main()
{
    /**
     * TODO: here's the main function. You can write the "main menu" loop/code
     * here or you can make separate functions - up to you.
     */
    std::string userinput;
    
    while (userinput != "3" && !std::cin.eof()) //loops the menu
    {
        menu();
        std::cout << std::endl;
        std::cout << "Please enter your choice: ";
        std::cin >> userinput;
        if (userinput == "2") {
            printStudentInfo();
        }    
    
        if (userinput == "1") {
            howToPlayTheGame();
            Game* game = new Game();

            delete game;
        }
    }

    std::cout << "Good bye!\n\n";

    return EXIT_SUCCESS;
}

void menu() { // displays the menu
    std::cout << std::endl;
    std::cout << "Welcome to Car Board" << std::endl;
    std::cout << "--------------------" << std::endl;
    std::cout << "1. Play game" << std::endl;
    std::cout << "2. Show student's information" << std::endl;
    std::cout << "3. Quit" << std::endl; 

}

void printStudentInfo() { // displays student info
    std::cout << std::endl;
    std::cout << "--------------------" << std::endl;
    std::cout << "Name: <Artemius Miave>" << std::endl;
    std::cout << "No: <s3841792>" << std::endl;
    std::cout << "Email: s3841792@student.rmit.edu.au" << std::endl;
    std::cout << "--------------------" << std::endl; 

}

void howToPlayTheGame() { //displays how to play the game
    std::cout << std::endl;
    std::cout << "You can use the following commands to play the game:" << std::endl;
    std::cout << std::endl;
    std::cout << "load <g>" << std::endl;
    std::cout << "   g: the id of the game board to load" << std::endl;
    std::cout << "init <x>,<y>,<direction>" << std::endl; 
    std::cout << "   x: horizontal position of the car on the board (between 0 & 9)" << std::endl;
    std::cout << "   y: vertical position of the car on the board (between 0 & 9)" << std::endl;
    std::cout << "   direction: direction of the car's movement (north, east, south, west)" << std::endl;
    std::cout << "forward (or f)" << std::endl;
    std::cout << "turn_left (or l)" << std::endl; 
    std::cout << "turn_right (or r)" << std::endl; 
    std::cout << "quit" << std::endl; 
}
