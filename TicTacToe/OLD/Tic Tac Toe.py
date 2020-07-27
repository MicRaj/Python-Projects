# Tic Tac Toe
# Lets players input x and y
# Game grid is refered to as "Grid"
# grid variable is global
# grid[y][x]

def createGrid():
    grid = []
    for row in range(3):
        rowappend = []
        for item in range(3):
            rowappend.append('_')
        grid.append(rowappend)
    return grid


def printGrid(grid):
    for row in grid:
        print(row)


def getXY():
    while True:
        try:
            x = int(input("Input X: "))
            y = int(input("Input Y: "))
            if 0 <= x <= 2 and 0 <= y <= 2:
                return x, y
        except TypeError:
            print("Error")


def placeSymbol(x, y, symbol, grid):
    grid[y][x] = symbol


def checkPlace(x, y, grid):
    if grid[y][x] == "_":
        return True
    else:
        return False


def checkWin(symbol, grid):
    # check rows
    for y in range(3):
        win = True
        for x in range(3):
            if grid[y][x] != symbol:
                win = False
                break
        if win == True:
            return True
    # check columns
    for x in range(3):
        win = True
        for y in range(3):
            if grid[y][x] != symbol:
                win = False
                break
        if win == True:
            return True
    # check diagonals
    win = True
    for xy in range(3):
        if grid[xy][xy] != symbol:
            win = False
            break
    if win == True:
        return True

    win = True
    for xy in range(3):
        if grid[2 - xy][xy] != symbol:
            win = False
            break
    if win == True:
        return True

    return False


def checkFull(grid):
    for row in grid:
        for item in row:
            if item == "_":
                return False
    return True


def turn(symbol, grid):
    printGrid(grid)
    x, y = getXY()
    while checkPlace(x, y, grid) == False:
        x, y = getXY()
    placeSymbol(x, y, symbol, grid)


grid = createGrid()
gameRun = True
while gameRun == True:
    for symbol in ["X", "X"]:
        turn(symbol, grid)
        if checkWin(symbol, grid):
            print(symbol, "wins")
            gameRun = False
            break
        elif checkFull(grid):
            print("Draw")
            gameRun = False
            break
