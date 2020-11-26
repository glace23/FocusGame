# Author: Scott Li
# Date: 11/24/20
# Description: Assignment Project Portfolio.
#               Creates Focus board game for two players with one set with Red color and
#               the other Green color. On a player's turn, the player can make moves based on the pieces they have on
#               on the grid they want to move. Players can move only one unit horizontally or vertically. Players
#               can have up to 5 pieces in a single grid. If more than 5 pieces, first item gets dequeued, goes to
#               player reserve if player's color or go to player captured if opponents color.
#               Whoever captures all opponents pieces wins the game.

class FocusGame:
    """Creates a Focus Game object."""

    def __init__(self, player1, player2):
        """Initiate variables that help track the game."""
        # initialize attributes
        self._turn = 1
        self._odd_turn_player = None
        self._even_turn_player = None
        self._total_set_piece = 18
        self._stack_height = 5

        # initialize players
        self._p1 = Player(player1)
        self._p2 = Player(player2)

        # initialize board
        self._board = Board(player1, player2)
        self._gameboard = self._board.get_board()

    def move_piece(self, name, origin, destination, pieces):
        """ Moves pieces from origin to destination on game board.

            :Keyword arguments:
            name -- player name
            origin -- original coordinates
            destination -- destination coordinates
            pieces -- number of pieces to move
        """
        # check if there is any illegal commands
        legality = self._check_move_piece_legal(name, origin, destination, pieces)
        piece_list = []

        if legality is True:
            # add turn if pass checks
            self._turn += 1

            # move pieces out of origin STACK into a destination STACK
            self._move_to_list(self._gameboard[origin], self._gameboard[destination], pieces)

            # check if destination list length and take piece if necessary
            self._check_take_piece(name, destination)

            # check win
            if self._check_win(name) is True:
                return f'{name} Wins!'

            return 'successfully moved'
        else:
            return legality

    def show_pieces(self, position):
        """Returns a list of pieces at game board position"""
        return self._gameboard[position]

    def show_reserve(self, name):
        """Returns number of pieces in player's reverse."""
        return len(self._get_player_by_name(name).get_reserve())

    def show_captured(self, name):
        """Returns number of pieces in player's captured."""
        return len(self._get_player_by_name(name).get_captured())

    def reserved_move(self, name, position):
        """Move reserve piece to board."""
        legality = self._check_move_reserve_legal(name, position)
        if legality is True:
            # check if reserve
            if self.show_reserve(name) == 0:
                return 'no pieces in reserve'

            # move turn
            self._turn += 1

            # move reserve to position
            self._move_to_list(self._get_player_by_name(name).get_reserve(), self._gameboard[position], 1)
            # check if position list length and take piece if necessary
            self._check_take_piece(name, position)

            # check win
            if self._check_win(name) is True:
                return f'{name} Wins!'

            return 'successfully moved'
        else:
            return legality

    def show_board(self):
        """Prints game board."""
        self._board.show_board()

    def get_board(self):
        """Return game board."""
        return self._gameboard

    def show_turn(self):
        """Show whose turn is it"""
        # return player
        if self._turn % 2 == 1:
            print(f"It is turn {self._turn} and {self._odd_turn_player}'s turn")
            return self._odd_turn_player
        elif self._turn % 2 == 0:
            print(f"It is turn {self._turn} and {self._even_turn_player}'s turn")
            return self._even_turn_player

    # --------Helper functions--------#

    def _check_player(self, name):
        """Check if player is initialized"""
        if name == self._p1.get_name() or name == self._p2.get_name():
            return True
        return False

    def _check_move(self, origin, destination):
        """Check move is legal or not."""
        # |(X1 - X2)| + |(Y1 - Y2)| = 1 is legal
        moved = abs(origin[0] - destination[0]) + abs(origin[1] - destination[1])
        if moved == 1:
            return True
        return False

    def _check_turn(self, name):
        """Check if is player's turn"""
        if self._turn == 1:
            self._odd_turn_player = name
            # set even player name to other player name
            if self._p1.get_name() == name:
                self._even_turn_player = self._p2.get_name()
            elif self._p1.get_name() != name:
                self._even_turn_player = self._p1.get_name()
            return True
        elif self._turn % 2 == 1 and self._even_turn_player != name:
            return True
        elif self._turn % 2 == 0 and self._odd_turn_player != name:
            return True
        return False

    def _check_pieces(self, name, origin, pieces):
        """Check if pieces are legal"""
        # check if moved pieces smaller than 1 or larger than total piece on origin
        stack = self._gameboard[origin]
        if 1 > pieces or pieces > len(stack):
            return False

        colour = self._get_player_by_name(name).get_color()
        count = 0
        # check if enough player piece in origin stack
        for i in range(0, len(stack)):
            # if last item in list is player color
            if stack[-1 - i] == colour:
                count += 1
                # if enough pieces to move in list
                if pieces == count:
                    return True
            else:
                return False

    def _check_position(self, position):
        """Check if position exists."""
        if self._gameboard.get(position) is not None:
            return True
        return False

    def _check_move_piece_legal(self, name, origin, destination, pieces):
        """Check legality of different conditions."""
        if not self._check_player(name):
            return 'player does not exist'
        if not self._check_turn(name):
            return 'not your turn'
        if not self._check_move(origin, destination):
            return 'invalid location'
        if not self._check_pieces(name, origin, pieces):
            return 'invalid number of pieces'
        return True

    def _check_move_reserve_legal(self, name, position):
        """Check legality of different conditions."""
        if not self._check_player(name):
            return 'player does not exist'
        if not self._check_turn(name):
            return 'not your turn'
        if not self._check_position(position):
            return 'invalid location'
        return True

    def _move_to_list(self, origin_list, destination_list, max_range):
        """ Move item from one list to another.

            :Keyword arguments:
            origin_list -- list to move from
            destination_list -- list to move to
            max_range -- number of times to move items
        """
        for i in range(0, max_range):
            # pop last item in list
            item = origin_list.pop()
            destination_list.append(item)
        return destination_list

    def _check_take_piece(self, name, origin):
        """Checks to take piece or not."""
        if len(self._gameboard[origin]) > self._stack_height:
            for k in range(self._stack_height, len(self._gameboard[origin])):
                # remove first item in list
                item = self._gameboard[origin].pop(0)
                # move to player reserve or captured
                self._take_piece(name, item)
        return False

    def _take_piece(self, name, item):
        """Move piece to reserve or captured."""
        # check player's color
        p = self._get_player_by_name(name)
        if p.get_color() == item:
            # if same color, move to reserve
            p.set_reserve(item)
        elif p.get_color() != item:
            # if different color, move to captured
            p.set_captured(item)

    def _get_player_by_name(self, name):
        """Return player object."""
        if self._p1.get_name() == name:
            return self._p1
        elif self._p2.get_name() == name:
            return self._p2

    def _check_win(self, name):
        """Check if player wins the game."""
        p = self._get_player_by_name(name)
        op = None
        # determine opponent name
        if p == self._odd_turn_player:
            op = self._even_turn_player
        elif p == self._even_turn_player:
            op = self._odd_turn_player

        # player wins by opponent not having movable pieces
        for key in self._gameboard:
            # check if coordinate has piece
            if len(self._gameboard.get(key)) > 0:
                # check if player has all top stack
                if self._gameboard.get(key)[-1] == self._get_player_by_name(p).get_color():
                    # check if opponent has any reserve
                    if self.show_reserve(op) == 0:
                        return True
        return False


