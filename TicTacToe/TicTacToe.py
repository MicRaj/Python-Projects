# TicTacToe
# By Michal Rajzer
"""
To Do:
-add validation for place input
"""


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


def check_full(grid):
    for i in grid:
        if i not in ['X', 'O']:
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


def main():
    game_grid = [i for i in range(1, 10)]

    symbols = ['X', 'O']
    symbol = symbols[0]
    win = False

    while win is not True:
        print_grid(game_grid)

        position = int(input("Player " + symbol + " enter : \n"))
        while game_grid[position - 1] in symbols:
            position = int(input())
        game_grid[position - 1] = symbol

        if check_for_win(symbol, game_grid):
            print(symbol + ' Win')
            win = True

        elif check_full(game_grid):
            print("Draw")
            win = True

        if symbol == symbols[0]:
            symbol = symbols[1]
        else:
            symbol = symbols[0]


if __name__ == '__main__':
    main()
