# Sudoku Solver
# By Michal Rajzer
# 9x9 Sudoku

"""
-Make a gui
-let user try and solve it and show the backtracking process
"""

grid = [[0, 0, 0, 0, 0, 0, 2, 3, 4],
        [0, 1, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 8, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 7, 9, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 8, 0]]


def possible(y, x, n):
    global grid
    # Check if number is present in row
    for i in range(9):
        if grid[y][i] == n:
            return False

    # Check if number is present in column
    for i in range(9):
        if grid[i][x] == n:
            return False

    # Check if number is present in the square
    quadrantX = (x // 3) * 3  # Top left of the square x n y
    quadrantY = (y // 3) * 3
    for i in range(3):
        for j in range(3):
            if grid[quadrantY + i][quadrantX + j] == n:
                return False

    return True


def solve():  # Returns True if no empty spaces (If it is solved), False if it cant be solved, then it backtracks and tries other combinations.
    global grid
    for y in range(9):
        for x in range(9):
            if grid[y][x] == 0:
                for n in range(1, 10):
                    if possible(y, x, n):
                        grid[y][x] = n
                        if solve():
                            return True
                        else:
                            grid[y][x] = 0
                return False
    printGrid(grid)
    return True


def printGrid(array):
    for row in array:
        print(row)


if __name__ == '__main__':
    solve()
