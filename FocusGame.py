# Author: Scott Li
# Date: 11/10/20
# Description: Assignment 7. Creates recursive functions for add, remove, contains, insert and reverse.
#                            Create get_head function.
import queue


class FocusGame:
    """Creates a Focus Game object."""
    def __init__(self, player1, player2):
        """"""
        # initialize players
        self._p1_name = player1[0]
        self._p1_color = player1[1]
        self._p1_reserve = []
        self._p1_capture = []

        self._p2_name = player2[0]
        self._p2_color = player2[1]
        self._p2_reserve = []
        self._p2_capture = []

        # initialize attributes
        self._turn = 0
        self._odd_turn_player = None
        self._even_turn_player = None
        self._total_set_piece = 18

        # initialize board
        self._board = Board()
        self._gameboard = self._board.get_board()

    def get_p1_name(self):
        """Return player 1 name."""
        return self._p1_name

    def get_p2_name(self):
        """Return player 2 name."""
        return self._p2_name

    def get_color(self, name):
        """Return player's color by name."""
        if name == self._p1_name:
            return self._p1_color
        elif name == self._p2_name:
            return self._p2_color

    def get_reserve(self, name):
        """Return player's reserve by name."""
        if name == self._p1_name:
            return self._p1_reserve
        elif name == self._p2_name:
            return self._p2_reserve

    def get_capture(self, name):
        """Return player's capture by name."""
        if name == self._p1_name:
            return self._p1_capture
        elif name == self._p2_name:
            return self._p2_capture

    def set_reserve(self, name, item):
        """Set player's reserve by name."""
        if name == self._p1_name:
            self._p1_reserve.append(item)
        elif name == self._p2_name:
            self._p2_reserve.append(item)

    def set_capture(self, name, item):
        """Set player's capture by name."""
        if name == self._p1_name:
            self._p1_capture.append(item)
        elif name == self._p2_name:
            self._p2_capture.append(item)

    def move_piece(self, player, origin, destination, pieces):
        """"""
        self._turn += 1
        legality = self._check_legal(player, origin, destination, pieces)
        piece_list = []
        if legality is True:
            # move pieces out of origin STACK into a new STACK
            for i in range(0, pieces):
                item = self._gameboard[origin].pop()
                piece_list.append(item)

            # move pieces into destination stack
            for j in range(0, pieces):
                item = piece_list.pop()
                self._gameboard[destination].append(item)

            # if destination list is larger than 5 after move
            if len(self._gameboard[destination]) > 5:
                for k in range(5, len(self._gameboard[destination])):
                    # remove first item in list
                    item = self._gameboard[destination].pop(0)
                    # move to player reserve or captured
                    self._take_piece(player, item)

            # check win
            if self._check_win(player) is True:
                return f'{player} Wins!'

            return 'successfully moved'
        else:
            return legality

    def _check_player(self, player):
        """Check if player is initialized"""
        if player == self._p1_name or player == self._p2_name:
            return True
        return False

    def _check_move(self, origin, destination):
        """Check move is legal or not."""
        # |(X1 - X2)| + |(Y1 - Y2)| = 1 is legal
        moved = abs(origin[0] - destination[0])  + abs(origin[1] - destination[1])
        if moved == 1:
            return True
        return False

    def _check_turn(self, player):
        """Check if is player's turn"""
        if self._turn == 1:
            self._odd_turn_player = player
            return True
        elif self._turn == 2 and self._odd_turn_player != player:
            self._even_turn_player = player
            return True
        elif self._turn % 2 == 1 and self._even_turn_player != player:
            return True
        elif self._turn % 2 == 0 and self._odd_turn_player != player:
            return True
        return False

    def _check_pieces(self, origin, pieces):
        """Check if pieces are legal"""
        # get list size from coordinate
        stacksize = len(self._gameboard[origin])
        if 1 <= pieces <= stacksize:
            return True
        return False

    def _check_legal(self, player, origin, destination, pieces):
        """Check legality of different conditions."""
        if not self._check_player(player):
            return 'player does not exist'
        if not self._check_turn(player):
            return 'not your turn'
        if not self._check_move(origin, destination):
            return 'invalid location'
        if not self._check_pieces(origin, pieces):
            return 'invalid number of pieces'
        return True

    def _take_piece(self, player, item):
        """Move piece to reserve or capture."""
        # check player's color
        if self.get_color(player) == item:
            # if same color, move to reserve
            self.set_reserve(player, item)
        elif self.get_color(player) != item:
            # if different color, move to capture
            self.set_capture(player, item)

    def _check_win(self, player):
        """Check if player wins the game."""
        # if total capture = set piece, player wins
        if len(self.get_capture(player)) == self._total_set_piece:
            return True
        return False



class Board:
    """Creates a board object"""
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
    print(game.move_piece('PlayerA', (0, 0), (1, 0), 1))  # Returns message "successfully moved"
    # game.show_pieces((0, 1))  # Returns ['R','R']
    # game.show_captured('PlayerA')  # Returns 0
    # game.reserved_move('PlayerA', (0, 0))  # Returns message "No pieces in reserve"
    # game.show_reserve('PlayerA')  # Returns 0


if __name__ == '__main__':
    main()
