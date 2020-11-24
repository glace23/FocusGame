# portfolio-project

Write a class named FocusGame for playing an abstract board game called Focus/Domination. You can see the rules [here](https://en.wikipedia.org/wiki/Focus_(board_game)).

Write your code for two-player version of the game.

The board looks like a checkerboard with three squares in each corner removed, hence forming 6X6 board with 1X4 extension on each side (You can find the picture of the board [here](https://en.wikipedia.org/wiki/Focus_(board_game))). Note that for the purpose of this project, we are not considering the 1X4 extensions on each side. In a two player game, the Green and Red pieces are placed, as shown in the figure in the [link](https://en.wikipedia.org/wiki/File:Focus_01.svg). 

Any player can start the game. 
#### Playing the game:
On a player’s turn they will make one move. They can either make a single move, a multiple move, or a reserve move.
###### Single Move
In a single move the player moves one of their playing pieces which is on a space by itself. This piece can be moved one space vertically or horizontally. The piece may never be moved diagonally. The piece can either be moved to an empty space, or a space with one or more playing pieces on it. If a piece is moved to a space with a stack of pieces on it, the piece that was just moved is placed on the top of the stack. A player can move their playing piece onto a stack containing their own pieces, pieces of other players, or both.
###### Multiple Move
In a multiple move a player can move a whole stack of pieces. A player may only move a stack if their pawn is on top of the stack. When a player wants to move a stack they choose how much of the stack that they want to move. They can either move the entire stack or take some pieces off the top of the stack and leave some of the playing pieces behind. The player will then be able to move the stack a number of spaces up to the height of the stack they are moving, so for example if the player has 3 pieces in stack they can move that stack 3 spaces. They can move the stack vertically or horizontally but not diagonally. When moving a stack it will only impact the pieces on the space that that stack lands on and won’t impact the pieces on the spaces that the stack was moved through.
###### Reserving and Capturing Pieces
After moving your playing piece/stack you need to check the height of the stack that you moved the piece(s) to. If the new stack ever contains more than five pieces some of the pieces will be removed from the stack. Starting with the playing piece on the bottom of the stack, you will remove pieces until the stack only has five pieces remaining.
The pieces that were removed from the board will either be captured or put into reserve. All pieces not belonging to the player who made the move are captured. These pieces are removed and won’t be used for the rest of the game. Pieces belonging to the player who made the move will be added to their reserve pile.
###### Reserve Move (Can be done by only the player who has reserved pieces)
If a player has playing pieces in reserve they can make a reserve move instead of a single or multiple move. To make a reserve move take one of your playing pieces in reserve and place it on any space on the gameboard. The reserve piece can be placed on an empty space, on a space containing one piece, or a space containing multiple pieces. Placing the reserve piece counts as your turn as you don’t get to move the piece you just added to the gameboard.
###### End of the Game
The first player who captures six pieces of the other player wins the game.

This [YouTube link](https://www.youtube.com/watch?v=DVRVQM9lo9E) explains how to play the game

Tip: Probably the easiest way of representing the board is to use a list of lists.
You're not required to print the board.

Your `FocusGame` class must include the following methods:
- An `init` method that takes as its parameters two tuples, each containing player name and color of the piece that player is playing (ex: ('PlayerA', 'R'), ('PlayerB','R')) and it intializes the board with the pieces placed in the correct positions. The board positions start with (0,0) and end at (5,5). The top left corner position being (0,0) and bottom right corner position being (5,5). In (0,0) the first 0 represents row and second 0 represents column. Note, we are not considering the 1X4 extensions on each side. The pieces are marked as R and G for Red and Green respectively -- this is case insensitive.
- A method named `move_piece` takes following parameters in order: the player name who is making the move, a tuple that represents the coordinate from where the move is being made, another tuple that represents the location to where the move is being made, an integer that represents the number of pieces that are being moved.
  - It returns an error or proper message:
    - if a player is trying to make a move out of turn, return 'not your turn'
    - if the player provides invalid locations (source or destination), return 'invalid location'
    - if the player is trying to move invalid number of pieces, return 'invalid number of pieces'
   - It returns 'successfully moved' message if the move was successful
   - If the move makes the player win, it returns `<player name> Wins` message (e.g. "PlayerB Wins")
   - If the number of pieces at the moved location are more than 5 in number, then it automatically captures bottom pieces if they belong to other player and moves to current players reserve if the pieces belong to current player.
- A method named `show_pieces` takes a position on the board and returns a list showing the pieces that are present at that location with the bottom-most pieces at the 0th index of the array and other pieces on it in the order. 
- A method named `show_reserve` takes the player name as the parameter and shows the count of pieces that are in reserve for the player. If no pieces are in reserve, return 0.
- A method named `show_captured` takes the player name as the parameter and shows the number of pieces captured by that player. If no pieces have been captured, return 0.
- A method named `reserved_move` takes the player name and the location on the board as the parameters. It places the piece from the reserve to the location. It should reduce the reserve pieces of that player by one and make appropriate adjustments to pieces at the location. If there are no pieces in reserve, return 'no pieces in reserve'

Case won't matter for all the messages that your methods return.

Feel free to add whatever other classes, methods, or data members you want. All data members must be private. All methods must have no more than 20-25 lines of code - don't try to get around this by making really long or complicated lines of code. (The rule in real life is just to not stuff too much into a single function, but that's probably too nebulous a rule for you at this point, and if your function is over 25 lines, you probably are trying to stuff too much into it.)


Here's a very simple example of how your `FocusGame` class could be used by the autograder or a TA:
```
game = FocusGame(('PlayerA', 'R'), ('PlayerB','G'))
game.move_piece('PlayerA',(0,0), (0,1), 1)  #Returns message "successfully moved"
game.show_pieces((0,1)) #Returns ['R','R']
game.show_captured('PlayerA') # Returns 0
game.reserved_move('PlayerA', (0,0)) # Returns message "No pieces in reserve"
game.show_reserve('PlayerA') # Returns 0
```

The file must be named: **FocusGame.py**
