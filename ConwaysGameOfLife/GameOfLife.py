"""
Conways Game Of Life The universe of the Game of Life is an infinite, two-dimensional orthogonal grid of square
cells, each of which is in one of two possible states, alive or dead
The rules of the game are:
    Any live cell with fewer than two live neighbours dies, as if caused by underpopulation.
    Any live cell with more than three live neighbours dies, as if by overcrowding.
    Any live cell with two or three live neighbours lives on to the next generation.
    Any dead cell with exactly three live neighbours becomes a live cell.

 """

import copy
import random


class Culture:
    # Initialises  and creates a 2D array with a specified number of rows and columns
    def __init__(self, row, columns):
        self.row = row
        self.columns = columns
        self.grid = []
        for r in range(row):
            subList = []
            for c in range(columns):
                subList.append(0)
            self.grid.append(subList)

    # Outputs the 2d array in a user-friendly grid form
    def __str__(self):
        string = ""
        for row in self.grid:
            for item in row:
                string += str(item) + "\t"
            string += "\n"
        return string

    # ------------ Creating the grid --------------------
    # Allows the user make a pattern of live cells
    def createManual(self):
        creating = True
        while creating:
            try:
                x = int(input("Input X of live cell"))
                y = int(input("Input y of live cell"))
                if x != "" or y != "":
                    self.grid[y][x] = 1
            except ValueError:
                print("Must be an Integer")
                creating = False
            except IndexError:
                print("Index Out of Range")
                creating = False

    # Creates a random pattern of alive cells
    def createRandom(self):
        for y in range(len(self.grid)):
            for x in range(len(self.grid[0])):
                self.grid[y][x] = random.choice([0, 1])

    # Allows an array to be inputted
    def new(self, cGrid):
        self.grid = cGrid
        self.row = len(cGrid)
        self.columns = len(cGrid[0])

    def clear(self):
        self.grid = []
        for r in range(self.row):
            subList = []
            for c in range(self.columns):
                subList.append(0)
            self.grid.append(subList)

    def rawGrid(self):
        return self.grid


# Create 2D List of the culture
def createGrid(row, columns):
    grid = []
    for i in range(row):
        subList = []
        for j in range(columns):
            subList.append(0)
        grid.append(subList)
    return grid


# Create a function to make a custom culture grid how many rows columns and where to put 1's
def createCulture(grid):
    new = grid
    creating = True
    while creating:
        try:
            x = int(input("Input X of live cell"))
            y = int(input("Input y of live cell"))
            if x != "" or y != "":
                new[y][x] = 1

        except ValueError:
            print("Must be an Integer")
            creating = False
        except IndexError:
            print("Index Out of Range")
            creating = False
    return new


# def write a function to return a list of items around the space
def border(cord, grid):
    x, y = cord
    content = []
    for i in range(-1, 2):
        for j in range(-1, 2):
            if (i, j) != (0, 0):
                if 0 <= (x + j) < len(grid[0]) and 0 <= (y + i) < len(grid):
                    content.append(grid[y + i][x + j])
    return content


# Create function to return how many live neighbours
def countLive(cellList):
    return cellList.count(1)


# Create a function to return new cell state
def cellState(cord, grid):
    state = grid[cord[1]][cord[0]]
    live = countLive(border(cord, grid))
    # Checks
    # fewer than two live neighbours dies
    if live < 2 and state == 1:
        return 0
    # more than three live neighbours dies
    elif live > 3 and state == 1:
        return 0
    # two or three live neighbours lives
    elif 1 < live <= 3 and state == 1:
        return 1
    # dead cell with exactly three live neighbours becomes a live cell.
    elif live == 3 and state == 0:
        return 1
    # All else stays dead
    else:
        return state


# Create a function to print the game ut nicely
def printGrid(grid):
    for row in grid:
        print()
        for item in row:
            print(str(item) + "\t", end="")


# loop through the 2d list and apply the function to each thing in the list to make a new list
def newGrid(grid):
    new = copy.deepcopy(grid)
    for x in range(len(grid[0])):
        for y in range(len(grid)):
            new[y][x] = cellState([x, y], grid)
    return new


# Do the same for the new list
if __name__ == "__main__":
    culture = Culture(4, 4)
    culture.createRandom()
    for i in range(1000):
        print(culture)
        culture.new(newGrid(culture.grid))

