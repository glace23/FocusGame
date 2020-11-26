# Author: Scott Li
# Date: 11/24/20
# Description: Assignment Project Portfolio.
#               Creates Focus board game for two players with one set with Red color and
#               the other Green color. On a player's turn, the player can make moves based on the pieces they have on
#               on the grid they want to move. Players can move only one unit horizontally or vertically. Players
#               can have up to 5 pieces in a single grid. If more than 5 pieces, first item gets dequeued, goes to
#               player reserve if player's color or go to player captured if opponents color.
#               Whoever captures all opponents pieces wins the game.

import random

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
        # check if there is any illegal commands
        legality = self._check_move_piece_legal(name, origin, destination, pieces)
        piece_list = []

        if legality is True:
            # add turn if pass checks
            self._turn += 1

            # move pieces out of origin STACK into a temp STACK
            self._move_to_list(self._gameboard[origin], piece_list, pieces)

            # move pieces in temp STACK into destination STACK
            self._move_to_list(piece_list, self._gameboard[destination], pieces)

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

            return 'successfully moved reserve'
        else:
            return legality

    def show_board(self):
        """Prints game board."""
        for i in range(0,6):
            row = ''
            for j in range(0,6):
                row = row + f'{(i,j)}:{self._gameboard[(i,j)]} '
            print(row)

    def show_turn(self, int = 0):
        """Show whose turn is it"""
        # check if method is at beginning or end of call
        if int == 0:
            first = self._odd_turn_player
            second = self._even_turn_player
        elif int == 1:
            first = self._even_turn_player
            second = self._odd_turn_player
        else:
            return False

        # return player
        if self._turn % 2 == 1:
            print(f"It is turn {self._turn + int} and {first}'s turn")
            return first
        elif self._turn % 2 == 0:
            print(f"It is turn {self._turn + int} and {second}'s turn")
            return second

    def get_board_coor(self, coor):
        """Return gameboard coordinate's list"""
        return self._gameboard[coor]


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
    p1 = 'A'
    p2 = 'B'
    game = FocusGame((p1, 'R'), (p2, 'G'))
    win = None
    turn = 1
    with open('FocusGame.txt', 'w') as outfile:
        while win is None:
            i = random.randint(0, 1)
            if game.show_reserve(p1) + game.show_reserve(p2) > 0 and i == 0:
                outfile.write(f'Turn {turn} \n')
                x = random.randint(0, 5)
                y = random.randint(0, 5)
                if turn % 2 == 1:
                    moves = game.reserved_move(p1, (x, y))
                    outfile.write(f' Player{p1}, {(x, y)} ')
                    outfile.write(f' {moves} \n')
                    if moves == 'successfully moved reserve':
                        turn += 1
                    if moves == f'{p1} Wins!':
                        break
                elif turn % 2 == 0:
                    moves = game.reserved_move(p2, (x, y))
                    outfile.write(f' Player{p2}, {(x, y)} ')
                    outfile.write(f' {moves} \n')
                    if moves == 'successfully moved reserve':
                        turn += 1
                    if moves == f'{p2} Wins!':
                        break
            else:
                outfile.write(f'Turn {turn} \n')
                x = random.randint(0, 5)
                y = random.randint(0, 5)
                a = random.randint(-1, 1)
                coor = [x, y]
                rand = random.randint(0, 1)
                coor[rand] += a
                coor = tuple(coor)
                max = len(game.get_board_coor((x, y)))
                if max > 0:
                    pieces = random.randint(1, max)
                else:
                    pieces = 1
                if 0 <= (x+a) <= 5 and 0 <= y + a <= 5:
                    if turn % 2 == 1:
                        moves = move(p1, (x, y), coor, pieces, game, outfile)
                        if moves == 'successfully moved':
                            turn += 1
                        if moves == f'{p1} Wins!':
                            break
                    elif turn % 2 == 0:
                        moves = move(p2, (x, y), coor, pieces, game, outfile)
                        if moves == 'successfully moved':
                            turn += 1
                        if moves == f'{p2} Wins!':
                            break
                else:
                    outfile.write(' Bad input \n')
    outfile.write(' END \n ')
    print('END')
    game.show_board()
    pr1 = game.show_reserve(p1)
    pr2 = game.show_reserve(p2)
    pc1 = game.show_captured(p1)
    pc2 = game.show_captured(p2)
    outfile.write(f'Reserves: P1 {pr1}, P2: {pr2} \n'
                  f'Captured: P1 {pc1}, P2: {pc2} \n'
                  f'Gameboard: {game.show_board()}')


def move(name, ori, dest, pieces, game, outfile):
    result = game.move_piece(name, ori, dest, pieces)
    outfile.write(f' Player{name}, {ori}, {dest}, {pieces} ')
    outfile.write(f' {result} \n')
    print(f'Player{name}, {ori}, {dest}, {pieces}')
    print(result)
    return result


if __name__ == '__main__':
    main()
