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
        self._turn = 0
        self._odd_turn_player = None
        self._even_turn_player = None
        self._total_set_piece = 18

        # initialize players
        self._p1 = Player(player1)
        self._p2 = Player(player2)

        # initialize board
        self._board = Board()
        self._gameboard = self._board.get_board()

    def move_piece(self, name, origin, destination, pieces):
        """ Moves pieces from origin to destination on game board.

            :Keyword arguments:
            name -- player name
            origin -- original coordinates
            destination -- destination coordinates
            pieces -- number of pieces to move
        """
        self._turn += 1
        # check if there is any illegal commands
        legality = self._check_legal(name, origin, destination, pieces)
        piece_list = []

        if legality is True:
            # move pieces out of origin STACK into a temp STACK
            self._move_to_list(self._gameboard[origin], piece_list, pieces)

            # move pieces in temp STACK into destination STACK
            self._move_to_list(piece_list, self._gameboard[destination], pieces)

            # if destination list is larger than 5 after move
            if len(self._gameboard[destination]) > 5:
                for k in range(5, len(self._gameboard[destination])):
                    # remove first item in list
                    item = self._gameboard[destination].pop(0)
                    # move to player reserve or capturedd
                    self._take_piece(name, item)

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
        if self.show_reserve(name) == 0:
            return 'no pieces in reserve'
        item = self._get_player_by_name(name).pop_reserve()
        self._gameboard[position].append(item)
        return

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
            return True
        elif self._turn == 2 and self._odd_turn_player != name:
            self._even_turn_player = name
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

    def _check_legal(self, name, origin, destination, pieces):
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
        """Return player."""
        if self._p1.get_name() == name:
            return self._p1
        elif self._p2.get_name() == name:
            return self._p2

    def _check_win(self, name):
        """Check if player wins the game."""
        p = self._get_player_by_name(name)
        # if total captured = total set piece, player wins
        if len(p.get_captured()) == self._total_set_piece:
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

    def __init__(self):
        """Initialize board and board pieces."""
        self._board = {
            (0, 0): ['R'], (0, 1): ['R'], (0, 2): ['G'], (0, 3): ['G'], (0, 4): ['R'], (0, 5): ['R'],
            (1, 0): ['G'], (1, 1): ['G'], (1, 2): ['R'], (1, 3): ['R'], (1, 4): ['G'], (1, 5): ['G'],
            (2, 0): ['R'], (2, 1): ['R'], (2, 2): ['G'], (2, 3): ['G'], (2, 4): ['R'], (2, 5): ['R'],
            (3, 0): ['G'], (3, 1): ['G'], (3, 2): ['R'], (3, 3): ['R'], (3, 4): ['G'], (3, 5): ['G'],
            (4, 0): ['R'], (4, 1): ['R'], (4, 2): ['G'], (4, 3): ['G'], (4, 4): ['R'], (4, 5): ['R'],
            (5, 0): ['G'], (5, 1): ['G'], (5, 2): ['R'], (5, 3): ['R'], (5, 4): ['G'], (5, 5): ['G'],
        }

    def get_board(self):
        """Return board."""
        return self._board


def main():
    game = FocusGame(('PlayerA', 'R'), ('PlayerB', 'G'))
    while True:
        mode = input('What would you like to do? (Move Piece/Show Piece/Show Reserve/Show Captured): ')
        name = input('Please enter player name (PlayerA/PlayerB): ')
        if mode == 'Move Piece':
            origin = int(input('Please enter origin coordinates you are moving from (x,y): '))
            destination = int(input('Please enter destination coordinates you are moving from (x,y): '))
            pieces = input('Please enter the number of pieces you would like to move: ')
            game.move_piece(name, origin, destination, pieces)

            prompt = input('Would you like to continue? (Y/N): ')
        else:
            print('Thanks for playing! Have a good day!')
            return



    # print(game.move_piece('PlayerA', (0, 0), (0,1), 1))  # Returns message "successfully moved"
    # print(game.show_pieces((0, 1)))  # Returns ['R','R']
    # print(game.show_captured('PlayerA'))  # Returns 0
    # print(game.reserved_move('PlayerA', (0, 0)))  # Returns message "No pieces in reserve"
    # print(game.show_reserve('PlayerA'))  # Returns 0


if __name__ == '__main__':
    main()