class Player:
    """Creates player object."""

    def __init__(self, player):
        # initialize players
        self._name = player[0]
        self._color = player[1]
        self._reserve = []
        self._captured = []

    def get_name(self):
        """Return player name."""
        return self._name

    def get_color(self):
        """Return player's color."""
        return self._color

    def get_reserve(self):
        """Return player's reserve."""
        return self._reserve

    def get_captured(self):
        """Return player's captured."""
        return self._captured

    def set_reserve(self, item):
        """Set player's reserve."""
        self._reserve.append(item)

    def set_captured(self, item):
        """Set player's captured."""
        self._captured.append(item)

    def pop_reserve(self, index=0):
        """Pop player's reserve."""
        return self._reserve.pop(index)

    def pop_captured(self, index):
        """Pop player's captured."""
        return self._captured.pop(index)


class Board:
    """Creates a board object."""

    def __init__(self, player1, player2):
        """Initialize board and board pieces."""
        # initialize player attributes
        self._p1 = Player(player1)
        self._p2 = Player(player2)
        self._p1_color = self._p1.get_color()
        self._p2_color = self._p2.get_color()

        self._board = {
            (0, 0): [self._p1_color], (0, 1): [self._p1_color], (0, 2): [self._p2_color],
            (0, 3): [self._p2_color], (0, 4): [self._p1_color], (0, 5): [self._p1_color],
            (1, 0): [self._p2_color], (1, 1): [self._p2_color], (1, 2): [self._p1_color],
            (1, 3): [self._p1_color], (1, 4): [self._p2_color], (1, 5): [self._p2_color],
            (2, 0): [self._p1_color], (2, 1): [self._p1_color], (2, 2): [self._p2_color],
            (2, 3): [self._p2_color], (2, 4): [self._p1_color], (2, 5): [self._p1_color],
            (3, 0): [self._p2_color], (3, 1): [self._p2_color], (3, 2): [self._p1_color],
            (3, 3): [self._p1_color], (3, 4): [self._p2_color], (3, 5): [self._p2_color],
            (4, 0): [self._p1_color], (4, 1): [self._p1_color], (4, 2): [self._p2_color],
            (4, 3): [self._p2_color], (4, 4): [self._p1_color], (4, 5): [self._p1_color],
            (5, 0): [self._p2_color], (5, 1): [self._p2_color], (5, 2): [self._p1_color],
            (5, 3): [self._p1_color], (5, 4): [self._p2_color], (5, 5): [self._p2_color],
        }

    def get_board(self):
        """Return board."""
        return self._board

    def show_board(self):
        """Prints game board."""
        for i in range(0, 6):
            row = ''
            for j in range(0, 6):
                row = row + f'{(i,j)}:{self._board[(i,j)]} '
            print(row)


