from SudokuMainMenu import *


def empty_arr():
    return [[i for i in range(9)] for j in range(9)]


file_name = 'sudoku.txt'

pickle_grids(file_name, [create_spot_grid(empty_arr()) for _ in range(3)])

while True:
    inp = input("=======================\n")
    if inp == "init":
        pickle_grids(file_name, [create_spot_grid(empty_arr()) for _ in range(3)])
    elif inp == "clear":
        f = open(file_name, 'w')
        f. close()
    else:
        break
