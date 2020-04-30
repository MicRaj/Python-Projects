# Tic Tac Toe - MIni Max
# Lets players input x and y
# Game grid is referred to as "Grid"
# grid variable is global
# grid[y][x]


def createGrid():
    grid = []
    for row in range(3):
        rowAppend = []
        for item in range(3):
            rowAppend.append('_')
        grid.append(rowAppend)
    return grid


def printGrid(grid):
    for row in grid:
        print(row)


def getXY():
    while True:
        try:
            xIn = int(input("Input X: "))
            yIn = int(input("Input Y: "))
            if 0 <= xIn <= 2 and 0 <= yIn <= 2:
                return xIn, yIn
        except ValueError:
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
        if win:
            return True
    # check columns
    for x in range(3):
        win = True
        for y in range(3):
            if grid[y][x] != symbol:
                win = False
                break
        if win:
            return True
    # check diagonals
    win = True
    for xy in range(3):
        if grid[xy][xy] != symbol:
            win = False
            break
    if win:
        return True

    win = True
    for xy in range(3):
        if grid[2 - xy][xy] != symbol:
            win = False
            break
    if win:
        return True
    return False


def checkFull(grid):
    for row in grid:
        for item in row:
            if item == "_":
                return False
    return True


def turn(symbol, grid):
    x, y = getXY()
    while not checkPlace(x, y, grid):
        x, y = getXY()
    placeSymbol(x, y, symbol, grid)


# MiniMax 'X' is Maximiser and 'O' is minimiser
# player = "X"
# opponent = "O"


def evaluate(grid):
    if checkWin("X", grid):
        return 10
    elif checkWin("O", grid):
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

    elif checkFull(grid):  # you could use an else statements
        return 0

    if isMax:  # Maximiser's move - this is the player
        best = -1000
        for y in range(3):
            for x in range(3):
                if grid[y][x] == "_":
                    # Make the Move (this will be reversed)
                    grid[y][x] = player  # player symbol X
                    # Calling MiniMax recursively
                    best = max(best, minimax(grid, depth + 1, not isMax))
                    # Undo the Move
                    grid[y][x] = "_"

    else:  # Minimiser move
        best = 1000
        for y in range(3):
            for x in range(3):
                if grid[y][x] == "_":
                    # Make the Move (this will be reversed)
                    grid[y][x] = opponent  # opponent symbol O
                    # Calling MiniMax recursively
                    best = min(best, minimax(grid, depth + 1, not isMax))
                    # Undo the Move
                    grid[y][x] = "_"
    return best


def findBestMove(grid, symbol):  # For Maximiser
    bestMove = []  # [x,y]
    if symbol == "X":
        isMax = True
        bestVal = -1000

        for y in range(3):
            for x in range(3):
                if grid[y][x] == "_":
                    # Make the Move (this will be reversed)
                    grid[y][x] = symbol  # player symbol X
                    # Calling MiniMax recursively
                    moveVal = minimax(grid, 0, not isMax)
                    # Undo the Move
                    grid[y][x] = "_"
                    if moveVal > bestVal:
                        bestMove = [x, y]
                        bestVal = moveVal

    elif symbol == "O":  # minimiser
        isMax = False
        bestVal = 1000
        for y in range(3):
            for x in range(3):
                if grid[y][x] == "_":
                    # Make the Move (this will be reversed)
                    grid[y][x] = symbol  # player symbol X
                    # Calling MiniMax recursively
                    moveVal = minimax(grid, 0, not isMax)
                    # Undo the Move
                    grid[y][x] = "_"
                    if moveVal < bestVal:
                        bestMove = [x, y]
                        bestVal = moveVal
    return bestMove


# Driver code - shite
player = "X"
opponent = "O"
gameRun = True
board = createGrid()
printGrid(board)

while gameRun:
    # Player Turn
    print("Players Turn")
    turn(player, board)
    printGrid(board)
    if checkWin(player, board):
        print(player, "wins")
        gameRun = False
        break
    elif checkFull(board):
        print("Draw")
        gameRun = False
        break

    # Computer turn
    print("Computers Turn")
    xVar, yVar = findBestMove(board, opponent)
    placeSymbol(xVar, yVar, opponent, board)
    printGrid(board)
    if checkWin(opponent, board):
        print(opponent, "wins")
        gameRun = False
        break
    elif checkFull(board):
        print("Draw")
        gameRun = False
        break

'''
    #computer 1 Turn
        #print("Computers Turn")
    x,y = findBestMove(board,player)
    placeSymbol(x,y,player,board)
    printGrid(board)
    if checkWin(player,board)== True:
        print(player,"wins")
        gameRun = False
        break
    elif checkFull(board) == True:
        print("Draw")
        gameRun = False
        break  
'''
'''
#Testing of minimax
board = [['X', '_', 'O'],  
        ['X', 'O', '_'],  
        ['_', '_', '_']]

print(findBestMove(board,"O"))

#Testing evaluate()
board = [['X', '_', 'O'],  
        ['O', 'O', 'O'],  
        ['_', '_', 'X']]  
       
value = evaluate(board)  
print("The value of this board is", value)         

'''

'''
#2 player game
board = createGrid()
gameRun = True
while gameRun == True:
    for symbol in ["X","O"]:
        turn(symbol,board)
        if checkWin(symbol,board)== True:
            print(symbol,"wins")
            gameRun = False
            break
        elif checkFull(board) == True:
            print("Draw")
            gameRun = False
            break
'''
