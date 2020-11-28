import random
import FocusGame


def interactive():
    """A user input interactive focus game"""
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
    game = FocusGame.FocusGame((player_1, 'R'), (player_2, 'G'))

    while True:
        # print game board
        print('Game Board:')
        game.get_board().show_board()
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
    """Generates a prompt, and act depending on input."""
    prompt = input('Would you like to continue? (Y/N): ')
    if prompt.lower() == 'n':
        print('Thanks for playing! Have a good day!')
        return 'n'


# --------------------------------------------------------#


def randgame():
    """Generates a random focus game."""
    p1 = 'A'
    p2 = 'B'
    game = FocusGame.FocusGame((p1, 'R'), (p2, 'G'))
    win = None
    turn = 1
    with open('FocusGame.txt', 'w') as outfile:
        while win is None:
            # generate random coordinates
            x = random.randint(0, 5)
            y = random.randint(0, 5)

            # get max pieces in (x,y)
            max = len(game.get_board().get_coordinates((x, y)))
            if max > 0:
                pieces = random.randint(1, max)
            else:
                pieces = 1

            # generate random coordinates to move to (x, y +- max)
            a = random.randint(-max, max)
            # add 1 random to x or y
            coor = [x, y]
            for z in range(0, a):
                rand = random.randint(0, 1)
                coor[rand] += 1
            coor = tuple(coor)

            # if (x,y) has elements in list and 0 <= x, y <= 5
            if len(game.get_board().get_coordinates((x, y))) > 0 and 0 <= coor[0] <= 5 and 0 <= coor[1] <= 5:
                # odd turn
                if turn % 2 == 1:
                    moves = move(p1, (x, y), coor, pieces, game, outfile)
                    if moves == 'successfully moved':
                        turn += 1
                    if moves == f'{p1} Wins!':
                        prints(p1, p2, turn, game, outfile)
                        return
                # even turn
                elif turn % 2 == 0:
                    moves = move(p2, (x, y), coor, pieces, game, outfile)
                    if moves == 'successfully moved':
                        turn += 1
                    if moves == f'{p2} Wins!':
                        prints(p1, p2, turn, game, outfile)
                        return
            # move reserve when reserve is not empty
            if game.show_reserve(p1) != 0 or game.show_reserve(p2) != 0:
                x = random.randint(0, 5)
                y = random.randint(0, 5)
                # odd turn
                if turn % 2 == 1:
                    moves = game.reserved_move(p1, (x, y))
                    if moves == 'successfully moved':
                        outfile.write(f"game.reserved_move('Player{p1}', {(x, y)}) \n")
                        turn += 1
                    if moves == f'{p1} Wins!':
                        prints(p1, p2, turn, game, outfile)
                        return
                # even turn
                elif turn % 2 == 0:
                    moves = game.reserved_move(p2, (x, y))
                    if moves == 'successfully moved':
                        outfile.write(f"game.reserved_move('Player{p2}', {(x, y)}) \n")
                        turn += 1
                    if moves == f'{p2} Wins!':
                        prints(p1, p2, turn, game, outfile)
                        return

            # # get remaining pieces
            # p1_pieces = 18 - game.show_reserve(p1) - game.show_captured(p2)
            # p2_pieces = 18 - game.show_reserve(p2) - game.show_captured(p1)
            # # if one set has less than 5 piece, declare a winner or tie
            # if p1_pieces < 5 or p2_pieces < 5:
            #     prints(p1, p2, turn, game, outfile)
            #     if p1_pieces > p2_pieces:
            #         outfile.write(f'{p1} Wins')
            #     elif p1_pieces < p2_pieces:
            #         outfile.write(f'{p2} Wins')
            #     else:
            #         outfile.write(f'TIE!')
            #     return


def prints(p1, p2, turn, game, outfile):
    """Prints end game statements."""
    outfile.write(' END \n ')
    print('END')
    pr1 = game.show_reserve(p1)
    pr2 = game.show_reserve(p2)
    pc1 = game.show_captured(p1)
    pc2 = game.show_captured(p2)
    outfile.write(f'Turn {turn} \n')
    outfile.write(f'Reserves: P1 {pr1}, P2: {pr2} \n'
                  f'Captured: P1 {pc1}, P2: {pc2} \n'
                  f'Gameboard: {game.get_board().show_board()} \n')


def move(name, ori, dest, pieces, game, outfile):
    """Return moved pieces result and write to outfile."""
    result = game.move_piece(name, ori, dest, pieces)
    if result == 'successfully moved':
        outfile.write(f"game.move_piece('Player{name}', {ori}, {dest}, {pieces}) \n")
    print(f'Player{name}, {ori}, {dest}, {pieces}')
    print(result)
    return result


def main():
    pick = input('interactive or random?')
    if pick == 'interactive':
        interactive()
    elif pick == 'random':
        randgame()


if __name__ == '__main__':
    main()
