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
        self._set_piece_to_win = 6
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

    def get_board(self):
        """Return game board."""
        return self._board

    def show_turn(self):
        """Show whose turn is it"""
        # return player
        if self._turn % 2 == 1:
            print(f"It is turn {self._turn} and {self._odd_turn_player}'s turn")
            return self._odd_turn_player
        elif self._turn % 2 == 0:
            print(f"It is turn {self._turn} and {self._even_turn_player}'s turn")
            return self._even_turn_player

    def get_set_piece_to_win(self):
        """Returns pieces required to capture to win."""
        return self._set_piece_to_win

    def set_set_piece_to_win(self, num):
        """Sets pieces required to capture to win."""
        self._set_piece_to_win = num

    # --------Helper functions--------#

    def _check_player(self, name):
        """Check if player is initialized"""
        if name == self._p1.get_name() or name == self._p2.get_name():
            return True
        return False

    def _check_move(self, origin, destination, pieces):
        """Check move is legal or not."""
        # |(X1 - X2)| + |(Y1 - Y2)| <= pieces is legal
        # move distance <= pieces moved
        moved = abs(origin[0] - destination[0]) + abs(origin[1] - destination[1])
        if moved == pieces:
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
        # check if enough consecutive player piece in origin stack
        for i in range(0, len(stack)):
            # if last item in list is player color, or the item on top of stack
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
        # if source or destination locations are invalid
        if not self._check_position(origin) or not self._check_position(destination):
            return 'invalid location'
        # if move length != pieces
        if not self._check_move(origin, destination, pieces):
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
        # if total captured = total set piece, player wins
        if len(p.get_captured()) == self._set_piece_to_win:
            return True
        return False

    # def _check_win(self, name):
    #     """Check if player wins the game."""
    #     opponent = None
    #     # determine opponent name
    #     if name == self._odd_turn_player:
    #         opponent = self._even_turn_player
    #     elif name == self._even_turn_player:
    #         opponent = self._odd_turn_player
    #
    #     # player wins by opponent not having movable pieces
    #     for key in self._gameboard:
    #         # check if coordinate has piece
    #         if len(self._gameboard.get(key)) > 0:
    #             # check if player has all top stack
    #             if self._gameboard.get(key)[-1] != self._get_player_by_name(name).get_color():
    #                 return False
    #     # check if opponent has any reserve after looping through all coordinates
    #     if self.show_reserve(opponent) == 0:
    #         return True
    #     else:
    #         return False


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

    def get_coordinates(self, coordinates):
        """Return the list in gameboard coordinate"""
        return self._board[coordinates]


def main():
    game = FocusGame(('PlayerA', 'R'), ('PlayerB', 'G'))
    print(game.move_piece('PlayerA', (0, 0), (0, 1), 1))  # Returns message "successfully moved"
    print(game.show_pieces((0, 1)))  # Returns ['R','R']
    print(game.move_piece('PlayerB', (0, 2), (0, 3), 1))
    print(game.show_pieces((0, 3)))  # Returns ['R','R']
    print(game.move_piece('PlayerA', (0, 1), (0, 3), 2))  # Returns message "successfully moved"
    print(game.show_pieces((0, 3)))
    print(game.show_captured('PlayerA'))  # Returns 0
    print(game.reserved_move('PlayerB', (0, 0)))  # Returns message "No pieces in reserve"
    print(game.show_reserve('PlayerA'))  # Returns 0
    print(game.move_piece('PlayerB',(0,6), (0,5), 1))


if __name__ == '__main__':
    main()