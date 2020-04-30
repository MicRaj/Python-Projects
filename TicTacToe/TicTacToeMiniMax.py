# MiniMax 'X' is Maximiser and 'O' is minimiser


def check_for_win(sym, grid):
    if (grid[0] == grid[1] == grid[2] == sym or
            grid[3] == grid[4] == grid[5] == sym or
            grid[6] == grid[7] == grid[8] == sym or
            grid[0] == grid[3] == grid[6] == sym or
            grid[1] == grid[4] == grid[7] == sym or
            grid[2] == grid[5] == grid[8] == sym or
            grid[0] == grid[4] == grid[8] == sym or
            grid[2] == grid[4] == grid[6] == sym):
        return True
    else:
        return False


def check_if_full(grid):
    for i in grid:
        if i not in symbols:
            return False
    return True


def print_grid(grid):
    print('\n'
          '       =        =       \n'
          '   {0}   =   {1}    =  {2}  \n'
          '= = = = = = = = = = = =\n'
          '   {3}   =   {4}    =  {5}\n'
          '= = = = = = = = = = = =\n'
          '   {6}   =   {7}    =  {8}\n'
          '       =        =       \n'
          '    '.format(*grid))


def evaluate(grid):
    if check_for_win("X", grid):
        return 10
    elif check_for_win("O", grid):
        return -10
    else:
        return 0  # No winners


def minimax(grid, depth, isMax):
    score = evaluate(grid)
    if score == 10:
        score -= depth
        return score

    elif score == -10:
        score += depth
        return score

    elif check_if_full(grid):  # You could use an else statement
        return 0

    if isMax:  # Maximiser's move - this is the player
        best = -1000
        for i in range(9):
            temp = grid[i]
            if grid[i] not in symbols:
                # Make the Move (this will be reversed)
                grid[i] = player  # player symbol X
                # Calling MiniMax recursively
                best = max(best, minimax(grid, depth + 1, not isMax))
                # Undo the Move
                grid[i] = temp

    else:  # Minimiser move
        best = 1000
        for i in range(9):
            temp = grid[i]
            if grid[i] not in symbols:
                # Make the Move (this will be reversed)
                grid[i] = opponent  # Computer move Y
                # Calling MiniMax recursively
                best = min(best, minimax(grid, depth + 1, not isMax))
                # Undo the Move
                grid[i] = temp
    return best


def findBestMove(sym, grid):
    best_move = 1
    if sym == symbols[0]:  # X For Maximiser
        isMax = True
        best_val = -1000

        for i in range(9):
            temp = grid[i]
            if grid[i] not in symbols:
                # Make the Move (this will be reversed)
                grid[i] = sym
                # Call Minimax
                move_val = minimax(grid, 0, not isMax)
                # Undo the Move
                grid[i] = temp
                if move_val > best_val:
                    best_move = i
                    best_val = move_val

    elif sym == symbols[1]:  # O minimiser
        isMax = False
        best_val = 1000
        for i in range(9):
            temp = grid[i]
            if grid[i] not in symbols:
                # Make the Move (this will be reversed)
                grid[i] = sym
                # Call Minimax
                move_val = minimax(grid, 0, not isMax)
                # Undo the Move
                grid[i] = temp
                if move_val < best_val:
                    best_move = i
                    best_val = move_val
    return best_move


if __name__ == '__main__':

    game_grid = [i for i in range(1, 10)]
    symbols = ['X', 'O']
    symbol = symbols[0]
    player = symbols[0]
    opponent = symbols[1]
    win = False

    print_grid(game_grid)

    while win is not True:
        if symbol == player:
            position = int(input("Player " + symbol + " enter : \n"))
            while game_grid[position - 1] in ['X', 'Y']:
                position = int(input())
            game_grid[position - 1] = symbol

        elif symbol == opponent:
            move = findBestMove(opponent, game_grid)
            game_grid[move] = opponent

        print_grid(game_grid)

        if check_for_win(symbol, game_grid):
            print(symbol + ' Win')
            win = True

        elif check_if_full(game_grid):
            print("Draw")
            win = True

        if symbol == symbols[0]:
            symbol = symbols[1]
        else:
            symbol = symbols[0]