def main():
    # initialize focus game
    name_1 = input('What is your name? (Red): ')
    name_2 = input('What is your name? (Green): ')
    if name_1 == '' or name_1.isspace() is True:
        name_1 = 'A'
        print('Oops! Invalid name 1, going default!')
    if name_2 == '' or name_2.isspace() is True:
        name_2 = 'B'
        print('Oops! Invalid name 2, going default!')
    if name_1 == name_2:
        name_1 = 'A'
        name_2 = 'B'
        print('Oops! same name, going default!')

    player_1 = f"Player{name_1.upper()}"
    player_2 = f"Player{name_2.upper()}"
    print(f'Hi {player_1} and {player_2}!')
    game = FocusGame((player_1, 'R'), (player_2, 'G'))

    while True:
        # print game board
        print('Game Board:')
        game.show_board()
        mode = input('What would you like to do? \n'
                     '(move piece/show pieces/show reserve/show captured/reserved move): ')
        game.show_turn()

        # move piece
        if mode.lower() == 'move piece':
            try:
                name = input(f'Please enter player name ({name_1}/{name_2}): ')
                playername = 'Player' + name.upper()

                print('Please enter origin coordinates you are moving from (x, y).')
                origin_x = int(input('x-coordinate: '))
                origin_y = int(input('y-coordinate: '))
                origin = (origin_x, origin_y)
                print(f'Origin: {origin}:{game.show_pieces(origin)}')

                print('Please enter destination coordinates you are moving to (x,y): ')
                destination_x = int(input('x-coordinate: '))
                destination_y = int(input('y-coordinate: '))
                destination = (destination_x, destination_y)
                print(f'Destination: {destination}:{game.show_pieces(destination)}')
                pieces = int(input('Please enter the number of pieces you would like to move: '))

                result = game.move_piece(playername, origin, destination, pieces)
                print(result)
                print(f'Results: {destination}:{game.show_pieces(destination)}')

            except ValueError:
                print('Oops! Incorrect coordinates!')

            finally:
                if prompt() == 'n':
                    return

        # show piece
        elif mode.lower() == 'show pieces':
            try:
                print('Please enter coordinates you want to check (x, y).')
                x = int(input('x-coordinate: '))
                y = int(input('y-coordinate: '))
                coor = (x, y)
                print(f'{coor}:{game.show_pieces(coor)}')

            except ValueError:
                print('Oops! Incorrect coordinates!')

            finally:
                if prompt() == 'n':
                    return

        # show reserve
        elif mode.lower() == 'show reserve':
            name = input(f'Please enter player name ({name_1}/{name_2}) number of reserve: ')
            playername = 'Player' + name.upper()
            print(f"{playername}'s reserve: {game.show_reserve(playername)}")

            if prompt() == 'n':
                return

        # show captured
        elif mode.lower() == 'show captured':
            name = input(f'Please enter player name ({name_1}/{name_2}) number of captured: ')
            playername = 'Player' + name.upper()
            print(f"{playername}'s captured: {game.show_captured(playername)}")

            if prompt() == 'n':
                return

        elif mode.lower() == 'reserved move':
            try:
                name = input(f"Please enter player name ({name_1}/{name_2})'s reserve to board: ")
                playername = 'Player' + name.upper()

                print('Please enter coordinates you want to move to (x, y).')
                x = int(input('x-coordinate: '))
                y = int(input('y-coordinate: '))
                coor = (x, y)
                print(f'{coor}:{game.show_pieces(coor)}')

                results = game.reserved_move(playername, coor)
                print(results)
                print(f'Results: {coor}:{game.show_pieces(coor)}')

            except ValueError:
                print('Oops! Incorrect coordinates!')

            finally:
                if prompt() == 'n':
                    return

        else:
            print('Invalid command!')
            if prompt() == 'n':
                return


def prompt():
    prompt = input('Would you like to continue? (Y/N): ')
    if prompt.lower() == 'n':
        print('Thanks for playing! Have a good day!')
        return 'n'


if __name__ == '__main__':
    main()
